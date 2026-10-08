"""workload fork と共通 run join/abandon の統合 realization test。

この file は 16,000 文字を超えるが、editing run の session state、run worktree、
fork report、および join/abandon は同じ lifecycle fixture を共有する。分割すると、
同じ branch・state 遷移の準備と検証を複数 file で重複させるため、一続きに保つ。

通知根拠: {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
"""

import json
import os
import signal
from pathlib import Path
from types import SimpleNamespace
from typing import NoReturn

import pytest
from _cli_support import run_doctor, runner, terminal_primary_report
from _git_support import (
    RUN_BRANCH,
    RUN_ID,
    SESSION_BRANCH,
    SESSION_ID,
    current_branch,
    make_repo,
    run_git,
)

import commons.runtime_cli as runtime_cli
import commons.runtime_merge_conflict as merge_conflict_module
import commons.runtime_run as runtime_run_module
import commons.runtime_run_join as run_join_module
import commons.runtime_run_lifecycle as lifecycle_module
import commons.runtime_run_report as run_report_module
import sub_commands.realization.apply.fork as apply_module
import sub_commands.realization.refactor.fork as refactor_module
import sub_commands.run.abandon as run_abandon_module
import sub_commands.run.join as run_join_command_module
import sub_commands.run.lifecycle as legacy_lifecycle_module
from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_content import file_sha256
from commons.runtime_errors import CmocError
from commons.runtime_ids import is_common_id
from commons.runtime_logging import SubcommandLogger
from commons.runtime_paths import timestamp
from commons.runtime_primary_report import (
    ensure_primary_report,
    reset_primary_report_context,
    start_primary_report_context,
)
from commons.runtime_refactor import load_refactor_state
from commons.runtime_results import TerminalResult
from commons.runtime_run import run_process_id_path
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    set_run_state,
    start_editing_run,
    worktree_change_paths,
)
from commons.runtime_state import SessionState
from main import app

_WORK_DIRECTORIES = ("oracle/doc", "oracle/src", "oracle/test", "src", "test")


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
    state_path = root / ".cmoc" / "gu" / "session" / f"{session_id}.json"
    return root, branch, state_path


def _state(path: Path) -> dict:
    """session state JSON をテスト用 dict として読み込む。"""
    return json.loads(path.read_text())


def _mark_refactor_target_no_findings(root: Path, target: str) -> None:
    """state sync が既存 target の変更を検出できる履歴を作る。"""
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
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


def _stop_after_cycles(monkeypatch: pytest.MonkeyPatch, cycles: int = 1) -> None:
    """指定巡数の次の開始要求でユーザー中断を発生させる。"""
    initialize = refactor_module._initialize_cycle
    started = 0

    def initialize_or_interrupt(context, **kwargs):
        nonlocal started
        if started == cycles:
            raise KeyboardInterrupt
        started += 1
        return initialize(context, **kwargs)

    monkeypatch.setattr(refactor_module, "_initialize_cycle", initialize_or_interrupt)


def test_legacy_lifecycle_shim_reexports_agent_path_validation() -> None:
    """旧 run lifecycle import path が canonical helper を再公開する。"""
    assert (
        legacy_lifecycle_module.unexpected_agent_paths
        is lifecycle_module.unexpected_agent_paths
    )
    assert "unexpected_agent_paths" in legacy_lifecycle_module.__all__


def test_fork_report_change_paths_exclude_deletions_and_rename_sources() -> None:
    """fork reportの変更pathは削除とrename元を含めない。"""
    assert flattened_change_paths(
        [
            GitChange("D", ("deleted.md",)),
            GitChange("R100", ("old.md", "new.md")),
            GitChange("M", ("modified.md",)),
        ]
    ) == ["modified.md", "new.md"]


def test_run_reports_use_execution_ids_and_keep_generated_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同一生成時刻でも report は別実行 ID で保存する。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path,
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=tmp_path,
    )
    generated_at = "2026-06-27_10-00-00_000"
    monkeypatch.setattr(run_report_module, "timestamp", lambda: generated_at)

    fork_paths = [
        run_report_module.write_fork_report(
            context,
            "realization/apply/fork",
            state_after="joinable",
            completion_reason="completed",
            changed_paths=[],
        )
        for _ in range(2)
    ]
    lifecycle_paths = [
        run_report_module.write_lifecycle_report(
            context,
            "join",
            state_after="ready",
            warnings=[],
            details={},
        )
        for _ in range(2)
    ]

    assert all(
        is_common_id(path.stem, "exec") for path in [*fork_paths, *lifecycle_paths]
    )
    assert len({path.stem for path in [*fork_paths, *lifecycle_paths]}) == 4
    assert all(
        f'generated_at: "{generated_at}"' in path.read_text()
        for path in [*fork_paths, *lifecycle_paths]
    )


def test_fork_report_escapes_special_changed_paths(tmp_path: Path) -> None:
    """変更 path の Markdown code span と行構造を壊さない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path,
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=tmp_path,
    )

    report = run_report_module.write_fork_report(
        context,
        "realization/apply/fork",
        state_after="joinable",
        completion_reason="completed",
        changed_paths=["line\nbreak`|<&.md"],
    )

    assert "- <code>line&#10;break&#96;&#124;&lt;&amp;.md</code>" in report.read_text()


@pytest.mark.parametrize("occupied", ["branch", "worktree", "dangling_symlink"])
def test_new_run_target_preserves_occupied_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, occupied: str
) -> None:
    """発行 ID の保存先が占有されていたら既存資源を保って停止する。"""
    root = make_repo(tmp_path)
    session_id = "sess_000000_2026-06-27_10-00"
    run_id = "run_000000_2026-06-27_10-00"
    branch = f"cmoc/run/{session_id}/{run_id}"
    collision = root / ".cmoc" / "gu" / "worktree" / session_id / run_id
    if occupied == "branch":
        run_git(root, "branch", branch)
        protected_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    else:
        collision.parent.mkdir(parents=True)
        if occupied == "worktree":
            collision.mkdir()
            (collision / "keep.txt").write_text("protected")
        else:
            collision.symlink_to(
                tmp_path / "missing-run-worktree", target_is_directory=True
            )
    monkeypatch.setattr(lifecycle_module, "new_id", lambda _root, _prefix: run_id)

    with pytest.raises(CmocError, match="発行した run ID の保存先が既に存在します。"):
        lifecycle_module.new_run_target(root, session_id)

    if occupied == "branch":
        assert run_git(root, "rev-parse", branch).stdout.strip() == protected_commit
    elif occupied == "worktree":
        assert (collision / "keep.txt").read_text() == "protected"
    else:
        assert collision.is_symlink()


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


def test_worktree_change_paths_returns_normalized_relative_paths(
    tmp_path: Path,
) -> None:
    """変更 path を refactor schema と同じ slash 区切りで返す。"""
    root = make_repo(tmp_path)
    nested = root / "nested" / "README.md"
    nested.parent.mkdir()
    nested.write_text("nested\n")

    assert worktree_change_paths(root) == ["nested/README.md"]


def test_apply_rolls_back_unexpected_oracle_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run branch の想定外差分を commit 後に rollback する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fake_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """apply agent が oracle file を変更した状態を再現する。"""
        worktree = parameter.agent_call_cwd
        assert "cwd" not in kwargs
        (worktree / "oracle" / "unexpected.md").write_text("unexpected\n")
        return SimpleNamespace(returncode=0, output_json=None)

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    state = _state(state_path)
    assert state["run"]["state"] == "error"
    parts = state["run"]["branch"].split("/")
    run_worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert not (run_worktree / "oracle" / "unexpected.md").exists()


def test_apply_rejects_agent_commit_and_rolls_back_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply agent の commit が処理単位をすり抜けず、開始 HEAD へ戻る。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fake_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """agent が realization file を直接 commit する状態を再現する。"""
        before_agent_call = kwargs["before_agent_call"]
        assert callable(before_agent_call)
        before_agent_call()
        worktree = parameter.agent_call_cwd
        (worktree / "README.md").write_text("agent commit\n")
        run_git(worktree, "add", "README.md")
        run_git(worktree, "commit", "-m", "agent commit")
        return SimpleNamespace(returncode=0, output_json=None)

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    parts = _state(state_path)["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert (worktree / "README.md").read_text() == "# repo\n"
    assert (
        "agent commit"
        not in run_git(worktree, "log", "--format=%s").stdout.splitlines()
    )
    assert run_git(worktree, "status", "--porcelain").stdout == ""


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

    run_join_module.doctor_preprocess_for_join()

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


def test_refactor_change_summary_escapes_special_changed_paths() -> None:
    """change summary の path が Markdown の構造を壊さない。"""
    assert refactor_module._render_summary(
        [
            {
                "category": "rename",
                "summary": "file renamed",
                "changed_paths": ["line\nbreak`|<&.md"],
            }
        ],
        ["line\nbreak`|<&.md"],
    ) == [
        "- rename: file renamed",
        "  - <code>line&#10;break&#96;&#124;&lt;&amp;.md</code>",
    ]
    assert refactor_module._render_summary(
        None,
        ["line\nbreak`|<&.md"],
    ) == ["- committed path: <code>line&#10;break&#96;&#124;&lt;&amp;.md</code>"]
    assert refactor_module._render_unresolved_findings(
        {
            "line\nbreak`|<&.md": [
                (
                    "title",
                    "reason",
                    Path("log`|<&.md"),
                )
            ]
        }
    ) == [
        "- <code>line&#10;break&#96;&#124;&lt;&amp;.md</code>: title",
        "  - resolution.summary: reason",
        "  - Codex call log: <code>log&#96;&#124;&lt;&amp;.md</code>",
    ]


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
        worktree = parameter.agent_call_cwd
        assert "cwd" not in kwargs
        assert all((worktree / relative).is_dir() for relative in _WORK_DIRECTORIES)
        calls.append((parameter, worktree))
        (worktree / "README.md").write_text("# repo\n\nrealized\n")
        return SimpleNamespace(returncode=0, output_json=None)

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    joined_process_stops: list[tuple[Path, str]] = []
    monkeypatch.setattr(
        run_join_module,
        "stop_tracked_codex_children",
        lambda repo, session_id: joined_process_stops.append((repo, session_id)),
    )
    monkeypatch.setattr(
        run_join_command_module,
        "stop_tracked_codex_children",
        lambda repo, session_id: joined_process_stops.append((repo, session_id)),
    )

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
    assert joined_process_stops == [
        (root, session_branch.removeprefix("cmoc/session/")),
        (root, session_branch.removeprefix("cmoc/session/")),
    ]
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
    assert (
        "- post_join_hook: `session.last_joined_apply_fork_commit updated`"
        in joined.output
    )
    report_path = terminal_primary_report(joined)
    report_text = report_path.read_text()
    assert "session.last_joined_apply_fork_commit=" not in report_text
    assert 'command: "cmoc run join"' in report_text
    assert 'terminal_classification: "natural_completion"' in report_text
    assert "exit_code: 0" in report_text
    assert "## Execution stages" in report_text
    assert "## Related logs" in report_text
    assert "診断用サブコマンドログ" in report_text
    assert current_branch(root) == session_branch


@pytest.mark.parametrize("run_state", ["joinable", "error"])
@pytest.mark.parametrize("has_run_change", [False, True], ids=["no-op", "merge"])
@pytest.mark.parametrize("has_previous_apply", [False, True], ids=["initial", "later"])
def test_apply_join_updates_diff_base_only_for_joinable_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    run_state: str,
    has_run_change: bool,
    has_previous_apply: bool,
) -> None:
    """join 開始時の state に応じた比較始点を、次回 apply へ渡す。"""
    # realization_apply.md の「join 後 hook」を state、report、次回 prompt で検査する。
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    state = _state(state_path)
    session_fork_commit = state["session"]["session_fork_commit"]
    previous_base = session_fork_commit if has_previous_apply else None
    state["session"]["last_joined_apply_fork_commit"] = previous_base
    state_path.write_text(json.dumps(state))
    (root / "oracle" / "spec.md").write_text("pending oracle change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "pending oracle change")
    context = start_editing_run("realization_apply")
    if has_run_change:
        (context.run_worktree / "README.md").write_text("realized\n")
        commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, run_state)

    joined = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert joined.exit_code == 0, joined.output
    expected_base = (
        context.run_fork_commit if run_state == "joinable" else previous_base
    )
    state = _state(state_path)
    assert state["session"]["last_joined_apply_fork_commit"] == expected_base
    assert state["run"]["state"] == "ready"
    assert (root / "README.md").read_text() == (
        "realized\n" if has_run_change else "# repo\n"
    )
    report = terminal_primary_report(joined).read_text()
    hook_action = "updated" if run_state == "joinable" else "preserved"
    for output in (joined.output, report):
        assert f"session.last_joined_apply_fork_commit {hook_action}" in output
        if run_state == "error":
            assert "session.last_joined_apply_fork_commit updated" not in output
    assert ("run_join_commit: null" in report) is (not has_run_change)

    # 成果物の取り込み後も、未追従の oracle change を次回の比較範囲に残す。
    prompts: list[str] = []

    def capture_apply(
        parameter: AgentCallParameter, **_kwargs: object
    ) -> SimpleNamespace:
        """次回 apply が受け取る commit 範囲を記録する。"""
        prompts.append(parameter.prompt)
        return SimpleNamespace(returncode=0, output_json=None)

    monkeypatch.setattr(apply_module, "run_codex_exec", capture_apply)
    fork = runner.invoke(app, ["realization", "apply", "fork"], catch_exceptions=False)

    assert fork.exit_code == 0, fork.output
    assert len(prompts) == 1
    diff_base = expected_base if expected_base is not None else session_fork_commit
    next_fork_commit = _state(state_path)["run"]["fork_commit"]
    assert f"- 始点: `{diff_base}`" in prompts[0]
    assert f"- 終点: `{next_fork_commit}`" in prompts[0]
    oracle_diff = run_git(root, "diff", diff_base, next_fork_commit, "--", "oracle")
    assert bool(oracle_diff.stdout) is (run_state == "error")


def test_run_join_reports_joinable_child_stop_warnings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """joinable run の descendant 停止 warning を join report に残す。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    monkeypatch.setattr(
        run_join_module,
        "stop_tracked_codex_children",
        lambda *_args: ["run child process already stopped: 789"],
    )

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    report_path = terminal_primary_report(result)
    assert "run child process already stopped: 789" in report_path.read_text()


