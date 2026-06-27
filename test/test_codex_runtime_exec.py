import subprocess
from pathlib import Path

import cmoc_runtime
import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from _support import make_repo, setup_codex_home, stub_codex_profile
from commons.runtime_codex import run_codex_exec, run_codex_tui


def _parameter(mode: FileAccessMode = FileAccessMode.READONLY) -> AgentCallParameter:
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


def test_run_codex_exec_rejects_unenforced_read_limits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)

    def fail_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("Codex subprocess must not start")

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fail_run)

    with pytest.raises(CmocError, match="読み取り制限"):
        run_codex_exec(
            _parameter(FileAccessMode.REPO_WRITE),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
        )


def test_run_codex_tui_checks_extra_read_path_before_starting_codex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)

    def fail_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("Codex subprocess must not start")

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fail_run)

    with pytest.raises(CmocError, match="保護領域"):
        run_codex_tui(
            _parameter(FileAccessMode.REPO_WRITE),
            root=root,
            extra_read_paths=[root / "memo" / "prompt_cmpl.md"],
            config=CmocConfig(),
        )


@pytest.mark.parametrize("runner", ["exec", "tui"])
def test_codex_runtime_reports_missing_codex_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, runner: str
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    real_run = subprocess.run

    def fake_run(args: list[str], *pos: object, **kwargs: object) -> object:
        if args[:1] == ["codex"]:
            raise FileNotFoundError("codex")
        return real_run(args, *pos, **kwargs)

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fake_run)

    with pytest.raises(CmocError, match="Codex CLI が見つかりません"):
        if runner == "exec":
            run_codex_exec(
                _parameter(),
                root=root,
                capacity_initial_sleep_sec=0,
                config=CmocConfig(),
            )
        else:
            run_codex_tui(_parameter(), root=root, config=CmocConfig())
