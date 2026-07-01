import re
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

from acp.builder.tui.resolve_parameter import (
    TUI_FILE_ACCESS_MODES,
    build_tui_resolve_parameter_parameter,
)
from acp.builder.tui.launch_tui import build_tui_launch_tui_parameter
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import (
    CmocError,
    CodexExecResult,
    ensure_cmoc_ignored,
    load_config,
    repo_root,
    run_cli_subcommand,
    run_codex_exec,
    run_codex_tui,
    timestamp,
    work_root,
)
from config.cmoc_config import CmocConfig
from commons.indexing import enable_indexing_preflight

ORIGINAL_PROMPT_TEMPLATE = """<!--
    AI Agent CLI/TUI に与えるプロンプトを書いて下さい。
    フォーマットは Markdown です。
    見出し (`#`, `##`, `###`, ...) やコードブロック (```...```) などの使用は自由です。
-->

TODO ここから書き始める
"""

CodexExec = Callable[..., CodexExecResult]
CodexTui = Callable[..., None]


def cmoc_tui_impl() -> None:
    """CLI runtime を通して tui を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_tui_from_current_context,
        pre_log_check=ensure_tui_cmoc_ignored,
        command_name="tui",
        command_argv=["cmoc", "tui"],
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
    original_path = initialize_original_prompt(root)
    run_editor(original_path)
    original_prompt = read_original_prompt(original_path)
    resolved = run_codex_exec(
        build_tui_resolve_parameter_parameter(original_prompt),
        root=root,
        cwd=work_root,
        config=config,
        purpose="tui resolve parameter",
    ).output_json
    launch_timestamp = original_path.name.removesuffix("_orig.md")
    parameter = build_tui_codex_parameter(
        original_prompt,
        resolved or {},
        launch_timestamp=launch_timestamp,
    )
    complete_prompt_path = root / ".cmoc" / "log" / "tui" / f"{launch_timestamp}_cmpl.md"
    run_codex_tui(
        parameter,
        root=root,
        cwd=work_root,
        config=config,
        purpose="tui codex",
        extra_read_paths=[complete_prompt_path],
    )


def ensure_tui_cmoc_ignored(root: Path) -> None:
    """TUI がログを書く root の `.cmoc` ignore をログ作成前に保証する。"""
    # <work-root>/oracle/doc/app_spec/sub_command/tui.md
    # <work-root>/oracle/doc/app_spec/misc_spec.md
    current_root = work_root()
    ensure_cmoc_ignored(current_root)
    if current_root.resolve() != root.resolve():
        ensure_cmoc_ignored(root)


def _cmoc_tui_from_current_context() -> None:
    """現在の repository 状態から `cmoc tui` の本体処理を起動する。"""
    root = repo_root()
    current_root = work_root()
    _cmoc_tui_body(
        run_codex_exec,
        run_codex_tui,
        root=root,
        work_root=current_root,
        config=load_config(root),
    )


def initialize_original_prompt(root: Path) -> Path:
    """利用者が編集する元 prompt ファイルを TUI log 領域へ作成する。"""
    path = root / ".cmoc" / "log" / "tui" / f"{timestamp()}_orig.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ORIGINAL_PROMPT_TEMPLATE)
    return path


def select_editor() -> list[str]:
    """cmoc tui で利用できる editor command を PATH から選ぶ。"""
    for command in ["code", "nano", "vim", "vi"]:
        executable = shutil.which(command)
        if executable is None:
            continue
        if command == "code":
            return [executable, "--wait"]
        return [executable]
    raise CmocError(
        "利用可能なエディタが見つかりません。",
        ["code, nano, vim, vi のいずれかを PATH から起動できるようにしてください。"],
        "searched: code, nano, vim, vi",
    )


def run_editor(path: Path) -> None:
    """利用者の prompt 編集が正常終了したことを確認する。"""
    argv = [*select_editor(), str(path)]
    result = subprocess.run(argv)
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから `cmoc tui` を再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )


def read_original_prompt(path: Path) -> str:
    """テンプレート用 HTML comment を除去した利用者 prompt を読む。"""
    return re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL).strip()


def build_tui_codex_parameter(
    original_prompt: str,
    resolved_parameter: dict,
    *,
    launch_timestamp: str | None = None,
) -> AgentCallParameter:
    """解決済み JSON から TUI 起動用 AgentCallParameter を構築する。"""
    file_access_mode = FileAccessMode(
        nested_value(resolved_parameter, "file_access_mode", FileAccessMode.READONLY.value)
    )
    if file_access_mode not in TUI_FILE_ACCESS_MODES:
        raise CmocError(
            "TUI では使用できないファイルアクセスモードです。",
            ["プロンプトを保存して `cmoc tui` を再実行してください。"],
            f"file_access_mode: {file_access_mode.value}",
        )
    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # <work-root>/oracle/doc/app_spec/sub_command/tui.md
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
        review_oracle_standard=nested_bool(
            resolved_parameter, "review_oracle_standard"
        ),
        apply_review_standard=nested_bool(resolved_parameter, "apply_review_standard"),
        index_entry_standard=nested_bool(resolved_parameter, "index_entry_standard"),
    )


def nested_value(data: dict, name: str, default: str) -> str:
    """TUI parameter JSON で `{value: ...}` 形式の項目から文字列値を取り出す。"""
    value = data.get(name)
    if (
        isinstance(value, dict)
        and isinstance(value.get("value"), str)
        and value["value"]
    ):
        return value["value"]
    return default


def nested_bool(data: dict, name: str) -> bool:
    """TUI parameter JSON で `{value: ...}` 形式の項目を真偽値として読む。"""
    value = data.get(name)
    return bool(value.get("value")) if isinstance(value, dict) else False