def test_apply_builder_uses_call_scoped_run_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """process cwd を変えずに parameter と prompt が run worktree を共有する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    # 入力差分の本文・path 一覧が prompt に混ざらないことも確認する。
    (root / "oracle" / "reference_only.md").write_text("oracle payload\n" * 1000)
    run_git(root, "add", "oracle/reference_only.md")
    run_git(root, "commit", "-m", "oracle change")
    expected_base = _state(state_path)["session"]["session_fork_commit"]
    original_builder = apply_module.build_realization_apply_fork_launch_exec_parameter
    observed: list[tuple[Path, Path, Path, str]] = []

    def capture_builder(
        diff_base_commit: str,
        run_fork_commit: str,
        run_worktree: Path,
    ) -> AgentCallParameter:
        """builder 構築時の process cwd、agent call cwd、prompt を記録する。"""
        parameter = original_builder(
            diff_base_commit,
            run_fork_commit,
            run_worktree,
        )
        observed.append(
            (
                Path.cwd().resolve(),
                run_worktree.resolve(),
                parameter.agent_call_cwd,
                parameter.prompt,
            )
        )
        return parameter

    monkeypatch.setattr(
        apply_module,
        "build_realization_apply_fork_launch_exec_parameter",
        capture_builder,
    )
    monkeypatch.setattr(
        apply_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, output_json=None),
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    assert len(observed) == 1
    cmoc_process_cwd, run_worktree, agent_call_cwd, prompt = observed[0]
    assert cmoc_process_cwd == root
    assert agent_call_cwd == run_worktree
    assert f"- {{{{work-root}}}} = {run_worktree}" in prompt
    expected_end = _state(state_path)["run"]["fork_commit"]
    assert f"- 始点: `{expected_base}`" in prompt
    assert f"- 終点: `{expected_end}`" in prompt
    assert "reference_only.md" not in prompt
    assert "oracle payload" not in prompt


def test_run_abandon_accepts_already_removed_run_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """既に削除された run worktree を warning 扱いで cleanup できる。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")
    process_stops: list[tuple[Path, str]] = []
    monkeypatch.setattr(
        run_abandon_module,
        "stop_tracked_codex_children",
        lambda repo, session_id: process_stops.append((repo, session_id)),
    )
    run_git(root, "worktree", "remove", "--force", str(context.run_worktree))

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert process_stops == [(root, context.session_id)]
    assert _state(state_path)["run"] == {
        "state": "ready",
        "kind": None,
        "branch": None,
        "fork_commit": None,
    }
    assert run_git(root, "branch", "--list", context.run_branch).stdout == ""
    reports = list((root / ".cmoc" / "gu" / "report" / "run" / "abandon").glob("*.md"))
    assert len(reports) == 1
    assert "run worktree was already absent" in reports[0].read_text()


def test_run_abandon_prunes_missing_registered_run_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """実体だけが欠損した run worktree の Git 登録も cleanup する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")
    moved_worktree = tmp_path / "moved-run-worktree"
    context.run_worktree.rename(moved_worktree)

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert moved_worktree.exists()
    assert _state(state_path)["run"] == {
        "state": "ready",
        "kind": None,
        "branch": None,
        "fork_commit": None,
    }
    assert run_git(root, "branch", "--list", context.run_branch).stdout == ""


def test_run_abandon_requires_process_stop_confirmation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """running run の process tracking がない場合は cleanup を開始しない。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    run_process_id_path(root, context.session_id).unlink()

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "process 停止を確認できません" in result.output
    assert _state(state_path)["run"]["state"] == "running"
    assert context.run_worktree.exists()
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()


def test_run_abandon_stops_tracked_process_for_error_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """error run cleanup が残存 process を停止してから資源を破棄する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "error")
    tracked = SimpleNamespace(process_id=123, start_time=456, child_processes=())
    events: list[str] = []

    monkeypatch.setattr(
        runtime_run_module,
        "read_run_process_id",
        lambda *_args: tracked,
    )
    monkeypatch.setattr(
        runtime_run_module,
        "stop_run_process",
        lambda *_args, **_kwargs: events.append("stop") or None,
    )

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert events == ["stop"]
    assert _state(state_path)["run"]["state"] == "ready"
    assert not context.run_worktree.exists()
    assert run_git(root, "branch", "--list", context.run_branch).stdout == ""


@pytest.mark.parametrize("run_state", ["joinable", "error"])
def test_run_abandon_rejects_unreadable_process_tracking(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    run_state: str,
) -> None:
    """破損した process tracking を無視して run 資源を削除しない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, run_state)
    tracking_path = run_process_id_path(root, context.session_id)
    tracking_path.write_bytes(b"\xff")

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 1
    assert "process tracking を検証できません" in result.output
    assert _state(state_path)["run"]["state"] == run_state
    assert context.run_worktree.exists()
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()
    assert tracking_path.read_bytes() == b"\xff"


