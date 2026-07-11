import os
import subprocess
import tempfile
import textwrap
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest
from click.testing import Result

from _cli_support import runner
from _command_support import write_python_executable

# <work-root>/oracle/doc/dev_rule/test_rule.md
# <work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md
# Deterministic tests use a separate endpoint; Real Codex never enters this context.


TEST_SLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"
_FAKE_OLLAMA_HOME = Path(tempfile.gettempdir()) / f"cmoc-test-ollama-v2-{os.getuid()}"
FAKE_OLLAMA_HOST = "127.0.0.1:11436"


def run_doctor(root: Path) -> Result:
    """Run doctor against the isolated deterministic Ollama service."""
    from main import app

    env = fake_managed_ollama_env(root)
    with fake_managed_ollama_runtime():
        result = runner.invoke(app, ["doctor"], env=env, catch_exceptions=False)
    assert result.exit_code == 0
    return result


def fake_managed_ollama_env(root: Path) -> dict[str, str]:
    """Prepare fake commands for deterministic doctor and provider tests."""
    env = fake_managed_systemctl_env(root)
    home = Path(env["HOME"])
    _write_fake_ollama(home / ".cmoc" / "ollama" / "bin" / "ollama")
    return env


def fake_managed_systemctl_env(_root: Path) -> dict[str, str]:
    """Use a fake HOME and user service, separate from production Ollama."""
    home = _FAKE_OLLAMA_HOME
    fake_bin = home / "bin"
    _write_fake_systemctl(fake_bin / "systemctl", home)
    return {
        "HOME": str(home),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
    }


@contextmanager
def fake_managed_ollama_runtime() -> Iterator[None]:
    """Point runtime Ollama checks at the deterministic test-only endpoint."""
    import commons.runtime_ollama as ollama_module

    previous_host = ollama_module._OLLAMA_HOST
    previous_listener = ollama_module._is_ollama_listen_socket

    def fake_listener(local_address: str, state: str) -> bool:
        if state != "0A":
            return False
        host_hex, port_hex = local_address.rsplit(":", 1)
        fake_port = int(FAKE_OLLAMA_HOST.rsplit(":", 1)[1])
        return host_hex == "0100007F" and int(port_hex, 16) == fake_port

    ollama_module._OLLAMA_HOST = FAKE_OLLAMA_HOST
    ollama_module._is_ollama_listen_socket = fake_listener

    try:
        yield
    finally:
        ollama_module._OLLAMA_HOST = previous_host
        ollama_module._is_ollama_listen_socket = previous_listener


def _write_fake_ollama(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    write_python_executable(
        path,
        textwrap.dedent(
            f"""\
            import http.server
            import json
            import os
            import sys

            if sys.argv[1:] == ["--version"]:
                print("ollama fake")
                raise SystemExit(0)
            if sys.argv[1:2] in [["show"], ["pull"]]:
                assert os.environ["OLLAMA_HOST"] == "{FAKE_OLLAMA_HOST}"
                assert os.environ["OLLAMA_MODELS"].endswith("/.cmoc/ollama/models")
                raise SystemExit(0)
            if sys.argv[1:] != ["serve"]:
                raise SystemExit(2)

            host, port = os.environ["OLLAMA_HOST"].split(":")
            loaded_model = None

            class Handler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == "/api/ps":
                        models = ([{{"name": loaded_model, "size_vram": 1}}]
                                  if loaded_model else [])
                        body = {{"models": models}}
                    else:
                        body = {{"models": []}}
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(body).encode())

                def do_POST(self):
                    global loaded_model
                    if self.path != "/api/generate":
                        self.send_response(404)
                        self.end_headers()
                        return
                    length = int(self.headers.get("content-length", "0"))
                    payload = json.loads(self.rfile.read(length))
                    loaded_model = payload["model"]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{{"done":true}}')

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
            import time
            from pathlib import Path

            home = Path({str(home)!r})
            service = home / ".config" / "systemd" / "user" / "cmoc-ollama.service"
            pid_path = home / ".cmoc" / "ollama" / "service.pid"
            args = sys.argv[1:]
            if args[:1] == ["--user"]:
                args = args[1:]
            if args == ["daemon-reload"]:
                raise SystemExit(0)
            if args in [["enable", "--now", "cmoc-ollama"], ["restart", "cmoc-ollama"]]:
                lines = service.read_text().splitlines()
                exec_start = next(line for line in lines if line.startswith("ExecStart="))
                env_lines = [line.removeprefix("Environment=") for line in lines if line.startswith("Environment=")]
                env = os.environ.copy()
                env.update({{
                    key: value.replace("%h", str(home))
                    for key, value in (item.split("=", 1) for item in env_lines)
                }})
                argv = exec_start.removeprefix("ExecStart=").split()
                if args == ["enable", "--now", "cmoc-ollama"] and pid_path.exists():
                    try:
                        if Path(f"/proc/{{int(pid_path.read_text())}}").exists():
                            raise SystemExit(0)
                    except ValueError:
                        pass
                if args == ["restart", "cmoc-ollama"] and pid_path.exists():
                    try:
                        old_pid = int(pid_path.read_text())
                        os.kill(old_pid, 15)
                        for _ in range(20):
                            if not Path(f"/proc/{{old_pid}}").exists():
                                break
                            time.sleep(0.05)
                    except (OSError, ValueError):
                        pass
                    pid_path.unlink(missing_ok=True)
                process = subprocess.Popen(argv, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                pid_path.parent.mkdir(parents=True, exist_ok=True)
                pid_path.write_text(str(process.pid))
                raise SystemExit(0)
            if args == ["is-active", "--quiet", "cmoc-ollama"]:
                raise SystemExit(0 if pid_path.exists() else 3)
            if args == ["show", "cmoc-ollama", "--property=MainPID", "--value"]:
                print(pid_path.read_text().strip() if pid_path.exists() else "0")
                raise SystemExit(0)
            print("unsupported fake systemctl args: " + repr(args), file=sys.stderr)
            raise SystemExit(2)
            """
        ).splitlines(),
    )
