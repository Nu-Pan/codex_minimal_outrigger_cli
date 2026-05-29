"""Codex CLI 呼び出しの共通処理。"""

import json
import re
import subprocess
import tempfile
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from time import perf_counter
from typing import NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .errors import CmocError
from .repo import (
    filter_oracle_file_paths,
    git_name_only_paths,
    git_name_status_entries,
    git_status_paths,
    run_git,
)
from .subcommand_log import add_quota_wait
from .subcommand_log import log_event
from .timing import format_duration
from .timestamps import make_timestamp

_DEFAULT_MODEL = "gpt-5.5"
_DEFAULT_REASONING_EFFORT = "medium"
FRONTIER_MODEL = _DEFAULT_MODEL
FRONTIER_REASONING_EFFORT = _DEFAULT_REASONING_EFFORT
FRONTIER_HIGH_REASONING_EFFORT = "high"
COST_PERFORMANCE_MODEL = "gpt-5.4-mini"
COST_PERFORMANCE_REASONING_EFFORT = "medium"
COMMIT_MESSAGE_MODEL = COST_PERFORMANCE_MODEL
COMMIT_MESSAGE_REASONING_EFFORT = "low"
INDEX_GENERATION_MODEL = COST_PERFORMANCE_MODEL
INDEX_GENERATION_REASONING_EFFORT = COST_PERFORMANCE_REASONING_EFFORT
_POLL_MODEL = COST_PERFORMANCE_MODEL
_POLL_REASONING_EFFORT = "low"
_QUOTA_POLL_INTERVAL_SECONDS = 30 * 60
_CAPACITY_MESSAGE = "Selected model is at capacity"
_QUOTA_MESSAGES = (
    "Quota exceeded",
    "You've hit your usage limit",
    "out of credits",
    "You hit your spend cap",
)
_CAPACITY_RETRY_LIMIT = 8
_CAPACITY_INITIAL_RETRY_DELAY_SECONDS = 5
_FORBIDDEN_REASONING_EFFORTS = {"xhigh"}
_CODEX_TEXT_ENCODING = "utf-8"
_CODEX_TEXT_ERRORS = "replace"


@dataclass(frozen=True)
class _CodexCommandRun:
    """1 回の `codex exec` 起動結果と対応する成果物 path。"""

    result: subprocess.CompletedProcess[str]
    log_path: Path
    last_message_path: Path
    command: list[str]


@dataclass(frozen=True)
class _OracleGuardSnapshot:
    """workspace-write Codex 実行前の oracle 保護検査用 snapshot。"""

    enabled: bool
    head_commit: str | None
    head_reflog_entry_count: int | None = None
    allowed_uncommitted_paths: tuple[str, ...] = ()