def test_run_abandon_reports_stale_child_stop_warning(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """joinable run の child 停止 warning を lifecycle report に残す。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")
    run_process_id_path(root, context.session_id).write_text(
        "123 456\nchild 789 1011 789\n"
    )
    monkeypatch.setattr(
        runtime_run_module,
        "stop_child_process_group",
        lambda _child: "run child process already stopped: 789",
    )

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    reports = list((root / ".cmoc" / "gu" / "report" / "run" / "abandon").glob("*.md"))
    assert len(reports) == 1
    report_text = reports[0].read_text()
    assert "run child process already stopped: 789" in report_text


def test_apply_report_fields_include_accepted_feedback_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply report が invocation 内で accepted になった raw 参照だけを含む。"""
    observations = [
        {
            "observation_id": "fbo_000000_2026-09-29_15-04",
            "path": "/repo/.cmoc/gu/feedback/observation/v1/2026/09/29/fbo_000000_2026-09-29_15-04.json",
        }
    ]
    monkeypatch.setattr(
        apply_module,
        "accepted_feedback_observations",
        lambda: observations,
    )

    token = start_primary_report_context("realization apply fork")
    try:
        fields = apply_module._apply_report_fields("base-commit")

        logger = SubcommandLogger(tmp_path, "realization apply fork")
        result = ensure_primary_report(
            tmp_path,
            "realization apply fork",
            ("cmoc", "realization", "apply", "fork"),
            "error",
            1,
            TerminalResult(),
            logger,
        )
    finally:
        reset_primary_report_context(token)

    assert fields == {
        "diff_base_commit": "base-commit",
        "feedback_observation_count": 1,
        "feedback_observations": observations,
    }
    assert result.primary_report is not None
    front_matter = result.primary_report.read_text(encoding="utf-8").split("---", 2)[1]
    assert "feedback_observation_count: 1" in front_matter
    assert f"feedback_observations: {json.dumps(observations)}" in front_matter


def test_run_abandon_rejects_dangling_worktree_link_after_removal_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """削除失敗後に残った dangling symlink を cleanup 完了と扱わない。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path / "session",
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=tmp_path / "run",
    )
    context.run_worktree.symlink_to(tmp_path / "missing", target_is_directory=True)
    monkeypatch.setattr(
        run_abandon_module,
        "remove_worktree",
        lambda *_args: SimpleNamespace(returncode=1, stderr="removal failed"),
    )

    warnings: list[str] = []
    assert not run_abandon_module._remove_run_worktree(context, warnings)
    assert warnings == ["removal failed"]


def test_run_abandon_preserves_branch_when_worktree_cleanup_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """worktree cleanup失敗時に再試行用のrun branchを保持する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")
    branch_calls: list[str] = []
    monkeypatch.setattr(
        run_abandon_module,
        "_remove_run_worktree",
        lambda _context, _warnings: False,
    )
    monkeypatch.setattr(
        run_abandon_module,
        "_remove_run_branch",
        lambda _context, _warnings: branch_calls.append("deleted") or True,
    )

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 1
    assert branch_calls == []
    assert _state(state_path)["run"]["state"] == "joinable"
    assert context.run_worktree.exists()
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()


def test_run_abandon_reports_process_stop_before_later_cleanup_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """停止済み process を、その後の cleanup 失敗 report にも残す。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")
    monkeypatch.setattr(
        run_abandon_module, "_stop_joinable_run", lambda *_args: "stopped"
    )

    def fail_worktree_cleanup(*_args: object) -> NoReturn:
        """停止後の worktree cleanup failure を再現する。"""
        raise RuntimeError("cleanup failed after process stop")

    monkeypatch.setattr(
        run_abandon_module, "_remove_run_worktree", fail_worktree_cleanup
    )

    result = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert result.exit_code == 1, result.output
    report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert 'process_stop: "stopped"' in report
    assert _state(state_path)["run"]["state"] == "joinable"
    assert context.run_worktree.exists()


def test_apply_fork_stops_tracked_codex_children_before_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply は joinable 公開前に残存 Codex child を停止する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    child = SimpleNamespace(process_id=123, start_time=456, process_group_id=123)
    tracked = SimpleNamespace(child_processes=(child,))
    stopped: list[object] = []
    monkeypatch.setattr(
        runtime_run_module,
        "read_run_process_id",
        lambda *_args: tracked,
    )
    monkeypatch.setattr(
        runtime_run_module,
        "stop_child_process_group",
        lambda process: stopped.append(process),
    )
    monkeypatch.setattr(
        apply_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, output_json=None),
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert stopped == [child]
    assert _state(state_path)["run"]["state"] == "joinable"


def test_apply_fork_reports_cleanup_warnings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply fork の cleanup warning を fork report に保存する。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(
        apply_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, output_json=None),
    )
    monkeypatch.setattr(
        apply_module,
        "stop_tracked_codex_children",
        lambda *_args: ["run child process already stopped: 789"],
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    reports = list(
        (root / ".cmoc" / "gu" / "report" / "realization" / "apply" / "fork").glob(
            "*.md"
        )
    )
    assert len(reports) == 1
    report_text = reports[0].read_text()
    assert "run child process already stopped: 789" in report_text
    assert "feedback_observation_count: 0" in report_text
    assert "feedback_observations: []" in report_text


def test_refactor_fork_stops_tracked_children_before_each_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor は cycle と各処理単位の commit 前に Codex child を停止する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    events: list[str] = []
    original_commit = refactor_module.commit_work_unit

    def record_stop(*_args: object) -> None:
        """tracked child の停止位置を記録する。"""
        events.append("stop")

    def record_commit(
        worktree: Path,
        message: str,
        **kwargs: object,
    ) -> str | None:
        """処理単位 commit の位置を記録して本来の commit を実行する。"""
        events.append("commit")
        return original_commit(worktree, message, **kwargs)

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """file review の固定 Structured Output を返す。"""
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "stop_tracked_codex_children", record_stop)
    monkeypatch.setattr(refactor_module, "commit_work_unit", record_commit)
    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert _state(state_path)["run"]["state"] == "joinable"
    commit_positions = [
        index for index, event in enumerate(events) if event == "commit"
    ]
    assert commit_positions
    assert any(index > 0 and events[index - 1] == "stop" for index in commit_positions)


def test_refactor_fork_reports_cleanup_warnings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor fork の child 停止 warning を fork report に保存する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """file review の固定 Structured Output を返す。"""
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)
    monkeypatch.setattr(
        refactor_module,
        "stop_tracked_codex_children",
        lambda *_args: ["run child process already stopped: 789"],
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert _state(state_path)["run"]["state"] == "joinable"
    reports = list(
        (root / ".cmoc" / "gu" / "report" / "realization" / "refactor" / "fork").glob(
            "*.md"
        )
    )
    assert len(reports) == 1
    assert "run child process already stopped: 789" in reports[0].read_text()


def test_refactor_fork_stops_tracked_codex_children_before_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor は joinable 公開前に残存 Codex child を停止する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    child = SimpleNamespace(process_id=123, start_time=456, process_group_id=123)
    tracked = SimpleNamespace(child_processes=(child,))
    stopped: list[object] = []
    monkeypatch.setattr(
        runtime_run_module,
        "read_run_process_id",
        lambda *_args: tracked,
    )
    monkeypatch.setattr(
        runtime_run_module,
        "stop_child_process_group",
        lambda process: stopped.append(process),
    )
    monkeypatch.setattr(
        refactor_module,
        "_initialize_cycle",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert stopped == [child]
    assert _state(state_path)["run"]["state"] == "joinable"


@pytest.mark.parametrize(
    ("replace_content", "add_unrelated_file"),
    [(False, False), (True, False), (True, True)],
)
def test_refactor_fork_moves_unresolved_target_after_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replace_content: bool,
    add_unrelated_file: bool,
) -> None:
    """rename 後も unresolved target と refactor state の path 集合を揃える。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """README の rename と unresolved finding を再現する。"""
        worktree = parameter.agent_call_cwd
        if kwargs["purpose"] == "realization refactor: README.md":
            (worktree / "README.md").rename(worktree / "renamed.md")
            if replace_content:
                (worktree / "renamed.md").write_text("completely different content\n")
            findings = [
                {
                    "title": "deferred",
                    "changed_paths": ["README.md", "renamed.md"],
                    "resolution": {
                        "status": "unresolved",
                        "summary": "needs follow-up",
                    },
                }
            ]
            if add_unrelated_file:
                # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
                # rename 判定の候補を増やしても unresolved の changed_paths から
                # rename 先を特定できることを検証する。
                (worktree / "extra.md").write_text("extra realization\n")
                findings.append(
                    {
                        "title": "extra update",
                        "changed_paths": ["extra.md"],
                        "resolution": {
                            "status": "fixed",
                            "summary": "updated extra file",
                        },
                    }
                )
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "findings": findings,
                    "verification": {
                        "status": "passed",
                        "summary": "fake full quality gate passed",
                    },
                },
                call_log_path=worktree / "README-call.json",
            )
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
            call_log_path=worktree / "call.json",
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    parts = state["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    refactor_state = load_refactor_state(worktree)
    assert "README.md" not in refactor_state
    assert refactor_state["renamed.md"]["investigation_required"] is True
    assert refactor_state["renamed.md"]["last_investigation_result"] == (
        "not_investigated"
    )
    reports = list(
        (root / ".cmoc" / "gu" / "report" / "realization" / "refactor" / "fork").glob(
            "*.md"
        )
    )
    assert len(reports) == 1
    report = reports[0].read_text()
    assert "## Completion\nuser_interruption" in report
    assert "## Unresolved targets\n- count: 1\n- paths:\n  - `renamed.md`" in report


def test_refactor_fork_moves_previous_unresolved_target_after_later_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """後続 target の rename でも既存 unresolved target を追従させる。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    call_log = (tmp_path / "unresolved_call.json").resolve()
    call_log.write_text("{}\n")
    reviewed: list[str] = []
    oracle_reviews = 0

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """README の unresolved 後、別 target で README を rename する。"""
        nonlocal oracle_reviews
        purpose = str(kwargs["purpose"])
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
                            "changed_paths": [],
                            "resolution": {
                                "status": "unresolved",
                                "summary": "人間の判断が必要",
                            },
                        }
                    ],
                    "verification": {
                        "status": "passed",
                        "summary": "fake full quality gate passed",
                    },
                },
            )
        if target == "oracle/spec.md":
            oracle_reviews += 1
            if oracle_reviews > 1:
                return SimpleNamespace(
                    returncode=0,
                    output_json={
                        "findings": [],
                        "verification": {
                            "status": "passed",
                            "summary": "fake full quality gate passed",
                        },
                    },
                )
            worktree = parameter.agent_call_cwd
            (worktree / "README.md").rename(worktree / "renamed.md")
            (worktree / "renamed.md").write_text("completely different content\n")
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "findings": [
                        {
                            "title": "README rename",
                            "changed_paths": ["README.md", "renamed.md"],
                            "resolution": {
                                "status": "fixed",
                                "summary": "rename completed",
                            },
                        }
                    ],
                    "verification": {
                        "status": "passed",
                        "summary": "fake full quality gate passed",
                    },
                },
            )
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    parts = state["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    refactor_state = load_refactor_state(worktree)
    assert "README.md" not in refactor_state
    assert refactor_state["renamed.md"]["investigation_required"] is True
    assert reviewed.count("README.md") == 1
    assert reviewed.count("oracle/spec.md") == 1
    assert "renamed.md" not in reviewed
    report = terminal_primary_report(result).read_text()
    assert 'completion_reason: "user_interruption"' in report
    assert "- count: 1" in report
    assert "`renamed.md`" in report


def test_refactor_missing_target_rejects_unexpected_processing_unit_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """消えた target の同期単位でも想定外 path を commit しない。"""
    _root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_refactor")

    (context.run_worktree / "README.md").unlink()
    unexpected_path = context.run_worktree / "memo" / "unexpected.md"
    unexpected_path.parent.mkdir()
    unexpected_path.write_text("must not be committed\n")
    before_head = run_git(context.run_worktree, "rev-parse", "HEAD").stdout.strip()

    with pytest.raises(CmocError, match="想定外差分"):
        refactor_module._run_refactor_unit(
            context,
            "README.md",
            [],
            {},
            [],
        )

    assert run_git(context.run_worktree, "rev-parse", "HEAD").stdout.strip() == (
        before_head
    )


def test_refactor_rejects_agent_changes_to_cmoc_managed_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor agent が cmoc 管理 file を変更した場合は commit しない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    managed_path = ".cmoc/gt/realization/refactor/state.json"

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """agent が refactor state を直接変更する状態を再現する。"""
        worktree = parameter.agent_call_cwd
        managed = worktree / managed_path
        managed.write_text(managed.read_text() + "\n")
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [
                    {
                        "title": "managed file change",
                        "changed_paths": [],
                        "resolution": {"status": "fixed"},
                    }
                ],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    parts = _state(state_path)["run"]["branch"].split("/")
    run_worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    restored = run_worktree / managed_path
    original = root / managed_path
    assert restored.exists() == original.exists()
    if original.exists():
        assert restored.read_text() == original.read_text()


def test_refactor_rejects_unreported_changed_paths_despite_evidences(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """evidences でなく changed_paths の申告漏れにより差分を拒否する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    first_review = True

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """evidences には全差分を載せ、changed_paths では一部だけ申告する。"""
        nonlocal first_review
        purpose = str(kwargs["purpose"])
        target = purpose.removeprefix("realization refactor: ")
        if target == "README.md" and first_review:
            first_review = False
            worktree = parameter.agent_call_cwd
            (worktree / "README.md").write_text("fixed\n")
            (worktree / "unattributed.py").write_text("unexpected\n")
            output = {
                "findings": [
                    {
                        "title": "README finding",
                        "evidences": [
                            {
                                "path": str(worktree / "README.md"),
                                "line_start": 1,
                                "line_end": 1,
                                "summary": "README の変更行",
                            },
                            {
                                "path": str(worktree / "unattributed.py"),
                                "line_start": 1,
                                "line_end": 1,
                                "summary": "追加した realization file",
                            },
                        ],
                        "changed_paths": ["README.md"],
                        "oracle_requirement": "README を正しく扱う",
                        "observed_implementation": "README に問題がある",
                        "reason": "修正が必要",
                        "resolution": {
                            "status": "fixed",
                            "summary": "README を修正した",
                            "verification": "確認済み",
                        },
                    }
                ],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            }
            postcondition = kwargs["structured_output_postcondition"]
            assert callable(postcondition)
            issues = postcondition(output, frozenset({"README.md", "unattributed.py"}))
            if issues:
                raise CmocError(
                    "Codex CLI の Structured Output 検証に失敗しました。",
                    ["Codex call log を確認してください。"],
                    repr(issues),
                )
            return SimpleNamespace(
                returncode=0,
                output_json=output,
            )
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Structured Output 検証に失敗しました" in result.output
    assert _state(state_path)["run"]["state"] == "error"
    parts = _state(state_path)["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert (worktree / "README.md").read_text() == "# repo\n"
    assert not (worktree / "unattributed.py").exists()


def test_refactor_changed_path_postcondition_reports_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """申告集合と初回 call の実差分が異なる場合は補正用エラーを返す。"""
    monkeypatch.setattr(
        refactor_module,
        "unexpected_agent_paths",
        lambda _context, _paths: [],
    )

    issues = refactor_module._changed_path_postcondition(
        SimpleNamespace(),
        {
            "findings": [{"changed_paths": ["README.md"]}],
            "verification": {
                "status": "passed",
                "summary": "fake full quality gate passed",
            },
        },
        frozenset({"README.md", "added.py"}),
    )

    assert len(issues) == 1
    assert issues[0].location == "findings[*].changed_paths"
    assert issues[0].expected == "['README.md', 'added.py']"
    assert issues[0].observed == "['README.md']"


def test_refactor_changed_path_postcondition_uses_deduplicated_union(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """複数所見で重複する changed_paths を集合として照合する。"""
    monkeypatch.setattr(
        refactor_module,
        "unexpected_agent_paths",
        lambda _context, _paths: [],
    )

    issues = refactor_module._changed_path_postcondition(
        SimpleNamespace(),
        {
            "findings": [
                {"changed_paths": ["README.md"]},
                {"changed_paths": ["README.md", "added.py"]},
            ],
            "verification": {
                "status": "passed",
                "summary": "fake full quality gate passed",
            },
        },
        frozenset({"README.md", "added.py"}),
    )

    assert not issues


def test_refactor_rejects_agent_commit_and_rolls_back_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor agent の commit が処理単位をすり抜けず、開始 HEAD へ戻る。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """agent が realization file を直接 commit する状態を再現する。"""
        before_agent_call = kwargs["before_agent_call"]
        assert callable(before_agent_call)
        before_agent_call()
        worktree = parameter.agent_call_cwd
        (worktree / "README.md").write_text("agent commit\n")
        run_git(worktree, "add", "README.md")
        run_git(worktree, "commit", "-m", "agent commit")
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    parts = _state(state_path)["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert (worktree / "README.md").read_text() == "# repo\n"
    assert (
        "agent commit"
        not in run_git(worktree, "log", "--format=%s").stdout.splitlines()
    )
    assert run_git(worktree, "status", "--porcelain").stdout == ""


def test_apply_error_report_survives_change_inspection_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """差分確認に失敗しても apply error report と state を保存する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    monkeypatch.setattr(
        apply_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("agent failed")),
    )
    monkeypatch.setattr(
        apply_module,
        "tree_changes",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            RuntimeError("git diff unavailable")
        ),
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    reports = list(
        (root / ".cmoc" / "gu" / "report" / "realization" / "apply" / "fork").glob(
            "*.md"
        )
    )
    assert len(reports) == 1
    assert "change inspection failed" in reports[0].read_text()


def test_apply_report_failure_after_joinable_publication_sets_error_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """成功処理後の fork report failure でも run state と report を一致させる。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(
        apply_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, output_json=None),
    )
    original_write_report = apply_module.write_fork_report
    calls = 0

    def fail_completed_report(*args: object, **kwargs: object) -> Path:
        """最初の completed report だけを失敗させる。"""
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("completed report failed")
        return original_write_report(*args, **kwargs)

    monkeypatch.setattr(apply_module, "write_fork_report", fail_completed_report)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert calls == 2
    assert _state(state_path)["run"]["state"] == "error"
    report = terminal_primary_report(result)
    assert 'state_after: "error"' in report.read_text()


def test_refactor_report_failure_after_joinable_publication_sets_error_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor の fork report failure でも run state と report を一致させる。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(
        refactor_module,
        "_initialize_cycle",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )
    original_write_report = refactor_module.write_fork_report
    calls = 0

    def fail_completed_report(*args: object, **kwargs: object) -> Path:
        """最初の completed report だけを失敗させる。"""
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("completed report failed")
        return original_write_report(*args, **kwargs)

    monkeypatch.setattr(refactor_module, "write_fork_report", fail_completed_report)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert calls == 2
    assert _state(state_path)["run"]["state"] == "error"
    report = terminal_primary_report(result)
    assert 'state_after: "error"' in report.read_text()


def test_apply_error_preserves_unreadable_process_tracking(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply error cleanup が検証不能な process tracking を削除しない。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    session_id = session_branch.removeprefix("cmoc/session/")
    tracking_path = run_process_id_path(root, session_id)

    def fail_agent(*_args: object, **_kwargs: object) -> NoReturn:
        """Codex failure と破損した tracking を再現する。"""
        tracking_path.write_bytes(b"\xff")
        raise RuntimeError("agent failed")

    monkeypatch.setattr(apply_module, "run_codex_exec", fail_agent)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    assert tracking_path.read_bytes() == b"\xff"


@pytest.mark.parametrize("interrupted", [False, True])
@pytest.mark.parametrize("inspection", ["changes", "state"])
def test_refactor_terminal_report_survives_change_inspection_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupted: bool,
    inspection: str,
) -> None:
    """確認不能な差分・履歴を空として扱わず terminal report と state を保存する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    agent_failed = False

    def fail_agent(*_args: object, **_kwargs: object) -> NoReturn:
        """agent failure または user interruption を再現する。"""
        nonlocal agent_failed
        agent_failed = True
        if interrupted:
            raise KeyboardInterrupt()
        raise RuntimeError("agent failed")

    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        fail_agent,
    )
    if inspection == "changes":
        monkeypatch.setattr(
            refactor_module,
            "tree_changes",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(
                RuntimeError("git diff unavailable")
            ),
        )
    else:
        load = refactor_module.load_refactor_state

        def unreadable_after_agent(root):
            if agent_failed:
                raise RuntimeError("state unavailable")
            return load(root)

        monkeypatch.setattr(
            refactor_module, "load_refactor_state", unreadable_after_agent
        )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    expected_state = "joinable" if interrupted else "error"
    expected_reason = "user_interruption" if interrupted else "error"
    assert result.exit_code == (0 if interrupted else 1)
    assert _state(state_path)["run"]["state"] == expected_state
    reports = list(
        (root / ".cmoc" / "gu" / "report" / "realization" / "refactor" / "fork").glob(
            "*.md"
        )
    )
    assert len(reports) == 1
    report_text = reports[0].read_text()
    if inspection == "changes":
        assert "change inspection failed" in report_text
        assert "## Changed paths\n- unavailable" in report_text
    else:
        assert "state inspection failed" in report_text
        assert "- entries: null" in report_text
    assert f'completion_reason: "{expected_reason}"' in report_text


def test_apply_failure_stops_tracked_codex_children_before_rollback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply error cleanup が追跡中 Codex child を rollback 前に停止する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    child = SimpleNamespace(process_id=123, start_time=456, process_group_id=123)
    tracked = SimpleNamespace(child_processes=(child,))
    events: list[str] = []

    monkeypatch.setattr(
        runtime_run_module,
        "read_run_process_id",
        lambda *_args: tracked,
    )
    monkeypatch.setattr(
        runtime_run_module,
        "stop_child_process_group",
        lambda _process: events.append("stop"),
    )
    original_rollback = apply_module.rollback_work_unit

    def record_rollback(worktree: Path) -> None:
        """rollback の順序を確認してから本来の cleanup を実行する。"""
        events.append("rollback")
        original_rollback(worktree)

    monkeypatch.setattr(apply_module, "rollback_work_unit", record_rollback)
    monkeypatch.setattr(
        apply_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert events == ["stop", "rollback"]
    assert _state(state_path)["run"]["state"] == "error"


def test_apply_error_cleanup_rejects_delayed_agent_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """error cleanup の停止後検査で遅延 agent commit を run に残さない。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    run_worktree: Path | None = None

    def fail_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> NoReturn:
        """本命 agent の失敗後に error cleanup へ進む状態を再現する。"""
        nonlocal run_worktree
        run_worktree = parameter.agent_call_cwd
        raise RuntimeError("agent failed")

    def delayed_agent_commit(_root: Path, _session_id: str) -> list[str]:
        """停止処理の直前に agent child が commit した状態を再現する。"""
        assert run_worktree is not None
        (run_worktree / "README.md").write_text("delayed agent commit\n")
        run_git(run_worktree, "add", "README.md")
        run_git(run_worktree, "commit", "-m", "delayed agent commit")
        return []

    monkeypatch.setattr(apply_module, "run_codex_exec", fail_apply)
    monkeypatch.setattr(
        apply_module,
        "stop_tracked_codex_children",
        delayed_agent_commit,
    )

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    assert run_worktree is not None
    assert (run_worktree / "README.md").read_text() == "# repo\n"
    assert (
        "delayed agent commit"
        not in run_git(run_worktree, "log", "--format=%s").stdout.splitlines()
    )
    report_path = terminal_primary_report(result)
    assert "agent commit cleanup failed" in report_path.read_text()


@pytest.mark.parametrize(
    "failure",
    [
        RuntimeError("process tracking setup failed"),
        CmocError("process tracking setup failed", [], "tracking path"),
    ],
)
def test_apply_start_failure_after_run_publish_is_reported(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: BaseException,
) -> None:
    """run state 公開後の初期化失敗でも apply fork report を残す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md。
    """

    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fail_process_tracking(*_args: object, **_kwargs: object) -> None:
        """process tracking 初期化の失敗を再現する。"""
        raise failure

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
        (root / ".cmoc" / "gu" / "report" / "realization" / "apply" / "fork").glob(
            "*.md"
        )
    )
    assert len(reports) == 1
    assert terminal_primary_report(result) == reports[0]
    assert 'state_before: "ready"' in reports[0].read_text()


def test_apply_start_failure_does_not_recover_existing_error_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """新しい apply fork の事前条件失敗で既存 error run を変更しない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "error")
    (context.run_worktree / "README.md").write_text("existing error run\n")

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    assert (context.run_worktree / "README.md").read_text() == "existing error run\n"
    assert current_branch(root) == context.session_branch


def test_refactor_start_failure_does_not_recover_existing_error_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """新しい refactor fork の事前条件失敗で既存 error run を変更しない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_refactor")
    set_run_state(context, "error")
    (context.run_worktree / "README.md").write_text("existing error run\n")

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    assert (context.run_worktree / "README.md").read_text() == "existing error run\n"
    assert current_branch(root) == context.session_branch


def test_start_run_rechecks_session_branch_under_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """fork lock 待機中の branch 変更で別 session の run を作成しない。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_current_branch = lifecycle_module.current_branch
    calls = 0

    def switch_branch_after_ready_check(_root: Path) -> str:
        """lock 内の再検査だけへ別 branch を返す。"""
        nonlocal calls
        calls += 1
        if calls == 3:
            return "cmoc/session/changed-before-fork"
        return original_current_branch(_root)

    monkeypatch.setattr(
        lifecycle_module,
        "current_branch",
        switch_branch_after_ready_check,
    )

    with pytest.raises(CmocError, match="current branch が lock 内で変更"):
        start_editing_run("realization_apply")

    assert _state(state_path)["run"]["state"] == "ready"
    assert current_branch(root) == session_branch
    assert not list((root / ".cmoc" / "gu" / "worktree").glob("*/*"))


@pytest.mark.parametrize("interrupted_before_tracking", [False, True])
def test_refactor_start_error_does_not_recover_competing_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupted_before_tracking: bool,
) -> None:
    """開始失敗や中断で別 invocation の run を回収しない。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_start = refactor_module.start_editing_run

    def competing_start(kind: str) -> EditingRunContext:
        """別 invocation が lock 内で run を公開した後の競合を再現する。"""
        context = original_start(kind)
        if interrupted_before_tracking:
            run_process_id_path(context.repo, context.session_id).unlink()
            raise KeyboardInterrupt
        raise CmocError(
            "別の editing run が先に開始されました。",
            [],
            "simulated concurrent start",
        )

    monkeypatch.setattr(refactor_module, "start_editing_run", competing_start)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == (0 if interrupted_before_tracking else 1)
    assert _state(state_path)["run"]["state"] == "running"
    assert current_branch(root) == session_branch


def test_recover_started_run_rejects_run_owned_by_other_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """別 process の tracking を持つ active run を recovery 対象にしない。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_refactor")
    tracked = SimpleNamespace(
        process_id=os.getpid() + 1,
        start_time=None,
        child_processes=(),
    )
    monkeypatch.setattr(lifecycle_module, "read_run_process_id", lambda *_args: tracked)

    assert lifecycle_module.recover_started_run("realization_refactor") is None
    assert _state(state_path)["run"]["state"] == "running"
    assert context.run_worktree.exists()


def test_recover_started_run_rejects_unreadable_process_tracking(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """壊れた tracking を未作成として別 process の run recovery に使わない。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_refactor")
    tracking_path = run_process_id_path(
        root, session_branch.removeprefix("cmoc/session/")
    )
    tracking_path.write_text("not a process identity\n")

    assert lifecycle_module.recover_started_run("realization_refactor") is None
    assert _state(state_path)["run"]["state"] == "running"
    assert context.run_worktree.exists()


def test_run_join_allows_oracle_change_on_session_branch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session branch の oracle change を run join が保持する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    _mark_refactor_target_no_findings(root, "oracle/spec.md")
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    (root / "oracle" / "spec.md").write_text("session oracle change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "session oracle change")

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"
    assert (root / "oracle" / "spec.md").read_text() == "session oracle change\n"
    diff_base = _state(state_path)["session"]["last_joined_apply_fork_commit"]
    assert diff_base == context.run_fork_commit
    assert (
        "session oracle change"
        in run_git(root, "diff", diff_base, "HEAD", "--", "oracle/spec.md").stdout
    )


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
    monkeypatch.chdir(context.run_worktree)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"


def test_run_join_from_run_worktree_tracks_main_doctor_repairs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run 起点の doctor が session 側へ行う修復も join の許可差分に含める。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    gitignore = root / ".gitignore"
    gitignore.write_text(gitignore.read_text().replace("/.cmoc/gu/\n", ""))
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "create stale cmoc ignore")

    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")
    monkeypatch.chdir(context.run_worktree)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert "/.cmoc/gu/" in gitignore.read_text()


def test_run_join_from_run_worktree_preserves_prior_session_doctor_path_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor と同じ path の先行 session 差分も統合する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    gitignore = root / ".gitignore"
    gitignore.write_text("user session change\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "change cmoc ignore policy")
    set_run_state(context, "joinable")
    monkeypatch.chdir(context.run_worktree)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert "user session change" in gitignore.read_text()
    assert _state(state_path)["run"]["state"] == "ready"


def test_run_join_preserves_existing_non_search_config_shape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通常起動の doctor は検索以外の不足を理由に config を書き換えない。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    config = root / ".cmoc" / "gt" / "config.json"
    config_data = json.loads(config.read_text())
    config_data.pop("num_parallel")
    config.write_text(json.dumps(config_data, indent=2) + "\n")
    run_git(root, "add", ".cmoc/gt/config.json")
    run_git(root, "commit", "-m", "create stale doctor config")
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert config.is_file()
    assert "num_parallel" not in json.loads(config.read_text())


@pytest.mark.parametrize("change", ["rename", "delete"])
def test_run_join_accepts_realization_rename_and_delete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change: str,
) -> None:
    """run join が fork 時点の realization path の rename と削除を許可する。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    readme = context.run_worktree / "README.md"
    if change == "rename":
        readme.rename(context.run_worktree / "renamed.md")
    else:
        readme.unlink()
    commit_work_unit(context.run_worktree, f"run {change}")
    set_run_state(context, "joinable")

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert not (root / "README.md").exists()
    assert (root / "renamed.md").exists() is (change == "rename")


def test_resolve_active_run_rejects_run_branch_from_another_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """active run の branch が state の session と異なる場合は拒否する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    state = _state(state_path)
    state["run"] = {
        "state": "running",
        "kind": "realization_apply",
        "branch": f"cmoc/run/sess_000001_2026-09-29_15-04/{RUN_ID}",
        "fork_commit": state["session"]["session_fork_commit"],
    }
    state_path.write_text(json.dumps(state, indent=2) + "\n")

    with pytest.raises(CmocError, match="branch が session state と一致しません"):
        lifecycle_module.resolve_active_run({"running"})


def test_set_run_state_rejects_overwriting_terminal_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """公開済み terminal state を遅延 cleanup が別 state へ変更しない。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    set_run_state(context, "joinable")

    with pytest.raises(CmocError, match="state が実行中に変更されました"):
        set_run_state(context, "error")

    assert _state(state_path)["run"]["state"] == "joinable"


@pytest.mark.parametrize(
    "unexpected_path", ["oracle/unexpected.md", "oracle/unexpected[1].md"]
)
def test_run_join_force_resolve_reverts_only_run_unexpected_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    unexpected_path: str,
) -> None:
    """force-resolve が run branch の想定外 path だけを戻すことを確認する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("allowed\n")
    (context.run_worktree / unexpected_path).write_text("unexpected\n")
    commit_work_unit(context.run_worktree, "mixed run changes")
    set_run_state(context, "joinable")

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
    assert not (root / unexpected_path).exists()
    assert (
        "--force-resolve reverted unexpected run paths"
        in terminal_primary_report(joined).read_text()
    )


def test_run_join_force_resolve_restores_realization_source_of_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """force-resolve が想定外 rename の realization 側を失わせないことを確認する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    destination = context.run_worktree / "oracle" / "unexpected.md"
    destination.parent.mkdir(exist_ok=True)
    (context.run_worktree / "README.md").rename(destination)
    commit_work_unit(context.run_worktree, "rename realization into oracle")
    set_run_state(context, "joinable")

    result = runner.invoke(
        app,
        ["run", "join", "--force-resolve"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert (root / "README.md").read_text() == "# repo\n"
    assert not (root / "oracle" / "unexpected.md").exists()


def test_run_join_cleanup_preserves_worktree_when_removal_leaves_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """worktree removal 後も path が残る場合は branch を削除しない。"""
    run_worktree = tmp_path / "run"
    run_worktree.mkdir()
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path / "session",
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=run_worktree,
    )
    monkeypatch.setattr(
        run_join_module,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0),
    )
    monkeypatch.setattr(
        run_join_module,
        "remove_worktree",
        lambda *_args: SimpleNamespace(returncode=0),
    )
    monkeypatch.setattr(
        run_join_module,
        "branch_exists",
        lambda *_args: pytest.fail("branch must not be deleted"),
    )

    warnings: list[str] = []
    cleanup = run_join_module.cleanup_joined_run(context, warnings)

    assert cleanup == "preserved"
    assert warnings == ["run worktree cleanup failed"]


def test_run_join_cleanup_warns_when_worktree_removal_raises(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """worktree removal の例外時も run resource を保持して warning にする。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path / "session",
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=tmp_path / "run",
    )
    monkeypatch.setattr(
        run_join_module,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0),
    )
    monkeypatch.setattr(
        run_join_module,
        "remove_worktree",
        lambda *_args: (_ for _ in ()).throw(RuntimeError("cleanup failed")),
    )
    monkeypatch.setattr(
        run_join_module,
        "branch_exists",
        lambda *_args: pytest.fail(
            "branch must not be inspected after removal failure"
        ),
    )

    warnings: list[str] = []
    cleanup = run_join_module.cleanup_joined_run(context, warnings)

    assert cleanup == "preserved"
    assert warnings == ["run worktree cleanup failed"]


