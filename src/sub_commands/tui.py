from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from acp.builder.tui.launch_tui import build_tui_launch_tui_parameter
from acp.builder.tui.resolve_parameter import (
    TUI_FILE_ACCESS_MODES,
    build_tui_resolve_parameter_parameter,
)
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import (
    CmocError,
    load_config,
    repo_root,
    run_cli_subcommand,
    run_codex_exec,
    run_codex_tui,
    start_subcommand_step,
    timestamp,
    work_root,
)
from commons.indexing import enable_indexing_preflight
from commons.prompt_editor_input import (
    collect_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
)
from commons.runtime_results import CodexExecCallable, CommandResult
from config.cmoc_config import CmocConfig

CodexExec = CodexExecCallable
CodexTui = Callable[..., CommandResult]


def cmoc_tui_impl() -> None:
    """CLI runtime を通して tui を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_tui_from_current_context,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="tui",
        command_argv=["cmoc", "tui"],
        total_steps=4,
    )


def _cmoc_tui_body(
    run_codex_exec: CodexExec,
    run_codex_tui: CodexTui,
    *,
    root: Path,
    work_root: Path,
    config: CmocConfig,
) -> None:
    """依頼文の編集、実行パラメータ解決、Codex TUI 起動を一連で行う。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    start_subcommand_step(2, "オリジナルプロンプトを入力", "edit original prompt")
    original_path, original_prompt = collect_prompt_editor_input(root)

    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    start_subcommand_step(3, "実行パラメータを決定", "resolve parameters")
    resolved = run_codex_exec(
        replace(
            build_tui_resolve_parameter_parameter(original_prompt),
            cwd=work_root,
        ),
        root=root,
        cwd=work_root,
        config=config,
        purpose="tui resolve parameter",
    ).output_json
    parameter = build_tui_codex_parameter(
        original_prompt,
        resolved or {},
        launch_timestamp=original_path.name.removesuffix("_orig.md"),
    )

    # TUI は対象 worktree を cwd とし、完全 prompt は repository 側のログを読む。
    parameter = replace(parameter, cwd=work_root)
    start_subcommand_step(4, "AI Agent TUI を起動", "launch agent TUI")
    run_codex_tui(
        parameter,
        root=root,
        cwd=work_root,
        config=config,
        purpose="tui codex",
    )


def _cmoc_tui_from_current_context() -> None:
    """現在の repository 状態から `cmoc tui` の本体処理を起動する。"""
    root = repo_root()
    current_root = work_root()
    _cmoc_tui_body(
        run_codex_exec,
        run_codex_tui,
        root=root,
        work_root=current_root,
        config=load_config(current_root),
    )


def build_tui_codex_parameter(
    original_prompt: str,
    resolved_parameter: dict[str, object],
    *,
    launch_timestamp: str | None = None,
) -> AgentCallParameter:
    """解決済み JSON から TUI 起動用 AgentCallParameter を構築する。"""
    file_access_mode = FileAccessMode(
        nested_value(
            resolved_parameter, "file_access_mode", FileAccessMode.READONLY.value
        )
    )
    if file_access_mode not in TUI_FILE_ACCESS_MODES:
        raise CmocError(
            "TUI では使用できないファイルアクセスモードです。",
            ["プロンプトを保存して `cmoc tui` を再実行してください。"],
            f"file_access_mode: {file_access_mode.value}",
        )

    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    return build_tui_launch_tui_parameter(
        launch_timestamp or timestamp(),
        role=nested_value(
            resolved_parameter,
            "role",
            "- あなたは AI Agent CLI/TUI として、ユーザーから与えられた依頼を実行します",
        ),
        summary=nested_value(
            resolved_parameter,
            "summary",
            "- 後述する詳細指示に従って作業してください",
        ),
        goal=nested_value(
            resolved_parameter,
            "goal",
            "- 詳細指示の要求を満たしていること",
        ),
        file_access_mode=file_access_mode,
        original_prompt=original_prompt,
        oracle_and_realization_basic=nested_bool(
            resolved_parameter, "oracle_and_realization_basic"
        ),
        oracle_standard=nested_bool(resolved_parameter, "oracle_standard"),
        realization_standard=nested_bool(resolved_parameter, "realization_standard"),
        oracle_review_standard=nested_bool(
            resolved_parameter, "oracle_review_standard"
        ),
        apply_review_standard=nested_bool(resolved_parameter, "apply_review_standard"),
        index_entry_standard=nested_bool(resolved_parameter, "index_entry_standard"),
    )


def nested_value(data: dict[str, object], name: str, default: str) -> str:
    """TUI parameter JSON で `{value: ...}` 形式の項目から文字列値を取り出す。"""
    value = data.get(name)
    if isinstance(value, dict):
        nested = value.get("value")
        if isinstance(nested, str) and nested:
            return nested
    return default


def nested_bool(data: dict[str, object], name: str) -> bool:
    """TUI parameter JSON で `{value: ...}` 形式の項目を真偽値として読む。"""
    value = data.get(name)
    return bool(value.get("value")) if isinstance(value, dict) else False
