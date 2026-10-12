"""Codex TUI の起動と call log・実行結果の記録を担う。"""

import json
import os
import subprocess
import time
from pathlib import Path

from oracle.editor_input_handoff.body import EditorInputHandoffSource

from basic.acp import AgentCallParameter
from basic.path_model import AgentCallPathContext
from config.cmoc_config import CmocConfig

from .runtime_cli import mark_current_tui_process_started
from .runtime_codex_logging import format_codex_call_error, write_codex_prompt_log
from .runtime_codex_profile import (
    codex_cli_supports_tui_notification_hooks,
    codex_subprocess_env,
    document_search_mcp_override_args,
    prepare_codex_override_args,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from .runtime_config import load_config
from .runtime_editor_input_handoff_protocol import (
    editor_input_handoff_subprocess_env,
)
from .runtime_errors import CmocError
from .runtime_feedback import begin_feedback_call
from .runtime_ids import new_id
from .runtime_logging import current_execution_id, current_subcommand_logger
from .runtime_paths import (
    codex_log_dir,
    timestamp,
)
from .runtime_results import CommandResult
from .runtime_windows_toast import create_tui_notification_callback


def run_codex_tui(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex tui",
    notification_command_name: str | None = None,
) -> CommandResult:
    """Codex TUI を設定上書き argv と call log を準備して起動する。"""
    # SessionStart は turn の開始時に実行され、UI の全会話切替を追跡できない。
    # 外部契約を確認できるまで、要求 ID だけを開いた主会話として扱わない。
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/core/src/session/turn.rs#L306-L324
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/tui/src/session_log.rs#L218-L248
    if parameter.tui_resume_session_id is not None:
        raise CmocError(
            "Codex TUI の対話再開に必要な会話追跡を確認できません。",
            ["Codex TUI の会話追跡に対応した cmoc を使用してください。"],
            f"tui_resume_session_id: {parameter.tui_resume_session_id}\n"
            "failed condition: verified TUI conversation lifecycle is unavailable",
        )
    path_context = AgentCallPathContext(parameter.agent_call_cwd)
    root = root or path_context.repo_root
    config = config or load_config(path_context.work_root)
    log_dir = codex_log_dir(root) / current_execution_id(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    agent_call_cwd = path_context.agent_call_cwd
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # 利用者指定の env value は変更せず、Codex が相対 CODEX_HOME を解決する場所に
    # validation を合わせる。
    codex_home = resolve_codex_home(agent_call_cwd)
    validate_codex_home(codex_home)
    codex_environment = codex_subprocess_env(codex_home)
    # {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
    # TUI の version probe も Codex executable を起動するため、agent call と
    # selected provider の設定を検証してから probe を開始する。
    override_args = prepare_codex_override_args(parameter, config)
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    # callback state はこの TUI process invocation の期間だけ保持する。
    notification_callback = None
    if "_CMOC_COMPLETE" not in os.environ and codex_cli_supports_tui_notification_hooks(
        agent_call_cwd,
        codex_environment,
    ):
        notification_callback = create_tui_notification_callback(
            notification_command_name or purpose,
            root,
        )
    try:
        # 通知を使わない場合は検証済み argv を再利用し、MCP 設定と root を再構築しない。
        # callback が追加された場合だけ、その invocation の通知設定を反映する。
        if notification_callback is not None:
            override_args = prepare_codex_override_args(
                parameter,
                config,
                notification_command=notification_callback.command,
                session_start_command=notification_callback.session_start_command,
            )
        return _run_codex_tui_process(
            parameter,
            root=root,
            config=config,
            purpose=purpose,
            agent_call_cwd=agent_call_cwd,
            repository=path_context.repo_root,
            work_root=path_context.work_root,
            codex_home=codex_home,
            codex_environment=codex_environment,
            log_dir=log_dir,
            override_args=override_args,
        )
    finally:
        if notification_callback is not None:
            notification_callback.close()


def _run_codex_tui_process(
    parameter: AgentCallParameter,
    *,
    root: Path,
    config: CmocConfig,
    purpose: str,
    agent_call_cwd: Path,
    repository: Path,
    work_root: Path,
    codex_home: Path,
    codex_environment: dict[str, str],
    log_dir: Path,
    override_args: list[str],
) -> CommandResult:
    """root session filter を設定した 1 つの Codex TUI process を実行する。"""
    # 検証・確定済みの argv に、今回の call ID と検索ログ context を追加する。
    call_config = config.codex.agent_calls[parameter.agent_call_kind]
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    ts = timestamp()
    agent_call_id = new_id(root, "ac")
    codex_call_id = new_id(root, "cc")
    assert parameter.prompt is not None
    argv = [
        "codex",
        *override_args,
        *document_search_mcp_override_args(
            parameter, config, codex_call_id=codex_call_id
        ),
        "--cd",
        str(agent_call_cwd),
        parameter.prompt,
    ]
    call_path = log_dir / f"{codex_call_id}_call.json"
    call_path.open("x").close()
    prompt_path = log_dir / f"{codex_call_id}_prompt.md"
    prompt_path.open("x").close()
    write_codex_prompt_log(prompt_path, parameter.prompt)
    execution_id = log_dir.name
    logger = current_subcommand_logger()
    tui_kind = {
        "build_tui_launch_tui_parameter": "tui",
        "build_oracle_investigation_launch_tui_parameter": "oracle_investigation",
    }.get(parameter.agent_call_kind)
    # 会話 ID の取得経路が未検証であることを保持し、通知 marker を流用しない。
    # oracle/doc/app_spec/console_and_file_log.md の「TUI 再開のための実行記録」。
    tui_context = {
        "tui_record_version": 1,
        "execution_id": execution_id,
        "resumed_from_execution_id": None,
        "subcommand": logger.command if logger is not None else None,
        "sub_command_log_path": str(logger.path.resolve())
        if logger is not None
        else None,
        "tui_kind": tui_kind,
        "agent_call_id": agent_call_id,
        "agent_call_kind": parameter.agent_call_kind,
        "codex_call_id": codex_call_id,
        "file_access_mode": parameter.file_access_mode.value,
        "cwd": str(agent_call_cwd.resolve()),
        "work_root": str(work_root.resolve()),
        "repo_root": str(repository.resolve()),
        "codex_home": str(codex_home.resolve()),
        "call_log_path": str(call_path.resolve()),
        "prompt_log_path": str(prompt_path.resolve()),
        "requested_codex_session_id": None,
        "codex_session_id": None,
        "conversation_state": "unverified",
    }
    call_path.write_text(
        json.dumps(
            {
                "purpose": purpose,
                "timestamp": ts,
                "argv": argv,
                "model_provider": call_config.model_provider,
                "model": call_config.model,
                "reasoning_effort": call_config.reasoning_effort,
                **tui_context,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    started_at = time.perf_counter()
    failure: subprocess.CalledProcessError | None = None
    startup_failure: BaseException | None = None
    returncode: int | None = None
    process_started = False

    def _process_started() -> None:
        # Popen 成功直後だけ起動確認を記録し、例外やログの途切れで代用しない。
        nonlocal process_started
        process_started = True
        mark_current_tui_process_started()
        if logger is not None:
            logger.event("tui_process_started", **tui_context, process_state="started")

    if logger is not None:
        logger.event("tui_process_prepared", **tui_context, process_state="prepared")
    feedback_call = begin_feedback_call(
        agent_call_cwd=parameter.agent_call_cwd,
        agent_call_id=agent_call_id,
        agent_call_kind=parameter.agent_call_kind,
        codex_call_id=codex_call_id,
        log_paths=[call_path, prompt_path],
        enable_feedback_reporting=parameter.enable_feedback_reporting,
    )
    try:
        environment = dict(codex_environment)
        if parameter.enable_editor_input_handoff_mcp:
            # call log と同じ ID を起動前に記録・flush し、MCP にも同じ値を供給する。
            source = None
            if logger is not None:
                source = EditorInputHandoffSource(
                    subcommand=logger.command,
                    execution_id=logger.execution_id,
                    codex_call_id=codex_call_id,
                    sub_command_log_path=logger.path.resolve(),
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
                environment,
                repository,
                source,
            )
        environment = feedback_call.subprocess_env(environment)
        result = run_codex_subprocess(
            argv,
            cwd=agent_call_cwd,
            env=environment,
            check=True,
            process_started_callback=_process_started,
        )
        returncode = result.returncode
    except subprocess.CalledProcessError as exc:
        failure = exc
        returncode = exc.returncode
    except BaseException as exc:
        startup_failure = exc
    finally:
        feedback_call.close()
        if logger is not None:
            # returncode は wrapper が process を回収した場合だけ得られる。
            # 中断・任意の例外だけでは停止を断定せず、会話も未確定のまま残す。
            logger.event(
                "tui_process_finished",
                **tui_context,
                process_state=(
                    "exited"
                    if returncode is not None
                    else "unknown"
                    if process_started
                    else "not_started"
                ),
                returncode=returncode,
            )
    elapsed_sec = time.perf_counter() - started_at
    error: str | None = None
    if startup_failure is not None:
        error = format_codex_call_error(startup_failure)
    status = "succeeded" if returncode == 0 else "failed"

    def _emit_event(error: str | None = None) -> None:
        """Codex CLI の成功・失敗 event を logger に記録する。

        根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
        """
        if logger is None:
            return
        payload = {
            "purpose": purpose,
            "status": status if error is None else "failed",
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "call_log_path": str(call_path),
            "codex_home": str(codex_home),
            "agent_call_id": agent_call_id,
            "agent_call_kind": parameter.agent_call_kind,
            "codex_call_id": codex_call_id,
        }
        if error is not None:
            payload["error"] = error
        logger.event(
            "codex_call",
            **payload,
        )

    if startup_failure is not None:
        _emit_event(error)
        raise startup_failure
    _emit_event()
    if failure is not None:
        raise CmocError(
            "Codex CLI/TUI 呼び出しが失敗しました。",
            ["Codex CLI/TUI の出力と call log を確認してください。"],
            f"returncode: {returncode}\ncall_log: {call_path}",
        ) from failure
    assert returncode is not None
    return CommandResult(returncode, "", "")
