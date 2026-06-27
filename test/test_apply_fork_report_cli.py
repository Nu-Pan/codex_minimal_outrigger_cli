"""apply fork の report と再検査制御を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は apply fork が所見列挙から
適用、commit、変更要約、report、session state 更新へ至る制御を検証することに
閉じている。収束、未収束、error、変更ファイル再調査、rolling fork は同じ loop と
report schema の観測結果として読まれるため、分割すると期待値の文脈が分散する。
現状は apply fork report の読み取り文脈を一箇所に保つ方が凝集性が高い。
"""

import json
from pathlib import Path

from basic.acp import AgentCallParameter
from _support import (
    make_repo,
    run_git,
    runner,
)
from main import app
from pytest import MonkeyPatch
import sub_commands.apply.fork as apply_fork_module
from sub_commands.apply.fork_report import (
    changed_diff_since_fork,
    changed_paths_since_fork,
    fallback_change_summary,
)


class FakeCodexResult:
    """apply fork テストが参照する Codex 実行結果 field だけを持つ fake。"""

    def __init__(self, output_json: object | None = None, output_text: str = "") -> None:
        """必要な結果 field をテストごとに差し替えられるように保持する。"""
        self.output_json = output_json
        self.output_text = output_text


def report_path_from_stdout(stdout: str) -> Path:
    """apply fork stdout は report の full path だけを返す。"""
    lines = stdout.splitlines()
    assert len(lines) == 1
    return Path(lines[0])


def test_apply_fork_writes_report_with_change_summary(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """未収束 report に Codex 由来の変更要約と commit message が反映される。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    calls: list[str] = []
    application_count = 0

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """所見、適用、commit message、変更要約の各 Codex 応答を返す。"""
        nonlocal application_count
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        schema = (
            parameter.structured_output_schema_path.name
            if parameter.structured_output_schema_path
            else None
        )
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            application_count += 1
            (Path.cwd() / "README.md").write_text(f"# updated {application_count}\n")
            return FakeCodexResult(None)
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if schema == "change_summary.json":
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "ドキュメント",
                            "summary": "README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 2
    report_path = report_path_from_stdout(result.stdout)
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "result: unconverged" in rendered
    assert "未収束: 回数上限に達したためループを終了しました。まだ所見が残っている可能性があります。" in rendered
    assert "# cmoc apply fork report" in rendered
    assert "## Finding Count" in rendered
    assert "ドキュメント: README を更新した (README.md)" in rendered
    assert "apply fork change summary" in calls
    assert "apply fork commit message" in calls
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    apply_branch = state["apply"]["apply_branch"]
    assert (
        run_git(root, "log", "-1", "--pretty=%s", apply_branch).stdout.strip()
        == "Update README from apply finding"
    )


def test_apply_fork_rechecks_changed_files_until_converged(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply 後の変更ファイルを再調査し、INDEX.md だけは再調査対象から外す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    enumerate_calls = 0
    target_rels: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """変更ファイル再調査が収束するまでの Codex 応答を返す。"""
        nonlocal enumerate_calls
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork enumerate findings"):
            enumerate_calls += 1
            return FakeCodexResult(
                {"findings": [finding] if enumerate_calls == 1 else []}
            )
        if purpose == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            (Path.cwd() / "INDEX.md").write_text("generated index\n")
            (Path.cwd() / "newdir").mkdir()
            (Path.cwd() / "newdir" / "new.py").write_text("print('new')\n")
            return FakeCodexResult(None)
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)
    original_enumerate = apply_fork_module.enumerate_apply_findings_for_target

    def enumerate_findings(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """実装側の列挙を呼びつつ再検査対象 path を記録する。"""
        target_rels.append(str(target.relative_to(root_arg)))
        return original_enumerate(root_arg, target, config, codex_exec, **kwargs)

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls >= 2
    assert "README.md" in target_rels
    assert "newdir/new.py" in target_rels
    assert "INDEX.md" not in target_rels
    report_path = report_path_from_stdout(result.stdout)
    assert "result: converged" in report_path.read_text()


def test_apply_fork_converges_when_last_allowed_target_has_no_findings(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """最後の調査対象が空所見なら上限回でも収束として扱う。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "change readme")
    config_path = root / ".cmoc" / "config.json"
    config = json.loads(config_path.read_text())
    config["apply_fork"]["num_apply_files"] = 1
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    enumerate_calls = 0

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """上限 1 回の唯一の調査対象に空所見を返す。"""
        nonlocal enumerate_calls
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork enumerate findings"):
            enumerate_calls += 1
            return FakeCodexResult({"findings": []})
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "session"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls == 1
    report_path = report_path_from_stdout(result.stdout)
    assert "result: converged" in report_path.read_text()


