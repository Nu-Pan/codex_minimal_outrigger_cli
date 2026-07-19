"""`cmoc oracle edit` の main-worktree TUI 制御を検証する。"""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import runner
from _git_support import current_branch, make_repo, run_git
from _ollama_support import run_doctor

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, CommandResult
from commons.runtime_state import (
    RunPart,
    SessionPart,
    SessionState,
    state_path,
    write_state,
)
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def _activate_session(
    root: Path,
    *,
    session_state: str = "active",
    run: RunPart | None = None,
) -> tuple[str, Path]:
    home_branch = current_branch(root)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    session_id = "oracle-edit-test"
    session_branch = f"cmoc/session/{session_id}"
    run_git(root, "checkout", "-b", session_branch)
    path = state_path(root, session_id)
    write_state(
        path,
        SessionState(
            SessionPart(session_state, home_branch, fork_commit, None),
            run or RunPart(),
        ),
    )
    return session_branch, path


def _prepared_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)
    return root


@pytest.mark.parametrize("tui_fails", [False, True], ids=["success", "failure"])
def test_oracle_edit_runs_tui_without_using_run_lifecycle_and_preserves_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tui_fails: bool,
) -> None:
    root = _prepared_repo(tmp_path, monkeypatch)
    active_run = RunPart(
        "running",
        "realization_apply",
        "cmoc/run/oracle-edit-test/active-run",
        "abc",
    )
    _session_branch, session_state_path = _activate_session(root, run=active_run)
    state_before = json.loads(session_state_path.read_text())
    editor_path = (
        root
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "editor_input"
        / "2026-07-20_00-00-00_000000000_orig.md"
    )
    editor_path.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(
        oracle_edit_module,
        "collect_prompt_editor_input",
        lambda *_args: (editor_path, "oracle spec を更新する"),
    )
    events: list[str] = []
    calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_indexing_preflight(
        update_root: Path,
        _codex_exec: object,
    ) -> None:
        assert update_root == root
        events.append("indexing")

    real_require_clean = oracle_edit_module.require_clean_worktree

    def record_clean_check(check_root: Path) -> None:
        events.append("check")
        real_require_clean(check_root)

    def fake_runtime_tui(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> CommandResult:
        events.append("tui")
        calls.append((parameter, kwargs))
        (root / "oracle" / "spec.md").write_text("# edited spec\n")
        if tui_fails:
            raise CmocError("TUI failed", [], "returncode: 7")
        return CommandResult(0, "", "")

    monkeypatch.setattr(
        indexing_module,
        "run_indexing_preflight",
        fake_indexing_preflight,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "require_clean_worktree",
        record_clean_check,
    )
    monkeypatch.setattr(
        codex_preflight_module,
        "runtime_run_codex_tui",
        fake_runtime_tui,
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == (1 if tui_fails else 0)
    assert events == ["indexing", "check", "tui"]
    assert len(calls) == 1
    parameter, kwargs = calls[0]
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.run_indexing_preflight is True
    assert parameter.cwd == root.resolve()
    assert kwargs["cwd"] == root
    assert kwargs["purpose"] == "oracle edit"
    prompt_suffix = " を読んで、その指示に従って下さい"
    assert parameter.prompt.endswith(prompt_suffix)
    complete_prompt_path = Path(parameter.prompt.removesuffix(prompt_suffix))
    complete_prompt = complete_prompt_path.read_text()
    assert "oracle spec を更新する" in complete_prompt
    assert "realization file、`INDEX.md`、`AGENTS.md` を編集していない" in (
        complete_prompt
    )
    assert (root / "oracle" / "spec.md").read_text() == "# edited spec\n"
    assert json.loads(session_state_path.read_text()) == state_before
    assert run_git(root, "status", "--short", "oracle/spec.md").stdout.strip()
    assert not (
        root / ".cmoc" / "gu" / "ar" / "report" / "oracle" / "edit" / "fork"
    ).exists()


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("linked", "main worktree"),
        ("non_session", "session branch"),
        ("inactive", "active な session"),
        ("dirty", "git 未コミット差分"),
    ],
)
def test_oracle_edit_launch_preconditions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
    message: str,
) -> None:
    root = _prepared_repo(tmp_path, monkeypatch)
    current_root = root
    if case != "non_session":
        _activate_session(
            root,
            session_state="joined" if case == "inactive" else "active",
        )
    if case == "linked":
        current_root = root / ".cmoc" / "gu" / "worktree" / "linked"
        run_git(
            root,
            "worktree",
            "add",
            "-b",
            "linked-oracle-edit-test",
            str(current_root),
            "HEAD",
        )
    elif case == "dirty":
        (root / "README.md").write_text("dirty\n")

    with pytest.raises(CmocError, match=message):
        oracle_edit_module._require_oracle_edit_launch_preconditions(
            root,
            current_root,
        )
