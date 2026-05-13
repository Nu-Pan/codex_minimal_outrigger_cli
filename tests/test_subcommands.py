"""サブコマンド本体の決定論的な制御ロジックのテスト。"""

import subprocess
from pathlib import Path

from pytest import MonkeyPatch

from sub_commands.apply import cmoc_apply_impl
from sub_commands.branch import cmoc_branch_impl
from sub_commands.eval_oracles import cmoc_eval_oracles_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.merge import cmoc_merge_impl


def test_init_adds_cmoc_ignore_and_commits_it(tmp_path: Path) -> None:
    """`cmoc init` は `.cmoc` ignore ルールを commit する。"""
    repo = _init_repo(tmp_path)

    cmoc_init_impl(repo)

    assert ".cmoc" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "Initialize cmoc"


def test_branch_creates_cmoc_branch_and_records_base_commit(tmp_path: Path) -> None:
    """`cmoc branch` は branch 作成と base commit 記録を行う。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_branch_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    record_path = repo / ".cmoc" / "branch" / f"{branch_name}.txt"
    assert branch_name.startswith("cmoc_")
    assert record_path.read_text(encoding="utf-8").strip() == base_commit


def test_eval_oracles_writes_report_with_fake_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc eval-oracles --full` は oracle 評価レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr("sub_commands.eval_oracles.maintain_indexes", lambda repo_root: False)
    monkeypatch.setattr(
        "sub_commands.eval_oracles.run_codex_exec",
        lambda *args, **kwargs: "no fatal problems",
    )

    cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    assert len(reports) == 1
    assert "mode: full" in reports[0].read_text(encoding="utf-8")
    assert "no fatal problems" in reports[0].read_text(encoding="utf-8")


def test_apply_returns_complete_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` はズレなし JSON で完了扱いのレポートを保存する。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr("sub_commands.apply.maintain_indexes", lambda repo_root: False)

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査ならズレなし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"discrepancies": []}'
        return "complete report"

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    reports = list((repo / ".cmoc" / "reports" / "apply").glob("*.md"))
    assert exit_code == 0
    assert len(reports) == 1
    assert reports[0].read_text(encoding="utf-8") == "complete report"


def test_merge_merges_explicit_cmoc_branch_and_deletes_it(tmp_path: Path) -> None:
    """`cmoc merge <branch>` は clean tree で merge し、安全なら branch を消す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    target_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")
    _git(repo, "checkout", target_branch)

    cmoc_merge_impl(repo, "cmoc_2026-05-10_22-21_10_123")

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout.splitlines()
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert "cmoc_2026-05-10_22-21_10_123" not in branches


def _init_repo(tmp_path: Path) -> Path:
    """テスト用 git repo を作り、初期 commit を置く。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "initial")
    return repo


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """git をテスト repo で実行する。"""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
