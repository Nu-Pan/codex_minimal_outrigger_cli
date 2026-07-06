import json
import subprocess
from pathlib import Path

import pytest

from basic.acp import ModelClass
import commons.runtime_doctor as doctor_module
import commons.runtime_ollama as ollama_module
from commons.runtime_config import write_config
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
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
    monkeypatch: pytest.MonkeyPatch,
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
    repair_commit_paths = run_git(
        root, "show", "--name-only", "--format=", "HEAD~1"
    ).stdout
    assert ".gitignore" in repair_commit_paths
    assert ".agents/.gitkeep" in repair_commit_paths
    config_commit_paths = run_git(
        root, "show", "--name-only", "--format=", "HEAD"
    ).stdout
    assert config_commit_paths.splitlines() == [".cmoc/config.json"]
    assert run_git(root, "ls-files", "--", ".cmoc/local").stdout.strip() == ""
    assert (
        run_git(
            root,
            "check-ignore",
            "-q",
            ".cmoc/local/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/config.json"],
            cwd=root,
            check=False,
        ).returncode
        != 0
    )


def test_doctor_pulls_each_unique_cmoc_provider_model(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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
        ollama_module, "_ensure_ollama_installed", lambda: Path("ollama")
    )
    monkeypatch.setattr(
        ollama_module, "_ensure_ollama_service", lambda executable: None
    )
    monkeypatch.setattr(
        ollama_module, "_verify_ollama_service", lambda executable: None
    )
    monkeypatch.setattr(
        ollama_module,
        "_ensure_ollama_model",
        lambda executable, model: pulled.append(model),
    )

    doctor_module.run_doctor_preprocess(root)

    assert pulled == ["alpha", "beta"]


def test_doctor_preprocess_in_linked_worktree_uses_repo_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked-ollama-config"
    run_git(root, "worktree", "add", "-b", "linked-ollama-config", str(linked), "HEAD")
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", "repo-model")
    write_config(root / ".cmoc" / "config.json", config)
    pulled: list[str] = []

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(
        ollama_module, "_ensure_ollama_installed", lambda: Path("ollama")
    )
    monkeypatch.setattr(
        ollama_module, "_ensure_ollama_service", lambda executable: None
    )
    monkeypatch.setattr(
        ollama_module, "_verify_ollama_service", lambda executable: None
    )
    monkeypatch.setattr(
        ollama_module,
        "_ensure_ollama_model",
        lambda executable, model: pulled.append(model),
    )

    doctor_module.run_doctor_preprocess(linked)

    assert pulled == ["repo-model"]
    assert not (linked / ".cmoc" / "config.json").exists()


def test_doctor_generates_and_tracks_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    monkeypatch.chdir(root)

    run_doctor(root)

    assert config_path.is_file()
    assert (
        run_git(root, "ls-files", "--", ".cmoc/config.json").stdout.strip()
        == ".cmoc/config.json"
    )
    assert json.loads(config_path.read_text())["codex"]["num_try_falv_recovery"] == 1
    assert run_git(
        root, "show", "--name-only", "--format=", "HEAD"
    ).stdout.splitlines() == [".cmoc/config.json"]


def test_dector_alias_runs_doctor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    result = runner.invoke(
        app,
        ["dector"],
        env=fake_managed_ollama_env(root),
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert (root / ".cmoc" / "config.json").is_file()


def test_doctor_preprocess_targets_current_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked-doctor"
    run_git(root, "worktree", "add", "-b", "linked-doctor", str(linked), "HEAD")
    monkeypatch.chdir(linked)

    result = runner.invoke(
        app,
        ["doctor"],
        env=fake_managed_ollama_env(linked),
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "/.cmoc/local/" in (linked / ".gitignore").read_text()
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(
        linked, "check-ignore", "-q", ".cmoc/local/.__cmoc_ignore_probe__"
    ).returncode == 0
    assert not (root / ".gitignore").exists()
    assert not (root / ".agents").exists()
    assert (root / ".cmoc" / "config.json").is_file()
    assert not (linked / ".cmoc" / "config.json").exists()
    assert f"- repo_root: `{root}`" in result.stdout


def test_doctor_syncs_default_config_without_overwriting_human_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    config_path.parent.mkdir()
    config_path.write_text(
        json.dumps(
            {
                "num_parallel": 3,
                "codex": {
                    "num_try_falv_recovery": 4,
                    "model": {
                        "mainstream": {
                            "model_provider": "codex",
                            "model": "CUSTOM",
                        }
                    },
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
    assert data["codex"]["num_try_falv_recovery"] == 4
    assert data["codex"]["reasoning_effort"]["low"] == "low"
    assert data["apply_fork"]["num_apply_files"] == 200


def test_doctor_preprocess_untracks_existing_cmoc_local_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    local_path = root / ".cmoc" / "local" / "cache.json"
    local_path.parent.mkdir(parents=True)
    local_path.write_text("{}\n")
    run_git(root, "add", "-f", ".cmoc/local/cache.json")
    run_git(root, "commit", "-m", "track old cmoc local cache")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert run_git(root, "ls-files", "--", ".cmoc/local").stdout.strip() == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_doctor_preprocess_does_not_restore_preexisting_staged_cmoc_local_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    local_path = root / ".cmoc" / "local" / "cache.json"
    local_path.parent.mkdir(parents=True)
    local_path.write_text('{"old": true}\n')
    run_git(root, "add", "-f", ".cmoc/local/cache.json")
    run_git(root, "commit", "-m", "track old cmoc local cache")
    local_path.write_text('{"new": true}\n')
    run_git(root, "add", "-f", ".cmoc/local/cache.json")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert local_path.read_text() == '{"new": true}\n'
    assert run_git(root, "ls-files", "--", ".cmoc/local").stdout.strip() == ""
    assert run_git(root, "diff", "--cached", "--name-only").stdout.strip() == ""


def test_doctor_repair_commit_does_not_include_preexisting_staged_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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
    assert gitignore.read_text() == "human-rule\n\n/.cmoc/local/\n"
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        ".gitignore"
    ]
    assert "human-rule" in run_git(root, "diff", "--cached").stdout


def test_doctor_preprocess_preserves_unstaged_hunks_on_repaired_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    gitignore.write_text("staged-rule\n")
    run_git(root, "add", ".gitignore")
    gitignore.write_text("staged-rule\nunstaged-rule\n")
    monkeypatch.chdir(root)

    run_doctor(root)

    cached_diff = run_git(root, "diff", "--cached").stdout
    unstaged_diff = run_git(root, "diff").stdout
    assert "staged-rule" in cached_diff
    assert "unstaged-rule" not in cached_diff
    assert "unstaged-rule" in unstaged_diff
    assert gitignore.read_text() == "staged-rule\nunstaged-rule\n\n/.cmoc/local/\n"


def test_doctor_preprocess_preserves_preexisting_staged_rename(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    old_path = root / "old.txt"
    new_path = root / "new.txt"
    old_path.write_text("same content\n")
    run_git(root, "add", "old.txt")
    run_git(root, "commit", "-m", "add old file")
    old_path.rename(new_path)
    run_git(root, "add", "-A", "old.txt", "new.txt")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert run_git(root, "diff", "--cached", "--name-status").stdout.splitlines() == [
        "R100\told.txt\tnew.txt"
    ]
    assert run_git(root, "diff", "--name-status").stdout.strip() == ""
