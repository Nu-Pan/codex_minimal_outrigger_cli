import json
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter
from _support import (
    apply_worktree_from_state,
    make_repo,
    run_git,
    runner,
)
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
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0
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
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "worktrees" / session_id / run_id
    assert apply_worktree.is_dir()
    assert not (root / ".cmoc" / "worktrees" / "apply").exists()
    assert "apply_worktree" not in state["apply"]
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert calls
    assert any(call.startswith("apply fork enumerate findings") for call in calls)


def test_apply_fork_uses_linked_worktree_branch_and_head(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """linked worktree 上の session branch と HEAD から apply run を開始する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    linked = root / ".cmoc" / "worktrees" / "linked-apply"
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
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["oracle_snapshot_commit"] == linked_commit
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == linked_commit
    )
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "worktrees" / session_id / run_id
    assert not apply_worktree.is_relative_to(linked)


def test_apply_fork_does_not_rewrite_session_gitignore(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork が session 側の既存 .gitignore 表現を書き換えないことを確認する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "use alternate cmoc ignore pattern")

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """gitignore 保持テスト用に空所見だけを返す。"""
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        fake_run_codex_exec,
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / ".gitignore").read_text() == ".cmoc/\n"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_apply_fork_rejects_tracked_cmoc_without_dirtying_session(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork は .cmoc の追跡解除を session 側で実行しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / ".gitignore").write_text("")
    run_git(root, "add", "-f", ".gitignore", ".cmoc")
    run_git(root, "commit", "-m", "track cmoc state")
    assert run_git(root, "status", "--short").stdout.strip() == ""

    with pytest.raises(apply_fork_module.CmocError) as exc_info:
        apply_fork_module._cmoc_apply_fork_body("full", lambda *args, **kwargs: None)

    assert ".cmoc が git 追跡対象外に初期化されていません。" in str(exc_info.value)
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert run_git(root, "ls-files", "--", ".cmoc").stdout.strip()


@pytest.mark.parametrize("config_case", ["invalid_json", "missing"])
def test_apply_fork_config_load_error_does_not_start_apply_run(
    tmp_path: Path, monkeypatch: MonkeyPatch, config_case: str
) -> None:
    """設定読み込み失敗時に apply run の branch/state を開始しないことを確認する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    config_path = root / ".cmoc" / "config.json"
    if config_case == "invalid_json":
        config_path.write_text("{invalid\n")
    else:
        config_path.unlink()

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "cmoc config" in result.stdout
    assert "cmoc config" not in result.stderr
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert run_git(root, "branch", "--list", f"cmoc/apply/{session_id}/*").stdout == ""
    if config_case == "missing":
        assert not config_path.exists()


def test_apply_fork_can_target_and_edit_gitignore(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """所見対象としての .gitignore は apply branch 側で編集できることを確認する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    current_findings = [finding]

    def enumerate_findings(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """対象 path を記録し、初回だけ gitignore 所見を返す。"""
        nonlocal current_findings
        target_rels_by_call.append([str(target.relative_to(root_arg))])
        current_findings = [finding] if len(target_rels_by_call) == 1 else []
        return current_findings

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """apply による .gitignore 編集と後続出力を再現する。"""
        purpose = str(kwargs["purpose"])
        if purpose == "apply fork finding application":
            (Path.cwd() / ".gitignore").write_text("/.cmoc/\n# editable\n")
            return FakeCodexResult()
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update gitignore\n")
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
    assert ".gitignore" in target_rels_by_call[0]
    assert [".gitignore"] in target_rels_by_call
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert (
        run_git(root, "show", f"{state['apply']['apply_branch']}:.gitignore").stdout
        == "/.cmoc/\n# editable\n"
    )


def test_apply_fork_target_normalization_keeps_nested_memo_directory(
    tmp_path: Path,
) -> None:
    """root 直下 memo を除外し、入れ子の memo directory は対象に残す。"""
    root = make_repo(tmp_path)
    (root / "memo").mkdir()
    (root / "memo" / "root.txt").write_text("private\n")
    (root / "docs" / "memo").mkdir(parents=True)
    nested = root / "docs" / "memo" / "public.txt"
    nested.write_text("target\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {root / "memo" / "root.txt", nested},
    )

    assert targets == [nested.resolve()]


def test_apply_fork_target_normalization_keeps_binary_files(
    tmp_path: Path,
) -> None:
    """full scope の候補になり得る binary file を file 種別だけで除外しない。"""
    root = make_repo(tmp_path)
    realization_binary = root / "asset.bin"
    oracle_binary = root / "oracle" / "asset.bin"
    realization_binary.write_bytes(b"\x00realization\n")
    oracle_binary.write_bytes(b"\x00oracle\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {realization_binary, oracle_binary},
    )

    assert targets == [realization_binary.resolve(), oracle_binary.resolve()]