def run_codex_exec(
    repo_root: Path,
    prompt: str,
    *,
    purpose: str = "codex exec",
    read_only: bool,
    expect_json: bool = False,
    output_schema: dict[str, object] | None = None,
    json_validator: Callable[[object], None] | None = None,
    text_validator: Callable[[str], None] | None = None,
    skip_index_maintenance: bool = False,
    index_excluded_roots: Iterable[Path | str] | None = None,
    allowed_uncommitted_oracle_paths: Iterable[Path | str] | None = None,
    model: str = _DEFAULT_MODEL,
    reasoning_effort: str = _DEFAULT_REASONING_EFFORT,
) -> str:
    """`codex exec` を実行し、フルログを `.cmoc/logs/codex_exec` に保存する。"""
    # Structured Output を要求する呼び出しは schema ファイルを必須にする。
    if expect_json and output_schema is None:
        raise ValueError("expect_json=True requires output_schema.")
    validates_structured_output = output_schema is not None
    _validate_model_options(model, reasoning_effort)
    if output_schema is not None:
        _validate_output_schema(output_schema)
    normalized_index_excluded_roots = (
        tuple(index_excluded_roots)
        if index_excluded_roots is not None
        else None
    )

    # 必要なら output schema ファイルを準備する。call log と last message は実行単位で払い出す。
    base_command = _build_codex_command(
        read_only=read_only,
        model=model,
        reasoning_effort=reasoning_effort,
    )
    _preflight_workspace_write_oracle_guard(repo_root, base_command)
    schema_path = _write_output_schema(repo_root, output_schema)
    if schema_path is not None:
        base_command.extend(["--output-schema", str(schema_path)])
    base_command.append("-")

    # last message 欠落も Codex CLI レスポンス要件の失敗として最大 3 回試行する。
    attempts = 3
    last_output = ""
    last_stdout_log = ""
    last_stderr = ""
    last_validation_error = ""
    last_log_path: Path | None = None
    last_message_path: Path | None = None
    for attempt in range(1, attempts + 1):
        command = [*base_command]
        # 利用者向けには prompt と回収出力の先頭だけを進捗表示する。
        _preflight_workspace_write_oracle_guard(repo_root, command)
        _maintain_indexes_before_codex(
            repo_root,
            skip_index_maintenance,
            normalized_index_excluded_roots,
        )
        print("## Codex CLI 実行準備")
        print(f"- attempt: {attempt}/{attempts}")
        print(f"- prompt preview: {_console_log_safe_head80(prompt)}")
        run = _run_codex_command(
            repo_root,
            command,
            prompt,
            purpose,
            attempt,
            schema_path,
            allowed_uncommitted_oracle_paths,
        )
        run = _retry_after_capacity_if_needed(
            repo_root,
            run,
            command,
            prompt,
            purpose,
            attempt,
            schema_path,
            allowed_uncommitted_oracle_paths,
            skip_index_maintenance,
            normalized_index_excluded_roots,
        )
        result = run.result
        last_log_path = run.log_path
        last_message_path = run.last_message_path
        last_stdout_log = result.stdout
        last_stderr = result.stderr

        # stdout JSONL の既知意味エラーは終了コードに依存せず扱う。
        if _stdout_jsonl_indicates_quota_exhaustion(result.stdout):
            session_id = _extract_session_id(result.stdout, result.stderr)
            resume_command = _resume_command(run.command, session_id)
            print("quota が枯渇したため、resume 前に復旧を待機します")
            run = _wait_for_quota_and_resume(
                repo_root,
                resume_command,
                prompt,
                purpose,
                attempt,
                schema_path,
                allowed_uncommitted_oracle_paths,
                skip_index_maintenance,
                normalized_index_excluded_roots,
            )
            result = run.result
            last_log_path = run.log_path
            last_message_path = run.last_message_path
            last_stdout_log = result.stdout
            last_stderr = result.stderr

        try:
            output = _read_last_message(last_message_path)
        except ValueError as error:
            last_validation_error = str(error)
            continue

        # last-message 欠落は終了コードに依存しないレスポンス要件違反として retry する。
        # last-message が正常に読めた非 0 終了は quota/capacity 以外の CLI 失敗として扱う。
        if result.returncode != 0:
            _raise_codex_failure(run.log_path, result)

        print("## Codex CLI 応答プレビュー")
        print(f"- attempt: {attempt}/{attempts}")
        print(f"- output preview: {_console_log_safe_head80(output)}")
        last_output = output

        if not validates_structured_output:
            if text_validator is None:
                return output
            try:
                text_validator(output)
                return output
            except ValueError as error:
                last_validation_error = str(error)
                continue

        # JSON parse、schema 検査、意味検査のいずれかが失敗した場合だけ次の試行へ進む。
        try:
            assert output_schema is not None
            value = json.loads(output)
            _validate_json_schema(value, output_schema)
            if json_validator is not None:
                json_validator(value)
            if text_validator is not None:
                text_validator(output)
            return output
        except (json.JSONDecodeError, ValueError) as error:
            last_validation_error = str(error)
            continue

    # 全試行失敗時は最後の output/stdout/stderr と検証エラーを診断情報として残す。
    validation_label = "JSON" if validates_structured_output else "text"
    raise CmocError(
        f"codex exec がリトライ後も有効な {validation_label} を返しませんでした。",
        [
            "codex exec のログを確認してください。",
            "prompt または fake Codex CLI の出力を修正してから、cmoc を再実行してください。",
        ],
        "\n".join(
            [
                f"Log: {last_log_path}",
                (
                    f"Output schema: {schema_path}"
                    if schema_path is not None
                    else "Output schema: none"
                ),
                f"Last message: {last_message_path}",
                f"Last validation error: {last_validation_error}",
                "Last output-last-message:",
                last_output,
                "Last stdout:",
                last_stdout_log,
                "Last stderr:",
                last_stderr,
            ]
        ),
    )


def parse_json_object(raw: str) -> dict[str, object]:
    """Codex CLI の JSON 応答を object として読む。"""
    # 呼び出し側が dict として扱えることをここで保証する。
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise CmocError(
            "codex exec が JSON object 以外を返しました。",
            [
                "Codex CLI の出力 schema を修正してください。",
                "cmoc を再実行してください。",
            ],
            raw,
        )
    return value


def _raise_codex_failure(
    log_path: Path,
    result: subprocess.CompletedProcess[str],
) -> None:
    """quota 以外の Codex CLI 非 0 終了を共通エラーにする。"""
    raise CmocError(
        "codex exec が失敗しました。",
        [
            "codex exec のログを確認してください。",
            "Codex CLI またはリポジトリ側の原因を修正してから、cmoc を再実行してください。",
        ],
        "\n".join(
            [
                f"Log: {log_path}",
                "STDOUT:",
                result.stdout,
                "STDERR:",
                result.stderr,
            ]
        ),
    )


def _validate_model_options(model: str, reasoning_effort: str) -> None:
    """Codex CLI に渡す model と reasoning effort の制約を検査する。"""
    # oracle が禁止する xhigh だけを呼び出し前に拒否する。
    if not model:
        raise ValueError("model must not be empty.")
    if reasoning_effort in _FORBIDDEN_REASONING_EFFORTS:
        raise ValueError("reasoning_effort xhigh is forbidden.")
    if reasoning_effort not in {"low", "medium", "high"}:
        raise ValueError("reasoning_effort must be low, medium, or high.")


