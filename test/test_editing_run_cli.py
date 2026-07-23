"""workload fork と共通 run join/abandon の統合 realization test。

この file は 16,000 文字を超えるが、editing run の session state、run worktree、
fork report、および join/abandon は同じ lifecycle fixture を共有する。分割すると、
同じ branch・state 遷移の準備と検証を複数 file で重複させるため、一続きに保つ。
"""

import json
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace

import pytest
from _cli_support import run_doctor, runner
from _codex_support import setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import current_branch, make_repo, run_git

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.investigation as investigation_module
import sub_commands.realization.apply.fork as apply_module
import sub_commands.realization.refactor.fork as refactor_module
import sub_commands.run.join as run_join_module
import sub_commands.run.lifecycle as lifecycle_module
from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_content import file_sha256
from commons.runtime_errors import CmocError
from commons.runtime_paths import timestamp
from commons.runtime_refactor import load_refactor_state
from commons.runtime_state import SessionState
from main import app
from sub_commands.run.lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    set_run_state,
    start_editing_run,
    worktree_change_paths,
)


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各 test の前後で indexing preflight の process-local state を初期化する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def _start_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, str, Path]:
    """隔離 repository で session を開始し、root・branch・state path を返す。"""
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
    """session state JSON をテスト用 dict として読み込む。"""
    return json.loads(path.read_text())


def _mark_refactor_target_no_findings(root: Path, target: str) -> None:
    """state sync が既存 target の変更を検出できる履歴を作る。"""
    path = root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    state = json.loads(path.read_text())
    state[target] = {
        "investigation_required": False,
        "last_investigation_result": "no_findings",
        "last_investigated_sha256": file_sha256(root / target),
        "last_investigated_at": timestamp(),
    }
    path.write_text(json.dumps(state, indent=2) + "\n")
    run_git(root, "add", str(path.relative_to(root)))
    run_git(root, "commit", "-m", "record refactor investigation")


def _no_index_refresh(_root: Path, *, commit: bool) -> list[Path]:
    """indexing の副作用を抑える test double を返す。"""
    return []


def test_fork_report_change_paths_exclude_deletions_and_rename_sources() -> None:
    """fork reportの変更pathは削除とrename元を含めない。"""
    assert flattened_change_paths(
        [
            GitChange("D", ("deleted.md",)),
            GitChange("R100", ("old.md", "new.md")),
            GitChange("M", ("modified.md",)),
        ]
    ) == ["modified.md", "new.md"]


def test_worktree_change_paths_keep_only_rename_destination(tmp_path: Path) -> None:
    """未commit renameの変更pathはrename後だけを返す。"""
    root = make_repo(tmp_path)
    (root / "README.md").rename(root / "renamed.md")
    run_git(root, "add", "-A")

    assert worktree_change_paths(root) == ["renamed.md"]
    assert worktree_change_paths(root, include_rename_sources=True) == [
        "README.md",
        "renamed.md",
    ]


def test_apply_rejects_rename_from_oracle_to_realization(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply agent の oracle から realization への rename を拒否する。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "oracle" / "spec.md").rename(
        context.run_worktree / "moved.md"
    )
    run_git(context.run_worktree, "add", "-A")

    with pytest.raises(CmocError):
        apply_module._validate_agent_changes(context)


