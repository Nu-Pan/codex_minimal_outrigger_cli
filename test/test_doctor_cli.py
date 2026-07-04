import socket
import json
from pathlib import Path

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig
from commons.runtime_codex_profile import prepare_codex_profile
from main import app
from _support import make_repo, run_doctor, run_git, runner


def test_doctor_preprocess_repairs_git_state_and_starts_repo_ollama(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)

    monkeypatch.chdir(root)
    result = run_doctor(root)

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
    assert ".cmoc/config.json" in committed_paths


def test_doctor_syncs_default_config_without_overwriting_human_values(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    config_path.parent.mkdir()
    config_path.write_text(
        json.dumps({"num_parallel": 3, "codex": {"model": {"mainstream": "CUSTOM"}}})
        + "\n"
    )
    monkeypatch.chdir(root)

    run_doctor(root)

    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model"]["mainstream"] == "CUSTOM"
    assert data["codex"]["model"]["efficiency"] == "gpt-5.4-mini"
    assert data["codex"]["reasoning_effort"]["low"] == "low"
    assert data["apply_fork"]["num_apply_files"] == 200


def test_doctor_repair_commit_does_not_include_preexisting_staged_changes(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    user_file = root / "user.txt"
    user_file.write_text("user change\n")
    run_git(root, "add", "user.txt")
    monkeypatch.chdir(root)

    run_doctor(root)

    committed_paths = run_git(root, "show", "--name-only", "--format=", "HEAD").stdout
    assert "user.txt" not in committed_paths
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "user.txt"
    ]


def test_prepare_local_slm_profile_runs_doctor_when_port_is_missing(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)
    (root / ".cmoc" / "local" / "ollama" / "port").unlink()
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()

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


def _can_connect(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex(("127.0.0.1", port)) == 0
