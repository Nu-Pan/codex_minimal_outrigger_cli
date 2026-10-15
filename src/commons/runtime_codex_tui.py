"""TUI の初回 exec と、保存済み会話への対話移行を管理する。"""

import json
import os
import sys
import threading
from contextlib import closing
from copy import deepcopy
from pathlib import Path
from typing import Any
from uuid import UUID

from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)
from oracle.acp_builder.tui.launch_tui import build_tui_launch_tui_parameter
from oracle.editor_input_handoff.body import EditorInputHandoffSource

from basic.acp import AgentCallParameter, TuiResumeTarget
from basic.path_model import AgentCallPathContext
from config.cmoc_config import CmocConfig

from .runtime_cli import mark_current_tui_process_started
from .runtime_codex_exec import run_codex_exec
from .runtime_codex_profile import (
    classify_codex_call,
    codex_subprocess_env,
    document_search_mcp_override_args,
    prepare_codex_override_args,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from .runtime_codex_recovery import (
    check_recovery_interruption,
    current_recovery_cancellation,
    install_recovery_interruption,
)
from .runtime_codex_session import CodexSessionLease
from .runtime_config import load_config
from .runtime_doctor import run_doctor_preprocess
from .runtime_editor_input_handoff_protocol import editor_input_handoff_subprocess_env
from .runtime_errors import CmocError, TuiStartupCancelled
from .runtime_feedback import begin_feedback_call
from .runtime_ids import is_common_id, new_id
from .runtime_logging import current_execution_id, current_subcommand_logger
from .runtime_paths import codex_log_dir, logs_dir, timestamp, work_root
from .runtime_results import CodexExecResult, CommandResult
from .runtime_windows_toast import (
    create_tui_notification_callback,
    notify_terminal_result,
)

_BUILDERS = {
    "tui": build_tui_launch_tui_parameter,
    "oracle_investigation": build_oracle_investigation_launch_tui_parameter,
}


def _kind(parameter: AgentCallParameter) -> str:
    """正本 builder に対応する workload を識別する。"""
    # 起動管理に別の workload 分類や設定 entry を持ち込まない。
    for kind, builder in _BUILDERS.items():
        if parameter.agent_call_kind == builder.__name__:
            return kind
    raise CmocError(
        "TUI workload の agent call 種別が不正です。",
        ["TUI workload の builder が返したパラメータを使用してください。"],
        f"agent_call_kind: {parameter.agent_call_kind}",
    )


def _session_id(stdout: str) -> str:
    """保存済み JSONL が示す、一意な初回会話 UUID を取得する。"""
    # 最初に見つかった ID だけで、矛盾する stream を受理しない。
    events = [json.loads(line) for line in stdout.splitlines()]
    values = [
        event.get("thread_id")
        for event in events
        if isinstance(event, dict) and event.get("type") == "thread.started"
    ]
    if len(values) != 1 or not isinstance(values[0], str):
        raise ValueError("exactly one initial session UUID is required")
    value = values[0]
    if str(UUID(value)) != value:
        raise ValueError("initial session ID is not a canonical UUID")
    return value


def _event(phase: str, record: dict[str, Any], **fields: Any) -> None:
    """今回の起動段階と、確定した事実を即時保存する。"""
    # この境界だけが、動的な call 記録を JSONL logger へ渡す。
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event("tui_startup", phase=phase, **{**record, **fields})


def _context(parameter: AgentCallParameter) -> dict[str, Any]:
    """workload の保存 cwd から今回の実行環境を導出する。"""
    # 現在の cmoc の cwd で、agent の実行場所を代用しない。
    paths = AgentCallPathContext(parameter.agent_call_cwd)
    logger = current_subcommand_logger()
    return {
        "tui_record_version": 3,
        "execution_id": logger.execution_id if logger else None,
        "subcommand": logger.command if logger else None,
        "tui_kind": _kind(parameter),
        "agent_call_kind": parameter.agent_call_kind,
        "file_access_mode": parameter.file_access_mode.value,
        "cwd": str(paths.agent_call_cwd.resolve()),
        "work_root": str(paths.work_root),
        "repo_root": str(paths.repo_root),
        "codex_home": str(resolve_codex_home(paths.agent_call_cwd).resolve()),
        "resumed_from_execution_id": None,
    }


def _initial_evidence(result: CodexExecResult) -> dict[str, Any]:
    """終了済み初回の成功と、会話・保存記録の対応を照合する。"""
    # exec の終了結果と、保存済みの終端情報を両方確認してから移行する。
    call = json.loads(result.call_log_path.read_text(encoding="utf-8"))
    stdout = result.stdout_log_path.read_text(encoding="utf-8")
    if (
        result.returncode != 0
        or classify_codex_call(stdout, result.returncode) != "succeeded"
    ):
        raise ValueError("initial exec did not succeed")
    if not result.output_path.is_file():
        raise ValueError("initial output was not saved")
    return {
        "initial_status": "succeeded",
        "initial_process_state": "exited",
        "initial_returncode": result.returncode,
        "initial_session_id": _session_id(stdout),
        "initial_execution_id": call["execution_id"],
        "initial_agent_call_id": call["agent_call_id"],
        "initial_codex_call_id": call["codex_call_id"],
        "initial_call_log_path": str(result.call_log_path.resolve()),
        "initial_prompt_log_path": str(result.prompt_log_path.resolve()),
        "initial_stdout_log_path": str(result.stdout_log_path.resolve()),
        "initial_stderr_log_path": str(result.stderr_log_path.resolve()),
        "initial_output_path": str(result.output_path.resolve()),
    }


def _run_codex_tui_process(
    parameter: AgentCallParameter,
    *,
    root: Path,
    config: CmocConfig,
    purpose: str,
    record: dict[str, Any],
    lease: CodexSessionLease,
) -> CommandResult:
    """固定した ID を prompt なしで開き、端末を継承して process 終了を待つ。"""
    # argv・設定・接続は今回の process に属し、過去の call から再使用しない。
    assert parameter.prompt is None
    assert parameter.tui_resume_session_id is not None
    paths = AgentCallPathContext(parameter.agent_call_cwd)
    codex_home = resolve_codex_home(paths.agent_call_cwd)
    validate_codex_home(codex_home)
    overrides = prepare_codex_override_args(parameter, config, path_context=paths)
    agent_call_id = new_id(root, "ac")
    codex_call_id = new_id(root, "cc")
    directory = codex_log_dir(root) / record["execution_id"]
    directory.mkdir(parents=True, exist_ok=True)
    call_path = directory / f"{codex_call_id}_call.json"
    logger = current_subcommand_logger()
    context = {
        **{
            key: value
            for key, value in record.items()
            if key not in {"tui_process_state", "tui_returncode"}
        },
        "agent_call_id": agent_call_id,
        "codex_call_id": codex_call_id,
        "call_log_path": str(call_path.resolve()),
        "prompt_log_path": None,
    }
    callback = None
    feedback_call = None
    call: dict[str, Any] = {}
    attempted = False
    try:
        # 通知の準備・符号化失敗は通知だけを無効化し、TUI 起動を継続する。
        try:
            callback = create_tui_notification_callback(
                record["subcommand"] or purpose, root, parameter.tui_resume_session_id
            )
            if callback is not None:
                overrides = prepare_codex_override_args(
                    parameter,
                    config,
                    path_context=paths,
                    notification_command=callback.command,
                )
        except Exception:
            pass
        overrides.extend(
            document_search_mcp_override_args(
                parameter,
                config,
                path_context=paths,
                codex_call_id=codex_call_id,
                logger=logger,
            )
        )
        # 0.162.1 は指定 ID が見つからなければ終了し、prompt 不在を保持する。
        # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/cli/src/main.rs#L2581-L2612
        # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/tui/src/lib.rs#L1556-L1587
        argv = [
            "codex",
            *overrides,
            "--cd",
            str(paths.agent_call_cwd),
            "resume",
            parameter.tui_resume_session_id,
        ]
        call_config = config.codex.agent_calls[parameter.agent_call_kind]
        call = {
            **context,
            "purpose": purpose,
            "timestamp": timestamp(),
            "argv": argv,
            "model_provider": call_config.model_provider,
            "model": call_config.model,
            "reasoning_effort": call_config.reasoning_effort,
            "process_state": "prepared",
            "returncode": None,
        }

        def save_state(state: str, returncode: int | None = None) -> None:
            # 生成前・生成後・終了後を同じ call と外側の実行へ対応付ける。
            record["tui_process_state"] = state
            record["tui_returncode"] = returncode
            call.update(process_state=state, returncode=returncode)
            call_path.write_text(
                json.dumps(call, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

        save_state("prepared")
        if logger is not None:
            logger.event("tui_process_prepared", **context, process_state="prepared")
        feedback_call = begin_feedback_call(
            agent_call_cwd=paths.agent_call_cwd,
            agent_call_id=agent_call_id,
            agent_call_kind=parameter.agent_call_kind,
            codex_call_id=codex_call_id,
            codex_session_id=parameter.tui_resume_session_id,
            log_paths=[call_path],
            enable_feedback_reporting=parameter.enable_feedback_reporting,
        )
        environment = feedback_call.subprocess_env(codex_subprocess_env(codex_home))
        if parameter.enable_editor_input_handoff_mcp:
            source = None
            if logger is not None:
                source = EditorInputHandoffSource(
                    logger.command,
                    record["execution_id"],
                    codex_call_id,
                    logger.path.resolve(),
                )
                logger.event(
                    "editor_input_handoff_source",
                    subcommand=source.subcommand,
                    execution_id=source.execution_id,
                    codex_call_id=source.codex_call_id,
                    sub_command_log_path=str(source.sub_command_log_path),
                    call_log_path=str(call_path.resolve()),
                )
            environment = editor_input_handoff_subprocess_env(
                environment, paths.repo_root, source
            )

        def process_started() -> None:
            # Popen 成功だけを記録し、会話・入力可能状態は監視しない。
            lease.process_started()
            record["tui_process_state"] = "started"
            mark_current_tui_process_started()
            save_state("started")
            if logger is not None:
                logger.event("tui_process_started", **context, process_state="started")
            if (
                record.get("initial_status") == "succeeded"
                and record["resumed_from_execution_id"] is None
            ):
                try:
                    notify_terminal_result(
                        record["subcommand"] or purpose, root, "initial_completed"
                    )
                except BaseException:
                    pass

        try:
            attempted = True
            result = run_codex_subprocess(
                argv,
                cwd=paths.agent_call_cwd,
                env=environment,
                process_started_callback=process_started,
            )
        except BaseException as exc:
            stopped_returncode = getattr(exc, "cmoc_process_returncode", None)
            if isinstance(stopped_returncode, int):
                lease.process_stopped()
                save_state("exited", stopped_returncode)
            elif record["tui_process_state"] == "started":
                save_state("unknown")
            else:
                save_state("spawn_failed")
            raise
        else:
            lease.process_stopped()
            save_state("exited", result.returncode)
        finally:
            if logger is not None:
                logger.event(
                    "tui_process_finished",
                    **context,
                    process_state=record["tui_process_state"],
                    returncode=record["tui_returncode"],
                )
        if result.returncode != 0:
            raise CmocError(
                "Codex TUI が異常終了しました。",
                ["対象の実行 ID と Codex call log を確認してください。"],
                f"session_id: {parameter.tui_resume_session_id}\ncall_log: {call_path}\nreturncode: {result.returncode}",
            )
        return CommandResult(result.returncode, "", "")
    finally:
        try:
            # 起動前の接続準備失敗も、生成失敗と区別して終了記録に残す。
            if call and not attempted:
                record["tui_process_state"] = "not_started"
                call.update(process_state="not_started")
                call_path.write_text(
                    json.dumps(call, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                if logger is not None:
                    logger.event(
                        "tui_process_finished",
                        **context,
                        process_state="not_started",
                        returncode=None,
                    )
        finally:
            try:
                if feedback_call is not None:
                    feedback_call.close()
            finally:
                if callback is not None:
                    try:
                        callback.close()
                    except BaseException:
                        pass


def _resume(
    parameter: AgentCallParameter,
    root: Path,
    config: CmocConfig,
    purpose: str,
    record: dict[str, Any],
    lease: CodexSessionLease,
) -> CommandResult:
    """固定した ID と由来を起動前に保存し、実際の process 結果を保持する。"""
    # 初回 exec の ID と指定値を対応付け、観測した実会話とは記録しない。
    if record["execution_id"] is None:
        record["execution_id"] = current_execution_id(root)
    record.update(
        fixed_session_id=parameter.tui_resume_session_id,
        session_id_source=(
            {"kind": "resume", "execution_id": record["resumed_from_execution_id"]}
            if record["resumed_from_execution_id"] is not None
            else {
                "kind": "initial_exec",
                "codex_call_id": record.get("initial_codex_call_id"),
            }
        ),
        tui_process_state="not_started",
        tui_returncode=None,
    )
    _event("resume_prepared", record)
    try:
        result = _run_codex_tui_process(
            parameter,
            root=root,
            config=config,
            purpose=purpose,
            record=record,
            lease=lease,
        )
    except BaseException:
        _event("tui_failed", record)
        raise
    _event("tui_finished", record)
    return result


def run_codex_tui(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex tui",
) -> CommandResult:
    """完全 prompt を初回 exec で実行し、検査済み UUID への対話再開を準備する。"""
    # 補完 probe では、初回作業も再開の資源準備も開始しない。
    if "_CMOC_COMPLETE" in os.environ:
        return CommandResult(0, "", "")
    paths = AgentCallPathContext(parameter.agent_call_cwd)
    root = root or paths.repo_root
    validate_codex_home(resolve_codex_home(paths.agent_call_cwd))
    config = deepcopy(config or load_config(paths.work_root))
    with closing(CodexSessionLease(resolve_codex_home(paths.agent_call_cwd))) as lease:
        record = _context(parameter)
        if parameter.prompt is None:
            assert parameter.tui_resume_session_id is not None
            lease.acquire(parameter.tui_resume_session_id)
            return _resume(parameter, root, config, purpose, record, lease)
        restore = None
        if (
            current_recovery_cancellation() is None
            and threading.current_thread() is threading.main_thread()
        ):
            restore = install_recovery_interruption()
        try:
            check_recovery_interruption()
            _event("initial_running", record)
            print("初回応答を生成中", file=sys.stderr, flush=True)
            result = run_codex_exec(
                parameter,
                root=root,
                config=config,
                purpose=purpose,
                tui_session_lease=lease,
            )
            check_recovery_interruption()
            try:
                record.update(_initial_evidence(result))
                if record["execution_id"] is None:
                    record["execution_id"] = record["initial_execution_id"]
            except (OSError, ValueError, KeyError, TypeError) as exc:
                _event("initial_record_failed", record)
                raise CmocError(
                    "初回 exec の再開に必要な記録を確認できません。",
                    ["Codex call log と保存出力を確認してください。"],
                    str(exc),
                ) from exc
            if (
                str(resolve_codex_home(paths.agent_call_cwd).resolve())
                != record["codex_home"]
            ):
                raise CmocError(
                    "Codex home が初回 exec の環境と一致しません。",
                    ["初回に使用した Codex home を確認してください。"],
                    record["codex_home"],
                )
            lease.acquire(record["initial_session_id"])
            resume = _BUILDERS[record["tui_kind"]](
                resume=TuiResumeTarget(
                    record["initial_session_id"], paths.agent_call_cwd
                )
            )
            check_recovery_interruption()
        except KeyboardInterrupt as exc:
            _event("initial_cancelled", record, initial_status="cancelled")
            raise TuiStartupCancelled from exc
        except BaseException:
            _event("initial_failed", record)
            raise
        finally:
            if restore is not None:
                restore()
        return _resume(resume, root, config, purpose, record, lease)


def _validate_initial_process_records(
    rows: list[dict[str, Any]], record: dict[str, Any]
) -> None:
    """今回実行した初回 exec と、引き継いだ成功の根拠を区別する。"""
    # 公開 resume は初回を再実行せず、自身のログに保存した根拠を使う。
    initial = [row for row in rows if row.get("event") == "tui_initial_exec"]
    if record["resumed_from_execution_id"] is not None:
        if initial:
            raise ValueError("public resume unexpectedly contains an initial exec")
        return
    states = [row.get("process_state") for row in initial]
    if (
        len(states) < 3
        or states[0] != "prepared"
        or states[-1] != "exited"
        or any(state != "started" for state in states[1:-1])
        or initial[-1].get("status") != "succeeded"
        or type(initial[-1].get("returncode")) is not int
        or initial[-1]["returncode"] != 0
    ):
        raise ValueError("initial process success or exit is unconfirmed")
    for row in initial:
        for key in (
            "execution_id",
            "agent_call_id",
            "codex_call_id",
            "call_log_path",
            "prompt_log_path",
            "stdout_log_path",
            "stderr_log_path",
            "output_path",
        ):
            if row[key] != record[f"initial_{key}"]:
                raise ValueError(f"initial process {key} is inconsistent")
        if row.get("cancel_requested") or (
            row.get("codex_session_id") is not None
            and row["codex_session_id"] != record["initial_session_id"]
        ):
            raise ValueError("initial cancellation or session ID is inconsistent")


def _validate_tui_process_records(
    rows: list[dict[str, Any]], record: dict[str, Any], root: Path
) -> None:
    """生成と終了の対応を検査し、会話の内部状態を再開条件にしない。"""
    # 同一 invocation の workload・環境・固定 ID が途中で変わっていないことを確認する。
    fields = (
        "tui_record_version",
        "execution_id",
        "subcommand",
        "tui_kind",
        "agent_call_kind",
        "file_access_mode",
        "cwd",
        "work_root",
        "repo_root",
        "codex_home",
        "resumed_from_execution_id",
        "fixed_session_id",
        "session_id_source",
    )
    related = [
        row
        for row in rows
        if row.get("event")
        in {
            "tui_startup",
            "tui_process_prepared",
            "tui_process_started",
            "tui_process_finished",
        }
    ]
    evidence_fields = tuple(key for key in record if key.startswith("initial_"))
    for row in related:
        for key in (*fields, *evidence_fields):
            if key in row and row[key] != record.get(key):
                raise ValueError(f"inconsistent TUI {key}")
    if record["fixed_session_id"] != record["initial_session_id"]:
        raise ValueError("fixed session ID differs from initial exec")
    source = record["session_id_source"]
    if record["resumed_from_execution_id"] is None:
        if source != {
            "kind": "initial_exec",
            "codex_call_id": record["initial_codex_call_id"],
        }:
            raise ValueError("initial session ID source is inconsistent")
    elif not is_common_id(record["resumed_from_execution_id"], "exec") or source != {
        "kind": "resume",
        "execution_id": record["resumed_from_execution_id"],
    }:
        raise ValueError("resume session ID source is inconsistent")
    processes = [row for row in related if row["event"] != "tui_startup"]
    state = record["tui_process_state"]
    if not processes:
        if state != "not_started" or record["tui_returncode"] is not None:
            raise ValueError("TUI process exit is unconfirmed")
        return
    names = [row["event"] for row in processes]
    expected = ["tui_process_prepared", "tui_process_finished"]
    if state == "exited":
        expected.insert(1, "tui_process_started")
    elif state not in {"not_started", "spawn_failed"}:
        raise ValueError("TUI process exit is unconfirmed")
    if names != expected:
        raise ValueError("TUI process lifecycle is incomplete or inconsistent")
    prepared, finished = processes[0], processes[-1]
    if prepared["process_state"] != "prepared" or (
        state == "exited" and processes[1]["process_state"] != "started"
    ):
        raise ValueError("TUI process generation is inconsistent")
    code = finished["returncode"]
    if (
        finished["process_state"] != state
        or code != record["tui_returncode"]
        or (state == "exited" and type(code) is not int)
        or (state != "exited" and code is not None)
    ):
        raise ValueError("TUI process result is inconsistent")
    for key, prefix in (("agent_call_id", "ac"), ("codex_call_id", "cc")):
        if not is_common_id(prepared[key], prefix) or any(
            row[key] != prepared[key] for row in processes
        ):
            raise ValueError(f"TUI {key} is inconsistent")
    path = (
        codex_log_dir(root)
        / record["execution_id"]
        / f"{prepared['codex_call_id']}_call.json"
    )
    if prepared["call_log_path"] != str(path.resolve()):
        raise ValueError("TUI call log path is inconsistent")
    call = json.loads(path.read_text(encoding="utf-8"))
    for key in (
        *fields,
        "agent_call_id",
        "codex_call_id",
        "call_log_path",
        "prompt_log_path",
    ):
        if key not in prepared or call[key] != prepared[key]:
            raise ValueError(f"TUI call log {key} is inconsistent")
    if (
        call["process_state"] != state
        or call["returncode"] != code
        or call["prompt_log_path"] is not None
    ):
        raise ValueError("TUI call result or prompt absence is inconsistent")
    argv = call["argv"]
    if (
        not isinstance(argv, list)
        or not all(isinstance(arg, str) for arg in argv)
        or argv[-2:] != ["resume", record["fixed_session_id"]]
        or "--cd" not in argv
        or argv[argv.index("--cd") + 1] != record["cwd"]
    ):
        raise ValueError("TUI argv differs from the saved session ID or cwd")


def _validated_resume_record(
    execution_id: str, root: Path
) -> tuple[AgentCallParameter, dict[str, Any]]:
    """終了済み初回成功の記録を照合し、prompt を送らず公開再開を準備する。"""
    # 指定 ID に対応する記録だけを読み、旧実行のログを連鎖して探索しない。
    source = logs_dir(root) / f"{execution_id}.jsonl"
    try:
        if not is_common_id(execution_id, "exec"):
            raise ValueError("invalid execution ID")
        rows = [
            json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
        ]
        if not rows or any(not isinstance(row, dict) for row in rows):
            raise ValueError("invalid subcommand log")
        finished = [row for row in rows if row.get("event") == "command_finished"]
        startups = [row for row in rows if row.get("event") == "tui_startup"]
        if len(finished) != 1 or not startups or rows[-1] != finished[0]:
            raise ValueError("outer invocation exit or startup record is unconfirmed")
        if (
            type(finished[0].get("returncode")) is not int
            or finished[0].get("classification") not in {"natural_completion", "error"}
            or (finished[0]["classification"] == "natural_completion")
            != (finished[0]["returncode"] == 0)
        ):
            raise ValueError("outer invocation result is inconsistent")
        record = startups[-1]
        if (
            record.get("tui_record_version") != 3
            or record.get("execution_id") != execution_id
        ):
            raise ValueError("unsupported or inconsistent startup record")
        kind = record.get("tui_kind")
        builder = _BUILDERS[kind]
        command = record.get("subcommand")
        if command not in {"tui", "oracle investigation", "resume"} or (
            command != "resume"
            and kind
            != {"tui": "tui", "oracle investigation": "oracle_investigation"}[command]
        ):
            raise ValueError("subcommand and workload are inconsistent")
        if (
            record.get("phase") not in {"tui_finished", "tui_failed"}
            or record.get("initial_status") != "succeeded"
            or record.get("initial_process_state") != "exited"
            or type(record.get("initial_returncode")) is not int
            or record.get("initial_returncode") != 0
        ):
            raise ValueError("initial success and process exit are unconfirmed")
        _validate_initial_process_records(rows, record)
        _validate_tui_process_records(rows, record, root)
        if finished[0].get("command") != command or any(
            row.get("execution_id") != execution_id for row in rows
        ):
            raise ValueError("invocation identifiers or subcommand are inconsistent")
        initial_exec = record["initial_execution_id"]
        initial_call = record["initial_codex_call_id"]
        if (
            not is_common_id(initial_exec, "exec")
            or not is_common_id(initial_call, "cc")
            or not is_common_id(record["initial_agent_call_id"], "ac")
        ):
            raise ValueError("initial call identifiers are invalid")
        if str(UUID(record["initial_session_id"])) != record["initial_session_id"]:
            raise ValueError("initial session ID is invalid")
        directory = codex_log_dir(root) / initial_exec
        for field, suffix in [
            ("call_log", "call.json"),
            ("prompt_log", "prompt.md"),
            ("stdout_log", "stdout.jsonl"),
            ("stderr_log", "stderr.log"),
            ("output", "output.json"),
        ]:
            path = directory / f"{initial_call}_{suffix}"
            if record[f"initial_{field}_path"] != str(path.resolve()) or (
                record["resumed_from_execution_id"] is None and not path.is_file()
            ):
                raise ValueError(f"initial {field} is missing or inconsistent")
        if record["resumed_from_execution_id"] is None:
            if initial_exec != execution_id:
                raise ValueError("initial exec belongs to a different invocation")
            initial = json.loads(
                Path(record["initial_call_log_path"]).read_text(encoding="utf-8")
            )
            for field, initial_field in [
                ("execution_id", "initial_execution_id"),
                ("agent_call_id", "initial_agent_call_id"),
                ("codex_call_id", "initial_codex_call_id"),
                ("agent_call_kind", "agent_call_kind"),
                ("file_access_mode", "file_access_mode"),
                ("cwd", "cwd"),
                ("codex_home", "codex_home"),
                ("prompt_log_path", "initial_prompt_log_path"),
                ("stdout_log_path", "initial_stdout_log_path"),
                ("stderr_log_path", "initial_stderr_log_path"),
                ("output_path", "initial_output_path"),
            ]:
                if initial[field] != record[initial_field]:
                    raise ValueError(f"initial {field} is inconsistent")
            stdout = Path(record["initial_stdout_log_path"]).read_text(encoding="utf-8")
            if (
                classify_codex_call(stdout, 0) != "succeeded"
                or _session_id(stdout) != record["initial_session_id"]
            ):
                raise ValueError("initial terminal information or UUID is inconsistent")
        paths = AgentCallPathContext(Path(record["cwd"]))
        if (
            not paths.agent_call_cwd.is_dir()
            or str(paths.agent_call_cwd.resolve()) != record["cwd"]
            or str(paths.work_root) != record["work_root"]
            or str(paths.repo_root) != record["repo_root"]
            or paths.repo_root != root.resolve()
        ):
            raise ValueError("saved cwd, worktree or repository does not match")
        if (
            str(resolve_codex_home(paths.agent_call_cwd).resolve())
            != record["codex_home"]
        ):
            raise ValueError("current CODEX_HOME does not match saved location")
        parameter = builder(
            resume=TuiResumeTarget(record["initial_session_id"], paths.agent_call_cwd)
        )
        if (
            parameter.agent_call_kind != record["agent_call_kind"]
            or parameter.file_access_mode.value != record["file_access_mode"]
        ):
            raise ValueError("workload constraints do not match")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        raise CmocError(
            "指定された実行は TUI の再開条件を満たしません。",
            ["対象の実行 ID と診断ログを確認してください。"],
            f"execution_id: {execution_id}\nsource_log: {source}\nfailed condition: {exc}",
        ) from exc
    return parameter, record


def resume_codex_tui(execution_id: str, root: Path) -> CommandResult:
    """終了済み実行の固定 ID を確保・検査し、新しい invocation で再開する。"""
    # 先に lock key だけを解決し、適格性の検査から起動・終了まで確保を保持する。
    source = logs_dir(root) / f"{execution_id}.jsonl"
    try:
        if not is_common_id(execution_id, "exec"):
            raise ValueError("invalid execution ID")
        rows = [
            json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
        ]
        startups = [
            row
            for row in rows
            if isinstance(row, dict) and row.get("event") == "tui_startup"
        ]
        candidate = startups[-1]
        session_id = candidate["fixed_session_id"]
        if str(UUID(session_id)) != session_id:
            raise ValueError("fixed session ID is invalid")
        codex_home = Path(candidate["codex_home"])
        if not codex_home.is_absolute():
            raise ValueError("saved CODEX_HOME is not absolute")
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        IndexError,
    ) as exc:
        raise CmocError(
            "指定された実行は TUI の再開条件を満たしません。",
            ["対象の実行 ID と診断ログを確認してください。"],
            f"execution_id: {execution_id}\nsource_log: {source}\nfailed condition: {exc}",
        ) from exc
    with closing(CodexSessionLease(codex_home)) as lease:
        lease.acquire(session_id)
        parameter, record = _validated_resume_record(execution_id, root)
        if (
            record["fixed_session_id"] != session_id
            or Path(record["codex_home"]) != codex_home
        ):
            raise CmocError(
                "再開対象の記録が検査中に変わりました。",
                ["対象の実行ログを確認してください。"],
                str(source),
            )
        current = _context(parameter)
        current.update(
            {key: value for key, value in record.items() if key.startswith("initial_")}
        )
        current["resumed_from_execution_id"] = execution_id
        paths = AgentCallPathContext(parameter.agent_call_cwd)
        if paths.work_root != work_root():
            run_doctor_preprocess(paths.work_root)
        return _resume(
            parameter,
            root,
            deepcopy(load_config(paths.work_root)),
            "resume",
            current,
            lease,
        )
