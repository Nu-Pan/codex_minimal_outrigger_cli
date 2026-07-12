import tomllib
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
# <work-root>/oracle/doc/app_spec/codex_exec_rule.md


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
    parsed = codex_override_config(args)
    return set(parsed.get("sandbox_workspace_write", {}).get("writable_roots", []))


def _override_permission_filesystem(args: list[str]) -> dict[str, str]:
    parsed = codex_override_config(args)
    return parsed.get("permissions", {}).get("cmoc", {}).get("filesystem", {})


def _override_permission_roots(args: list[str], access: str) -> set[str]:
    return {
        path
        for path, actual_access in _override_permission_filesystem(args).items()
        if actual_access == access
    }


def _standard_realization_override_roots(root: Path) -> set[str]:
    roots: set[str] = set()
    for name in ("src", "test", "bin"):
        roots.add(str((root / name).resolve()))
    roots.add(str((root / ".gitignore").resolve()))
    if (root / "README.md").exists():
        roots.add(str((root / "README.md").resolve()))
    return roots


def _override_write_roots(args: list[str]) -> set[str]:
    return {
        *_override_writable_roots(args),
        *_override_permission_roots(args, "write"),
    }


def _most_specific_permission_access(args: list[str], path: Path) -> str | None:
    target = path.resolve()
    matches = [
        (Path(allowed).resolve(), access)
        for allowed, access in _override_permission_filesystem(args).items()
        if target.is_relative_to(Path(allowed).resolve())
    ]
    return max(matches, key=lambda item: len(item[0].parts))[1] if matches else None


def _assert_writable(args: list[str], path: Path) -> None:
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
