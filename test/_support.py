import json
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from typer.testing import CliRunner

import cmoc_runtime
import commons.runtime_codex_preflight as codex_preflight_module
import main as main_module
import sub_commands.apply.abandon as apply_abandon_module
import sub_commands.apply.fork as apply_fork_module
import sub_commands.apply.join as apply_module
import sub_commands.indexing as indexing_module
import sub_commands.review as review_module
import sub_commands.session.abandon as session_module
import sub_commands.session.join as session_join_module
import sub_commands.tui as tui_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.path_model import RootToken, resolve_real_path, resolve_token_path
from config.cmoc_config import CmocConfig
from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    ensure_cmoc_ignored,
    file_access_to_sandbox_mode,
    format_duration,
    render_error,
    repo_root,
    run_codex_exec,
    run_codex_tui,
    work_root,
)
from main import app
from sub_commands.tui import parse_markdown_prompt

runner = CliRunner()


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True
    )


def current_branch(root: Path) -> str:
    return run_git(root, "branch", "--show-current").stdout.strip()


def make_repo(tmp_path: Path) -> Path:
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
    (root / ".gitignore").write_text("oracle/ignored.md\n")
    (root / "oracle" / "ignored.md").write_text("# ignored\n")
    run_git(root, "add", "-f", ".gitignore", "oracle/ignored.md")
    run_git(root, "commit", "-m", "add ignored oracle")


def setup_codex_home(tmp_path: Path, monkeypatch) -> Path:
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    return codex_home


def write_python_executable(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join([f"#!{sys.executable}", *lines]) + "\n")
    path.chmod(0o755)


def apply_worktree_from_state(root: Path, state: dict) -> Path:
    return apply_module.worktree_for_branch(root, state["apply"]["apply_branch"])
