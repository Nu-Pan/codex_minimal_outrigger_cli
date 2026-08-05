"""workload fork と共通 run join/abandon の統合 realization test。

この file は 16,000 文字を超えるが、editing run の session state、run worktree、
fork report、および join/abandon は同じ lifecycle fixture を共有する。分割すると、
同じ branch・state 遷移の準備と検証を複数 file で重複させるため、一続きに保つ。
"""

import json
import os
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace
from typing import NoReturn

import pytest
from _cli_support import run_doctor, runner
from _codex_support import setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import current_branch, make_repo, run_git

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
import commons.runtime_codex_profile as codex_profile_module
import commons.runtime_run as runtime_run_module
import commons.runtime_run_lifecycle as lifecycle_module
import commons.runtime_run_report as run_report_module
import sub_commands.realization.apply.fork as apply_module
import sub_commands.realization.refactor.fork as refactor_module
import sub_commands.run.abandon as run_abandon_module
import sub_commands.run.join as run_join_module
import sub_commands.run.lifecycle as legacy_lifecycle_module
from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_content import file_sha256
from commons.runtime_errors import CmocError
from commons.runtime_paths import timestamp
from commons.runtime_refactor import load_refactor_state
from commons.runtime_run import run_process_id_path
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    raw_oracle_diff,
    set_run_state,
    start_editing_run,
    worktree_change_paths,
)
from commons.runtime_state import SessionState
from main import app


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


def test_refactor_rejects_empty_refactor_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """対象 file のない cycle を natural completion にしない。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path,
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="fork",
        kind="realization_refactor",
        run_branch="cmoc/run/session/run",
        run_fork_commit="fork",
        run_worktree=tmp_path,
    )
    monkeypatch.setattr(refactor_module, "sync_refactor_state", lambda _root: {})

    with pytest.raises(CmocError, match="対象 file がありません"):
        refactor_module._initialize_cycle(context)


def test_refresh_indexes_does_not_change_process_cwd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """明示 worktree の INDEX 更新で process-global cwd を変更しない。"""
    root = make_repo(tmp_path)
    caller = tmp_path.resolve()
    monkeypatch.chdir(caller)
    observed: list[Path] = []

    def fake_update_indexes(worktree: Path, _codex_exec: object) -> list[Path]:
        """対象 worktree と呼び出し時の process cwd を記録する。"""
        observed.append(Path.cwd().resolve())
        assert worktree == root
        return []

    monkeypatch.setattr(lifecycle_module, "update_indexes", fake_update_indexes)

    lifecycle_module.refresh_indexes(root, commit=False)

    assert observed == [caller]
    assert Path.cwd().resolve() == caller


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


def test_raw_oracle_diff_treats_changed_paths_as_literal_pathspecs(
    tmp_path: Path,
) -> None:
    """oracle path の glob 文字を raw diff の pathspec として解釈しない。"""
    root = make_repo(tmp_path)
    special_path = root / "oracle" / "spec[1].md"
    base = run_git(root, "rev-parse", "HEAD").stdout.strip()
    special_path.write_text("after\n")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-m", "add special oracle path")
    end = run_git(root, "rev-parse", "HEAD").stdout.strip()

    diff = raw_oracle_diff(root, base, end)

    assert "oracle/spec[1].md" in diff
    assert "+after" in diff


def test_raw_oracle_diff_excludes_oracle_gitlinks(
    tmp_path: Path,
) -> None:
    """oracle file ではない Gitlink を raw diff に含めない。"""
    root = make_repo(tmp_path)
    gitlink = root / "oracle" / "gitlink"
    gitlink.mkdir()
    base = run_git(root, "rev-parse", "HEAD").stdout.strip()
    commit = base
    run_git(
        root,
        "update-index",
        "--add",
        "--cacheinfo",
        f"160000,{commit},oracle/gitlink",
    )
    run_git(root, "commit", "-m", "add oracle gitlink")
    end = run_git(root, "rev-parse", "HEAD").stdout.strip()

    assert raw_oracle_diff(root, base, end) == ""


def test_run_reports_keep_distinct_files_on_timestamp_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同一 timestamp の fork/lifecycle report を相互に上書きしない。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path,
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
        run_fork_commit="run-fork",
        run_worktree=tmp_path,
    )
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    monkeypatch.setattr(run_report_module, "timestamp", lambda: next(timestamps))

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

    assert [path.stem for path in fork_paths] == [
        "2026-06-27_10-00_00_000001000",
        "2026-06-27_10-00_00_000002000",
    ]
    assert [path.stem for path in lifecycle_paths] == [
        "2026-06-27_10-00_00_000001000",
        "2026-06-27_10-00_00_000002000",
    ]
    assert all(
        f'generated_at: "{path.stem}"' in path.read_text()
        for path in [*fork_paths, *lifecycle_paths]
    )


def test_fork_report_escapes_special_changed_paths(tmp_path: Path) -> None:
    """変更 path の Markdown code span と行構造を壊さない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path,
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
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


