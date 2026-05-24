"""Codex CLI 呼び出しの共通処理。"""

import json
import re
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from time import perf_counter

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .errors import CmocError
from .subcommand_log import add_quota_wait
from .timing import format_duration
from .timestamps import make_timestamp

_DEFAULT_MODEL = "gpt-5.5"
_DEFAULT_REASONING_EFFORT = "medium"
COST_PERFORMANCE_MODEL = "gpt-5.4-mini"
COST_PERFORMANCE_REASONING_EFFORT = "medium"
COMMIT_MESSAGE_MODEL = COST_PERFORMANCE_MODEL
COMMIT_MESSAGE_REASONING_EFFORT = "low"
INDEX_GENERATION_MODEL = COST_PERFORMANCE_MODEL
INDEX_GENERATION_REASONING_EFFORT = COST_PERFORMANCE_REASONING_EFFORT
_POLL_MODEL = COST_PERFORMANCE_MODEL
_POLL_REASONING_EFFORT = "low"
_QUOTA_POLL_INTERVAL_SECONDS = 30 * 60
_FORBIDDEN_REASONING_EFFORTS = {"xhigh"}


@dataclass(frozen=True)
class _CodexCommandRun:
    """1 回の `codex exec` 起動結果と対応する成果物 path。"""

    result: subprocess.CompletedProcess[str]
    log_path: Path
    last_message_path: Path
    command: list[str]


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
    model: str = _DEFAULT_MODEL,
    reasoning_effort: str = _DEFAULT_REASONING_EFFORT,
) -> str:
    """`codex exec` を実行し、フルログを `logs/codex_exec` に保存する。"""
    # Structured Output を要求する呼び出しは schema ファイルを必須にする。
    if expect_json and output_schema is None:
        raise ValueError("expect_json=True requires output_schema.")
    validates_structured_output = output_schema is not None
    _validate_model_options(model, reasoning_effort)

    # 必要なら output schema ファイルを準備する。call log と last message は実行単位で払い出す。
    command = _build_codex_command(
        read_only=read_only,
        model=model,
        reasoning_effort=reasoning_effort,
    )
    schema_path = _write_output_schema(repo_root, output_schema)
    if schema_path is not None:
        command.extend(["--output-schema", str(schema_path)])
    command.append("-")

    # last message 欠落も Codex CLI レスポンス要件の失敗として最大 3 回試行する。
    attempts = 3
    last_output = ""
    last_stdout_log = ""
    last_stderr = ""
    last_validation_error = ""
    last_log_path: Path | None = None
    last_message_path: Path | None = None
    for attempt in range(1, attempts + 1):
        # 利用者向けには prompt と回収出力の先頭だけを進捗表示する。
        step = f"codex exec attempt ({attempt}/{attempts})"
        print(f"{step} prompt: {_head80(prompt)}")
        _maintain_indexes_before_codex(repo_root, skip_index_maintenance)
        run = _run_codex_command(
            repo_root,
            command,
            prompt,
            purpose,
            attempt,
            schema_path,
        )
        result = run.result
        last_log_path = run.log_path
        last_message_path = run.last_message_path
        command = run.command
        last_stdout_log = result.stdout
        last_stderr = result.stderr

        # quota 枯渇だけは待機・resume に入り、それ以外の CLI 失敗は中断する。
        if result.returncode != 0:
            if _looks_like_quota_exhaustion(result.stdout, result.stderr):
                session_id = _extract_session_id(result.stdout, result.stderr)
                command = _resume_command(command, session_id)
                print("quota exhausted; waiting before resume")
                while True:
                    run = _wait_for_quota_and_resume(
                        repo_root,
                        command,
                        prompt,
                        purpose,
                        attempt,
                        schema_path,
                        skip_index_maintenance,
                    )
                    result = run.result
                    last_log_path = run.log_path
                    last_message_path = run.last_message_path
                    command = run.command
                    last_stdout_log = result.stdout
                    last_stderr = result.stderr
                    if result.returncode == 0:
                        break
                    if not _looks_like_quota_exhaustion(
                        result.stdout,
                        result.stderr,
                    ):
                        _raise_codex_failure(run.log_path, result)
                    print("quota exhausted again after resume; waiting")
            else:
                _raise_codex_failure(run.log_path, result)

        try:
            output = _read_last_message(last_message_path)
        except ValueError as error:
            last_validation_error = str(error)
            continue
        print(f"{step} output: {_head80(output)}")
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
        f"Log: {log_path}\nSTDERR:\n{result.stderr}",
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
    skip_index_maintenance: bool,
) -> _CodexCommandRun:
    """quota 復活まで疎通確認を繰り返してから元セッションを再開する。"""
    # 復活確認は低コスト model/effort の最小 prompt で行う。
    while True:
        poll_prompt = _quota_poll_prompt(repo_root)
        print("quota poll: running minimal codex exec check")
        print(f"quota poll prompt: {_head80(poll_prompt)}")
        poll_command = _build_codex_command(
            read_only=True,
            model=_POLL_MODEL,
            reasoning_effort=_POLL_REASONING_EFFORT,
        )
        poll_command.append("-")
        _maintain_indexes_before_codex(repo_root, skip_index_maintenance)
        poll_run = _run_codex_command(
            repo_root,
            poll_command,
            poll_prompt,
            "quota recovery check",
            attempt,
            None,
        )
        poll_result = poll_run.result
        if poll_result.returncode == 0:
            poll_output = _read_last_message(poll_run.last_message_path)
            print(f"quota poll output: {_head80(poll_output)}")
            print("quota restored; resuming codex exec")
            _maintain_indexes_before_codex(repo_root, skip_index_maintenance)
            return _run_codex_command(
                repo_root,
                command,
                prompt,
                purpose,
                attempt,
                schema_path,
            )
        wait_started = perf_counter()
        time.sleep(_QUOTA_POLL_INTERVAL_SECONDS)
        add_quota_wait(perf_counter() - wait_started)


