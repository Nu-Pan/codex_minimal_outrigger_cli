"""`cmoc init` の本体処理。"""

from pathlib import Path

from commons.timing import StepTimer
from commons.repo import commit_if_changed, ensure_cmoc_ignored


def cmoc_init_impl(repo_root: Path) -> None:
    """cmoc 作業用ディレクトリを git 追跡対象外にする。"""
    timer = StepTimer("init")
    timer.start("ensure .cmoc is ignored")
    print("init (1/2) ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)

    timer.start("commit initialization changes")
    print("init (2/2) commit initialization changes")
    committed = commit_if_changed(
        repo_root,
        [".gitignore", ".cmoc"],
        "Initialize cmoc",
    )
    if committed:
        print("committed initialization changes")
    else:
        print("no initialization changes")
    timer.report()
