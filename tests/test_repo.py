"""git リポジトリ共通処理のテスト。"""

import json
import subprocess
from pathlib import Path

import pytest

from commons.errors import CmocError
from commons.repo import (
    active_session_ids_for_home_branch,
    assert_cmoc_ignored,
    assert_no_uncommitted_changes,
    changed_paths,
    changed_oracle_files,
    changed_implementation_files,
    commit_if_changed,
    ensure_cmoc_ignored,
    find_repo_root,
    has_deleted_implementation_files,
    has_deleted_oracle_files,
    is_cmoc_branch,
    list_implementation_files,
    list_oracle_files,
    read_session_state,
    read_session_start_commit,
    session_state_path,
    session_state_root,
    write_session_state,
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


def test_assert_cmoc_ignored_does_not_modify_repository(
    tmp_path: Path,
) -> None:
    """副作用なし検証は `.gitignore` や index を補修しない。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(CmocError) as error:
        assert_cmoc_ignored(repo)

    assert "cmoc init" in "\n".join(error.value.actions)
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_assert_cmoc_ignored_rejects_global_exclude_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """外部 exclude だけで `.cmoc` が ignore されても保証済みにしない。"""
    repo = _init_repo(tmp_path)
    global_ignore = tmp_path / "global-ignore"
    global_ignore.write_text(".cmoc/\n", encoding="utf-8")
    global_config = tmp_path / "global-gitconfig"
    global_config.write_text(
        f"[core]\n\texcludesFile = {global_ignore}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))

    assert (
        _git(
            repo,
            "check-ignore",
            "-q",
            "--",
            ".cmoc/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    with pytest.raises(CmocError) as error:
        assert_cmoc_ignored(repo)

    assert "probe が ignore されませんでした" in error.value.detail
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_assert_cmoc_ignored_rejects_tracked_cmoc_without_untracking(
    tmp_path: Path,
) -> None:
    """tracked な `.cmoc` は検証失敗にし、index からは外さない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".gitignore", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")

    with pytest.raises(CmocError) as error:
        assert_cmoc_ignored(repo)

    assert ".cmoc/logs/tracked.log" in error.value.detail
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == (
        ".cmoc/logs/tracked.log\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


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


def test_list_implementation_files_excludes_specified_paths(
    tmp_path: Path,
) -> None:
    """実装ファイル列挙は oracles、memo、INDEX.md、gitignore 対象を除外する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (repo / "INDEX.md").write_text("index\n", encoding="utf-8")
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_implementation_files(repo)
    ]

    assert relative_paths == [".gitignore", "README.md", "app.py"]


def test_list_implementation_files_respects_gitignore_for_newline_paths(
    tmp_path: Path,
) -> None:
    """root .gitignore 判定でも newline を含む path 境界を保つ。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored*\n", encoding="utf-8")
    (repo / "kept\nname.py").write_text("kept\n", encoding="utf-8")
    (repo / "ignored\nname.py").write_text("ignored\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_implementation_files(repo)
    ]

    assert relative_paths == [
        ".gitignore",
        "README.md",
        "kept\nname.py",
    ]


def test_list_implementation_files_excludes_only_root_memo(
    tmp_path: Path,
) -> None:
    """実装ファイル列挙の memo 除外は repo root 直下だけに限定する。"""
    repo = _init_repo(tmp_path)
    nested_memo = repo / "docs" / "memo"
    nested_memo.mkdir(parents=True)
    (nested_memo / "note.md").write_text("note\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_implementation_files(repo)
    ]

    assert relative_paths == ["README.md", "docs/memo/note.md"]


def test_list_implementation_files_ignores_only_root_gitignore(
    tmp_path: Path,
) -> None:
    """実装ファイル列挙では nested .gitignore を除外判定に使わない。"""
    repo = _init_repo(tmp_path)
    cache_root = repo / ".pytest_cache"
    cache_root.mkdir()
    (cache_root / ".gitignore").write_text("*\n", encoding="utf-8")
    (cache_root / "CACHEDIR.TAG").write_text("cache\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_implementation_files(repo)
    ]

    assert relative_paths == [
        ".pytest_cache/.gitignore",
        ".pytest_cache/CACHEDIR.TAG",
        "README.md",
        "app.py",
    ]


def test_list_implementation_files_ignores_git_info_exclude(
    tmp_path: Path,
) -> None:
    """実装ファイル列挙では `.git/info/exclude` を除外判定に使わない。"""
    repo = _init_repo(tmp_path)
    exclude = repo / ".git" / "info" / "exclude"
    exclude.write_text("/logs/\n", encoding="utf-8")
    log_root = repo / "logs"
    log_root.mkdir()
    (log_root / "subcommand.log").write_text("log\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_implementation_files(repo)
    ]

    assert relative_paths == ["README.md", "app.py", "logs/subcommand.log"]


def test_list_implementation_files_ignores_system_excludes_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """実装ファイル列挙では system config の excludesFile を除外判定に使わない。"""
    external_ignore = tmp_path / "system-excludes"
    external_ignore.write_text("/system-only.txt\n", encoding="utf-8")
    system_config = tmp_path / "system-gitconfig"
    system_config.write_text(
        f"[core]\n\texcludesFile = {external_ignore.as_posix()}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", system_config.as_posix())

    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("# root only\n", encoding="utf-8")
    (repo / "system-only.txt").write_text("kept\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in list_implementation_files(repo)
    ]

    assert relative_paths == [".gitignore", "README.md", "system-only.txt"]


def test_changed_oracle_files_uses_session_start_and_uncommitted_changes(
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


def test_changed_oracle_files_preserves_special_path_tokens(
    tmp_path: Path,
) -> None:
    """変更 oracle path は newline や前後空白を含んでも実 path のまま扱う。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_path = oracle_root / "old\nname.md"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    renamed = oracle_root / " new\nname.md "
    _git(
        repo,
        "mv",
        old_path.relative_to(repo).as_posix(),
        renamed.relative_to(repo).as_posix(),
    )
    untracked = oracle_root / " untracked\nspec.md "
    untracked.write_text("new\n", encoding="utf-8")

    relative_paths = {
        path.relative_to(repo).as_posix()
        for path in changed_oracle_files(repo, base_commit)
    }

    assert relative_paths == {
        "oracles/ new\nname.md ",
        "oracles/ untracked\nspec.md ",
    }


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


def test_has_deleted_oracle_files_detects_committed_rename_out_of_oracles(
    tmp_path: Path,
) -> None:
    """committed oracle 外 rename は旧 oracle path の削除として検出する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    docs_root = repo / "docs"
    oracle_root.mkdir()
    docs_root.mkdir()
    old_path = oracle_root / "old.md"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "oracles/old.md", "docs/old.md")
    _git(repo, "commit", "-m", "move oracle out")

    assert has_deleted_oracle_files(repo, base_commit) is True


def test_has_deleted_oracle_files_detects_staged_rename_out_of_oracles(
    tmp_path: Path,
) -> None:
    """staged oracle 外 rename は旧 oracle path の削除として検出する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    docs_root = repo / "docs"
    oracle_root.mkdir()
    docs_root.mkdir()
    old_path = oracle_root / "old.md"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "oracles/old.md", "docs/old.md")

    assert has_deleted_oracle_files(repo, base_commit) is True


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


def test_changed_implementation_files_filters_to_implementation_targets(
    tmp_path: Path,
) -> None:
    """変更済み実装ファイルは oracles、memo、INDEX.md を除外して返す。"""
    repo = _init_repo(tmp_path)
    (repo / "base.py").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (repo / "base.py").write_text("changed\n", encoding="utf-8")
    (repo / "new.py").write_text("new\n", encoding="utf-8")
    (repo / "INDEX.md").write_text("index\n", encoding="utf-8")
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_implementation_files(repo, base_commit)
    ]

    assert relative_paths == ["base.py", "new.py"]


def test_changed_implementation_files_preserves_special_path_tokens(
    tmp_path: Path,
) -> None:
    """変更済み実装 path は newline や前後空白を含んでも実 path のまま扱う。"""
    repo = _init_repo(tmp_path)
    old_path = repo / "old\nname.py"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    renamed = repo / " new\nname.py "
    _git(
        repo,
        "mv",
        old_path.relative_to(repo).as_posix(),
        renamed.relative_to(repo).as_posix(),
    )
    untracked = repo / " untracked\nimpl.py "
    untracked.write_text("new\n", encoding="utf-8")

    relative_paths = {
        path.relative_to(repo).as_posix()
        for path in changed_implementation_files(repo, base_commit)
    }

    assert relative_paths == {
        " new\nname.py ",
        " untracked\nimpl.py ",
    }


def test_changed_implementation_files_ignores_only_root_gitignore(
    tmp_path: Path,
) -> None:
    """変更済み実装ファイルでは nested .gitignore を除外判定に使わない。"""
    repo = _init_repo(tmp_path)
    cache_root = repo / ".pytest_cache"
    cache_root.mkdir()
    (cache_root / ".gitignore").write_text("*\n", encoding="utf-8")
    ignored = cache_root / "CACHEDIR.TAG"
    ignored.write_text("base\n", encoding="utf-8")
    _git(
        repo,
        "add",
        "-f",
        ".pytest_cache/.gitignore",
        ".pytest_cache/CACHEDIR.TAG",
    )
    _git(repo, "commit", "-m", "track ignored cache")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    ignored.write_text("changed\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in changed_implementation_files(repo, base_commit)
    ]

    assert relative_paths == [".pytest_cache/CACHEDIR.TAG", "app.py"]


def test_commit_if_changed_keeps_index_when_staged_restore_fails(
    tmp_path: Path,
) -> None:
    """復元失敗時も、事前の staged blob を reset 済み index で壊さない。"""
    repo = _init_repo(tmp_path)
    target = repo / "target.txt"
    target.write_text("base\n", encoding="utf-8")
    _git(repo, "add", "target.txt")
    _git(repo, "commit", "-m", "target base")

    target.write_text("staged\n", encoding="utf-8")
    _git(repo, "add", "target.txt")
    target.write_text("internal\n", encoding="utf-8")

    with pytest.raises(CmocError):
        commit_if_changed(repo, ["target.txt"], "internal target")

    assert _git(repo, "show", ":target.txt").stdout == "staged\n"
    assert _git(repo, "diff", "--cached", "--name-only").stdout == (
        "target.txt\n"
    )
    assert _git(repo, "show", "HEAD:target.txt").stdout == "internal\n"


def test_has_deleted_implementation_files_detects_target_deletion(
    tmp_path: Path,
) -> None:
    """cmoc ブランチ上の実装ファイル削除を全体適用切替用に検出する。"""
    repo = _init_repo(tmp_path)
    deleted = repo / "deleted.py"
    deleted.write_text("delete me\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    deleted.unlink()

    assert has_deleted_implementation_files(repo, base_commit) is True


def test_has_deleted_implementation_files_preserves_special_path_tokens(
    tmp_path: Path,
) -> None:
    """削除済み実装 path の判定でも newline や前後空白を path として扱う。"""
    repo = _init_repo(tmp_path)
    deleted = repo / " delete\nme.py "
    deleted.write_text("delete me\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    deleted.unlink()

    assert has_deleted_implementation_files(repo, base_commit) is True


def test_has_deleted_implementation_files_ignores_only_root_gitignore(
    tmp_path: Path,
) -> None:
    """削除済み実装ファイルでは nested .gitignore を除外判定に使わない。"""
    repo = _init_repo(tmp_path)
    cache_root = repo / ".pytest_cache"
    cache_root.mkdir()
    (cache_root / ".gitignore").write_text("*\n", encoding="utf-8")
    ignored = cache_root / "CACHEDIR.TAG"
    ignored.write_text("base\n", encoding="utf-8")
    _git(
        repo,
        "add",
        "-f",
        ".pytest_cache/.gitignore",
        ".pytest_cache/CACHEDIR.TAG",
    )
    _git(repo, "commit", "-m", "track ignored cache")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    ignored.unlink()
    _git(repo, "add", "-u", ".pytest_cache")

    assert has_deleted_implementation_files(repo, base_commit) is True


def test_has_deleted_implementation_files_detects_committed_rename_out(
    tmp_path: Path,
) -> None:
    """committed 実装外 rename は旧実装 path の削除として検出する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_path = repo / "old.py"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "old.py", "oracles/old.py")
    _git(repo, "commit", "-m", "move implementation out")

    assert has_deleted_implementation_files(repo, base_commit) is True


def test_has_deleted_implementation_files_detects_staged_rename_out(
    tmp_path: Path,
) -> None:
    """staged 実装外 rename は旧実装 path の削除として検出する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_path = repo / "old.py"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "old.py", "oracles/old.py")

    assert has_deleted_implementation_files(repo, base_commit) is True


def test_has_deleted_implementation_files_ignores_implementation_rename(
    tmp_path: Path,
) -> None:
    """実装ファイル同士の rename は削除扱いしない。"""
    repo = _init_repo(tmp_path)
    old_path = repo / "old.py"
    old_path.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "old.py", "new.py")

    assert has_deleted_implementation_files(repo, base_commit) is False


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


def test_assert_no_uncommitted_changes_rejects_oracle_changes(
    tmp_path: Path,
) -> None:
    """`cmoc apply` の事前条件として oracle 差分も拒否する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        assert_no_uncommitted_changes(repo)

    assert "未コミットの変更があります。" in error.value.message
    assert "oracles/" in error.value.detail


def test_changed_paths_preserves_special_path_tokens(tmp_path: Path) -> None:
    """porcelain 由来の変更 path でも newline や前後空白を保持する。"""
    repo = _init_repo(tmp_path)
    tracked = repo / "old\nname.py"
    tracked.write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")

    renamed = repo / " new\nname.py "
    _git(
        repo,
        "mv",
        tracked.relative_to(repo).as_posix(),
        renamed.relative_to(repo).as_posix(),
    )
    untracked = repo / " untracked\nimpl.py "
    untracked.write_text("new\n", encoding="utf-8")

    assert set(changed_paths(repo)) == {
        " new\nname.py ",
        " untracked\nimpl.py ",
    }


@pytest.mark.parametrize(
    ("branch_name", "expected"),
    [
        ("cmoc/session/2026-05-10_22-21_10_000000123", True),
        (
            "cmoc/apply/"
            "2026-05-10_22-21_10_000000123/"
            "2026-05-10_22-22_10_000000123",
            True,
        ),
        ("cmoc/session/test", False),
        ("cmoc/apply/2026-05-10_22-21_10_000000123/run-1", False),
        ("cmoc/apply/a/b", False),
        ("cmoc/session/2026-05-10_22-21_10_000000123/extra", False),
        ("cmoc/apply/2026-05-10_22-21_10_000000123", False),
    ],
)
def test_is_cmoc_branch(branch_name: str, expected: bool) -> None:
    """cmoc ブランチ命名規則を判定する。"""
    assert is_cmoc_branch(branch_name) is expected


def test_read_session_start_commit_uses_session_state(
    tmp_path: Path,
) -> None:
    """部分評価用 base commit は session state から読む。"""
    repo = _init_repo(tmp_path)
    session_id = "2026-05-10_22-21_10_000000123"
    write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": "main",
                "session_start_commit": "abc123",
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )

    assert session_state_path(repo, session_id) == (
        repo / ".cmoc" / "sessions" / f"{session_id}.json"
    )
    assert read_session_start_commit(repo, f"cmoc/session/{session_id}") == (
        "abc123"
    )


