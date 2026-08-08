"""AI Agent 用 prompt をエディタから受け取る共通境界。"""

import re
import shutil
import subprocess
from pathlib import Path
from types import FunctionType

from oracle.prompt_builder import editor_input as _canonical_editor_input

from basic.struct_doc import render_as_markdown as _render_as_markdown

from .runtime_errors import CmocError
from .runtime_git import ensure_cmoc_ignored
from .runtime_paths import (
    _reserve_timestamped_path,
    editor_input_dir,
    timestamp,
    work_root,
)

ORIGINAL_PROMPT_PLACEHOLDER = "{{original-prompt-here}}"


def reserve_prompt_editor_input(root: Path) -> tuple[str, Path, Path]:
    """同じ timestamp を持つ入力 path と完全 prompt path を準備する。"""
    # 入力を上書きしないよう original prompt path だけを排他的に予約する。
    editor_dir = editor_input_dir(root)
    editor_dir.mkdir(parents=True, exist_ok=True)
    time_stamp, original_prompt_path = _reserve_timestamped_path(
        editor_dir,
        "_orig.md",
        timestamp,
    )
    complete_prompt_path = editor_dir / f"{time_stamp}_cmpl.md"
    return time_stamp, original_prompt_path, complete_prompt_path


def collect_prompt_editor_input(
    original_prompt_path: Path,
    complete_prompt_skeleton: str,
) -> str:
    """完全 prompt の skeleton を提示し、コメント除去済み入力を返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    _require_single_original_prompt_placeholder(complete_prompt_skeleton)

    # 正本が構築する案内と完全 prompt の skeleton を編集対象へ保存する。
    # {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
    original_prompt_path.write_text(
        _build_prompt_editor_input_initial_text(complete_prompt_skeleton),
        encoding="utf-8",
    )

    # エディタが戻った時点を入力完了とし、終了失敗は利用者向けエラーにする。
    argv = [*_select_editor(), str(original_prompt_path)]
    result = subprocess.run(argv)
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから cmoc コマンドを再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )
    return _read_prompt_editor_input(original_prompt_path)


def finalize_complete_prompt(
    complete_prompt_path: Path,
    complete_prompt_skeleton: str,
    original_prompt: str,
) -> None:
    """skeleton の唯一の入力位置を置換して完全 prompt を確定する。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    _require_single_original_prompt_placeholder(complete_prompt_skeleton)
    complete_prompt_path.write_text(
        complete_prompt_skeleton.replace(
            ORIGINAL_PROMPT_PLACEHOLDER,
            original_prompt,
            1,
        ),
        encoding="utf-8",
    )


def ensure_prompt_editor_roots_ignored(root: Path) -> None:
    """editor/TUI が使う repository と現在 worktree の `.cmoc` ignore を保証する。"""
    current_root = work_root()
    ensure_cmoc_ignored(current_root)
    if current_root.resolve() != root.resolve():
        ensure_cmoc_ignored(root)


def _select_editor() -> list[str]:
    """仕様の優先順で PATH 上の editor command を選ぶ。"""
    for command in ("code", "nano", "vim", "vi"):
        executable = shutil.which(command)
        if executable is None:
            continue
        return [executable, "--wait"] if command == "code" else [executable]
    raise CmocError(
        "利用可能なエディタが見つかりません。",
        ["code, nano, vim, vi のいずれかを PATH から起動できるようにしてください。"],
        "searched: code, nano, vim, vi",
    )


def _read_prompt_editor_input(path: Path) -> str:
    """HTML comment と前後の空白を除去して利用者入力を読む。"""
    return re.sub(
        r"<!--.*?-->",
        "",
        path.read_text(encoding="utf-8"),
        flags=re.DOTALL,
    ).strip()


def _require_single_original_prompt_placeholder(
    complete_prompt_skeleton: str,
) -> None:
    """完全 prompt の未確定位置が唯一であることを検証する。"""
    count = complete_prompt_skeleton.count(ORIGINAL_PROMPT_PLACEHOLDER)
    if count == 1:
        return
    raise CmocError(
        "完全プロンプトの skeleton が不正です。",
        ["cmoc の prompt builder と oracle file の整合性を確認してください。"],
        f"placeholder: {ORIGINAL_PROMPT_PLACEHOLDER}\ncount: {count}",
    )


def _build_prompt_editor_input_initial_text(
    complete_prompt_skeleton: str,
) -> str:
    """正本 builder を文字列 child 対応 renderer で実行する。"""
    # NOTE:
    #   現行の正本 renderer は StructBlock の str child を受理する一方で、その
    #   検証時に str.children を参照する。正本の案内文を複製せず局所的に補うため、
    #   builder の globals だけを差し替えた関数を生成する。この互換処理は
    #   oracle/src/oracle/other/struct_doc.py が str child を描画可能になれば削除する。
    canonical_builder = _canonical_editor_input.build_prompt_editor_input_initial_text
    builder_globals = {
        **canonical_builder.__globals__,
        "render_as_markdown": _render_as_markdown,
    }
    adapted_builder = FunctionType(
        canonical_builder.__code__,
        builder_globals,
        canonical_builder.__name__,
        canonical_builder.__defaults__,
        canonical_builder.__closure__,
    )
    result: object = adapted_builder(complete_prompt_skeleton)
    if not isinstance(result, str):
        raise TypeError(
            "build_prompt_editor_input_initial_text returned an unexpected type "
            f"(type={type(result)})"
        )
    return result
