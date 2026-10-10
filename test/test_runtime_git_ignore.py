"""Git ignore file の安全な更新と判定を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
- {{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md
- {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
"""

import os
import subprocess
from pathlib import Path

import pytest
from _git_support import run_git

import commons.runtime_git as runtime_git
from cmoc_runtime import (
    CmocError,
    ensure_cmoc_ignored,
    ensure_cmoc_ignored_in_exclude,
    is_git_ignored,
    is_untracked_git_ignored,
)
from commons.runtime_results import CommandResult


@pytest.fixture
def _repository_exclude(cli_repository: Path) -> Path:
    """通常 repository の exclude 保存先を Git 問い合わせなしで用意する。"""
    # cli_repository は template を使わず、通常の .git directory を作る。
    path = cli_repository / ".git" / "info" / "exclude"
    path.parent.mkdir(exist_ok=True)
    return path


# ignore 判定には実 index を使い、HEAD との比較が必要なケースだけ commit する。
def test_ensure_cmoc_ignored_updates_gitignore(cli_repository: Path) -> None:
    """`.cmoc/gu` が未 ignore の repo では literal ignore pattern を追加する。"""
    root = cli_repository

    ensure_cmoc_ignored(root)

    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0


def test_ignore_checks_classify_literal_path_names(cli_repository: Path) -> None:
    """check-ignore が path 名をそのまま判定し、literal pathspec magic に依存しない。"""
    root = cli_repository
    path = root / "probe[1].txt"
    magic_prefix_path = root / ":(literal)probe.txt"
    path.write_text("probe\n")
    magic_prefix_path.write_text("probe\n")
    (root / ".gitignore").write_text("probe[[]1].txt\n:(literal)probe.txt\n")

    assert is_git_ignored(root, path)
    assert is_untracked_git_ignored(root, path)
    assert is_git_ignored(root, magic_prefix_path)
    assert is_untracked_git_ignored(root, magic_prefix_path)


def test_ignore_checks_respect_tracked_and_untracked_states(
    cli_repository: Path,
) -> None:
    """tracked file は保持し、untracked file は ignore 状態に従って判定する。"""
    root = cli_repository
    ignored = root / "ignored.txt"
    visible = root / "visible.txt"
    ignored.write_text("ignored\n")
    visible.write_text("visible\n")
    (root / ".gitignore").write_text("ignored.txt\n")
    run_git(root, "add", "-f", "ignored.txt")

    assert is_git_ignored(root, ignored)
    assert not is_untracked_git_ignored(root, ignored)
    assert not is_git_ignored(root, visible)
    assert not is_untracked_git_ignored(root, visible)


@pytest.mark.parametrize(
    "path_kind",
    [
        "directory",
        pytest.param(
            "fifo",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
    ],
)
def test_ensure_cmoc_ignored_rejects_non_file_gitignore(
    cli_repository: Path, path_kind: str
) -> None:
    """.gitignore が特殊 file でも read_text で停止せずエラーにする。"""
    root = cli_repository
    gitignore = root / ".gitignore"
    if path_kind == "directory":
        gitignore.mkdir()
    else:
        os.mkfifo(gitignore)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored(root)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ensure_cmoc_ignored_rejects_non_file_info_exclude(
    cli_repository: Path,
    _repository_exclude: Path,
) -> None:
    """.gitignore 更新時の共通 ignore 判定も特殊 file で停止しない。"""
    os.mkfifo(_repository_exclude)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored(cli_repository)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ignore_checks_reject_non_file_global_exclude(cli_repository: Path) -> None:
    """global excludes が特殊 file でも git check-ignore を停止させない。"""
    root = cli_repository
    global_exclude = root / "global-ignore"
    os.mkfifo(global_exclude)
    run_git(root, "config", "core.excludesFile", "global-ignore")

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="global excludes"):
            checker(root, root / "probe")
    with pytest.raises(CmocError, match="global excludes"):
        ensure_cmoc_ignored(root)


