import socket
import textwrap
from pathlib import Path

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig
from commons.runtime_codex_profile import prepare_codex_profile
from main import app
from _support import make_repo, run_git, runner


def test_doctor_preprocess_repairs_git_state_and_starts_repo_ollama(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    _write_fake_ollama(root / ".cmoc" / "local" / "ollama" / "bin" / "ollama")

    monkeypatch.chdir(root)
    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "/.cmoc/local/" in (root / ".gitignore").read_text()
    assert run_git(root, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    port = int((root / ".cmoc" / "local" / "ollama" / "port").read_text())
    assert 49152 <= port <= 65535
    assert _can_connect(port)
    committed_paths = run_git(root, "show", "--name-only", "--format=", "HEAD").stdout
    assert ".gitignore" in committed_paths
    assert ".agents/.gitkeep" in committed_paths


def test_prepare_local_slm_profile_runs_doctor_when_port_is_missing(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    _write_fake_ollama(root / ".cmoc" / "local" / "ollama" / "bin" / "ollama")
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    monkeypatch.chdir(root)

    profile_path = prepare_codex_profile(
        AgentCallParameter(
            ModelClass.LOCAL_SLM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
        ),
        CmocConfig(),
        codex_home,
        root,
    )

    assert profile_path.is_file()
    assert 'model_provider = "cmoc_ollama"' in profile_path.read_text()
    assert (root / ".cmoc" / "local" / "ollama" / "port").is_file()


def _write_fake_ollama(path: Path) -> None:
    path.parent.mkdir(parents=True)
    path.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            import http.server
            import os
            import sys

            if sys.argv[1:] == ["--version"]:
                print("ollama fake")
                raise SystemExit(0)
            if sys.argv[1:2] in [["show"], ["pull"]]:
                raise SystemExit(0)
            if sys.argv[1:] != ["serve"]:
                raise SystemExit(2)

            host, port = os.environ["OLLAMA_HOST"].split(":")

            class Handler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"models":[]}')

                def log_message(self, *_args):
                    pass

            http.server.ThreadingHTTPServer((host, int(port)), Handler).serve_forever()
            """
        )
    )
    path.chmod(0o755)


def _can_connect(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex(("127.0.0.1", port)) == 0