def test_session_state_root_uses_main_worktree_for_linked_worktree(
    tmp_path: Path,
) -> None:
    """linked worktree からも session state の canonical root は共有 root になる。"""
    repo = _init_repo(tmp_path)
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")

    assert session_state_root(linked) == repo


def test_write_session_state_persists_only_oracle_schema(
    tmp_path: Path,
) -> None:
    """session state は oracle 定義の固定 field だけ永続化する。"""
    repo = _init_repo(tmp_path)
    session_id = "2026-05-10_22-21_10_000000123"

    state_path = write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": "main",
                "session_start_commit": "abc123",
                "runtime_note": "not durable",
            },
            "apply": {
                "state": "completed",
                "apply_branch": (
                    "cmoc/apply/2026-05-10_22-21_10_000000123/"
                    "2026-05-10_22-22_10_000000123"
                ),
                "oracle_snapshot_commit": "def456",
                "apply_worktree": "/repo/.cmoc/worktrees/apply/session/run",
                "completed": True,
                "discrepancy_counts": [0],
                "report_path": "/repo/.cmoc/reports/apply/fork/report.md",
            },
        },
    )

    assert json.loads(state_path.read_text(encoding="utf-8")) == {
        "session": {
            "state": "active",
            "session_home_branch": "main",
            "session_start_commit": "abc123",
        },
        "apply": {
            "state": "completed",
            "apply_branch": (
                "cmoc/apply/2026-05-10_22-21_10_000000123/"
                "2026-05-10_22-22_10_000000123"
            ),
            "oracle_snapshot_commit": "def456",
        },
    }