def _wait_for_quota_and_resume(
    repo_root: Path,
    command: list[str],
    prompt: str,
    purpose: str,
    attempt: int,
    schema_path: Path | None,
    allowed_uncommitted_oracle_paths: Iterable[Path | str] | None,
    skip_index_maintenance: bool,
    index_excluded_roots: Iterable[Path | str] | None,
) -> _CodexCommandRun:
    """quota 復活まで疎通確認を繰り返してから元セッションを再開する。"""
    while True:
        poll_prompt = _quota_poll_prompt(repo_root)
        print("quota poll: 最小限の codex exec 疎通確認を実行します")
        print(f"quota poll prompt: {_console_log_safe_head80(poll_prompt)}")
        poll_command = _build_codex_command(
            read_only=True,
            model=_POLL_MODEL,
            reasoning_effort=_POLL_REASONING_EFFORT,
        )
        poll_command.append("-")
        _preflight_workspace_write_oracle_guard(repo_root, poll_command)
        _maintain_indexes_before_codex(
            repo_root,
            skip_index_maintenance,
            index_excluded_roots,
        )
        poll_run = _run_codex_command(
            repo_root,
            poll_command,
            poll_prompt,
            "quota 復旧確認",
            attempt,
            None,
            None,
        )
        poll_run = _retry_after_capacity_if_needed(
            repo_root,
            poll_run,
            poll_command,
            poll_prompt,
            "quota 復旧確認",
            attempt,
            None,
            None,
            skip_index_maintenance,
            index_excluded_roots,
        )
        poll_result = poll_run.result
        if _stdout_jsonl_indicates_quota_exhaustion(poll_result.stdout):
            _sleep_for_quota_poll_interval()
            continue
        if poll_result.returncode == 0:
            try:
                poll_output = _read_last_message(poll_run.last_message_path)
            except ValueError as error:
                _raise_quota_poll_failure(poll_run, str(error))
            print(f"quota poll output: {_console_log_safe_head80(poll_output)}")
            if poll_output.strip() != "ok":
                _raise_quota_poll_failure(
                    poll_run,
                    "quota poll の output-last-message が ok ではありませんでした。",
                )
            print("quota が復旧したため、codex exec を resume します")
            _preflight_workspace_write_oracle_guard(repo_root, command)
            _maintain_indexes_before_codex(
                repo_root,
                skip_index_maintenance,
                index_excluded_roots,
            )
            resume_run = _run_codex_command(
                repo_root,
                command,
                prompt,
                purpose,
                attempt,
                schema_path,
                allowed_uncommitted_oracle_paths,
            )
            resume_run = _retry_after_capacity_if_needed(
                repo_root,
                resume_run,
                command,
                prompt,
                purpose,
                attempt,
                schema_path,
                allowed_uncommitted_oracle_paths,
                skip_index_maintenance,
                index_excluded_roots,
            )
            if _stdout_jsonl_indicates_quota_exhaustion(
                resume_run.result.stdout,
            ):
                print("resume 後に quota が再度枯渇したため、待機します")
                _sleep_for_quota_poll_interval()
                continue
            if resume_run.result.returncode == 0:
                return resume_run
            _raise_codex_failure(resume_run.log_path, resume_run.result)
        if not _stdout_jsonl_indicates_quota_exhaustion(
            poll_run.result.stdout,
        ):
            _raise_codex_failure(poll_run.log_path, poll_result)
        _sleep_for_quota_poll_interval()


def _sleep_for_quota_poll_interval() -> None:
    """次の quota 疎通確認まで oracle 規定の間隔を空ける。"""
    wait_started = perf_counter()
    time.sleep(_QUOTA_POLL_INTERVAL_SECONDS)
    add_quota_wait(perf_counter() - wait_started)


def _retry_after_capacity_if_needed(
    repo_root: Path,
    run: _CodexCommandRun,
    command: list[str],
    prompt: str,
    purpose: str,
    attempt: int,
    schema_path: Path | None,
    allowed_uncommitted_oracle_paths: Iterable[Path | str] | None,
    skip_index_maintenance: bool,
    index_excluded_roots: Iterable[Path | str] | None,
) -> _CodexCommandRun:
    """capacity 一時失敗なら同じ Codex CLI 呼び出しを指数 backoff で再実行する。"""
    delay_seconds = _CAPACITY_INITIAL_RETRY_DELAY_SECONDS
    current_run = run
    for retry_index in range(1, _CAPACITY_RETRY_LIMIT + 1):
        if not _stdout_jsonl_indicates_capacity(current_run.result.stdout):
            return current_run
        print(
            "選択された model が capacity 上限に達しています。"
            f"{delay_seconds} sec 後に codex exec を再試行します "
            f"({retry_index}/{_CAPACITY_RETRY_LIMIT})"
        )
        time.sleep(delay_seconds)
        delay_seconds *= 2
        _preflight_workspace_write_oracle_guard(repo_root, command)
        _maintain_indexes_before_codex(
            repo_root,
            skip_index_maintenance,
            index_excluded_roots,
        )
        current_run = _run_codex_command(
            repo_root,
            command,
            prompt,
            purpose,
            attempt,
            schema_path,
            allowed_uncommitted_oracle_paths,
        )
    if _stdout_jsonl_indicates_capacity(current_run.result.stdout):
        _raise_capacity_failure(current_run)
    return current_run


def _maintain_indexes_before_codex(
    repo_root: Path,
    skip_index_maintenance: bool,
    index_excluded_roots: Iterable[Path | str] | None,
) -> None:
    """通常の Codex CLI 起動直前に INDEX.md メンテナンスを実行する。"""
    if skip_index_maintenance or not (repo_root / ".git").exists():
        return
    from .indexing import maintain_indexes

    if index_excluded_roots is None:
        maintain_indexes(repo_root)
        return
    maintain_indexes(repo_root, excluded_index_roots=index_excluded_roots)


