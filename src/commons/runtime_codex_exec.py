"""Codex exec の出力検証・補正と、回復待ち後の同一 call 再開を制御する。"""

import json
import subprocess
import threading
import time
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import SchemaError, validators

from basic.acp import AgentCallParameter
from basic.path_model import AgentCallPathContext
from config.cmoc_config import CmocConfig

from .runtime_codex_logging import format_codex_call_error
from .runtime_codex_profile import (
    classify_codex_call,
    codex_error_text,
    codex_subprocess_env,
    extract_resume_token,
    prepare_codex_override_args,
    prepare_schema,
    read_output_json,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from .runtime_codex_recovery import (
    CodexOutcome,
    RecoveryReason,
    check_recovery_interruption,
    current_recovery_cancellation,
    wait_for_recovery,
)
from .runtime_config import load_config
from .runtime_errors import CmocError
from .runtime_feedback import begin_feedback_call
from .runtime_feedback_store import rfc3339_now, sha256_bytes, uuid7_prefixed
from .runtime_git import (
    WorktreeSnapshot,
    capture_worktree_snapshot,
    restore_worktree_snapshot,
)
from .runtime_logging import SubcommandLogger, current_subcommand_logger
from .runtime_paths import (
    _reserve_timestamped_path,
    codex_log_dir,
    timestamp,
)
from .runtime_results import (
    CodexExecResult,
    StructuredOutputPostcondition,
    StructuredOutputValidationIssue,
)

_MAX_OUTPUT_CORRECTIONS = 2
_CODEX_LOG_TIMESTAMP_LOCK = threading.Lock()
_LAST_CODEX_LOG_TIMESTAMPS: dict[Path, str] = {}


def _write_prompt_log(path: Path, prompt: str) -> None:
    """Codex に渡した完全 prompt を再実行可能な stdin log として保存する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # prompt log 自体を再実行可能な stdin source とし、metadata にはしない。
    path.write_text(prompt, encoding="utf-8")


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def _reject_non_json_constant(value: str) -> Any:
    """JSON 仕様外の非有限数リテラルを JSON input から拒否する。"""
    raise ValueError(f"non-standard JSON constant: {value}")


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
        return json.loads(text, parse_constant=_reject_non_json_constant)
    except (RecursionError, ValueError) as exc:
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
    # Codex の root parser が受理する共通の設定上書きは `exec` より前へ置く。
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
    # 一時障害の確認間隔は未確定なので、runtime の暫定値として 5 分を使う。
    transient_poll_interval_sec: float = 300.0,
    probe_timeout_sec: float = 120.0,
    quota_poll_interval_sec: float = 1800.0,
    subcommand_logger: SubcommandLogger | None = None,
) -> CodexExecResult:
    """Codex exec の再試行、Structured Output 補正、実行記録を一括制御する。"""
    # 設定の外部変更を correction・probe・resume へ持ち込まない。
    check_recovery_interruption()
    path_context = AgentCallPathContext(parameter.agent_call_cwd)
    root = root or path_context.repo_root
    config = deepcopy(config or load_config(path_context.work_root))
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
            schema_definition = json.loads(
                schema_path.read_text(encoding="utf-8"),
                parse_constant=_reject_non_json_constant,
            )
            validator_class = validators.validator_for(schema_definition)
            validator_class.check_schema(schema_definition)
            schema_validator = validator_class(schema_definition)
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            ValueError,
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
    # Structured Output correction 全体で共有する論理 agent call ID を先に固定する。
    agent_call_id = uuid7_prefixed("agc_")
    active_agent_call_id = agent_call_id
    active_agent_call_kind = parameter.agent_call_kind
    active_codex_call_id: str | None = None

    def _call_data(
        run_parameter: AgentCallParameter,
        run_codex_home: Path,
        run_agent_call_cwd: Path,
        run_config: CmocConfig = config,
    ) -> dict[str, str]:
        """call log に残す論理値を実際の呼び出し parameter に揃える。"""
        call_config = run_config.codex.agent_calls[run_parameter.agent_call_kind]
        return {
            "codex_home": str(run_codex_home),
            "agent_call_kind": run_parameter.agent_call_kind,
            "model_provider": call_config.model_provider,
            "model": call_config.model,
            "reasoning_effort": call_config.reasoning_effort,
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
        timeout: float | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """prompt logをstdinとしてCodex subprocessを起動する。"""
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # prompt log file は `codex exec ... -` の stdin source である。
        check_recovery_interruption()
        with run_prompt_path.open(encoding="utf-8") as prompt_file:
            return run_codex_subprocess(
                run_argv,
                cwd=run_agent_call_cwd,
                stdin=prompt_file,
                text=True,
                encoding="utf-8",
                capture_output=True,
                env=run_codex_env,
                timeout=timeout,
                cancellation=current_recovery_cancellation(),
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
        run_agent_call_id: str | None = None,
        run_codex_call_id: str | None = None,
    ) -> None:
        """後から実行条件を追跡できる call log JSON を保存する。"""
        path.write_text(
            json.dumps(
                {
                    "purpose": run_purpose,
                    "timestamp": run_ts,
                    "argv": run_argv,
                    "agent_call_id": run_agent_call_id or active_agent_call_id,
                    "codex_call_id": run_codex_call_id or active_codex_call_id,
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
    transient_wait_sec = 0.0
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
        run_codex_home: Path = codex_home,
    ) -> None:
        """Codex call の結果を subcommand log へ記録する。"""
        elapsed_sec = time.perf_counter() - started_at
        if logger is None:
            return
        payload: dict[str, Any] = {
            "purpose": run_purpose,
            "status": status,
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "quota_wait_sec": quota_wait_sec,
            "transient_wait_sec": transient_wait_sec,
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
        payload.update(
            {
                "agent_call_id": active_agent_call_id,
                "agent_call_kind": active_agent_call_kind,
                "codex_call_id": active_codex_call_id,
            }
        )
        logger.event("codex_call", **payload)

    def _emit_structured_output_exhausted(
        last_failure_stage: str,
        run_call_path: Path,
    ) -> None:
        """正式出力を得られなかった stable diagnostic event を記録する。"""
        if logger is None or schema_path is None:
            return
        try:
            logger.event(
                "codex.structured_output_validation_exhausted",
                event_schema_version=1,
                event_id=uuid7_prefixed("evt_"),
                event_type="codex.structured_output_validation_exhausted",
                occurred_at=rfc3339_now(),
                subcommand_invocation_id=logger.invocation_id,
                agent_call_id=active_agent_call_id,
                agent_call_kind=active_agent_call_kind,
                codex_call_id=active_codex_call_id,
                codex_session_id=correction_session_id or resume_session_id,
                call_log_path=str(run_call_path),
                schema_sha256=sha256_bytes(schema_path.read_bytes()),
                last_failure_stage=last_failure_stage,
            )
        except BaseException:
            # diagnostic の記録失敗を正式な Structured Output error へ混ぜない。
            return

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
        emit_exhausted: bool = True,
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
            if emit_exhausted:
                _emit_structured_output_exhausted("artifact_changed", run_call_path)
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
        if emit_exhausted:
            _emit_structured_output_exhausted("artifact_changed", run_call_path)
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
            transient_wait_sec=transient_wait_sec,
            quota_polls=quota_polls,
        )

    output_corrections = 0
    quota_polls = 0
    resume_session_id: str | None = None
    correction_session_id: str | None = None
    recovery_source_call_id: str | None = None
    current_prompt = parameter.prompt
    frozen_artifact_snapshot: WorktreeSnapshot | None = None
    artifact_changed_paths: frozenset[str] = frozenset()

    def _probe_recovery(
        reason: RecoveryReason, inherited: bool, recovery_id: str
    ) -> CodexOutcome:
        # probe は独立した agent call。元の session や output correction を使わない。
        nonlocal active_agent_call_id, active_agent_call_kind, active_codex_call_id
        nonlocal quota_polls
        check_recovery_interruption()
        probe_parameter = _quota_availability_probe_parameter(parameter)
        probe_config = deepcopy(config)
        if inherited:
            probe_config.codex.agent_calls[probe_parameter.agent_call_kind] = (
                config.codex.agent_calls[parameter.agent_call_kind]
            )
        probe_agent_call_cwd = AgentCallPathContext(
            probe_parameter.agent_call_cwd
        ).agent_call_cwd
        probe_codex_home = codex_home
        probe_args = prepare_codex_override_args(probe_parameter, probe_config)
        probe_call_data = _call_data(
            probe_parameter, probe_codex_home, probe_agent_call_cwd, probe_config
        )
        probe_call_data.update(
            recovery_id=recovery_id,
            stopped_agent_call_id=agent_call_id,
            stopped_codex_call_id=recovery_source_call_id or "",
        )
        active_agent_call_id = uuid7_prefixed("agc_")
        active_agent_call_kind = probe_parameter.agent_call_kind
        active_codex_call_id = uuid7_prefixed("cdc_")
        probe_ts, probe_prompt, probe_stdout, probe_stderr, probe_output, probe_call = (
            _new_log_paths()
        )
        probe_argv = _base_exec_argv(probe_args, probe_agent_call_cwd)
        probe_argv.extend(["--json", "--output-last-message", str(probe_output), "-"])
        probe_purpose = (
            "quota availability probe"
            if reason == "quota"
            else "transient recovery probe"
        )
        _write_prompt_log(probe_prompt, probe_parameter.prompt)
        _write_call_log(
            probe_call,
            run_purpose=probe_purpose,
            run_ts=probe_ts,
            run_argv=probe_argv,
            run_prompt_path=probe_prompt,
            run_stdout_path=probe_stdout,
            run_stderr_path=probe_stderr,
            run_output_path=probe_output,
            run_schema_path=None,
            run_call_data=probe_call_data,
        )
        started_at = time.perf_counter()
        probe_feedback = begin_feedback_call(
            agent_call_cwd=probe_agent_call_cwd,
            agent_call_id=active_agent_call_id,
            agent_call_kind=active_agent_call_kind,
            codex_call_id=active_codex_call_id,
            log_paths=[probe_call, probe_prompt, probe_stdout, probe_stderr],
        )
        outcome: CodexOutcome = "failed"
        returncode = None
        error = None
        try:
            if reason == "quota":
                quota_polls += 1
            poll = _run_with_prompt_file(
                probe_argv,
                probe_prompt,
                run_agent_call_cwd=probe_agent_call_cwd,
                run_codex_env=probe_feedback.subprocess_env(codex_env),
                timeout=probe_timeout_sec,
            )
            probe_stdout.write_text(poll.stdout, encoding="utf-8")
            probe_stderr.write_text(poll.stderr, encoding="utf-8")
            returncode = poll.returncode
            outcome = classify_codex_call(poll.stdout, poll.returncode)
            if outcome == "succeeded":
                # builder は固定 literal を指定しないため、短い非空応答を確認する。
                try:
                    response = probe_output.read_text(encoding="utf-8")
                except (FileNotFoundError, UnicodeError):
                    response = ""
                if not response.strip() or len(response) > 4096:
                    outcome = "failed"
            if outcome != "succeeded":
                error = (
                    codex_error_text(poll.stdout, poll.stderr)
                    or "probe response unavailable"
                )
            check_recovery_interruption()
            return outcome
        except subprocess.TimeoutExpired as exc:
            # 部分 stdout の既知 marker だけで、無応答を以前の理由へ分類しない。
            for path, content in (
                (probe_stdout, exc.stdout),
                (probe_stderr, exc.stderr),
            ):
                path.write_text(
                    content.decode("utf-8", errors="replace")
                    if isinstance(content, bytes)
                    else content or "",
                    encoding="utf-8",
                )
            error = "recovery probe timed out"
            return "failed"
        except BaseException as exc:
            error = format_codex_call_error(exc)
            outcome = "failed"
            raise
        finally:
            probe_feedback.close()
            _emit_codex_call_event(
                run_purpose=probe_purpose,
                run_call_path=probe_call,
                run_prompt_path=probe_prompt,
                run_stdout_path=probe_stdout,
                run_stderr_path=probe_stderr,
                run_output_path=probe_output,
                run_schema_path=None,
                started_at=started_at,
                returncode=returncode,
                status=f"{outcome}_waiting"
                if outcome in {"quota", "transient"}
                else outcome,
                error=error,
                run_codex_home=probe_codex_home,
            )

    while True:
        check_recovery_interruption()
        ts, prompt_path, stdout_path, stderr_path, output_path, call_path = (
            _new_log_paths()
        )
        active_agent_call_id = agent_call_id
        active_agent_call_kind = parameter.agent_call_kind
        active_codex_call_id = uuid7_prefixed("cdc_")
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
            run_call_data={
                **base_call_data,
                **(
                    {"resumed_from_codex_call_id": recovery_source_call_id}
                    if recovery_source_call_id
                    else {}
                ),
            },
        )
        attempt_started_at = time.perf_counter()
        feedback_call = begin_feedback_call(
            agent_call_cwd=agent_call_cwd,
            agent_call_id=active_agent_call_id,
            agent_call_kind=active_agent_call_kind,
            codex_call_id=active_codex_call_id,
            codex_session_id=resume_session_id,
            log_paths=[
                call_path,
                prompt_path,
                stdout_path,
                stderr_path,
            ],
        )
        try:
            result = _run_with_prompt_file(
                current_argv,
                prompt_path,
                run_codex_env=feedback_call.subprocess_env(codex_env),
            )
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
                emit_exhausted=not isinstance(exc, KeyboardInterrupt),
            )
            startup_error = format_codex_call_error(exc)
            if (
                not isinstance(exc, KeyboardInterrupt)
                and schema_path is not None
                and output_corrections > 0
            ):
                _emit_structured_output_exhausted("resume_unavailable", call_path)
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
            )
            raise
        finally:
            feedback_call.close()
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
        # 最終 outcome を先に確定し、途中の error と回復済みの成功を区別する。
        check_recovery_interruption()
        resume_session_id = resume_session_id or _extract_session_id_from_stdout_log(
            stdout_path
        )
        outcome = classify_codex_call(result.stdout, result.returncode)
        if outcome != "succeeded":
            if outcome in {"quota", "transient"}:
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
                    status=f"{outcome}_waiting",
                    error=error_text,
                )
                assert active_codex_call_id is not None
                recovery_source_call_id = active_codex_call_id
                try:
                    waited = wait_for_recovery(
                        key=(
                            logger.invocation_id if logger else root.resolve(),
                            agent_call_cwd.resolve(),
                            codex_home.resolve(),
                            tuple(sorted(codex_env.items())),
                            tuple(override_args),
                            repr(config.codex),
                            current_recovery_cancellation(),
                        ),
                        reason=outcome,
                        probe=_probe_recovery,
                        quota_interval=quota_poll_interval_sec,
                        transient_interval=transient_poll_interval_sec,
                        logger=logger,
                        agent_call_id=agent_call_id,
                        stopped_codex_call_id=recovery_source_call_id,
                        call_log_path=str(call_path),
                    )
                except Exception:
                    # probe の失敗でも、正式出力を失った本来の call を記録する。
                    active_agent_call_id = agent_call_id
                    active_agent_call_kind = parameter.agent_call_kind
                    active_codex_call_id = recovery_source_call_id
                    _emit_structured_output_exhausted("resume_unavailable", call_path)
                    raise
                quota_wait_sec += waited["quota"]
                transient_wait_sec += waited["transient"]
                continue
            if schema_path is not None and output_corrections > 0:
                _emit_structured_output_exhausted("resume_unavailable", call_path)
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
                _emit_structured_output_exhausted(
                    "deterministic_postcondition", call_path
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
                    correction_session_id = resume_session_id
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
                if failure_reason == "Codex session ID is unavailable":
                    last_failure_stage = "resume_unavailable"
                elif any(
                    issue.condition == "JSON parse" for issue in validation_issues
                ):
                    last_failure_stage = "json_parse"
                elif any(
                    issue.condition.startswith("JSON Schema keyword")
                    for issue in validation_issues
                ):
                    last_failure_stage = "schema_validation"
                else:
                    last_failure_stage = "deterministic_postcondition"
                _emit_structured_output_exhausted(last_failure_stage, call_path)
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
            transient_wait_sec=transient_wait_sec,
            quota_polls=quota_polls,
        )
        return exec_result
