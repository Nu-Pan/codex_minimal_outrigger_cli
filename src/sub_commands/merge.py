"""cmot merge サブコマンド。"""

from commons.errors import CmotError, exit_with_error
from commons.git import (
    current_branch,
    default_branch,
    fetch_origin,
    prepare_repo,
    require_cmot_branch,
)
from commons.process import run_command


def cmot_merge_impl() -> None:
    """cmot feature branch を default branch へ merge して削除する。"""
    try:
        repo_root, _ = prepare_repo()
        feature_branch = require_cmot_branch(repo_root)

        # default branch を最新化してから feature branch を merge する。
        base_branch = default_branch(repo_root)
        run_command(["git", "checkout", base_branch], repo_root, capture_output=False)
        fetch_origin(repo_root)
        run_command(
            ["git", "pull", "--ff-only", "origin", base_branch],
            repo_root,
            capture_output=False,
        )
        run_command(["git", "merge", "--no-ff", feature_branch], repo_root, capture_output=False)

        # merge 後の branch を確認し、マージ済み feature branch を削除する。
        if current_branch(repo_root) != base_branch:
            raise CmotError("merge did not leave repository on default branch")
        run_command(["git", "branch", "-d", feature_branch], repo_root, capture_output=False)
    except CmotError as error:
        exit_with_error(error)
