import json
from pathlib import Path

import pytest

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
import commons.runtime_doctor as doctor_module
from commons.runtime_config import write_config
from commons.runtime_errors import CmocError
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from commons.runtime_codex_profile import prepare_codex_profile
from main import app
from _support import (
    TEST_SLM_MODEL,
    fake_managed_ollama_env,
    make_repo,
    runner,
    run_doctor,
    run_git,
)


def test_doctor_preprocess_repairs_git_state_and_starts_managed_ollama(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)
    write_config(root / ".cmoc" / "config.json", config)

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
    assert ".cmoc/config.json" not in committed_paths
    assert run_git(root, "ls-files", "--", ".cmoc").stdout.strip() == ""
    assert (
        run_git(root, "check-ignore", "-q", ".cmoc/config.json").returncode == 0
    )


def test_verify_ollama_service_rejects_missing_main_pid(monkeypatch) -> None:
    executable = Path("/home/user/.cmoc/ollama/bin/ollama")

    monkeypatch.setattr(doctor_module, "_service_active", lambda: True)
    monkeypatch.setattr(doctor_module, "_service_main_pid", lambda: None)

    with pytest.raises(CmocError):
        doctor_module._verify_ollama_service(executable)


def test_ollama_listener_must_be_expected_service_process(monkeypatch) -> None:
    executable = Path("/home/user/.cmoc/ollama/bin/ollama")

    monkeypatch.setattr(doctor_module, "_ollama_listener_process_ids", lambda: {20, 30})
    monkeypatch.setattr(
        doctor_module, "_process_is_descendant", lambda pid, main: pid == 20
    )
    monkeypatch.setattr(
        doctor_module,
        "_process_argv_uses_executable",
        lambda pid, path: path == executable and pid == 30,
    )

    assert not doctor_module._listener_matches_service(10, executable)

    monkeypatch.setattr(
        doctor_module,
        "_process_argv_uses_executable",
        lambda pid, path: path == executable and pid == 20,
    )

    assert doctor_module._listener_matches_service(10, executable)


def test_doctor_pulls_each_unique_cmoc_provider_model(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    config = CmocConfig()
    config.codex.model[ModelClass.MAINSTREAM] = CodexModelSpec("cmoc", "alpha")
    config.codex.model[ModelClass.FLAGSHIP] = CodexModelSpec("cmoc", "beta")
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", "alpha")
    write_config(root / ".cmoc" / "config.json", config)
    pulled: list[str] = []

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(
        doctor_module, "_ensure_ollama_installed", lambda: Path("ollama")
    )
    monkeypatch.setattr(
        doctor_module, "_ensure_ollama_service", lambda executable: None
    )
    monkeypatch.setattr(
        doctor_module, "_verify_ollama_service", lambda executable: None
    )
    monkeypatch.setattr(
        doctor_module,
        "_ensure_ollama_model",
        lambda executable, model: pulled.append(model),
    )

    doctor_module.run_doctor_preprocess(root)

    assert pulled == ["alpha", "beta"]


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


def test_init_generates_config_and_ignores_cmoc(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    result = runner.invoke(
        app,
        ["init"],
        env=fake_managed_ollama_env(root),
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "# cmoc init" in result.stdout
    assert (root / ".cmoc" / "config.json").is_file()
    assert run_git(root, "check-ignore", "-q", ".cmoc/config.json").returncode == 0
    assert run_git(root, "ls-files", "--", ".cmoc").stdout.strip() == ""


def test_doctor_preprocess_untracks_existing_cmoc_files(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    write_config(config_path, CmocConfig())
    run_git(root, "add", "-f", ".cmoc/config.json")
    run_git(root, "commit", "-m", "track old cmoc config")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert run_git(root, "ls-files", "--", ".cmoc").stdout.strip() == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""


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


def test_doctor_repair_commit_does_not_include_preexisting_staged_gitignore(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    gitignore.write_text("human-rule\n")
    run_git(root, "add", ".gitignore")
    monkeypatch.chdir(root)

    run_doctor(root)

    committed_gitignore = run_git(root, "show", "HEAD:.gitignore").stdout
    assert "human-rule" not in committed_gitignore
    assert "/.cmoc/local/" in committed_gitignore
    assert gitignore.read_text() == "human-rule\n\n/.cmoc/\n/.cmoc/local/\n"
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        ".gitignore"
    ]
    assert "human-rule" in run_git(root, "diff", "--cached").stdout


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
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)

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