def test_ignore_checks_reject_check_ignore_failure(
    cli_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """check-ignore が判定不能なら未 ignore として分類しない。"""
    root = cli_repository
    path = root / "probe.txt"
    path.write_text("probe\n")
    original_run_git = runtime_git.run_git

    def failing_check_ignore(
        args: list[str], git_cwd: Path, check: bool = True
    ) -> CommandResult:
        """単一 path の check-ignore だけを失敗させる。"""
        if args[:1] == ["check-ignore"]:
            return CommandResult(
                returncode=128,
                stdout="",
                stderr="simulated check-ignore failure",
            )
        return original_run_git(args, git_cwd, check)

    monkeypatch.setattr(runtime_git, "run_git", failing_check_ignore)

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="Git ignore 判定"):
            checker(root, path)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ignore_checks_reject_non_file_nested_gitignore(cli_repository: Path) -> None:
    """path 親 directory の特殊 .gitignore でも git check-ignore を停止させない。"""
    root = cli_repository
    source = root / "src"
    source.mkdir()
    os.mkfifo(source / ".gitignore")

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="通常の file"):
            checker(root, source / "probe")


def test_ignore_checks_do_not_inspect_ignored_symlink_target(
    tmp_path: Path,
    cli_repository: Path,
) -> None:
    """ignored symlink の参照先を ignore source として検査しない。"""
    root = cli_repository
    (root / ".gitignore").write_text("*.link\n")
    target = tmp_path / "outside"
    target.mkdir()
    (target / ".gitignore").mkdir()
    link = root / "candidate.link"
    link.symlink_to(target, target_is_directory=True)

    for checker in (is_git_ignored, is_untracked_git_ignored):
        assert checker(root, link)


def test_ensure_cmoc_ignored_rejects_symlinked_gitignore(
    tmp_path: Path, cli_repository: Path
) -> None:
    """.gitignore の symlink 先を cmoc が書き換えないことを検証する。"""
    root = cli_repository
    external = tmp_path / "external.gitignore"
    external.write_text("existing\n")
    (root / ".gitignore").symlink_to(external)

    with pytest.raises(CmocError, match="symlink"):
        ensure_cmoc_ignored(root)

    assert external.read_text() == "existing\n"


@pytest.mark.parametrize(
    "path_kind",
    [
        "directory",
        pytest.param(
            "fifo",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
    ],
)
def test_ensure_cmoc_ignored_in_exclude_rejects_non_file(
    cli_repository: Path, _repository_exclude: Path, path_kind: str
) -> None:
    """Git info/exclude が特殊 file でも read_text で停止せずエラーにする。"""
    if path_kind == "directory":
        _repository_exclude.mkdir()
    else:
        os.mkfifo(_repository_exclude)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored_in_exclude(cli_repository)


def test_ensure_cmoc_ignored_in_exclude_rejects_symlinked_exclude(
    tmp_path: Path,
    cli_repository: Path,
    _repository_exclude: Path,
) -> None:
    """Git info/exclude の symlink 先を cmoc が書き換えないことを検証する。"""
    external = tmp_path / "external.exclude"
    external.write_text("existing\n")
    _repository_exclude.symlink_to(external)

    with pytest.raises(CmocError, match="symlink"):
        ensure_cmoc_ignored_in_exclude(cli_repository)

    assert external.read_text() == "existing\n"


def test_ensure_cmoc_ignored_preserves_existing_pattern_and_runtime_state(
    cli_repository: Path,
) -> None:
    """既存 pattern を保ち、cmoc 管理 state の ignore 例外を維持する。"""
    root = cli_repository
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore cmoc")

    ensure_cmoc_ignored(root)

    content = (root / ".gitignore").read_text()
    assert ".cmoc/\n" in content
    assert "/.cmoc/gu/\n" in content
    for relative in (
        ".cmoc/gt/config.json",
        ".cmoc/gt/realization/refactor/state.json",
    ):
        not_ignored = subprocess.run(
            ["git", "check-ignore", "--no-index", "-q", "--", relative],
            cwd=root,
            check=False,
        )
        assert not_ignored.returncode == 1
    assert run_git(root, "status", "--short").stdout.strip() == "M .gitignore"
