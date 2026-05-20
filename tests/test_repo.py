"""git リポジトリ共通処理のテスト。"""

import subprocess
from pathlib import Path

import pytest

from commons.errors import CmocError
from commons.repo import (
    assert_only_oracles_uncommitted,
    branch_base_commit_path,
    changed_oracle_files,
    ensure_cmoc_ignored,
    find_repo_root,
    has_deleted_oracle_files,
    is_cmoc_branch,
    list_oracle_files,
)


def test_find_repo_root_walks_up_from_nested_directory(tmp_path: Path) -> None:
    """`.git` を持つ親ディレクトリを repo root として見つける。"""
    repo = _init_repo(tmp_path)
    nested = repo / "a" / "b"
    nested.mkdir(parents=True)

    assert find_repo_root(nested) == repo


def test_ensure_cmoc_ignored_is_idempotent(tmp_path: Path) -> None:
    """`.cmoc` ignore ルールは重複追記しない。"""
    repo = _init_repo(tmp_path)

    assert ensure_cmoc_ignored(repo) is True
    assert ensure_cmoc_ignored(repo) is False
    assert (
        repo / ".gitignore"
    ).read_text(encoding="utf-8").count(".cmoc") == 1


def test_ensure_cmoc_ignored_untracks_existing_cmoc_files(
    tmp_path: Path,
) -> None:
    """既に tracked な `.cmoc` 配下ファイルは git index から外す。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")

    assert ensure_cmoc_ignored(repo) is True

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert cmoc_file.exists()
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")


def test_list_oracle_files_excludes_index_and_gitignored_files(
    tmp_path: Path,
) -> None:
    """oracle 列挙は INDEX.md と gitignore 対象を除外する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "INDEX.md").write_text("index", encoding="utf-8")
    (oracle_root / "kept.md").write_text("kept", encoding="utf-8")
    (oracle_root / "ignored.md").write_text("ignored", encoding="utf-8")

    assert [path.name for path in list_oracle_files(repo)] == ["kept.md"]


def test_list_oracle_files_excludes_tracked_gitignored_files(
    tmp_path: Path,
) -> None:
    """tracked でも .gitignore pattern に一致する oracle ファイルは除外する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "ignored.md").write_text("ignored", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "tracked oracle")
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")

    assert list_oracle_files(repo) == []


def test_list_oracle_files_respects_slash_pattern_depth(
    tmp_path: Path,
) -> None:
    """`oracles/*.md` は oracles 直下だけに一致し、ネスト先には一致しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/*.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    nested = oracle_root / "nested"
    nested.mkdir(parents=True)
    (oracle_root / "ignored.md").write_text("ignored", encoding="utf-8")
    (nested / "kept.md").write_text("kept", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_oracle_files(repo)
    ]

    assert relative_paths == ["oracles/nested/kept.md"]


def test_list_oracle_files_uses_git_double_star_semantics(
    tmp_path: Path,
) -> None:
    """root .gitignore の `**` は Git と同じ semantics で評価する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "oracles/**/ignored.md\n",
        encoding="utf-8",
    )
    oracle_root = repo / "oracles"
    nested = oracle_root / "a" / "b"
    nested.mkdir(parents=True)
    (oracle_root / "ignored.md").write_text("ignored", encoding="utf-8")
    (nested / "ignored.md").write_text("ignored", encoding="utf-8")
    (nested / "kept.md").write_text("kept", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_oracle_files(repo)
    ]

    assert relative_paths == ["oracles/a/b/kept.md"]


def test_list_oracle_files_ignores_only_root_gitignore(
    tmp_path: Path,
) -> None:
    """oracle 列挙では oracles 配下の .gitignore は除外判定に使わない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / ".gitignore").write_text("nested.md\n", encoding="utf-8")
    (oracle_root / "nested.md").write_text("nested", encoding="utf-8")

    assert [path.name for path in list_oracle_files(repo)] == [
        ".gitignore",
        "nested.md",
    ]


def test_list_oracle_files_keeps_nested_file_for_rooted_basename_pattern(
    tmp_path: Path,
) -> None:
    """root 起点 basename pattern は oracles 配下の同名ファイルに当てない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "ignored.md").write_text("oracle\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_oracle_files(repo)
    ]

    assert relative_paths == ["oracles/ignored.md"]


def test_changed_oracle_files_uses_cmoc_branch_base_and_uncommitted_changes(
    tmp_path: Path,
) -> None:
    """部分評価対象は base..HEAD と未コミット oracle 変更の和集合になる。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "base.md").write_text("base", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "committed.md").write_text("committed", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle change")
    (oracle_root / "working.md").write_text("working", encoding="utf-8")

    names = [path.name for path in changed_oracle_files(repo, base_commit)]

    assert names == ["committed.md", "working.md"]


def test_changed_oracle_files_includes_reverted_history_changes(
    tmp_path: Path,
) -> None:
    """HEAD で base と同じ内容に戻っても履歴上の変更は部分評価対象にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    reverted = oracle_root / "reverted.md"
    reverted.write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    reverted.write_text("changed\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "change oracle")
    reverted.write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "revert oracle")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_oracle_files(repo, base_commit)
    ]

    assert relative_paths == ["oracles/reverted.md"]


def test_changed_oracle_files_includes_untracked_files_under_new_directory(
    tmp_path: Path,
) -> None:
    """未追跡ディレクトリ配下の新規 oracle ファイルも部分評価対象にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "base.md").write_text("base", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    nested = oracle_root / "new_dir"
    nested.mkdir()
    (nested / "new.md").write_text("new", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_oracle_files(repo, base_commit)
    ]

    assert relative_paths == ["oracles/new_dir/new.md"]


def test_changed_oracle_files_uses_renamed_oracle_new_path(
    tmp_path: Path,
) -> None:
    """staged oracle rename は rename 後 path を部分評価対象にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_path = oracle_root / "old.md"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    new_path = oracle_root / "new.md"
    _git(
        repo,
        "mv",
        old_path.relative_to(repo).as_posix(),
        new_path.relative_to(repo).as_posix(),
    )

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_oracle_files(repo, base_commit)
    ]

    assert relative_paths == ["oracles/new.md"]
    assert has_deleted_oracle_files(repo, base_commit) is False


