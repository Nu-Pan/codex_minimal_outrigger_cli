"""apply fork CLI の lifecycle、state、gitignore 挙動を検証する回帰テスト。

対象正規化は CLI lifecycle や repository fixture を必要としないため、独立した test
module に分けている。実行順は
{{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md.

この file は 16,000 文字を超えるが、各 scenario は同じ repository/session fixture と apply
state/worktree context を共有するため、分割すると自然な責務境界なしに lifecycle の読解
context が分散する。このサイズ判断は
{{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py.
"""

import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from _apply_support import apply_worktree_from_state
from _cli_support import runner
from _codex_support import FakeCodexResult
from _git_support import make_repo, run_git
from _ollama_support import run_doctor
from pytest import MonkeyPatch

import commons.runtime_cli as runtime_cli_module
import sub_commands.apply.fork as apply_fork_module
from basic.acp import AgentCallParameter
from cmoc_runtime import CmocError
from main import app


def test_apply_fork_runs_codex_loop_and_updates_state(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork が Codex loop 後に state と worktree を完成状態へ更新する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    doctor_result = run_doctor(root)
    assert doctor_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """apply fork の Codex 呼び出し順を記録し、空所見を返す。"""
        calls.append(str(kwargs["purpose"]))
        if parameter.structured_output_schema_path is None:
            return FakeCodexResult(None)
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads(
        (root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json").read_text()
    )
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "gu" / "worktree" / session_id / run_id
    assert apply_worktree.is_dir()
    assert (
        run_git(apply_worktree, "branch", "--show-current").stdout.strip()
        == state["apply"]["apply_branch"]
    )
    assert not (root / ".cmoc" / "gu" / "worktree" / "apply").exists()
    assert "apply_worktree" not in state["apply"]
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "gu" / "ar" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert calls
    assert any(call.startswith("apply fork review and fix") for call in calls)


def test_apply_fork_interrupt_keeps_commits_and_discards_current_unit(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """Ctrl+C で確定済み commit を保ち、実行中単位の未確定差分を捨てる。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    review_calls = 0
    purposes: list[str] = []

    def interrupting_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """1 単位を確定後、次のレビュー・修正中に割り込む。"""
        nonlocal review_calls
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        if purpose.startswith("apply fork review and fix"):
            review_calls += 1
            worktree = Path(kwargs["cwd"])
            target = (
                worktree / "src" / ("kept.py" if review_calls == 1 else "discarded.py")
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"value = {review_calls}\n")
            if review_calls == 2:
                raise KeyboardInterrupt
            return FakeCodexResult(
                {
                    "findings": [
                        {
                            "title": f"finding {review_calls}",
                            "reason": "test interruption",
                        }
                    ]
                }
            )
        raise AssertionError(f"interruption 後に開始された Codex call: {purpose}")

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        interrupting_codex_exec,
    )

    result = runner.invoke(
        app,
        ["apply", "fork", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 2
    assert "# ERROR" not in result.output
    assert "ユーザー中断要求" in result.output
    session_id = (
        run_git(root, "branch", "--show-current")
        .stdout.strip()
        .removeprefix("cmoc/session/")
    )
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    apply_worktree = apply_worktree_from_state(root, state)
    assert (apply_worktree / "src" / "kept.py").is_file()
    assert not (apply_worktree / "src" / "discarded.py").exists()
    assert run_git(apply_worktree, "status", "--short").stdout == ""
    assert (
        "src/kept.py"
        in run_git(
            apply_worktree,
            "show",
            "--name-only",
            "--format=",
            "HEAD",
        ).stdout.splitlines()
    )
    reports = sorted(
        (root / ".cmoc" / "gu" / "ar" / "report" / "apply" / "fork").glob("*.md")
    )
    assert reports
    rendered = reports[-1].read_text()
    assert "result: unconverged" in rendered
    assert "ユーザー中断要求を受け付けたため" in rendered
    assert "apply fork change summary" not in purposes
    assert not (
        root / ".cmoc" / "gu" / "ar" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    logs = sorted(
        (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    )
    assert '"event": "user_interruption"' in logs[-1].read_text()


def test_apply_fork_uses_linked_worktree_branch_and_head(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """linked worktree 上の session branch と HEAD から apply run を開始する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-apply"
    run_git(root, "worktree", "add", "-b", "linked-apply-home", str(linked), "HEAD")
    (linked / "README.md").write_text("# linked apply\n")
    run_git(linked, "add", "README.md")
    run_git(linked, "commit", "-m", "linked apply change")
    linked_commit = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    start_points: list[str] = []
    original_create_run_worktree = apply_fork_module.create_run_worktree

    def advance_session_before_run_creation(
        root_arg: Path, branch_arg: str, worktree: Path, start_point: str
    ) -> Path:
        """snapshot 後に session branch が進んでも、渡した起点を観測する。"""
        (linked / "README.md").write_text("# session advanced\n")
        run_git(linked, "add", "README.md")
        run_git(linked, "commit", "-m", "advance session during apply setup")
        start_points.append(start_point)
        return original_create_run_worktree(root_arg, branch_arg, worktree, start_point)

    monkeypatch.setattr(
        apply_fork_module,
        "create_run_worktree",
        advance_session_before_run_creation,
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """apply fork を最小ループで完了させる。"""
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    branch = run_git(linked, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads(
        (root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json").read_text()
    )
    assert state["apply"]["oracle_snapshot_commit"] == linked_commit
    assert start_points == [linked_commit]
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == linked_commit
    )
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "gu" / "worktree" / session_id / run_id
    assert apply_worktree.is_dir()
    assert (
        run_git(apply_worktree, "branch", "--show-current").stdout.strip()
        == state["apply"]["apply_branch"]
    )
    assert not apply_worktree.is_relative_to(linked)


def test_apply_fork_runs_doctor_preprocess_before_body(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """doctor preprocess、run 隔離、apply 本体の順で開始する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "use alternate cmoc ignore pattern")

    events: list[str] = []
    original_run_doctor_preprocess = runtime_cli_module.run_doctor_preprocess
    original_create_run_worktree = apply_fork_module.create_run_worktree

    def record_doctor_preprocess(root_arg: Path) -> None:
        """doctor preprocess の実行を記録して本来の修復処理へ委譲する。"""
        events.append("doctor preprocess")
        original_run_doctor_preprocess(root_arg)

    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_doctor_preprocess,
    )

    def record_create_run_worktree(
        root_arg: Path, branch: str, worktree: Path, start_point: str
    ) -> Path:
        """run の隔離開始を記録して本来の worktree 作成へ委譲する。"""
        events.append("run isolation")
        return original_create_run_worktree(root_arg, branch, worktree, start_point)

    monkeypatch.setattr(
        apply_fork_module,
        "create_run_worktree",
        record_create_run_worktree,
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """apply 本体の開始を記録し、空所見だけを返す。"""
        events.append("apply body")
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        fake_run_codex_exec,
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0, result.stdout
    assert (
        events.index("doctor preprocess")
        < events.index("run isolation")
        < events.index("apply body")
    )
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_apply_fork_ensures_cmoc_ignore_without_dirtying_session(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork は未 ignore の .cmoc/gu を clean worktree のまま ignore する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / ".gitignore").write_text("")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "stop ignoring cmoc in gitignore")
    exclude = root / ".git" / "info" / "exclude"
    exclude.write_text(
        "\n".join(
            line for line in exclude.read_text().splitlines() if line != "/.cmoc/gu/"
        )
        + "\n"
    )
    assert run_git(root, "status", "--short").stdout.strip() == "?? .cmoc/gu/"

    result = apply_fork_module._cmoc_apply_fork_body(
        "full", lambda *args, **kwargs: FakeCodexResult({"findings": []})
    )

    assert result.returncode == 0
    assert Path(result.stdout).is_file()
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert "/.cmoc/gu/" in exclude.read_text().splitlines()


def test_apply_fork_config_load_error_does_not_start_apply_run(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """設定読み込み失敗時に apply run の branch/state を開始しないことを確認する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.write_text("{invalid\n")
    run_git(root, "add", ".cmoc/gt/ar/config.json")
    run_git(root, "commit", "-m", "break cmoc config")

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "cmoc config" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "cmoc config" not in result.stderr
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "gu" / "ar" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert run_git(root, "branch", "--list", f"cmoc/apply/{session_id}/*").stdout == ""


def test_apply_fork_missing_config_is_repaired_before_starting_apply_run(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """設定不足時も doctor が config を再生成して apply run を開始する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    run_git(root, "rm", ".cmoc/gt/ar/config.json")
    run_git(root, "commit", "-m", "remove cmoc config")
    codex_calls: list[None] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """設定失敗経路で使われる Codex 結果の契約を満たす。"""
        codex_calls.append(None)
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code == 0
    assert (root / ".cmoc" / "gt" / "ar" / "config.json").is_file()
    assert codex_calls
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    assert (root / ".cmoc" / "gu" / "worktree" / session_id).is_dir()
    assert not (
        root / ".cmoc" / "gu" / "ar" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert run_git(root, "branch", "--list", f"cmoc/apply/{session_id}/*").stdout


def test_apply_fork_can_target_and_edit_gitignore(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """所見対象としての .gitignore は apply branch 側で編集できることを確認する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update gitignore",
        "evidences": [
            {
                "path": str(root / ".gitignore"),
                "line_start": 1,
                "line_end": 1,
                "summary": "gitignore",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "resolution": {
            "status": "fixed",
            "summary": "updated gitignore",
            "verification": "content checked",
        },
    }
    target_rels_by_call: list[list[str]] = []
    gitignore_finding_returned = False

    def review_and_fix(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """対象 path を記録し、gitignore 初回調査で修正と所見を返す。"""
        nonlocal gitignore_finding_returned
        rel = str(target.relative_to(root_arg))
        target_rels_by_call.append([rel])
        if rel == ".gitignore" and not gitignore_finding_returned:
            gitignore_finding_returned = True
            (root_arg / ".gitignore").write_text("/.cmoc/gu/\n# editable\n")
            return [finding]
        return []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """apply 後の変更要約出力を再現する。"""
        purpose = str(kwargs["purpose"])
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(
        apply_fork_module, "review_and_fix_apply_target", review_and_fix
    )
    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert [".gitignore"] in target_rels_by_call
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads(
        (root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json").read_text()
    )
    assert (
        run_git(root, "show", f"{state['apply']['apply_branch']}:.gitignore").stdout
        == "/.cmoc/gu/\n# editable\n"
    )


def test_apply_fork_marks_state_completed_before_report(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply loop 正常完了直後、report 生成前に completed を state file へ書く。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    seen_states: list[str] = []
    monkeypatch.setattr(apply_fork_module, "enumerate_apply_targets", lambda *args: [])

    def fake_write_report(*args: object, **kwargs: object) -> Path:
        """report生成前に保存済みapply stateを記録する。"""
        seen_states.append(json.loads(state_path.read_text())["apply"]["state"])
        report_path = (
            root / ".cmoc" / "gu" / "ar" / "report" / "apply" / "fork" / "state.md"
        )
        report_path.parent.mkdir(parents=True)
        report_path.write_text("# report\n")
        return report_path

    monkeypatch.setattr(apply_fork_module, "write_apply_fork_report", fake_write_report)

    result = apply_fork_module._cmoc_apply_fork_body(
        "full", lambda *args, **kwargs: FakeCodexResult({"findings": []})
    )

    assert result.returncode == 0
    assert seen_states == ["completed"]


def test_apply_fork_rechecks_ready_state_before_creating_run(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """lock 内の再読込で、競合した apply run の作成を拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    lock_entries = 0
    created: list[Path] = []

    @contextmanager
    def fake_apply_run_lock(_root: Path, _session_id: str) -> Iterator[None]:
        """初回lock取得時に競合したrunning stateを公開する。"""
        nonlocal lock_entries
        lock_entries += 1
        if lock_entries == 1:
            # {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
            data = json.loads(state_path.read_text())
            data["apply"].update(
                {
                    "state": "running",
                    "apply_branch": f"cmoc/apply/{session_id}/other",
                    "oracle_snapshot_commit": "other",
                }
            )
            state_path.write_text(json.dumps(data) + "\n")
        yield

    def fake_create_run_worktree(
        _root: Path, _branch: str, worktree: Path, _start_point: str
    ) -> Path:
        """run worktreeを作成したと記録し、対象directoryを用意する。"""
        created.append(worktree)
        worktree.mkdir(parents=True)
        return worktree

    monkeypatch.setattr(apply_fork_module, "apply_run_lock", fake_apply_run_lock)
    monkeypatch.setattr(
        apply_fork_module, "create_run_worktree", fake_create_run_worktree
    )

    with pytest.raises(CmocError, match="事前条件"):
        apply_fork_module._cmoc_apply_fork_body(
            "full", lambda *args, **kwargs: FakeCodexResult({"findings": []})
        )

    assert lock_entries == 1
    assert created == []


@pytest.mark.parametrize("failure", ["pid", "state"])
def test_apply_fork_initialization_failure_is_recoverable_by_abandon(
    tmp_path: Path, monkeypatch: MonkeyPatch, failure: str
) -> None:
    """worktree 作成後の PID/state failure を error state と abandon で回収する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    monkeypatch.setattr(apply_fork_module, "enumerate_apply_targets", lambda *args: [])
    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult({"findings": []}),
    )

    if failure == "pid":

        def fail_write_pid(*args: object, **kwargs: object) -> None:
            """PID保存を失敗させ、初期化失敗経路を検証する。"""
            raise OSError("pid save failed")

        monkeypatch.setattr(apply_fork_module, "write_apply_process_id", fail_write_pid)
    else:
        original_write_state = apply_fork_module.write_state
        write_count = 0

        def fail_completed_state(path: Path, state: object) -> None:
            """completed stateの保存だけを失敗させる。"""
            nonlocal write_count
            write_count += 1
            if write_count == 2:
                raise OSError("completed state save failed")
            original_write_state(path, state)

        monkeypatch.setattr(apply_fork_module, "write_state", fail_completed_state)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code != 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "error"
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree.is_dir()
    assert run_git(root, "rev-parse", "--verify", apply_branch).stdout.strip()

    abandoned = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert abandoned.exit_code == 0
    assert not apply_worktree.exists()
    assert run_git(root, "branch", "--list", apply_branch).stdout == ""
    assert json.loads(state_path.read_text())["apply"]["state"] == "ready"