def test_new_run_target_skips_dangling_worktree_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """dangling symlink を空き run worktree として再利用しない。"""
    root = make_repo(tmp_path)
    collision_id = "2026-06-27_10-00_00_000001000"
    free_id = "2026-06-27_10-00_00_000002000"
    collision = root / ".cmoc" / "gu" / "worktree" / "session" / collision_id
    collision.parent.mkdir(parents=True)
    collision.symlink_to(tmp_path / "missing-run-worktree", target_is_directory=True)
    target_ids = iter([collision_id, free_id])
    monkeypatch.setattr(lifecycle_module, "timestamp", lambda: next(target_ids))

    branch, worktree = lifecycle_module.new_run_target(root, "session")

    assert branch == f"cmoc/run/session/{free_id}"
    assert worktree == root / ".cmoc" / "gu" / "worktree" / "session" / free_id
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
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)

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


def test_apply_rejects_agent_index_change_before_index_refresh(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply agent が INDEX.md を変更した場合は cmoc 更新前に拒否する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    refresh_calls = 0

    def fake_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """apply agent が INDEX.md を変更した状態を再現する。"""
        worktree = parameter.agent_call_cwd
        assert "cwd" not in kwargs
        index_path = worktree / "INDEX.md"
        index_path.write_text("agent change\n")
        return SimpleNamespace(returncode=0, output_json=None)

    def fail_refresh(_worktree: Path, *, commit: bool) -> list[Path]:
        """agent の禁止差分検査前に INDEX 更新へ進まないことを確認する。"""
        nonlocal refresh_calls
        refresh_calls += 1
        raise AssertionError("INDEX refresh must not run")

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    monkeypatch.setattr(apply_module, "refresh_indexes", fail_refresh)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert refresh_calls == 0
    state = _state(state_path)
    assert state["run"]["state"] == "error"
    parts = state["run"]["branch"].split("/")
    run_worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert not (run_worktree / "INDEX.md").exists()


def test_apply_rejects_agent_commit_and_rolls_back_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply agent の commit が処理単位をすり抜けず、開始 HEAD へ戻る。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)

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