def _quota_poll_prompt(repo_root: Path) -> str:
    """quota 疎通確認用の read-only prompt を組み立てる。"""
    return "\n".join(
        [
            "あなたは Codex CLI の疎通確認担当です。",
            "この実行環境で最小限の応答が可能か確認してください。",
            "完了条件は `ok` だけを出力することです。",
            "詳細な作業内容:",
            "- ファイル編集は禁止です。",
            f"- `{repo_root / 'memo'}` は読み書き禁止です。",
            "- この疎通確認では、その他のファイルも読む必要はありません。",
        ]
    )


def _build_codex_command(
    *,
    read_only: bool,
    model: str,
    reasoning_effort: str,
) -> list[str]:
    """必須オプション込みの `codex exec` コマンドを組み立てる。"""
    # last message の保存先は実行単位で決まるため、起動直前に追加する。
    sandbox = "read-only" if read_only else "workspace-write"
    return [
        "codex",
        "exec",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--sandbox",
        sandbox,
        "--json",
    ]


def _run_codex_command(
    repo_root: Path,
    command: list[str],
    prompt: str,
    purpose: str,
    attempt: int,
    schema_path: Path | None,
    allowed_uncommitted_oracle_paths: Iterable[Path | str] | None,
) -> _CodexCommandRun:
    """Codex CLI を 1 回起動し、その呼び出し専用ログを出力する。"""
    paths = _prepare_codex_exec_paths(repo_root)
    log_path = paths["call"]
    last_message_path = paths["last_message"]
    run_command = _command_with_last_message(command, last_message_path)
    oracle_guard = _start_oracle_guard(
        repo_root,
        command,
        allowed_uncommitted_oracle_paths,
    )
    started = perf_counter()
    result = subprocess.run(
        run_command,
        cwd=repo_root,
        input=prompt,
        text=True,
        encoding=_CODEX_TEXT_ENCODING,
        errors=_CODEX_TEXT_ERRORS,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _append_codex_log(
        log_path,
        run_command,
        prompt,
        attempt,
        result,
        schema_path,
        last_message_path,
    )
    _print_codex_notification(
        purpose=purpose,
        repo_root=repo_root,
        log_path=log_path,
        elapsed_seconds=perf_counter() - started,
        returncode=result.returncode,
    )
    _assert_workspace_write_oracles_unchanged(repo_root, oracle_guard)
    return _CodexCommandRun(
        result=result,
        log_path=log_path,
        last_message_path=last_message_path,
        command=run_command,
    )


def _start_oracle_guard(
    repo_root: Path,
    command: list[str],
    allowed_uncommitted_oracle_paths: Iterable[Path | str] | None,
) -> _OracleGuardSnapshot:
    """workspace-write 実行前 HEAD を記録する。"""
    if not _workspace_write_oracle_guard_applies(repo_root, command):
        return _OracleGuardSnapshot(enabled=False, head_commit=None)
    head, head_reflog_entry_count = _verify_workspace_write_oracle_guard_head(
        repo_root
    )
    return _OracleGuardSnapshot(
        enabled=True,
        head_commit=head,
        head_reflog_entry_count=head_reflog_entry_count,
        allowed_uncommitted_paths=_active_allowed_oracle_conflict_paths(
            repo_root,
            allowed_uncommitted_oracle_paths,
        ),
    )


def _preflight_workspace_write_oracle_guard(
    repo_root: Path,
    command: list[str],
) -> None:
    """workspace-write の副作用前に HEAD/reflog 検査だけを済ませる。"""
    if not _workspace_write_oracle_guard_applies(repo_root, command):
        return
    _verify_workspace_write_oracle_guard_head(repo_root)


def _workspace_write_oracle_guard_applies(
    repo_root: Path,
    command: list[str],
) -> bool:
    """workspace-write guard の対象になる Codex コマンドか判定する。"""
    # Git repo 外や read-only 実行では oracle 変更検査の対象外にする。
    if "--sandbox" not in command or not (repo_root / ".git").exists():
        return False
    sandbox_index = command.index("--sandbox") + 1
    return (
        sandbox_index < len(command)
        and command[sandbox_index] == "workspace-write"
    )


def _verify_workspace_write_oracle_guard_head(
    repo_root: Path,
) -> tuple[str, int]:
    """workspace-write guard の開始 HEAD と reflog が読めることを検証する。"""
    result = run_git(
        repo_root,
        ["rev-parse", "--verify", "HEAD"],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "workspace-write oracle guard の開始 HEAD を検証できませんでした。",
            [
                "workspace-write で Codex CLI を実行する前に、HEAD が存在する状態へしてください。",
                "初期 commit が未作成の場合は、先に必要な初期 commit を作成してください。",
            ],
            result.stderr.strip(),
        )
    head = result.stdout.strip()
    head_reflog_entry_count = _head_reflog_entry_count(repo_root)
    if head_reflog_entry_count is None:
        raise CmocError(
            "workspace-write oracle guard の HEAD reflog を検証できませんでした。",
            [
                "workspace-write で Codex CLI を実行する前に、HEAD reflog が記録される状態へしてください。",
                "HEAD 移動の履歴を検査できない状態では、oracles ファイル保護を保証できません。",
            ],
        )
    return (head, head_reflog_entry_count)


def _assert_workspace_write_oracles_unchanged(
    repo_root: Path,
    snapshot: _OracleGuardSnapshot,
) -> None:
    """workspace-write 実行後の oracle ファイル変更を拒否する。"""
    if not snapshot.enabled:
        return
    allowed = set(snapshot.allowed_uncommitted_paths)
    uncommitted = [
        path
        for path in _uncommitted_oracle_file_paths(repo_root)
        if path not in allowed
    ]
    range_error, committed = _committed_oracle_file_paths(
        repo_root,
        snapshot.head_commit,
    )
    reflog_error, reflog_committed = _head_reflog_oracle_file_paths(
        repo_root,
        snapshot.head_commit,
        snapshot.head_reflog_entry_count,
    )
    committed = sorted(
        {
            *committed,
            *reflog_committed,
        }
    )
    head_errors = [
        error for error in [range_error, reflog_error] if error is not None
    ]
    if not uncommitted and not committed and not head_errors:
        return

    detail_lines: list[str] = []
    if uncommitted:
        detail_lines.append("未コミット差分:")
        detail_lines.extend(uncommitted)
    if head_errors:
        detail_lines.append("Codex CLI 実行中の HEAD 検査エラー:")
        detail_lines.extend(head_errors)
    if committed:
        detail_lines.append("Codex CLI 実行中の commit range 変更:")
        detail_lines.extend(committed)
    raise CmocError(
        "codex exec が oracles ファイルを変更しました。",
        [
            "oracles ファイルの変更を確認し、手動で解消してください。",
            "作業ツリーと commit 履歴が許容できる状態になってから、cmoc を再実行してください。",
        ],
        "\n".join(detail_lines),
    )


def _active_allowed_oracle_conflict_paths(
    repo_root: Path,
    allowed_paths: Iterable[Path | str] | None,
) -> tuple[str, ...]:
    """現に conflict 中の oracle path だけを guard 例外対象へ正規化する。"""
    if allowed_paths is None:
        return ()
    requested = set(_normalize_repo_relative_paths(repo_root, allowed_paths))
    if not requested:
        return ()
    unmerged = run_git(
        repo_root,
        ["diff", "--name-only", "-z", "--diff-filter=U"],
    )
    active = set(git_name_only_paths(unmerged.stdout))
    return tuple(
        sorted(
            filter_oracle_file_paths(
                repo_root,
                [path for path in requested if path in active],
            )
        )
    )


def _normalize_repo_relative_paths(
    repo_root: Path,
    paths: Iterable[Path | str],
) -> list[str]:
    """Path/str の混在を repo root 相対の POSIX path にそろえる。"""
    normalized: list[str] = []
    concrete_root = repo_root.resolve()
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(concrete_root)
            except ValueError:
                continue
        normalized.append(path.as_posix())
    return normalized


def _uncommitted_oracle_file_paths(repo_root: Path) -> list[str]:
    """未コミット差分に含まれる oracle ファイルを返す。"""
    relative_paths: list[str] = []
    diff = run_git(
        repo_root,
        ["diff", "--name-status", "-z", "-M", "HEAD", "--", "oracles"],
    )
    relative_paths.extend(_paths_from_name_status_z(diff.stdout))
    status = run_git(
        repo_root,
        [
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
            "--",
            "oracles",
        ],
    )
    relative_paths.extend(
        path for status_code, path in git_status_paths(status.stdout)
        if status_code == "??"
    )
    return filter_oracle_file_paths(repo_root, relative_paths)


def _committed_oracle_file_paths(
    repo_root: Path,
    before_head: str | None,
) -> tuple[str | None, list[str]]:
    """Codex 実行前後の HEAD range に含まれる oracle ファイルを返す。"""
    if before_head is None:
        return ("Codex CLI 実行前 HEAD が記録されていません。", [])
    after = run_git(
        repo_root,
        ["rev-parse", "--verify", "HEAD"],
        check=False,
    )
    if after.returncode != 0:
        return ("Codex CLI 実行後 HEAD を検証できません。", [])
    after_head = after.stdout.strip()
    if after_head == before_head:
        return (None, [])
    ancestor = run_git(
        repo_root,
        ["merge-base", "--is-ancestor", before_head, after_head],
        check=False,
    )
    if ancestor.returncode == 1:
        return (
            "Codex CLI 実行後 HEAD が実行前 HEAD の子孫ではありません。",
            [],
        )
    if ancestor.returncode != 0:
        return ("Codex CLI 実行前後 HEAD の祖先関係を検証できません。", [])
    log = run_git(
        repo_root,
        [
            "log",
            "--format=",
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=ACDMRT",
            f"{before_head}..HEAD",
            "--",
            "oracles",
        ],
    )
    return (
        None,
        filter_oracle_file_paths(
            repo_root,
            _paths_from_name_status_z(log.stdout),
        ),
    )


def _head_reflog_entry_count(repo_root: Path) -> int | None:
    """HEAD reflog の現在 entry 数を返す。"""
    reflog = run_git(
        repo_root,
        ["reflog", "--format=%H", "HEAD"],
        check=False,
    )
    if reflog.returncode != 0:
        return None
    return len(reflog.stdout.splitlines())


def _head_reflog_oracle_file_paths(
    repo_root: Path,
    before_head: str | None,
    baseline_entry_count: int | None,
) -> tuple[str | None, list[str]]:
    """Codex 実行中に HEAD reflog へ現れた commit の oracle 変更を返す。"""
    if before_head is None or baseline_entry_count is None:
        return ("Codex CLI 実行前 HEAD reflog が記録されていません。", [])
    reflog = run_git(
        repo_root,
        ["reflog", "--format=%H", "HEAD"],
        check=False,
    )
    if reflog.returncode != 0:
        return ("Codex CLI 実行後 HEAD reflog を検証できません。", [])
    # `git reflog` は新しい entry から返すため、開始時 entry 数を超える先頭部分が
    # Codex 実行中に追加された HEAD 移動である。
    entries = reflog.stdout.splitlines()
    if len(entries) < baseline_entry_count:
        return ("Codex CLI 実行中に HEAD reflog が短くなりました。", [])
    new_commits = entries[: max(0, len(entries) - baseline_entry_count)]
    paths: list[str] = []
    for commit in new_commits:
        if not commit or set(commit) == {"0"}:
            continue
        already_reachable = run_git(
            repo_root,
            ["merge-base", "--is-ancestor", commit, before_head],
            check=False,
        )
        if already_reachable.returncode == 0:
            continue
        log = run_git(
            repo_root,
            [
                "log",
                "--format=",
                "--name-status",
                "-z",
                "-M",
                "--diff-filter=ACDMRT",
                f"{commit}^!",
                "--",
                "oracles",
            ],
            check=False,
        )
        if log.returncode == 0:
            paths.extend(_paths_from_name_status_z(log.stdout))
    return (None, filter_oracle_file_paths(repo_root, paths))


def _paths_from_name_status_z(output: str) -> list[str]:
    """`git diff --name-status -z` の変更前後 path を取り出す。"""
    # rename/copy では旧 path と新 path の両方を検査し、oracle から外への移動も
    # oracle ファイル変更として検出できるようにする。
    paths: list[str] = []
    for _status, entry_paths in git_name_status_entries(output):
        paths.extend(entry_paths)
    return paths


def _command_with_last_message(
    command: list[str],
    last_message_path: Path,
) -> list[str]:
    """`--output-last-message` の保存先だけを実行単位の path に差し替える。"""
    run_command = [*command]
    if "--output-last-message" in run_command:
        option_index = run_command.index("--output-last-message")
        if option_index + 1 < len(run_command):
            run_command[option_index + 1] = str(last_message_path)
            return run_command
        run_command.append(str(last_message_path))
        return run_command
    insert_index = len(run_command)
    if "resume" in run_command[2:]:
        insert_index = run_command.index("resume")
    elif run_command and run_command[-1] == "-":
        insert_index -= 1
    run_command[insert_index:insert_index] = [
        "--output-last-message",
        str(last_message_path),
    ]
    return run_command


def _print_codex_notification(
    *,
    purpose: str,
    repo_root: Path,
    log_path: Path,
    elapsed_seconds: float,
    returncode: int,
) -> None:
    """Codex CLI 呼び出し完了をコンソール・サブコマンドログへ通知する。"""
    log_event(
        "codex_exec_call",
        {
            "purpose": purpose,
            "log_path": str(log_path),
            "elapsed_seconds": elapsed_seconds,
            "returncode": returncode,
        },
    )
    print("## Codex CLI 呼び出し完了")
    print(f"- purpose: {_console_log_safe_text(purpose)}")
    print(f"- log path: {_console_log_safe_text(str(log_path))}")
    print(f"- elapsed: {format_duration(elapsed_seconds)}")
    print(f"- returncode: {returncode}")


def _console_log_safe_text(value: str) -> str:
    """制御文字で markdown の行構造が壊れない表示文字列へ変換する。"""
    parts: list[str] = []
    for char in value:
        if char == "%" or ord(char) < 0x20 or ord(char) == 0x7F:
            parts.extend(f"%{byte:02X}" for byte in char.encode("utf-8"))
        else:
            parts.append(char)
    return "".join(parts)


def _console_log_safe_head80(value: str) -> str:
    """元文字列を切り詰めてから console/log 表示用に安全化する。"""
    return _console_log_safe_text(_head80(value))


def _read_last_message(path: Path) -> str:
    """`--output-last-message` の成果物を読み取る。"""
    # Codex CLI の成果物は stdout ではなく last message ファイルとする。
    if not path.exists():
        raise ValueError(f"output-last-message was not created: {path}")
    try:
        return path.read_text(
            encoding=_CODEX_TEXT_ENCODING,
            errors=_CODEX_TEXT_ERRORS,
        )
    except OSError as error:
        raise ValueError(
            f"output-last-message could not be read: {path}; "
            f"reason: {error}"
        ) from error


def _raise_quota_poll_failure(
    run: _CodexCommandRun,
    reason: str,
) -> NoReturn:
    """quota 疎通確認が実行可能状態を証明しない場合は中断する。"""
    raise CmocError(
        "quota 復旧確認に失敗しました。",
        [
            "codex exec のログを確認してください。",
            "Codex CLI または実行環境の状態を確認してから、cmoc を再実行してください。",
        ],
        "\n".join(
            [
                f"Log: {run.log_path}",
                f"Last message: {run.last_message_path}",
                f"Reason: {reason}",
                "STDOUT:",
                run.result.stdout,
                "STDERR:",
                run.result.stderr,
            ]
        ),
    )


def _raise_capacity_failure(run: _CodexCommandRun) -> NoReturn:
    """capacity 一時失敗を規定回数リトライしても解消しない場合は中断する。"""
    raise CmocError(
        "codex exec が capacity リトライ後も失敗しました。",
        [
            "codex exec のログを確認してください。",
            "Codex CLI または実行環境の状態を確認してから、cmoc を再実行してください。",
        ],
        "\n".join(
            [
                f"Log: {run.log_path}",
                f"Last message: {run.last_message_path}",
                "STDOUT:",
                run.result.stdout,
                "STDERR:",
                run.result.stderr,
            ]
        ),
    )


def _stdout_jsonl_indicates_quota_exhaustion(stdout: str) -> bool:
    """Codex CLI の stdout JSONL から quota 枯渇を判定する。"""
    return _stdout_jsonl_has_error_message(stdout, _QUOTA_MESSAGES)


def _stdout_jsonl_indicates_capacity(stdout: str) -> bool:
    """Codex CLI の stdout JSONL から capacity 一時失敗を判定する。"""
    return _stdout_jsonl_has_error_message(stdout, (_CAPACITY_MESSAGE,))


def _stdout_jsonl_has_error_message(
    stdout: str,
    message_fragments: tuple[str, ...],
) -> bool:
    """stdout JSONL の既知 error event に指定文言が含まれるか調べる。"""
    for line in stdout.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = _codex_error_message(value)
        if message is None:
            continue
        if any(fragment in message for fragment in message_fragments):
            return True
    return False


def _codex_error_message(value: object) -> str | None:
    """Codex JSONL の error / turn.failed event から message を取り出す。"""
    if not isinstance(value, dict):
        return None
    event_type = value.get("type")
    if event_type == "error":
        message = value.get("message")
        return message if isinstance(message, str) else None
    if event_type == "turn.failed":
        error = value.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            return message if isinstance(message, str) else None
    return None


def _extract_session_id(stdout: str, stderr: str) -> str | None:
    """JSONL ログから resume 用 id を取り出す。"""
    # Codex JSONL の構造化 field だけを参照し、本文中のコード断片を誤抽出しない。
    for line in f"{stdout}\n{stderr}".splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        session_id = _session_id_from_json(value)
        if session_id is not None:
            return session_id
    return None


def _session_id_from_json(value: object) -> str | None:
    """ネストした JSON object から resume 用 id らしい文字列を探す。"""
    # Codex JSONL のフィールド名変化に備えて再帰的に探す。
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key).lower().replace("-", "_")
            if key_text in {
                "session_id",
                "sessionid",
                "thread_id",
                "threadid",
            } and isinstance(child, str):
                return child
            found = _session_id_from_json(child)
            if found is not None:
                return found
    if isinstance(value, list):
        for child in value:
            found = _session_id_from_json(child)
            if found is not None:
                return found
    return None


