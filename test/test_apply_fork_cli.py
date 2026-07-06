"""Apply fork CLI regression tests share one fixture-heavy external behavior context.

The file intentionally stays above 16,000 characters because target normalization,
doctor preflight, config failure, state updates, and gitignore handling are all
observed through the same apply fork CLI boundary and shared repository fixtures.
Splitting those cases would increase repeated setup and hide the cross-case context.
Size rationale: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter
from _support import (
    add_tracked_ignored_oracle_file,
    apply_worktree_from_state,
    make_repo,
    run_git,
    runner,
    run_init,
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
    init_result = run_init(root)
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
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "local" / "worktree" / session_id / run_id
    assert apply_worktree.is_dir()
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
    assert run_init(root).exit_code == 0
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
    assert not apply_worktree.is_relative_to(linked)


def test_apply_fork_runs_doctor_preprocess_before_body(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork 本体前に doctor preprocess の共通修復が実行される。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
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

    assert result.exit_code == 0, result.stdout
    assert "/.cmoc/local/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_apply_fork_ensures_cmoc_ignore_without_dirtying_session(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply fork は未 ignore の .cmoc/local を clean worktree のまま ignore する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
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

    class FakeCodexResult:
        output_json = {"findings": []}

    result = apply_fork_module._cmoc_apply_fork_body(
        "full", lambda *args, **kwargs: FakeCodexResult()
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
    assert run_init(root).exit_code == 0
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
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    run_git(root, "rm", ".cmoc/config.json")
    run_git(root, "commit", "-m", "remove cmoc config")

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "cmoc config が存在しません。" in result.stdout
    assert not (root / ".cmoc" / "config.json").exists()


def test_apply_fork_can_target_and_edit_gitignore(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """所見対象としての .gitignore は apply branch 側で編集できることを確認する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
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


def test_apply_fork_target_normalization_excludes_non_realization_paths(
    tmp_path: Path,
) -> None:
    """realization file 定義から外れる管理 path と規範 path を除外する。"""
    root = make_repo(tmp_path)
    src_target = root / "src" / "target.py"
    codex_target = root / ".codex" / "config.toml"
    nested_codex_target = root / "src" / ".codex" / "template.txt"
    nested_agents_target = root / "docs" / ".agents" / "rule.md"
    agents_target = root / "AGENTS.md"
    index_target = root / "INDEX.md"
    src_target.parent.mkdir()
    codex_target.parent.mkdir()
    nested_codex_target.parent.mkdir(parents=True)
    nested_agents_target.parent.mkdir(parents=True)
    src_target.write_text("target\n")
    codex_target.write_text("config\n")
    nested_codex_target.write_text("template\n")
    nested_agents_target.write_text("rule\n")
    agents_target.write_text("agents\n")
    index_target.write_text("index\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {
            src_target,
            codex_target,
            nested_codex_target,
            nested_agents_target,
            agents_target,
            index_target,
        },
    )

    assert targets == [
        nested_agents_target.resolve(),
        nested_codex_target.resolve(),
        src_target.resolve(),
    ]


def test_apply_fork_target_normalization_excludes_cmoc_runtime_files(
    tmp_path: Path,
) -> None:
    """作業用状態領域の .cmoc/local 配下 file は対象にしない。"""
    root = make_repo(tmp_path)
    config_target = root / ".cmoc" / "config.json"
    ignored_local_target = root / ".cmoc" / "local" / "cache.json"
    config_target.parent.mkdir()
    ignored_local_target.parent.mkdir(parents=True)
    config_target.write_text("{}\n")
    ignored_local_target.write_text("{}\n")
    (root / ".gitignore").write_text("/.cmoc/local/\n")
    run_git(root, "add", ".gitignore", ".cmoc/config.json")
    run_git(root, "commit", "-m", "add cmoc config")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {config_target, ignored_local_target},
    )

    assert targets == [config_target.resolve()]


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


def test_apply_fork_target_normalization_keeps_tracked_ignored_files(
    tmp_path: Path,
) -> None:
    """通常の git check-ignore と同じく tracked ignored file を対象に残す。"""
    root = make_repo(tmp_path)
    add_tracked_ignored_oracle_file(root)
    realization_target = root / "src" / "ignored.py"
    realization_target.parent.mkdir()
    realization_target.write_text("value = 1\n")
    with (root / ".gitignore").open("a") as file:
        file.write("src/ignored.py\nsrc/untracked.py\n")
    run_git(root, "add", "-f", ".gitignore", "src/ignored.py")
    run_git(root, "commit", "-m", "add ignored realization")
    untracked_ignored = root / "src" / "untracked.py"
    untracked_ignored.write_text("value = 2\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {
            root / "oracle" / "ignored.md",
            realization_target,
            untracked_ignored,
        },
    )

    assert targets == [
        (root / "oracle" / "ignored.md").resolve(),
        realization_target.resolve(),
    ]


def test_apply_fork_target_normalization_classifies_oracle_symlink_by_repo_path(
    tmp_path: Path,
) -> None:
    """oracle 配下 symlink は link 先ではなく repository path で分類する。"""
    root = make_repo(tmp_path)
    (root / "memo").mkdir()
    (root / "memo" / "draft.md").write_text("# draft\n")
    oracle_link = root / "oracle" / "memo-link.md"
    oracle_link.symlink_to("../memo/draft.md")
    run_git(root, "add", "memo/draft.md", "oracle/memo-link.md")
    run_git(root, "commit", "-m", "add oracle symlink")

    targets = apply_fork_module.normalize_apply_targets(root, {oracle_link})

    assert targets == [oracle_link.absolute()]


def test_apply_fork_marks_state_completed_before_report(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply loop 正常完了直後、report 生成前に completed を state file へ書く。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
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

    class FakeCodexResult:
        output_json = {"findings": []}

    result = apply_fork_module._cmoc_apply_fork_body(
        "full", lambda *args, **kwargs: FakeCodexResult()
    )

    assert result.returncode == 0
    assert seen_states == ["completed"]