def test_committed_oracle_rename_does_not_count_as_deletion(
    tmp_path: Path,
) -> None:
    """committed oracle rename も削除扱いせず rename 後 path で評価する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_path = oracle_root / "old.md"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    new_path = oracle_root / "new.md"
    _git(
        repo,
        "mv",
        old_path.relative_to(repo).as_posix(),
        new_path.relative_to(repo).as_posix(),
    )
    _git(repo, "commit", "-m", "rename oracle")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_oracle_files(repo, base_commit)
    ]

    assert relative_paths == ["oracles/new.md"]
    assert has_deleted_oracle_files(repo, base_commit) is False


def test_changed_oracle_files_excludes_gitignored_files(
    tmp_path: Path,
) -> None:
    """部分評価対象でも gitignore 対象の oracle ファイルは除外する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "ignored.md").write_text("ignored", encoding="utf-8")

    assert changed_oracle_files(repo, base_commit) == []


def test_changed_oracle_files_respects_slash_pattern_depth(
    tmp_path: Path,
) -> None:
    """変更 oracle 抽出でも slash 付き pattern の階層 semantics を守る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/*.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    nested = oracle_root / "nested"
    nested.mkdir(parents=True)
    (nested / "base.md").write_text("base", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "ignored.md").write_text("ignored", encoding="utf-8")
    (nested / "kept.md").write_text("kept", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_oracle_files(repo, base_commit)
    ]

    assert relative_paths == ["oracles/nested/kept.md"]


def test_has_deleted_oracle_files_detects_base_to_head_deletion(
    tmp_path: Path,
) -> None:
    """cmoc ブランチ上の oracle 削除を全体評価切替用に検出する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "deleted.md").write_text("delete me\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "deleted.md").unlink()
    _git(repo, "add", "-u", "oracles")
    _git(repo, "commit", "-m", "delete oracle")

    assert has_deleted_oracle_files(repo, base_commit) is True


def test_has_deleted_oracle_files_detects_delete_then_readd_history(
    tmp_path: Path,
) -> None:
    """途中 commit の oracle 削除は HEAD に再追加されても全体評価へ切り替える。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    deleted = oracle_root / "deleted.md"
    deleted.write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    deleted.unlink()
    _git(repo, "add", "-u", "oracles")
    _git(repo, "commit", "-m", "delete oracle")
    deleted.write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "readd oracle")

    assert has_deleted_oracle_files(repo, base_commit) is True


def test_has_deleted_oracle_files_detects_uncommitted_worktree_deletion(
    tmp_path: Path,
) -> None:
    """working tree の oracle 削除も全体評価切替条件にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "deleted.md").write_text("delete me\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "deleted.md").unlink()

    assert has_deleted_oracle_files(repo, base_commit) is True


def test_has_deleted_oracle_files_detects_staged_deletion(
    tmp_path: Path,
) -> None:
    """staging area の oracle 削除も全体評価切替条件にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "deleted.md").write_text("delete me\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "deleted.md").unlink()
    _git(repo, "add", "-u", "oracles")

    assert has_deleted_oracle_files(repo, base_commit) is True


def test_has_deleted_oracle_files_ignores_index_md_deletion(
    tmp_path: Path,
) -> None:
    """INDEX.md だけの削除は oracle ファイル削除扱いにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle index")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "INDEX.md").unlink()
    _git(repo, "add", "-u", "oracles")

    assert has_deleted_oracle_files(repo, base_commit) is False


def test_has_deleted_oracle_files_ignores_gitignored_deletion(
    tmp_path: Path,
) -> None:
    """root .gitignore 対象の削除は oracle ファイル削除扱いにしない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "oracles/ignored.md\n",
        encoding="utf-8",
    )
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "ignored.md").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", "-f", ".gitignore", "oracles/ignored.md")
    _git(repo, "commit", "-m", "ignored oracle")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "ignored.md").unlink()
    _git(repo, "add", "-u", "oracles")

    assert has_deleted_oracle_files(repo, base_commit) is False


def test_assert_only_oracles_uncommitted_rejects_non_oracle_changes(
    tmp_path: Path,
) -> None:
    """`cmoc apply` の事前条件として oracles 外差分を拒否する。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("print('changed')\n", encoding="utf-8")

    with pytest.raises(CmocError):
        assert_only_oracles_uncommitted(repo)


@pytest.mark.parametrize(
    ("branch_name", "expected"),
    [
        ("cmoc_2026-05-10_22-21_10_123", True),
        ("feature/cmoc_2026-05-10_22-21_10_123", False),
        ("cmoc_2026-05-10_22-21-10", False),
    ],
)
def test_is_cmoc_branch(branch_name: str, expected: bool) -> None:
    """cmoc ブランチ命名規則を判定する。"""
    assert is_cmoc_branch(branch_name) is expected


def test_branch_base_commit_path_points_under_cmoc_branch_dir(
    tmp_path: Path,
) -> None:
    """branch base commit 記録先は `.cmoc/branch` 配下になる。"""
    repo = _init_repo(tmp_path)

    assert branch_base_commit_path(repo, "cmoc_2026-05-10_22-21_10_123") == (
        repo / ".cmoc" / "branch" / "cmoc_2026-05-10_22-21_10_123.txt"
    )


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