def test_run_join_cleanup_checks_branch_deletion_postcondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """branch 削除が成功を返しても残存を検出して warning にする。"""
    run_worktree = tmp_path / "run"
    session_worktree = tmp_path / "session"
    session_worktree.mkdir()
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=session_worktree,
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=run_worktree,
    )
    branch_checks = iter([True, True])
    deleted: list[str] = []
    monkeypatch.setattr(
        run_join_module,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0),
    )
    monkeypatch.setattr(
        run_join_module,
        "remove_worktree",
        lambda *_args: SimpleNamespace(returncode=0),
    )
    monkeypatch.setattr(
        run_join_module,
        "branch_exists",
        lambda *_args: next(branch_checks),
    )
    monkeypatch.setattr(
        run_join_module,
        "delete_branch",
        lambda _repo, branch: deleted.append(branch) or SimpleNamespace(returncode=0),
    )

    warnings: list[str] = []
    cleanup = run_join_module.cleanup_joined_run(context, warnings)

    assert cleanup == "branch_preserved"
    assert deleted == [context.run_branch]
    assert warnings == ["run branch cleanup failed"]


def test_run_join_conflict_abort_failure_still_restores_session_tree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """merge --abort の失敗時も join 開始前の clean tree へ戻す。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path / "session",
        session_id=SESSION_ID,
        state_path=tmp_path / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit="run-fork",
        run_worktree=tmp_path / "run",
    )
    commands: list[list[str]] = []

    def fake_run_git(
        args: list[str],
        _cwd: Path,
        check: bool = True,
    ) -> SimpleNamespace:
        """join rollback の分岐を確認するための Git 実行結果を返す。"""
        commands.append(args)
        if args[:2] == ["rev-parse", "-q"]:
            return SimpleNamespace(returncode=0, stdout="")
        if args == ["merge", "--abort"]:
            return SimpleNamespace(returncode=1, stdout="")
        return SimpleNamespace(returncode=0, stdout="")

    monkeypatch.setattr(run_join_module, "run_git", fake_run_git)
    run_join_module.restore_session_after_join_failure(
        context, "session-head-before-join"
    )

    assert ["reset", "--hard", "session-head-before-join"] in commands
    assert ["clean", "-fd"] in commands


def test_run_join_keeps_merge_when_post_join_sync_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """post-join 同期失敗時は確定済み merge と run 資源を保持する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    session_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    monkeypatch.setattr(
        run_join_module,
        "sync_refactor_state",
        lambda _root: (_ for _ in ()).throw(RuntimeError("sync failed")),
    )

    failed = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert failed.exit_code == 1
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() != session_head
    assert (root / "README.md").read_text() == "realized\n"
    assert _state(state_path)["run"]["state"] == "error"
    assert _state(state_path)["session"]["last_joined_apply_fork_commit"] is None
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()

    monkeypatch.setattr(run_join_module, "sync_refactor_state", lambda _root: None)
    joined = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert joined.exit_code == 0
    assert (root / "README.md").read_text() == "realized\n"
    assert _state(state_path)["session"]["last_joined_apply_fork_commit"] is None
    for output in (joined.output, terminal_primary_report(joined).read_text()):
        assert "session.last_joined_apply_fork_commit updated" not in output


