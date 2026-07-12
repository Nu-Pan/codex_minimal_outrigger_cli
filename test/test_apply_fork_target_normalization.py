"""apply fork の対象 file 正規化だけを検証する回帰テスト。

対象分類の正本: <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md
"""

from pathlib import Path

from _git_support import add_tracked_ignored_oracle_file, make_repo, run_git
import sub_commands.apply.fork as apply_fork_module


def test_apply_fork_target_normalization_keeps_nested_memo_directory(
    tmp_path: Path,
) -> None:
    """root 直下 memo を除外し、入れ子の memo directory は対象に残す。"""
    root = make_repo(tmp_path)
    (root / "memo").mkdir()
    (root / "memo" / "root.txt").write_text("private\n")
    (root / "docs" / "memo").mkdir(parents=True)
    nested = root / "docs" / "memo" / "public.txt"
    nested.write_text("target\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {root / "memo" / "root.txt", nested},
    )

    assert targets == [nested.resolve()]


def test_apply_fork_target_normalization_excludes_non_realization_paths(
    tmp_path: Path,
) -> None:
    """realization file 定義から外れる管理 path と規範 path を除外する。"""
    root = make_repo(tmp_path)
    src_target = root / "src" / "target.py"
    codex_target = root / ".codex" / "config.toml"
    nested_codex_target = root / "src" / ".codex" / "template.txt"
    nested_agents_target = root / "docs" / ".agents" / "rule.md"
    agents_target = root / "AGENTS.md"
    index_target = root / "INDEX.md"
    src_target.parent.mkdir()
    codex_target.parent.mkdir()
    nested_codex_target.parent.mkdir(parents=True)
    nested_agents_target.parent.mkdir(parents=True)
    src_target.write_text("target\n")
    codex_target.write_text("config\n")
    nested_codex_target.write_text("template\n")
    nested_agents_target.write_text("rule\n")
    agents_target.write_text("agents\n")
    index_target.write_text("index\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {
            src_target,
            codex_target,
            nested_codex_target,
            nested_agents_target,
            agents_target,
            index_target,
        },
    )

    assert targets == [
        nested_agents_target.resolve(),
        nested_codex_target.resolve(),
        src_target.resolve(),
    ]


def test_apply_fork_target_normalization_excludes_cmoc_runtime_files(
    tmp_path: Path,
) -> None:
    """作業用状態領域の .cmoc/local 配下 file は対象にしない。"""
    root = make_repo(tmp_path)
    config_target = root / ".cmoc" / "config.json"
    ignored_local_target = root / ".cmoc" / "local" / "cache.json"
    config_target.parent.mkdir()
    ignored_local_target.parent.mkdir(parents=True)
    config_target.write_text("{}\n")
    ignored_local_target.write_text("{}\n")
    (root / ".gitignore").write_text("/.cmoc/local/\n")
    run_git(root, "add", ".gitignore", ".cmoc/config.json")
    run_git(root, "commit", "-m", "add cmoc config")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {config_target, ignored_local_target},
    )

    assert targets == [config_target.resolve()]


def test_apply_fork_target_normalization_keeps_binary_files(
    tmp_path: Path,
) -> None:
    """full scope の候補になり得る binary file を file 種別だけで除外しない。"""
    root = make_repo(tmp_path)
    realization_binary = root / "asset.bin"
    oracle_binary = root / "oracle" / "asset.bin"
    realization_binary.write_bytes(b"\x00realization\n")
    oracle_binary.write_bytes(b"\x00oracle\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {realization_binary, oracle_binary},
    )

    assert targets == [realization_binary.resolve(), oracle_binary.resolve()]


def test_apply_fork_target_normalization_keeps_tracked_ignored_files(
    tmp_path: Path,
) -> None:
    """通常の git check-ignore と同じく tracked ignored file を対象に残す。"""
    root = make_repo(tmp_path)
    add_tracked_ignored_oracle_file(root)
    realization_target = root / "src" / "ignored.py"
    realization_target.parent.mkdir()
    realization_target.write_text("value = 1\n")
    with (root / ".gitignore").open("a") as file:
        file.write("src/ignored.py\nsrc/untracked.py\n")
    run_git(root, "add", "-f", ".gitignore", "src/ignored.py")
    run_git(root, "commit", "-m", "add ignored realization")
    untracked_ignored = root / "src" / "untracked.py"
    untracked_ignored.write_text("value = 2\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {
            root / "oracle" / "ignored.md",
            realization_target,
            untracked_ignored,
        },
    )

    assert targets == [
        (root / "oracle" / "ignored.md").resolve(),
        realization_target.resolve(),
    ]


def test_apply_fork_target_normalization_classifies_oracle_symlink_by_repo_path(
    tmp_path: Path,
) -> None:
    """oracle 配下 symlink は link 先ではなく repository path で分類する。"""
    root = make_repo(tmp_path)
    (root / "memo").mkdir()
    (root / "memo" / "draft.md").write_text("# draft\n")
    oracle_link = root / "oracle" / "memo-link.md"
    oracle_link.symlink_to("../memo/draft.md")
    run_git(root, "add", "memo/draft.md", "oracle/memo-link.md")
    run_git(root, "commit", "-m", "add oracle symlink")

    targets = apply_fork_module.normalize_apply_targets(root, {oracle_link})

    assert targets == [oracle_link.absolute()]
