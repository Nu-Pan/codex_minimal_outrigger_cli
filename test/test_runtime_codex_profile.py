"""Codex override の model、root、permission profile 基本契約を検証する。

根拠:
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
- <work-root>/oracle/doc/app_spec/codex_exec_rule.md
- <work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md
"""

from pathlib import Path

import pytest

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec

from _codex_support import (
    _assert_not_permission_accessible,
    _assert_not_writable,
    _assert_writable,
    _override_permission_filesystem,
    _override_permission_roots,
    _override_writable_roots,
    codex_arg_value,
    codex_override_config,
)
from _git_support import make_repo, run_git
from _ollama_support import TEST_SLM_MODEL


def test_codex_overrides_generates_rooted_sandbox(tmp_path: Path) -> None:
    """root 付き通常経路でも FileAccessMode ごとの argv を生成する。"""
    root = make_repo(tmp_path)
    (root / ".cmoc").mkdir()
    (root / ".codex").mkdir()
    (root / ".pytest_cache").mkdir()
    (root / "AGENTS.md").write_text("agents\n")
    (root / "INDEX.md").write_text("index\n")
    (root / "src").mkdir()
    (root / "src" / "INDEX.md").write_text("index\n")
    (root / "src" / "existing.py").write_text("print('ok')\n")
    (root / "test").mkdir()
    (root / "test" / "INDEX.md").write_text("index\n")
    (root / "test" / "test_existing.py").write_text("def test_ok(): pass\n")
    (root / "README.md").write_text("# repo\n")
    (root / "oracle" / "INDEX.md").write_text("index\n")
    (root / "oracle" / "AGENTS.md").write_text("agents\n")
    (root / "oracle" / "spec.md").write_text("# spec\n")
    (root / "memo").mkdir()
    (root / ".agents").mkdir()
    (root / ".gitignore").write_text("memo\n")

    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    overrides = {
        mode: build_codex_override_args(
            AgentCallParameter(
                parameter.model_class,
                parameter.reasoning_effort,
                mode,
                parameter.prompt,
                parameter.structured_output_schema_path,
            ),
            CmocConfig(),
            root,
        )
        for mode in FileAccessMode
    }

    for mode in FileAccessMode:
        parsed = codex_override_config(overrides[mode])
        assert "--sandbox" not in overrides[mode]
        assert "sandbox_workspace_write" not in parsed
        assert parsed["default_permissions"] == "cmoc"
        assert parsed["permissions"]["cmoc"]["extends"] == ":workspace"
    assert _override_permission_filesystem(overrides[FileAccessMode.READONLY]) == {
        str(path.resolve()): "read"
        for path in root.iterdir()
        if path.name != "memo"
    }
    _assert_not_permission_accessible(
        overrides[FileAccessMode.READONLY], root / "memo" / "private.md"
    )
    assert str((root / ".agents").resolve()) in _override_permission_roots(
        overrides[FileAccessMode.READONLY], "read"
    )
    assert _override_permission_filesystem(
        overrides[FileAccessMode.PURE_ORACLE_READ]
    ) == {str((root / "oracle").resolve()): "read"}
    pure_oracle_write_filesystem = _override_permission_filesystem(
        overrides[FileAccessMode.PURE_ORACLE_WRITE]
    )
    assert pure_oracle_write_filesystem[str((root / "oracle").resolve())] == "write"
    for name in ("AGENTS.md", "INDEX.md"):
        assert pure_oracle_write_filesystem[
            str((root / "oracle" / name).resolve())
        ] == "read"
    _assert_not_permission_accessible(
        overrides[FileAccessMode.PURE_ORACLE_WRITE], root / "src" / "existing.py"
    )
    realization_roots = {str(root.resolve())}
    assert _override_permission_roots(
        overrides[FileAccessMode.REALIZATION_WRITE], "write"
    ) == realization_roots
    assert _override_writable_roots(overrides[FileAccessMode.READONLY]) == set()
    assert _override_writable_roots(overrides[FileAccessMode.PURE_ORACLE_READ]) == set()
    assert _override_writable_roots(overrides[FileAccessMode.PURE_ORACLE_WRITE]) == set()
    assert _override_permission_roots(
        overrides[FileAccessMode.READONLY], "write"
    ) == set()
    assert _override_permission_roots(
        overrides[FileAccessMode.PURE_ORACLE_READ], "write"
    ) == set()
    assert _override_permission_roots(
        overrides[FileAccessMode.PURE_ORACLE_WRITE], "write"
    ) == {str((root / "oracle").resolve())}
    assert _override_permission_roots(
        overrides[FileAccessMode.REPO_WRITE], "write"
    ) == realization_roots
    _assert_writable(
        overrides[FileAccessMode.REALIZATION_WRITE], root / "src" / "existing.py"
    )
    _assert_writable(
        overrides[FileAccessMode.REALIZATION_WRITE], root / "src" / "new.py"
    )
    _assert_writable(
        overrides[FileAccessMode.REALIZATION_WRITE], root / "test" / "test_new.py"
    )
    _assert_not_writable(overrides[FileAccessMode.REALIZATION_WRITE], root / "INDEX.md")
    for path in (root / "src" / "INDEX.md", root / "test" / "INDEX.md"):
        assert _override_permission_filesystem(
            overrides[FileAccessMode.REALIZATION_WRITE]
        )[str(path.resolve())] == "read"
        _assert_not_writable(overrides[FileAccessMode.REALIZATION_WRITE], path)
    _assert_writable(overrides[FileAccessMode.REALIZATION_WRITE], root / ".gitignore")
    _assert_not_writable(
        overrides[FileAccessMode.REALIZATION_WRITE], root / ".agents" / "blocked.md"
    )
    _assert_not_writable(
        overrides[FileAccessMode.PURE_ORACLE_READ], root / "oracle" / "blocked.md"
    )
    for name in ("AGENTS.md", "INDEX.md"):
        path = root / "oracle" / name
        assert _override_permission_filesystem(
            overrides[FileAccessMode.REPO_WRITE]
        )[str(path.resolve())] == "read"
        _assert_not_writable(overrides[FileAccessMode.REPO_WRITE], path)
    _assert_writable(
        overrides[FileAccessMode.REPO_WRITE], root / "oracle" / "spec.md"
    )
    _assert_writable(
        overrides[FileAccessMode.REPO_WRITE], root / "oracle" / "new.md"
    )
    _assert_not_writable(overrides[FileAccessMode.REPO_WRITE], root / "INDEX.md")
    _assert_writable(
        overrides[FileAccessMode.PURE_ORACLE_WRITE], root / "oracle" / "new.md"
    )
    _assert_writable(overrides[FileAccessMode.REPO_WRITE], root / ".gitignore")
    _assert_not_writable(
        overrides[FileAccessMode.REPO_WRITE], root / ".agents" / "blocked.md"
    )

    extra = root / "src" / "existing.py"
    override_args = build_codex_override_args(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.REALIZATION_WRITE,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[extra],
    )
    assert _override_permission_roots(override_args, "write") == realization_roots

    repo_extra = root / "new_dir"
    override_args = build_codex_override_args(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.REPO_WRITE,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[repo_extra],
    )
    _assert_writable(override_args, repo_extra)

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_override_args(
            parameter,
            CmocConfig(),
            root,
            [root / "memo" / "blocked.md"],
        )

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_override_args(
            AgentCallParameter(
                parameter.model_class,
                parameter.reasoning_effort,
                FileAccessMode.PURE_ORACLE_READ,
                parameter.prompt,
                parameter.structured_output_schema_path,
            ),
            CmocConfig(),
            root,
            [root / "src" / "blocked.md"],
        )

    build_codex_override_args(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.PURE_ORACLE_READ,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        root,
        [root / ".cmoc" / "local" / "log" / "tui" / "20260101_cmpl.md"],
    )

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_override_args(
            AgentCallParameter(
                parameter.model_class,
                parameter.reasoning_effort,
                FileAccessMode.PURE_ORACLE_READ,
                parameter.prompt,
                parameter.structured_output_schema_path,
            ),
            CmocConfig(),
            root,
            [root / ".cmoc" / "local" / "log" / "tui" / "20260101_orig.md"],
        )