@pytest.mark.parametrize("unexpected_path", ["oracle/unexpected.md", "README.md"])
def test_apply_rejects_unexpected_refresh_change_before_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    unexpected_path: str,
) -> None:
    """INDEX refresh の想定外差分を run commit に含めない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)

    def fake_apply(
        _parameter: AgentCallParameter,
        **_kwargs: object,
    ) -> SimpleNamespace:
        """apply agent の正常終了を再現する。"""
        return SimpleNamespace(returncode=0, output_json=None)

    def fake_refresh(worktree: Path, *, commit: bool) -> list[Path]:
        """INDEX 更新処理が誤って管理外 file を変更した状態を再現する。"""
        assert not commit
        (worktree / unexpected_path).write_text("unexpected\n")
        return []

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    monkeypatch.setattr(apply_module, "refresh_indexes", fake_refresh)

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
    restored = run_worktree / unexpected_path
    assert restored.exists() is (unexpected_path == "README.md")
    if unexpected_path == "README.md":
        assert restored.read_text() == "# repo\n"


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
        calls.append((parameter, worktree))
        (worktree / "README.md").write_text("# repo\n\nrealized\n")
        return SimpleNamespace(returncode=0, output_json=None)

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)
    joined_process_stops: list[tuple[Path, str]] = []
    monkeypatch.setattr(
        run_join_module,
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
    report_path = Path(
        next(
            line
            for line in joined.output.splitlines()
            if line.startswith("- report: `")
        )
        .removeprefix("- report: `")
        .removesuffix("`")
    )
    report_text = report_path.read_text()
    assert "session.last_joined_apply_fork_commit=" not in report_text
    assert current_branch(root) == session_branch


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
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)
    monkeypatch.setattr(
        run_join_module,
        "stop_tracked_codex_children",
        lambda *_args: ["run child process already stopped: 789"],
    )

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    report_path = Path(
        next(
            line
            for line in result.output.splitlines()
            if line.startswith("- report: `")
        )
        .removeprefix("- report: `")
        .removesuffix("`")
    )
    assert "run child process already stopped: 789" in report_path.read_text()


def test_run_join_tracks_indexing_codex_calls_and_stops_children_after_refresh(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """join 後の INDEX 用 Codex child を追跡し、refresh 後に停止する。"""
    _root, _session_branch, _state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    events: list[tuple[str, bool]] = []

    def fake_refresh(_worktree: Path, *, commit: bool) -> list[Path]:
        """INDEX refresh 中の tracking 状態を記録する。"""
        assert commit
        events.append(("refresh", codex_profile_module.run_process_tracking_active()))
        return []

    def record_stop(*_args: object) -> list[str]:
        """tracked child 停止位置と tracking 状態を記録する。"""
        events.append(("stop", codex_profile_module.run_process_tracking_active()))
        return []

    monkeypatch.setattr(run_join_module, "refresh_indexes", fake_refresh)
    monkeypatch.setattr(run_join_module, "stop_tracked_codex_children", record_stop)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert events == [("stop", False), ("refresh", True), ("stop", True)]


def test_run_join_rejects_index_refresh_side_effect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """INDEX refresh の管理外差分を state sync commit へ混入させない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")

    def fake_refresh(worktree: Path, *, commit: bool) -> list[Path]:
        """INDEX builder の管理外 file 副作用を再現する。"""
        assert commit
        (worktree / "index-side-effect.txt").write_text("unexpected\n")
        return []

    monkeypatch.setattr(run_join_module, "refresh_indexes", fake_refresh)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    assert not (root / "index-side-effect.txt").exists()
    assert (root / "README.md").read_text() == "# repo\n"


def test_apply_builder_uses_call_scoped_run_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """process cwd を変えずに parameter と prompt が run worktree を共有する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_builder = apply_module.build_realization_apply_fork_launch_exec_parameter
    observed: list[tuple[Path, Path, Path, str]] = []

    def capture_builder(
        diff_base_commit: str,
        run_fork_commit: str,
        raw_oracle_git_diff: str,
        run_worktree: Path,
    ) -> AgentCallParameter:
        """builder 構築時の process cwd、agent call cwd、prompt を記録する。"""
        parameter = original_builder(
            diff_base_commit,
            run_fork_commit,
            raw_oracle_git_diff,
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
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)

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
    reports = list(
        (root / ".cmoc" / "gu" / "ar" / "report" / "run" / "abandon").glob("*.md")
    )
    assert len(reports) == 1
    assert "run worktree was already absent" in reports[0].read_text()


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
    reports = list(
        (root / ".cmoc" / "gu" / "ar" / "report" / "run" / "abandon").glob("*.md")
    )
    assert len(reports) == 1
    assert "run child process already stopped: 789" in reports[0].read_text()


def test_run_abandon_rejects_dangling_worktree_link_after_removal_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """削除失敗後に残った dangling symlink を cleanup 完了と扱わない。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path / "session",
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
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


def test_apply_fork_tracks_indexing_codex_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply の INDEX 再生成中も Codex child tracking を有効にする。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    tracking_states: list[bool] = []

    def fake_apply(
        _parameter: AgentCallParameter,
        **_kwargs: object,
    ) -> SimpleNamespace:
        """apply agent の正常終了を再現する。"""
        return SimpleNamespace(returncode=0, output_json=None)

    def fake_refresh(_worktree: Path, *, commit: bool) -> list[Path]:
        """INDEX 更新時の process tracking 状態を記録する。"""
        assert not commit
        tracking_states.append(codex_profile_module.run_process_tracking_active())
        return []

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_apply)
    monkeypatch.setattr(apply_module, "refresh_indexes", fake_refresh)

    result = runner.invoke(
        app,
        ["realization", "apply", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    assert tracking_states == [True]


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
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)

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
    monkeypatch.setattr(apply_module, "refresh_indexes", _no_index_refresh)
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
        (
            root / ".cmoc" / "gu" / "ar" / "report" / "realization" / "apply" / "fork"
        ).glob("*.md")
    )
    assert len(reports) == 1
    assert "run child process already stopped: 789" in reports[0].read_text()