def _resume_command(command: list[str], session_id: str | None) -> list[str]:
    """元コマンドを `codex exec ... resume <session-id> ...` に変換する。"""
    if session_id is None:
        raise CmocError(
            "quota 枯渇後の resume session id を取得できませんでした。",
            [
                "codex exec のログを確認してください。",
                "停止した session id が出力される状態で、cmoc を再実行してください。",
            ],
            "Codex CLI の JSONL 出力から session_id/thread_id を取得できませんでした。",
        )
    resumed = [*command]
    if "resume" in resumed[2:]:
        return resumed
    insert_index = len(resumed)
    if resumed and resumed[-1] == "-":
        insert_index -= 1
    resumed[insert_index:insert_index] = ["resume", session_id]
    return resumed


def _append_codex_log(
    log_path: Path,
    command: list[str],
    prompt: str,
    attempt: int,
    result: subprocess.CompletedProcess[str],
    schema_path: Path | None,
    last_message_path: Path,
) -> None:
    """1 回分の Codex CLI 入出力を Markdown フルログへ書き出す。"""
    output_last_message = _read_optional_text(last_message_path)
    body = "\n".join(
        [
            "## Codex Exec Call",
            "",
            "### Prompt",
            "",
            _markdown_text_block(prompt),
            "",
            "### Return Code",
            "",
            f"`{result.returncode}`",
            "",
            "### Stdout",
            "",
            _markdown_text_block(result.stdout),
            "",
            "### Stderr",
            "",
            _markdown_text_block(result.stderr),
            "",
            "### Output Last Message",
            "",
            f"`{last_message_path}`",
            "",
            _markdown_text_block(output_last_message),
            "",
        ]
    )
    front_matter = _codex_log_front_matter(
        command=command,
        attempt=attempt,
        returncode=result.returncode,
        schema_path=schema_path,
        last_message_path=last_message_path,
    )
    log_path.write_text(
        front_matter + body,
        encoding="utf-8",
    )


