"""`cmoc branch` の本体処理。"""

from pathlib import Path
from time import sleep

from commons.repo import branch_base_commit_path, ensure_cmoc_ignored, head_commit, run_git
from commons.timestamps import make_timestamp


def cmoc_branch_impl(repo_root: Path) -> None:
    """cmoc 作業用ブランチを作成し、作成元 commit を記録する。"""
    print("branch (1/3) create cmoc branch")
    base_commit = head_commit(repo_root)
    branch_name = _create_unique_branch(repo_root)

    print("branch (2/3) ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)

    print("branch (3/3) record branch base commit")
    base_path = branch_base_commit_path(repo_root, branch_name)
    base_path.parent.mkdir(parents=True, exist_ok=True)
    base_path.write_text(f"{base_commit}\n", encoding="utf-8")
    print(f"created branch: {branch_name}")


def _create_unique_branch(repo_root: Path) -> str:
    """衝突時に timestamp を作り直して branch 作成をリトライする。"""
    for _ in range(10):
        branch_name = f"cmoc_{make_timestamp()}"
        result = run_git(repo_root, ["checkout", "-b", branch_name], check=False)
        if result.returncode == 0:
            return branch_name
        sleep(0.001)
    raise RuntimeError("Failed to create unique cmoc branch after retries.")
