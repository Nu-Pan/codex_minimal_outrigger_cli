"""Apply fork CLI regression tests for lifecycle, state, and gitignore behavior.

Target normalization has an independent test module because it does not need the
CLI lifecycle or its repository fixtures. The execution order follows
<work-root>/oracle/doc/app_spec/sub_command/apply_fork.md.
"""

import json
from pathlib import Path

from basic.acp import AgentCallParameter
import commons.runtime_cli as runtime_cli_module
from _apply_support import apply_worktree_from_state
from _cli_support import runner
from _git_support import make_repo, run_git
from _ollama_support import run_doctor
from main import app
from pytest import MonkeyPatch
import sub_commands.apply.fork as apply_fork_module


class FakeCodexResult:
    """apply fork テストが参照する Codex 実行結果 field だけを持つ fake。"""

    def __init__(self, output_json: object | None = None, output_text: str = "") -> None:
        """必要な結果 field をテストごとに差し替えられるように保持する。"""
        self.output_json = output_json
        self.output_text = output_text


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
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "local" / "worktree" / session_id / run_id
    assert apply_worktree.is_dir()
    assert run_git(apply_worktree, "branch", "--show-current").stdout.strip() == state["apply"]["apply_branch"]
    assert not (root / ".cmoc" / "local" / "worktree" / "apply").exists()
    assert "apply_worktree" not in state["apply"]
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "local" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert calls
    assert any(call.startswith("apply fork enumerate findings") for call in calls)


def test_apply_fork_uses_linked_worktree_branch_and_head(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """linked worktree 上の session branch と HEAD から apply run を開始する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "local" / "worktree" / "linked-apply"
    run_git(root, "worktree", "add", "-b", "linked-apply-home", str(linked), "HEAD")
    (linked / "README.md").write_text("# linked apply\n")
    run_git(linked, "add", "README.md")
    run_git(linked, "commit", "-m", "linked apply change")
    linked_commit = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
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
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    assert state["apply"]["oracle_snapshot_commit"] == linked_commit
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == linked_commit
    )
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "local" / "worktree" / session_id / run_id
    assert apply_worktree.is_dir()
    assert run_git(apply_worktree, "branch", "--show-current").stdout.strip() == state["apply"]["apply_branch"]
    assert not apply_worktree.is_relative_to(linked)


def test_apply_fork_runs_doctor_preprocess_before_body(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork 本体前に doctor preprocess の共通修復が実行される。"""
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

    def record_doctor_preprocess(root_arg: Path) -> None:
        """doctor preprocess の実行を記録して本来の修復処理へ委譲する。"""
        events.append("doctor preprocess")
        original_run_doctor_preprocess(root_arg)

    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_doctor_preprocess,
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
    assert events.index("doctor preprocess") < events.index("apply body")
    assert "/.cmoc/local/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_apply_fork_ensures_cmoc_ignore_without_dirtying_session(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork は未 ignore の .cmoc/local を clean worktree のまま ignore する。"""
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
            line
            for line in exclude.read_text().splitlines()
            if line != "/.cmoc/local/"
        )
        + "\n"
    )
    assert run_git(root, "status", "--short").stdout.strip() == "?? .cmoc/local/"

    result = apply_fork_module._cmoc_apply_fork_body(
        "full", lambda *args, **kwargs: FakeCodexResult({"findings": []})
    )

    assert result.returncode == 0
    assert Path(result.stdout).is_file()
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert "/.cmoc/local/" in exclude.read_text().splitlines()


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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    config_path = root / ".cmoc" / "config.json"
    config_path.write_text("{invalid\n")
    run_git(root, "add", ".cmoc/config.json")
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
        root / ".cmoc" / "local" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert run_git(root, "branch", "--list", f"cmoc/apply/{session_id}/*").stdout == ""


def test_apply_fork_missing_config_fails_before_starting_apply_run(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """設定不足時に apply run を開始せず、Codex も呼び出さない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    run_git(root, "rm", ".cmoc/config.json")
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

    assert result.exit_code != 0
    assert "cmoc config が存在しません。" in result.stdout
    assert not (root / ".cmoc" / "config.json").exists()
    assert not codex_calls
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None
    assert not (root / ".cmoc" / "local" / "worktree" / session_id).exists()
    assert not (
        root / ".cmoc" / "local" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert run_git(root, "branch", "--list", f"cmoc/apply/{session_id}/*").stdout == ""


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
        "suggested_fix": "update gitignore",
    }
    target_rels_by_call: list[list[str]] = []
    gitignore_finding_returned = False

    def enumerate_findings(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """対象 path を記録し、gitignore 初回調査だけ所見を返す。"""
        nonlocal gitignore_finding_returned
        rel = str(target.relative_to(root_arg))
        target_rels_by_call.append([rel])
        if rel == ".gitignore" and not gitignore_finding_returned:
            gitignore_finding_returned = True
            return [finding]
        return []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """apply による .gitignore 編集と後続出力を再現する。"""
        purpose = str(kwargs["purpose"])
        if purpose == "apply fork finding application":
            (Path.cwd() / ".gitignore").write_text("/.cmoc/local/\n# editable\n")
            return FakeCodexResult()
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )
    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert [".gitignore"] in target_rels_by_call
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    assert (
        run_git(root, "show", f"{state['apply']['apply_branch']}:.gitignore").stdout
        == "/.cmoc/local/\n# editable\n"
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    seen_states: list[str] = []
    monkeypatch.setattr(apply_fork_module, "enumerate_apply_targets", lambda *args: [])

    def fake_write_report(*args: object, **kwargs: object) -> Path:
        seen_states.append(json.loads(state_path.read_text())["apply"]["state"])
        report_path = root / ".cmoc" / "local" / "report" / "apply" / "fork" / "state.md"
        report_path.parent.mkdir(parents=True)
        report_path.write_text("# report\n")
        return report_path

    monkeypatch.setattr(apply_fork_module, "write_apply_fork_report", fake_write_report)

    result = apply_fork_module._cmoc_apply_fork_body(
        "full", lambda *args, **kwargs: FakeCodexResult({"findings": []})
    )

    assert result.returncode == 0
    assert seen_states == ["completed"]