def test_refactor_fork_tracks_initialization_indexing_codex_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor の初期 cycle から INDEX 用 Codex child tracking を有効にする。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    tracking_states: list[bool] = []

    def fake_refresh(_worktree: Path, *, commit: bool) -> list[Path]:
        """初期 cycle と各処理単位の tracking 状態を記録する。"""
        assert not commit
        tracking_states.append(codex_profile_module.run_process_tracking_active())
        return []

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """file review と change summary の固定 Structured Output を返す。"""
        if kwargs["purpose"] == "realization refactor change summary":
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
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "refresh_indexes", fake_refresh)
    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert _state(state_path)["run"]["state"] == "joinable"
    assert tracking_states and all(tracking_states)


def test_refactor_fork_stops_tracked_children_before_each_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor は cycle と各処理単位の commit 前に Codex child を停止する。"""
    _root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
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
        """file review と change summary の固定 Structured Output を返す。"""
        if kwargs["purpose"] == "realization refactor change summary":
            return SimpleNamespace(
                returncode=0,
                output_json={"changes": [{"category": "state", "summary": "更新"}]},
            )
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "stop_tracked_codex_children", record_stop)
    monkeypatch.setattr(refactor_module, "commit_work_unit", record_commit)
    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

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
    assert all(index > 0 and events[index - 1] == "stop" for index in commit_positions)


def test_refactor_fork_reports_cleanup_warnings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor fork の child 停止 warning を fork report に保存する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

    def fake_refactor(
        _parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """file review と change summary の固定 Structured Output を返す。"""
        if kwargs["purpose"] == "realization refactor change summary":
            return SimpleNamespace(
                returncode=0,
                output_json={"changes": [{"category": "state", "summary": "更新"}]},
            )
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
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
        (
            root
            / ".cmoc"
            / "gu"
            / "ar"
            / "report"
            / "realization"
            / "refactor"
            / "fork"
        ).glob("*.md")
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
    monkeypatch.setattr(refactor_module, "_initialize_cycle", lambda _context: None)
    monkeypatch.setattr(
        refactor_module,
        "select_refactor_target",
        lambda *_args: None,
    )
    monkeypatch.setattr(
        refactor_module,
        "_completion_reason",
        lambda *_args: "natural_completion",
    )
    monkeypatch.setattr(
        refactor_module,
        "_completion_change_summary",
        lambda *_args: None,
    )

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert stopped == [child]
    assert _state(state_path)["run"]["state"] == "joinable"


@pytest.mark.parametrize("replace_content", [False, True])
def test_refactor_fork_moves_unresolved_target_after_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replace_content: bool,
) -> None:
    """rename 後も unresolved target と refactor state の path 集合を揃える。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

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
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "findings": [
                        {
                            "title": "deferred",
                            "changed_paths": ["README.md", "renamed.md"],
                            "resolution": {
                                "status": "unresolved",
                                "summary": "needs follow-up",
                            },
                        }
                    ]
                },
                call_log_path=worktree / "README-call.json",
            )
        if kwargs["purpose"] == "realization refactor change summary":
            return SimpleNamespace(
                returncode=0,
                output_json={
                    "changes": [{"category": "rename", "summary": "README renamed"}]
                },
            )
        return SimpleNamespace(
            returncode=0,
            output_json={"findings": []},
            call_log_path=worktree / "call.json",
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

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
        (
            root
            / ".cmoc"
            / "gu"
            / "ar"
            / "report"
            / "realization"
            / "refactor"
            / "fork"
        ).glob("*.md")
    )
    assert len(reports) == 1
    report = reports[0].read_text()
    assert "## Completion\ncompleted_with_unresolved" in report
    assert "## Unresolved targets\n- count: 1\n- paths:\n  - `renamed.md`" in report


