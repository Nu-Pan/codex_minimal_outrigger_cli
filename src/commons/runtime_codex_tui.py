"""TUI の初回 exec と、保存済み会話への対話移行を管理する。"""

import json
import os
import sys
import threading
from copy import deepcopy
from pathlib import Path
from typing import Any
from uuid import UUID

from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)
from oracle.acp_builder.tui.launch_tui import build_tui_launch_tui_parameter

from basic.acp import AgentCallParameter, TuiResumeTarget
from basic.path_model import AgentCallPathContext
from config.cmoc_config import CmocConfig

from .runtime_codex_exec import run_codex_exec
from .runtime_codex_profile import (
    classify_codex_call,
    prepare_codex_override_args,
    resolve_codex_home,
    validate_codex_home,
)
from .runtime_codex_recovery import (
    check_recovery_interruption,
    current_recovery_cancellation,
    install_recovery_interruption,
)
from .runtime_config import load_config
from .runtime_doctor import run_doctor_preprocess
from .runtime_errors import CmocError, TuiStartupCancelled
from .runtime_ids import is_common_id, new_id
from .runtime_logging import current_execution_id, current_subcommand_logger
from .runtime_paths import codex_log_dir, logs_dir, timestamp, work_root
from .runtime_results import CodexExecResult, CommandResult

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
        "tui_record_version": 2,
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
) -> CommandResult:
    """再開の call 記録を保存し、未確認の会話 lifecycle では起動を拒否する。"""
    # prompt ファイルを作らず、今回の再開準備を別 call として保存する。
    assert parameter.prompt is None
    assert parameter.tui_resume_session_id is not None
    paths = AgentCallPathContext(parameter.agent_call_cwd)
    validate_codex_home(resolve_codex_home(paths.agent_call_cwd))
    overrides = prepare_codex_override_args(parameter, config, path_context=paths)
    if record["execution_id"] is None:
        record["execution_id"] = current_execution_id(root)
    agent_call_id = new_id(root, "ac")
    codex_call_id = new_id(root, "cc")
    directory = codex_log_dir(root) / record["execution_id"]
    directory.mkdir(parents=True, exist_ok=True)
    call_path = directory / f"{codex_call_id}_call.json"
    call_config = config.codex.agent_calls[parameter.agent_call_kind]
    # argv と prompt 不在の契約は 0.162.1 の resume wrapper で確認済み。
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/cli/src/main.rs#L354-L393
    context = {
        **record,
        "agent_call_id": agent_call_id,
        "codex_call_id": codex_call_id,
        "call_log_path": str(call_path.resolve()),
        "prompt_log_path": None,
        "requested_codex_session_id": parameter.tui_resume_session_id,
        "codex_session_id": None,
        "conversation_state": "not_opened",
    }
    call_path.write_text(
        json.dumps(
            {
                **context,
                "purpose": purpose,
                "timestamp": timestamp(),
                "argv": [
                    "codex",
                    *overrides,
                    "--cd",
                    str(paths.agent_call_cwd),
                    "resume",
                    parameter.tui_resume_session_id,
                ],
                "model_provider": call_config.model_provider,
                "model": call_config.model,
                "reasoning_effort": call_config.reasoning_effort,
                "process_state": "not_started",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event("tui_process_prepared", **context, process_state="prepared")
        logger.event(
            "tui_process_finished",
            **context,
            process_state="not_started",
            returncode=None,
        )
    # SessionStart は turn 開始時、session log の一般 event は variant のみ。
    # 要求 UUID や初回 UUID を実際に開いた主会話とみなして起動しない。
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/core/src/session/turn.rs#L306-L324
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/tui/src/session_log.rs#L218-L248
    raise CmocError(
        "Codex TUI の対話再開に必要な会話追跡と入力待ち確認を利用できません。",
        [
            "診断ログに保存された初回作業と会話を確認してください。",
            "会話 lifecycle に対応した Codex CLI 連携が必要です。",
        ],
        f"requested session: {parameter.tui_resume_session_id}\ncall_log: {call_path}\n"
        "failed condition: verified TUI conversation lifecycle and resume readiness are unavailable",
    )


def _resume(
    parameter: AgentCallParameter,
    root: Path,
    config: CmocConfig,
    purpose: str,
    record: dict[str, Any],
) -> CommandResult:
    """初回成功を保持し、TUI の準備失敗を別の終了状態として記録する。"""
    # この経路はまだ process を起動しないため、準備失敗は未起動と確定できる。
    _event("resume_prepared", record)
    try:
        return _run_codex_tui_process(
            parameter, root=root, config=config, purpose=purpose, record=record
        )
    except BaseException:
        _event(
            "tui_failed",
            record,
            tui_process_state="not_started",
            tui_conversation_state="not_opened",
        )
        raise


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
    record = _context(parameter)
    if parameter.prompt is None:
        return _resume(parameter, root, config, purpose, record)
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
        result = run_codex_exec(parameter, root=root, config=config, purpose=purpose)
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
        resume = _BUILDERS[record["tui_kind"]](
            resume=TuiResumeTarget(record["initial_session_id"], paths.agent_call_cwd)
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
    return _resume(resume, root, config, purpose, record)


def resume_codex_tui(execution_id: str, root: Path) -> CommandResult:
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
            finished[0].get("classification") != "error"
            or type(finished[0].get("returncode")) is not int
            or finished[0]["returncode"] == 0
        ):
            raise ValueError("TUI startup failure and outer exit are inconsistent")
        record = startups[-1]
        if (
            record.get("tui_record_version") != 2
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
            record.get("phase") != "tui_failed"
            or record.get("initial_status") != "succeeded"
            or record.get("initial_process_state") != "exited"
            or type(record.get("initial_returncode")) is not int
            or record.get("initial_returncode") != 0
            or record.get("tui_process_state") != "not_started"
            or record.get("tui_conversation_state") != "not_opened"
        ):
            raise ValueError("initial success and TUI not opened are unconfirmed")
        if any(row.get("event") == "tui_process_started" for row in rows):
            raise ValueError("TUI final primary conversation is unconfirmed")
        tui_exits = [row for row in rows if row.get("event") == "tui_process_finished"]
        if len(tui_exits) > 1 or any(
            row.get("process_state") != "not_started"
            or row.get("conversation_state") != "not_opened"
            or row.get("codex_session_id") is not None
            for row in tui_exits
        ):
            raise ValueError("TUI exit or conversation opening is unconfirmed")
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
        directory = codex_log_dir(root) / initial_exec
        for field, suffix in [
            ("call_log", "call.json"),
            ("prompt_log", "prompt.md"),
            ("stdout_log", "stdout.jsonl"),
            ("stderr_log", "stderr.log"),
            ("output", "output.json"),
        ]:
            path = directory / f"{initial_call}_{suffix}"
            if (
                record[f"initial_{field}_path"] != str(path.resolve())
                or not path.is_file()
            ):
                raise ValueError(f"initial {field} is missing or inconsistent")
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
    current = _context(parameter)
    current.update(
        {key: value for key, value in record.items() if key.startswith("initial_")}
    )
    current["resumed_from_execution_id"] = execution_id
    if paths.work_root != work_root():
        run_doctor_preprocess(paths.work_root)
    return _resume(
        parameter, root, deepcopy(load_config(paths.work_root)), "resume", current
    )
