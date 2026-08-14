"""AI Agent 用 prompt をエディタから受け取る共通境界。"""

import re
import shutil
import stat
import subprocess
import time
from pathlib import Path

from oracle.prompt_builder.editor_input import build_prompt_editor_input_initial_text

from .runtime_errors import CmocError
from .runtime_git import ensure_cmoc_ignored
from .runtime_paths import (
    _reserve_timestamped_path,
    editor_input_log_dir,
    editor_work_dir,
    timestamp,
    work_root,
)

ORIGINAL_PROMPT_PLACEHOLDER = "{{original-prompt-here}}"


def reserve_prompt_editor_input(root: Path) -> tuple[str, Path, Path, Path]:
    """同じ timestamp を持つ作業 path と保存 path を準備する。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    # 可変な作業 file と cmoc だけが書く保存記録を別 directory に置く。
    work_dir = editor_work_dir(root)
    log_dir = editor_input_log_dir(root)
    work_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    # 削除済み work file と同じ timestamp の保存記録も上書きしない。
    while True:
        time_stamp, editor_work_path = _reserve_timestamped_path(
            work_dir,
            "_orig.md",
            timestamp,
        )
        input_copy_path = log_dir / f"{time_stamp}_orig.md"
        complete_prompt_path = log_dir / f"{time_stamp}_cmpl.md"
        output_paths = (input_copy_path, complete_prompt_path)
        if not any(path.exists() or path.is_symlink() for path in output_paths):
            return (
                time_stamp,
                editor_work_path,
                input_copy_path,
                complete_prompt_path,
            )
        editor_work_path.unlink()
        time.sleep(0.000001)


def collect_prompt_editor_input(
    root: Path,
    editor_work_path: Path,
    input_copy_path: Path,
    complete_prompt_skeleton: str,
) -> str:
    """作業 file を一度だけ最終読み取りし、入力を保存して返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    _require_single_original_prompt_placeholder(complete_prompt_skeleton)
    _validate_editor_work_file(root, editor_work_path)

    # 正本が構築する案内と完全 prompt の skeleton を作業 file へ保存する。
    # {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
    editor_work_path.write_text(
        build_prompt_editor_input_initial_text(complete_prompt_skeleton),
        encoding="utf-8",
    )

    # エディタが戻った時点を入力完了とし、終了失敗は利用者向けエラーにする。
    argv = [*_select_editor(), str(editor_work_path)]
    result = subprocess.run(argv)
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから cmoc コマンドを再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )

    # 最終時点の通常 file を一度だけ読み、同じ結果を保存と入力抽出に使う。
    _validate_editor_work_file(root, editor_work_path)
    final_read_result = editor_work_path.read_bytes()
    with input_copy_path.open("xb") as file:
        file.write(final_read_result)
    return _extract_original_prompt(final_read_result.decode("utf-8"))


def finalize_complete_prompt(
    editor_work_path: Path,
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
    # 完全 prompt の保存まで成功した作業 file だけを削除する。
    editor_work_path.unlink()


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


def _extract_original_prompt(final_read_result: str) -> str:
    """同じ最終読み取り結果から HTML comment と前後空白を除去する。"""
    return re.sub(
        r"<!--.*?-->",
        "",
        final_read_result,
        flags=re.DOTALL,
    ).strip()


def _validate_editor_work_file(root: Path, path: Path) -> None:
    """最終読み取り対象を所定 directory 内の通常 file に限定する。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    expected_dir = editor_work_dir(root)
    try:
        resolved_dir = expected_dir.resolve(strict=True)
        mode = path.lstat().st_mode
    except (OSError, RuntimeError) as exc:
        raise _invalid_editor_work_file(path, "path is not readable") from exc
    if not stat.S_ISREG(mode):
        raise _invalid_editor_work_file(path, "path is not a regular file")
    try:
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_dir)
    except (OSError, RuntimeError, ValueError) as exc:
        raise _invalid_editor_work_file(
            path,
            f"path is outside editor work directory: {expected_dir}",
        ) from exc


def _invalid_editor_work_file(path: Path, reason: str) -> CmocError:
    """不正な editor work file 用の利用者向けエラーを構築する。"""
    return CmocError(
        "editor work file を読み取れません。",
        ["復旧用に残った editor work file を確認してから再実行してください。"],
        f"path: {path}\nreason: {reason}",
    )


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
