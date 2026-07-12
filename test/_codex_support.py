import tomllib
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from commons.runtime_git import is_untracked_git_ignored
# <work-root>/oracle/doc/app_spec/codex_exec_rule.md


def setup_codex_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Prepare a minimal authenticated Codex home for fake CLI execution."""
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    return codex_home


def stub_managed_ollama_preflight(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip managed Ollama setup while testing fake Codex subprocess argv."""
    import commons.runtime_doctor as doctor_module

    # <work-root>/oracle/doc/dev_rule/test_rule.md
    # Fake Codex tests verify cmoc's argv construction, not the shared service.
    monkeypatch.setattr(
        doctor_module,
        "ensure_ollama_serves_local_slm",
        lambda *_args, **_kwargs: None,
    )


def codex_parameter(mode: FileAccessMode = FileAccessMode.READONLY) -> AgentCallParameter:
    """Build the small default Codex parameter used by runtime wrapper tests."""
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


def codex_arg_value(args: list[str], flag: str) -> str | None:
    """Return the value following a single-value Codex CLI flag."""
    return args[args.index(flag) + 1] if flag in args else None


def codex_override_config(args: list[str]) -> dict[str, object]:
    """Merge repeated Codex `--config key=value` arguments for assertions."""
    result: dict[str, object] = {}

    def merge(target: dict[str, object], source: dict[str, object]) -> None:
        for key, value in source.items():
            current = target.get(key)
            if isinstance(current, dict) and isinstance(value, dict):
                merge(current, value)
            else:
                target[key] = value

    for index, arg in enumerate(args):
        if arg == "--config":
            merge(result, tomllib.loads(args[index + 1]))
    return result


# <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
def _override_writable_roots(args: list[str]) -> set[str]:
    """Extract sandbox roots that the Codex override allows tests to write."""
    parsed = codex_override_config(args)
    return set(parsed.get("sandbox_workspace_write", {}).get("writable_roots", []))


def _override_permission_filesystem(args: list[str]) -> dict[str, str]:
    """Extract the explicit permission filesystem map from Codex overrides."""
    parsed = codex_override_config(args)
    return parsed.get("permissions", {}).get("cmoc", {}).get("filesystem", {})


def _override_permission_roots(args: list[str], access: str) -> set[str]:
    """Return explicit permission roots matching the requested access mode."""
    return {
        path
        for path, actual_access in _override_permission_filesystem(args).items()
        if actual_access == access
    }


def _standard_realization_override_roots(root: Path) -> set[str]:
    """Return tracked standard realization paths allowed by the test override."""
    root = root.resolve()
    candidates = [root / name for name in ("src", "test", "bin", ".gitignore")]
    if (root / "README.md").exists():
        candidates.append(root / "README.md")
    # <work-root>/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    return {
        str(path)
        for candidate in candidates
        for path in (candidate.resolve(),)
        if path.is_relative_to(root) and not is_untracked_git_ignored(root, path)
    }


def _override_write_roots(args: list[str]) -> set[str]:
    """Combine override roots that grant write access to tests."""
    return {
        *_override_writable_roots(args),
        *_override_permission_roots(args, "write"),
    }


def _most_specific_permission_access(args: list[str], path: Path) -> str | None:
    """Resolve the most specific explicit permission for a test path."""
    target = path.resolve()
    matches = [
        (Path(allowed).resolve(), access)
        for allowed, access in _override_permission_filesystem(args).items()
        if target.is_relative_to(Path(allowed).resolve())
    ]
    return max(matches, key=lambda item: len(item[0].parts))[1] if matches else None


def _assert_writable(args: list[str], path: Path) -> None:
    """Assert that a path is writable under the Codex override."""
    access = _most_specific_permission_access(args, path)
    if access is not None:
        assert access == "write"
        return
    target = path.resolve()
    assert any(
        target.is_relative_to(Path(root))
        for root in _override_write_roots(args)
    )


def _assert_not_writable(args: list[str], path: Path) -> None:
    """Assert that a path is not writable under the Codex override."""
    access = _most_specific_permission_access(args, path)
    if access is not None:
        assert access != "write"
        return
    target = path.resolve()
    assert not any(
        target.is_relative_to(Path(root))
        for root in _override_write_roots(args)
    )


def _assert_not_permission_accessible(args: list[str], path: Path) -> None:
    """Assert that a path has no explicit permission entry in the override."""
    target = path.resolve()
    assert not any(
        target.is_relative_to(Path(root))
        for root in _override_permission_filesystem(args)
    )


def stub_codex_overrides(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Use stable Codex override argv in tests that target subprocess control."""
    import commons.runtime_codex_exec as exec_module
    import commons.runtime_codex_tui as tui_module

    override_args = [
        "--model",
        "fake",
        "--config",
        'model_reasoning_effort="low"',
        "--sandbox",
        "read-only",
    ]

    def fake_prepare(*_args: object, **_kwargs: object) -> list[str]:
        return list(override_args)

    monkeypatch.setattr(exec_module, "prepare_codex_override_args", fake_prepare)
    monkeypatch.setattr(tui_module, "prepare_codex_override_args", fake_prepare)
    return override_args
