"""Git ignore file の安全な更新と判定を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
- {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
"""

import os
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest
from _git_support import make_repo, run_git

import commons.runtime_git as runtime_git
from cmoc_runtime import (
    CmocError,
    ensure_cmoc_ignored,
    ensure_cmoc_ignored_in_exclude,
    is_git_ignored,
    is_untracked_git_ignored,
)
from commons.runtime_results import CommandResult


def test_ensure_cmoc_ignored_updates_gitignore(tmp_path: Path) -> None:
    """cmoc/local が未 ignore の repo では literal ignore pattern を追加する。"""
    root = make_repo(tmp_path)

    ensure_cmoc_ignored(root)

    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0


def test_ignore_checks_classify_literal_path_names(tmp_path: Path) -> None:
    """check-ignore が path 名をそのまま判定し、literal pathspec magic に依存しない。"""
    root = make_repo(tmp_path)
    path = root / "probe[1].txt"
    magic_prefix_path = root / ":(literal)probe.txt"
    path.write_text("probe\n")
    magic_prefix_path.write_text("probe\n")
    (root / ".gitignore").write_text("probe[[]1].txt\n:(literal)probe.txt\n")

    assert is_git_ignored(root, path)
    assert is_untracked_git_ignored(root, path)
    assert is_git_ignored(root, magic_prefix_path)
    assert is_untracked_git_ignored(root, magic_prefix_path)


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
    tmp_path: Path, path_kind: str
) -> None:
    """.gitignore が特殊 file でも read_text で停止せずエラーにする。"""
    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    if path_kind == "directory":
        gitignore.mkdir()
    else:
        os.mkfifo(gitignore)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored(root)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ensure_cmoc_ignored_rejects_non_file_info_exclude(tmp_path: Path) -> None:
    """.gitignore 更新時の共通 ignore 判定も特殊 file で停止しない。"""
    root = make_repo(tmp_path)
    exclude_path = root / Path(
        run_git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    )
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    os.mkfifo(exclude_path)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored(root)


def test_ignore_checks_reject_non_file_global_exclude(tmp_path: Path) -> None:
    """global excludes が特殊 file でも git check-ignore を停止させない。"""
    root = make_repo(tmp_path)
    global_exclude = root / "global-ignore"
    os.mkfifo(global_exclude)
    run_git(root, "config", "core.excludesFile", "global-ignore")

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="global excludes"):
            checker(root, root / "probe")
    with pytest.raises(CmocError, match="global excludes"):
        ensure_cmoc_ignored(root)


@pytest.mark.parametrize(
    "checker",
    [is_git_ignored, is_untracked_git_ignored],
    ids=["index-aware", "untracked-aware"],
)
def test_ignore_checks_reject_check_ignore_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    checker: Callable[[Path, Path], bool],
) -> None:
    """check-ignore が判定不能なら未 ignore として分類しない。"""
    root = make_repo(tmp_path)
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

    with pytest.raises(CmocError, match="Git ignore 判定"):
        checker(root, path)


def test_ignore_checks_reject_non_file_nested_gitignore(tmp_path: Path) -> None:
    """path 親 directory の特殊 .gitignore でも git check-ignore を停止させない。"""
    root = make_repo(tmp_path)
    source = root / "src"
    source.mkdir()
    os.mkfifo(source / ".gitignore")

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="通常の file"):
            checker(root, source / "probe")


def test_ignore_checks_do_not_inspect_ignored_symlink_target(
    tmp_path: Path,
) -> None:
    """ignored symlink の参照先を ignore source として検査しない。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("*.link\n")
    target = tmp_path / "outside"
    target.mkdir()
    (target / ".gitignore").mkdir()
    link = root / "candidate.link"
    link.symlink_to(target, target_is_directory=True)

    for checker in (is_git_ignored, is_untracked_git_ignored):
        assert checker(root, link)


def test_ensure_cmoc_ignored_rejects_symlinked_gitignore(tmp_path: Path) -> None:
    """.gitignore の symlink 先を cmoc が書き換えないことを検証する。"""
    root = make_repo(tmp_path)
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
    tmp_path: Path, path_kind: str
) -> None:
    """Git info/exclude が特殊 file でも read_text で停止せずエラーにする。"""
    root = make_repo(tmp_path)
    exclude_path = root / Path(
        run_git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    )
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    if path_kind == "directory":
        exclude_path.mkdir()
    else:
        os.mkfifo(exclude_path)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored_in_exclude(root)


def test_ensure_cmoc_ignored_in_exclude_rejects_symlinked_exclude(
    tmp_path: Path,
) -> None:
    """Git info/exclude の symlink 先を cmoc が書き換えないことを検証する。"""
    root = make_repo(tmp_path)
    external = tmp_path / "external.exclude"
    external.write_text("existing\n")
    exclude_path = root / Path(
        run_git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    )
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    exclude_path.unlink(missing_ok=True)
    exclude_path.symlink_to(external)

    with pytest.raises(CmocError, match="symlink"):
        ensure_cmoc_ignored_in_exclude(root)

    assert external.read_text() == "existing\n"


def test_ensure_cmoc_ignored_adds_literal_pattern_after_existing_effective_pattern(
    tmp_path: Path,
) -> None:
    """既存 pattern が有効でも root 固定 pattern を追記して表現を安定させる。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore cmoc")

    ensure_cmoc_ignored(root)

    assert (root / ".gitignore").read_text() == (
        ".cmoc/\n\n"
        "!/.cmoc/\n"
        "/.cmoc/*\n"
        "!/.cmoc/gt/\n"
        "/.cmoc/gt/*\n"
        "!/.cmoc/gt/ar/\n"
        "/.cmoc/gt/ar/*\n"
        "!/.cmoc/gt/ar/config.json\n"
        "!/.cmoc/gt/ar/realization/\n"
        "/.cmoc/gt/ar/realization/*\n"
        "!/.cmoc/gt/ar/realization/refactor/\n"
        "/.cmoc/gt/ar/realization/refactor/*\n"
        "!/.cmoc/gt/ar/realization/refactor/state.json\n"
        "/.cmoc/gu/\n"
    )
    assert run_git(root, "status", "--short").stdout.strip() == "M .gitignore"
