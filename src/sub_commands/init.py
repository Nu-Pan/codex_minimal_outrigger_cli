"""`cmoc init` の本体処理。"""

from pathlib import Path

from commons.command_runner import run_command
from commons.repo import (
    commit_cmoc_initialization_changes,
    ensure_cmoc_ignored,
    gitignore_has_cmoc_rule,
)
from commons.timing import StepTimer


def cmoc_init_impl(repo_root: Path | None = None) -> None:
    """cmoc 作業用ディレクトリを git 追跡対象外にする。"""
    if repo_root is None:
        run_command(cmoc_init_impl)
        return

    # `.cmoc` ignore ルールと tracked file 解除を保証する。
    timer = StepTimer("init")
    timer.start("ensure .cmoc is ignored")
    print("init (1/2) ensure .cmoc is ignored")
    had_cmoc_rule = gitignore_has_cmoc_rule(repo_root)
    ensure_cmoc_ignored(repo_root)

    # 初期化によって発生した `.gitignore` や index 変更だけを commit する。
    timer.start("commit initialization changes")
    print("init (2/2) commit initialization changes")
    committed = commit_cmoc_initialization_changes(
        repo_root,
        had_cmoc_rule,
    )
    if committed:
        print("committed initialization changes")
    else:
        print("no initialization changes")
    timer.report()
