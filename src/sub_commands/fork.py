"""cmot fork サブコマンド。"""

from datetime import datetime

from commons.errors import CmotError, exit_with_error
from commons.git import (
    commit_cmot_ignore,
    default_branch,
    fetch_origin,
    prepare_repo,
    require_clean_worktree,
    require_not_cmot_branch,
)
from commons.process import run_command
from commons.progress import format_elapsed, progress, start_timer


def cmot_fork_impl() -> None:
    """remote default branch から cmot feature branch を作る。"""
    started_at = start_timer()
    progress("fork started")
    try:
        # repository root と cmot 用 ignore を準備する。
        progress("preparing repository")
        repo_root, cmot_ignore_added = prepare_repo()

        # fork は人間がクリーンにした状態からだけ開始する。
        progress("checking working tree")
        allowed_paths = [".gitignore"] if cmot_ignore_added else []
        require_clean_worktree(repo_root, allowed_paths=allowed_paths)
        require_not_cmot_branch(repo_root)

        # remote 最新 commit を分岐元にする。
        progress("fetching origin")
        fetch_origin(repo_root)
        base_branch = default_branch(repo_root)
        branch_name = f"cmot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        progress(f"creating branch {branch_name}")
        run_command(
            ["git", "checkout", "-b", branch_name, f"origin/{base_branch}"],
            repo_root,
            capture_output=False,
        )

        # 初回導入時の cmot ignore だけを feature branch 上で確定する。
        if cmot_ignore_added:
            progress("committing cmot ignore")
            commit_cmot_ignore(repo_root)
        progress(f"fork completed in {format_elapsed(started_at)}")
    except CmotError as error:
        progress(f"fork failed in {format_elapsed(started_at)}")
        exit_with_error(error)
