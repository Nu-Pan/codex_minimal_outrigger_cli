"""workload fork と共通 run join/abandon の統合 realization test。"""

import json
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace

import pytest
from _cli_support import runner
from _codex_support import setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import current_branch, make_repo, run_git
from _ollama_support import run_doctor

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.investigation as investigation_module
import sub_commands.realization.apply.fork as apply_module
import sub_commands.realization.refactor.fork as refactor_module
import sub_commands.run.join as run_join_module
from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_refactor import load_refactor_state
from main import app
from sub_commands.run.lifecycle import (
    commit_work_unit,
    set_run_state,
    start_editing_run,
)


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def _start_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, str, Path]:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert result.exit_code == 0
    branch = current_branch(root)
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    return root, branch, state_path


def _state(path: Path) -> dict:
    return json.loads(path.read_text())


def _no_index_refresh(_root: Path, *, commit: bool) -> list[Path]:
    return []


def test_realization_apply_fork_and_run_join_use_common_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    calls: list[tuple[AgentCallParameter, Path]] = []

    def fake_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        cwd = Path(str(kwargs["cwd"]))
        calls.append((parameter, cwd))
        (cwd / "README.md").write_text("# repo\n\nrealized\n")
        return SimpleNamespace(returncode=0, output_json=None)

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)

    fork = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert fork.exit_code == 0
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    assert state["run"]["kind"] == "realization_apply"
    run_branch = state["run"]["branch"]
    run_fork_commit = state["run"]["fork_commit"]
    assert isinstance(run_branch, str) and run_branch.startswith("cmoc/run/")
    assert calls[0][0].file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert calls[0][1] != root
    assert (root / "README.md").read_text() == "# repo\n"

    joined = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert joined.exit_code == 0
    state = _state(state_path)
    assert state["run"] == {
        "state": "ready",
        "kind": None,
        "branch": None,
        "fork_commit": None,
    }
    assert state["session"]["last_joined_apply_fork_commit"] == run_fork_commit
    assert (root / "README.md").read_text() == "# repo\n\nrealized\n"
    assert run_git(root, "branch", "--list", run_branch).stdout == ""
    assert f"- run_branch: `{run_branch}`" in joined.output
    assert "cmoc run join" in joined.output
    assert current_branch(root) == session_branch


def test_run_join_force_resolve_reverts_only_run_unexpected_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("allowed\n")
    (context.run_worktree / "oracle" / "unexpected.md").write_text("unexpected\n")
    commit_work_unit(context.run_worktree, "mixed run changes")
    set_run_state(context, "joinable")
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)

    rejected = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert rejected.exit_code == 1
    assert "run branch に想定外差分があります" in rejected.output
    assert _state(state_path)["run"]["state"] == "joinable"

    joined = runner.invoke(
        app,
        ["run", "join", "--force-resolve"],
        catch_exceptions=False,
    )

    assert joined.exit_code == 0
    assert (root / "README.md").read_text() == "allowed\n"
    assert not (root / "oracle" / "unexpected.md").exists()
    assert (
        "--force-resolve reverted unexpected run paths"
        in Path(
            [
                line.removeprefix("- report: `").removesuffix("`")
                for line in joined.output.splitlines()
                if line.startswith("- report: `")
            ][0]
        ).read_text()
    )


def test_run_join_rolls_back_merge_when_post_join_sync_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    session_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.setattr(
        run_join_module,
        "sync_refactor_state",
        lambda _root: (_ for _ in ()).throw(RuntimeError("sync failed")),
    )

    failed = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert failed.exit_code == 1
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == session_head
    assert (root / "README.md").read_text() == "# repo\n"
    assert _state(state_path)["run"]["state"] == "error"
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()

    monkeypatch.setattr(run_join_module, "sync_refactor_state", lambda _root: None)
    joined = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert joined.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"


def test_oracle_investigation_has_no_session_precondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    editor_path = root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / "x.md"
    monkeypatch.setattr(
        investigation_module,
        "collect_prompt_editor_input",
        lambda *_args: (editor_path, "oracle の根拠を調査する"),
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
    assert calls[0].file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert calls[0].prompt.endswith("_cmpl.md を読んで、その指示に従って下さい")


def test_refactor_fork_completes_persistent_full_cycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    reviewed: list[str] = []
    summary_calls = 0

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        nonlocal summary_calls
        purpose = str(kwargs["purpose"])
        if purpose == "realization refactor change summary":
            summary_calls += 1
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "changes": [
                        {
                            "category": "state",
                            "summary": "調査履歴を更新",
                            "changed_paths": [
                                ".cmoc/gt/ar/realization/refactor/state.json"
                            ],
                        }
                    ]
                },
            )
        reviewed.append(purpose.removeprefix("realization refactor: "))
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    parts = state["run"]["branch"].split("/")
    worktree = (
        Path(state_path).parents[4] / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    )
    refactor_state = load_refactor_state(worktree)
    assert reviewed == sorted(refactor_state)
    assert all(not entry["investigation_required"] for entry in refactor_state.values())
    assert all(
        entry["last_investigation_result"] == "no_findings"
        for entry in refactor_state.values()
    )
    assert summary_calls == 1
    assert "natural_completion" in result.output or "fork report" in result.output


def test_refactor_fork_refreshes_changed_file_index_during_process_tracking(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor の file 変更後も tracked INDEX subprocess を安全に実行する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            'output.write_text(\'{"summary": ["summary"], "read_this_when": ["read"], "do_not_read_this_when": ["skip"]}\')',
            'print(\'{"type":"turn.completed"}\')',
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    readme_reviews = 0

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """README の初回調査だけ file を修正し、他は固定応答を返す。"""
        nonlocal readme_reviews
        purpose = str(kwargs["purpose"])
        if purpose == "realization refactor change summary":
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "changes": [
                        {
                            "category": "realization",
                            "summary": "README と INDEX entry を更新",
                            "changed_paths": [
                                ".cmoc/gt/ar/realization/refactor/state.json",
                                "INDEX.md",
                                "README.md",
                            ],
                        }
                    ]
                },
            )
        if purpose == "realization refactor: README.md":
            readme_reviews += 1
            if readme_reviews == 1:
                worktree = Path(str(kwargs["cwd"]))
                (worktree / "README.md").write_text("# repo\n\nfixed\n")
                return SimpleNamespace(
                    returncode=0,
                    output_json={
                        "findings": [
                            {
                                "title": "README finding",
                                "resolution": {"status": "fixed"},
                            }
                        ]
                    },
                )
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    parts = state["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    readme = worktree / "README.md"
    assert readme.read_text() == "# repo\n\nfixed\n"
    readme_entry = indexing_module.parse_index_entries(worktree / "INDEX.md")[
        "README.md"
    ]
    assert readme_entry["hash"] == indexing_module.index_target_hash(worktree, readme)
    readme_commit = run_git(
        worktree, "log", "-1", "--format=%H", "--", "README.md"
    ).stdout.strip()
    committed_paths = set(
        run_git(worktree, "show", "--format=", "--name-only", readme_commit)
        .stdout.strip()
        .splitlines()
    )
    assert {
        ".cmoc/gt/ar/realization/refactor/state.json",
        "INDEX.md",
        "README.md",
    } <= committed_paths
    assert readme_reviews == 2


def test_refactor_interrupt_rolls_back_current_unit_and_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
    assert 'completion_reason: "interrupted"' in report.read_text()