def test_run_join_integrates_content_conflict_and_incidental_edit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run と session の変更を agent が統合し、付随編集も merge へ含める。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("run change\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    (root / "README.md").write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_head = run_git(context.run_worktree, "rev-parse", "HEAD").stdout.strip()
    session_head = run_git(root, "rev-parse", "HEAD").stdout.strip()

    def fake_codex(parameter: AgentCallParameter, **_kwargs: object) -> object:
        assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE
        assert parameter.agent_call_cwd == root
        assert run_head in parameter.prompt
        assert session_head in parameter.prompt
        (root / "README.md").write_text("session change\nrun change\n")
        (root / "src" / "related.py").parent.mkdir(exist_ok=True)
        (root / "src" / "related.py").write_text("value = 1\n")
        return SimpleNamespace(
            output_text="merge_resolution: resolved\n検証: 両側の内容を確認しました。\n"
        )

    monkeypatch.setattr(merge_conflict_module, "run_codex_exec", fake_codex)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert (root / "README.md").read_text() == "session change\nrun change\n"
    assert (root / "src" / "related.py").read_text() == "value = 1\n"
    assert _state(state_path)["run"]["state"] == "ready"
    assert "src/related.py" in terminal_primary_report(result).read_text()


def test_run_join_rolls_back_unresolved_content_conflict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """agent が未解消と報告した merge は付随編集ごと開始前へ戻す。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("run change\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    (root / "README.md").write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    session_head = run_git(root, "rev-parse", "HEAD").stdout.strip()

    def fake_codex(_parameter: AgentCallParameter, **_kwargs: object) -> object:
        (root / "src" / "incidental.py").parent.mkdir(exist_ok=True)
        (root / "src" / "incidental.py").write_text("value = 1\n")
        return SimpleNamespace(
            output_text="merge_resolution: unresolved\n検証不足: 人間意図を確認できません。\n"
        )

    monkeypatch.setattr(merge_conflict_module, "run_codex_exec", fake_codex)
    failed = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert failed.exit_code == 1
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == session_head
    assert (root / "README.md").read_text() == "session change\n"
    assert not (root / "src" / "incidental.py").exists()
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert _state(state_path)["run"]["state"] == "error"
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()


def test_run_join_keeps_completed_merge_when_final_report_update_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """cleanup 後の report 更新失敗でも保存済み report と merge を保持する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    original_write_report = run_join_module.write_lifecycle_report

    def fail_final_report(
        _report_context: EditingRunContext,
        _operation: str,
        **kwargs: object,
    ) -> Path:
        """cleanup 前の report 保存後に行う最終更新失敗を再現する。"""
        if kwargs.get("report_path") is not None:
            raise RuntimeError("final report update failed")
        return original_write_report(_report_context, _operation, **kwargs)

    monkeypatch.setattr(run_join_module, "write_lifecycle_report", fail_final_report)
    monkeypatch.setattr(
        run_join_command_module, "write_lifecycle_report", fail_final_report
    )

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 1, result.output
    assert (root / "README.md").read_text() == "realized\n"
    assert "run join report の最終状態を保存できませんでした。" in result.output
    assert _state(state_path)["run"]["state"] == "ready"
    assert (
        _state(state_path)["session"]["last_joined_apply_fork_commit"]
        == context.run_fork_commit
    )
    assert not context.run_worktree.exists()
    assert not run_git(root, "branch", "--list", context.run_branch).stdout.strip()
    reports = list(root.joinpath(".cmoc", "gu", "report", "run", "join").glob("*.md"))
    assert reports == [terminal_primary_report(result)]
    rendered = reports[0].read_text()
    assert 'terminal_classification: "error"' in rendered
    assert 'state_after: "ready"' in rendered
    assert 'cleanup: "pending"' in rendered
    assert "cleanup pending" in rendered


def test_run_join_saves_report_before_cleanup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run resource を削除する前に pending report を保存する。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    events: list[tuple[str, object]] = []
    original_write_report = run_join_command_module.write_lifecycle_report

    def record_report(
        report_context: EditingRunContext,
        operation: str,
        **kwargs: object,
    ) -> Path:
        """report 保存の cleanup 前後の順序を記録する。"""
        details = kwargs["details"]
        assert isinstance(details, dict)
        events.append(("report", details["cleanup"]))
        return original_write_report(report_context, operation, **kwargs)

    def record_cleanup(_context: EditingRunContext, _warnings: list[str]) -> str:
        """cleanup の開始を記録して成功を返す。"""
        events.append(("cleanup", None))
        return "completed"

    monkeypatch.setattr(
        run_join_command_module, "write_lifecycle_report", record_report
    )
    monkeypatch.setattr(run_join_module, "cleanup_joined_run", record_cleanup)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert events == [("report", "pending"), ("cleanup", None), ("report", "completed")]
    assert (root / "README.md").read_text() == "realized\n"


def test_run_join_preserves_active_state_when_cleanup_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """cleanup 失敗時も残存 resource を abandon で回収できる状態を保つ。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    monkeypatch.setattr(
        run_join_module,
        "cleanup_joined_run",
        lambda _context, warnings: warnings.append("cleanup pending") or "preserved",
    )

    joined = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert joined.exit_code == 0, joined.output
    state = _state(state_path)
    assert state["run"] == {
        "state": "error",
        "kind": "realization_apply",
        "branch": context.run_branch,
        "fork_commit": context.run_fork_commit,
    }
    assert state["session"]["last_joined_apply_fork_commit"] == context.run_fork_commit
    assert context.run_worktree.exists()
    assert run_git(root, "branch", "--list", context.run_branch).stdout.strip()

    abandoned = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)

    assert abandoned.exit_code == 0, abandoned.output
    assert _state(state_path)["run"]["state"] == "ready"
    assert not context.run_worktree.exists()
    assert not run_git(root, "branch", "--list", context.run_branch).stdout.strip()


def test_refactor_fork_commits_cycle_until_user_interruption(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """一巡の確定実績を保持し、ユーザー停止で joinable にする。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    reviewed: list[str] = []

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """refactor agent の deterministic response を返す。"""
        purpose = str(kwargs["purpose"])
        target = purpose.removeprefix("realization refactor: ")
        reviewed.append(target)
        if target == "README.md":
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "findings": [
                        {
                            "title": "差分のない fixed 自己申告",
                            "changed_paths": [],
                            "resolution": {
                                "status": "fixed",
                                "summary": "agent は修正済みと申告した",
                            },
                        }
                    ],
                    "verification": {
                        "status": "passed",
                        "summary": "fake full quality gate passed",
                    },
                },
            )
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

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
    assert all(not entry["investigation_required"] for entry in refactor_state.values())
    assert all(
        entry["last_investigation_result"] == "no_findings"
        for entry in refactor_state.values()
    )
    assert "- completion_reason: `user_interruption`" in result.output
    assert "- unresolved targets: `0`" in result.output
    report = terminal_primary_report(result)
    report_text = report.read_text()
    assert "- `README.md`: 0 finding(s)" in report_text
    assert 'command: "cmoc realization refactor fork"' in report_text
    assert 'terminal_classification: "user_interruption"' in report_text
    assert "exit_code: 0" in report_text
    assert "## Related logs" in report_text


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
    notifications: list[tuple[str, str]] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda command, _root, state: notifications.append((command, state)),
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    report = terminal_primary_report(result)
    assert 'completion_reason: "user_interruption"' in report.read_text()
    assert notifications == [("realization refactor fork", "interrupted")]