@pytest.mark.parametrize(
    "managed_path",
    ["INDEX.md", ".cmoc/gt/ar/realization/refactor/state.json"],
)
def test_refactor_rejects_agent_changes_to_cmoc_managed_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    managed_path: str,
) -> None:
    """refactor agent が cmoc 管理 file を変更した場合は commit しない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """agent が INDEX または refactor state を変更する状態を再現する。"""
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
                ]
            },
        )

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

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
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
    first_review = True

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """evidences には全差分を載せ、changed_paths では一部だけ申告する。"""
        nonlocal first_review
        purpose = str(kwargs["purpose"])
        if purpose == "realization refactor change summary":
            return SimpleNamespace(
                returncode=0,
                output_json={"changes": [{"category": "state", "summary": "更新"}]},
            )
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
                ]
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
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

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
        {"findings": [{"changed_paths": ["README.md"]}]},
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
            ]
        },
        frozenset({"README.md", "added.py"}),
    )

    assert not issues


def test_refactor_rejects_agent_commit_and_rolls_back_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """refactor agent の commit が処理単位をすり抜けず、開始 HEAD へ戻る。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """agent が realization file を直接 commit する状態を再現する。"""
        worktree = parameter.agent_call_cwd
        (worktree / "README.md").write_text("agent commit\n")
        run_git(worktree, "add", "README.md")
        run_git(worktree, "commit", "-m", "agent commit")
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

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


def test_apply_failure_rolls_back_index_with_realization_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """apply 失敗時に realization 差分と生成 INDEX を同時に戻す。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    calls: list[bool] = []
    before_index: str | None = None

    def fake_apply(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """apply agent の代わりに差分と rollback 前の INDEX を作る。"""
        nonlocal before_index
        worktree = parameter.agent_call_cwd
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
        (
            root / ".cmoc" / "gu" / "ar" / "report" / "realization" / "apply" / "fork"
        ).glob("*.md")
    )
    assert len(reports) == 1
    assert "change inspection failed" in reports[0].read_text()


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
def test_refactor_terminal_report_survives_change_inspection_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupted: bool,
) -> None:
    """差分確認に失敗しても refactor の terminal report と state を保存する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

    def fail_agent(*_args: object, **_kwargs: object) -> NoReturn:
        """agent failure または user interruption を再現する。"""
        if interrupted:
            raise KeyboardInterrupt()
        raise RuntimeError("agent failed")

    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        fail_agent,
    )
    monkeypatch.setattr(
        refactor_module,
        "tree_changes",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            RuntimeError("git diff unavailable")
        ),
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
        (
            root
            / ".cmoc"
            / "gu"
            / "ar"
            / "report"
            / "realization"
            / "refactor"
            / "fork"
        ).glob("*.md")
    )
    assert len(reports) == 1
    report_text = reports[0].read_text()
    assert "change inspection failed" in report_text
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


def test_refactor_cmoc_start_error_does_not_recover_competing_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """並行 start の CmocError で別 invocation の run を error にしない。"""
    root, session_branch, state_path = _start_session(tmp_path, monkeypatch)
    original_start = refactor_module.start_editing_run

    def competing_start(kind: str) -> EditingRunContext:
        """別 invocation が lock 内で run を公開した後の競合を再現する。"""
        original_start(kind)
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

    assert result.exit_code == 1
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
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)

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
        "branch": "cmoc/run/another-session/run-id",
        "fork_commit": state["session"]["session_fork_commit"],
    }
    state_path.write_text(json.dumps(state, indent=2) + "\n")

    with pytest.raises(CmocError, match="branch が session state と一致しません"):
        lifecycle_module.resolve_active_run({"running"})


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
    assert not (root / unexpected_path).exists()
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
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)

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
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
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
    cleanup = run_join_module._cleanup_joined_run(context, warnings)

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
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
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
    cleanup = run_join_module._cleanup_joined_run(context, warnings)

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
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
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
    cleanup = run_join_module._cleanup_joined_run(context, warnings)

    assert cleanup == "branch_preserved"
    assert deleted == [context.run_branch]
    assert warnings == ["run branch cleanup failed"]


