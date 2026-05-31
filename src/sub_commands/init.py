"""`cmoc init` の本体処理。"""

from pathlib import Path

from commons.command_runner import run_command
from commons.repo import (
    commit_cmoc_initialization_changes,
    ensure_cmoc_ignored,
    gitignore_has_cmoc_rule,
    staged_diff_from_head,
)
from commons.timing import StepTimer, start_step


def cmoc_init_impl(repo_root: Path | None = None) -> None:
    """cmoc 作業用ディレクトリを git 追跡対象外にする。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_init_impl, command_path="cmoc init")
        return

    # `.cmoc` ignore ルールと tracked file 解除を保証する。
    timer = StepTimer("init")
    start_step(timer, 1, 2, ".cmoc ignore 確認")
    had_cmoc_rule = gitignore_has_cmoc_rule(repo_root)
    preexisting_staged_diff = staged_diff_from_head(repo_root)
    ensure_cmoc_ignored(repo_root)

    # 初期化によって発生した `.gitignore` や index 変更だけを commit する。
    start_step(timer, 2, 2, "初期化変更 commit")
    committed = commit_cmoc_initialization_changes(
        repo_root,
        had_cmoc_rule,
        preexisting_staged_diff,
    )
    if committed:
        print("committed initialization changes")
    else:
        print("no initialization changes")
    timer.report()