def _maintain_indexes_before_codex(
    repo_root: Path,
    skip_index_maintenance: bool,
) -> None:
    """通常の Codex CLI 起動直前に INDEX.md メンテナンスを実行する。"""
    if skip_index_maintenance or not (repo_root / ".git").exists():
        return
    from .indexing import maintain_indexes

    maintain_indexes(repo_root)


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
) -> _CodexCommandRun:
    """Codex CLI を 1 回起動し、その呼び出し専用ログを出力する。"""
    paths = _prepare_codex_exec_paths(repo_root)
    log_path = paths["call"]
    last_message_path = paths["last_message"]
    run_command = _command_with_last_message(command, last_message_path)
    print(
        "codex exec call: "
        f"{_head80(prompt)} -> {log_path.relative_to(repo_root)}"
    )
    # 前回 attempt の最終メッセージを誤読しないよう、起動前に消しておく。
    last_message_path.unlink(missing_ok=True)
    started = perf_counter()
    result = subprocess.run(
        run_command,
        cwd=repo_root,
        input=prompt,
        text=True,
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
    return _CodexCommandRun(
        result=result,
        log_path=log_path,
        last_message_path=last_message_path,
        command=run_command,
    )


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
    if run_command and run_command[-1] == "-":
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
    print(
        "codex exec: "
        f"{purpose} "
        f"log={log_path.relative_to(repo_root)} "
        f"elapsed={format_duration(elapsed_seconds)} "
        f"returncode={returncode}"
    )


def _read_last_message(path: Path) -> str:
    """`--output-last-message` の成果物を読み取る。"""
    # Codex CLI の成果物は stdout ではなく last message ファイルとする。
    if not path.exists():
        raise ValueError(f"output-last-message was not created: {path}")
    return path.read_text(encoding="utf-8")


def _looks_like_quota_exhaustion(stdout: str, stderr: str) -> bool:
    """Codex CLI 出力から quota 枯渇らしさを判定する。"""
    # Codex の表現ゆれに備えて、limit/credits/quota 系の語を広めに拾う。
    text = f"{stdout}\n{stderr}".lower()
    quota_words = ["quota", "limit", "credit", "credits", "rate limit"]
    exhaustion_words = ["exhaust", "insufficient", "reached", "exceeded"]
    return (
        any(word in text for word in quota_words)
        and any(word in text for word in exhaustion_words)
    )


def _extract_session_id(stdout: str, stderr: str) -> str | None:
    """JSONL ログなどから resume 用 session id を取り出す。"""
    # JSONL と人間向けログのどちらにも耐える最小限の抽出を行う。
    for line in stdout.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        session_id = _session_id_from_json(value)
        if session_id is not None:
            return session_id
    text = f"{stdout}\n{stderr}"
    match = re.search(r"session[_ -]?id['\":= ]+([A-Za-z0-9_.:-]+)", text)
    if match is None:
        return None
    return match.group(1)


def _session_id_from_json(value: object) -> str | None:
    """ネストした JSON object から session id らしい文字列を探す。"""
    # Codex JSONL のフィールド名変化に備えて再帰的に探す。
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key).lower().replace("-", "_")
            if key_text in {"session_id", "sessionid"} and isinstance(
                child,
                str,
            ):
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
    """元コマンドへ `--resume` を追加する。"""
    # session id が取れない場合も Codex CLI 側の既定 resume に委ねる。
    if "--resume" in command:
        return command
    resumed = [*command[:2], "--resume"]
    if session_id is not None:
        resumed.append(session_id)
    resumed.extend(command[2:])
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
    body = "\n".join(
        [
            "## Codex Exec Call",
            "",
            "### Prompt",
            "",
            "```text",
            prompt,
            "```",
            "",
            "### Return Code",
            "",
            f"`{result.returncode}`",
            "",
            "### Stdout",
            "",
            "```text",
            result.stdout,
            "```",
            "",
            "### Stderr",
            "",
            "```text",
            result.stderr,
            "```",
            "",
            "### Output Last Message",
            "",
            f"`{last_message_path}`",
            "",
            "```text",
            _read_optional_text(last_message_path),
            "```",
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
    schema_dir = repo_root / "logs" / "codex_exec" / "output_schemae"
    schema_dir.mkdir(parents=True, exist_ok=True)
    schema_path = schema_dir / f"{schema_hash}.log"
    if not schema_path.exists():
        schema_path.write_text(schema_body, encoding="utf-8")
    return schema_path


def _prepare_codex_exec_paths(repo_root: Path) -> dict[str, Path]:
    """codex exec の call log と last message の保存先を準備する。"""
    base_dir = repo_root / "logs" / "codex_exec"
    call_dir = base_dir / "call"
    last_message_dir = base_dir / "output_last_message"
    call_dir.mkdir(parents=True, exist_ok=True)
    last_message_dir.mkdir(parents=True, exist_ok=True)
    timestamp = _make_unused_codex_call_timestamp(call_dir)
    return {
        "call": call_dir / f"{timestamp}.log",
        "last_message": last_message_dir / f"{timestamp}.log",
    }


def _make_unused_codex_call_timestamp(call_dir: Path) -> str:
    """既存 call log と衝突しない timestamp を作る。"""
    while True:
        timestamp = make_timestamp()
        if not (call_dir / f"{timestamp}.log").exists():
            return timestamp
        time.sleep(0.001)


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
    return path.read_text(encoding="utf-8")


def _validate_json_schema(value: object, schema: dict[str, object]) -> None:
    """Codex CLI の Structured Output を JSON Schema として検査する。"""
    # Codex CLI の応答を cmoc 側でも機械的に再検証する。
    try:
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(value)
    except (SchemaError, ValidationError) as error:
        raise ValueError(error.message) from error


def _head80(value: str) -> str:
    """元文字列の先頭 80 文字を stdout 表示向けに返す。"""
    # oracle の切り詰め対象は、表示用変換前の prompt/output そのものである。
    return value[:80].replace("\n", "\\n")
