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