def test_apply_fork_is_unconverged_when_finding_application_makes_no_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """所見対応で差分が出なくても、所見ありの起点対象は再調査待ちに戻す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "change readme")
    config_path = root / ".cmoc" / "config.json"
    config = json.loads(config_path.read_text())
    config["apply_fork"]["num_apply_files"] = 1
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    finding = {
        "title": "No-op finding",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    calls: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """所見は返すが適用では差分を作らない。"""
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            return FakeCodexResult()
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "session"], catch_exceptions=False
    )

    assert result.exit_code == 2
    assert "apply fork commit message" not in calls
    report_path = report_path_from_stdout(result.stdout)
    assert "result: unconverged" in report_path.read_text()
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == run_git(root, "rev-parse", "HEAD").stdout.strip()
    )


def test_apply_fork_error_report_summarizes_uncommitted_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """エラー report の変更要約は commit 前の working tree 差分も対象にする。"""
    root = make_repo(tmp_path)
    (root / ".agents").mkdir()
    (root / ".agents" / "skill.md").write_text("original\n")
    run_git(root, "add", ".agents/skill.md")
    run_git(root, "commit", "-m", "add agents")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README before error",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    applications = 0
    summary_prompt = ""

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """未 commit 差分を残したまま編集禁止対象エラーへ進める。"""
        nonlocal applications, summary_prompt
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            applications += 1
            (Path.cwd() / "README.md").write_text("# updated before error\n")
            (Path.cwd() / ".agents" / "skill.md").write_text("forbidden\n")
            return FakeCodexResult()
        if purpose == "apply fork change summary":
            summary_prompt = parameter.prompt
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "実装",
                            "summary": "commit 前に README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert applications == 2
    assert "README.md" in summary_prompt
    assert "+# updated before error" in summary_prompt
    rendered = report_path_from_stdout(result.stdout).read_text()
    assert "result: error" in rendered
    assert "実装: commit 前に README を更新した (README.md)" in rendered


def test_apply_fork_change_summary_includes_untracked_files(tmp_path: Path) -> None:
    """report 用変更要約は未追跡 file だけの作業 tree も差分として扱う。"""
    root = make_repo(tmp_path)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "new_realization.py").write_text("print('new')\n")

    raw_diff = changed_diff_since_fork(root, fork_commit)
    paths = changed_paths_since_fork(root, fork_commit)
    fallback = fallback_change_summary(root, fork_commit, "fallback")

    assert "new_realization.py" in raw_diff
    assert "+print('new')" in raw_diff
    assert paths == ["new_realization.py"]
    assert fallback == [
        {
            "category": "fallback",
            "summary": "変更 path のみを機械的に記録しました。",
            "changed_paths": ["new_realization.py"],
        }
    ]


def test_apply_fork_report_does_not_invent_loop_when_no_targets(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """調査対象がない場合、未実行の loop 1 を report しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    monkeypatch.setattr(apply_fork_module, "enumerate_apply_targets", lambda *args: [])

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """変更要約だけを返し、所見列挙が呼ばれたら失敗させる。"""
        purpose = str(kwargs["purpose"])
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    rendered = report_path_from_stdout(result.stdout).read_text()
    assert "result: converged" in rendered
    assert "- no finding enumeration loops were executed" in rendered
    assert "- loop 1: 0" not in rendered


def test_apply_fork_rejects_forbidden_agents_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """編集禁止対象の差分を検出し、error state と report に落とし込む。"""
    root = make_repo(tmp_path)
    (root / ".agents").mkdir()
    (root / ".agents" / "skill.md").write_text("original\n")
    run_git(root, "add", ".agents/skill.md")
    run_git(root, "commit", "-m", "add agents")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    readme_finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    agents_finding = {
        "title": "Bad agents edit",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update agents",
    }
    applications = 0
    calls: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """編集禁止対象への差分を含む Codex 適用結果を再現する。"""
        nonlocal applications
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [readme_finding, agents_finding]})
        if purpose == "apply fork finding application":
            applications += 1
            if applications == 1:
                (Path.cwd() / "README.md").write_text("# updated before error\n")
            else:
                (Path.cwd() / ".agents" / "skill.md").write_text("forbidden\n")
            return FakeCodexResult()
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README before error\n")
        if purpose == "apply fork change summary":
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "実装",
                            "summary": "エラー前に README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "編集禁止対象" in result.stderr
    report_path = report_path_from_stdout(result.stdout)
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "実装: エラー前に README を更新した (README.md)" in rendered
    assert "apply fork change summary" in calls
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "error"


def test_apply_fork_rolling_uses_previous_apply_join_commit(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """rolling apply fork が前回 apply join 後の変更だけを対象にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    apply_branch = f"cmoc/apply/{session_id}/manual"
    apply_worktree = root / ".cmoc" / "worktrees" / session_id / "manual"
    oracle_snapshot_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "worktree", "add", "-b", apply_branch, str(apply_worktree), "HEAD")
    (apply_worktree / "README.md").write_text("# updated by apply\n")
    run_git(apply_worktree, "add", "README.md")
    run_git(apply_worktree, "commit", "-m", "update readme from apply")
    state = json.loads(state_path.read_text())
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "oracle_snapshot_commit": oracle_snapshot_commit,
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    assert (
        runner.invoke(app, ["apply", "join"], catch_exceptions=False).exit_code == 0
    )
    (root / "oracle" / "spec.md").write_text("# changed after join\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "change oracle after apply join")

    target_rels: list[str] = []

    def enumerate_findings(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """rolling 対象 path を記録し、追加所見なしとして返す。"""
        target_rels.append(str(target.relative_to(root_arg)))
        return []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """rolling apply fork 用に空所見を返す。"""
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )
    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        fake_run_codex_exec,
    )

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert target_rels == ["oracle/spec.md"]
    state = json.loads(state_path.read_text())["session"]
    assert state["last_joined_apply_oracle_snapshot_commit"] == oracle_snapshot_commit
