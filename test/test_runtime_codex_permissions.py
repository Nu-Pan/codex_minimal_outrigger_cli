"""Codex の read/write 許可領域と追加 writable path を検証する。

根拠:
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
- <work-root>/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
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
    _standard_realization_override_roots,
)
from _git_support import make_repo, run_git


@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_readonly_modes_allow_only_ignored_gap_writes(
    tmp_path: Path, mode: FileAccessMode
) -> None:
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
    ],
)
def test_codex_overrides_protect_memo_and_future_routing_files(
    tmp_path: Path, mode: FileAccessMode
) -> None:
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


def test_codex_overrides_uses_allowed_top_level_roots_for_realization_write(
    tmp_path: Path,
) -> None:
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

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    expected_roots = {
        *_standard_realization_override_roots(root),
        str((root / "build" / "artifact.txt").resolve()),
    }
    assert _override_permission_roots(override_args, "write") == expected_roots
    _assert_writable(override_args, root / "src" / "main.py")
    _assert_writable(override_args, root / "src" / "new.py")
    _assert_writable(override_args, root / ".gitignore")
    _assert_not_writable(override_args, root / "build" / "new.txt")
    _assert_not_writable(override_args, root / ".agents" / "blocked.md")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[root / "build" / "artifact.txt"],
    )
    assert _override_permission_roots(override_args, "write") == expected_roots


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
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    (root / "memo").mkdir()
    (root / ".agents").mkdir()
    if extra == ".gitignore":
        (root / extra).write_text("memo\n")

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


def test_codex_overrides_allows_root_ancillary_extra_writable_path(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("memo\n")
    (root / "README.md").write_text("# repo\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "add gitignore")

    for extra in [root / ".gitignore", root / "README.md"]:
        override_args = build_codex_override_args(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.REALIZATION_WRITE,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[extra],
        )

        assert _override_permission_roots(
            override_args, "write"
        ) == _standard_realization_override_roots(root)
        _assert_writable(override_args, extra)



@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_readonly_modes_allow_extra_ignored_gap_path(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/scratch/\n")
    (root / "scratch").mkdir()
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "add gitignore")
    target = root / "scratch" / "agent.tmp"

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
        extra_writable_paths=[target],
    )

    _assert_writable(override_args, target)
