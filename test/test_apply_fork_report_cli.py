"""apply fork の report と再検査制御を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は apply fork がレビュー・修正から
commit、変更要約、report、session state 更新へ至る制御を検証することに
閉じている。収束、未収束、error、変更ファイル再調査、rolling fork は同じ loop と
report schema の観測結果として読まれるため、分割すると期待値の文脈が分散する。
現状は apply fork report の読み取り文脈を一箇所に保つ方が凝集性が高い。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
from pathlib import Path

import pytest
from _apply_support import apply_worktree_from_state
from _cli_support import runner
from _codex_support import FakeCodexResult
from _git_support import make_repo, run_git
from _ollama_support import run_doctor
from pytest import MonkeyPatch

import sub_commands.apply.fork as apply_fork_module
from basic.acp import AgentCallParameter
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from main import app
from sub_commands.apply.fork_report import (
    build_change_summary,
    changed_diff_since_fork,
    changed_paths_since_fork,
    fallback_change_summary,
)


def report_path_from_stdout(stdout: str) -> Path:
    """apply fork stdout の共通ログ後に出る report full path を返す。"""
    lines = [line for line in stdout.splitlines() if line.startswith("/")]
    assert lines
    return Path(lines[-1])


def test_apply_fork_writes_report_and_joins_realization_changes(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """fork の README/test/ancillary 差分を report 後に通常 join できる。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    session_state = json.loads(state_path.read_text())
    session_fork_commit = session_state["session"]["session_start_commit"]

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
        "resolution": {
            "status": "fixed",
            "summary": "updated readme",
            "verification": "content checked",
        },
    }
    calls: list[str] = []
    review_count = 0

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """レビュー・修正と変更要約の Codex 応答を返す。"""
        nonlocal review_count
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        schema = (
            parameter.structured_output_schema_path.name
            if parameter.structured_output_schema_path
            else None
        )
        if purpose.startswith("apply fork review and fix"):
            review_count += 1
            worktree = Path.cwd()
            (worktree / "README.md").write_text(f"# updated {review_count}\n")
            generated_test = worktree / "test" / "test_generated.py"
            generated_test.parent.mkdir(exist_ok=True)
            generated_test.write_text(f"VALUE = {review_count}\n")
            (worktree / ".gitignore").write_text(
                f"/.cmoc/gu/\n# updated {review_count}\n"
            )
            return FakeCodexResult({"findings": [finding]})
        if schema == "change_summary.json":
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "ドキュメント",
                            "summary": "realization file を更新した",
                            "changed_paths": [
                                ".gitignore",
                                "README.md",
                                "test/test_generated.py",
                            ],
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
    assert "未収束: 回数上限に達したためループを終了しました。" in rendered
    assert "# cmoc apply fork 作業レポート" in rendered
    assert "## 所見数の推移" in rendered
    count_section = rendered.split("## 所見数の推移\n", 1)[1].split(
        "\n## 変更内容要約", 1
    )[0]
    assert "まだ所見が残っている可能性があります。" in count_section
    assert (
        "ドキュメント: realization file を更新した "
        "(.gitignore, README.md, test/test_generated.py)" in rendered
    )
    assert "apply fork change summary" in calls
    assert "apply fork commit message" not in calls
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_fork_commit = state["apply"]["oracle_snapshot_commit"]
    apply_worktree = (
        root
        / ".cmoc"
        / "gu"
        / "worktree"
        / session_id
        / apply_branch.rsplit("/", 1)[-1]
    )
    front_matter = dict(
        line.split(": ", 1) for line in rendered.split("---\n", 2)[1].splitlines()
    )
    assert front_matter["cmoc_session_branch"] == session_branch
    assert front_matter["cmoc_session_fork_commit"] == session_fork_commit
    assert front_matter["cmoc_apply_branch"] == apply_branch
    assert front_matter["cmoc_apply_fork_commit"] == apply_fork_commit
    assert front_matter["cmoc_apply_worktree"] == str(apply_worktree)
    assert (
        run_git(root, "log", "-1", "--pretty=%s", apply_branch).stdout.strip()
        == "Apply finding: Update README"
    )
    joined = runner.invoke(app, ["apply", "join"], catch_exceptions=False)
    assert joined.exit_code == 0
    assert (root / "README.md").read_text().startswith("# updated ")
    assert (root / "test" / "test_generated.py").read_text().startswith("VALUE = ")
    assert "# updated " in (root / ".gitignore").read_text()


