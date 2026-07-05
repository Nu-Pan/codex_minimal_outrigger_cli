import json
from pathlib import Path

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from commons.runtime_codex_profile import prepare_codex_profile
from _support import fake_managed_ollama_env, make_repo, run_doctor, run_git


def test_doctor_preprocess_repairs_git_state_and_starts_managed_ollama(
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
    home = root / ".cmoc" / "local" / "test-home"
    service = home / ".config" / "systemd" / "user" / "cmoc-ollama.service"
    assert (home / ".cmoc" / "ollama" / "bin" / "ollama").is_file()
    assert (home / ".cmoc" / "ollama" / "models").is_dir()
    assert service.read_text().splitlines() == [
        "[Unit]",
        "Description=cmoc managed ollama",
        "",
        "[Service]",
        f"ExecStart={home}/.cmoc/ollama/bin/ollama serve",
        "Environment=OLLAMA_HOST=127.0.0.1:11434",
        "Environment=OLLAMA_MODELS=%h/.cmoc/ollama/models",
        "",
        "[Install]",
        "WantedBy=default.target",
    ]
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
        json.dumps(
            {
                "num_parallel": 3,
                "codex": {
                    "model": {
                        "mainstream": {
                            "model_provider": "codex",
                            "model": "CUSTOM",
                        }
                    }
                },
            }
        )
        + "\n"
    )
    monkeypatch.chdir(root)

    run_doctor(root)

    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model"]["mainstream"] == {
        "model_provider": "codex",
        "model": "CUSTOM",
    }
    assert data["codex"]["model"]["efficiency"] == {
        "model_provider": "codex",
        "model": "gpt-5.4-mini",
    }
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
    for key, value in fake_managed_ollama_env(root).items():
        monkeypatch.setenv(key, value)
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", "smollm2:135m")

    profile_path = prepare_codex_profile(
        AgentCallParameter(
            ModelClass.MINIMUM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
        ),
        config,
        codex_home,
        root,
    )

    assert profile_path.is_file()
    assert 'model_provider = "cmoc_managed_ollama"' in profile_path.read_text()
    assert (
        root
        / ".cmoc"
        / "local"
        / "test-home"
        / ".config"
        / "systemd"
        / "user"
        / "cmoc-ollama.service"
    ).is_file()
