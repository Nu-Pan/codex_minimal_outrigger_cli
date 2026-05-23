"""`cmoc branch` の本体処理。"""

from pathlib import Path
from time import sleep

from commons.command_runner import run_command
from commons.repo import (
    branch_base_commit_path,
    ensure_cmoc_ignored,
    head_commit,
    run_git,
)
from commons.timing import StepTimer, start_step
from commons.timestamps import make_timestamp


def cmoc_branch_impl(repo_root: Path | None = None) -> None:
    """cmoc 作業用ブランチを作成し、作成元 commit を記録する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_branch_impl)
        return

    # branch 作成前の HEAD を、cmoc branch の base commit として記録する。
    timer = StepTimer("branch")
    start_step(timer, 1, 3, "create cmoc branch")
    base_commit = head_commit(repo_root)
    branch_name = _create_unique_branch(repo_root)

    # 作成した branch 上で `.cmoc` が git 追跡対象外であることを保証する。
    start_step(timer, 2, 3, "ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)

    # branch 名に対応する `.cmoc/branch` ファイルへ base commit を保存する。
    start_step(timer, 3, 3, "record branch base commit")
    base_path = branch_base_commit_path(repo_root, branch_name)
    base_path.parent.mkdir(parents=True, exist_ok=True)
    base_path.write_text(f"{base_commit}\n", encoding="utf-8")
    print(f"created branch: {branch_name}")
    timer.report()


def _create_unique_branch(repo_root: Path) -> str:
    """衝突時に timestamp を作り直して branch 作成をリトライする。"""
    # timestamp 衝突に備えて短い sleep を挟みながら最大 10 回リトライする。
    for attempt in range(1, 11):
        branch_name = f"cmoc_{make_timestamp()}"
        print(f"create cmoc branch attempt ({attempt}/10) {branch_name}")
        result = run_git(
            repo_root,
            ["checkout", "-b", branch_name],
            check=False,
        )
        if result.returncode == 0:
            return branch_name
        sleep(0.001)
    raise RuntimeError("リトライ後も一意な cmoc branch を作成できませんでした。")
