import atexit
import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from click.testing import Result
from typer.testing import CliRunner

runner = CliRunner()
_FAKE_OLLAMA_PID_PATHS: set[Path] = set()

# <work-root>/oracle/doc/dev_rule/test_rule.md は Codex CLI テストで使う
# local SLM を固定している。
TEST_SLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"


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
    # <work-root>/oracle/doc/dev_rule/test_rule.md: cmoc の制御ロジック実行前に、
    # テストリポジトリが user Git signing や hook 設定へ依存しないようにする。
    run_git(root, "config", "commit.gpgsign", "false")
    run_git(root, "config", "core.hooksPath", "/dev/null")
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


def codex_parameter(mode: FileAccessMode = FileAccessMode.READONLY) -> AgentCallParameter:
    """Build the small default Codex parameter used by runtime wrapper tests."""
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


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


def run_doctor(root: Path) -> Result:
    """Run doctor with fake managed Ollama/systemctl commands."""
    from main import app

    env = fake_managed_ollama_env(root)
    result = runner.invoke(app, ["doctor"], env=env, catch_exceptions=False)
    assert result.exit_code == 0
    return result


def fake_managed_ollama_env(root: Path) -> dict[str, str]:
    """Prepare fake commands for tests that trigger doctor through profile creation."""
    home = root / ".cmoc" / "local" / "test-home"
    fake_bin = root / ".cmoc" / "local" / "fake-bin"
    _stop_registered_fake_ollama_services()
    _FAKE_OLLAMA_PID_PATHS.add(home / ".cmoc" / "ollama" / "service.pid")
    _write_fake_ollama(home / ".cmoc" / "ollama" / "bin" / "ollama")
    _write_fake_systemctl(fake_bin / "systemctl", home)
    return {
        "HOME": str(home),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
    }


def _stop_registered_fake_ollama_services() -> None:
    # <work-root>/oracle/doc/dev_rule/test_rule.md は fake service state を各
    # tmp_path 配下に保つ。この in-memory registry は同一 pytest process 内の
    # テスト間で fixed-port collision を避けるためだけに使う。
    for pid_path in _FAKE_OLLAMA_PID_PATHS:
        try:
            process_id = int(pid_path.read_text())
        except (OSError, ValueError):
            continue
        try:
            os.kill(process_id, signal.SIGTERM)
        except OSError:
            continue
        for _ in range(20):
            try:
                os.kill(process_id, 0)
            except OSError:
                break
            time.sleep(0.05)


atexit.register(_stop_registered_fake_ollama_services)


def _write_fake_ollama(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_python_executable(
        path,
        textwrap.dedent(
            """\
            import http.server
            import json
            import os
            import sys

            if sys.argv[1:] == ["--version"]:
                print("ollama fake")
                raise SystemExit(0)
            if sys.argv[1:2] in [["show"], ["pull"]]:
                assert os.environ["OLLAMA_HOST"] == "127.0.0.1:11434"
                assert os.environ["OLLAMA_MODELS"].endswith("/.cmoc/ollama/models")
                raise SystemExit(0)
            if sys.argv[1:] != ["serve"]:
                raise SystemExit(2)

            host, port = os.environ["OLLAMA_HOST"].split(":")

            class Handler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"models":[]}')

                def do_POST(self):
                    if self.path != "/api/generate":
                        self.send_response(404)
                        self.end_headers()
                        return
                    length = int(self.headers.get("content-length", "0"))
                    payload = json.loads(self.rfile.read(length))
                    assert payload["model"]
                    assert payload["stream"] is False
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"done":true}')

                def log_message(self, *_args):
                    pass

            http.server.ThreadingHTTPServer((host, int(port)), Handler).serve_forever()
            """
        ).splitlines(),
    )


def _write_fake_systemctl(path: Path, home: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_python_executable(
        path,
        textwrap.dedent(
            f"""\
            import os
            import subprocess
            import sys
            from pathlib import Path

            home = Path({str(home)!r})
            service = home / ".config" / "systemd" / "user" / "cmoc-ollama.service"
            pid_path = home / ".cmoc" / "ollama" / "service.pid"

            args = sys.argv[1:]
            if args[:1] == ["--user"]:
                args = args[1:]
            if args == ["daemon-reload"]:
                raise SystemExit(0)
            if args == ["enable", "--now", "cmoc-ollama"]:
                lines = service.read_text().splitlines()
                exec_start = next(line for line in lines if line.startswith("ExecStart="))
                env_lines = [line.removeprefix("Environment=") for line in lines if line.startswith("Environment=")]
                env = os.environ.copy()
                env.update(dict(item.split("=", 1) for item in env_lines))
                argv = exec_start.removeprefix("ExecStart=").split()
                if pid_path.exists():
                    try:
                        os.kill(int(pid_path.read_text()), 0)
                        raise SystemExit(0)
                    except OSError:
                        pass
                process = subprocess.Popen(argv, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                pid_path.parent.mkdir(parents=True, exist_ok=True)
                pid_path.write_text(str(process.pid))
                raise SystemExit(0)
            if args == ["is-active", "--quiet", "cmoc-ollama"]:
                if not pid_path.exists():
                    raise SystemExit(3)
                raise SystemExit(0)
            if args == ["show", "cmoc-ollama", "--property=MainPID", "--value"]:
                print(pid_path.read_text().strip() if pid_path.exists() else "0")
                raise SystemExit(0)
            print("unsupported fake systemctl args: " + repr(args), file=sys.stderr)
            raise SystemExit(2)
            """
        ).splitlines(),
    )


def apply_worktree_from_state(root: Path, state: dict) -> Path:
    """Resolve the apply worktree path encoded by a session state snapshot."""
    import commons.runtime_apply as apply_module

    return apply_module.worktree_for_branch(root, state["apply"]["apply_branch"])
