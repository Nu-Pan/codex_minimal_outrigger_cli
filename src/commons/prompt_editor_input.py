"""AI Agent 用 prompt をエディタから受け取る共通境界。"""

import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from oracle.prompt_builder.editor_input import (
    build_prompt_editor_input_console_guidance,
)

from .runtime_editor_input_handoff import (
    start_editor_input_handoff,
    validate_editor_input_file,
)
from .runtime_errors import CmocError
from .runtime_git import ensure_cmoc_ignored
from .runtime_paths import (
    _reserve_timestamped_path,
    editor_input_log_dir,
    timestamp,
    work_root,
)

ORIGINAL_PROMPT_PLACEHOLDER = "{{original-prompt-here}}"


def reserve_prompt_editor_input(root: Path) -> Path:
    """編集から確定保存まで共用する空の本文 file を予約する。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    # 保存済み入力も編集中の入力も、排他的な予約で上書きを避ける。
    directory = editor_input_log_dir(root)
    _validate_editor_storage_path(directory, require_directory=True)
    directory.mkdir(parents=True, exist_ok=True)
    _validate_editor_storage_path(directory, require_directory=True)
    _, input_path = _reserve_timestamped_path(directory, "_orig.md", timestamp)
    return input_path


def edit_prompt_editor_input(
    root: Path,
    input_path: Path,
    complete_prompt_skeleton: str,
) -> None:
    """空の入力 file と独立した handoff ガイドを準備し、エディタを起動する。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    validate_editor_input_file(root, input_path)

    # 人間向け案内や受信側の雛形を依頼本文へ混入させない。
    input_path.write_text("", encoding="utf-8")

    argv = [*_select_editor(), str(input_path)]
    target = start_editor_input_handoff(root, input_path, complete_prompt_skeleton)
    try:
        # 非対話サブコマンドの stdout は terminal result 用なので、editor の
        # 待機中に人間へ渡す target ID は stderr へ表示する。
        print(
            f"editor input handoff target ID: {target.target_id}",
            file=sys.stderr,
            flush=True,
        )
        print(
            build_prompt_editor_input_console_guidance(),
            end="",
            file=sys.stderr,
            flush=True,
        )
        # エディタが戻った後は target を drain・無効化してから処理を進める。
        result = subprocess.run(argv)
    finally:
        target.close()
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから cmoc コマンドを再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )


def collect_prompt_editor_input(
    root: Path,
    input_path: Path,
) -> str:
    """本文を一度だけ読み、同じ path へ確定保存して入力を返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    # 最終時点の通常 file を一度だけ読み、同じ結果を保存と入力抽出に使う。
    validate_editor_input_file(root, input_path)
    final_read_result = input_path.read_bytes()
    _save_editor_input(root, input_path, final_read_result)
    return final_read_result.decode("utf-8").strip()


def _save_editor_input(root: Path, input_path: Path, content: bytes) -> None:
    """書き込み完了までは元の入力を保持し、確定原文へ置換する。"""
    # 同じ filesystem 内で置換し、書き込み・flush・置換の失敗で本文を壊さない。
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=input_path.parent,
            prefix=f".{input_path.name}.",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        validate_editor_input_file(root, input_path)
        os.replace(temporary_path, input_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


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


def _validate_editor_storage_path(
    path: Path,
    *,
    require_directory: bool = False,
) -> None:
    """editor input の保存 path が symlink 経由でないことを検証する。"""
    absolute = path.absolute()
    current = absolute
    while True:
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            mode = None
        except OSError as exc:
            raise CmocError(
                "editor input の保存先を検証できません。",
                [
                    "editor input の保存先と親 directory を確認してから再実行してください。"
                ],
                f"path: {path}\nreason: {exc}",
            ) from exc
        if mode is not None:
            if stat.S_ISLNK(mode):
                raise CmocError(
                    "editor input の保存先は symlink 経由で扱えません。",
                    [
                        "editor input の保存先と親 directory を通常の file/directory に戻してから再実行してください。"
                    ],
                    f"path: {path}\nsymlink: {current}",
                )
            if current != absolute and not stat.S_ISDIR(mode):
                raise CmocError(
                    "editor input の保存先の親が directory ではありません。",
                    [
                        "editor input の保存先と親 directory を通常の file/directory に戻してから再実行してください。"
                    ],
                    f"path: {path}\nnon-directory: {current}",
                )
            if require_directory and current == absolute and not stat.S_ISDIR(mode):
                raise CmocError(
                    "editor input の保存先 directory が通常の directory ではありません。",
                    [
                        "editor input の保存先と親 directory を通常の directory に戻してから再実行してください。"
                    ],
                    f"path: {path}",
                )
        if current == current.parent:
            return
        current = current.parent
