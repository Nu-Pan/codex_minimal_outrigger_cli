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


def cmot_fork_impl() -> None:
    """remote default branch から cmot feature branch を作る。"""
    try:
        repo_root, cmot_ignore_added = prepare_repo()

        # fork は人間がクリーンにした状態からだけ開始する。
        allowed_paths = [".gitignore"] if cmot_ignore_added else []
        require_clean_worktree(repo_root, allowed_paths=allowed_paths)
        require_not_cmot_branch(repo_root)

        # remote 最新 commit を分岐元にする。
        fetch_origin(repo_root)
        base_branch = default_branch(repo_root)
        branch_name = f"cmot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        run_command(
            ["git", "checkout", "-b", branch_name, f"origin/{base_branch}"],
            repo_root,
            capture_output=False,
        )

        # 初回導入時の cmot ignore だけを feature branch 上で確定する。
        if cmot_ignore_added:
            commit_cmot_ignore(repo_root)
    except CmotError as error:
        exit_with_error(error)