@pytest.mark.parametrize(
    "kind", ["realization_apply", "realization_refactor", "feedback_report"]
)
def test_start_run_prepares_work_directories_before_publishing_state(
    tmp_path, monkeypatch, kind
):
    """全 editing workload の新 worktree を running state の公開前に補完する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_write = lifecycle_module.write_state
    observed = []

    def observe_running(path, state):
        if state.run.state == "running":
            run_worktree = lifecycle_module.worktree_for_branch(root, state.run.branch)
            assert all(
                (run_worktree / relative).is_dir() for relative in _WORK_DIRECTORIES
            )
            assert run_git(run_worktree, "status", "--short").stdout == ""
            observed.append(run_worktree)
        original_write(path, state)

    monkeypatch.setattr(lifecycle_module, "write_state", observe_running)

    context = start_editing_run(kind)

    assert observed == [context.run_worktree]
    assert context.run_worktree != root
    assert all(
        not list((context.run_worktree / relative).iterdir())
        for relative in _WORK_DIRECTORIES
    )
    assert _state(state_path)["run"]["state"] == "running"


@pytest.mark.parametrize(
    "kind", ["realization_apply", "realization_refactor", "feedback_report"]
)
def test_start_run_directory_conflict_cleans_unpublished_resources(
    tmp_path, monkeypatch, kind
):
    """配置先の衝突で開始に失敗した場合、session の内容と ready state を保つ。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    collision = root / "src"
    collision.rmdir()
    collision.write_text("kept tracked collision\n")
    run_git(root, "add", "src")
    run_git(root, "commit", "-m", "track conflicting placement")
    state_before = state_path.read_bytes()
    original_target = lifecycle_module.new_run_target
    targets = []

    def record_target(*args):
        target = original_target(*args)
        targets.append(target)
        return target

    monkeypatch.setattr(lifecycle_module, "new_run_target", record_target)

    with pytest.raises(CmocError) as exc_info:
        start_editing_run(kind)

    [(run_branch, run_worktree)] = targets
    assert "作業用配置先" in exc_info.value.summary
    assert f"work-root: {run_worktree}" in exc_info.value.detail
    assert f"path: {run_worktree / 'src'}" in exc_info.value.detail
    assert state_path.read_bytes() == state_before
    assert collision.read_text() == "kept tracked collision\n"
    assert not run_worktree.exists()
    assert not lifecycle_module.branch_exists(root, run_branch)
    assert not run_process_id_path(
        root, session_branch.removeprefix("cmoc/session/")
    ).exists()


