"""`cmoc oracle investigation` の CLI 起動条件を検証する。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _git_support import make_repo

import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.investigation as investigation_module
from basic.acp import AgentCallParameter, FileAccessMode
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各 test の前後で indexing preflight の process-local state を初期化する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def test_oracle_investigation_has_no_session_precondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """oracle investigation が session なしの main worktree でも起動できる。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    editor_path = root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / "x.md"
    editor_calls: list[tuple[Path, str]] = []

    def fake_collect_prompt_editor_input(
        target_root: Path,
        automatically_injected_instruction: str,
    ) -> tuple[Path, str]:
        """エディタ入力 call と自動注入指示を記録する。"""
        editor_calls.append((target_root, automatically_injected_instruction))
        return editor_path, "oracle の根拠を調査する"

    monkeypatch.setattr(
        investigation_module,
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    calls: list[AgentCallParameter] = []
    monkeypatch.setattr(
        investigation_module,
        "run_codex_tui",
        lambda parameter, **_kwargs: calls.append(parameter),
    )

    result = runner.invoke(
        app,
        ["oracle", "investigation"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert editor_calls[0][0] == root
    assert "oracle file は読み取り専用" in editor_calls[0][1]
    assert "realization file の読み書き禁止" in editor_calls[0][1]
    assert "oracle file の規約・規範" in editor_calls[0][1]
    assert calls[0].file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert calls[0].prompt.endswith("_cmpl.md を読んで、その指示に従って下さい")
