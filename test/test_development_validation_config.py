"""自己開発用 dependency と blocking tool 設定の機械可読契約を検証する。"""

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_development_tools_are_isolated_in_dev_extra() -> None:
    """自己開発専用 tool を runtime dependency へ混在させない。"""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    runtime_dependencies = project["project"]["dependencies"]
    dev_dependencies = project["project"]["optional-dependencies"]["dev"]

    assert all(
        not dependency.startswith(("pytest", "ruff", "mypy"))
        for dependency in runtime_dependencies
    )
    for dependency_prefix in (
        "pytest>=",
        "pytest-timeout>=",
        "ruff>=",
        "mypy>=",
    ):
        assert any(
            dependency.startswith(dependency_prefix) for dependency in dev_dependencies
        )


def test_validation_tools_have_blocking_project_configuration() -> None:
    """Ruff、mypy、pytest-timeout の対象と主要な failure 条件を固定する。"""
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]

    assert config["ruff"]["target-version"] == "py312"
    assert config["ruff"]["lint"]["select"] == ["E4", "E7", "E9", "F", "I", "B"]
    assert config["mypy"]["files"] == ["src", "oracle/src", "test"]
    assert config["mypy"]["disallow_untyped_defs"] is True
    assert config["mypy"]["check_untyped_defs"] is True
    assert config["mypy"]["warn_return_any"] is True
    assert config["mypy"]["warn_unused_ignores"] is True
    assert config["pytest"]["ini_options"]["timeout"] == 180
    assert config["pytest"]["ini_options"]["timeout_method"] == "signal"


def test_workspace_uses_ruff_as_the_only_python_formatter() -> None:
    """VS Code の Python formatter を Ruff と一致させる。"""
    workspace_text = (ROOT / "codex_minimal_outrigger_cli.code-workspace").read_text()
    workspace = json.loads(workspace_text)

    assert (
        workspace["settings"]["[python]"]["editor.defaultFormatter"]
        == "charliermarsh.ruff"
    )
    assert "black-formatter" not in workspace_text
