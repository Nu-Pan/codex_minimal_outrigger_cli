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
def _ignore_source_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """ignore source の拒否検査に、Git が解決した保存先だけを渡す。"""
    # 実 Git の保存先解決は test_git_query_reuse.py と test_file_inventory.py に残す。
    # file の種別検証と公開 entrypoint は実経路を通し、repository は準備しない。
    root = tmp_path / "repo"
    root.mkdir()
    (root / "info").mkdir()
    monkeypatch.setattr(
        runtime_git, "_git_info_exclude_path", lambda _root: root / "info" / "exclude"
    )
    monkeypatch.setattr(
        runtime_git, "_global_git_ignore_paths", lambda _root: [root / "global-ignore"]
    )
    return root


# pattern と tracked/untracked の判定には実 Git と index を使う。
def test_ensure_cmoc_ignored_updates_gitignore(
    cli_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """未 ignore の repo を修復し、修復前の重複した Git 判定を起動しない。"""
    root = cli_repository
    commands = []
    original_run = runtime_git.subprocess.run

    def record_command(argv, *args, **kwargs):
        commands.append(argv)
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(runtime_git.subprocess, "run", record_command)

    ensure_cmoc_ignored(root)

    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    # source の配置取得、index 確認、最終 probe を一度ずつに収める。
    assert len(commands) <= 4, commands
    assert not any(command[:2] == ["git", "rm"] for command in commands)
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0


@pytest.mark.parametrize("failure", ["index", "ignore", "probe-error"])
def test_ensure_cmoc_ignored_rejects_incomplete_repair(
    _ignore_source_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """index 除外や最終 probe が失敗した修復を成功とせず、実ファイルを保つ。"""
    root = _ignore_source_directory
    relative = ".cmoc/gu/cache.txt"
    cache = root / relative
    cache.parent.mkdir(parents=True)
    cache.write_text("preserve\n")
    tracked = True
    probe_returncode = {"index": 0, "ignore": 1, "probe-error": 128}[failure]

    def incomplete_repair(args, git_cwd, check=True):
        nonlocal tracked
        assert git_cwd == root
        if args[0] == "ls-files":
            return CommandResult(0, relative if tracked else "", "")
        if args[0] == "rm":
            tracked = failure == "index"
            return CommandResult(0, "", "")
        if args[0] == "check-ignore":
            return CommandResult(probe_returncode, "", "")
        pytest.fail(f"unexpected Git command: {args}")

    monkeypatch.setattr(runtime_git, "run_git", incomplete_repair)

    with pytest.raises(CmocError, match="追跡対象外にできません") as caught:
        ensure_cmoc_ignored(root)

    assert cache.read_text() == "preserve\n"
    if failure == "index":
        assert relative in caught.value.detail
    else:
        assert f"check-ignore returncode: {probe_returncode}" in caught.value.detail


def test_ignore_checks_classify_literal_path_names(cli_repository: Path) -> None:
    """check-ignore が path 名をそのまま判定し、literal pathspec magic に依存しない。"""
    root = cli_repository
    path = root / "probe[1].txt"
    magic_prefix_path = root / ":(literal)probe.txt"
    path.write_text("probe\n")
    magic_prefix_path.write_text("probe\n")
    (root / ".gitignore").write_text("probe[[]1].txt\n:(literal)probe.txt\n")

    # 設定・保存先は固定なので問い合わせを共有し、path ごとの判定は実 Git を使う。
    with runtime_git.reuse_git_path_queries():
        assert is_git_ignored(root, path)
        assert is_untracked_git_ignored(root, path)
        assert is_git_ignored(root, magic_prefix_path)
        assert is_untracked_git_ignored(root, magic_prefix_path)


def test_ignore_checks_respect_tracked_and_untracked_states(
    cli_repository: Path,
) -> None:
    """ignore 設定と index の変更を反映し、tracked・unignored file を保持する。"""
    root = cli_repository
    ignored = root / "ignored.txt"
    visible = root / "visible.txt"
    ignored.write_text("ignored\n")
    visible.write_text("visible\n")
    gitignore = root / ".gitignore"
    gitignore.write_text("")

    # 配置の問い合わせを共有しても、ignore 内容と index の判定は更新する。
    with runtime_git.reuse_git_path_queries():
        assert not is_git_ignored(root, ignored)
        assert not is_untracked_git_ignored(root, ignored)

        gitignore.write_text("ignored.txt\n")
        assert is_git_ignored(root, ignored)
        assert is_untracked_git_ignored(root, ignored)

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
    tmp_path: Path, path_kind: str
) -> None:
    """.gitignore が特殊 file でも read_text で停止せずエラーにする。"""
    # Git 問い合わせ前の種類検証なので、repository と index は用意しない。
    root = tmp_path
    gitignore = root / ".gitignore"
    if path_kind == "directory":
        gitignore.mkdir()
    else:
        os.mkfifo(gitignore)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored(root)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ensure_cmoc_ignored_rejects_non_file_info_exclude(
    _ignore_source_directory: Path,
) -> None:
    """.gitignore 更新時の共通 ignore 判定も特殊 file で停止しない。"""
    root = _ignore_source_directory
    os.mkfifo(root / "info" / "exclude")

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored(root)

    assert not (root / ".gitignore").exists()


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ignore_checks_reject_non_file_global_exclude(
    _ignore_source_directory: Path,
) -> None:
    """global excludes が特殊 file でも git check-ignore を停止させない。"""
    root = _ignore_source_directory
    global_exclude = root / "global-ignore"
    os.mkfifo(global_exclude)

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="global excludes"):
            checker(root, root / "probe")
    with pytest.raises(CmocError, match="global excludes"):
        ensure_cmoc_ignored(root)

    assert not (root / ".gitignore").exists()


