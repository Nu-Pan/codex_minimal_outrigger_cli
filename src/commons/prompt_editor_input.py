"""AI Agent 用 prompt をエディタから受け取る共通境界。"""

import re
import shutil
import subprocess
from pathlib import Path

from oracle.prompt_builder.editor_input import build_prompt_editor_input_initial_text

from .runtime_errors import CmocError
from .runtime_git import ensure_cmoc_ignored
from .runtime_paths import (
    _reserve_timestamped_path,
    editor_input_dir,
    timestamp,
    work_root,
)


def collect_prompt_editor_input(
    root: Path,
    automatically_injected_instruction: str,
) -> tuple[Path, str]:
    """初期 prompt を保存・編集し、コメント除去済み入力と path を返す。"""
    # 同じ timestamp の呼び出しでも入力を上書きしないよう先に path を予約する。
    editor_dir = editor_input_dir(root)
    editor_dir.mkdir(parents=True, exist_ok=True)
    _, path = _reserve_timestamped_path(editor_dir, "_orig.md", timestamp)
    # {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
    path.write_text(
        build_prompt_editor_input_initial_text(automatically_injected_instruction),
        encoding="utf-8",
    )

    # エディタが戻った時点を入力完了とし、終了失敗は利用者向けエラーにする。
    argv = [*_select_editor(), str(path)]
    result = subprocess.run(argv)
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから cmoc コマンドを再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )
    return path, _read_prompt_editor_input(path)


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
