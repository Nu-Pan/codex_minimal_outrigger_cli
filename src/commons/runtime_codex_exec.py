"""1 回の agent call に含まれる Codex call の実行ループを扱う。

このファイルは 16,000 文字を超えるが、Structured Output 検証・補正、capacity
retry、quota 代表 probe、resume 継続は同じ subprocess 結果、call log、
subcommand event、補正・retry counter を共有する 1 つの状態機械である。TUI 起動は
別 module へ分け、exec の分岐だけをここに残すことで責務境界を exec 実行制御
へ限定している。quota 処理だけをさらに分離すると、resume session ID と log/event
の読み取り文脈が呼び出し元と分断されるため、現状は一体で読む方が凝集性が高い。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import subprocess
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import SchemaError, validators

from basic.acp import AgentCallParameter
from basic.path_model import AgentCallPathContext
from config.cmoc_config import CmocConfig

from .runtime_codex_logging import (
    emit_codex_call_console,
    format_codex_call_error,
)
from .runtime_codex_profile import (
    codex_error_text,
    codex_subprocess_env,
    extract_resume_token,
    is_capacity_error,
    is_quota_error,
    is_unexpected_error,
    prepare_codex_override_args,
    prepare_schema,
    read_output_json,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from .runtime_config import load_config
from .runtime_errors import CmocError
from .runtime_git import (
    WorktreeSnapshot,
    capture_worktree_snapshot,
    restore_worktree_snapshot,
)
from .runtime_logging import SubcommandLogger, current_subcommand_logger
from .runtime_paths import (
    _reserve_timestamped_path,
    codex_log_dir,
    console_timestamp,
    timestamp,
)
from .runtime_results import (
    CodexExecResult,
    StructuredOutputPostcondition,
    StructuredOutputValidationIssue,
)

_QUOTA_CONDITION = threading.Condition()
_QUOTA_POLLING = False
_QUOTA_PROBE_AVAILABLE = False
_QUOTA_PROBE_ERROR: BaseException | None = None
_MAX_OUTPUT_CORRECTIONS = 2
_CODEX_LOG_TIMESTAMP_LOCK = threading.Lock()
_LAST_CODEX_LOG_TIMESTAMPS: dict[Path, str] = {}


def _write_prompt_log(path: Path, prompt: str) -> None:
    """Codex に渡した完全 prompt を再実行可能な stdin log として保存する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # prompt log 自体を再実行可能な stdin source とし、metadata にはしない。
    path.write_text(prompt, encoding="utf-8")


def _read_required_output_json(path: Path) -> Any:
    """Structured Output の必須 JSON を機械的検証用に厳格に読み取る。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # 欠落、空、malformed な output は JSON parse 不合格として補正対象にする。
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"output file does not exist: {path}") from exc
    if not text.strip():
        raise ValueError(f"output file is empty: {path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"output file is not valid JSON: {exc}") from exc


def _display_validation_value(value: Any, *, limit: int = 1000) -> str:
    """補正に必要な観測値を、prompt を過大化しない JSON 表現へ整える。"""
    try:
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError):
        rendered = repr(value)
    if len(rendered) <= limit:
        return rendered
    return f"{rendered[:limit]}... (truncated, {len(rendered)} characters total)"


def _parse_validation_issue(
    path: Path, exc: Exception
) -> StructuredOutputValidationIssue:
    """JSON parse failure を補正 prompt 用の共通表現へ変換する。"""
    if isinstance(exc.__cause__, json.JSONDecodeError):
        cause = exc.__cause__
        assert isinstance(cause, json.JSONDecodeError)
        location = f"line {cause.lineno}, column {cause.colno}, character {cause.pos}"
    else:
        location = str(path)
    return StructuredOutputValidationIssue(
        condition="JSON parse",
        location=location,
        expected="UTF-8 で符号化された空でない有効な JSON document",
        observed=str(exc),
    )


def _schema_validation_issues(
    output: Any, schema_validator: Any
) -> tuple[StructuredOutputValidationIssue, ...]:
    """JSON Schema 違反を field ごとの補正可能なエラーへ変換する。"""
    errors = sorted(
        schema_validator.iter_errors(output),
        key=lambda error: (str(getattr(error, "json_path", "$")), error.message),
    )
    return tuple(
        StructuredOutputValidationIssue(
            condition=f"JSON Schema keyword `{error.validator}`",
            location=str(getattr(error, "json_path", "$")),
            expected=_display_validation_value(error.validator_value),
            observed=_display_validation_value(error.instance),
        )
        for error in errors
    )


def _validate_structured_output(
    path: Path,
    schema_validator: Any,
    postcondition: StructuredOutputPostcondition | None,
    changed_paths: frozenset[str],
) -> tuple[Any, tuple[StructuredOutputValidationIssue, ...]]:
    """parse、schema、宣言済み事後条件を順番どおり検証する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    try:
        output = _read_required_output_json(path)
    except (UnicodeError, ValueError) as exc:
        return None, (_parse_validation_issue(path, exc),)
    issues = _schema_validation_issues(output, schema_validator)
    if issues or postcondition is None:
        return output, issues
    postcondition_issues = tuple(postcondition(output, changed_paths))
    if any(
        not isinstance(issue, StructuredOutputValidationIssue)
        for issue in postcondition_issues
    ):
        raise TypeError(
            "structured output postcondition must return validation issue objects"
        )
    return output, postcondition_issues