def test_apply_fork_rechecks_changed_files_until_converged(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply 後の変更ファイルを再調査し、新規ディレクトリ配下も展開する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
        "resolution": {
            "status": "fixed",
            "summary": "updated readme",
            "verification": "content checked",
        },
    }
    review_calls = 0
    target_rels: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """変更ファイル再調査が収束するまでの Codex 応答を返す。"""
        nonlocal review_calls
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork review and fix"):
            review_calls += 1
            if review_calls == 1:
                (Path.cwd() / "README.md").write_text("# updated\n")
                (Path.cwd() / "newdir").mkdir()
                (Path.cwd() / "newdir" / "new.py").write_text("print('new')\n")
                return FakeCodexResult({"findings": [finding]})
            return FakeCodexResult({"findings": []})
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)
    original_review_and_fix = apply_fork_module.review_and_fix_apply_target

    def review_and_fix(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """実装側のレビュー・修正を呼びつつ再検査対象 path を記録する。"""
        target_rels.append(str(target.relative_to(root_arg)))
        return original_review_and_fix(root_arg, target, config, codex_exec, **kwargs)

    monkeypatch.setattr(
        apply_fork_module, "review_and_fix_apply_target", review_and_fix
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert review_calls >= 2
    assert "README.md" in target_rels
    assert "newdir/new.py" in target_rels
    report_path = report_path_from_stdout(result.stdout)
    assert "result: converged" in report_path.read_text()


def test_apply_fork_converges_when_last_allowed_target_has_no_findings(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """最後の調査対象が空所見なら上限回でも収束として扱う。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("value = 1\n")
    run_git(root, "add", "README.md", "src/app.py")
    run_git(root, "commit", "-m", "change readme")
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config = json.loads(config_path.read_text())
    config["apply_fork"]["num_apply_files"] = 2
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    run_git(root, "add", ".cmoc/gt/ar/config.json")
    run_git(root, "commit", "-m", "set apply file limit")
    review_calls = 0

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """上限内の全調査対象に空所見を返す。"""
        nonlocal review_calls
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork review and fix"):
            review_calls += 1
            return FakeCodexResult({"findings": []})
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "session"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert review_calls == 2
    report_path = report_path_from_stdout(result.stdout)
    assert "result: converged" in report_path.read_text()


def test_apply_fork_is_unconverged_when_file_review_and_fix_makes_no_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """レビュー・修正で差分がなくても、所見ありの起点を再調査待ちに戻す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "change readme")
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config = json.loads(config_path.read_text())
    config["apply_fork"]["num_apply_files"] = 1
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    run_git(root, "add", ".cmoc/gt/ar/config.json")
    run_git(root, "commit", "-m", "set apply file limit")
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
        "resolution": {
            "status": "unresolved",
            "summary": "no change was made",
            "verification": "worktree stayed clean",
        },
    }
    calls: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """所見は返すがレビュー・修正では差分を作らない。"""
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        if purpose.startswith("apply fork review and fix"):
            return FakeCodexResult({"findings": [finding]})
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
    state = json.loads(
        (root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json").read_text()
    )
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == run_git(root, "rev-parse", "HEAD").stdout.strip()
    )


def test_apply_fork_rejects_diff_without_findings(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """空所見の agent call が作った差分を commit せず error にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "change readme")
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """空所見と不正な差分、および error report 用要約を返す。"""
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork review and fix"):
            (Path.cwd() / "unexpected.py").write_text("value = 'unexpected'\n")
            return FakeCodexResult({"findings": []})
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "session"])

    assert result.exit_code == 1
    assert "所見なしで差分を生成しました" in result.output
    assert "unexpected.py" in result.output
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "error"
    apply_worktree = apply_worktree_from_state(root, state)
    assert (apply_worktree / "unexpected.py").is_file()
    assert (
        "?? unexpected.py"
        in run_git(apply_worktree, "status", "--short").stdout.splitlines()
    )
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == run_git(root, "rev-parse", "HEAD").stdout.strip()
    )


def test_apply_fork_error_report_summarizes_uncommitted_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """エラー report の変更要約は commit 前の working tree 差分も対象にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"

    reviews = 0
    summary_prompt = ""

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """未 commit 差分を残したまま Codex 適用エラーへ進める。"""
        nonlocal reviews, summary_prompt
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork review and fix"):
            reviews += 1
            (Path.cwd() / "README.md").write_text("# updated before error\n")
            raise CmocError("Codex レビュー・修正に失敗しました。", [], "test")
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

    assert result.exit_code == 1
    assert reviews == 1
    assert "README.md" in summary_prompt
    assert "+# updated before error" in summary_prompt
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "error"
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


def test_apply_fork_change_summary_excludes_deleted_tracked_files(
    tmp_path: Path,
) -> None:
    """管理 branch 上の削除済み file は report 用変更要約の対象外にする。"""
    root = make_repo(tmp_path)
    (root / "deleted_realization.py").write_text("print('delete')\n")
    run_git(root, "add", "deleted_realization.py")
    run_git(root, "commit", "-m", "add deleted target")
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "deleted_realization.py").unlink()
    (root / "README.md").write_text("# kept change\n")
    captured_prompt = ""

    def fake_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """要約promptを記録し、変更要約の固定結果を返す。"""
        nonlocal captured_prompt
        captured_prompt = parameter.prompt
        return FakeCodexResult(
            {
                "changes": [
                    {
                        "category": "実装",
                        "summary": "README を更新した",
                        "changed_paths": ["README.md"],
                    }
                ]
            }
        )

    raw_diff = changed_diff_since_fork(root, fork_commit)
    paths = changed_paths_since_fork(root, fork_commit)
    fallback = fallback_change_summary(root, fork_commit, "fallback")
    summary = build_change_summary(
        root, root, fork_commit, CmocConfig(), fake_codex_exec
    )

    assert "README.md" in raw_diff
    assert "+# kept change" in raw_diff
    assert "deleted_realization.py" not in raw_diff
    assert "-print('delete')" not in raw_diff
    assert paths == ["README.md"]
    assert fallback[0]["changed_paths"] == ["README.md"]
    assert summary[0]["changed_paths"] == ["README.md"]
    assert "README.md" in captured_prompt
    assert "deleted_realization.py" not in captured_prompt


@pytest.mark.parametrize("codex_output", [{"changes": []}, {}])
def test_apply_fork_change_summary_fallback_keeps_paths(
    tmp_path: Path, codex_output: dict[str, object]
) -> None:
    """Codex の空要約時も、差分がある report から変更 path を落とさない。"""
    root = make_repo(tmp_path)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "README.md").write_text("# fallback path\n")

    def fake_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """指定した空または欠落要約をCodex結果として返す。"""
        return FakeCodexResult(codex_output)

    summary = build_change_summary(
        root, root, fork_commit, CmocConfig(), fake_codex_exec
    )

    assert summary == [
        {
            "category": "変更要約なし",
            "summary": "変更 path のみを機械的に記録しました。",
            "changed_paths": ["README.md"],
        }
    ]