@pytest.mark.parametrize(
    ("kind", "expected_sync"),
    [
        ("realization_apply", True),
        ("realization_refactor", False),
    ],
)
def test_run_join_doctor_sync_depends_on_active_run_kind(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    kind: str,
    expected_sync: bool,
) -> None:
    """run kind に応じて join 前 doctor の refactor state 同期を切り替える。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    start_editing_run(kind)
    calls: list[bool] = []
    monkeypatch.setattr(
        run_join_module,
        "run_doctor_preprocess",
        lambda _root, *, sync_refactor_entries: calls.append(sync_refactor_entries),
    )

    run_join_module._doctor_preprocess_for_join()

    assert calls == [expected_sync]


def test_refactor_change_summary_keeps_only_actual_changed_paths() -> None:
    """change summaryのpathを実際の変更対象へ制限する。"""
    assert refactor_module._render_summary(
        [
            {
                "category": "rename",
                "summary": "file renamed",
                "changed_paths": ["old.md", "new.md", "outside.md"],
            }
        ],
        ["new.md"],
    ) == ["- rename: file renamed", "  - `new.md`"]


def test_realization_apply_fork_and_run_join_use_common_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply fork と run join が共通 state を使って成果物を merge する。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    calls: list[tuple[AgentCallParameter, Path]] = []

    def fake_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """apply agent の代わりに run worktree の realization file を変更する。"""
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


def test_apply_failure_rolls_back_index_with_realization_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply 失敗時に realization 差分と生成 INDEX を同時に戻す。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    calls: list[bool] = []
    before_index: str | None = None

    def fake_apply(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """apply agent の代わりに差分と rollback 前の INDEX を作る。"""
        nonlocal before_index
        worktree = Path(str(kwargs["cwd"]))
        index_path = worktree / "INDEX.md"
        before_index = index_path.read_text() if index_path.exists() else None
        (worktree / "README.md").write_text("realized\n")
        return SimpleNamespace(returncode=0, output_json=None)

    def fake_refresh(worktree: Path, *, commit: bool) -> list[Path]:
        """INDEX 更新を記録し、要求時だけ fake commit を作る。"""
        calls.append(commit)
        (worktree / "INDEX.md").write_text("generated for realized\n")
        if commit:
            run_git(worktree, "add", "INDEX.md")
            run_git(worktree, "commit", "-m", "fake indexing")
        return [worktree / "INDEX.md"]

    def fail_commit(*_args: object, **_kwargs: object) -> None:
        """work unit commit の失敗を再現する。"""
        raise RuntimeError("commit failed")

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    monkeypatch.setattr(apply_module, "refresh_indexes", fake_refresh)
    monkeypatch.setattr(apply_module, "commit_work_unit", fail_commit)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert calls == [False]
    state = _state(state_path)
    assert state["run"]["state"] == "error"
    parts = state["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert (worktree / "README.md").read_text() == "# repo\n"
    index_path = worktree / "INDEX.md"
    assert (index_path.read_text() if index_path.exists() else None) == before_index


def test_apply_start_failure_after_run_publish_is_reported(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run state 公開後の初期化失敗でも apply fork report を残す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md。
    """

    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fail_process_tracking(*_args: object, **_kwargs: object) -> None:
        """process tracking 初期化の失敗を再現する。"""
        raise RuntimeError("process tracking setup failed")

    monkeypatch.setattr(
        lifecycle_module,
        "write_run_process_id",
        fail_process_tracking,
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    reports = list(
        (
            root / ".cmoc" / "gu" / "ar" / "report" / "realization" / "apply" / "fork"
        ).glob("*.md")
    )
    assert len(reports) == 1
    assert f"- fork report: `{reports[0]}" in result.output


def test_run_join_allows_oracle_change_on_session_branch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session branch の oracle change を run join が保持する。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    _mark_refactor_target_no_findings(root, "oracle/spec.md")
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    (root / "oracle" / "spec.md").write_text("session oracle change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "session oracle change")
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"
    assert (root / "oracle" / "spec.md").read_text() == "session oracle change\n"


def test_run_join_from_run_worktree_allows_doctor_state_sync(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run worktree からの join でも doctor state 同期を許可する。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    _mark_refactor_target_no_findings(root, "README.md")
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.chdir(context.run_worktree)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"


def test_run_join_force_resolve_reverts_only_run_unexpected_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """force-resolve が run branch の想定外 path だけを戻すことを確認する。"""
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
    """post-join 同期失敗時に merge と state 更新を rollback する。"""
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
    assert _state(state_path)["session"]["last_joined_apply_fork_commit"] is None
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()

    monkeypatch.setattr(run_join_module, "sync_refactor_state", lambda _root: None)
    joined = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert joined.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"


def test_oracle_investigation_has_no_session_precondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """oracle investigation が session なしの main worktree でも起動できる。"""
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
    """refactor fork が全 target を調査して永続 cycle を完了する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    reviewed: list[str] = []
    summary_calls = 0

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """refactor agent と change-summary agent の deterministic response を返す。"""
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
    assert "- completion_reason: `natural_completion`" in result.output
    assert "- unresolved targets: `0`" in result.output


def test_refactor_interrupt_after_run_publish_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run 公開直後の中断を joinable state として report する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_start = refactor_module.start_editing_run

    def interrupt_after_start(kind: str) -> EditingRunContext:
        """run を作成した直後に利用者中断を送出する。"""
        original_start(kind)
        raise KeyboardInterrupt()

    monkeypatch.setattr(refactor_module, "start_editing_run", interrupt_after_start)

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
    report = Path(report_line.removeprefix("- fork report: ").strip("`"))
    assert 'completion_reason: "user_interruption"' in report.read_text()


def test_refactor_start_failure_after_run_publish_is_reported(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run 公開後の初期化失敗を error report として保存する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_start = refactor_module.start_editing_run

    def fail_after_start(kind: str) -> EditingRunContext:
        """run 公開直後に通常例外を送出する。"""
        original_start(kind)
        raise RuntimeError("start failed after publish")

    monkeypatch.setattr(refactor_module, "start_editing_run", fail_after_start)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: ").strip("`"))
    assert 'completion_reason: "error"' in report.read_text()


def test_refactor_fork_defers_unresolved_target_and_completes_remaining_targets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """unresolved target を保留し、残りの target を処理して cycle を完了する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    reviewed: list[str] = []
    summary_calls = 0
    call_log = (tmp_path / "unresolved_call.json").resolve()
    call_log.write_text("{}\n")

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """unresolved target を返し、他の target は処理済みとして返す。"""
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
        target = purpose.removeprefix("realization refactor: ")
        reviewed.append(target)
        if target == "README.md":
            return SimpleNamespace(
                returncode=0,
                call_log_path=call_log,
                output_json={
                    "findings": [
                        {
                            "title": "README unresolved finding",
                            "resolution": {
                                "status": "unresolved",
                                "summary": "人間の判断が必要",
                            },
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
    refactor_state = load_refactor_state(worktree)
    assert reviewed == sorted(refactor_state)
    assert reviewed.count("README.md") == 1
    assert reviewed.index("oracle/spec.md") > reviewed.index("README.md")
    assert {
        path
        for path, entry in refactor_state.items()
        if entry["investigation_required"]
    } == {"README.md"}
    assert refactor_state["README.md"]["last_investigation_result"] == "findings"
    assert summary_calls == 1
    assert "- completion_reason: `completed_with_unresolved`" in result.output
    assert "- unresolved targets: `1`" in result.output
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
    report_text = report.read_text()
    assert 'completion_reason: "completed_with_unresolved"' in report_text
    assert f"- processed targets: {len(refactor_state)}" in report_text
    assert "- uninvestigated targets: 0" in report_text
    assert "- count: 1" in report_text
    assert "`README.md`" in report_text
    assert "README unresolved finding" in report_text
    assert "resolution.summary: 人間の判断が必要" in report_text
    assert f"Codex call log: `{call_log}`" in report_text


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
    """current refactor unit の中断時に差分を戻して joinable にする。"""
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
    assert 'completion_reason: "user_interruption"' in report.read_text()
    assert "- completion_reason: `user_interruption`" in result.output
    assert "- unresolved targets: `0`" in result.output


def test_refactor_interrupt_stops_tracked_codex_children_before_rollback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """中断時に追跡中 Codex child を停止してから rollback する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    child = SimpleNamespace(process_id=123, start_time=456, process_group_id=123)
    tracked = SimpleNamespace(child_processes=(child,))
    stopped: list[object] = []
    monkeypatch.setattr(
        refactor_module,
        "read_run_process_id",
        lambda *_args: tracked,
    )
    monkeypatch.setattr(
        refactor_module,
        "stop_child_process_group",
        lambda process: stopped.append(process),
    )
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
    assert stopped == [child]
    assert _state(state_path)["run"]["state"] == "joinable"


def test_refactor_interrupt_cleanup_failure_sets_error_and_reports(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """中断時 cleanup 失敗を error state と report に反映する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )
    monkeypatch.setattr(
        refactor_module,
        "rollback_work_unit",
        lambda _worktree: (_ for _ in ()).throw(RuntimeError("rollback failed")),
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
    report_text = report.read_text()
    assert 'completion_reason: "error"' in report_text
    assert "rollback failed" in report_text


def test_refactor_interrupt_during_completion_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """completion 中の中断を joinable state と user interruption report にする。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "_initialize_cycle", lambda _context: None)
    monkeypatch.setattr(
        refactor_module,
        "select_refactor_target",
        lambda _state, _excluded: None,
    )
    monkeypatch.setattr(
        refactor_module,
        "_completion_reason",
        lambda _root, _unresolved: "natural_completion",
    )
    monkeypatch.setattr(
        refactor_module,
        "_completion_change_summary",
        lambda _context: None,
    )
    original_set_run_state = refactor_module.set_run_state
    interrupted = False

    def interrupt_once(
        context: EditingRunContext,
        run_state: str,
    ) -> SessionState:
        """最初の state 公開だけを中断し、再試行では本来の処理へ戻す。"""
        nonlocal interrupted
        if not interrupted:
            interrupted = True
            raise KeyboardInterrupt()
        return original_set_run_state(context, run_state)

    monkeypatch.setattr(refactor_module, "set_run_state", interrupt_once)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    assert "- completion_reason: `user_interruption`" in result.output