def _render_validation_issues(
    issues: tuple[StructuredOutputValidationIssue, ...],
) -> str:
    """検証エラーの四要素を補正 prompt と failure detail に共通利用する。"""
    sections: list[str] = []
    for index, issue in enumerate(issues, start=1):
        sections.extend(
            [
                f"### {index}",
                "",
                f"- 違反した条件: {issue.condition}",
                f"- 対象 field または位置: {issue.location}",
                f"- 期待値: {issue.expected}",
                f"- 観測値: {issue.observed}",
                "",
            ]
        )
    return "\n".join(sections).rstrip()


def _build_output_correction_prompt(
    issues: tuple[StructuredOutputValidationIssue, ...],
) -> str:
    """初回 prompt を加工せず、同じ session の次 turn 用入力を構築する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    return "\n".join(
        [
            "# Structured Output の出力補正",
            "",
            "直前の Structured Output は、初回 prompt で宣言済みの機械的検証に合格しませんでした。",
            "作業成果物を変更せず、初回と同じ schema に従う完全な置換出力を返してください。",
            "差分、patch、または不合格出力の一部分だけを返してはいけません。",
            "",
            "## 検証エラー",
            "",
            _render_validation_issues(issues),
            "",
        ]
    )


def _extract_session_id_from_stdout_log(path: Path) -> str | None:
    """Codex call の stdout JSONL log から session ID を取り出す。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # session ID を取得できない場合の扱いは、quota 再開と出力補正で異なるため、
    # 呼び出し側が判断できるよう None を返す。
    try:
        return extract_resume_token(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return None


def _base_exec_argv(override_args: list[str], agent_call_cwd: Path) -> list[str]:
    """cmoc 側で検査済みの cwd と設定上書きを Codex exec argv にする。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # cmoc は linked worktree や生成 root から Codex を実行し得るため、repo の検証は
    # Codex CLI startup ではなく cmoc 自身の preflight が担う。
    # `--ask-for-approval` は Codex の root parser だけが受理するため、
    # 共通の設定上書きは `exec` より前へ置く。
    return [
        "codex",
        *override_args,
        "exec",
        "--skip-git-repo-check",
        "--cd",
        str(agent_call_cwd),
    ]


def _quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    """quota判定用のprobe parameterをcanonical builderから作る。"""
    try:
        from acp.builder.quota_probe import build_quota_availability_probe_parameter

        return build_quota_availability_probe_parameter(base_parameter)
    except (AttributeError, ModuleNotFoundError) as exc:
        raise CmocError(
            "quota availability probe の builder が見つかりません。",
            ["cmoc のインストール内容を確認してから再実行してください。"],
            str(exc),
        ) from exc


def _codex_failure_detail(
    *,
    classification: str,
    returncode: int | None,
    call_path: Path,
    stdout_path: Path,
    stderr_path: Path,
) -> str:
    """失敗した Codex の本文を露出せず、調査先だけを返す。"""
    return "\n".join(
        [
            f"classification: {classification}",
            f"returncode: {returncode if returncode is not None else 'not started'}",
            f"call_log: {call_path}",
            f"stdout_log: {stdout_path}",
            f"stderr_log: {stderr_path}",
        ]
    )


def _next_codex_log_timestamp(log_dir: Path) -> str:
    """log directory ごとに Codex exec log 名を単調増加させる。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # quota retry の時系列は同じ log directory 内だけで保ち、別 repository の
    # 呼び出し履歴で新しい log 名を進めない。
    log_dir = log_dir.resolve()
    with _CODEX_LOG_TIMESTAMP_LOCK:
        current = timestamp()
        last = _LAST_CODEX_LOG_TIMESTAMPS.get(log_dir)
        if last is not None and current <= last:
            try:
                current_dt = datetime.strptime(last[:-3], "%Y-%m-%d_%H-%M_%S_%f")
            except ValueError:
                # canonical timestamp でない値は、path reservation の衝突解消へ委ねる。
                pass
            else:
                current = (current_dt + timedelta(microseconds=1)).strftime(
                    "%Y-%m-%d_%H-%M_%S_%f000"
                )
        _LAST_CODEX_LOG_TIMESTAMPS[log_dir] = current
        return current


def run_codex_exec(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex exec",
    structured_output_postcondition: StructuredOutputPostcondition | None = None,
    max_capacity_retries: int = 8,
    capacity_initial_sleep_sec: float = 5.0,
    quota_poll_interval_sec: float = 1800.0,
    max_quota_polls: int | None = None,
    subcommand_logger: SubcommandLogger | None = None,
) -> CodexExecResult:
    """Codex exec の再試行、Structured Output 補正、実行記録を一括制御する。"""
    path_context = AgentCallPathContext(parameter.agent_call_cwd)
    root = root or path_context.repo_root
    config = config or load_config(path_context.work_root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    agent_call_cwd = path_context.agent_call_cwd
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # 相対 CODEX_HOME は変更せず渡すため、preflight は Codex が実際の cwd から解決する
    # path を対象にする。
    codex_home = resolve_codex_home(agent_call_cwd)
    validate_codex_home(codex_home)
    codex_env = codex_subprocess_env(codex_home)
    override_args = prepare_codex_override_args(
        parameter,
        config,
    )
    schema_path: Path | None = None
    schema_validator: Any | None = None
    schema_source_path = parameter.structured_output_schema_path
    if schema_source_path is not None:
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # `--output-schema` は Codex 自身が linked worktree 内で動く場合も repo-root の
        # local schema store を指さなければならない。source の読み取り・UTF-8 decode、
        # JSON parse、schema validation を同じ local failure として扱う。
        try:
            schema_path = prepare_schema(root, schema_source_path)
            assert schema_path is not None
            schema_definition = json.loads(schema_path.read_text(encoding="utf-8"))
            validator_class = validators.validator_for(schema_definition)
            validator_class.check_schema(schema_definition)
            schema_validator = validator_class(schema_definition)
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            SchemaError,
            TypeError,
            AttributeError,
        ) as exc:
            raise CmocError(
                "Structured Output schema が不正です。",
                [
                    "Structured Output schema の JSON と schema 定義を確認してください。",
                    "schema を修正してから同じ cmoc コマンドを再実行してください。",
                ],
                f"schema: {schema_path or schema_source_path}\nerror: {exc}",
            ) from exc
    elif structured_output_postcondition is not None:
        raise CmocError(
            "Structured Output の決定論的事後条件を検証できません。",
            ["postcondition を Structured Output schema と一緒に指定してください。"],
            "structured_output_schema_path is None",
        )

    artifact_snapshot_before = (
        capture_worktree_snapshot(path_context.work_root)
        if schema_path is not None
        else None
    )

    def _call_data(
        run_parameter: AgentCallParameter,
        run_codex_home: Path,
        run_agent_call_cwd: Path,
    ) -> dict[str, str]:
        """call log に残す論理値を実際の呼び出し parameter に揃える。"""
        return {
            "codex_home": str(run_codex_home),
            "model_class": run_parameter.model_class.value,
            "reasoning_effort": run_parameter.reasoning_effort.value,
            "file_access_mode": run_parameter.file_access_mode.value,
            "cwd": str(run_agent_call_cwd.resolve()),
        }

    base_call_data = _call_data(parameter, codex_home, agent_call_cwd)

    def _new_log_paths() -> tuple[str, Path, Path, Path, Path, Path]:
        """Codex call 用 log path 群を時刻順に追える名前で確保する。"""
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # sibling path を導出する前に O_EXCL で call path を予約する。process-local の
        # timestamp lock だけでは並列 cmoc process を保護できない。
        run_ts, run_call_path = _reserve_timestamped_path(
            log_dir,
            "_call.json",
            lambda: _next_codex_log_timestamp(log_dir),
        )
        return (
            run_ts,
            log_dir / f"{run_ts}_prompt.md",
            log_dir / f"{run_ts}_stdout.jsonl",
            log_dir / f"{run_ts}_stderr.log",
            log_dir / f"{run_ts}_output.json",
            run_call_path,
        )

    def _build_argv(output_path: Path, resume_session_id: str | None) -> list[str]:
        """schema と resume 状態を反映した `codex exec` の argv を組み立てる。"""
        run_argv = _base_exec_argv(override_args, agent_call_cwd)
        run_argv.extend(["--json", "--output-last-message", str(output_path)])
        if schema_path is not None:
            run_argv.extend(["--output-schema", str(schema_path)])
        if resume_session_id:
            run_argv.extend(["resume", resume_session_id])
        run_argv.append("-")
        return run_argv

    def _run_with_prompt_file(
        run_argv: list[str],
        run_prompt_path: Path,
        *,
        run_agent_call_cwd: Path = agent_call_cwd,
        run_codex_env: dict[str, str] = codex_env,
    ) -> subprocess.CompletedProcess[str]:
        """prompt logをstdinとしてCodex subprocessを起動する。"""
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # prompt log file は `codex exec ... -` の stdin source である。
        with run_prompt_path.open(encoding="utf-8") as prompt_file:
            return run_codex_subprocess(
                run_argv,
                cwd=run_agent_call_cwd,
                stdin=prompt_file,
                text=True,
                encoding="utf-8",
                capture_output=True,
                env=run_codex_env,
            )

    def _write_call_log(
        path: Path,
        *,
        run_purpose: str,
        run_ts: str,
        run_argv: list[str],
        run_prompt_path: Path,
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        run_schema_path: Path | None,
        run_call_data: dict[str, str] | None = None,
    ) -> None:
        """後から実行条件を追跡できる call log JSON を保存する。"""
        path.write_text(
            json.dumps(
                {
                    "purpose": run_purpose,
                    "timestamp": run_ts,
                    "argv": run_argv,
                    **(run_call_data or base_call_data),
                    "schema_path": str(run_schema_path) if run_schema_path else None,
                    "prompt_log_path": str(run_prompt_path),
                    "stdout_log_path": str(run_stdout_path),
                    "stderr_log_path": str(run_stderr_path),
                    "output_path": str(run_output_path),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    call_started_at = time.perf_counter()
    quota_wait_sec = 0.0
    logger = subcommand_logger or current_subcommand_logger()

    def _emit_codex_call_event(
        *,
        run_purpose: str,
        run_call_path: Path,
        run_prompt_path: Path,
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        run_schema_path: Path | None,
        started_at: float,
        returncode: int | None,
        status: str,
        error: str | None = None,
        console_error: str | None = None,
        run_codex_home: Path = codex_home,
    ) -> None:
        """console と subcommand log の両方へ Codex call 結果を記録する。"""
        elapsed_sec = time.perf_counter() - started_at
        if console_error is None:
            # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
            # returncode 0 でも malformed JSONL や最終 schema failure は error である。
            # stdout/stderr 本文を console へ漏らさず、固定メッセージだけ stderr へ出す。
            console_error = {
                "failed": "Codex CLI 呼び出しが失敗しました。",
                "structured_output_validation_failed": (
                    "Codex CLI の Structured Output 検証に失敗しました。"
                ),
                "output_correction_failed": (
                    "Codex CLI の Structured Output 補正に失敗しました。"
                ),
            }.get(status)
        emit_codex_call_console(
            run_purpose, run_call_path, elapsed_sec, returncode, console_error
        )
        if logger is None:
            return
        payload: dict[str, Any] = {
            "purpose": run_purpose,
            "status": status,
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "quota_wait_sec": quota_wait_sec,
            "quota_polls": quota_polls,
            "call_log_path": str(run_call_path),
            "prompt_log_path": str(run_prompt_path),
            "stdout_log_path": str(run_stdout_path),
            "stderr_log_path": str(run_stderr_path),
            "output_path": str(run_output_path),
            "codex_home": str(run_codex_home),
            "schema_path": str(run_schema_path) if run_schema_path else None,
        }
        if error is not None:
            payload["error"] = error
        logger.event("codex_call", **payload)

    def _ensure_correction_artifacts_unchanged(
        frozen_snapshot: WorktreeSnapshot | None,
        *,
        run_call_path: Path,
        run_prompt_path: Path,
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        started_at: float,
        returncode: int | None,
    ) -> None:
        """補正 turn の差分変動を復元し、補正不能な失敗として通知する。"""
        if frozen_snapshot is None:
            return
        try:
            current_snapshot = capture_worktree_snapshot(frozen_snapshot.root)
            changed = frozen_snapshot.changed_paths(current_snapshot)
            if not changed:
                return
            restore_worktree_snapshot(frozen_snapshot)
        except Exception as exc:
            detail = f"artifact inspection or restoration failed: {exc!r}"
            _emit_codex_call_event(
                run_purpose=purpose,
                run_call_path=run_call_path,
                run_prompt_path=run_prompt_path,
                run_stdout_path=run_stdout_path,
                run_stderr_path=run_stderr_path,
                run_output_path=run_output_path,
                run_schema_path=schema_path,
                started_at=started_at,
                returncode=returncode,
                status="output_correction_failed",
                error=detail,
            )
            raise CmocError(
                "Structured Output 補正中の作業成果物を復元できませんでした。",
                ["run worktree と Codex call log を確認してください。"],
                detail,
            ) from exc
        detail = "\n".join(
            [
                "correction turn changed work artifacts",
                f"changed paths: {sorted(changed)!r}",
                "restoration: succeeded",
            ]
        )
        _emit_codex_call_event(
            run_purpose=purpose,
            run_call_path=run_call_path,
            run_prompt_path=run_prompt_path,
            run_stdout_path=run_stdout_path,
            run_stderr_path=run_stderr_path,
            run_output_path=run_output_path,
            run_schema_path=schema_path,
            started_at=started_at,
            returncode=returncode,
            status="output_correction_failed",
            error=detail,
        )
        raise CmocError(
            "Structured Output 補正 turn が作業成果物を変更しました。",
            ["復元済みの run worktree と Codex call log を確認してください。"],
            detail,
        )

    def _codex_exec_result_from_paths(
        result: subprocess.CompletedProcess[str],
        *,
        run_call_path: Path,
        run_prompt_path: Path,
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        run_schema_path: Path | None = schema_path,
    ) -> CodexExecResult:
        """保存済みlog pathから一回分のCodex結果を組み立てる。"""
        try:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # output JSON の parse failure は caller が分類するため、壊れた UTF-8 の
            # output-last-message でも結果の組み立て自体を UnicodeDecodeError で中断しない。
            output_text = run_output_path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            output_text = ""
        return CodexExecResult(
            returncode=result.returncode,
            output_text=output_text,
            output_json=read_output_json(run_output_path),
            call_log_path=run_call_path,
            prompt_log_path=run_prompt_path,
            stdout_log_path=run_stdout_path,
            stderr_log_path=run_stderr_path,
            output_path=run_output_path,
            codex_home=codex_home,
            schema_path=run_schema_path,
            elapsed_sec=time.perf_counter() - call_started_at,
            quota_wait_sec=quota_wait_sec,
            quota_polls=quota_polls,
        )

    output_corrections = 0
    capacity_attempts = 0
    quota_polls = 0
    sleep_sec = capacity_initial_sleep_sec
    capacity_retry_pending = False
    resume_session_id: str | None = None
    correction_session_id: str | None = None
    current_prompt = parameter.prompt
    frozen_artifact_snapshot: WorktreeSnapshot | None = None
    artifact_changed_paths: frozenset[str] = frozenset()

    while True:
        ts, prompt_path, stdout_path, stderr_path, output_path, call_path = (
            _new_log_paths()
        )
        current_argv = _build_argv(output_path, resume_session_id)
        _write_prompt_log(prompt_path, current_prompt)
        _write_call_log(
            call_path,
            run_purpose=purpose,
            run_ts=ts,
            run_argv=current_argv,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
            run_schema_path=schema_path,
        )
        attempt_started_at = time.perf_counter()
        try:
            result = _run_with_prompt_file(current_argv, prompt_path)
        except BaseException as exc:
            _ensure_correction_artifacts_unchanged(
                frozen_artifact_snapshot,
                run_call_path=call_path,
                run_prompt_path=prompt_path,
                run_stdout_path=stdout_path,
                run_stderr_path=stderr_path,
                run_output_path=output_path,
                started_at=attempt_started_at,
                returncode=None,
            )
            startup_error = format_codex_call_error(exc)
            _emit_codex_call_event(
                run_purpose=purpose,
                run_call_path=call_path,
                run_prompt_path=prompt_path,
                run_stdout_path=stdout_path,
                run_stderr_path=stderr_path,
                run_output_path=output_path,
                run_schema_path=schema_path,
                started_at=attempt_started_at,
                returncode=None,
                status="failed",
                error=startup_error,
                console_error=startup_error,
            )
            raise
        stdout_path.write_text(result.stdout, encoding="utf-8")
        stderr_path.write_text(result.stderr, encoding="utf-8")
        _ensure_correction_artifacts_unchanged(
            frozen_artifact_snapshot,
            run_call_path=call_path,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
            started_at=attempt_started_at,
            returncode=result.returncode,
        )
        error_text = codex_error_text(result.stdout, result.stderr)
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # retry/wait 挙動は JSONL event で決め、既知の event がない場合だけ exit status を
        # fallback の failure signal とする。
        capacity_error = is_capacity_error(result.stdout)
        quota_error = is_quota_error(result.stdout)
        unexpected_error = is_unexpected_error(result.stdout)
        if result.returncode != 0 or capacity_error or quota_error or unexpected_error:
            if (
                capacity_error
                and not unexpected_error
                and capacity_attempts < max_capacity_retries
            ):
                capacity_attempts += 1
                _emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="capacity_retrying",
                    error=error_text,
                )
                time.sleep(sleep_sec)
                sleep_sec *= 2
                continue
            if quota_error and not unexpected_error:
                global _QUOTA_POLLING, _QUOTA_PROBE_AVAILABLE, _QUOTA_PROBE_ERROR
                _emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="quota_waiting",
                    error=error_text,
                )
                with _QUOTA_CONDITION:
                    if _QUOTA_POLLING:
                        wait_started_at = time.perf_counter()
                        print(
                            "# "
                            f"{console_timestamp()} "
                            "Codex CLI quota wait: waiting for representative probe",
                            flush=True,
                        )
                        _QUOTA_CONDITION.wait_for(lambda: not _QUOTA_POLLING)
                        waited_sec = time.perf_counter() - wait_started_at
                        quota_wait_sec += waited_sec
                        if logger is not None:
                            logger.add_quota_wait(waited_sec)
                        if _QUOTA_PROBE_ERROR is not None:
                            raise _QUOTA_PROBE_ERROR
                        if not _QUOTA_PROBE_AVAILABLE:
                            raise CmocError(
                                "Codex CLI quota 待機の代表 probe が中断しました。",
                                [
                                    "quota 回復後に同じ cmoc コマンドを再実行してください。"
                                ],
                                _codex_failure_detail(
                                    classification="quota wait interrupted",
                                    returncode=result.returncode,
                                    call_path=call_path,
                                    stdout_path=stdout_path,
                                    stderr_path=stderr_path,
                                ),
                            )
                        resume_session_id = correction_session_id or (
                            _extract_session_id_from_stdout_log(stdout_path)
                        )
                        continue
                    _QUOTA_PROBE_AVAILABLE = False
                    _QUOTA_PROBE_ERROR = None
                    _QUOTA_POLLING = True
                try:
                    print(
                        f"# {console_timestamp()} Codex CLI quota wait: entering polling mode",
                        flush=True,
                    )
                except BaseException as exc:
                    with _QUOTA_CONDITION:
                        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
                        # polling を開始できない場合は waiter を解放する。
                        _QUOTA_PROBE_ERROR = exc
                        _QUOTA_POLLING = False
                        _QUOTA_CONDITION.notify_all()
                    raise
                probe_available = False
                probe_error: BaseException | None = None
                try:
                    while True:
                        if (
                            max_quota_polls is not None
                            and quota_polls >= max_quota_polls
                        ):
                            raise CmocError(
                                "Codex CLI quota が枯渇しました。",
                                [
                                    "quota 回復後に同じ cmoc コマンドを再実行してください。"
                                ],
                                _codex_failure_detail(
                                    classification="quota exhausted",
                                    returncode=result.returncode,
                                    call_path=call_path,
                                    stdout_path=stdout_path,
                                    stderr_path=stderr_path,
                                ),
                            )
                        quota_polls += 1
                        if capacity_retry_pending:
                            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
                            # capacity retry は自身の backoff をすでに待っているため、通常の
                            # quota polling interval を追加しない。
                            capacity_retry_pending = False
                        else:
                            if logger is not None:
                                logger.add_quota_wait(quota_poll_interval_sec)
                            quota_wait_sec += quota_poll_interval_sec
                            time.sleep(quota_poll_interval_sec)
                        quota_probe_parameter = _quota_availability_probe_parameter(
                            parameter
                        )
                        probe_agent_call_cwd = AgentCallPathContext(
                            quota_probe_parameter.agent_call_cwd
                        ).agent_call_cwd
                        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
                        # quota probe は別の Codex call なので、最小の AgentCallParameter も
                        # argv/cwd/env を駆動しなければならない。
                        probe_codex_home = resolve_codex_home(probe_agent_call_cwd)
                        validate_codex_home(probe_codex_home)
                        probe_codex_env = codex_subprocess_env(probe_codex_home)
                        probe_override_args = prepare_codex_override_args(
                            quota_probe_parameter,
                            config,
                        )
                        probe_call_data = _call_data(
                            quota_probe_parameter,
                            probe_codex_home,
                            probe_agent_call_cwd,
                        )
                        (
                            probe_ts,
                            probe_prompt_path,
                            probe_stdout_path,
                            probe_stderr_path,
                            probe_output_path,
                            probe_call_path,
                        ) = _new_log_paths()
                        probe_argv = _base_exec_argv(
                            probe_override_args, probe_agent_call_cwd
                        )
                        probe_argv.extend(
                            [
                                "--json",
                                "--output-last-message",
                                str(probe_output_path),
                                "-",
                            ]
                        )
                        _write_prompt_log(
                            probe_prompt_path, quota_probe_parameter.prompt
                        )
                        _write_call_log(
                            probe_call_path,
                            run_purpose="quota availability probe",
                            run_ts=probe_ts,
                            run_argv=probe_argv,
                            run_prompt_path=probe_prompt_path,
                            run_stdout_path=probe_stdout_path,
                            run_stderr_path=probe_stderr_path,
                            run_output_path=probe_output_path,
                            run_schema_path=None,
                            run_call_data=probe_call_data,
                        )
                        probe_started_at = time.perf_counter()
                        try:
                            poll = _run_with_prompt_file(
                                probe_argv,
                                probe_prompt_path,
                                run_agent_call_cwd=probe_agent_call_cwd,
                                run_codex_env=probe_codex_env,
                            )
                        except BaseException as exc:
                            startup_error = format_codex_call_error(exc)
                            _emit_codex_call_event(
                                run_purpose="quota availability probe",
                                run_call_path=probe_call_path,
                                run_prompt_path=probe_prompt_path,
                                run_stdout_path=probe_stdout_path,
                                run_stderr_path=probe_stderr_path,
                                run_output_path=probe_output_path,
                                run_schema_path=None,
                                started_at=probe_started_at,
                                returncode=None,
                                status="failed",
                                error=startup_error,
                                console_error=startup_error,
                                run_codex_home=probe_codex_home,
                            )
                            raise
                        probe_stdout_path.write_text(poll.stdout, encoding="utf-8")
                        probe_stderr_path.write_text(poll.stderr, encoding="utf-8")
                        probe_error_text = codex_error_text(poll.stdout, poll.stderr)
                        probe_quota_error = is_quota_error(poll.stdout)
                        probe_capacity_error = is_capacity_error(poll.stdout)
                        probe_unexpected_error = is_unexpected_error(poll.stdout)
                        probe_available = (
                            poll.returncode == 0
                            and not probe_quota_error
                            and not probe_capacity_error
                            and not probe_unexpected_error
                        )
                        if (
                            probe_capacity_error
                            and not probe_unexpected_error
                            and capacity_attempts < max_capacity_retries
                        ):
                            capacity_attempts += 1
                            quota_polls -= 1
                            _emit_codex_call_event(
                                run_purpose="quota availability probe",
                                run_call_path=probe_call_path,
                                run_prompt_path=probe_prompt_path,
                                run_stdout_path=probe_stdout_path,
                                run_stderr_path=probe_stderr_path,
                                run_output_path=probe_output_path,
                                run_schema_path=None,
                                started_at=probe_started_at,
                                returncode=poll.returncode,
                                status="capacity_retrying",
                                error=probe_error_text,
                                run_codex_home=probe_codex_home,
                            )
                            time.sleep(sleep_sec)
                            sleep_sec *= 2
                            capacity_retry_pending = True
                            continue
                        if not probe_available and (
                            probe_unexpected_error or not probe_quota_error
                        ):
                            _emit_codex_call_event(
                                run_purpose="quota availability probe",
                                run_call_path=probe_call_path,
                                run_prompt_path=probe_prompt_path,
                                run_stdout_path=probe_stdout_path,
                                run_stderr_path=probe_stderr_path,
                                run_output_path=probe_output_path,
                                run_schema_path=None,
                                started_at=probe_started_at,
                                returncode=poll.returncode,
                                status="failed",
                                error=probe_error_text,
                                run_codex_home=probe_codex_home,
                            )
                            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
                            # probe も `codex exec` であり、quota 以外の failure は quota reset
                            # を待っても回復しない。
                            raise CmocError(
                                "Codex CLI quota availability probe が失敗しました。",
                                [
                                    "stderr/stdout log を確認して原因を解消してください。"
                                ],
                                _codex_failure_detail(
                                    classification="quota availability probe failed",
                                    returncode=poll.returncode,
                                    call_path=probe_call_path,
                                    stdout_path=probe_stdout_path,
                                    stderr_path=probe_stderr_path,
                                ),
                            )
                        _emit_codex_call_event(
                            run_purpose="quota availability probe",
                            run_call_path=probe_call_path,
                            run_prompt_path=probe_prompt_path,
                            run_stdout_path=probe_stdout_path,
                            run_stderr_path=probe_stderr_path,
                            run_output_path=probe_output_path,
                            run_schema_path=None,
                            started_at=probe_started_at,
                            returncode=poll.returncode,
                            status="succeeded" if probe_available else "quota_waiting",
                            error=None if probe_available else probe_error_text,
                            run_codex_home=probe_codex_home,
                        )
                        if probe_available:
                            break
                except BaseException as exc:
                    probe_error = exc
                    raise
                finally:
                    with _QUOTA_CONDITION:
                        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
                        # waiter は代表 probe が quota availability を証明した後だけ再開できる。
                        # probe failure は共有する。
                        _QUOTA_PROBE_AVAILABLE = probe_available
                        _QUOTA_PROBE_ERROR = probe_error
                        _QUOTA_POLLING = False
                        _QUOTA_CONDITION.notify_all()
                print(
                    f"# {console_timestamp()} Codex CLI quota wait: resuming work",
                    flush=True,
                )
                resume_session_id = correction_session_id or (
                    _extract_session_id_from_stdout_log(stdout_path)
                )
                continue
            _emit_codex_call_event(
                run_purpose=purpose,
                run_call_path=call_path,
                run_prompt_path=prompt_path,
                run_stdout_path=stdout_path,
                run_stderr_path=stderr_path,
                run_output_path=output_path,
                run_schema_path=schema_path,
                started_at=attempt_started_at,
                returncode=result.returncode,
                status="failed",
                error=error_text,
            )
            raise CmocError(
                "Codex CLI 呼び出しが失敗しました。",
                ["stderr/stdout log を確認して原因を解消してください。"],
                _codex_failure_detail(
                    classification="codex exec failed",
                    returncode=result.returncode,
                    call_path=call_path,
                    stdout_path=stdout_path,
                    stderr_path=stderr_path,
                ),
            )
        if schema_path is not None:
            assert schema_validator is not None
            if frozen_artifact_snapshot is None:
                assert artifact_snapshot_before is not None
                frozen_artifact_snapshot = capture_worktree_snapshot(
                    artifact_snapshot_before.root
                )
                artifact_changed_paths = artifact_snapshot_before.changed_paths(
                    frozen_artifact_snapshot
                )
            try:
                output_json, validation_issues = _validate_structured_output(
                    output_path,
                    schema_validator,
                    structured_output_postcondition,
                    artifact_changed_paths,
                )
            except Exception as exc:
                _emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="structured_output_validation_failed",
                    error=f"structured output validation could not run: {exc!r}",
                )
                raise CmocError(
                    "Structured Output を機械的に検証できませんでした。",
                    [
                        "Codex call log、prompt、schema、および validator の整合性を確認してください。"
                    ],
                    f"schema: {schema_path}\noutput: {output_path}\nerror: {exc!r}",
                ) from exc
            if validation_issues:
                rendered_issues = _render_validation_issues(validation_issues)
                failure_reason: str | None = None
                if output_corrections >= _MAX_OUTPUT_CORRECTIONS:
                    failure_reason = (
                        f"maximum output corrections reached: {_MAX_OUTPUT_CORRECTIONS}"
                    )
                elif correction_session_id is None:
                    correction_session_id = _extract_session_id_from_stdout_log(
                        stdout_path
                    )
                    if correction_session_id is None:
                        failure_reason = "Codex session ID is unavailable"
                if failure_reason is None:
                    output_corrections += 1
                    resume_session_id = correction_session_id
                    current_prompt = _build_output_correction_prompt(validation_issues)
                    _emit_codex_call_event(
                        run_purpose=purpose,
                        run_call_path=call_path,
                        run_prompt_path=prompt_path,
                        run_stdout_path=stdout_path,
                        run_stderr_path=stderr_path,
                        run_output_path=output_path,
                        run_schema_path=schema_path,
                        started_at=attempt_started_at,
                        returncode=result.returncode,
                        status="output_correction_requested",
                        error=rendered_issues,
                    )
                    continue
                detail = "\n".join(
                    [
                        f"schema: {schema_path}",
                        f"output: {output_path}",
                        f"reason: {failure_reason}",
                        "validation errors:",
                        rendered_issues,
                    ]
                )
                _emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="structured_output_validation_failed",
                    error=f"{failure_reason}\n{rendered_issues}",
                )
                raise CmocError(
                    "Codex CLI の Structured Output 検証に失敗しました。",
                    ["Codex call log、schema、および validator を確認してください。"],
                    detail,
                )
        else:
            output_json = read_output_json(output_path)
        _emit_codex_call_event(
            run_purpose=purpose,
            run_call_path=call_path,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
            run_schema_path=schema_path,
            started_at=attempt_started_at,
            returncode=result.returncode,
            status="succeeded",
        )
        exec_result = _codex_exec_result_from_paths(
            result,
            run_call_path=call_path,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
        )
        exec_result = CodexExecResult(
            returncode=exec_result.returncode,
            output_text=exec_result.output_text,
            output_json=output_json,
            call_log_path=call_path,
            prompt_log_path=prompt_path,
            stdout_log_path=stdout_path,
            stderr_log_path=stderr_path,
            output_path=output_path,
            codex_home=codex_home,
            schema_path=schema_path,
            elapsed_sec=exec_result.elapsed_sec,
            quota_wait_sec=quota_wait_sec,
            quota_polls=quota_polls,
        )
        return exec_result
