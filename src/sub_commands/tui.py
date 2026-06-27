import re
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

from acp.builder.tui.resolve_parameter import (
    TUI_FILE_ACCESS_MODES,
    build_tui_resolve_parameter_parameter,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.struct_doc import StructDoc, render_as_markdown
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
    parameter = build_tui_codex_parameter(original_prompt, resolved or {})
    complete_prompt_path = save_complete_prompt(work_root, original_path, parameter.prompt)
    run_codex_tui(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            parameter.file_access_mode,
            f"`{complete_prompt_path}` の指示に従って下さい。",
            parameter.structured_output_schema_path,
        ),
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


def save_complete_prompt(work_root: Path, original_path: Path, prompt: str) -> Path:
    """解決済みの完全 prompt を work root 側の TUI log 領域へ保存する。"""
    path = work_root / ".cmoc" / "log" / "tui" / original_path.name.replace(
        "_orig.md", "_cmpl.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt)
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
    prompt = build_complete_prompt(
        role="- あなたは AI Agent CLI/TUI として、ユーザーから与えられた依頼を実行します",
        summary="- 後述する詳細指示に従って作業してください",
        goal="- 詳細指示の要求を満たしていること",
        file_access_mode=file_access_mode,
        aux_prompt=[StructDoc("詳細指示", *parse_markdown_prompt(original_prompt))],
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
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        file_access_mode,
        render_as_markdown(prompt),
        None,
    )


def parse_markdown_prompt(markdown: str) -> list[StructDoc] | list[str]:
    """Markdown 見出しを StructDoc 階層へ変換し、見出しなし本文は文字列で保つ。"""
    sections: list[StructDoc] = []
    current_title: str | None = None
    current_body: list[str] = []
    fence: tuple[str, int] | None = None
    for line in markdown.splitlines():
        fence_pattern = (
            r"^[ \t]{0,3}(`{3,}|~{3,}).*$"
            if fence is None
            else r"^[ \t]{0,3}(`{3,}|~{3,})[ \t]*$"
        )
        fence_match = re.match(fence_pattern, line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            current_body.append(line)
            continue
        match = (
            None
            if fence is not None
            else re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        )
        if match:
            if current_title is not None:
                sections.append(StructDoc(current_title, "\n".join(current_body).strip()))
            else:
                preamble = "\n".join(current_body).strip()
                if preamble:
                    sections.append(StructDoc("本文", preamble))
            current_title = match.group(2)
            current_body = []
            continue
        current_body.append(line)
    if current_title is None:
        return [markdown]
    sections.append(StructDoc(current_title, "\n".join(current_body).strip()))
    return sections


def nested_value(data: dict, name: str, default: str) -> str:
    """TUI parameter JSON で `{value: ...}` 形式の項目から文字列値を取り出す。"""
    value = data.get(name)
    if isinstance(value, dict) and isinstance(value.get("value"), str):
        return value["value"]
    return default


def nested_bool(data: dict, name: str) -> bool:
    """TUI parameter JSON で `{value: ...}` 形式の項目を真偽値として読む。"""
    value = data.get(name)
    return bool(value.get("value")) if isinstance(value, dict) else False