def test_codex_overrides_uses_cmoc_ollama_provider_for_local_slm(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.MINIMUM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
        ),
        config,
        root,
    )

    parsed = codex_override_config(override_args)
    provider = parsed["model_providers"]["cmoc_managed_ollama"]
    assert codex_arg_value(override_args, "--model") == TEST_SLM_MODEL
    assert codex_arg_value(override_args, "--disable") == "multi_agent"
    assert parsed["web_search"] == "disabled"
    assert parsed["model_provider"] == "cmoc_managed_ollama"
    assert provider == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }


def test_standard_realization_roots_follow_path_boundaries(tmp_path: Path) -> None:
    """Expected roots exclude outside symlinks and untracked ignored paths."""
    root = make_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "src").symlink_to(outside, target_is_directory=True)
    (root / "test").mkdir()
    (root / "test" / "nested").mkdir()
    (root / "test" / "nested" / "link").symlink_to(
        outside, target_is_directory=True
    )
    (root / ".gitignore").write_text("test/\n")

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

    assert _override_permission_roots(override_args, "write") == {
        str(root.resolve())
    }
    filesystem = _override_permission_filesystem(override_args)
    assert filesystem[str(outside.resolve())] == "deny"
    _assert_not_writable(override_args, outside / "new.py")


def test_codex_overrides_allows_repo_local_read_from_linked_worktree(
    tmp_path: Path,
) -> None:
    """linked worktree 実行時だけ repo 側 cmoc/local 読み取りを追加許可する。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked-read"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-read", str(linked), "HEAD")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.PURE_ORACLE_READ,
        "prompt",
        None,
    )

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        linked,
        [root / ".cmoc" / "local" / "report" / "review" / "report.md"],
        extra_read_root=root,
    )
    filesystem = _override_permission_filesystem(override_args)
    assert codex_override_config(override_args)["default_permissions"] == "cmoc"
    assert filesystem[str((root / ".cmoc" / "local").resolve())] == "read"
    assert "sandbox_workspace_write" not in codex_override_config(override_args)

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        linked,
        extra_read_root=root,
    )
    filesystem = _override_permission_filesystem(override_args)
    assert filesystem[str((root / ".cmoc" / "local").resolve())] == "read"

    override_args = build_codex_override_args(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.REPO_WRITE,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        linked,
        extra_read_root=root,
    )
    parsed = codex_override_config(override_args)
    assert "--sandbox" not in override_args
    assert parsed["permissions"]["cmoc"]["filesystem"][
        str((root / ".cmoc" / "local").resolve())
    ] == "read"

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_override_args(
            parameter,
            CmocConfig(),
            linked,
            [root / "src" / "blocked.md"],
            extra_read_root=root,
        )