def test_ignore_checks_reject_check_ignore_failure(
    _ignore_source_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """check-ignore が判定不能なら未 ignore として分類しない。"""
    root = _ignore_source_directory
    path = root / "probe.txt"

    def failing_check_ignore(
        args: list[str], git_cwd: Path, check: bool = True
    ) -> CommandResult:
        """解決済み source の下で、単一 path の ignore 判定を失敗させる。"""
        assert args[0] == "check-ignore"
        assert git_cwd == root
        return CommandResult(
            returncode=128,
            stdout="",
            stderr="simulated check-ignore failure",
        )

    monkeypatch.setattr(runtime_git, "run_git", failing_check_ignore)

    for checker in (is_git_ignored, is_untracked_git_ignored):
        with pytest.raises(CmocError, match="Git ignore 判定"):
            checker(root, path)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_ignore_checks_reject_non_file_nested_gitignore(
    _ignore_source_directory: Path,
) -> None:
    """path 親 directory の特殊 .gitignore でも git check-ignore を停止させない。"""
    root = _ignore_source_directory
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

    with runtime_git.reuse_git_path_queries():
        for checker in (is_git_ignored, is_untracked_git_ignored):
            assert checker(root, link)


def test_ensure_cmoc_ignored_rejects_symlinked_gitignore(tmp_path: Path) -> None:
    """.gitignore の symlink 先を cmoc が書き換えないことを検証する。"""
    root = tmp_path / "repo"
    root.mkdir()
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
    _ignore_source_directory: Path, path_kind: str
) -> None:
    """Git info/exclude が特殊 file でも read_text で停止せずエラーにする。"""
    root = _ignore_source_directory
    exclude = root / "info" / "exclude"
    if path_kind == "directory":
        exclude.mkdir()
    else:
        os.mkfifo(exclude)

    with pytest.raises(CmocError, match="通常の file"):
        ensure_cmoc_ignored_in_exclude(root)


def test_ensure_cmoc_ignored_in_exclude_rejects_symlinked_exclude(
    tmp_path: Path,
    cli_repository: Path,
) -> None:
    """Git info/exclude の symlink 先を cmoc が書き換えないことを検証する。"""
    external = tmp_path / "external.exclude"
    external.write_text("existing\n")
    # 保存先の解決が symlink を dereference してしまう回帰も、実 Git で検出する。
    root = cli_repository
    exclude = root / ".git" / "info" / "exclude"
    exclude.parent.mkdir(exist_ok=True)
    exclude.symlink_to(external)

    with pytest.raises(CmocError, match="symlink"):
        ensure_cmoc_ignored_in_exclude(root)

    assert external.read_text() == "existing\n"


def test_ensure_cmoc_ignored_preserves_existing_pattern_and_runtime_state(
    cli_repository: Path,
) -> None:
    """既存 pattern を保ち、cmoc 管理 state の ignore 例外を維持する。"""
    root = cli_repository
    (root / ".gitignore").write_text(".cmoc/\n")
    # 修復前の index を残せば、履歴を作らず working tree の変更だけを検査できる。
    run_git(root, "add", ".gitignore")

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
    assert run_git(root, "status", "--short").stdout.strip() == "AM .gitignore"