def test_start_run_interrupt_during_worktree_creation_cleans_partial_resources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run worktree の作成途中で中断しても未公開 resource を残さない。"""
    root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    original_create = lifecycle_module.create_run_worktree
    created_target: dict[str, Path | str] = {}

    def create_then_interrupt(
        repository: Path,
        branch: str,
        worktree: Path,
        *,
        start_point: str,
    ) -> None:
        """git resource 作成後、lifecycle の ownership 記録前に中断する。"""
        original_create(repository, branch, worktree, start_point=start_point)
        created_target.update(branch=branch, worktree=worktree)
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        lifecycle_module,
        "create_run_worktree",
        create_then_interrupt,
    )

    with pytest.raises(KeyboardInterrupt):
        start_editing_run("realization_refactor")

    created_worktree = Path(str(created_target["worktree"]))
    assert not created_worktree.exists()
    assert not created_worktree.is_symlink()
    assert not lifecycle_module.branch_exists(root, str(created_target["branch"]))


def test_start_run_interrupt_after_state_write_restores_ready_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """state 公開直後の中断で resource と running state を残さない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_write_state = lifecycle_module.write_state
    write_count = 0

    def write_then_interrupt(path: Path, state: SessionState) -> None:
        """running state の保存後、公開 flag 更新前に中断する。"""
        nonlocal write_count
        original_write_state(path, state)
        write_count += 1
        if write_count == 1:
            raise KeyboardInterrupt()

    monkeypatch.setattr(lifecycle_module, "write_state", write_then_interrupt)

    with pytest.raises(KeyboardInterrupt):
        start_editing_run("realization_refactor")

    assert _state(state_path)["run"] == {
        "state": "ready",
        "kind": None,
        "branch": None,
        "fork_commit": None,
    }
    assert list((root / ".cmoc" / "gu" / "worktree").glob("*/*")) == []
    run_entries = run_git(root, "branch", "--list", "cmoc/run/*").stdout
    assert run_entries.strip() == ""


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
    report = terminal_primary_report(result)
    assert 'completion_reason: "error"' in report.read_text()
    assert 'state_before: "ready"' in report.read_text()


def test_refactor_start_interruption_with_broken_tracking_reports_existing_run(
    tmp_path, monkeypatch
):
    """成立済み run の追跡失敗を「run 未成立」とせず、資源を残して error にする。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    session_id = session_branch.removeprefix("cmoc/session/")
    tracking = run_process_id_path(root, session_id)

    def interrupted_tracking(*_args):
        tracking.parent.mkdir(parents=True, exist_ok=True)
        tracking.write_bytes(b"\xff")
        signal.raise_signal(signal.SIGINT)

    monkeypatch.setattr(lifecycle_module, "write_run_process_id", interrupted_tracking)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 1, result.output
    run = _state(state_path)["run"]
    assert run["state"] == "error"
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    assert worktree.is_dir()
    assert tracking.read_bytes() == b"\xff"
    report = terminal_primary_report(result).read_text()
    assert "run not established" not in report
    assert "Codex child stop failed" in report
    assert "rollback not attempted" in report


def test_refactor_fork_defers_unresolved_target_and_completes_remaining_targets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """unresolved target を保留し、残りの target を処理して cycle を完了する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    reviewed: list[str] = []
    call_log = (tmp_path / "unresolved_call.json").resolve()
    call_log.write_text("{}\n")

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """unresolved target を返し、他の target は処理済みとして返す。"""
        purpose = str(kwargs["purpose"])
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
                            "changed_paths": [],
                            "resolution": {
                                "status": "unresolved",
                                "summary": "人間の判断が必要",
                            },
                        }
                    ],
                    "verification": {
                        "status": "passed",
                        "summary": "fake full quality gate passed",
                    },
                },
            )
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)

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
    assert "- completion_reason: `user_interruption`" in result.output
    assert "- unresolved targets: `1`" in result.output
    report = terminal_primary_report(result)
    report_text = report.read_text()
    assert 'completion_reason: "user_interruption"' in report_text
    assert f"- processed targets: {len(refactor_state)}" in report_text
    assert "- uninvestigated targets: 0" in report_text
    assert "- count: 1" in report_text
    assert "`README.md`" in report_text
    assert "README unresolved finding" in report_text
    assert "resolution.summary: 人間の判断が必要" in report_text
    assert f"Codex call log: `{call_log}`" in report_text


def test_refactor_interrupt_rolls_back_current_unit_and_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """current refactor unit の中断時に差分を戻して joinable にする。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def interrupting_agent(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> NoReturn:
        """差分を作成した処理単位の途中で利用者中断を再現する。"""
        worktree = parameter.agent_call_cwd
        (worktree / "README.md").write_text("interrupted\n")
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        interrupting_agent,
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    parts = state["run"]["branch"].split("/")
    run_worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert (run_worktree / "README.md").read_text() == "# repo\n"
    report = terminal_primary_report(result)
    assert 'completion_reason: "user_interruption"' in report.read_text()
    assert "- completion_reason: `user_interruption`" in result.output
    assert "- unresolved targets: `0`" in result.output
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    events = [
        json.loads(line)
        for path in (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
        for line in path.read_text().splitlines()
    ]
    completion = next(
        event
        for event in events
        if event["event"] == "command_finished"
        and event["command"] == "realization refactor fork"
    )
    assert completion["completion_reason"] == "user_interruption"
    assert completion["terminal_result"]["details"] == [
        {"name": "unresolved targets", "value": 0}
    ]
    assert completion["primary_report_path"] == str(report.resolve())


def test_refactor_interrupt_before_run_creation_is_normal_completion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run 作成前の fork lifecycle 中断も正常終了として記録する。"""
    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_step = refactor_module.start_subcommand_step

    def interrupt_before_run(
        index: int | str,
        description: str,
        log_description: str | None = None,
    ) -> None:
        """run 作成 step の開始直前に利用者中断を再現する。"""
        if index == 2:
            raise KeyboardInterrupt()
        original_step(index, description, log_description)

    monkeypatch.setattr(refactor_module, "start_subcommand_step", interrupt_before_run)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "ready"
    assert "# 失敗" not in result.output
    events = [
        json.loads(line)
        for path in (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
        for line in path.read_text().splitlines()
    ]
    assert any(
        event.get("event") == "user_interruption"
        and event.get("result") == "interrupted"
        for event in events
    )
    assert any(
        event.get("event") == "command_finished" and event.get("returncode") == 0
        for event in events
    )


@pytest.mark.parametrize("interrupt_point", ["commit", "post_commit_record"])
def test_refactor_interrupt_after_unit_commit_reports_confirmed_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupt_point: str,
) -> None:
    """処理単位の commit または確定記録後に中断しても進捗を report する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    call_log = (tmp_path / "unresolved_call.json").resolve()
    call_log.write_text("{}\n")

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """README の commit 済み処理単位に unresolved finding を返す。"""
        target = str(kwargs["purpose"]).removeprefix("realization refactor: ")
        if target == "README.md":
            worktree = parameter.agent_call_cwd
            (worktree / "README.md").write_text("# repo\n\nfixed\n")
            return SimpleNamespace(
                returncode=0,
                call_log_path=call_log,
                output_json={
                    "findings": [
                        {
                            "title": "README unresolved finding",
                            "changed_paths": ["README.md"],
                            "resolution": {
                                "status": "unresolved",
                                "summary": "人間の判断が必要",
                            },
                        }
                    ],
                    "verification": {
                        "status": "passed",
                        "summary": "fake full quality gate passed",
                    },
                },
            )
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [],
                "verification": {
                    "status": "passed",
                    "summary": "fake full quality gate passed",
                },
            },
        )

    original_commit = refactor_module.commit_work_unit
    original_tree_changes = refactor_module.tree_changes
    tree_interrupted = False

    def commit_then_interrupt(
        worktree: Path,
        message: str,
        **kwargs: object,
    ) -> str | None:
        """README の処理単位を commit した直後に中断する。"""
        result = original_commit(worktree, message, **kwargs)
        if (
            interrupt_point == "commit"
            and message == "cmoc realization refactor README.md"
        ):
            raise KeyboardInterrupt()
        return result

    def interrupt_during_recording(
        worktree: Path,
        base: str,
        end: str = "HEAD",
    ) -> list[GitChange]:
        """commit 済み処理単位の差分記録中断を再現する。"""
        nonlocal tree_interrupted
        changes = original_tree_changes(worktree, base, end)
        if (
            interrupt_point == "post_commit_record"
            and not tree_interrupted
            and any("README.md" in change.paths for change in changes)
        ):
            tree_interrupted = True
            raise KeyboardInterrupt()
        return changes

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    _stop_after_cycles(monkeypatch)
    monkeypatch.setattr(refactor_module, "commit_work_unit", commit_then_interrupt)
    monkeypatch.setattr(refactor_module, "tree_changes", interrupt_during_recording)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    state = _state(state_path)
    assert state["run"]["state"] == "joinable"
    parts = state["run"]["branch"].split("/")
    run_worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert (run_worktree / "README.md").read_text() == "# repo\n\nfixed\n"
    assert (
        run_git(
            run_worktree, "log", "-1", "--format=%s", "--", "README.md"
        ).stdout.strip()
        == "cmoc realization refactor README.md"
    )
    report = terminal_primary_report(result)
    report_text = report.read_text()
    assert "- processed targets: 2" in report_text
    assert "- `README.md`: 1 finding(s)" in report_text
    assert "- count: 1" in report_text
    assert "README unresolved finding" in report_text


def test_refactor_interrupt_stops_tracked_codex_children_before_rollback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """中断時に追跡中 Codex child を停止してから rollback する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    child = SimpleNamespace(process_id=123, start_time=456, process_group_id=123)
    tracked = SimpleNamespace(child_processes=(child,))
    stopped: list[object] = []
    monkeypatch.setattr(
        runtime_run_module,
        "read_run_process_id",
        lambda *_args: tracked,
    )
    monkeypatch.setattr(
        runtime_run_module,
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
    report = terminal_primary_report(result)
    report_text = report.read_text()
    assert 'completion_reason: "error"' in report_text
    assert "rollback failed" in report_text


def test_refactor_interrupt_during_completion_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """completion 中の中断を joinable state と user interruption report にする。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(
        refactor_module,
        "_initialize_cycle",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )
    original_set_run_state = refactor_module.set_run_state
    interrupted = False

    def interrupt_once(
        context: EditingRunContext,
        run_state: str,
    ) -> SessionState:
        """最初の state 公開だけを中断し、再試行では本来の処理へ戻す。"""
        nonlocal interrupted
        result = original_set_run_state(context, run_state)
        if not interrupted:
            interrupted = True
            signal.raise_signal(signal.SIGINT)
        return result

    monkeypatch.setattr(refactor_module, "set_run_state", interrupt_once)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    assert "- completion_reason: `user_interruption`" in result.output


def test_refactor_with_no_targets_keeps_synchronizing(tmp_path, monkeypatch):
    """空対象でも巡を継続し、ユーザー停止だけで終了する。"""
    _root, _, state_path = _start_session(tmp_path, monkeypatch)
    synchronized = []

    def empty_state(root):
        synchronized.append(root)
        refactor_module.write_refactor_state(root, {})
        return {}

    monkeypatch.setattr(refactor_module, "sync_refactor_state", empty_state)
    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("agent call without a target"),
    )
    _stop_after_cycles(monkeypatch, cycles=2)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 0, result.output
    assert len(synchronized) == 2
    assert _state(state_path)["run"]["state"] == "joinable"
    report = terminal_primary_report(result).read_text()
    assert "- completed cycles: 2" in report
    assert "- cycle targets: 0" in report
    assert "- committed processing units: 0" in report


@pytest.mark.parametrize("change_kind", ["delete", "revert"])
def test_refactor_summary_distinguishes_net_artifacts_from_unit_history(
    tmp_path, monkeypatch, change_kind
):
    """削除は成果に含め、後の巡で戻した変更は net 成果へ数えない。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)
    reviewed = 0

    def review(parameter, **kwargs):
        nonlocal reviewed
        findings = []
        if kwargs["purpose"] == "realization refactor: README.md":
            reviewed += 1
            path = parameter.agent_call_cwd / "README.md"
            if change_kind == "delete":
                path.unlink()
            else:
                path.write_text("changed\n" if reviewed == 1 else "# repo\n")
            findings = [
                {
                    "title": change_kind,
                    "changed_paths": ["README.md"],
                    "resolution": {"status": "fixed", "summary": "confirmed change"},
                }
            ]
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": findings,
                "verification": {"status": "passed", "summary": "full gate passed"},
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", review)
    _stop_after_cycles(monkeypatch, cycles=1 if change_kind == "delete" else 2)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 0, result.output
    run = _state(state_path)["run"]
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    report = terminal_primary_report(result).read_text()
    summary = report.split("## Change summary\n", 1)[1].split("## Test timing", 1)[0]
    if change_kind == "delete":
        assert not (worktree / "README.md").exists()
        assert "- confirmed: delete: fixed: confirmed change" in summary
        assert "`README.md`" in summary
    else:
        assert (worktree / "README.md").read_text() == "# repo\n"
        assert summary.strip() == "- none"
        assert reviewed == 2
    assert "- resolutions:" in report
    assert "full gate passed" in report