def test_run_join_resolves_deleted_session_index_conflict(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session 側で削除された INDEX.md の conflict を再生成可能な状態にする。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    index_path = root / "INDEX.md"
    index_path.write_text("base index\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    context = start_editing_run("realization_apply")
    (context.run_worktree / "INDEX.md").write_text("run index\n")
    commit_work_unit(context.run_worktree, "run index change")
    set_run_state(context, "joinable")
    index_path.unlink()
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "delete session index")
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert not index_path.exists()
    assert _state(state_path)["run"]["state"] == "ready"


def test_run_join_conflict_abort_failure_still_restores_session_tree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """merge --abort の失敗時も join 開始前の clean tree へ戻す。"""
    context = EditingRunContext(
        repo=tmp_path,
        session_worktree=tmp_path / "session",
        session_id="session",
        state_path=tmp_path / "state.json",
        session_branch="cmoc/session/session",
        session_fork_commit="session-fork",
        kind="realization_apply",
        run_branch="cmoc/run/session/run",
        run_fork_commit="run-fork",
        run_worktree=tmp_path / "run",
    )
    state = SessionState()
    commands: list[list[str]] = []

    def fake_run_git(
        args: list[str],
        _cwd: Path,
        check: bool = True,
    ) -> SimpleNamespace:
        """join rollback の分岐を確認するための Git 実行結果を返す。"""
        commands.append(args)
        if args[:2] == ["diff", "--name-only"]:
            return SimpleNamespace(returncode=0, stdout="README.md\0")
        if args[:2] == ["rev-parse", "-q"]:
            return SimpleNamespace(returncode=0, stdout="")
        if args == ["merge", "--abort"]:
            return SimpleNamespace(returncode=1, stdout="")
        return SimpleNamespace(returncode=0, stdout="")

    report = tmp_path / "report.md"
    monkeypatch.setattr(run_join_module, "run_git", fake_run_git)
    monkeypatch.setattr(
        run_join_module,
        "write_state",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        run_join_module,
        "write_lifecycle_report",
        lambda *_args, **_kwargs: report,
    )

    with pytest.raises(CmocError, match="INDEX.md 以外"):
        run_join_module._resolve_index_only_conflict_or_fail(
            context,
            state,
            [],
            "session-head-before-join",
        )

    assert ["reset", "--hard", "session-head-before-join"] in commands
    assert ["clean", "-fd"] in commands


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


def test_run_join_keeps_completed_merge_when_final_report_update_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """cleanup 後の report 更新失敗で完了済み merge を rollback しない。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    context = start_editing_run("realization_apply")
    (context.run_worktree / "README.md").write_text("realized\n")
    commit_work_unit(context.run_worktree, "run change")
    set_run_state(context, "joinable")
    monkeypatch.setattr(run_join_module, "refresh_indexes", _no_index_refresh)
    original_write_report = run_join_module.write_lifecycle_report

    def fail_final_report(
        report_context: EditingRunContext,
        operation: str,
        **kwargs: object,
    ) -> Path:
        """final report rewrite だけの失敗を再現する。"""
        if kwargs.get("report_path") is not None:
            raise RuntimeError("final report update failed")
        return original_write_report(report_context, operation, **kwargs)

    monkeypatch.setattr(run_join_module, "write_lifecycle_report", fail_final_report)

    result = runner.invoke(app, ["run", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert (root / "README.md").read_text() == "realized\n"
    assert "final join report update failed" in result.output
    assert _state(state_path)["run"]["state"] == "ready"
    assert not context.run_worktree.exists()
    assert not run_git(root, "branch", "--list", context.run_branch).stdout.strip()
    report = next(
        root.joinpath(".cmoc", "gu", "ar", "report", "run", "join").glob("*.md")
    )
    assert 'cleanup: "pending"' in report.read_text()


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
        parameter: AgentCallParameter,
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
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
    assert "- `README.md`: 0 finding(s)" in report.read_text()


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
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: ").strip("`"))
    assert 'completion_reason: "error"' in report.read_text()
    assert 'state_before: "ready"' in report.read_text()


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
                            "changed_paths": [],
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
        parameter: AgentCallParameter,
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
                worktree = parameter.agent_call_cwd
                (worktree / "README.md").write_text("# repo\n\nfixed\n")
                return SimpleNamespace(
                    returncode=0,
                    output_json={
                        "findings": [
                            {
                                "title": "README finding",
                                "changed_paths": ["README.md"],
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


@pytest.mark.parametrize("rogue_refresh_call", [1, 2])
def test_refactor_rejects_realization_change_added_by_index_refresh(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    rogue_refresh_call: int,
) -> None:
    """INDEX refresh 後に増えた realization 差分を commit しない。

    根拠: {{work-root}}/oracle/doc/app_spec/indexing.md
    {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    """
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    refresh_calls = 0

    def fake_refresh(worktree: Path, *, commit: bool) -> list[Path]:
        """初期化後の INDEX refresh が管理外 realization を作る状態を再現する。"""
        nonlocal refresh_calls
        assert not commit
        refresh_calls += 1
        if refresh_calls == rogue_refresh_call:
            (worktree / "refresh-created.py").write_text("unexpected\n")
        return []

    def fake_refactor(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> SimpleNamespace:
        """対象 realization file だけを変更して fixed finding を返す。"""
        purpose = str(kwargs["purpose"])
        if purpose == "realization refactor change summary":
            raise AssertionError("change summary must not run after invalid unit")
        target = purpose.removeprefix("realization refactor: ")
        worktree = parameter.agent_call_cwd
        target_path = worktree / target
        if target_path.is_file():
            target_path.write_text(target_path.read_text() + "fixed\n")
        return SimpleNamespace(
            returncode=0,
            output_json={
                "findings": [
                    {
                        "title": "target finding",
                        "changed_paths": [target] if target_path.is_file() else [],
                        "resolution": {"status": "fixed"},
                    }
                ]
            },
        )

    monkeypatch.setattr(refactor_module, "refresh_indexes", fake_refresh)
    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)

    result = runner.invoke(
        app,
        ["realization", "refactor", "fork"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert _state(state_path)["run"]["state"] == "error"
    parts = _state(state_path)["run"]["branch"].split("/")
    worktree = root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
    assert not (worktree / "refresh-created.py").exists()


def test_refactor_interrupt_rolls_back_current_unit_and_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """current refactor unit の中断時に差分を戻して joinable にする。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

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
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
    assert 'completion_reason: "user_interruption"' in report.read_text()
    assert "- completion_reason: `user_interruption`" in result.output
    assert "- unresolved targets: `0`" in result.output
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    events = [
        json.loads(line)
        for path in (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob(
            "*.jsonl"
        )
        for line in path.read_text().splitlines()
    ]
    completion = next(event for event in events if event["event"] == "fork_completed")
    assert completion["completion_reason"] == "user_interruption"
    assert completion["unresolved_target_count"] == 0
    assert completion["report_path"] == str(report.resolve())


def test_refactor_interrupt_during_indexing_preflight_is_joinable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """agent 境界前の indexing commit と中断でも joinable にする。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)

    def interrupting_preflight(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> NoReturn:
        """before_agent_call callback 前の indexing commit と中断を再現する。"""
        worktree = parameter.agent_call_cwd
        (worktree / "README.md").write_text("preflight-only\n")
        run_git(worktree, "add", "README.md")
        run_git(worktree, "commit", "-m", "cmoc indexing")
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        refactor_module,
        "run_codex_exec",
        interrupting_preflight,
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
    assert (
        "cmoc indexing"
        not in run_git(run_worktree, "log", "--format=%s").stdout.splitlines()
    )
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
    assert 'completion_reason: "user_interruption"' in report.read_text()


def test_refactor_interrupt_after_unit_commit_reports_confirmed_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """処理単位の commit 後に中断しても確定済み進捗を report する。"""
    root, _session_branch, state_path = _start_session(tmp_path, monkeypatch)
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
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
                    ]
                },
            )
        return SimpleNamespace(returncode=0, output_json={"findings": []})

    original_commit = refactor_module.commit_work_unit

    def commit_then_interrupt(
        worktree: Path,
        message: str,
        **kwargs: object,
    ) -> str | None:
        """README の処理単位を commit した直後に中断する。"""
        result = original_commit(worktree, message, **kwargs)
        if message == "cmoc realization refactor README.md":
            raise KeyboardInterrupt()
        return result

    monkeypatch.setattr(refactor_module, "run_codex_exec", fake_refactor)
    monkeypatch.setattr(refactor_module, "commit_work_unit", commit_then_interrupt)

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
    report_line = next(
        line
        for line in result.output.splitlines()
        if line.startswith("- fork report: `")
    )
    report = Path(report_line.removeprefix("- fork report: `").removesuffix("`"))
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
    monkeypatch.setattr(refactor_module, "refresh_indexes", _no_index_refresh)
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
    assert stopped == [child, child]
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
