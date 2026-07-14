"""Codex の read/write 許可領域と追加 writable path を検証する。

根拠:
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
- <work-root>/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
- <work-root>/oracle/doc/app_spec/doctor_preprocess.md
"""

from fnmatch import fnmatch
from pathlib import Path

import pytest

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig

from _codex_support import (
    _assert_not_writable,
    _assert_writable,
    _override_permission_filesystem,
    _override_permission_roots,
)
from _git_support import make_repo, run_git


@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_readonly_modes_allow_only_ignored_gap_writes(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """読み取り専用モードが無視対象の未追跡パスだけを書き込み可能にすることを検証する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("__pycache__/\n/build/\n")
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('ok')\n")
    (root / "src" / "__pycache__").mkdir()
    (root / "src" / "__pycache__" / "main.pyc").write_text("cache\n")
    (root / "oracle" / "spec.md").write_text("# spec\n")
    (root / "oracle" / "__pycache__").mkdir()
    (root / "oracle" / "__pycache__" / "spec.pyc").write_text("cache\n")
    (root / "build").mkdir()
    (root / "build" / "artifact.txt").write_text("tracked\n")
    (root / "build" / "scratch.txt").write_text("scratch\n")
    run_git(root, "add", ".gitignore", "src/main.py", "oracle/spec.md")
    run_git(root, "add", "-f", "build/artifact.txt")
    run_git(root, "commit", "-m", "add tracked files")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )
    _assert_not_writable(override_args, root / "src" / "new.py")
    _assert_not_writable(override_args, root / "oracle" / "new.md")
    _assert_not_writable(override_args, root / "new.md")

    _assert_writable(override_args, root / "src" / "__pycache__" / "new.pyc")
    _assert_writable(override_args, root / "oracle" / "__pycache__" / "new.pyc")
    _assert_writable(override_args, root / "build" / "scratch.txt")
    _assert_not_writable(override_args, root / "src" / "main.py")
    _assert_not_writable(override_args, root / "oracle" / "spec.md")
    _assert_not_writable(override_args, root / "build" / "artifact.txt")
    _assert_not_writable(override_args, root / "memo" / "private.md")
    _assert_not_writable(
        override_args, root / ".cmoc" / "local" / "state.json"
    )


@pytest.mark.parametrize(
    "mode",
    [
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
        FileAccessMode.NO_RULE,
    ],
)
def test_codex_overrides_protect_memo_and_future_routing_files(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """memo と将来のルーティングファイルを全書き込みモードで保護することを検証する。"""
    root = make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "test").mkdir()

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    filesystem = _override_permission_filesystem(override_args)
    assert filesystem[str((root / "memo").resolve())] == "deny"
    assert filesystem["glob_scan_max_depth"] == 64
    routing_rules = filesystem[":workspace_roots"]
    assert routing_rules == {
        "AGENTS.md": "read",
        "INDEX.md": "read",
        "**/AGENTS.md": "read",
        "**/INDEX.md": "read",
    }

    for relative in (
        "AGENTS.md",
        "INDEX.md",
        "src/INDEX.md",
        "src/deep/AGENTS.md",
        "oracle/INDEX.md",
    ):
        assert any(
            access == "read" and fnmatch(relative, pattern)
            for pattern, access in routing_rules.items()
        )
    _assert_not_writable(override_args, root / "memo" / "private.md")


def test_codex_overrides_no_rule_excludes_runtime_blocked_roots(
    tmp_path: Path,
) -> None:
    """NO_RULE でも runtime/Codex の禁止 root を work root-wide write に含めない。"""
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    root = make_repo(tmp_path)
    for name in (".agents", ".cmoc", ".codex", "memo"):
        (root / name).mkdir()
    (root / "src").mkdir()

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.NO_RULE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    assert str(root.resolve()) not in _override_permission_roots(
        override_args, "write"
    )
    for relative in (
        ".agents/blocked.md",
        ".cmoc/local/state.json",
        ".codex/config.toml",
        ".git/config",
        "memo/private.md",
    ):
        _assert_not_writable(override_args, root / relative)
    _assert_writable(override_args, root / "src" / "new.py")


@pytest.mark.parametrize(
    "mode", [FileAccessMode.REALIZATION_WRITE, FileAccessMode.REPO_WRITE]
)
def test_codex_overrides_allows_tracked_cmoc_config_but_blocks_local(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """tracked な config は許可し、runtime state と routing file は保護する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    local_path = root / ".cmoc" / "local"
    local_path.mkdir(parents=True)
    config_path.write_text("{}\n")
    (root / ".gitignore").write_text("/.cmoc/local/\n")
    run_git(root, "add", ".gitignore", ".cmoc/config.json")
    run_git(root, "commit", "-m", "add tracked cmoc config")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    _assert_writable(override_args, config_path)
    _assert_not_writable(override_args, local_path / "state.json")
    _assert_not_writable(override_args, root / "AGENTS.md")
    _assert_not_writable(override_args, root / "INDEX.md")


def test_codex_overrides_allows_root_realization_file_and_protects_ignored_dir(
    tmp_path: Path,
) -> None:
    """root 直下の realization file を許可し、無視対象 directory を保護する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/build/\n")
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('ok')\n")
    (root / "test").mkdir()
    (root / "test" / "test_main.py").write_text("def test_ok(): pass\n")
    (root / "build").mkdir()
    (root / "build" / "artifact.txt").write_text("artifact\n")
    run_git(root, "add", ".gitignore", "src", "test")
    run_git(root, "add", "-f", "build")
    run_git(root, "commit", "-m", "add realization dirs")

    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.REALIZATION_WRITE,
        "prompt",
        None,
    )
    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
    )

    expected_roots = {
        str(root.resolve()),
        str((root / "build" / "artifact.txt").resolve()),
    }
    assert _override_permission_roots(override_args, "write") == expected_roots
    _assert_writable(override_args, root / "src" / "main.py")
    _assert_writable(override_args, root / "src" / "new.py")
    _assert_writable(override_args, root / "build" / "artifact.txt")
    _assert_writable(override_args, root / ".gitignore")
    _assert_not_writable(override_args, root / "build" / "new.txt")
    _assert_not_writable(override_args, root / ".agents" / "blocked.md")
    extra = root / "docs" / "generated.md"

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
        extra_writable_paths=[extra],
    )
    assert _override_permission_roots(override_args, "write") == expected_roots
    _assert_writable(override_args, extra)


@pytest.mark.parametrize(
    ("mode", "extra"),
    [
        (FileAccessMode.REALIZATION_WRITE, "oracle/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, "memo/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, ".agents/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, ".cmoc/local/state.json"),
        (FileAccessMode.REALIZATION_WRITE, ".codex/config.toml"),
        (FileAccessMode.REALIZATION_WRITE, "AGENTS.md"),
        (FileAccessMode.REALIZATION_WRITE, "INDEX.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "src/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "memo/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, ".agents/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "oracle/INDEX.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "oracle/AGENTS.md"),
        (FileAccessMode.REPO_WRITE, "memo/blocked.md"),
        (FileAccessMode.REPO_WRITE, ".agents/blocked.md"),
        (FileAccessMode.REPO_WRITE, ".cmoc/local/state.json"),
        (FileAccessMode.REPO_WRITE, ".git/config"),
        (FileAccessMode.REPO_WRITE, "AGENTS.md"),
        (FileAccessMode.REPO_WRITE, "INDEX.md"),
        (FileAccessMode.REPO_WRITE, "../outside.md"),
    ],
)
def test_codex_overrides_rejects_disallowed_extra_writable_paths(
    tmp_path: Path, mode: FileAccessMode, extra: str
) -> None:
    """モードごとの許可領域外にある追加書き込み先を拒否することを検証する。"""
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    (root / "memo").mkdir()
    (root / ".agents").mkdir()

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_override_args(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                mode,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[root / extra],
        )


@pytest.mark.parametrize(
    "mode", [FileAccessMode.REALIZATION_WRITE, FileAccessMode.REPO_WRITE]
)
def test_codex_overrides_allows_new_root_ancillary_file(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """realization write がルート直下の ancillary ファイルを追加許可できることを検証する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("memo\n")
    (root / "README.md").write_text("# repo\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "add gitignore")

    extra = root / "CHANGELOG.md"
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )
    baseline_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
    )
    _assert_writable(baseline_args, extra)
    assert _override_permission_roots(baseline_args, "write") == {
        str(root.resolve())
    }



@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_readonly_modes_allow_extra_ignored_gap_path(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """読み取り専用モードが ignore された gap path の追加許可を受け入れることを検証する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/scratch.tmp\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "add gitignore")
    target = root / "scratch.tmp"

    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )
    baseline_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
    )
    _assert_not_writable(baseline_args, target)

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
        extra_writable_paths=[target],
    )

    _assert_writable(override_args, target)
