import tomllib
from dataclasses import replace
from pathlib import Path

import pytest

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort

# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md


class FakeCodexResult:
    """apply fork test 用の最小 Structured Codex result double。"""

    def __init__(self, output_json: object | None = None) -> None:
        """structured outputの検証対象を初期化する。"""
        self.output_json = output_json


def setup_codex_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """fake CLI 実行用の最小 authenticated Codex home を準備する。"""
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    return codex_home


def stub_managed_ollama_preflight(monkeypatch: pytest.MonkeyPatch) -> None:
    """fake Codex subprocess argv のテスト中は managed Ollama setup を省略する。"""
    import commons.runtime_doctor as doctor_module

    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # fake Codex test は cmoc の argv construction を検証し、共有 service は検証しない。
    monkeypatch.setattr(
        doctor_module,
        "ensure_ollama_serves_local_slm",
        lambda *_args, **_kwargs: None,
    )


def codex_parameter(
    mode: FileAccessMode = FileAccessMode.READONLY, *, cwd: Path | None = None
) -> AgentCallParameter:
    """runtime wrapper test で使う小さな既定 Codex parameter を作る。"""
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )
    if cwd is None:
        return parameter
    # {{work-root}}/oracle/src/oracle/acp_builder/basic.py
    return replace(parameter, cwd=cwd)


def codex_arg_value(args: list[str], flag: str) -> str | None:
    """単一値 Codex CLI flag の直後にある value を返す。"""
    return args[args.index(flag) + 1] if flag in args else None


def codex_override_config(args: list[str]) -> dict[str, object]:
    """assertion 用に繰り返された Codex `--config key=value` argument を merge する。"""
    result: dict[str, object] = {}

    def merge(target: dict[str, object], source: dict[str, object]) -> None:
        """nested dictを再帰的にmergeする。"""
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
    """subprocess control を対象にする test で安定した Codex override argv を使う。"""
    import commons.runtime_codex_exec as exec_module
    import commons.runtime_codex_tui as tui_module

    override_args = [
        "--ask-for-approval",
        "on-request",
        "--model",
        "fake",
        "--config",
        'approvals_reviewer="auto_review"',
        "--config",
        'model_reasoning_effort="low"',
        "--sandbox",
        "read-only",
    ]

    def fake_prepare(*_args: object, **_kwargs: object) -> list[str]:
        """Codex overrideを固定値で返す。"""
        return list(override_args)

    monkeypatch.setattr(exec_module, "prepare_codex_override_args", fake_prepare)
    monkeypatch.setattr(tui_module, "prepare_codex_override_args", fake_prepare)
    return override_args