def test_read_session_state_rejects_unknown_state_values(
    tmp_path: Path,
) -> None:
    """session/apply state は oracle 定義の列挙値だけ受け入れる。"""
    repo = _init_repo(tmp_path)
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = session_state_path(repo, session_id)
    state_path.parent.mkdir(parents=True)
    state_path.write_text(
        json.dumps(
            {
                "session": {
                    "state": "paused",
                    "session_home_branch": "main",
                    "session_start_commit": "abc123",
                },
                "apply": {
                    "state": "ready",
                    "apply_branch": None,
                    "oracle_snapshot_commit": None,
                },
            },
        ),
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error:
        read_session_state(repo, session_id)

    assert "session.state は" in error.value.actions[0]
    assert "session.state: paused" in error.value.detail


def test_read_session_state_rejects_ready_apply_with_run_fields(
    tmp_path: Path,
) -> None:
    """apply.state が ready の永続 state は補助 field を null に保つ。"""
    repo = _init_repo(tmp_path)
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = session_state_path(repo, session_id)
    state_path.parent.mkdir(parents=True)
    state_path.write_text(
        json.dumps(
            {
                "session": {
                    "state": "active",
                    "session_home_branch": "main",
                    "session_start_commit": "abc123",
                },
                "apply": {
                    "state": "ready",
                    "apply_branch": (
                        "cmoc/apply/2026-05-10_22-21_10_000000123/"
                        "2026-05-10_22-22_10_000000123"
                    ),
                    "oracle_snapshot_commit": None,
                },
            },
        ),
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error:
        read_session_state(repo, session_id)

    assert "apply.state が ready" in error.value.actions[0]
    assert "apply.apply_branch:" in error.value.detail


def test_read_session_state_rejects_apply_schema_mismatch(
    tmp_path: Path,
) -> None:
    """永続 session state の apply field 集合は oracle schema と一致させる。"""
    repo = _init_repo(tmp_path)
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = session_state_path(repo, session_id)
    state_path.parent.mkdir(parents=True)
    state_path.write_text(
        json.dumps(
            {
                "session": {
                    "state": "active",
                    "session_home_branch": "main",
                    "session_start_commit": "abc123",
                },
                "apply": {
                    "state": "ready",
                    "oracle_snapshot_commit": None,
                    "process_id": 12345,
                },
            },
        ),
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error:
        read_session_state(repo, session_id)

    assert "apply セクションの field 集合" in error.value.actions[0]
    assert "missing apply fields: apply_branch" in error.value.detail
    assert "unknown apply fields: process_id" in error.value.detail


def test_write_session_state_rejects_completed_apply_without_run_fields(
    tmp_path: Path,
) -> None:
    """completed/running apply は cleanup/join 用の補助 field を必須にする。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(CmocError) as error:
        write_session_state(
            repo,
            "2026-05-10_22-21_10_000000123",
            {
                "session": {
                    "state": "active",
                    "session_home_branch": "main",
                    "session_start_commit": "abc123",
                },
                "apply": {
                    "state": "completed",
                    "apply_branch": None,
                    "oracle_snapshot_commit": "def456",
                },
            },
        )

    assert "apply.apply_branch" in error.value.detail


def test_write_session_state_allows_error_before_apply_run_fields_exist(
    tmp_path: Path,
) -> None:
    """apply branch 作成前の失敗は error state として保存できる。"""
    repo = _init_repo(tmp_path)
    session_id = "2026-05-10_22-21_10_000000123"

    state_path = write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": "main",
                "session_start_commit": "abc123",
            },
            "apply": {
                "state": "error",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )

    assert json.loads(state_path.read_text(encoding="utf-8"))["apply"] == {
        "state": "error",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }


def test_active_session_scan_fails_on_malformed_state_json(
    tmp_path: Path,
) -> None:
    """active session 判定では壊れた state JSON を無視しない。"""
    repo = _init_repo(tmp_path)
    state_root = repo / ".cmoc" / "sessions"
    state_root.mkdir(parents=True)
    malformed_path = state_root / "broken.json"
    malformed_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        active_session_ids_for_home_branch(repo, "main")

    assert "JSON が不正" in error.value.message
    assert str(malformed_path) in error.value.detail


def test_active_session_scan_fails_on_schema_invalid_state(
    tmp_path: Path,
) -> None:
    """active session 判定では session/apply セクション不正を無視しない。"""
    repo = _init_repo(tmp_path)
    state_root = repo / ".cmoc" / "sessions"
    state_root.mkdir(parents=True)
    invalid_path = state_root / "broken.json"
    invalid_path.write_text(
        json.dumps({"session": "broken", "apply": {"state": "ready"}}),
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error:
        active_session_ids_for_home_branch(repo, "main")

    assert "形式が不正" in error.value.message
    assert str(invalid_path) in error.value.detail


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
