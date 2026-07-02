import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

runner = CliRunner()


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a git command in the test repository and fail on command errors."""
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True
    )


def current_branch(root: Path) -> str:
    """Return the checked-out branch name for git-state assertions."""
    return run_git(root, "branch", "--show-current").stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    """Create the smallest committed repository that cmoc CLI tests can target."""
    root = tmp_path / "repo"
    root.mkdir()
    run_git(root, "init")
    run_git(root, "config", "user.email", "cmoc@example.invalid")
    run_git(root, "config", "user.name", "cmoc test")
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "initial")
    return root


def add_tracked_ignored_oracle_file(root: Path) -> None:
    """Create a tracked oracle file that is also ignored by repository rules."""
    (root / ".gitignore").write_text("oracle/ignored.md\n")
    (root / "oracle" / "ignored.md").write_text("# ignored\n")
    run_git(root, "add", "-f", ".gitignore", "oracle/ignored.md")
    run_git(root, "commit", "-m", "add ignored oracle")


def setup_codex_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Prepare a minimal authenticated Codex home for fake CLI execution."""
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    return codex_home


def stub_codex_profile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Bypass profile generation in tests that target subprocess control."""
    import commons.runtime_codex_exec as exec_module
    import commons.runtime_codex_tui as tui_module

    fallback_path = tmp_path / "cmoc_fake.config.toml"
    fallback_path.write_text('model = "fake"\nsandbox_mode = "read-only"\n')

    def fake_prepare(*args: object, **_kwargs: object) -> Path:
        codex_home = args[2] if len(args) > 2 and isinstance(args[2], Path) else None
        if codex_home is None:
            return fallback_path
        profile_path = codex_home / fallback_path.name
        profile_path.write_text(fallback_path.read_text())
        return profile_path

    monkeypatch.setattr(exec_module, "prepare_codex_profile", fake_prepare)
    monkeypatch.setattr(tui_module, "prepare_codex_profile", fake_prepare)
    return fallback_path


def write_python_executable(path: Path, lines: list[str]) -> None:
    """Write an executable Python script used as a fake external command."""
    path.write_text("\n".join([f"#!{sys.executable}", *lines]) + "\n")
    path.chmod(0o755)


def apply_worktree_from_state(root: Path, state: dict) -> Path:
    """Resolve the apply worktree path encoded by a session state snapshot."""
    import commons.runtime_apply as apply_module

    return apply_module.worktree_for_branch(root, state["apply"]["apply_branch"])