def test_apply_fork_report_does_not_invent_loop_when_no_targets(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """調査対象がない場合、未実行の loop 1 を report しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    assert (
        "収束: 調査待ちファイルリストが空になったことによりループを終了しました。"
        in rendered
    )
    assert "- 所見列挙ループは実行されませんでした" in rendered
    assert "- ループ 1: 0" not in rendered


def test_apply_fork_rolling_uses_previous_apply_join_commit(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """rolling apply fork が前回 apply join 後の変更だけを対象にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    (root / "unrelated.py").write_text("print('before join')\n")
    run_git(root, "add", "unrelated.py")
    run_git(root, "commit", "-m", "change before apply join")
    apply_branch = f"cmoc/apply/{session_id}/manual"
    apply_worktree = root / ".cmoc" / "gu" / "worktree" / session_id / "manual"
    oracle_snapshot_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "worktree", "add", "-b", apply_branch, str(apply_worktree), "HEAD")
    applied = apply_worktree / "src" / "applied.py"
    applied.parent.mkdir()
    applied.write_text("value = 'updated by apply'\n")
    run_git(apply_worktree, "add", "src/applied.py")
    run_git(apply_worktree, "commit", "-m", "update implementation from apply")
    state = json.loads(state_path.read_text())
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "oracle_snapshot_commit": oracle_snapshot_commit,
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    assert runner.invoke(app, ["apply", "join"], catch_exceptions=False).exit_code == 0
    (root / "oracle" / "spec.md").write_text("# changed after join\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "change oracle after apply join")

    target_rels: list[str] = []

    def review_and_fix(
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
        apply_fork_module, "review_and_fix_apply_target", review_and_fix
    )
    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        fake_run_codex_exec,
    )

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "oracle/spec.md" in target_rels
    assert "src/applied.py" not in target_rels
    assert "unrelated.py" not in target_rels
    state = json.loads(state_path.read_text())["session"]
    assert state["last_joined_apply_oracle_snapshot_commit"] == oracle_snapshot_commit