def _markdown_text_block(text: str) -> str:
    """Markdown code fence と衝突しない text code block を組み立てる。"""
    max_backtick_run = max(
        (len(match.group(0)) for match in re.finditer(r"`+", text)),
        default=0,
    )
    fence = "`" * max(3, max_backtick_run + 1)
    return "\n".join([f"{fence}text", text, fence])


def _write_output_schema(
    repo_root: Path,
    output_schema: dict[str, object] | None,
) -> Path | None:
    """Structured Output 用 JSON schema を hash 名で保存する。"""
    # Structured Output を使わない呼び出しでは schema ファイルを作らない。
    if output_schema is None:
        return None

    # schema 本文を安定化し、同一 hash の中間ファイルをキャッシュとして再利用する。
    schema_body = json.dumps(
        output_schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    schema_hash = sha256(schema_body.encode("utf-8")).hexdigest()
    schema_dir = repo_root / ".cmoc" / "logs" / "codex_exec" / "output_schema"
    schema_dir.mkdir(parents=True, exist_ok=True)
    schema_path = schema_dir / f"{schema_hash}.log"
    if schema_path.exists() and schema_path.read_text(encoding="utf-8") == schema_body:
        return schema_path

    # 最終 path へ直接書かず、完成済みの一時ファイルを atomic に公開する。
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=schema_dir,
            prefix=f".{schema_hash}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_file.write(schema_body)
            temp_path = Path(temp_file.name)
        temp_path.replace(schema_path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
    return schema_path


def _prepare_codex_exec_paths(repo_root: Path) -> dict[str, Path]:
    """codex exec の call log と last message の保存先を準備する。"""
    base_dir = repo_root / ".cmoc" / "logs" / "codex_exec"
    call_dir = base_dir / "call"
    last_message_dir = base_dir / "output_last_message"
    call_dir.mkdir(parents=True, exist_ok=True)
    last_message_dir.mkdir(parents=True, exist_ok=True)
    while True:
        timestamp = make_timestamp()
        call_path = call_dir / f"{timestamp}.log"
        last_message_path = last_message_dir / f"{timestamp}.log"
        try:
            with call_path.open("x", encoding="utf-8"):
                pass
        except FileExistsError:
            time.sleep(0.001)
            continue
        if last_message_path.exists():
            call_path.unlink(missing_ok=True)
            time.sleep(0.001)
            continue
        return {
            "call": call_path,
            "last_message": last_message_path,
        }


def _codex_log_front_matter(
    *,
    command: list[str],
    attempt: int,
    returncode: int,
    schema_path: Path | None,
    last_message_path: Path,
) -> str:
    """codex exec 呼び出し情報を YAML Front Matter として組み立てる。"""
    model = _value_after(command, "--model")
    sandbox = _value_after(command, "--sandbox")
    reasoning_effort = _reasoning_effort_from_command(command)
    output_schema = str(schema_path) if schema_path else None
    lines = [
        "---",
        "command:",
        *[f"  - {_yaml_scalar(part)}" for part in command],
        f"command_line: {_yaml_scalar(' '.join(command))}",
        f"model: {_yaml_scalar(model)}",
        f"reasoning_effort: {_yaml_scalar(reasoning_effort)}",
        f"sandbox: {_yaml_scalar(sandbox)}",
        f"output_schema: {_yaml_scalar(output_schema)}",
        f"output_last_message: {_yaml_scalar(str(last_message_path))}",
        f"attempt: {attempt}",
        f"returncode: {returncode}",
        "---",
        "",
    ]
    return "\n".join(lines)


def _yaml_scalar(value: str | None) -> str:
    """Front Matter 用の YAML scalar を安全な JSON quote で表す。"""
    if value is None:
        return "null"
    return json.dumps(value, ensure_ascii=False)


def _value_after(command: list[str], option: str) -> str | None:
    """コマンド配列から option 直後の値を取り出す。"""
    try:
        return command[command.index(option) + 1]
    except (ValueError, IndexError):
        return None


def _reasoning_effort_from_command(command: list[str]) -> str | None:
    """`-c model_reasoning_effort=...` から reasoning effort を読む。"""
    for index, part in enumerate(command[:-1]):
        if part != "-c":
            continue
        config = command[index + 1]
        match = re.fullmatch(r'model_reasoning_effort="([^"]+)"', config)
        if match is not None:
            return match.group(1)
    return None


def _read_optional_text(path: Path) -> str:
    """存在するテキストファイルだけをログ本文へ取り込む。"""
    if not path.exists():
        return ""
    try:
        return path.read_text(
            encoding=_CODEX_TEXT_ENCODING,
            errors=_CODEX_TEXT_ERRORS,
        )
    except OSError as error:
        return f"[unreadable: {path}; reason: {error}]"


def _validate_json_schema(value: object, schema: dict[str, object]) -> None:
    """Codex CLI の Structured Output を JSON Schema として検査する。"""
    # Codex CLI の応答を cmoc 側でも機械的に再検証する。
    try:
        Draft202012Validator(schema).validate(value)
    except ValidationError as error:
        raise ValueError(error.message) from error


def _validate_output_schema(schema: dict[str, object]) -> None:
    """cmoc 側の Structured Output schema 定義を事前検査する。"""
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise CmocError(
            "Codex CLI の出力 schema 定義が不正です。",
            [
                "cmoc の Structured Output schema 定義を修正してください。",
                "schema 定義修正後に cmoc を再実行してください。",
            ],
            error.message,
        ) from error


def _head80(value: str) -> str:
    """元文字列の先頭 80 文字を返す。"""
    # oracle の切り詰め対象は、表示用変換前の prompt/output そのものである。
    return value[:80]