@pytest.mark.parametrize("during_commit", [False, True])
def test_refactor_cycle_interruption_respects_state_commit_boundary(
    tmp_path, monkeypatch, during_commit
):
    """巡開始の state 準備は rollback、確定区間の停止要求は記録まで完了する。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)
    _mark_refactor_target_no_findings(root, "README.md")
    if during_commit:
        commit = refactor_module.commit_work_unit

        def commit_then_interrupt(*args, **kwargs):
            result = commit(*args, **kwargs)
            signal.raise_signal(signal.SIGINT)
            return result

        monkeypatch.setattr(refactor_module, "commit_work_unit", commit_then_interrupt)
    else:
        write = refactor_module.write_refactor_state

        def prepare_then_interrupt(*args):
            write(*args)
            signal.raise_signal(signal.SIGINT)

        monkeypatch.setattr(
            refactor_module, "write_refactor_state", prepare_then_interrupt
        )
    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("new call after interruption"),
    )
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 0, result.output
    run = _state(state_path)["run"]
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    state = load_refactor_state(worktree)
    assert state["README.md"]["investigation_required"] is during_commit
    assert state["README.md"]["last_investigation_result"] == "no_findings"
    assert not worktree_change_paths(worktree)
    report = terminal_primary_report(result).read_text()
    assert f"- current cycle: {int(during_commit)}" in report
    assert "- cycle confirmed investigations: 0" in report


@pytest.mark.parametrize("interrupt_next_cycle_start", [False, True])
def test_refactor_repeats_cycles_and_prioritizes_carried_requests(
    tmp_path, monkeypatch, interrupt_next_cycle_start
):
    """旧履歴を調査機会にせず、未解決を次巡で再検討して全対象を公平に処理する。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)
    _mark_refactor_target_no_findings(root, "README.md")
    reviewed = []
    if interrupt_next_cycle_start:
        commit = refactor_module.commit_work_unit
        cycles = 0

        def interrupt_second_cycle(root, message):
            nonlocal cycles
            result = commit(root, message)
            if message == "cmoc realization refactor cycle":
                cycles += 1
                if cycles == 2:
                    signal.raise_signal(signal.SIGINT)
            return result

        monkeypatch.setattr(refactor_module, "commit_work_unit", interrupt_second_cycle)
    else:
        _stop_after_cycles(monkeypatch, cycles=2)

    def review(parameter, **kwargs):
        purpose = kwargs["purpose"]
        assert purpose.startswith("realization refactor: ")
        target = purpose.removeprefix("realization refactor: ")
        reviewed.append(target)
        findings = []
        if target == "README.md" and reviewed.count(target) == 1:
            findings = [
                {
                    "title": "deferred",
                    "changed_paths": [],
                    "resolution": {"status": "unresolved", "summary": "try next cycle"},
                }
            ]
        return SimpleNamespace(
            returncode=0,
            call_log_path=parameter.agent_call_cwd / "call.json",
            output_json={
                "findings": findings,
                "verification": {
                    "status": "not_required",
                    "summary": "no net changes",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", review)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 0, result.output
    run = _state(state_path)["run"]
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    state = load_refactor_state(worktree)
    count = len(state)
    report = terminal_primary_report(result).read_text()
    if interrupt_next_cycle_start:
        assert len(reviewed) == count
        assert "- completed cycles: 1" in report
        assert "- current cycle: 2" in report
        assert "- cycle confirmed investigations: 0" in report
        assert "- cycle deferred targets: 0" in report
        assert "## Unresolved findings\n- `README.md`: deferred" in report
        assert "try next cycle" in report
        return
    assert len(reviewed) == count * 2
    assert set(reviewed[:count]) == set(state) == set(reviewed[count:])
    assert reviewed[count - 1] == reviewed[count] == "README.md"
    assert all(reviewed.count(target) == 2 for target in state)
    assert "- completed cycles: 2" in report
    assert "## Unresolved findings\n- none" in report
    assert "test timing: unavailable" in result.output


def test_refactor_does_not_reselect_related_edits_or_starve_waiting_targets(
    tmp_path, monkeypatch
):
    """関連 file の変更を調査実績へ数えず、追加 file は次巡に公平に処理する。"""
    _root, _, _state_path = _start_session(tmp_path, monkeypatch)
    reviewed = []

    def review(parameter, **kwargs):
        target = kwargs["purpose"].removeprefix("realization refactor: ")
        reviewed.append(target)
        findings = []
        if len(reviewed) == 1:
            assert target == ".gitignore"
            (parameter.agent_call_cwd / "src/new.py").write_text("VALUE = 1\n")
            (parameter.agent_call_cwd / "README.md").write_text("related edit\n")
            findings = [
                {
                    "title": "related changes",
                    "changed_paths": ["src/new.py", "README.md"],
                    "resolution": {"status": "fixed", "summary": "verified edits"},
                }
            ]
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": findings,
                "verification": {"status": "passed", "summary": "full gate passed"},
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", review)
    _stop_after_cycles(monkeypatch, cycles=2)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 0, result.output
    assert reviewed == [
        ".gitignore",
        "README.md",
        "oracle/spec.md",
        "src/new.py",
        ".gitignore",
        "README.md",
        "oracle/spec.md",
    ]
    report = terminal_primary_report(result).read_text()
    assert "- processed targets: 4" in report
    assert "- committed processing units: 7" in report


def test_refactor_latest_resolution_survives_commit_inspection_failure(
    tmp_path, monkeypatch
):
    """確定後の差分確認が失敗しても、最新結果で解消した過去の未解決を復活させない。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)
    reviewed = 0
    inspect = refactor_module.tree_changes

    def review(parameter, **kwargs):
        nonlocal reviewed
        findings = []
        if kwargs["purpose"] == "realization refactor: README.md":
            reviewed += 1
            if reviewed == 1:
                findings = [
                    {
                        "title": "old unresolved finding",
                        "changed_paths": [],
                        "resolution": {"status": "unresolved", "summary": "defer"},
                    }
                ]
        return SimpleNamespace(
            returncode=0,
            call_log_path=parameter.agent_call_cwd / "call.json",
            output_json={
                "findings": findings,
                "verification": {"status": "not_required", "summary": "no edits"},
            },
        )

    def failed_unit_inspection(*args):
        if reviewed == 2 and len(args) == 3:
            raise RuntimeError("committed unit inspection failed")
        return inspect(*args)

    monkeypatch.setattr(refactor_module, "run_codex_exec", review)
    monkeypatch.setattr(refactor_module, "tree_changes", failed_unit_inspection)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 1, result.output
    run = _state(state_path)["run"]
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    assert (
        load_refactor_state(worktree)["README.md"]["last_investigation_result"]
        == "no_findings"
    )
    assert not worktree_change_paths(worktree)
    report = terminal_primary_report(result).read_text()
    assert "## Unresolved findings\n- none" in report
    assert "committed unit inspection failed" in report


@pytest.mark.parametrize(
    "verification_status", ["failed", "incomplete", "not_required"]
)
def test_refactor_rejects_unverified_changes(
    tmp_path, monkeypatch, verification_status
):
    """構文上は妥当な出力でも品質検証が成功していない変更を確定しない。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)
    calls = []

    def review(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        (parameter.agent_call_cwd / "README.md").write_text("unverified change\n")
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [
                    {
                        "title": "change",
                        "changed_paths": ["README.md"],
                        "resolution": {"status": "fixed", "summary": "changed"},
                    }
                ],
                "verification": {
                    "status": verification_status,
                    "summary": "gate not passed",
                },
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", review)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 1
    run = _state(state_path)["run"]
    assert run["state"] == "error"
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    assert (worktree / "README.md").read_text() == "# repo\n"
    assert not worktree_change_paths(worktree)
    assert len(calls) == 1
    assert "品質検証が完了していません" in terminal_primary_report(result).read_text()


def test_refactor_stop_failure_preserves_uncommitted_work(tmp_path, monkeypatch):
    """子の停止を確認できなければ rollback と joinable 公開を行わない。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)

    def interrupted_review(parameter, **kwargs):
        (parameter.agent_call_cwd / "README.md").write_text("still owned by child\n")
        raise KeyboardInterrupt

    monkeypatch.setattr(refactor_module, "run_codex_exec", interrupted_review)
    monkeypatch.setattr(
        refactor_module,
        "stop_tracked_codex_children",
        lambda *_args: (_ for _ in ()).throw(RuntimeError("stop unavailable")),
    )
    monkeypatch.setattr(
        refactor_module,
        "rollback_work_unit",
        lambda *_args: pytest.fail("rollback before stop confirmation"),
    )
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 1
    run = _state(state_path)["run"]
    assert run["state"] == "error"
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    assert (worktree / "README.md").read_text() == "still owned by child\n"
    report = terminal_primary_report(result).read_text()
    assert "rollback not attempted" in report
    assert "observed uncommitted paths" in report
    assert "  - `README.md`" in report
    assert "停止と未確定差分の解消を確認してから" in result.output


def test_refactor_interrupted_agent_commit_rolls_back_remaining_untracked_files(
    tmp_path, monkeypatch
):
    """agent の禁止 commit を除去した後も、未確定の追加 file を残さない。"""
    root, _, state_path = _start_session(tmp_path, monkeypatch)

    def interrupted_review(parameter, **_kwargs):
        worktree = parameter.agent_call_cwd
        (worktree / "README.md").write_text("forbidden commit\n")
        run_git(worktree, "add", "README.md")
        run_git(worktree, "commit", "-m", "forbidden agent commit")
        (worktree / "src/untracked.py").write_text("VALUE = 1\n")
        signal.raise_signal(signal.SIGINT)

    monkeypatch.setattr(refactor_module, "run_codex_exec", interrupted_review)
    result = runner.invoke(
        app, ["realization", "refactor", "fork"], catch_exceptions=False
    )
    assert result.exit_code == 1, result.output
    run = _state(state_path)["run"]
    assert run["state"] == "error"
    worktree = root / ".cmoc/gu/worktree" / Path(*run["branch"].split("/")[2:])
    assert (worktree / "README.md").read_text() == "# repo\n"
    assert not (worktree / "src/untracked.py").exists()
    assert not worktree_change_paths(worktree)
    assert (
        "forbidden agent commit" not in run_git(worktree, "log", "--format=%s").stdout
    )
    report = terminal_primary_report(result).read_text()
    assert "- committed processing units: 0" in report
    assert "uncommitted work rolled back" in report
