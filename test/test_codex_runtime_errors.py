import subprocess
from pathlib import Path

import cmoc_runtime
import pytest
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from _support import (
    codex_parameter,
    make_repo,
    setup_codex_home,
    stub_codex_profile,
)
from commons.runtime_codex import run_codex_exec, run_codex_tui


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
                codex_parameter(),
                root=root,
                capacity_initial_sleep_sec=0,
                config=CmocConfig(),
            )
        else:
            run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
