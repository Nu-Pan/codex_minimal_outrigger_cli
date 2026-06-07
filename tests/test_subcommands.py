"""サブコマンド本体の決定論的な制御ロジックのテスト。"""

import ast
import builtins
import inspect
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
import typer
from pytest import MonkeyPatch

import sub_commands.apply.fork as apply_module
import sub_commands.apply.join as apply_join_module
import sub_commands.indexing as indexing_module
import sub_commands.review.oracles as review_oracles_module
import sub_commands.session.abandon as session_abandon_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module
import commons.repo as repo_module
import commons.timing as timing_module
from commons.codex import COST_PERFORMANCE_MODEL
from commons.codex import COST_PERFORMANCE_REASONING_EFFORT
from commons.codex import FRONTIER_HIGH_REASONING_EFFORT
from commons.codex import FRONTIER_MODEL
from commons.codex import FRONTIER_REASONING_EFFORT
from commons.codex import COMMIT_MESSAGE_MODEL
from commons.codex import COMMIT_MESSAGE_REASONING_EFFORT
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.errors import format_error_report
from commons.repo import write_apply_process_id
from commons.repo import write_session_state
from commons.subcommand_log import log_event
from commons.subcommand_log import subcommand_log
from commons.timing import StepTimer, start_step
from commons.timestamps import is_timestamp
from sub_commands.apply.fork import cmoc_apply_impl
from sub_commands.apply.fork import _apply_prompt
from sub_commands.apply.fork import _apply_index_excluded_roots
from sub_commands.apply.fork import APPLY_FORK_EXIT_CODE_CONVERGED
from sub_commands.apply.fork import APPLY_FORK_EXIT_CODE_UNCONVERGED
from sub_commands.apply.fork import _DISCREPANCY_OUTPUT_SCHEMA
from sub_commands.apply.fork import _commit_all_changes
from sub_commands.apply.fork import _organize_prompt
from sub_commands.apply.fork import _validate_discrepancy_payload
from sub_commands.apply.abandon import cmoc_apply_abandon_impl
from sub_commands.apply.join import cmoc_apply_join_impl
from sub_commands.review.oracles import cmoc_review_oracles_impl
from sub_commands.indexing import cmoc_indexing_impl
from sub_commands.review.oracles import _evaluation_prompt
from sub_commands.review.oracles import _improvement_prompt
from sub_commands.init import cmoc_init_impl
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl
from sub_commands.session.join import _conflict_prompt
from sub_commands.session.join import _files_with_conflict_markers


def _assert_markdown_error_report(report: str) -> None:
    """共通エラーレポートは markdown 見出しで区切り、空行を含めない。"""
    assert "# ERROR" in report
    assert "## Summary" in report
    assert "## Next actions" in report
    assert "## Detail" in report
    assert "## Call stack" in report
    assert all(line != "" for line in report.splitlines())


def test_python_sources_do_not_use_future_annotations() -> None:
    """実装コードは annotations future import を使わない。"""
    src_root = Path(__file__).resolve().parents[1] / "src"
    violating_paths: list[Path] = []

    for path in src_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.module != "__future__":
                continue
            imported_names = {alias.name for alias in node.names}
            if "annotations" in imported_names:
                violating_paths.append(path.relative_to(src_root.parent))

    assert violating_paths == []


def test_literal_cmoc_error_actions_offer_multiple_choices() -> None:
    """CmocError の静的な actions は oracle 通り複数提示する。"""
    repo_root = Path(__file__).resolve().parents[1]
    violating_locations: list[str] = []

    for source_root in (repo_root / "src", repo_root / "tests"):
        for path in source_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if getattr(node.func, "id", None) != "CmocError":
                    continue
                actions = None
                if len(node.args) >= 2:
                    actions = node.args[1]
                for keyword in node.keywords:
                    if keyword.arg == "actions":
                        actions = keyword.value
                if not isinstance(actions, ast.List):
                    continue
                if len(actions.elts) < 2:
                    relative_path = path.relative_to(repo_root)
                    violating_locations.append(f"{relative_path}:{node.lineno}")

    assert violating_locations == []


def test_subcommands_do_not_emit_step_timer_report_directly() -> None:
    """ステップ別経過時間は共通の完了サマリー内だけで出す。"""
    repo_root = Path(__file__).resolve().parents[1]
    subcommands_root = repo_root / "src" / "sub_commands"
    violating_locations: list[str] = []

    for path in subcommands_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "report":
                continue
            if not isinstance(node.func.value, ast.Name):
                continue
            if node.func.value.id != "timer":
                continue
            relative_path = path.relative_to(repo_root)
            violating_locations.append(f"{relative_path}:{node.lineno}")

    assert violating_locations == []


def test_run_command_reports_returned_nonzero_exit_code(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """handler が返した非 0 終了コードは共通エラーレポートにする。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.setattr(
        sys,
        "argv",
        ["cmoc", "sample", "--flag", "value"],
    )

    def handler(resolved_repo: Path) -> int:
        """非 0 終了コードを返すサブコマンド本体。"""
        assert resolved_repo == repo
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "first step")
        return 2

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler, command_path="cmoc sample")

    captured = capsys.readouterr()
    log_files = list((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    log_events = [
        json.loads(line)
        for line in log_files[0].read_text(encoding="utf-8").splitlines()
    ]
    assert exit_info.value.exit_code == 2
    assert captured.err == ""
    assert len(log_files) == 1
    _assert_markdown_error_report(captured.out)
    assert "サブコマンドがエラー終了しました。" in captured.out
    assert "終了コード 2 を返しました。" in captured.out
    assert "# cmoc subcommand start: cmoc sample" in captured.out
    assert "(1/1) first step" in captured.out
    assert "sample (1/1) first step" not in captured.out
    assert "# Command completion report" in captured.out
    assert f"subcommand log: {log_files[0]}" in captured.out
    assert captured.out.index("# Command completion report") < captured.out.index(
        "sample step timings:"
    )
    assert "sample step timings:" in captured.out
    assert "- 1/1 first step:" in captured.out
    assert "subcommand total elapsed:" in captured.out
    assert "subcommand quota wait elapsed:" in captured.out
    assert "subcommand return code: 2" in captured.out
    assert log_events[0]["event"] == "subcommand_start"
    assert log_events[0]["command_path"] == "cmoc sample"
    assert log_events[0]["argv"] == ["cmoc", "sample", "--flag", "value"]
    assert log_events[0]["cwd"] == str(repo)
    assert log_events[0]["repo_root"] == str(repo)
    assert log_events[0]["subcommand_log"] == str(log_files[0])
    assert any(
        event["event"] == "step_start"
        and event["step"] == "first step"
        and event["step_index"] == "1/1"
        for event in log_events
    )
    assert any(
        event["event"] == "subcommand_end"
        and event["returncode"] == 2
        and event["subcommand_log"] == str(log_files[0])
        for event in log_events
    )
    assert "/.cmoc/logs/" in (repo / ".git" / "info" / "exclude").read_text(
        encoding="utf-8"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_start_step_logs_hierarchical_step_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """階層ステップ番号は console と JSONL の両方に全階層を出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> int:
        """階層化されたサブステップ開始を 1 件出す。"""
        timer = StepTimer("sample")
        start_step(
            timer,
            ((5, 6), (2, 3), (1, 4)),
            None,
            "nested step",
        )
        return 0

    run_command(handler)

    captured = capsys.readouterr()
    log_file = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    )
    log_content = log_file.read_text(encoding="utf-8")
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert "(5/6, 2/3, 1/4) nested step" in captured.out
    assert any(
        event["event"] == "step_start"
        and event["step"] == "nested step"
        and event["step_index"] == "5/6, 2/3, 1/4"
        for event in log_events
    )


def test_step_timer_reports_hierarchical_step_timings(
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """完了サマリーは階層 step index ごとに親子の経過時間を出す。"""
    times = iter(float(value) for value in range(12))
    monkeypatch.setattr(timing_module, "perf_counter", lambda: next(times))

    timer = StepTimer("sample")
    start_step(timer, 5, 6, "parent")
    start_step(timer, ((5, 6), (1, 2)), None, "child")
    start_step(timer, ((5, 6), (2, 2)), None, "child")
    start_step(timer, 6, 6, "next")

    timer.report()

    captured = capsys.readouterr()
    assert "- 5/6 parent:  0h  0m  5.0s" in captured.out
    assert "- 5/6, 1/2 child:  0h  0m  1.0s" in captured.out
    assert "- 5/6, 2/2 child:  0h  0m  1.0s" in captured.out
    assert "- 6/6 next:  0h  0m  1.0s" in captured.out


def test_run_command_logs_summary_on_exception(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """例外終了時は stdout へエラーと終了集計を出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> None:
        """例外終了するサブコマンド本体として途中進捗を出す。"""
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "failing step")
        raise RuntimeError("boom")

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    log_file = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    )
    log_content = log_file.read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 1
    assert captured.err == ""
    _assert_markdown_error_report(captured.out)
    assert "RuntimeError" in captured.out
    assert "boom" in captured.out
    assert "# Command completion report" in captured.out
    assert f"subcommand log: {log_file}" in captured.out
    assert "subcommand return code: 1" in captured.out
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert any(
        event["event"] == "step_start" and event["step"] == "failing step"
        for event in log_events
    )
    assert any(
        event["event"] == "subcommand_end"
        and event["returncode"] == 1
        and event["subcommand_log"] == str(log_file)
        for event in log_events
    )


def test_run_command_reports_total_elapsed_from_command_entry(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """終了集計の全体経過時間はログ開始ではなく共通入口から測る。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    command_times = iter([10.0, 35.0])
    monkeypatch.setattr(
        "commons.command_runner.perf_counter",
        lambda: next(command_times),
    )
    monkeypatch.setattr(
        "commons.subcommand_log.perf_counter",
        lambda: 20.0,
    )

    def handler(_repo: Path) -> None:
        """正常終了する空のサブコマンド本体。"""

    run_command(handler)

    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    log_events = [json.loads(line) for line in log_content.splitlines()]
    end_event = next(event for event in log_events if event["event"] == "subcommand_end")
    assert end_event["total_elapsed_seconds"] == 25.0


def test_run_command_reports_nonzero_typer_exit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """非 0 の typer.Exit も共通エラーレポートとして stdout に出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> None:
        """Typer の中断例外でエラー終了するサブコマンド本体。"""
        raise typer.Exit(7)

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 7
    assert captured.err == ""
    _assert_markdown_error_report(captured.out)
    assert "サブコマンドがエラー終了しました。" in captured.out
    assert "typer.Exit(7)" in captured.out
    assert "raise typer.Exit(7)" in captured.out
    assert "Traceback is not available for this exception." not in captured.out
    assert "# Command completion report" in captured.out
    assert "subcommand return code: 7" in captured.out
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert any(
        event["event"] == "subcommand_end" and event["returncode"] == 7
        for event in log_events
    )


def test_run_command_treats_apply_unconverged_as_non_error_exit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply fork の未収束区分はエラーレポートなしで終了コードを保持する。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    assert APPLY_FORK_EXIT_CODE_CONVERGED == 0
    assert APPLY_FORK_EXIT_CODE_UNCONVERGED not in {
        APPLY_FORK_EXIT_CODE_CONVERGED,
        1,
        2,
    }

    def handler(_repo: Path) -> int:
        """未収束の apply fork 本体と同じ終了コードを返す。"""
        return APPLY_FORK_EXIT_CODE_UNCONVERGED

    with pytest.raises(typer.Exit) as exit_info:
        run_command(
            handler,
            non_error_exit_codes={APPLY_FORK_EXIT_CODE_UNCONVERGED},
        )

    captured = capsys.readouterr()
    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert captured.err == ""
    assert "ERROR" not in captured.out
    assert "# Command completion report" in captured.out
    assert (
        f"subcommand return code: {APPLY_FORK_EXIT_CODE_UNCONVERGED}"
        in captured.out
    )
    assert f'"returncode": {APPLY_FORK_EXIT_CODE_UNCONVERGED}' in log_content


def test_run_command_reports_repo_root_resolution_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """repo root 解決失敗は stdout へエラーと終了集計を出す。"""
    def fail_enter_repo_root() -> Path:
        """repo root 解決に失敗する setup 処理。"""
        raise CmocError(
            "Git リポジトリのルートが見つかりませんでした。",
            [
                "git 管理下のリポジトリへ移動してください。",
                "このディレクトリをリポジトリにする場合は `git init` を実行してください。",
            ],
            f"開始パス: {tmp_path.resolve()}",
        )

    monkeypatch.setattr(
        "commons.command_runner.enter_repo_root",
        fail_enter_repo_root,
    )

    def handler(_repo: Path) -> None:
        """repo root 解決に失敗するため呼ばれない。"""
        raise AssertionError("handler must not be called")

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    assert exit_info.value.exit_code == 1
    assert captured.err == ""
    _assert_markdown_error_report(captured.out)
    assert "Git リポジトリのルートが見つかりませんでした。" in captured.out
    assert f"開始パス: {tmp_path.resolve()}" in captured.out
    assert "# Command completion report" in captured.out
    assert "subcommand log: unavailable" in captured.out
    assert "subcommand total elapsed:" in captured.out
    assert "subcommand quota wait elapsed:" in captured.out
    assert "subcommand return code: 1" in captured.out
    assert not (tmp_path / ".cmoc" / "logs" / "sub_commands").exists()


def test_init_adds_cmoc_ignore_and_commits_it(tmp_path: Path) -> None:
    """`cmoc init` は `.cmoc` ignore ルールを commit する。"""
    repo = _init_repo(tmp_path)

    cmoc_init_impl(repo)

    assert ".cmoc" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert (
        _git(repo, "log", "-1", "--pretty=%s").stdout.strip()
        == "Initialize cmoc"
    )


def test_indexing_impl_runs_maintenance_on_clean_repo(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc indexing` 本体は clean repo で INDEX メンテナンスへ委譲する。"""
    repo = _init_repo(tmp_path)
    maintained_roots: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        maintained_roots.append(repo_root)
        return True

    monkeypatch.setattr(
        indexing_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    cmoc_indexing_impl(repo)

    captured = capsys.readouterr()
    assert maintained_roots == [repo]
    assert "committed INDEX.md maintenance changes" in captured.out


def test_indexing_impl_rejects_dirty_repo_before_maintenance(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc indexing` は実行前の未コミット差分があれば止まる。"""
    repo = _init_repo(tmp_path)
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    maintained_roots: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        maintained_roots.append(repo_root)
        return True

    monkeypatch.setattr(
        indexing_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError) as error:
        cmoc_indexing_impl(repo)

    assert maintained_roots == []
    assert "未コミットの変更があります。" in error.value.message
    assert "dirty.txt" in error.value.detail


def test_init_repairs_negated_cmoc_ignore_rule_and_commits_it(
    tmp_path: Path,
) -> None:
    """`cmoc init` は negation で無効な既存 `/.cmoc/` も補修して commit する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n!/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "add ineffective cmoc ignore")

    cmoc_init_impl(repo)

    assert (repo / ".gitignore").read_text(encoding="utf-8") == (
        "/.cmoc/\n!/.cmoc/\n/.cmoc/\n"
    )
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert (
        _git(
            repo,
            "check-ignore",
            "-q",
            "--",
            ".cmoc/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    assert _git(repo, "show", "HEAD:.gitignore").stdout == (
        "/.cmoc/\n!/.cmoc/\n/.cmoc/\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert (
        _git(repo, "log", "-1", "--pretty=%s").stdout.strip()
        == "Initialize cmoc"
    )


def test_init_untracks_existing_cmoc_file_and_commits_it(
    tmp_path: Path,
) -> None:
    """`cmoc init` は tracked `.cmoc` ファイルの追跡解除も commit する。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert cmoc_file.exists()
    assert _git(repo, "status", "--porcelain").stdout == ""
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout
    assert ".gitignore" in last_commit_paths
    assert ".cmoc/logs/tracked.log" in last_commit_paths


def test_init_untracks_modified_cmoc_file_and_keeps_worktree_file(
    tmp_path: Path,
) -> None:
    """差分あり tracked `.cmoc` でも init を完了し、実ファイルは残す。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")
    cmoc_file.write_text("staged\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    cmoc_file.write_text("worktree\n", encoding="utf-8")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert (
        _git(
            repo,
            "check-ignore",
            "-q",
            "--",
            ".cmoc/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    assert cmoc_file.read_text(encoding="utf-8") == "worktree\n"
    assert _git(repo, "status", "--porcelain").stdout == ""
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout
    assert ".gitignore" in last_commit_paths
    assert ".cmoc/logs/tracked.log" in last_commit_paths


def test_init_does_not_commit_existing_gitignore_changes(
    tmp_path: Path,
) -> None:
    """`cmoc init` は既存 `.gitignore` 差分を初期化 commit に混ぜない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    cmoc_init_impl(repo)

    gitignore = (repo / ".gitignore").read_text(encoding="utf-8")
    committed_gitignore = _git(repo, "show", "HEAD:.gitignore").stdout
    assert gitignore == "user-rule\n/.cmoc/\n"
    assert committed_gitignore == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert _git(repo, "status", "--porcelain").stdout == " M .gitignore\n"


def test_init_does_not_commit_preexisting_staged_changes(
    tmp_path: Path,
) -> None:
    """`cmoc init` は実行前から stage 済みの別差分を commit に混ぜない。"""
    repo = _init_repo(tmp_path)
    staged_file = repo / "feature.txt"
    staged_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")

    cmoc_init_impl(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout.splitlines()
    assert last_commit_paths == [".gitignore"]
    assert _git(repo, "diff", "--cached", "--name-only").stdout == (
        "feature.txt\n"
    )


def test_init_keeps_head_when_preexisting_staged_restore_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """既存 staged 差分を戻せない場合、`cmoc init` は HEAD を進めない。"""
    repo = _init_repo(tmp_path)
    base_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    staged_file = repo / "feature.txt"
    staged_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")

    def fail_apply_staged_diff(
        repo_root: Path,
        staged_diff: str,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        assert repo_root == repo
        assert staged_diff
        assert env.get("GIT_INDEX_FILE")
        assert _git(repo, "rev-parse", "HEAD").stdout.strip() == base_head
        return subprocess.CompletedProcess(
            ["git", "apply", "--cached", "--3way"],
            1,
            "",
            "forced restore failure",
        )

    monkeypatch.setattr(
        repo_module,
        "_apply_staged_diff_to_index",
        fail_apply_staged_diff,
    )

    with pytest.raises(CmocError):
        cmoc_init_impl(repo)

    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == base_head
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "diff", "--cached", "--name-only").stdout == (
        "feature.txt\n"
    )


def test_init_does_not_restore_preexisting_staged_cmoc_changes(
    tmp_path: Path,
) -> None:
    """実行前に stage 済みの `.cmoc` 差分も最終的に追跡対象外にする。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "staged.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/staged.log")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(
        repo,
        "check-ignore",
        "-q",
        "--",
        ".cmoc/.__cmoc_ignore_probe__",
    ).returncode == 0
    assert ".cmoc" not in _git(
        repo,
        "diff",
        "--cached",
        "--name-only",
    ).stdout
    assert cmoc_file.exists()


def test_init_can_create_first_commit(tmp_path: Path) -> None:
    """`cmoc init` は unborn HEAD のリポジトリでも初期化 commit を作る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")

    cmoc_init_impl(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_init_first_commit_keeps_existing_gitignore_content(
    tmp_path: Path,
) -> None:
    """unborn HEAD の初期 commit は既存 `.gitignore` 内容も保持する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    cmoc_init_impl(repo)

    assert (repo / ".gitignore").read_text(encoding="utf-8") == (
        "user-rule\n/.cmoc/\n"
    )
    assert _git(repo, "show", "HEAD:.gitignore").stdout == (
        "user-rule\n/.cmoc/\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_init_can_create_first_commit_with_existing_cmoc_ignore_rule(
    tmp_path: Path,
) -> None:
    """既存 ignore rule 付き unborn HEAD でも初期 commit を作る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / ".gitignore").write_text("user-rule\n/.cmoc/\n", encoding="utf-8")

    cmoc_init_impl(repo)
    init_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    state_paths = _session_state_paths(repo)
    session_state = json.loads(state_paths[0].read_text(encoding="utf-8"))
    assert _git(repo, "show", "HEAD:.gitignore").stdout == (
        "user-rule\n/.cmoc/\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert session_state["session"]["session_start_commit"] == init_head


def test_session_fork_creates_session_branch_and_records_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc session fork` は session branch 作成と state 記録を行う。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    record_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(record_path.read_text(encoding="utf-8"))
    assert branch_name.startswith("cmoc/session/")
    assert is_timestamp(session_id)
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["session_start_commit"] == base_commit
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is None
    assert state["apply"] == {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    output = capsys.readouterr().out
    assert "(1/4) repository 状態検証" in output
    assert "session fork (1/4) repository 状態検証" not in output
    assert "session branch 作成試行 (1/10)" in output


def test_session_fork_repairs_missing_cmoc_ignore_before_clean_check(
    tmp_path: Path,
) -> None:
    """`.cmoc` ignore 不足は内部初期化 commit として補修して続行する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    initial_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    state = json.loads(
        (repo / ".cmoc" / "sessions" / f"{session_id}.json").read_text(
            encoding="utf-8",
        )
    )
    assert branch_name.startswith("cmoc/session/")
    assert state["session"]["session_start_commit"] == initial_head
    assert _git(repo, "merge-base", home_branch, branch_name).stdout.strip() == (
        initial_head
    )
    assert _git(repo, "show", "HEAD:.gitignore").stdout == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc session branch"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_fork_ensures_cmoc_ignore_before_active_state_scan(
    tmp_path: Path,
) -> None:
    """ignore 保証が済む前に `.cmoc/sessions` の壊れた state を読まない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    broken_path = repo / ".cmoc" / "sessions" / "broken.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert ".cmoc/" in error.value.detail
    assert "JSON が不正" not in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _session_state_paths(repo) == [broken_path]


@pytest.mark.parametrize(
    ("target_kind", "expected_message"),
    [
        ("commit_hash", "detached HEAD"),
        ("remote_tracking_branch", "detached HEAD"),
    ],
)
def test_session_fork_rejects_non_local_branch_start_points(
    tmp_path: Path,
    target_kind: str,
    expected_message: str,
) -> None:
    """`cmoc session fork` は local branch 以外から開始しない。"""
    repo = _init_repo(tmp_path)
    start_branch = _git(repo, "branch", "--show-current").stdout.strip()
    start_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "update-ref", "refs/remotes/origin/main", start_commit)
    checkout_target = start_commit
    if target_kind == "remote_tracking_branch":
        checkout_target = "origin/main"
    _git(repo, "checkout", checkout_target)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert expected_message in error.value.message
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == start_commit
    assert start_branch in _git(repo, "branch", "--format=%(refname:short)").stdout
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_cmoc_managed_branch_before_creating_state(
    tmp_path: Path,
) -> None:
    """cmoc 管理 branch 上では session branch を二重作成しない。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc/session/2026-05-10_22-21_10_000000123")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "cmoc 管理 branch" in error.value.message
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert branches.count("cmoc/session/") == 1
    assert _session_state_paths(repo) == []


@pytest.mark.parametrize(
    "branch_name",
    [
        "cmoc/session/not-a-timestamp",
        "cmoc/session/2026-05-10_22-21_10_000000123/extra",
        "cmoc/apply/foo/bar",
        "cmoc/apply/2026-05-10_22-21_10_000000123/run-1",
    ],
)
def test_session_fork_rejects_cmoc_reserved_branch_namespace(
    tmp_path: Path,
    branch_name: str,
) -> None:
    """不正形式でも cmoc 予約 namespace 上では session を開始しない。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", branch_name)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "cmoc 管理 branch" in error.value.message
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout.splitlines()
    assert branch_name in branches
    assert [
        branch
        for branch in branches
        if branch.startswith("cmoc/session/") and branch != branch_name
    ] == []
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_uncommitted_changes_before_branch_creation(
    tmp_path: Path,
) -> None:
    """未コミット差分がある場合は branch 作成前に止める。"""
    repo = _init_repo(tmp_path)
    start_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "README.md").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == start_branch
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_existing_active_session_for_home_branch(
    tmp_path: Path,
) -> None:
    """同じ home branch の active session がある場合は新規作成しない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    start_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    session_id = "2026-05-10_22-21_10_000000123"
    _git(repo, "branch", f"cmoc/session/{session_id}")
    write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": home_branch,
                "session_start_commit": start_commit,
                "last_joined_apply_oracle_snapshot_commit": None,
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "active session" in error.value.message
    assert error.value.detail == session_id
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / f"{session_id}.json",
    ]


def test_session_fork_rejects_ambiguous_null_active_session_at_same_commit(
    tmp_path: Path,
) -> None:
    """null home branch の active session が曖昧なら新規 session を止める。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    start_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "branch", "feature", start_commit)

    cmoc_session_fork_impl(repo)
    first_session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    first_session_id = first_session_branch.removeprefix("cmoc/session/")
    first_state_path = repo / ".cmoc" / "sessions" / f"{first_session_id}.json"
    first_state = json.loads(first_state_path.read_text(encoding="utf-8"))
    first_state["session"]["session_home_branch"] = None
    write_session_state(repo, first_session_id, first_state)
    _git(repo, "checkout", "feature")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    first_state = json.loads(first_state_path.read_text(encoding="utf-8"))
    assert "home branch 未確定の active session" in error.value.message
    assert first_state["session"]["session_home_branch"] is None
    assert _git(repo, "branch", "--show-current").stdout.strip() == "feature"
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / f"{first_session_id}.json",
    ]


def test_session_fork_rechecks_active_session_before_branch_creation(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """作成直前に active session が見えた場合も新規 session を作らない。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    calls = 0

    def racing_active_session_ids(
        _repo_root: Path,
        _session_home_branch: str,
    ) -> list[str]:
        """事前確認後に別 session が作られた競合を模擬する。"""
        nonlocal calls
        calls += 1
        if calls == 1:
            return []
        return ["existing"]

    monkeypatch.setattr(
        session_fork_module,
        "active_session_ids_for_home_branch",
        racing_active_session_ids,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "active session" in error.value.message
    assert error.value.detail == "existing"
    assert calls == 2
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert "cmoc/session/" not in branches
    assert _session_state_paths(repo) == []


def test_session_fork_from_linked_worktree_records_state_in_linked_repo_root(
    tmp_path: Path,
) -> None:
    """linked worktree で作った session state は linked repo-root 側へ保存する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")

    cmoc_session_fork_impl(linked)

    branch_name = _git(linked, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    assert (linked / ".cmoc" / "sessions" / f"{session_id}.json").exists()
    assert not (repo / ".cmoc" / "sessions" / f"{session_id}.json").exists()


def test_session_fork_from_linked_worktree_rejects_linked_active_session(
    tmp_path: Path,
) -> None:
    """active session 判定は linked repo-root 側の state を見る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")
    start_commit = _git(linked, "rev-parse", "HEAD").stdout.strip()
    session_id = "2026-05-10_22-21_10_000000123"
    _git(linked, "branch", f"cmoc/session/{session_id}")
    write_session_state(
        linked,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": "feature",
                "session_start_commit": start_commit,
                "last_joined_apply_oracle_snapshot_commit": None,
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(linked)

    assert "active session" in error.value.message
    assert error.value.detail == session_id
    assert _git(linked, "branch", "--show-current").stdout.strip() == "feature"
    assert _session_state_paths(linked) == [
        linked / ".cmoc" / "sessions" / f"{session_id}.json",
    ]
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_malformed_session_state_before_branch_creation(
    tmp_path: Path,
) -> None:
    """壊れた session state がある場合は active guard を fail closed にする。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    broken_path = repo / ".cmoc" / "sessions" / "broken.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "JSON が不正" in error.value.message
    assert str(broken_path) in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert "cmoc/session/" not in branches
    assert _session_state_paths(repo) == [broken_path]


def test_session_fork_rejects_orphan_session_branch_before_creation(
    tmp_path: Path,
) -> None:
    """対応 state がない session branch が残る場合は新規 session を作らない。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    orphan_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _git(repo, "branch", orphan_branch)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "session state がない session branch" in error.value.message
    assert orphan_branch in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert branches.count("cmoc/session/") == 1
    assert _session_state_paths(repo) == []


def test_session_fork_rolls_back_branch_when_state_write_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """state 保存に失敗した session branch は残さない。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()

    def fail_write_session_state(
        _repo_root: Path,
        _session_id: str,
        _state: dict[str, object],
    ) -> Path:
        """session state 保存失敗を模擬する。"""
        raise OSError("fake state write failure")

    monkeypatch.setattr(
        session_fork_module,
        "write_session_state",
        fail_write_session_state,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "session state の保存に失敗" in error.value.message
    assert "fake state write failure" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert "cmoc/session/" not in branches
    assert _session_state_paths(repo) == []
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_fork_keeps_state_when_rollback_branch_delete_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """rollback が branch を消せない場合は対応する state を残す。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = "2026-05-10_22-21_10_000000123"
    session_branch = f"cmoc/session/{session_id}"
    original_run_git = session_fork_module.run_git

    monkeypatch.setattr(
        session_fork_module,
        "make_timestamp",
        lambda: session_id,
    )

    def fail_after_writing_session_state(
        repo_root: Path,
        state_session_id: str,
        state: dict[str, object],
    ) -> Path:
        """state 作成後の保存失敗を模擬する。"""
        path = write_session_state(repo_root, state_session_id, state)
        raise OSError(f"fake state write failure after {path.name}")

    def fail_branch_delete(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """rollback 中の session branch 削除失敗を模擬する。"""
        if args == ["branch", "-D", session_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                stdout="",
                stderr="fake branch delete failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_fork_module,
        "write_session_state",
        fail_after_writing_session_state,
    )
    monkeypatch.setattr(session_fork_module, "run_git", fail_branch_delete)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "session state の保存に失敗" in error.value.message
    assert "完全には取り消せません" in error.value.message
    assert "fake branch delete failure" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert session_branch in branches
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["apply"]["state"] == "ready"


def test_eval_oracles_writes_report_with_fake_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc eval-oracles --full` は oracle 評価レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    maintain_calls: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review oracles 冒頭の INDEX.md メンテナンスを記録する。"""
        maintain_calls.append(repo_root)
        return False

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """不整合なしの oracle 評価結果を返す Codex 実行を模擬する。"""
        codex_kwargs.append(kwargs)
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert len(maintain_calls) == 1
    review_worktree = maintain_calls[0]
    assert review_worktree != repo
    assert review_worktree.is_dir()
    assert review_worktree.is_relative_to(repo / ".cmoc" / "worktrees")
    assert _git(review_worktree, "branch", "--show-current").stdout.startswith(
        "cmoc/review/"
    )
    assert codex_kwargs[0]["expect_json"] is True
    assert codex_kwargs[0]["output_schema"] == (
        review_oracles_module._EVALUATION_OUTPUT_SCHEMA
    )
    issue_schema = review_oracles_module._EVALUATION_OUTPUT_SCHEMA["properties"][
        "issues"
    ]["items"]
    basis_schema = issue_schema["properties"]["specification_only_basis"]
    assert basis_schema == {
        "type": "string",
        "description": (
            "この問題点の評価が仕様ファイルと INDEX.md だけに"
            "基づくことの説明。"
        ),
    }
    assert codex_kwargs[0].get("skip_index_maintenance") is not True
    assert "json_validator" in codex_kwargs[0]
    assert 'mode: "full"' in report
    assert 'result: "ok"' in report
    assert "## Fatal issues" in report
    assert "No issues." in report
    assert "## Specification-only basis" not in report


def test_review_oracles_parallel_evaluation_records_worker_codex_events(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """並列 oracle 評価の worker 内 Codex 呼び出しもサブコマンド JSONL に残す。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    for name in ["a.md", "b.md"]:
        (oracle_root / name).write_text(f"{name}\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(
        repo_root: Path,
        prompt: str,
        *,
        purpose: str,
        **kwargs: object,
    ) -> str:
        """run_codex_exec の完了通知と同じイベントだけを worker thread で記録する。"""
        log_event(
            "codex_exec_call",
            {
                "purpose": purpose,
                "log_path": str(
                    repo_root / ".cmoc" / "logs" / "codex_exec" / "fake.log"
                ),
                "elapsed_seconds": 0.1,
                "returncode": 0,
            },
        )
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with subcommand_log(repo):
        cmoc_review_oracles_impl(
            repo,
            full=True,
            repeat_improve_issues_list=0,
        )

    log_file = next((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    events = [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").splitlines()
    ]
    codex_events = [
        event for event in events if event["event"] == "codex_exec_call"
    ]
    assert sorted(event["purpose"] for event in codex_events) == [
        "oracle 評価 oracles/a.md",
        "oracle 評価 oracles/b.md",
    ]


def test_review_oracles_runs_codex_in_review_worktree(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review oracles の Codex 評価は session worktree ではなく review worktree で動く。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    codex_repo_roots: list[Path] = []

    def fake_codex(repo_root: Path, *args: object, **kwargs: object) -> str:
        """Codex 実行 root を記録して問題なしを返す。"""
        codex_repo_roots.append(repo_root)
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert len(codex_repo_roots) == 1
    assert codex_repo_roots[0] != repo
    assert codex_repo_roots[0].is_relative_to(repo / ".cmoc" / "worktrees")
    assert _git(codex_repo_roots[0], "branch", "--show-current").stdout.startswith(
        "cmoc/review/"
    )


def test_review_oracles_merges_review_branch_to_session(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review branch の INDEX.md 更新は終了時に session branch へ自動 merge される。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (repo / "docs").mkdir()
    (repo / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
    _git(repo, "add", "oracles", "docs")
    _git(repo, "commit", "-m", "add docs and oracles")
    _prepare_review_oracles_session(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review worktree 側だけで INDEX.md 更新 commit を作る。"""
        (repo_root / "docs" / "INDEX.md").write_text(
            "review maintained docs index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "docs/INDEX.md")
        _git(repo_root, "commit", "-m", "fake review index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(
        review_oracles_module,
        "run_codex_exec",
        lambda *args, **kwargs: json.dumps({"issues": []}, ensure_ascii=False),
    )

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == (
        "review maintained docs index\n"
    )
    head_parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    assert len(head_parents) == 3
    assert "fake review index maintenance" in _git(repo, "log", "--oneline").stdout


def test_review_oracles_index_conflict_keeps_session_side(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review branch merge の INDEX.md conflict は session branch 側を採用する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    docs = repo / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("guide\n", encoding="utf-8")
    (docs / "INDEX.md").write_text("base docs index\n", encoding="utf-8")
    _git(repo, "add", "oracles", "docs")
    _git(repo, "commit", "-m", "add docs index")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review worktree 側の INDEX.md 更新 commit を作る。"""
        (repo_root / "docs" / "INDEX.md").write_text(
            "review docs index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "docs/INDEX.md")
        _git(repo_root, "commit", "-m", "fake review index maintenance")
        return True

    codex_called = False

    def fake_codex(*args: object, **kwargs: object) -> str:
        """merge 前に session branch 側の同じ INDEX.md を変更済み commit にする。"""
        nonlocal codex_called
        if not codex_called:
            codex_called = True
            (repo / "docs" / "INDEX.md").write_text(
                "session docs index\n",
                encoding="utf-8",
            )
            _git(repo, "add", "docs/INDEX.md")
            _git(repo, "commit", "-m", "session index update during review")
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == (
        "session docs index\n"
    )
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == ""
    head_parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    assert len(head_parents) == 3


def test_eval_oracles_snapshots_oracles_with_maintained_indexes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価 snapshot は開始時点本文とメンテナンス後 INDEX.md を読む。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    original_oracle = oracle_root / "original.md"
    original_oracle.write_text("original\n", encoding="utf-8")
    original_index = oracle_root / "INDEX.md"
    original_index.write_text("initial oracle index\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add original oracle")
    _prepare_review_oracles_session(repo)
    review_start_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    maintain_exclusions: list[list[str]] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """メンテナンス中に HEAD と oracle file set が動く状況を模擬する。"""
        maintain_exclusions.append([])
        (repo_root / "oracles" / "generated.md").write_text(
            "generated\n",
            encoding="utf-8",
        )
        (repo_root / "oracles" / "INDEX.md").write_text(
            "maintained oracle index\n",
            encoding="utf-8",
        )
        (repo_root / "INDEX.md").write_text("index\n", encoding="utf-8")
        _git(repo_root, "add", "INDEX.md", "oracles")
        _git(repo_root, "commit", "-m", "fake index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    evaluated_purposes: list[str] = []
    snapshot_reads: list[tuple[str, str]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """固定済み oracle だけが開始時点 INDEX snapshot で評価されることを記録する。"""
        evaluated_purposes.append(str(kwargs["purpose"]))
        prompt = str(args[1])
        index_match = re.search(
            r"`([^`]+/oracles/INDEX\.md)` から始まる INDEX\.md",
            prompt,
        )
        oracle_match = re.search(
            r"開始時点の内容を固定したコピー `([^`]+/oracles/original\.md)`",
            prompt,
        )
        assert index_match is not None
        assert oracle_match is not None
        snapshot_reads.append(
            (
                Path(oracle_match.group(1)).read_text(encoding="utf-8"),
                Path(index_match.group(1)).read_text(encoding="utf-8"),
            )
        )
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert maintain_exclusions == [[]]
    assert evaluated_purposes == ["oracle 評価 oracles/original.md"]
    assert snapshot_reads == [("original\n", "maintained oracle index\n")]
    assert f'head_commit: "{review_start_head}"' in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 1" in report
    assert "oracles/generated.md" not in report


def test_eval_oracles_snapshot_gets_missing_oracles_index_after_maintenance(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """元の INDEX.md がなくても評価 prompt の snapshot 側 INDEX.md は存在する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """欠落していた oracles/INDEX.md がメンテナンスで作られる状況を模擬する。"""
        (repo_root / "oracles" / "INDEX.md").write_text(
            "created oracle index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "oracles/INDEX.md")
        _git(repo_root, "commit", "-m", "fake oracle index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    snapshot_index_texts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """評価 prompt が指す snapshot 側 INDEX.md の実在と内容を記録する。"""
        prompt = str(args[1])
        index_match = re.search(
            r"`([^`]+/oracles/INDEX\.md)` から始まる INDEX\.md",
            prompt,
        )
        assert index_match is not None
        snapshot_index_texts.append(
            Path(index_match.group(1)).read_text(encoding="utf-8")
        )
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert snapshot_index_texts == ["created oracle index\n"]


def test_eval_oracles_reads_fixed_snapshot_after_oracle_tree_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価本文と path 検証は評価直前の oracle snapshot に固定する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("original snapshot text\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX.md メンテナンス自体は oracle 本文を変えない。"""
        (repo_root / "oracles" / "INDEX.md").write_text(
            "maintained index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "oracles/INDEX.md")
        _git(repo_root, "commit", "-m", "fake oracle index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    snapshot_texts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """prompt 上の snapshot path を読み、live tree 変更の影響がないことを返す。"""
        prompt = str(args[1])
        match = re.search(
            r"開始時点の内容を固定したコピー `([^`]+/oracles/spec\.md)`",
            prompt,
        )
        assert match is not None
        oracle_file.unlink()
        (repo / "oracles" / "later.md").write_text(
            "later live text\n",
            encoding="utf-8",
        )
        _git(repo, "add", "-A", "oracles")
        _git(repo, "commit", "-m", "change live oracle tree during review")
        snapshot_path = Path(match.group(1))
        snapshot_texts.append(snapshot_path.read_text(encoding="utf-8"))
        issue = _eval_oracle_issue(
            "warning",
            "snapshot warning",
            oracle_file,
            1,
            1,
            [oracle_file],
        )
        return json.dumps({"issues": [issue]}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert snapshot_texts == ["original snapshot text\n"]
    assert "snapshot warning" in report
    assert "| 1 | `oracles/spec.md` | 1 |" in report
    assert "oracles/later.md" not in report


def test_eval_oracles_index_maintenance_updates_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review 前の INDEX.md メンテナンスは oracles 配下も最新化する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    stale_index = "stale oracle routing\n"
    (oracle_root / "INDEX.md").write_text(stale_index, encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add stale oracle index")
    _prepare_review_oracles_session(repo)

    def fake_index_codex(*args: object, **kwargs: object) -> str:
        """repo root INDEX 生成だけを決定論的に返す。"""
        return json.dumps(
            {
                "summary": ["テスト用 entry です。"],
                "read_this_when": ["テストで読むとき。"],
                "do_not_read_this_when": ["テストで読まないとき。"],
            },
            ensure_ascii=False,
        )

    def fake_review_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価では問題なしを返す。"""
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_index_codex)
    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_review_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert (oracle_root / "INDEX.md").read_text(encoding="utf-8") != stale_index
    changed_files = _git(
        repo,
        "diff",
        "--name-only",
        "HEAD^1",
        "HEAD",
    ).stdout.splitlines()
    assert "oracles/INDEX.md" in changed_files


def test_eval_oracles_runs_file_evaluations_in_parallel(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """ファイルごとの oracle 評価は並列実行し、report 順は対象順を保つ。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    for name in ["a.md", "b.md", "c.md"]:
        (oracle_root / name).write_text(f"{name}\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    barrier = threading.Barrier(3, timeout=2.0)
    lock = threading.Lock()
    active_calls = 0
    max_active_calls = 0
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """全評価呼び出しが同時に開始されることを観測する。"""
        nonlocal active_calls, max_active_calls
        with lock:
            active_calls += 1
            max_active_calls = max(max_active_calls, active_calls)
            purposes.append(str(kwargs["purpose"]))
        barrier.wait()
        time.sleep(0.05)
        with lock:
            active_calls -= 1
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert max_active_calls > 1
    assert sorted(purposes) == [
        "oracle 評価 oracles/a.md",
        "oracle 評価 oracles/b.md",
        "oracle 評価 oracles/c.md",
    ]
    assert report.index("| 1 | `oracles/a.md` | 0 |") < report.index(
        "| 2 | `oracles/b.md` | 0 |"
    )
    assert report.index("| 2 | `oracles/b.md` | 0 |") < report.index(
        "| 3 | `oracles/c.md` | 0 |"
    )


def test_eval_oracles_writes_error_report_when_evaluation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価処理に失敗した場合も `result: error` レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価中に失敗する Codex 実行を模擬する。"""
        raise RuntimeError("fake evaluation failure")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake evaluation failure"):
        cmoc_review_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert 'result: "error"' in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 0" in report
    assert "- Failed stage: `oracle ファイル評価`" in report
    assert "- Exception type: `RuntimeError`" in report
    assert "- Exception message: `fake evaluation failure`" in report
    assert "# cmoc review oracles report" in report
    assert "## Summary" in report
    assert "## Verdict" in report
    assert "## Specification-only basis" not in report
    assert "成功評価ではありません" in report
    assert "今回評価した範囲では問題点が検出されませんでした" not in report
    assert "## Evaluated oracle files" in report
    assert "## Fatal issues" in report
    assert "## Inconclusive issues" in report
    assert "## Warnings" in report
    assert "## Referenced files" in report
    expected_sections = [
        "# cmoc review oracles report",
        "## Summary",
        "## Verdict",
        "## Evaluated oracle files",
        "## Fatal issues",
        "## Inconclusive issues",
        "## Warnings",
        "## Referenced files",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
    evaluated_section = report[
        report.index("## Evaluated oracle files") : report.index(
            "## Fatal issues"
        )
    ]
    assert "Not evaluated oracle files:" not in evaluated_section


def test_eval_oracles_writes_error_report_when_preparation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """前処理に失敗した場合も、取得済み範囲で error レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(_repo_root: Path) -> bool:
        """INDEX.md メンテナンス中の失敗を模擬する。"""
        raise RuntimeError("fake preparation failure")

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(RuntimeError, match="fake preparation failure"):
        cmoc_review_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert 'result: "error"' in report
    assert 'mode: "full"' in report
    assert "branch:" in report
    assert "head_commit: null" not in report
    assert "deleted_oracles_detected: false" in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 0" in report
    assert "- Failed stage: `INDEX.md メンテナンス`" in report
    assert "| 1 | `oracles/spec.md` | not_evaluated | - |" in report


def test_eval_oracles_error_report_marks_unevaluated_files_in_table(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """途中失敗時、未評価 file は評価済み行ではなく状態付き行にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_a = oracle_root / "a.md"
    oracle_b = oracle_root / "b.md"
    oracle_a.write_text("a\n", encoding="utf-8")
    oracle_b.write_text("b\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """a.md だけ成功し、b.md の評価で失敗する。"""
        purpose = str(kwargs["purpose"])
        if "oracles/b.md" in purpose:
            raise RuntimeError("fake second evaluation failure")
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake second evaluation failure"):
        cmoc_review_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert "oracle_count_total: 2" in report
    assert "oracle_count_evaluated: 1" in report
    assert "## Specification-only basis" not in report
    assert "| 1 | `oracles/a.md` | evaluated | 0 |" in report
    assert "| 2 | `oracles/b.md` | not_evaluated | - |" in report
    assert "| 2 | `oracles/b.md` | evaluated | 0 |" not in report
    assert "Not evaluated oracle files:" not in report
    assert report.index("## Evaluated oracle files") < report.index(
        "## Fatal issues"
    )


def test_eval_oracles_writes_error_report_when_report_generation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """通常レポート生成失敗も `result: error` レポートとして残す。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """レポート生成前までは成功する Codex 実行を模擬する。"""
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    def fake_write_report(*args: object, **kwargs: object) -> Path:
        """通常レポート書き込みだけが失敗する状態を模擬する。"""
        raise OSError("fake report failure")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)
    monkeypatch.setattr(
        review_oracles_module,
        "_write_report",
        fake_write_report,
    )

    with pytest.raises(OSError, match="fake report failure"):
        cmoc_review_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert 'result: "error"' in report
    assert "oracle_count_evaluated: 1" in report
    assert "- Failed stage: `report 書き込み`" in report
    assert "- Exception type: `OSError`" in report
    assert "- Exception message: `fake report failure`" in report
    assert "成功評価ではありません" in report
    assert "今回評価した範囲では問題点が検出されませんでした" not in report
    assert "## Specification-only basis" not in report


def test_eval_oracles_preserves_original_error_when_error_report_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """error report 保存の二次失敗で一次失敗情報を失わない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価中の一次失敗を模擬する。"""
        raise RuntimeError("primary evaluation failure")

    def fake_write_error_report(*args: object, **kwargs: object) -> Path:
        """error report 書き込み自体の二次失敗を模擬する。"""
        raise OSError("secondary report failure")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)
    monkeypatch.setattr(
        review_oracles_module,
        "_write_error_report",
        fake_write_error_report,
    )

    with pytest.raises(RuntimeError, match="primary evaluation failure") as exc_info:
        cmoc_review_oracles_impl(repo, full=True)

    assert [
        "review oracles error report generation also failed: "
        "OSError: secondary report failure"
    ] == exc_info.value.__notes__
    captured = capsys.readouterr()
    assert "cmoc review oracles error report generation failed." in captured.err
    assert "- result: error" in captured.err
    assert "- failed_stage: oracle ファイル評価" in captured.err
    assert "- exception: RuntimeError: primary evaluation failure" in captured.err
    assert "- report_exception: OSError: secondary report failure" in captured.err


def test_eval_oracles_report_aggregates_issues_by_severity(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """レポートはファイル単位ではなく issue 単位で severity 順に集約する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_a = oracle_root / "a.md"
    oracle_b = oracle_root / "b.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle_a.write_text("a\n", encoding="utf-8")
    oracle_b.write_text("b\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """対象 oracle ごとに異なる severity の評価結果を返す。"""
        purpose = str(kwargs["purpose"])
        if "oracles/a.md" in purpose:
            return json.dumps(
                {
                    "issues": [
                        _eval_oracle_issue(
                            "warning",
                            "A warning",
                            oracle_a,
                            3,
                            4,
                            [oracle_a, oracle_index],
                        ),
                        _eval_oracle_issue(
                            "fatal",
                            "A fatal",
                            oracle_a,
                            5,
                            5,
                            [oracle_a, oracle_index],
                        ),
                    ],
                },
                ensure_ascii=False,
            )
        return json.dumps(
            {
                "issues": [
                    _eval_oracle_issue(
                        "inconclusive",
                        "B inconclusive",
                        oracle_b,
                        None,
                        None,
                        [oracle_b, oracle_index],
                    ),
                    _eval_oracle_issue(
                        "fatal",
                        "B fatal",
                        oracle_b,
                        8,
                        9,
                        [oracle_b, oracle_index],
                    ),
                    _eval_oracle_issue(
                        "warning",
                        "B warning",
                        oracle_b,
                        10,
                        10,
                        [oracle_b, oracle_index],
                    ),
                ],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    for field in [
        "schema_version: 1",
        'command: "cmoc review oracles"',
        "generated_at:",
        f'repo_root: "{repo.resolve()}"',
        f'oracle_root: "{oracle_root.resolve()}"',
        'mode: "full"',
        "full_requested: true",
        "branch:",
        "is_cmoc_branch: true",
        "base_commit: null",
        "head_commit:",
        "deleted_oracles_detected: false",
        "oracle_count_total: 2",
        "oracle_count_evaluated: 2",
        "fatal_issue_count: 2",
        "warning_issue_count: 2",
        "inconclusive_issue_count: 1",
        'result: "fatal"',
    ]:
        assert field in report

    expected_sections = [
        "# cmoc review oracles report",
        "## Summary",
        "## Verdict",
        "## Evaluated oracle files",
        "## Fatal issues",
        "## Inconclusive issues",
        "## Warnings",
        "## Referenced files",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
    assert "## Specification-only basis" not in report
    assert report.index("### FATAL-001: A fatal") < report.index(
        "### FATAL-002: B fatal"
    )
    assert report.index("### FATAL-002: B fatal") < report.index(
        "### INCONCLUSIVE-001: B inconclusive"
    )
    assert report.index("### INCONCLUSIVE-001: B inconclusive") < report.index(
        "### WARN-001: A warning"
    )
    assert report.index("### WARN-001: A warning") < report.index(
        "### WARN-002: B warning"
    )
    assert "| 1 | `oracles/a.md` | 2 |" in report
    assert "| 2 | `oracles/b.md` | 3 |" in report
    assert "- Oracle file: `oracles/a.md`" in report
    assert "- Oracle file: `oracles/b.md`" in report
    assert "- Specification-only basis:" in report
    assert "oracles 配下の仕様だけを参照しました。" in report
    assert f"- Oracle file: `{oracle_a.resolve()}`" not in report
    assert f"- Oracle file: `{oracle_b.resolve()}`" not in report
    assert "| No. | Referenced file |" in report
    assert "| 1 | `oracles/a.md` |" in report
    assert "| 2 | `oracles/INDEX.md` |" in report
    assert "| 3 | `oracles/b.md` |" in report
    assert report.count("| 2 | `oracles/INDEX.md` |") == 1


def test_eval_oracles_report_frontmatter_quotes_string_scalars(
    tmp_path: Path,
) -> None:
    """frontmatter の文字列値は YAML 特殊文字を含んでも quote する。"""
    repo = tmp_path / "repo # root: value"
    oracle_root = repo / "oracles"
    oracle_root.mkdir(parents=True)
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    branch_name = "feature: #topic\nquoted \"branch\""
    commit_hash = "abc123: #hash\nnext"

    report_path = review_oracles_module._write_report(
        repo,
        "full",
        True,
        branch_name,
        False,
        None,
        commit_hash,
        False,
        1,
        [oracle_file],
        [],
    )

    frontmatter = report_path.read_text(encoding="utf-8").split("---\n", 2)[1]
    repo_root_value = review_oracles_module._yaml_string(str(repo.resolve()))
    oracle_root_value = review_oracles_module._yaml_string(
        str(oracle_root.resolve())
    )
    branch_value = review_oracles_module._yaml_string(branch_name)
    commit_value = review_oracles_module._yaml_string(commit_hash)
    assert f"repo_root: {repo_root_value}" in frontmatter
    assert f"oracle_root: {oracle_root_value}" in frontmatter
    assert f"branch: {branch_value}" in frontmatter
    assert f"head_commit: {commit_value}" in frontmatter
    assert f"commit: {commit_value}" in frontmatter


def test_eval_oracles_error_report_frontmatter_quotes_string_scalars(
    tmp_path: Path,
) -> None:
    """error report の frontmatter も文字列値を安全な scalar にする。"""
    repo = tmp_path / "repo # root: value"
    oracle_root = repo / "oracles"
    oracle_root.mkdir(parents=True)
    branch_name = "feature: #topic\nquoted \"branch\""
    commit_hash = "abc123: #hash\nnext"

    report_path = review_oracles_module._write_error_report(
        repo,
        "partial: #mode",
        False,
        branch_name,
        None,
        None,
        commit_hash,
        None,
        None,
        [],
        [],
        "stage: #failure",
        RuntimeError("boom"),
    )

    frontmatter = report_path.read_text(encoding="utf-8").split("---\n", 2)[1]
    repo_root_value = review_oracles_module._yaml_string(str(repo.resolve()))
    mode_value = review_oracles_module._yaml_string("partial: #mode")
    branch_value = review_oracles_module._yaml_string(branch_name)
    commit_value = review_oracles_module._yaml_string(commit_hash)
    assert f"repo_root: {repo_root_value}" in frontmatter
    assert f"mode: {mode_value}" in frontmatter
    assert f"branch: {branch_value}" in frontmatter
    assert f"head_commit: {commit_value}" in frontmatter


def test_review_oracles_improves_combined_issue_list(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価後の結合 issue list は指定回数まで改善され、改善後をレポートする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    calls: list[str] = []
    codex_kwargs: list[dict[str, object]] = []

    def issue(title: str) -> dict[str, object]:
        result = _eval_oracle_issue("warning", title, oracle_file, 1, 1)
        result["referenced_paths"] = [str(oracle_file.resolve())]
        result["specification_only_basis"] = "oracles 配下の仕様だけを参照しました。"
        return result

    def fake_codex(*args: object, **kwargs: object) -> str:
        """評価結果を改善呼び出しで置き換える Codex 実行を模擬する。"""
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        codex_kwargs.append(kwargs)
        if "oracle 問題点リスト改善" in purpose:
            return json.dumps(
                {"issues": [issue("Improved warning")]},
                ensure_ascii=False,
            )
        return json.dumps({"issues": [issue("Raw warning")]}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=2)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert calls == [
        "oracle 評価 oracles/spec.md",
        "oracle 問題点リスト改善 1",
        "oracle 問題点リスト改善 2",
    ]
    assert [
        kwargs.get("skip_index_maintenance") for kwargs in codex_kwargs
    ] == [None, None, None]
    improve_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if "oracle 問題点リスト改善" in kwargs["purpose"]
    ]
    assert all(kwargs["model"] == FRONTIER_MODEL for kwargs in improve_kwargs)
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_HIGH_REASONING_EFFORT
        for kwargs in improve_kwargs
    )
    assert "Improved warning" in report
    assert "Raw warning" not in report


def test_review_oracles_rejects_too_many_refine_findings_loops(
    tmp_path: Path,
) -> None:
    """所見リスト検証ループの反復回数は oracle の最大 3 回を超えられない。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(
        ValueError,
        match="--refine-findings-loop must be between 0 and 3",
    ):
        cmoc_review_oracles_impl(repo, scope="full", refine_findings_loop=4)


def test_review_oracles_accepts_improved_issue_for_unevaluated_oracle(
    tmp_path: Path,
) -> None:
    """改善後 issue の oracle_path が評価対象外でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    evaluated_oracle = oracle_root / "evaluated.md"
    unevaluated_oracle = oracle_root / "unevaluated.md"
    evaluated_oracle.write_text("evaluated\n", encoding="utf-8")
    unevaluated_oracle.write_text("unevaluated\n", encoding="utf-8")

    evaluations = [
        {
            "target_oracle_path": str(evaluated_oracle.resolve()),
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
    ]
    improved_issue = _eval_oracle_issue(
        "warning",
        "outside target",
        unevaluated_oracle,
        1,
        1,
    )

    review_oracles_module._validate_issues_payload(
        {"issues": [improved_issue]},
        repo,
        {evaluated_oracle.resolve()},
    )

    redistributed = review_oracles_module._redistribute_improved_issues(
        evaluations,
        [improved_issue],
    )

    assert redistributed[0]["issues"] == [improved_issue]


def test_review_oracles_redistribution_uses_only_final_issue_provenance(
    tmp_path: Path,
) -> None:
    """改善後 report の根拠情報は最終 issue list だけから再計算する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    basis = "元評価は oracles 配下の仕様断片と INDEX だけを参照しました。"
    evaluations = [
        {
            "target_oracle_path": str(oracle.resolve()),
            "referenced_paths": [
                str(oracle.resolve()),
                str(oracle_index.resolve()),
            ],
            "specification_only_basis": basis,
            "issues": [],
        }
    ]
    improved_issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    improved_issue["referenced_paths"] = []
    improved_issue["specification_only_basis"] = ""

    redistributed = review_oracles_module._redistribute_improved_issues(
        evaluations,
        [improved_issue],
    )

    issue = redistributed[0]["issues"][0]
    assert issue["referenced_paths"] == []
    assert issue["specification_only_basis"] == ""
    assert redistributed[0]["referenced_paths"] == []
    assert redistributed[0]["specification_only_basis"] == ""


def test_review_oracles_redistribution_clears_deleted_issue_provenance(
    tmp_path: Path,
) -> None:
    """改善で issue が消えた評価には改善前の根拠情報を残さない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    evaluations = [
        {
            "target_oracle_path": str(oracle.resolve()),
            "referenced_paths": [
                str(oracle.resolve()),
                str(oracle_index.resolve()),
            ],
            "specification_only_basis": (
                "元評価は oracles 配下の仕様断片と INDEX だけを参照しました。"
            ),
            "issues": [_eval_oracle_issue("warning", "warning", oracle, 1, 1)],
        }
    ]

    redistributed = review_oracles_module._redistribute_improved_issues(
        evaluations,
        [],
    )

    assert redistributed == [
        {
            "target_oracle_path": str(oracle.resolve()),
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
    ]


def test_eval_oracles_result_precedence() -> None:
    """result は評価対象数と severity 件数から機械的に決まる。"""
    assert review_oracles_module._evaluation_result(
        0,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "no_targets"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 1, "inconclusive": 1, "warning": 1},
    ) == "fatal"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 1, "warning": 1},
    ) == "inconclusive"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 1},
    ) == "warning"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "ok"


def test_eval_oracles_payload_accepts_existing_oracle_and_index_paths(
    tmp_path: Path,
) -> None:
    """評価 payload は referenced_paths の実在 oracle / INDEX file 参照を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [
                _eval_oracle_issue(
                    "warning",
                    "warning",
                    oracle,
                    1,
                    1,
                    [oracle, oracle_index],
                ),
            ],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_index_as_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path が INDEX.md でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        "fatal",
        "fatal",
        oracle_index,
        1,
        1,
        [oracle, oracle_index],
    )

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_other_oracle_as_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """1 file 評価の issue でも別 oracle への oracle_path をエラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    other_oracle = oracle_root / "other.md"
    oracle.write_text("spec\n", encoding="utf-8")
    other_oracle.write_text("other\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        "fatal",
        "fatal",
        other_oracle,
        1,
        1,
        [oracle, other_oracle],
    )

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_rejects_legacy_top_level_metadata(
    tmp_path: Path,
) -> None:
    """評価 payload は top-level の評価対象メタ情報を受理しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Evaluation payload keys do not match schema",
    ):
        review_oracles_module._validate_evaluation_payload(
            {
                "target_oracle_path": str(oracle.resolve()),
                "referenced_paths": [str(oracle.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_rejects_legacy_issue_metadata(
    tmp_path: Path,
) -> None:
    """issue item は referenced_paths と specification_only_basis を必須にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    del issue["referenced_paths"]
    del issue["specification_only_basis"]

    with pytest.raises(
        ValueError,
        match="issues\\[0\\] keys do not match schema",
    ):
        review_oracles_module._validate_evaluation_payload(
            {"issues": [issue]},
            repo,
            oracle,
        )


def test_eval_oracles_payload_accepts_empty_referenced_paths(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は oracle schema に合わせて空配列を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    issue["referenced_paths"] = []

    review_oracles_module._validate_evaluation_payload(
        {"issues": [issue]},
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_empty_specification_only_basis(
    tmp_path: Path,
) -> None:
    """issues[].specification_only_basis は空文字を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    issue["specification_only_basis"] = ""

    review_oracles_module._validate_evaluation_payload(
        {"issues": [issue]},
        repo,
        oracle,
    )


def test_eval_oracles_payload_rejects_missing_referenced_path(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は存在しない oracles 配下 path を受理しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")

    with pytest.raises(ValueError, match="referenced_paths\\[1\\] must exist"):
        review_oracles_module._validate_evaluation_payload(
            {
                "issues": [
                    _eval_oracle_issue(
                        "warning",
                        "warning",
                        oracle,
                        1,
                        1,
                        [oracle, oracle_root / "missing.md"],
                    ),
                ],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_rejects_directory_referenced_path(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は directory を参照済みファイルにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_dir = oracle_root / "nested"
    oracle_dir.mkdir(parents=True)
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")

    with pytest.raises(ValueError, match="referenced_paths\\[1\\] must be a file"):
        review_oracles_module._validate_evaluation_payload(
            {
                "issues": [
                    _eval_oracle_issue(
                        "warning",
                        "warning",
                        oracle,
                        1,
                        1,
                        [oracle, oracle_dir],
                    ),
                ],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_rejects_ignored_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は .gitignore 対象 oracle file を受理しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    ignored_oracle = oracle_root / "ignored.md"
    oracle.write_text("spec\n", encoding="utf-8")
    ignored_oracle.write_text("ignored\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="referenced_paths\\[1\\] must be an oracle file or INDEX.md",
    ):
        review_oracles_module._validate_evaluation_payload(
            {
                "issues": [
                    _eval_oracle_issue(
                        "warning",
                        "warning",
                        oracle,
                        1,
                        1,
                        [oracle, ignored_oracle],
                    ),
                ],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_accepts_missing_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path が存在しない oracle path でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    missing_oracle = oracle_root / "missing.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("fatal", "fatal", missing_oracle, 1, 1, [oracle])

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_non_oracles_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path が oracles 外でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    implementation_path = repo / "src" / "app.py"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        "fatal",
        "fatal",
        implementation_path,
        1,
        1,
        [oracle],
    )

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_verdict_text_distinguishes_error() -> None:
    """error や未知の result を ok 相当の Verdict にしない。"""
    ok_verdict = review_oracles_module._verdict_text("ok")
    error_verdict = review_oracles_module._verdict_text("error")
    unknown_verdict = review_oracles_module._verdict_text("unexpected")

    assert "問題点が検出されませんでした" in ok_verdict
    assert "成功評価ではありません" in error_verdict
    assert "問題点が検出されませんでした" not in error_verdict
    assert "成功として扱えません" in unknown_verdict
    assert "問題点が検出されませんでした" not in unknown_verdict


def test_eval_oracles_stays_partial_when_oracle_was_deleted(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """削除済み oracle があっても `--full` なしの session branch は部分評価する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    changed_oracle = oracle_root / "changed.md"
    unchanged_oracle = oracle_root / "unchanged.md"
    deleted_oracle = oracle_root / "deleted.md"
    changed_oracle.write_text("before\n", encoding="utf-8")
    unchanged_oracle.write_text("unchanged\n", encoding="utf-8")
    deleted_oracle.write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _checkout_session_branch(repo)
    changed_oracle.write_text("after\n", encoding="utf-8")
    deleted_oracle.unlink()
    _git(repo, "add", "-A", "oracles")
    _git(repo, "commit", "-m", "change session oracles")

    evaluated_prompts: list[str] = []
    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """部分評価対象の prompt を記録し、不整合なしの結果を返す。"""
        evaluated_prompts.append(str(args[1]))
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=False)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    report = reports[0].read_text(encoding="utf-8")
    assert len(evaluated_prompts) == 1
    assert str(changed_oracle) in evaluated_prompts[0]
    assert str(unchanged_oracle) not in evaluated_prompts[0]
    assert 'mode: "partial"' in report
    assert "deleted_oracles_detected: true" in report
    assert "oracle_count: 1" in report


def test_eval_oracles_full_mode_requires_valid_session_state(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """session branch 上の full mode でも session state を検証する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    existing_oracle = oracle_root / "existing.md"
    deleted_oracle = oracle_root / "deleted.md"
    existing_oracle.write_text("existing\n", encoding="utf-8")
    deleted_oracle.write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _checkout_session_branch(repo)
    deleted_oracle.unlink()
    session_state = next((repo / ".cmoc" / "sessions").glob("*.json"))
    session_state.write_text("{broken\n", encoding="utf-8")

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """full mode の既存 oracle 評価結果を返す。"""
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "session state ファイルの JSON が不正です。" in error.value.message


def test_eval_oracles_rejects_non_session_branch(tmp_path: Path) -> None:
    """通常 branch 上の `review oracles` は事前条件違反として拒否する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "oracles")
    _git(repo, "commit", "-m", "prepare clean normal branch")

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "`cmoc review oracles` は session branch 上で実行してください。" in (
        error.value.message
    )
    assert "現在の branch:" in error.value.detail


def test_eval_oracles_rejects_missing_session_state(tmp_path: Path) -> None:
    """session state file がない session branch では実行しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    next((repo / ".cmoc" / "sessions").glob("*.json")).unlink()

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "session state ファイルが見つかりませんでした。" in error.value.message


def test_eval_oracles_rejects_inactive_session_state(tmp_path: Path) -> None:
    """session.state が active でない session branch では実行しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    state_path = next((repo / ".cmoc" / "sessions").glob("*.json"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["state"] = "joined"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "active な session ではありません。" in error.value.message
    assert "session.state: joined" in error.value.detail


def test_eval_oracles_rejects_uncommitted_changes(tmp_path: Path) -> None:
    """git 未コミット差分がある session branch では実行しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    oracle_file.write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "未コミットの変更があります。" in error.value.message
    assert "oracles/spec.md" in error.value.detail


def test_eval_oracles_rejects_apply_branch(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply branch 上の `review oracles` は事前条件違反として拒否する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    changed_oracle = oracle_root / "changed.md"
    unchanged_oracle = oracle_root / "unchanged.md"
    changed_oracle.write_text("before\n", encoding="utf-8")
    unchanged_oracle.write_text("unchanged\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _git(
        repo,
        "checkout",
        "-b",
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123",
    )
    changed_oracle.write_text("after\n", encoding="utf-8")

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    evaluated_targets: list[Path] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """評価 prompt 内の対象 oracle に対応した結果を返す。"""
        prompt = str(args[1])
        target = (
            changed_oracle
            if str(changed_oracle.resolve()) in prompt
            else unchanged_oracle
        )
        evaluated_targets.append(target)
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=False)

    assert "`cmoc review oracles` は session branch 上で実行してください。" in (
        error.value.message
    )
    assert evaluated_targets == []


def test_review_oracles_body_uses_command_path_module_name() -> None:
    """`review oracles` の本体はコマンド path 対応のモジュールに置く。"""
    repo_root = Path(__file__).resolve().parents[1]

    body = repo_root / "src" / "sub_commands" / "review" / "oracles.py"
    legacy = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    body_text = body.read_text(encoding="utf-8")
    assert "def cmoc_review_oracles_impl" in body_text
    assert "spec_from_file_location" not in body_text
    assert not legacy.exists()


def test_eval_oracles_validation_helpers_are_ordered_caller_first() -> None:
    """同一ファイル内の validation helper は caller first に並べる。"""
    repo_root = Path(__file__).resolve().parents[1]
    source = (
        repo_root / "src" / "sub_commands" / "review" / "oracles.py"
    ).read_text(encoding="utf-8")

    callee = source.index("def _require_issue_oracle_path_string(")
    assert source.index("def _validate_evaluation_payload(") < callee
    assert source.index("def _validate_referenced_paths(") < callee
    assert source.index("def _validate_evaluation_issues(") < callee


def test_eval_oracles_prompt_forbids_implementation_references() -> None:
    """評価 prompt は仕様だけから致命的問題を判断させる。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))

    assert "`/repo/oracles` 外のファイルは一切参照禁止です。" in prompt
    assert "`/repo/oracles/INDEX.md` から始まる INDEX.md" in prompt
    assert "`oracles` 外のファイルは一切参照禁止です。" not in prompt
    assert "`oracles/INDEX.md`" not in prompt
    assert "INDEX.md は自動生成されるため評価対象ではありません。" in prompt
    assert "INDEX.md は関連ファイル選定・参照根拠としてだけ読んでください。" in prompt
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt
    assert "各 issue の referenced_paths には参照した仕様ファイル" in prompt
    assert "Structured Output schema に一致する JSON" in prompt
    assert "仕様だけから判断・実装したとき" in prompt


def test_eval_oracles_improvement_prompt_uses_index_routing() -> None:
    """改善 prompt も INDEX のルーティング情報で関連 oracle を選定させる。"""
    prompt = _improvement_prompt(
        Path("/repo"),
        {
            "issues": [
                {
                    "oracle_path": "/repo/oracles/spec.md",
                    "referenced_paths": ["/repo/oracles/INDEX.md"],
                }
            ]
        },
    )

    assert "`/repo/oracles/INDEX.md` から始まる INDEX.md" in prompt
    assert "Read this when / Do not read this when を根拠に、" in prompt
    assert "関連する仕様ファイルを選定してください。" in prompt
    assert "`/repo/oracles` 外のファイルは一切参照禁止です。" in prompt
    assert "`oracles/INDEX.md`" not in prompt
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt


def test_eval_oracles_prompt_orders_completion_before_details() -> None:
    """評価 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア仕様のレビュー担当です。"
    assert lines[1] == (
        "`/repo` 内の仕様ファイル `/repo/oracles/spec.md` を評価してください。"
    )
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "issues には検出した問題点を入れ、問題がない場合は空配列を返してください。"
    ) > 2


def test_eval_oracles_improvement_prompt_orders_completion_before_snapshot_details() -> None:
    """snapshot 付き改善 prompt も完了条件を詳細指示より前に置く。"""
    snapshot = review_oracles_module._OracleEvaluationSnapshot(
        original_repo_root=Path("/repo"),
        original_oracle_root=Path("/repo/oracles"),
        snapshot_root=Path("/snapshot"),
        snapshot_oracle_root=Path("/snapshot/oracles"),
        oracle_files=frozenset({Path("/repo/oracles/spec.md")}),
        reference_files=frozenset({Path("/repo/oracles/spec.md")}),
    )
    prompt = _improvement_prompt(
        Path("/repo"),
        {
            "issues": [
                {
                    "oracle_path": "/repo/oracles/spec.md",
                    "referenced_paths": ["/repo/oracles/INDEX.md"],
                }
            ]
        },
        snapshot,
    )
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア仕様レビュー結果の整理担当です。"
    assert lines[1] == (
        "`/repo` の仕様評価で得られた問題点リストを改善してください。"
    )
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "必要に応じて読む仕様ファイル群は、開始時点の内容を固定したコピー "
        "`/snapshot/oracles` です。"
    ) > 2


def test_apply_returns_complete_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` は不整合なし JSON で完了扱いのレポートを保存する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    codex_kwargs: list[dict[str, object]] = []
    codex_prompts: list[str] = []
    event_order: list[str] = []
    original_mark_apply_completed = apply_module._mark_apply_completed
    original_write_apply_report = apply_module._write_apply_report

    def record_mark_apply_completed(*args: object, **kwargs: object) -> None:
        event_order.append("apply 完了記録")
        original_mark_apply_completed(*args, **kwargs)

    def record_write_apply_report(*args: object, **kwargs: object) -> Path:
        event_order.append("report 書き込み")
        return original_write_apply_report(*args, **kwargs)

    monkeypatch.setattr(
        apply_module,
        "_mark_apply_completed",
        record_mark_apply_completed,
    )
    monkeypatch.setattr(
        apply_module,
        "_write_apply_report",
        record_write_apply_report,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、変更要約なら summary JSON を返す。"""
        codex_kwargs.append(kwargs)
        codex_prompts.append(str(args[1]))
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return _apply_report(str(args[1]), "収束", [0])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert exit_code == 0
    assert len(reports) == 1
    assert state["apply"]["state"] == "completed"
    assert event_order == ["report 書き込み", "apply 完了記録"]
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert state["apply"]["oracle_snapshot_commit"] == _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    apply_run_id = state["apply"]["apply_branch"].rsplit("/", 1)[1]
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "2026-05-10_22-21_10_000000123"
        / apply_run_id
    )
    assert apply_worktree.is_dir()
    assert set(state["apply"]) == {
        "state",
        "apply_branch",
        "oracle_snapshot_commit",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert report_text.startswith("---\n")
    session_fork_commit = state["session"]["session_start_commit"]
    assert "cmoc_session_id: \"2026-05-10_22-21_10_000000123\"" in report_text
    assert "cmoc_apply_run_id: " in report_text
    assert (
        "cmoc_session_branch: \"cmoc/session/2026-05-10_22-21_10_000000123\""
        in report_text
    )
    assert (
        f"cmoc_session_fork_commit: \"{session_fork_commit}\""
        in report_text
    )
    assert (
        "cmoc_apply_branch: \"cmoc/apply/2026-05-10_22-21_10_000000123/"
        in report_text
    )
    apply_fork_commit = state["apply"]["oracle_snapshot_commit"]
    assert f"cmoc_apply_fork_commit: \"{apply_fork_commit}\"" in report_text
    assert "apply_worktree_path: " in report_text
    assert "oracle_snapshot_commit: " in report_text
    assert "session_head_at_apply_start: " in report_text
    assert "session_head_at_apply_finish: " in report_text
    assert f"session_head_at_apply_start: \"{session_head}\"" in report_text
    assert f"session_head_at_apply_finish: \"{session_head}\"" in report_text
    assert "## 作業結果" in report_text
    assert "## 要修正点件数の推移" in report_text
    assert "全変更内容" in report_text
    assert codex_kwargs[0]["output_schema"] == _DISCREPANCY_OUTPUT_SCHEMA
    assert "fixing_points" in codex_prompts[0]
    assert "実装だけから見た成果物品質上の致命的な問題" in codex_prompts[0]
    assert "oracle_requirement" in codex_prompts[0]
    investigation_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if str(kwargs.get("purpose", "")).startswith("oracle 調査 ")
        or str(kwargs.get("purpose", "")).startswith("実装調査 ")
    ]
    investigation_purposes = [
        str(kwargs.get("purpose", "")) for kwargs in investigation_kwargs
    ]
    assert investigation_kwargs
    assert any(
        purpose.startswith("oracle 調査 ")
        for purpose in investigation_purposes
    )
    assert any(
        purpose.startswith("実装調査 ")
        for purpose in investigation_purposes
    )
    assert all(
        kwargs["model"] == FRONTIER_MODEL
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_REASONING_EFFORT
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs.get("skip_index_maintenance") is not True
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs["index_excluded_roots"] == [apply_worktree / "oracles"]
        for kwargs in investigation_kwargs
    )
    report_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if kwargs.get("purpose") == "apply 変更要約"
    ]
    assert report_kwargs == []
    assert "カテゴリ: 変更なし" in report_text
    assert (
        "今回の自動適用処理以前の作業も含めてください"
        not in "\n".join(codex_prompts)
    )


def test_apply_investigates_file_origin_targets_in_parallel(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork の file 起点調査は事前列挙対象を N+M 並列で実行する。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (repo / "app.py").write_text("print('hello')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "targets")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    active = 0
    max_active = 0
    lock = threading.Lock()
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査呼び出しが重なっているかを記録する。"""
        nonlocal active
        nonlocal max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
            codex_kwargs.append(kwargs)
        try:
            time.sleep(0.05)
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        finally:
            with lock:
                active -= 1

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    discrepancies = apply_module._investigate_discrepancies(
        repo,
        base_commit,
        oracle_snapshot_commit,
        timer=StepTimer("test"),
        step_path=((1, 1),),
        repeat_improove_fixing_list=0,
        scope="session",
    )

    purposes = [str(kwargs.get("purpose", "")) for kwargs in codex_kwargs]
    assert discrepancies == []
    assert len(codex_kwargs) >= 2
    assert max_active >= 2
    assert any(purpose.startswith("oracle 調査 ") for purpose in purposes)
    assert any(
        purpose.startswith("実装調査 ")
        for purpose in purposes
    )
    assert all(kwargs["model"] == FRONTIER_MODEL for kwargs in codex_kwargs)
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_REASONING_EFFORT
        for kwargs in codex_kwargs
    )


def test_apply_scope_rolling_uses_last_joined_oracle_snapshot(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """rolling scope は最後に join された oracle snapshot 以降だけを調査する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("old spec\n", encoding="utf-8")
    (repo / "old.py").write_text("print('old')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old targets")
    last_joined_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()

    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["last_joined_apply_oracle_snapshot_commit"] = (
        last_joined_snapshot
    )
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)

    (oracle_root / "new.md").write_text("new spec\n", encoding="utf-8")
    (repo / "new.py").write_text("print('new')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "new targets")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        purpose = str(kwargs.get("purpose"))
        purposes.append(purpose)
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return '{"git_head_commit_hash": null, "fixing_points": []}'

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=0,
    ) == 0

    assert any(purpose.endswith("oracles/new.md") for purpose in purposes)
    assert any(purpose.endswith("new.py") for purpose in purposes)
    assert not any(purpose.endswith("oracles/old.md") for purpose in purposes)
    assert not any(purpose.endswith("old.py") for purpose in purposes)


def test_apply_scope_target_selection_supports_session_and_full(
    tmp_path: Path,
) -> None:
    """session scope と full scope は仕様通り差分対象・全件対象を選べる。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("old spec\n", encoding="utf-8")
    (repo / "old.py").write_text("print('old')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old targets")
    last_joined_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "new.md").write_text("new spec\n", encoding="utf-8")
    (repo / "new.py").write_text("print('new')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "new targets")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    session_oracles = apply_module._target_oracle_files(
        repo,
        base_commit,
        oracle_snapshot_commit,
        partial=True,
    )
    session_impls = apply_module._target_implementation_files(
        repo,
        base_commit,
        oracle_snapshot_commit,
        partial=True,
    )
    rolling_oracles = apply_module._target_oracle_files(
        repo,
        last_joined_snapshot,
        oracle_snapshot_commit,
        partial=True,
    )
    rolling_impls = apply_module._target_implementation_files(
        repo,
        last_joined_snapshot,
        oracle_snapshot_commit,
        partial=True,
    )
    full_oracles = apply_module._target_oracle_files(
        repo,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        partial=False,
    )
    full_impls = apply_module._target_implementation_files(
        repo,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        partial=False,
    )

    assert {target.path.name for target in session_oracles} == {
        "old.md",
        "new.md",
    }
    assert {"old.py", "new.py"} <= {
        target.path.name for target in session_impls
    }
    assert {target.path.name for target in rolling_oracles} == {"new.md"}
    assert {"new.py"} <= {target.path.name for target in rolling_impls}
    assert {"old.md", "new.md"} <= {target.path.name for target in full_oracles}
    assert {"old.py", "new.py"} <= {target.path.name for target in full_impls}


def test_apply_commits_index_changes_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """不整合 0 件でも apply worktree の INDEX 差分を commit して完了する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    maintained_roots: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """apply worktree の初回 INDEX メンテナンスだけ差分を作る。"""
        maintained_roots.append(repo_root)
        if not (repo_root / ".git").is_file():
            return False
        index_path = repo_root / "docs" / "INDEX.md"
        if index_path.exists():
            return False
        index_path.parent.mkdir()
        index_path.write_text("# `docs`\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査、commit message、変更要約生成を目的別に返す。"""
        codex_kwargs.append(kwargs)
        if kwargs.get("purpose") == "commit message 生成":
            return "Maintain apply indexes"
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return _apply_report(str(args[1]), "収束", [0])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    apply_run_id = state["apply"]["apply_branch"].rsplit("/", 1)[1]
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "2026-05-10_22-21_10_000000123"
        / apply_run_id
    )
    report_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if kwargs.get("purpose") == "apply 変更要約"
    ]
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    assert len(reports) == 1
    report_text = reports[0].read_text(encoding="utf-8")
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()

    assert exit_code == 0
    assert state["apply"]["state"] == "completed"
    assert _git(apply_worktree, "status", "--porcelain").stdout == ""
    assert _git(apply_worktree, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Maintain apply indexes"
    )
    assert _git(apply_worktree, "show", "HEAD:docs/INDEX.md").stdout == (
        "# `docs`\n"
    )
    assert len(report_kwargs) == 1
    assert report_kwargs[0].get("skip_index_maintenance") is not True
    assert report_kwargs[0]["index_excluded_roots"] == [
        apply_worktree / "oracles"
    ]
    assert maintained_roots.count(apply_worktree) == 2
    assert f"session_head_at_apply_start: \"{session_head}\"" in report_text
    assert f"session_head_at_apply_finish: \"{session_head}\"" in report_text
    assert session_head != apply_head
    assert f"session_head_at_apply_finish: \"{apply_head}\"" not in report_text


def test_apply_report_records_session_head_at_finish_when_session_advances(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork は終了時点の session branch HEAD を report に記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head_at_start = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    advanced_session = False
    advance_lock = threading.Lock()

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査中に session branch を進め、調査自体は収束させる。"""
        nonlocal advanced_session
        if kwargs.get("expect_json") is True:
            with advance_lock:
                if not advanced_session:
                    (repo / "session-progress.txt").write_text(
                        "session advanced\n",
                        encoding="utf-8",
                    )
                    _git(repo, "add", "session-progress.txt")
                    _git(repo, "commit", "-m", "advance session during apply")
                    advanced_session = True
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        return "No changes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    session_head_at_finish = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()

    assert exit_code == 0
    assert len(reports) == 1
    assert session_head_at_start != session_head_at_finish
    assert session_head_at_finish != apply_head
    assert (
        f"session_head_at_apply_start: \"{session_head_at_start}\""
        in report_text
    )
    assert (
        f"session_head_at_apply_finish: \"{session_head_at_finish}\""
        in report_text
    )
    assert f"session_head_at_apply_finish: \"{apply_head}\"" not in report_text


def test_apply_join_merges_completed_apply_branch_and_resets_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply join` は apply branch を session branch へ merge する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] == (
        oracle_snapshot
    )
    assert "last_joined_apply_result" not in state["session"]
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()
    assert "joined apply branch:" in output


def test_apply_join_rejects_cross_session_apply_branch_without_merge(
    tmp_path: Path,
) -> None:
    """apply join は別 session の apply branch を merge しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _create_completed_apply_run(repo, oracle_snapshot)
    other_session_id = "2026-05-10_22-21_10_000000999"
    other_apply_run_id = "2026-05-10_22-22_10_000000123"
    other_apply_branch = f"cmoc/apply/{other_session_id}/{other_apply_run_id}"
    other_apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / other_session_id
        / other_apply_run_id
    )
    _git(repo, "branch", other_apply_branch, oracle_snapshot)
    _git(repo, "worktree", "add", str(other_apply_worktree), other_apply_branch)
    (other_apply_worktree / "foreign.txt").write_text(
        "foreign\n",
        encoding="utf-8",
    )
    _git(other_apply_worktree, "add", "foreign.txt")
    _git(other_apply_worktree, "commit", "-m", "foreign implementation")
    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["apply_branch"] = other_apply_branch
    state["apply"]["oracle_snapshot_commit"] = oracle_snapshot
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "同じ session の apply branch" in error_info.value.actions[0]
    assert not (repo / "foreign.txt").exists()
    assert _git(repo, "branch", "--list", other_apply_branch).stdout.strip()
    assert other_apply_worktree.exists()


def test_apply_join_cleans_worktree_created_under_linked_worktree_repo_root(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """linked worktree で fork した apply run は linked repo-root 側で cleanup する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")
    cmoc_session_fork_impl(linked)
    session_branch = _git(linked, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    oracle_root = linked / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(linked, "add", "oracles/spec.md")
    _git(linked, "commit", "-m", "add oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査を要修正点なしとして完了させる。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "No changes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(linked)

    state_path = linked / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    apply_branch = state["apply"]["apply_branch"]
    oracle_snapshot = state["apply"]["oracle_snapshot_commit"]
    apply_run_id = apply_branch.rsplit("/", 1)[1]
    apply_worktree = linked / ".cmoc" / "worktrees" / session_id / apply_run_id
    main_apply_worktree = repo / ".cmoc" / "worktrees" / session_id / apply_run_id
    reports = list(
        (linked / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    assert exit_code == 0
    assert apply_worktree.is_dir()
    assert not main_apply_worktree.exists()
    assert len(reports) == 1
    assert f'apply_worktree_path: "{apply_worktree}"' in reports[0].read_text(
        encoding="utf-8"
    )

    _git(linked, "switch", session_branch)
    cmoc_apply_join_impl(linked)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert isinstance(state["session"]["session_home_branch"], str)
    assert state["session"]["session_home_branch"]
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] == (
        oracle_snapshot
    )
    assert "last_joined_apply_result" not in state["session"]
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert state_path.exists()


def test_apply_join_keeps_artifacts_when_report_result_is_missing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """result 保存済みを確認できない場合、merge 後も apply artifacts は残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    expected_apply_branch = (
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    )
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
        report_text="\n".join(
            [
                "---",
                f'cmoc_apply_branch: "{expected_apply_branch}"',
                "---",
                "",
                "## 作業結果",
                "収束",
                "",
            ]
        ),
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert "last_joined_apply_result" not in state["session"]
    assert apply_branch in _git(repo, "branch", "--list", apply_branch).stdout
    assert apply_worktree.exists()
    assert report_path.exists()
    assert "warning: apply cleanup skipped:" in output


def test_apply_join_cleans_artifacts_without_session_result_field(
    tmp_path: Path,
) -> None:
    """cleanup は session state に apply result を永続化せず report metadata で判定する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert "last_joined_apply_result" not in state["session"]
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()


def test_apply_join_keeps_branch_when_worktree_remove_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply worktree 削除に失敗した場合は branch 削除へ進まない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    original_run_git = apply_join_module.run_git
    branch_delete_attempted = False

    def fail_worktree_remove(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        nonlocal branch_delete_attempted
        if args == ["worktree", "remove", str(apply_worktree)]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                "",
                "simulated worktree remove failure",
            )
        if args == ["branch", "-d", apply_branch]:
            branch_delete_attempted = True
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(apply_join_module, "run_git", fail_worktree_remove)

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert apply_branch in _git(repo, "branch", "--list", apply_branch).stdout
    assert apply_worktree.exists()
    assert not branch_delete_attempted
    assert "warning: apply worktree was not deleted:" in output


def test_apply_join_ignores_worktree_local_log_cmoc(
    tmp_path: Path,
) -> None:
    """apply worktree 内のログ用 `.cmoc` ではなく所有元の state を読む。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / ".cmoc" / "logs" / "sub_commands").mkdir(parents=True)
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_join_stops_on_unexpected_diff_in_normal_mode(
    tmp_path: Path,
) -> None:
    """通常モードの apply join は想定外差分を報告して停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "oracles" / "spec.md").write_text(
        "unexpected oracle edit\n",
        encoding="utf-8",
    )
    _git(apply_worktree, "add", "oracles/spec.md")
    _git(apply_worktree, "commit", "-m", "edit oracle unexpectedly")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        in error_info.value.detail
    )
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_apply_branch_non_implementation_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の非実装ファイル変更は想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt")
    _git(apply_worktree, "commit", "-m", "edit non implementation file")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in error_info.value.detail
    )
    assert not (repo / "ignored.txt").exists()
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        (".agents/note.txt", "joined agents note\n"),
        (".cmoc/state.json", "{}\n"),
        ("memo/note.md", "joined memo note\n"),
    ],
)
def test_apply_join_stops_on_apply_branch_forbidden_diff(
    tmp_path: Path,
    relative_path: str,
    content: str,
) -> None:
    """apply fork/Codex CLI の禁止 path は apply branch 成果物にしない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    repo_target = repo / relative_path
    before_exists = repo_target.exists()
    before_content = (
        repo_target.read_text(encoding="utf-8") if before_exists else None
    )
    target = apply_worktree / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    _git(apply_worktree, "add", "-f", relative_path)
    _git(apply_worktree, "commit", "-m", "edit forbidden path")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert repo_target.exists() is before_exists
    if before_content is not None:
        assert repo_target.read_text(encoding="utf-8") == before_content
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("README.md", "joined readme\n"),
        ("AGENTS.md", "joined agents\n"),
    ],
)
def test_apply_join_rejects_root_doc_implementation_diff(
    tmp_path: Path,
    relative_path: str,
    content: str,
) -> None:
    """root の README/AGENTS は apply join の実装差分として取り込まない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    repo_target = repo / relative_path
    before_exists = repo_target.exists()
    before_content = (
        repo_target.read_text(encoding="utf-8") if before_exists else None
    )
    target = apply_worktree / relative_path
    target.write_text(content, encoding="utf-8")
    _git(apply_worktree, "add", relative_path)
    _git(apply_worktree, "commit", "-m", "edit root doc implementation file")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert repo_target.exists() is before_exists
    if before_content is not None:
        assert repo_target.read_text(encoding="utf-8") == before_content


def test_apply_join_reports_unexpected_diff_with_control_chars(
    tmp_path: Path,
) -> None:
    """apply join の想定外差分検査は改行・tab を含む path を壊さない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored*\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation files")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    relative_path = "ignored\nline\tname.md"
    (apply_worktree / relative_path).write_text("note\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", relative_path)
    _git(apply_worktree, "commit", "-m", "edit odd ignored path")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: "
        f"{json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert "\tignored" not in error_info.value.detail
    assert json.dumps((repo / relative_path).resolve().as_posix()) in (
        error_info.value.detail
    )


def test_apply_join_accepts_apply_branch_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の cmoc 管理 INDEX.md 差分は merge 対象にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(apply_worktree, "add", "INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain index")

    cmoc_apply_join_impl(repo)

    assert (repo / "INDEX.md").read_text(encoding="utf-8") == "index\n"


def test_apply_join_stops_on_apply_branch_memo_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の root memo/INDEX.md は想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(apply_worktree, "add", "memo/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain memo index")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'memo/INDEX.md').resolve().as_posix())}"
        in error_info.value.detail
    )


@pytest.mark.parametrize(
    "relative_path",
    [".cache/INDEX.md", ".cache/nested/INDEX.md"],
)
def test_apply_join_stops_on_apply_branch_unmaintained_index_diff(
    tmp_path: Path,
    relative_path: str,
) -> None:
    """apply branch 側の配置対象外 INDEX.md 差分は想定外として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    index_path = apply_worktree / relative_path
    index_path.parent.mkdir(parents=True)
    index_path.write_text("index\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", relative_path)
    _git(apply_worktree, "commit", "-m", "maintain untracked index")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert not (repo / relative_path).exists()


def test_apply_join_accepts_apply_branch_oracles_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の oracles/INDEX.md 差分は merge 対象にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "oracles" / "INDEX.md").write_text(
        "index\n",
        encoding="utf-8",
    )
    _git(apply_worktree, "add", "oracles/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain oracle index")

    cmoc_apply_join_impl(repo)

    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == (
        "index\n"
    )


def test_apply_join_accepts_session_branch_oracles_index_diff(
    tmp_path: Path,
) -> None:
    """session branch 側の oracles/INDEX.md 差分は想定内として扱う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    (repo / "oracles" / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(repo, "add", "oracles/INDEX.md")
    _git(repo, "commit", "-m", "maintain oracle index on session")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == "index\n"
    assert state["apply"]["state"] == "ready"


def test_apply_join_accepts_session_branch_new_oracle_file(
    tmp_path: Path,
) -> None:
    """session branch 側の新規 oracle ファイル追加は想定内として扱う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    new_oracle = repo / "oracles" / "new_spec.md"
    new_oracle.write_text("new spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/new_spec.md")
    _git(repo, "commit", "-m", "add oracle on session")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert new_oracle.read_text(encoding="utf-8") == "new spec\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"


def test_apply_join_accepts_session_branch_memo_diff(
    tmp_path: Path,
) -> None:
    """session branch 側の root memo 差分は想定内として扱う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    _git(repo, "add", "memo/note.md")
    _git(repo, "commit", "-m", "edit memo on session")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "memo" / "note.md").read_text(encoding="utf-8") == "note\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"


def test_apply_join_stops_on_session_branch_ignored_oracle_diff(
    tmp_path: Path,
) -> None:
    """session branch 側でも root .gitignore 対象の oracle 配下差分は停止する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore oracle path")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, _apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "oracles" / "ignored.md").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", "-f", "oracles/ignored.md")
    _git(repo, "commit", "-m", "edit ignored oracle path")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{session_branch}: "
        f"{json.dumps((repo / 'oracles/ignored.md').resolve().as_posix())}"
        in error_info.value.detail
    )


def test_apply_join_force_resolve_keeps_expected_apply_index_diff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは想定内差分だけを維持し、禁止 path は戻す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    (apply_worktree / "INDEX.md").write_text("index\n", encoding="utf-8")
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt", "INDEX.md", "memo/note.md")
    _git(apply_worktree, "commit", "-m", "implement with index and memo")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "INDEX.md").read_text(encoding="utf-8") == "index\n"
    assert not (repo / "memo" / "note.md").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'memo/note.md').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_keeps_session_branch_new_oracle_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードも session branch 側の新規 oracle ファイル追加を戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    new_oracle = repo / "oracles" / "new_spec.md"
    new_oracle.write_text("new spec\n", encoding="utf-8")
    (repo / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
    _git(repo, "add", "oracles/new_spec.md", "unexpected.txt")
    _git(repo, "commit", "-m", "edit session during apply")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert new_oracle.read_text(encoding="utf-8") == "new spec\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "unexpected.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'feature.txt').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / 'unexpected.txt').resolve().as_posix())}"
        in output
    )
    assert "oracles/new_spec.md" not in output


def test_apply_join_auto_resolves_index_conflict(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """INDEX.md だけの merge conflict は削除で自動解決する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (repo / "INDEX.md").write_text("session index\n", encoding="utf-8")
    _git(repo, "add", "INDEX.md")
    _git(repo, "commit", "-m", "maintain session index")
    (apply_worktree / "INDEX.md").write_text("apply index\n", encoding="utf-8")
    _git(apply_worktree, "add", "INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain apply index")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert not (repo / "INDEX.md").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert "auto-resolved INDEX.md conflicts:" in output
    assert f"- {json.dumps((repo / 'INDEX.md').resolve().as_posix())}" in output


def test_apply_join_unmerged_paths_are_nul_safe(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """unmerged path 取得は改行・tab を含む path を token のまま返す。"""
    repo = _init_repo(tmp_path)
    calls: list[list[str]] = []

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        del check, text, input_text, env
        calls.append(args)
        return subprocess.CompletedProcess(
            ["git", *args],
            0,
            "dir/a\nb/INDEX.md\0feature\tfile.txt\0",
            "",
        )

    monkeypatch.setattr(apply_join_module, "run_git", fake_run_git)

    assert apply_join_module._unmerged_paths(repo) == [
        "dir/a\nb/INDEX.md",
        "feature\tfile.txt",
    ]
    assert calls == [["diff", "--name-only", "-z", "--diff-filter=U"]]


def test_apply_join_resolves_index_conflict_before_reporting_other_conflict(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """混在 conflict では INDEX.md だけ自動解決し、他 path は報告する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    (apply_worktree / "INDEX.md").write_text("apply index\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt", "INDEX.md")
    _git(apply_worktree, "commit", "-m", "implement feature with index")
    original_run_git = apply_join_module.run_git
    removed_index = False

    def fail_merge_with_mixed_conflicts(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        nonlocal removed_index
        if args == ["merge", "--no-ff", apply_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                "",
                "\n".join(
                    [
                        "CONFLICT (content): Merge conflict in INDEX.md",
                        "CONFLICT (content): Merge conflict in feature.txt",
                    ]
                ),
            )
        if args == ["rm", "--ignore-unmatch", "--", "INDEX.md"]:
            removed_index = True
            return subprocess.CompletedProcess(["git", *args], 0, "", "")
        if args == ["commit", "--no-edit"]:
            pytest.fail("non INDEX.md conflict が残る場合は merge commit しない")
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def mixed_unmerged_paths(_repo: Path) -> list[str]:
        if removed_index:
            return ["feature.txt"]
        return ["INDEX.md", "feature.txt"]

    monkeypatch.setattr(apply_join_module, "run_git", fail_merge_with_mixed_conflicts)
    monkeypatch.setattr(apply_join_module, "_unmerged_paths", mixed_unmerged_paths)

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert removed_index
    assert json.dumps((repo / "feature.txt").resolve().as_posix()) in (
        error_info.value.detail
    )
    assert json.dumps((repo / "INDEX.md").resolve().as_posix()) not in (
        error_info.value.detail
    )
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_non_index_conflict(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md 以外の conflict は自動解決せず state を維持する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    original_run_git = apply_join_module.run_git

    def fail_merge_with_feature_conflict(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        if args == ["merge", "--no-ff", apply_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                "",
                "CONFLICT (content): Merge conflict in feature.txt",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(apply_join_module, "run_git", fail_merge_with_feature_conflict)
    monkeypatch.setattr(
        apply_join_module,
        "_unmerged_paths",
        lambda _repo: ["feature.txt"],
    )

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict" in error_info.value.message
    assert json.dumps((repo / "feature.txt").resolve().as_posix()) in (
        error_info.value.detail
    )
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_apply_branch_rename_from_oracle_to_implementation(
    tmp_path: Path,
) -> None:
    """apply branch 側の oracle source rename は想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(apply_worktree, "mv", "oracles/spec.md", "feature.txt")
    _git(apply_worktree, "commit", "-m", "rename oracle to implementation")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        in error_info.value.detail
    )
    assert not (repo / "feature.txt").exists()
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert state["apply"]["state"] == "completed"


def test_apply_join_force_resolves_apply_branch_non_implementation_diff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply branch 側の非実装ファイル変更を revert して merge する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected ignored file")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "ignored.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_uses_snapshot_gitignore_for_apply_paths(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """session 側の後続 .gitignore 変更で apply 成果物を誤って戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    (repo / ".gitignore").write_text("/feature.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore feature on session")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / ".gitignore").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'feature.txt').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / '.gitignore').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_uses_snapshot_gitignore_for_apply_indexes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """session 側の後続 .gitignore 変更で apply 側 INDEX.md を誤って戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    _add_oracle_snapshot(repo)
    docs = repo / "docs"
    docs.mkdir()
    (docs / "source.txt").write_text("source\n", encoding="utf-8")
    _git(repo, "add", "docs/source.txt")
    _git(repo, "commit", "-m", "add indexed directory")
    oracle_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    apply_docs = apply_worktree / "docs"
    (apply_docs / "INDEX.md").write_text("apply index\n", encoding="utf-8")
    _git(apply_worktree, "add", "docs/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain docs index")
    (repo / ".gitignore").write_text("/docs/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore docs on session")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == (
        "apply index\n"
    )
    assert not (repo / ".gitignore").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'docs' / 'INDEX.md').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / '.gitignore').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolves_apply_branch_rename_from_oracle(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは oracle source rename の source/destination を戻す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "other.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "other.txt")
    _git(apply_worktree, "commit", "-m", "implement other feature")
    _git(apply_worktree, "mv", "oracles/spec.md", "feature.txt")
    _git(apply_worktree, "commit", "-m", "rename oracle to implementation")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "other.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "feature.txt").exists()
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolves_with_missing_apply_worktree(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply worktree 欠落時も一時 worktree で revert する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected ignored file")
    _git(repo, "worktree", "remove", "--force", str(apply_worktree))

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "ignored.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert list((repo / ".cmoc" / "worktrees" / "tmp").glob("*")) == []
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolves_from_apply_branch_without_apply_worktree(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは現在の apply branch worktree で想定外差分を revert する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected ignored file")
    _git(repo, "worktree", "remove", "--force", str(apply_worktree))
    _git(repo, "switch", apply_branch)

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "ignored.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert not (repo / ".cmoc" / "worktrees" / "tmp").exists()
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in output
    )


def test_apply_join_accepts_apply_branch_copy_to_expected_path(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply branch 側の copy は変更後 path を想定外差分検査に使う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("spec\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "copy oracle to implementation")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "spec\n"
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert state["apply"]["state"] == "ready"
    assert "force-resolved unexpected diffs:" not in output


def test_apply_abandon_deletes_apply_artifacts_and_resets_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply abandon` は apply 成果物を merge せず破棄する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_abandon_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()
    assert not (repo / "feature.txt").exists()
    assert f"abandoned apply branch: {apply_branch}" in output
    assert f"abandoned apply worktree: {apply_worktree}" in output
    assert "previous apply.state: completed" in output
    assert "current apply.state: ready" in output


def test_apply_abandon_rejects_cross_session_apply_branch_without_cleanup(
    tmp_path: Path,
) -> None:
    """apply abandon は別 session の apply branch/worktree を削除しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _create_completed_apply_run(repo, oracle_snapshot)
    other_session_id = "2026-05-10_22-21_10_000000999"
    other_apply_run_id = "2026-05-10_22-22_10_000000123"
    other_apply_branch = f"cmoc/apply/{other_session_id}/{other_apply_run_id}"
    other_apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / other_session_id
        / other_apply_run_id
    )
    _git(repo, "branch", other_apply_branch, oracle_snapshot)
    _git(repo, "worktree", "add", str(other_apply_worktree), other_apply_branch)
    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["apply_branch"] = other_apply_branch
    state["apply"]["oracle_snapshot_commit"] = oracle_snapshot
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    assert "同じ session の apply branch" in error_info.value.actions[0]
    assert _git(repo, "branch", "--list", other_apply_branch).stdout.strip()
    assert other_apply_worktree.exists()


def test_apply_abandon_accepts_apply_branch_worktree(
    tmp_path: Path,
) -> None:
    """apply worktree 上から実行しても所有元 repo root の state を更新する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )

    cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_relocates_from_apply_branch_before_cleanup(
    tmp_path: Path,
) -> None:
    """apply branch からの実行時は session branch の worktree へ移動してから消す。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)

    cmoc_apply_abandon_impl(apply_worktree)

    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_ignores_worktree_local_log_cmoc(
    tmp_path: Path,
) -> None:
    """ログ用 `.cmoc` がある apply worktree からでも所有元の state を更新する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / ".cmoc" / "logs" / "sub_commands").mkdir(parents=True)

    cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_rejects_dirty_session_branch_worktree(
    tmp_path: Path,
) -> None:
    """apply branch からの実行でも session branch worktree の差分で停止する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)
    session_worktree = tmp_path / "session-worktree"
    _git(repo, "worktree", "add", str(session_worktree), session_branch)
    (session_worktree / "session-dirty.txt").write_text(
        "dirty\n",
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(apply_worktree)

    assert "未コミットの変更" in error_info.value.message
    assert "session-dirty.txt" in error_info.value.detail
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_abandon_does_not_check_unrelated_owner_worktree(
    tmp_path: Path,
) -> None:
    """session branch が別 worktree にある場合、所有元 root の差分は見ない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)
    session_worktree = tmp_path / "session-worktree"
    _git(repo, "worktree", "add", str(session_worktree), session_branch)
    (repo / "home-dirty.txt").write_text("dirty\n", encoding="utf-8")

    cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert (repo / "home-dirty.txt").exists()


def test_apply_abandon_rejects_dirty_owner_before_session_switch(
    tmp_path: Path,
) -> None:
    """session worktree 作成に使う owner root の差分を持ち越さない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)
    (repo / "home-dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "未コミットの変更" in error_info.value.message
    assert "home-dirty.txt" in error_info.value.detail
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_abandon_rejects_ready_state_without_cleanup(
    tmp_path: Path,
) -> None:
    """apply.state が ready の場合は破棄対象なしとして停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "破棄対象の apply run" in error_info.value.message
    assert state["apply"]["state"] == "ready"


def test_apply_abandon_accepts_error_state(
    tmp_path: Path,
) -> None:
    """apply.state が error の apply run も成果物を破棄できる。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "error"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    cmoc_apply_abandon_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_stops_running_process_and_resets_state(
    tmp_path: Path,
) -> None:
    """running apply は process を停止してから成果物を破棄する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    process = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    write_apply_process_id(
        repo,
        "2026-05-10_22-21_10_000000123",
        process.pid,
        apply_branch,
    )

    try:
        cmoc_apply_abandon_impl(repo)
    finally:
        process.wait(timeout=5)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert process.returncode is not None
    assert state["apply"]["state"] == "ready"
    assert "process_id" not in state["apply"]
    assert not (
        repo / ".cmoc" / "runtime" / "apply" / "2026-05-10_22-21_10_000000123.pid"
    ).exists()
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_rejects_legacy_pid_without_killing_process(
    tmp_path: Path,
) -> None:
    """PID だけの runtime file では apply process と断定せず停止しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    process = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    process_id_path = (
        repo / ".cmoc" / "runtime" / "apply"
        / "2026-05-10_22-21_10_000000123.pid"
    )
    process_id_path.parent.mkdir(parents=True)
    process_id_path.write_text(f"{process.pid}\n", encoding="utf-8")

    try:
        with pytest.raises(CmocError) as error_info:
            cmoc_apply_abandon_impl(repo)

        assert "安全に特定できませんでした" in error_info.value.message
        assert process.poll() is None
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["apply"]["state"] == "running"
        assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
        assert apply_worktree.exists()
    finally:
        process.terminate()
        process.wait(timeout=5)


def test_apply_abandon_rejects_running_state_without_process_id(
    tmp_path: Path,
) -> None:
    """running state に process id が無い場合は cleanup せず停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "process id が記録されていません" in error_info.value.message
    assert "apply.state: running" in error_info.value.detail
    assert state["apply"]["state"] == "running"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_abandon_rejects_unknown_state_without_cleanup(
    tmp_path: Path,
) -> None:
    """未知の apply.state は state 破損として扱い cleanup しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "paused"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "形式が不正" in error_info.value.message
    assert "apply.state: paused" in error_info.value.detail
    assert state["apply"]["state"] == "paused"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_uses_investigate_repeat_option_for_loop_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply` は指定された調査・修正ループ回数を上限に使う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """常に不整合を返し、指定回数で incomplete になることを見やすくする。"""
        codex_prompts.append(str(args[1]))
        if str(kwargs.get("purpose")).startswith("要修正点適用"):
            (Path(args[0]) / "app.py").write_text(
                "fixed but still needs review\n",
                encoding="utf-8",
            )
            return ""
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return _discrepancy_json("f")
        return _apply_report(str(args[1]), "未収束", [1, 1])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=2)

    assert exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert (
        "実装反復 (2/2) 要修正点: 1"
        in capsys.readouterr().out
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert codex_prompts
    assert "## 作業結果\n未収束" in report_text
    assert "まだ要修正点が残っている可能性" in report_text


def test_apply_reinvestigates_files_changed_by_previous_fix(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex 修正で増えた実装差分は次の partial 調査対象に戻す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc state")
    _checkout_session_branch(repo)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    apply_ran = False
    implementation_investigation_purposes: list[str] = []

    def first_discrepancy() -> str:
        payload = json.loads(_discrepancy_json("create app"))
        payload["fixing_points"][0]["evidences"][0]["path"] = str(
            repo / "oracles" / "spec.md"
        )
        return json.dumps(payload)

    def fake_codex(*args: object, **kwargs: object) -> str:
        """初回だけ要修正点を返し、修正後の実装調査対象を記録する。"""
        nonlocal apply_ran
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査"):
            if apply_ran:
                return '{"git_head_commit_hash": null, "fixing_points": []}'
            return first_discrepancy()
        if purpose.startswith("実装調査"):
            implementation_investigation_purposes.append(purpose)
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("要修正点適用"):
            apply_ran = True
            (Path(args[0]) / "app.py").write_text("fixed\n", encoding="utf-8")
            return ""
        if purpose == "commit message 生成":
            return "Apply fix"
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=2,
        repeat_improove_fixing_list=0,
    ) == 0

    assert any(
        purpose.endswith("app.py")
        for purpose in implementation_investigation_purposes
    )


def test_apply_keeps_empty_oracle_dirty_set_when_only_implementation_evidence(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """実装 evidence だけの次ループで oracle dirty 空集合を再スコープ化しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (repo / "app.py").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "targets")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    discrepancy_returned = False
    oracle_investigation_purposes: list[str] = []
    implementation_investigation_purposes: list[str] = []

    def implementation_only_discrepancy() -> str:
        payload = json.loads(_discrepancy_json("fix app"))
        payload["fixing_points"][0]["evidences"][0]["path"] = "app.py"
        return json.dumps(payload)

    def fake_codex(*args: object, **kwargs: object) -> str:
        """初回 oracle 調査だけ実装 evidence の要修正点を返す。"""
        nonlocal discrepancy_returned
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査"):
            oracle_investigation_purposes.append(purpose)
            if not discrepancy_returned:
                discrepancy_returned = True
                return implementation_only_discrepancy()
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("実装調査"):
            implementation_investigation_purposes.append(purpose)
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("要修正点適用"):
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=2,
        repeat_improove_fixing_list=0,
    ) == 0

    assert len(oracle_investigation_purposes) == 1
    assert sum(
        purpose.endswith("app.py")
        for purpose in implementation_investigation_purposes
    ) == 2


def test_apply_improoves_fixing_list_until_same_result_or_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """要修正点リスト改善ループは上限内で同一結果まで繰り返す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    organize_prompts: list[str] = []
    organize_kwargs: list[dict[str, object]] = []
    apply_prompts: list[str] = []
    organize_results = [
        _discrepancy_json("first improvement"),
        _discrepancy_json("second improvement"),
        _discrepancy_json("second improvement"),
    ]

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査、改善、修正、レポートの呼び出しを purpose で分岐する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
            organize_kwargs.append(kwargs)
            return organize_results.pop(0)
        if purpose.startswith("要修正点適用"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=3,
    )

    output = capsys.readouterr().out
    assert exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert len(organize_prompts) == 3
    assert all(kwargs["model"] == FRONTIER_MODEL for kwargs in organize_kwargs)
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_HIGH_REASONING_EFFORT
        for kwargs in organize_kwargs
    )
    assert "(5/6, 1/1, 4/5, 3/3) 要修正点リスト改善" in output
    assert "(5/6, 1/1, 5/5, 1/1) 要修正点適用" in output
    assert "要修正点リスト改善ループ (3/3) 要修正点: 1" in output
    assert "second improvement" in apply_prompts[0]
    assert "initial" in organize_prompts[0]
    assert "first improvement" in organize_prompts[1]


def test_apply_improove_fixing_list_uses_oracle_snapshot_base(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """要修正点整理の過去修正範囲は apply snapshot 起点に限定する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("old spec\n", encoding="utf-8")
    (repo / "old.py").write_text("print('old')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old targets")
    last_joined_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()

    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["last_joined_apply_oracle_snapshot_commit"] = (
        last_joined_snapshot
    )
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)

    (oracle_root / "new.md").write_text("new spec\n", encoding="utf-8")
    (repo / "new.py").write_text("print('new')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "new targets")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    purposes: list[str] = []
    organize_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """rolling の調査範囲と整理 prompt の base を記録する。"""
        purpose = str(kwargs.get("purpose"))
        purposes.append(purpose)
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=1,
        scope="rolling",
    ) == 0

    assert any(purpose.endswith("oracles/new.md") for purpose in purposes)
    assert any(purpose.endswith("new.py") for purpose in purposes)
    assert not any(purpose.endswith("oracles/old.md") for purpose in purposes)
    assert not any(purpose.endswith("old.py") for purpose in purposes)
    assert organize_prompts
    assert (
        f"`{oracle_snapshot_commit}..{oracle_snapshot_commit}`"
        in organize_prompts[0]
    )
    assert (
        f"`{last_joined_snapshot}..{oracle_snapshot_commit}`"
        not in organize_prompts[0]
    )


def test_apply_stops_improoving_fixing_list_when_it_becomes_empty(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """要修正点リスト改善ループは空リストになった時点で収束する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    organize_prompts: list[str] = []
    apply_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査後の整理で空リストを返し、以後の改善を不要にする。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("要修正点適用"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=3,
    )

    output = capsys.readouterr().out
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert exit_code == 0
    assert len(organize_prompts) == 1
    assert apply_prompts == []
    assert "要修正点リスト改善ループ (1/3) 要修正点: 0" in output
    assert "要修正点リスト改善ループ (2/3)" not in output
    assert "実装反復 (1/1) 要修正点: 0" in output
    assert "## 作業結果\n収束" in report_text


def test_apply_fills_discrepancy_head_commit_hash(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """AI が null を返しても要修正点には cmoc 側で発見時 HEAD を付与する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    expected_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    apply_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は null の hash を返し、修正依頼 prompt を記録する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("fill hash")
        if purpose.startswith("要修正点適用"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=0,
    ) == APPLY_FORK_EXIT_CODE_UNCONVERGED

    assert apply_prompts
    assert all(
        f'"git_head_commit_hash": "{expected_head}"' in prompt
        for prompt in apply_prompts
    )
    assert all(
        '"git_head_commit_hash": null' not in prompt
        for prompt in apply_prompts
    )


def test_apply_commits_each_discrepancy_before_next_codex_call(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """修正作業ループは要修正点 1 件ごとに検査と commit を完了する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    first_payload = json.loads(_discrepancy_json("first fix"))
    second_item = json.loads(_discrepancy_json("second fix"))[
        "fixing_points"
    ][0]
    first_payload["fixing_points"].append(second_item)
    two_discrepancies_json = json.dumps(first_payload)
    apply_count = 0
    commit_message_count = 0
    status_before_second_apply: list[str] = []
    head_before_second_apply: list[str] = []
    apply_repos: list[Path] = []
    commit_message_options: list[tuple[object, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """2 件の修正依頼の間で作業ツリーと HEAD を記録する。"""
        nonlocal apply_count
        nonlocal commit_message_count
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return two_discrepancies_json
        if purpose == "要修正点整理":
            return two_discrepancies_json
        if purpose.startswith("要修正点適用"):
            apply_count += 1
            apply_repos.append(Path(args[0]))
            if apply_count == 2:
                apply_repo = Path(args[0])
                status_before_second_apply.append(
                    _git(apply_repo, "status", "--porcelain").stdout
                )
                head_before_second_apply.append(
                    _git(apply_repo, "log", "-1", "--pretty=%s").stdout.strip()
                )
            (Path(args[0]) / "app.py").write_text(
                f"fix {apply_count}\n",
                encoding="utf-8",
            )
            return ""
        if purpose == "commit message 生成":
            commit_message_count += 1
            commit_message_options.append(
                (
                    kwargs.get("model"),
                    kwargs.get("reasoning_effort"),
                )
            )
            return f"Apply fix {commit_message_count}"
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert (
        cmoc_apply_impl(repo, repeat_investigate_and_fix=1)
        == APPLY_FORK_EXIT_CODE_UNCONVERGED
    )

    assert apply_repos
    commit_subjects = _git(
        apply_repos[-1],
        "log",
        "--pretty=%s",
        "-3",
    ).stdout.splitlines()
    assert apply_count == 2
    assert commit_message_count == 2
    assert commit_message_options == [
        (COMMIT_MESSAGE_MODEL, COMMIT_MESSAGE_REASONING_EFFORT),
        (COMMIT_MESSAGE_MODEL, COMMIT_MESSAGE_REASONING_EFFORT),
    ]
    assert status_before_second_apply == [""]
    assert head_before_second_apply == ["Apply fix 1"]
    assert commit_subjects[:2] == ["Apply fix 2", "Apply fix 1"]
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )


def test_organize_prompt_includes_fixing_list_quality_requirements(
    tmp_path: Path,
) -> None:
    """要修正点リスト改善 prompt は oracle の品質観点を明示する。"""
    prompt = _organize_prompt(
        tmp_path,
        json.loads(_discrepancy_json("fix"))["fixing_points"],
        "cmoc/session/2026-05-10_22-21_10_000000123",
        "1111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222",
    )

    assert "内容の品質に明確な問題がない" in prompt
    assert "重複する要修正点は 1 件にマージ" in prompt
    assert "矛盾する修正方針は矛盾しない内容に調整" in prompt
    assert "git ブランチ `cmoc/session/2026-05-10_22-21_10_000000123`" in prompt
    assert (
        "`1111111111111111111111111111111111111111"
        "..2222222222222222222222222222222222222222`"
    ) in prompt
    assert "に含まれる過去の修正内容を確認" in prompt
    assert "False-Positive と判断できる要修正点は除外" in prompt
    assert "作業順序として適切になるよう並べ替えてください" in prompt
    assert "改善過程で発見した漏れがあれば" in prompt


def test_apply_prompt_treats_discrepancy_as_optional_hint(
    tmp_path: Path,
) -> None:
    """修正作業 prompt は要修正点情報を無視可能なヒントとして扱う。"""
    prompt = _apply_prompt(
        tmp_path,
        {
            "title": "sample",
            "oracle_requirement": "oracle requirement",
            "observed_implementation": "observed implementation",
            "reason": "reason",
            "suggested_fix": "suggested fix",
            "evidences": [],
        },
    )

    assert "作業のためのヒント" in prompt
    assert "絶対に従わなければならない指示書としては扱わない" in prompt
    assert "無視してかまいません" in prompt
    assert "ベストエフォート" in prompt
    assert "目的を達成した保証は不要" in prompt
    assert f"`{tmp_path / 'oracles'}` は編集禁止です。" in prompt
    assert "配下の `INDEX.md` 以外は編集禁止" not in prompt
    assert f"`{tmp_path / 'README.md'}` は編集禁止です。" in prompt
    assert f"`{tmp_path / 'AGENTS.md'}` は編集禁止です。" in prompt
    assert f"`{tmp_path / '.cmoc'}` は編集禁止です。" in prompt


def test_apply_prompt_orders_completion_before_details() -> None:
    """修正作業 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    prompt = _apply_prompt(
        Path("/repo"),
        {
            "title": "sample",
            "oracle_requirement": "oracle requirement",
            "observed_implementation": "observed implementation",
            "reason": "reason",
            "suggested_fix": "suggested fix",
            "evidences": [],
        },
    )
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア実装担当です。"
    assert lines[1] == (
        "`/repo` の実装を、要修正点情報に記載された仕様要求に"
        "追従するようベストエフォートで更新してください。"
    )
    assert lines[2] == (
        "完了条件は、必要と判断した実装修正とテスト更新を終え、変更内容と残課題を報告することです。"
    )
    assert lines.index("以下の要修正点情報は作業のためのヒントです。") > 2


def test_apply_report_validation_requires_markdown_sections() -> None:
    """apply report 検証は本文全体の substring だけでは通さない。"""
    body = "\n".join(
        [
            "作業結果 収束",
            "要修正点件数の推移 1 回目: 0 件",
            "cmoc/apply/session/run 全変更内容 カテゴリ: 実装修正",
            "本文に必要語はあるが Markdown 見出しではない。",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            body,
            "cmoc/apply/session/run",
            "収束",
            True,
            [0],
        )

    assert "作業結果の区分" in str(error.value)
    assert "要修正点件数の推移" in str(error.value)
    assert "ブランチ上の全変更内容" in str(error.value)


def test_apply_report_validation_matches_loop_counts_by_line() -> None:
    """件数推移は loop 番号と件数が同じ行に対応している必要がある。"""
    body = "\n".join(
        [
            "## 作業結果",
            "未収束",
            "",
            "## 要修正点件数の推移",
            "- 1 回目: 9 件",
            "- 2 回目: 1 件",
            "まだ要修正点が残っている可能性があります。",
            "",
            "## ブランチ cmoc/apply/session/run 上の全変更内容",
            "- カテゴリ: 実装修正",
            "  - 要約を記録しました。",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            body,
            "cmoc/apply/session/run",
            "未収束",
            False,
            [1, 9],
        )

    assert "要修正点件数の推移 loop 1" in str(error.value)
    assert "要修正点件数の推移 loop 2" in str(error.value)


def test_apply_report_validation_requires_change_summary_item() -> None:
    """全変更内容 section はカテゴリ名だけでなく要約項目も必要とする。"""
    body = "\n".join(
        [
            "## 作業結果",
            "収束",
            "",
            "## 要修正点件数の推移",
            "- 1 回目: 0 件",
            "",
            "## ブランチ cmoc/apply/session/run 上の全変更内容",
            "- カテゴリ: 実装修正",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            body,
            "cmoc/apply/session/run",
            "収束",
            True,
            [0],
        )

    assert "ブランチ上の全変更内容" in str(error.value)


def test_apply_report_validation_requires_fork_commit_metadata() -> None:
    """Front Matter は session/apply それぞれの分岐元 commit を必須にする。"""
    report = "\n".join(
        [
            "---",
            "generated_at: \"2026-05-10T22:21:10\"",
            "cmoc_session_id: \"session\"",
            "cmoc_apply_run_id: \"run\"",
            "cmoc_session_branch: \"cmoc/session/session\"",
            "cmoc_apply_branch: \"cmoc/apply/session/run\"",
            "apply_worktree_path: \"/tmp/worktree\"",
            "oracle_snapshot_commit: \"apply-fork\"",
            "session_head_at_apply_start: \"apply-fork\"",
            "session_head_at_apply_finish: \"apply-finish\"",
            "result: \"収束\"",
            "---",
            "",
            "## 作業結果",
            "収束",
            "",
            "## 要修正点件数の推移",
            "- 1 回目: 0 件",
            "",
            "## ブランチ cmoc/apply/session/run 上の全変更内容",
            "- カテゴリ: 実装修正",
            "  - 要約を記録しました。",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            report,
            "cmoc/apply/session/run",
            "収束",
            True,
            [0],
            require_front_matter=True,
        )

    assert "YAML Front Matter cmoc_session_fork_commit" in str(error.value)
    assert "YAML Front Matter cmoc_apply_fork_commit" in str(error.value)


def test_apply_marks_error_when_success_report_generation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """成功 report 生成失敗は completed ではなく error として記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """apply worktree 側だけ report 対象差分を作る。"""
        if not (repo_root / ".git").is_file():
            return False
        index_path = repo_root / "docs" / "INDEX.md"
        if index_path.exists():
            return False
        index_path.parent.mkdir()
        index_path.write_text("# `docs`\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    advanced_session = False

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は収束、変更要約は必須項目不足にする。"""
        nonlocal advanced_session
        if kwargs.get("purpose") == "apply 変更要約":
            if not advanced_session:
                (repo / "session-progress.txt").write_text(
                    "session advanced\n",
                    encoding="utf-8",
                )
                _git(repo, "add", "session-progress.txt")
                _git(repo, "commit", "-m", "advance session during apply")
                advanced_session = True
            return '{"changes": []}'
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "Maintain indexes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    report_dir = repo / ".cmoc" / "reports" / "apply" / "fork"
    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    reports = list(report_dir.glob("*.md"))
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()
    session_head_at_finish = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert len(reports) == 1
    assert 'result: "エラー"' in reports[0].read_text(encoding="utf-8")
    assert session_head != session_head_at_finish
    assert session_head != apply_head
    assert not (
        repo
        / ".cmoc"
        / "sessions"
        / "2026-05-10_22-21_10_000000123.apply_process.json"
    ).exists()


def test_apply_marks_error_when_final_output_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """最終出力失敗は completed ではなく error として記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は収束させ、必要なら変更要約を返す。"""
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "No changes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)
    failed_once = False

    def fake_print(*args: object, **kwargs: object) -> None:
        """収束 report path の最初の出力だけ失敗させる。"""
        nonlocal failed_once
        if (
            not failed_once
            and len(args) == 1
            and str(args[0]).endswith(".md")
        ):
            failed_once = True
            raise RuntimeError("fake final output failure")
        builtins.print(*args, **kwargs)

    monkeypatch.setattr(apply_module, "print", fake_print, raising=False)

    with pytest.raises(RuntimeError, match="fake final output failure"):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_texts = [report.read_text(encoding="utf-8") for report in reports]

    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert len(reports) == 1
    assert any('result: "エラー"' in text for text in report_texts)
    assert not (
        repo
        / ".cmoc"
        / "sessions"
        / "2026-05-10_22-21_10_000000123.apply_process.json"
    ).exists()


def test_apply_fallback_change_summary_preserves_special_path_tokens(
    tmp_path: Path,
) -> None:
    """fallback report の changed_paths は newline や前後空白を削らない。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    special_path = repo / " changed\nfile.py "
    special_path.write_text("changed\n", encoding="utf-8")
    _git(repo, "add", special_path.relative_to(repo).as_posix())
    _git(repo, "commit", "-m", "special path")
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()

    summary = apply_module._fallback_change_summary_from_git(
        repo,
        branch_name,
        snapshot_commit,
        RuntimeError("summary failed"),
    )

    assert summary[0]["changed_paths"] == [" changed\nfile.py "]


def test_apply_fallback_change_summary_includes_uncommitted_paths(
    tmp_path: Path,
) -> None:
    """fallback report は staged/working tree/untracked の変更も列挙する。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()

    (repo / "working.py").write_text("working\n", encoding="utf-8")
    _git(repo, "add", "working.py")
    _git(repo, "commit", "-m", "add working")
    (repo / "staged.py").write_text("staged\n", encoding="utf-8")
    _git(repo, "add", "staged.py")
    (repo / "working.py").write_text("working changed\n", encoding="utf-8")
    (repo / "untracked.py").write_text("untracked\n", encoding="utf-8")

    summary = apply_module._fallback_change_summary_from_git(
        repo,
        branch_name,
        snapshot_commit,
        RuntimeError("summary failed"),
    )

    assert summary[0]["category"] == "変更ファイル一覧"
    assert summary[0]["changed_paths"] == [
        "staged.py",
        "untracked.py",
        "working.py",
    ]


def test_apply_fallback_change_summary_includes_deleted_paths(
    tmp_path: Path,
) -> None:
    """fallback report は commit 済み/staged/working tree の削除も列挙する。"""
    repo = _init_repo(tmp_path)
    (repo / "committed_delete.py").write_text("committed\n", encoding="utf-8")
    (repo / "staged_delete.py").write_text("staged\n", encoding="utf-8")
    (repo / "working_delete.py").write_text("working\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "add delete targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()

    (repo / "committed_delete.py").unlink()
    _git(repo, "add", "committed_delete.py")
    _git(repo, "commit", "-m", "delete committed")
    (repo / "staged_delete.py").unlink()
    _git(repo, "add", "staged_delete.py")
    (repo / "working_delete.py").unlink()

    summary = apply_module._fallback_change_summary_from_git(
        repo,
        branch_name,
        snapshot_commit,
        RuntimeError("summary failed"),
    )

    assert summary[0]["category"] == "変更ファイル一覧"
    assert summary[0]["changed_paths"] == [
        "committed_delete.py",
        "staged_delete.py",
        "working_delete.py",
    ]


def test_apply_change_summary_treats_uncommitted_paths_as_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """変更要約は commit 間差分が空でも未コミット差分があれば Codex に依頼する。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "working.py").write_text("working\n", encoding="utf-8")

    prompts: list[str] = []

    def fake_codex(repo_root: Path, prompt: str, **kwargs: object) -> str:
        prompts.append(prompt)
        return _change_summary_json()

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    summary = apply_module._generate_change_summary(
        repo,
        branch_name,
        snapshot_commit,
    )

    assert prompts
    assert "working tree / staging area" in prompts[0]
    assert summary[0]["category"] == "実装修正"


def test_apply_change_summary_treats_deleted_paths_as_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """変更要約は削除のみの差分でも Codex に依頼する。"""
    repo = _init_repo(tmp_path)
    (repo / "deleted.py").write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "deleted.py")
    _git(repo, "commit", "-m", "add deleted target")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "deleted.py").unlink()
    _git(repo, "add", "deleted.py")

    prompts: list[str] = []

    def fake_codex(repo_root: Path, prompt: str, **kwargs: object) -> str:
        prompts.append(prompt)
        return json.dumps(
            {
                "changes": [
                    {
                        "category": "削除",
                        "summary": "不要なファイルを削除しました。",
                        "changed_paths": ["deleted.py"],
                    }
                ]
            }
        )

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    summary = apply_module._generate_change_summary(
        repo,
        branch_name,
        snapshot_commit,
    )

    assert prompts
    assert '["deleted.py"]' in prompts[0]
    assert summary[0]["changed_paths"] == ["deleted.py"]


def test_apply_writes_error_report_when_midway_stage_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply fork は途中エラーでも保存済みレポートのパスを出力する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    def fail_maintain_indexes(repo_root: Path) -> bool:
        raise RuntimeError(f"fake maintain failure at {repo_root.name}")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fail_maintain_indexes,
    )

    with pytest.raises(RuntimeError, match="fake maintain failure"):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    captured = capsys.readouterr()

    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert len(reports) == 1
    assert str(reports[0]) in captured.out
    report_text = reports[0].read_text(encoding="utf-8")
    session_fork_commit = state["session"]["session_start_commit"]
    assert "result: \"エラー\"" in report_text
    assert "cmoc_apply_run_id: " in report_text
    assert (
        f"cmoc_session_fork_commit: \"{session_fork_commit}\""
        in report_text
    )
    assert (
        "cmoc_apply_branch: \"cmoc/apply/2026-05-10_22-21_10_000000123/"
        in report_text
    )
    apply_fork_commit = state["apply"]["oracle_snapshot_commit"]
    assert f"cmoc_apply_fork_commit: \"{apply_fork_commit}\"" in report_text
    assert "apply_worktree_path: " in report_text
    assert "- Failed stage: `INDEX.md メンテナンス`" in report_text
    assert "- Exception type: `RuntimeError`" in report_text
    assert "- Exception message: `fake maintain failure at " in report_text
    assert "エラー発生前に記録済みの要修正点件数はありません。" in report_text
    assert "カテゴリ: 変更なし" in report_text


def test_apply_error_report_includes_codex_change_summary(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """error report でも apply branch の変更要約を Codex Structured Output から描画する。"""
    repo = _init_repo(tmp_path)
    (repo / "oracles").mkdir()
    (repo / "oracles" / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_branch = "cmoc/apply/session/run"
    _git(repo, "checkout", "-b", apply_branch)
    (repo / "app.py").write_text("print('changed')\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "change app")

    codex_purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        codex_purposes.append(str(kwargs.get("purpose")))
        return _change_summary_json()

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    report_path = apply_module._write_apply_error_report(
        repo,
        "session",
        "run",
        "cmoc/session/session",
        apply_branch,
        repo,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        "要修正点適用",
        RuntimeError("fake apply failure"),
        [1],
    )

    report_text = report_path.read_text(encoding="utf-8")
    assert codex_purposes == ["apply 変更要約"]
    assert "result: \"エラー\"" in report_text
    assert "## エラー詳細" in report_text
    assert "- Failed stage: `要修正点適用`" in report_text
    assert "カテゴリ: 実装修正" in report_text
    assert "テスト用の変更内容を整理しました。" in report_text
    assert "- `app.py`" in report_text
    assert "カテゴリ: エラー終了" not in report_text


def test_apply_rejects_non_cmoc_branch(tmp_path: Path) -> None:
    """`cmoc apply` は cmoc ブランチ外では仕様通り CmocError にする。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "`cmoc apply` は session branch 上で実行してください。" in error.value.message


def test_apply_rejects_non_oracle_changes_after_cmoc_guarantee(
    tmp_path: Path,
) -> None:
    """開始前の未コミット実装差分は ignore 保証前に拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert "app.py" in error.value.detail
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


def test_apply_does_not_commit_preexisting_gitignore_changes(
    tmp_path: Path,
) -> None:
    """開始前からある `.gitignore` 差分も precondition failure にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert _git(repo, "status", "--porcelain", "--", ".gitignore").stdout == (
        "?? .gitignore\n"
    )


def test_apply_untracks_existing_cmoc_before_worktree_creation(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork は state 検証後に tracked `.cmoc` を初期化 commit で外す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_000000123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=0)

    assert exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert _git(repo, "show", "HEAD:.gitignore").stdout == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert (repo / ".cmoc" / "worktrees").exists()
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" in branches
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_apply_rejects_broken_session_state_before_cmoc_ignore(
    tmp_path: Path,
) -> None:
    """壊れた session state は `.gitignore` を作らずに拒否する。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc/session/2026-05-10_22-21_10_000000123")
    broken_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "JSON が不正" in error.value.message
    assert not (repo / ".gitignore").exists()
    assert not (repo / ".cmoc" / "worktrees").exists()
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" not in branches


def test_apply_rejects_not_ready_state_before_cmoc_ignore(
    tmp_path: Path,
) -> None:
    """apply.state の事前条件違反では `.gitignore` を変更しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        f"cmoc/apply/{session_id}/2026-05-10_22-22_10_000000123"
    )
    state["apply"]["oracle_snapshot_commit"] = _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "apply run を開始できる状態ではありません。" in error.value.message
    assert "apply.state: running" in error.value.detail
    assert not (repo / ".gitignore").exists()
    assert not (repo / ".cmoc" / "worktrees").exists()
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" not in branches


def test_apply_rejects_negative_repeat_before_worktree_creation(
    tmp_path: Path,
) -> None:
    """repeat 系オプションの負値は apply 開始副作用の前に拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo, repeat_investigate_and_fix=-1)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "調査・修正ループ回数に負の値" in error.value.message
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert "cmoc/apply/" not in branches


def test_apply_marks_error_when_running_state_write_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply 開始中の state 書き込み失敗も error state として残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    real_write_session_state = apply_module.write_session_state
    calls = 0

    def flaky_write_session_state(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
    ) -> Path:
        """running 遷移の保存だけ失敗させる。"""
        nonlocal calls
        calls += 1
        if calls == 1:
            raise OSError("fake running write failure")
        return real_write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(
        apply_module,
        "write_session_state",
        flaky_write_session_state,
    )

    with pytest.raises(OSError) as error:
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    apply_branch = state["apply"]["apply_branch"]
    assert "fake running write failure" in str(error.value)
    assert state["apply"]["state"] == "error"
    assert isinstance(apply_branch, str)
    assert apply_branch.startswith("cmoc/apply/2026-05-10_22-21_10_000000123/")
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert calls == 2


def test_apply_revalidates_ready_state_under_start_lock(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork は lock 獲得後に state を読み直して二重開始を拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    running_branch = (
        f"cmoc/apply/{session_id}/2026-05-10_22-22_10_000000123"
    )
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    real_read_session_state = apply_module.read_session_state
    read_calls = 0

    def read_state_with_concurrent_start(
        repo_root: Path,
        requested_session_id: str,
    ) -> dict[str, object]:
        """初回検証後に別 apply が running を保存した状態を模擬する。"""
        nonlocal read_calls
        read_calls += 1
        state = real_read_session_state(repo_root, requested_session_id)
        if read_calls == 1:
            concurrent_state = json.loads(
                json.dumps(state, ensure_ascii=False),
            )
            concurrent_state["apply"] = {
                "state": "running",
                "apply_branch": running_branch,
                "oracle_snapshot_commit": snapshot_commit,
            }
            write_session_state(repo_root, requested_session_id, concurrent_state)
        return state

    monkeypatch.setattr(
        apply_module,
        "read_session_state",
        read_state_with_concurrent_start,
    )

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    assert "apply run を開始できる状態ではありません" in error.value.message
    assert state["apply"] == {
        "state": "running",
        "apply_branch": running_branch,
        "oracle_snapshot_commit": snapshot_commit,
    }
    assert read_calls == 2
    assert "cmoc/apply/" not in branches
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert reports == []


def test_apply_marks_error_when_worktree_creation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply 開始後の worktree 作成失敗は error state として残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")

    def fail_create_apply_worktree(
        _repo_root: Path,
        _session_id: str,
        _oracle_snapshot_commit: str,
        _initial_plan: apply_module._ApplyWorktreePlan,
    ) -> apply_module._ApplyWorktreePlan:
        """worktree 作成失敗を模擬する。"""
        raise RuntimeError("fake worktree creation failure")

    monkeypatch.setattr(
        apply_module,
        "_create_apply_worktree",
        fail_create_apply_worktree,
    )

    with pytest.raises(RuntimeError) as error:
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    captured = capsys.readouterr()
    assert "fake worktree creation failure" in str(error.value)
    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert state["apply"]["oracle_snapshot_commit"] == _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert "cmoc/apply/" not in branches
    assert len(reports) == 1
    assert str(reports[0]) in captured.out
    report_text = reports[0].read_text(encoding="utf-8")
    apply_run_id_match = re.search(
        r'^cmoc_apply_run_id: "([^"]+)"$',
        report_text,
        re.MULTILINE,
    )
    assert apply_run_id_match is not None
    apply_run_id = apply_run_id_match.group(1)
    planned_apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "2026-05-10_22-21_10_000000123"
        / apply_run_id
    )
    assert f"apply_worktree_path: \"{planned_apply_worktree}\"" in report_text
    assert f"apply_worktree_path: \"{repo}\"" not in report_text

    cmoc_apply_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }


def test_create_apply_worktree_failure_reports_last_attempted_plan(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """worktree 作成リトライ失敗は最後に実試行した候補を例外に載せる。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    session_id = "session"
    oracle_snapshot_commit = "abc123"
    initial_plan = apply_module._ApplyWorktreePlan(
        "run0",
        f"cmoc/apply/{session_id}/run0",
        repo / ".cmoc" / "worktrees" / session_id / "run0",
    )
    timestamps = iter(f"run{index}" for index in range(1, 10))
    attempted_branches: list[str] = []

    def fake_make_timestamp() -> str:
        return next(timestamps)

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del check
        if args[:1] == ["branch"]:
            attempted_branches.append(args[1])
        return subprocess.CompletedProcess(args, 1, "", "fake collision")

    monkeypatch.setattr(apply_module, "make_timestamp", fake_make_timestamp)
    monkeypatch.setattr(apply_module, "run_git", fake_run_git)
    monkeypatch.setattr(apply_module, "sleep", lambda _seconds: None)

    with pytest.raises(apply_module._ApplyWorktreeCreationError) as error:
        apply_module._create_apply_worktree(
            repo,
            session_id,
            oracle_snapshot_commit,
            initial_plan,
        )

    assert attempted_branches[0] == initial_plan.apply_branch
    assert attempted_branches[-1] == f"cmoc/apply/{session_id}/run9"
    assert error.value.last_plan.apply_run_id == "run9"
    assert error.value.last_plan.apply_branch == attempted_branches[-1]
    assert error.value.last_plan.apply_worktree == (
        repo / ".cmoc" / "worktrees" / session_id / "run9"
    )


def test_create_apply_worktree_reports_branch_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """worktree 作成後始末の branch 削除失敗は診断付きで即時失敗する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    session_id = "session"
    oracle_snapshot_commit = "abc123"
    initial_plan = apply_module._ApplyWorktreePlan(
        "run0",
        f"cmoc/apply/{session_id}/run0",
        repo / ".cmoc" / "worktrees" / session_id / "run0",
    )
    git_calls: list[list[str]] = []

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del check
        git_calls.append(args)
        if args[:1] == ["branch"] and args[1] != "-D":
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:2] == ["worktree", "add"]:
            return subprocess.CompletedProcess(
                args,
                1,
                "worktree stdout",
                "worktree failed",
            )
        if args[:2] == ["branch", "-D"]:
            return subprocess.CompletedProcess(
                args,
                1,
                "cleanup stdout",
                "cleanup failed",
            )
        raise AssertionError(f"unexpected git args: {args}")

    monkeypatch.setattr(apply_module, "run_git", fake_run_git)
    monkeypatch.setattr(apply_module, "sleep", lambda _seconds: None)

    with pytest.raises(apply_module._ApplyWorktreeCreationError) as error:
        apply_module._create_apply_worktree(
            repo,
            session_id,
            oracle_snapshot_commit,
            initial_plan,
        )

    assert git_calls == [
        ["branch", initial_plan.apply_branch, oracle_snapshot_commit],
        [
            "worktree",
            "add",
            str(initial_plan.apply_worktree),
            initial_plan.apply_branch,
        ],
        ["branch", "-D", initial_plan.apply_branch],
    ]
    assert error.value.last_plan == initial_plan
    message = str(error.value)
    assert "branch cleanup に失敗しました" in message
    assert f"apply_branch: {initial_plan.apply_branch}" in message
    assert f"apply_worktree: {initial_plan.apply_worktree}" in message
    assert "worktree failed" in message
    assert "cleanup failed" in message


def test_apply_commits_untracked_oracle_changes_after_cmoc_guarantee(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """未追跡 oracle 差分は自動 commit せず precondition failure にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    cmoc_log = repo / ".cmoc" / "logs" / "poll.log"
    cmoc_log.parent.mkdir(parents=True)
    cmoc_log.write_text("local log\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc/session/2026-05-10_22-21_10_000000123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert "oracles/" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "status", "--porcelain", "--", "oracles").stdout == (
        "?? oracles/\n"
    )
    assert _git(repo, "status", "--porcelain", "--", ".cmoc").stdout == ""


def test_apply_commits_preexisting_staged_oracles_after_cmoc_guarantee(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """事前 stage 済み oracle 差分も自動 commit せず拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc/session/2026-05-10_22-21_10_000000123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert "oracles/spec.md" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "status", "--porcelain", "--", "oracles").stdout == (
        "A  oracles/spec.md\n"
    )


def test_commit_all_changes_rejects_oracles_index_after_index_update(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス後も oracles/INDEX.md 差分は commit 前に止める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンス時に oracle INDEX 差分を作る fake。"""
        oracle_index = repo_root / "oracles" / "INDEX.md"
        oracle_index.parent.mkdir()
        oracle_index.write_text("index\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        lambda *args, **kwargs: "maintain indexes",
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert "oracles/INDEX.md" in error.value.detail
    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == (
        "index\n"
    )
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "status", "--porcelain").stdout


def test_commit_all_changes_rejects_committed_maintained_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス自身の oracles/INDEX.md commit も禁止 path 扱いする。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンスが oracle INDEX を自動 commit する状況を模擬する。"""
        oracle_index = repo_root / "oracles" / "INDEX.md"
        oracle_index.parent.mkdir()
        oracle_index.write_text("index\n", encoding="utf-8")
        _git(repo_root, "add", "oracles/INDEX.md")
        _git(repo_root, "commit", "-m", "Maintain INDEX.md files")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        lambda *args, **kwargs: "apply changes",
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert "oracles/INDEX.md" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Maintain INDEX.md files"
    )


def test_apply_index_maintenance_excludes_oracles_root(
    tmp_path: Path,
) -> None:
    """apply worktree の INDEX メンテナンスは oracles 配下を対象外にする。"""
    repo = _init_repo(tmp_path)

    assert _apply_index_excluded_roots(repo) == [repo / "oracles"]


def test_maintain_apply_indexes_leaves_oracles_index_unchanged(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply 用 INDEX メンテナンスは既存 oracles/INDEX.md を更新しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (oracle_root / "INDEX.md").write_text("manual oracle index\n", encoding="utf-8")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = apply_module._maintain_apply_indexes(repo)

    assert changed is True
    assert (oracle_root / "INDEX.md").read_text(encoding="utf-8") == (
        "manual oracle index\n"
    )
    assert "oracles/INDEX.md" not in _git(
        repo,
        "show",
        "--name-only",
        "--pretty=",
    ).stdout


def test_maintain_apply_indexes_does_not_create_missing_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply 用 INDEX メンテナンスは欠落した oracles/INDEX.md も作らない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = apply_module._maintain_apply_indexes(repo)

    assert changed is True
    assert not (oracle_root / "INDEX.md").exists()
    assert "oracles/INDEX.md" not in _git(
        repo,
        "show",
        "--name-only",
        "--pretty=",
    ).stdout


def test_commit_all_changes_rejects_oracle_file_after_index_update(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス後も oracle ファイル差分は commit 前に止める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンス時に oracle ファイル差分を作る fake。"""
        oracle_file = repo_root / "oracles" / "spec.md"
        oracle_file.parent.mkdir()
        oracle_file.write_text("forbidden\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert "oracles/spec.md" in error.value.detail
    assert _git(repo, "status", "--porcelain").stdout


def test_apply_implementation_files_at_commit_matches_implementation_files(
    tmp_path: Path,
) -> None:
    """apply の snapshot 調査対象は Codex 編集不能 path を含めない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text("agents\n", encoding="utf-8")
    agents_root = repo / ".agents"
    agents_root.mkdir()
    (agents_root / "skill.md").write_text("skill\n", encoding="utf-8")
    nested_memo = repo / "docs" / "memo"
    nested_memo.mkdir(parents=True)
    (nested_memo / "note.md").write_text("note\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "implementation targets")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._implementation_files_at_commit(
            repo,
            commit_hash,
        )
    ]

    assert relative_paths == [
        ".gitignore",
        "app.py",
        "docs/memo/note.md",
    ]


def test_apply_files_at_commit_exclude_tracked_root_gitignored_files(
    tmp_path: Path,
) -> None:
    """apply の snapshot 調査対象は tracked でも root .gitignore 対象を含めない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "oracles/ignored.md\nignored.py\n",
        encoding="utf-8",
    )
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept\n", encoding="utf-8")
    (oracle_root / "ignored.md").write_text("ignored\n", encoding="utf-8")
    (repo / "kept.py").write_text("kept\n", encoding="utf-8")
    (repo / "ignored.py").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "oracles/kept.md", "kept.py")
    _git(repo, "add", "-f", "oracles/ignored.md", "ignored.py")
    _git(repo, "commit", "-m", "snapshot targets")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._oracle_files_at_commit(repo, commit_hash)
    ]
    implementation_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._implementation_files_at_commit(
            repo,
            commit_hash,
        )
    ]

    assert oracle_paths == ["oracles/kept.md"]
    assert implementation_paths == [".gitignore", "kept.py"]


def test_apply_files_at_commit_use_snapshot_root_gitignore(
    tmp_path: Path,
) -> None:
    """snapshot 調査対象は現在の worktree ではなく snapshot の .gitignore で絞る。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text(
        "oracles/snapshot_ignored.md\nsnapshot_ignored.py\n",
        encoding="utf-8",
    )
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept\n", encoding="utf-8")
    (oracle_root / "snapshot_ignored.md").write_text(
        "snapshot ignored\n",
        encoding="utf-8",
    )
    (oracle_root / "worktree_ignored.md").write_text(
        "worktree ignored\n",
        encoding="utf-8",
    )
    (repo / "kept.py").write_text("kept\n", encoding="utf-8")
    (repo / "snapshot_ignored.py").write_text(
        "snapshot ignored\n",
        encoding="utf-8",
    )
    (repo / "worktree_ignored.py").write_text(
        "worktree ignored\n",
        encoding="utf-8",
    )
    _git(
        repo,
        "add",
        ".gitignore",
        "oracles/kept.md",
        "oracles/worktree_ignored.md",
        "kept.py",
        "worktree_ignored.py",
    )
    _git(
        repo,
        "add",
        "-f",
        "oracles/snapshot_ignored.md",
        "snapshot_ignored.py",
    )
    _git(repo, "commit", "-m", "snapshot targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text(
        "oracles/worktree_ignored.md\nworktree_ignored.py\n",
        encoding="utf-8",
    )

    oracle_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._oracle_files_at_commit(
            repo,
            snapshot_commit,
        )
    ]
    implementation_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._implementation_files_at_commit(
            repo,
            snapshot_commit,
        )
    ]
    changed_oracle_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._changed_oracle_files_at_commit(
            repo,
            base_commit,
            snapshot_commit,
        )
    ]
    changed_implementation_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._changed_implementation_files_at_commit(
            repo,
            base_commit,
            snapshot_commit,
        )
    ]

    assert oracle_paths == [
        "oracles/kept.md",
        "oracles/worktree_ignored.md",
    ]
    assert implementation_paths == [
        ".gitignore",
        "kept.py",
        "worktree_ignored.py",
    ]
    assert changed_oracle_paths == [
        "oracles/kept.md",
        "oracles/worktree_ignored.md",
    ]
    assert changed_implementation_paths == [
        ".gitignore",
        "kept.py",
        "worktree_ignored.py",
    ]


def test_apply_partial_targets_exclude_tracked_root_gitignored_files(
    tmp_path: Path,
) -> None:
    """部分 apply の変更調査対象は tracked でも root .gitignore 対象を含めない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "oracles/ignored.md\nignored.py\n",
        encoding="utf-8",
    )
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "base ignore rules")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept\n", encoding="utf-8")
    (oracle_root / "ignored.md").write_text("ignored\n", encoding="utf-8")
    (repo / "kept.py").write_text("kept\n", encoding="utf-8")
    (repo / "ignored.py").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", "oracles/kept.md", "kept.py")
    _git(repo, "add", "-f", "oracles/ignored.md", "ignored.py")
    _git(repo, "commit", "-m", "change targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]
    implementation_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]

    assert oracle_targets == ["oracles/kept.md"]
    assert implementation_targets == ["kept.py"]


def test_apply_partial_targets_exclude_deleted_and_keep_reverted_paths(
    tmp_path: Path,
) -> None:
    """部分 apply は削除済みを除外し、存在する履歴変更 path は対象にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (oracle_root / "obsolete.md").write_text("obsolete\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (repo / "obsolete.py").write_text("obsolete\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    (oracle_root / "spec.md").write_text("changed\n", encoding="utf-8")
    _git(repo, "add", "app.py", "oracles/spec.md")
    _git(repo, "commit", "-m", "change then revert targets")

    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "app.py", "oracles/spec.md")
    _git(repo, "commit", "-m", "revert targets")

    (repo / "obsolete.py").unlink()
    (oracle_root / "obsolete.md").unlink()
    _git(repo, "rm", "obsolete.py", "oracles/obsolete.md")
    _git(repo, "commit", "-m", "delete targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = {
        target.path.relative_to(repo).as_posix(): target.deleted_at_snapshot
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    }
    implementation_targets = {
        target.path.relative_to(repo).as_posix(): target.deleted_at_snapshot
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    }

    assert oracle_targets == {"oracles/spec.md": False}
    assert implementation_targets == {"app.py": False}


def test_apply_dirty_targets_record_snapshot_and_worktree_existence(
    tmp_path: Path,
) -> None:
    """dirty path は snapshot/worktree の存在状態を分けて対象化する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (oracle_root / "created.md").write_text("created\n", encoding="utf-8")
    (repo / "created.py").write_text("created\n", encoding="utf-8")
    (oracle_root / "spec.md").unlink()
    (repo / "app.py").unlink()

    oracle_targets = {
        target.path.relative_to(repo).as_posix(): (
            target.exists_at_snapshot,
            target.exists_in_worktree,
            target.deleted_at_snapshot,
        )
        for target in apply_module._target_oracle_files(
            repo,
            snapshot_commit,
            snapshot_commit,
            partial=True,
            dirty_paths={
                oracle_root / "created.md",
                oracle_root / "deleted.md",
                oracle_root / "spec.md",
            },
        )
    }
    implementation_targets = {
        target.path.relative_to(repo).as_posix(): (
            target.exists_at_snapshot,
            target.exists_in_worktree,
            target.deleted_at_snapshot,
        )
        for target in apply_module._target_implementation_files(
            repo,
            snapshot_commit,
            snapshot_commit,
            partial=True,
            dirty_paths={
                repo / "app.py",
                repo / "created.py",
                repo / "deleted.py",
            },
        )
    }

    assert oracle_targets == {
        "oracles/created.md": (False, True, False),
        "oracles/deleted.md": (False, False, True),
        "oracles/spec.md": (True, False, False),
    }
    assert implementation_targets == {
        "app.py": (True, False, False),
        "created.py": (False, True, False),
        "deleted.py": (False, False, True),
    }


def test_apply_dirty_changed_implementation_files_include_deleted_paths(
    tmp_path: Path,
) -> None:
    """修正後 dirty 更新用の変更実装 path は削除側 path も含める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (repo / "obsolete.py").write_text("obsolete\n", encoding="utf-8")
    (repo / "old.py").write_text("old\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base implementation files")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    _git(repo, "rm", "obsolete.py")
    _git(repo, "mv", "old.py", "new.py")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "change delete and rename implementation files")
    head_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    dirty_paths = sorted(
        path.relative_to(repo).as_posix()
        for path in apply_module._changed_implementation_files_since(
            repo,
            base_commit,
            head_commit,
        )
    )

    assert dirty_paths == [
        "app.py",
        "new.py",
        "obsolete.py",
        "old.py",
    ]


def test_apply_partial_targets_use_renamed_new_paths(
    tmp_path: Path,
) -> None:
    """部分 apply の rename 調査対象は rename 後 path だけにする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("oracle\n", encoding="utf-8")
    (repo / "old.py").write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "oracles/old.md", "oracles/new.md")
    _git(repo, "mv", "old.py", "new.py")
    _git(repo, "commit", "-m", "rename targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]
    implementation_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]

    assert oracle_targets == ["oracles/new.md"]
    assert implementation_targets == ["new.py"]


def test_apply_partial_targets_preserve_special_path_tokens(
    tmp_path: Path,
) -> None:
    """部分 apply の調査対象 path は newline や前後空白を保持する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_oracle = oracle_root / "old\nspec.md"
    old_impl = repo / "old\nimpl.py"
    old_oracle.write_text("oracle\n", encoding="utf-8")
    old_impl.write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "oracles/old\nspec.md", "oracles/ new\nspec.md ")
    _git(repo, "mv", "old\nimpl.py", " new\nimpl.py ")
    _git(repo, "commit", "-m", "rename special targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]
    implementation_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]

    assert oracle_targets == ["oracles/ new\nspec.md "]
    assert implementation_targets == [" new\nimpl.py "]


def test_apply_deleted_investigation_target_prompt_mentions_history(
    tmp_path: Path,
) -> None:
    """削除済み調査起点は存在しない path として履歴確認を促す。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "deleted.py",
        exists_at_snapshot=False,
        exists_in_worktree=False,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "deleted.py") + "` を起点" in prompt
    assert "調査対象として固定された commit 時点では存在しません" in prompt
    assert "削除差分や履歴上の変更内容" in prompt


def test_apply_oracle_investigation_prompt_orders_completion_before_details() -> None:
    """oracle 起点調査 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    repo = Path("/repo")
    target = apply_module._InvestigationTarget(
        repo / "oracles/spec.md",
        exists_at_snapshot=True,
        exists_in_worktree=True,
    )

    prompt = apply_module._investigation_prompt(repo, target)
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア実装の監査担当です。"
    assert lines[1] == "`/repo/oracles/spec.md` を起点に `/repo` の要修正点を調査してください。"
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert (
        lines.index(
            "この起点 path は調査対象として固定された commit 時点に存在するファイルです。"
        )
        > 2
    )


def test_apply_implementation_investigation_prompt_orders_completion_before_details() -> None:
    """実装起点調査 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    repo = Path("/repo")
    target = apply_module._InvestigationTarget(
        repo / "src/app.py",
        exists_at_snapshot=False,
        exists_in_worktree=False,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア実装の監査担当です。"
    assert lines[1] == "`/repo/src/app.py` を起点に、"
    assert lines[2] == "`/repo` の要修正点を調査してください。"
    assert lines[3] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "この起点 path は調査対象として固定された commit 時点では存在しません。"
        "削除差分や履歴上の変更内容を確認して調査してください。"
    ) > 3


def test_apply_created_dirty_investigation_target_prompt_mentions_worktree_content(
    tmp_path: Path,
) -> None:
    """新規作成 dirty 起点は現在 worktree の内容確認を促す。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "created.py",
        exists_at_snapshot=False,
        exists_in_worktree=True,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "created.py") + "` を起点" in prompt
    assert "調査対象として固定された commit 時点では存在せず" in prompt
    assert "現在の worktree には存在します" in prompt
    assert "前回までの修正で新規作成されたファイル" in prompt
    assert "現在の worktree の内容を確認" in prompt
    assert "削除差分や履歴上の変更内容" not in prompt


def test_apply_removed_dirty_investigation_target_prompt_mentions_deletion_diff(
    tmp_path: Path,
) -> None:
    """削除された dirty 起点は snapshot 上の存在と削除差分確認を伝える。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "removed.py",
        exists_at_snapshot=True,
        exists_in_worktree=False,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "removed.py") + "` を起点" in prompt
    assert "調査対象として固定された commit 時点には存在し" in prompt
    assert "現在の worktree には存在しません" in prompt
    assert "前回までの修正で削除されたファイル" in prompt
    assert "削除差分や履歴上の変更内容" in prompt


def test_commit_all_changes_rejects_memo_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """workspace-write prompt の読み書き禁止領域 memo は commit 前に検出する。"""
    repo = _init_repo(tmp_path)
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert "memo/" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


@pytest.mark.parametrize(
    "forbidden_file",
    [".cmoc/state.json", "README.md", "AGENTS.md"],
)
def test_commit_all_changes_rejects_root_forbidden_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    forbidden_file: str,
) -> None:
    """root の workspace-write 編集禁止 path 変更は commit 前に検出する。"""
    repo = _init_repo(tmp_path)
    target = repo / forbidden_file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("tampered\n", encoding="utf-8")
    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    if forbidden_file.startswith(".cmoc/"):
        assert ".cmoc/" in error.value.detail
    else:
        assert forbidden_file in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("README.md", "changed readme\n"),
        ("AGENTS.md", "changed agents\n"),
    ],
)
def test_commit_all_changes_rejects_root_doc_implementation_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    relative_path: str,
    content: str,
) -> None:
    """root の README/AGENTS 変更は apply 実装差分として commit しない。"""
    repo = _init_repo(tmp_path)
    target = repo / relative_path
    target.write_text(content, encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        lambda *args, **kwargs: "Apply root doc implementation change",
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert relative_path in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert target.read_text(encoding="utf-8") == content


def test_apply_discrepancies_rejects_committed_forbidden_change(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex CLI が commit 済みにした禁止 path 差分も検出する。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("base\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "add app")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(repo_root: Path, *args: object, **kwargs: object) -> str:
        """workspace-write Codex 実行中の禁止 path commit を模擬する。"""
        target = repo_root / ".agents" / "skill.md"
        target.parent.mkdir()
        target.write_text("forbidden\n", encoding="utf-8")
        _git(repo_root, "add", ".agents/skill.md")
        _git(repo_root, "commit", "-m", "commit forbidden path")
        return ""

    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        fake_codex,
    )

    with pytest.raises(CmocError) as error:
        apply_module._apply_discrepancies(
            repo,
            [
                {
                    "title": "fix",
                    "evidences": [],
                    "oracle_requirement": "requirement",
                    "observed_implementation": "observed",
                    "reason": "reason",
                    "suggested_fix": "suggested",
                }
            ],
            timer=StepTimer("test"),
            step_path=((1, 1),),
        )

    assert "編集禁止パス" in error.value.message
    assert ".agents/skill.md" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "commit forbidden path"
    )


def test_apply_parallel_investigation_records_worker_codex_events(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """並列 file 起点調査の worker 内 Codex 呼び出しもサブコマンド JSONL に残す。"""
    repo = _init_repo(tmp_path)
    oracle_path = repo / "oracles" / "docs" / "spec.md"
    implementation_path = repo / "src" / "app.py"
    oracle_path.parent.mkdir(parents=True)
    implementation_path.parent.mkdir(parents=True)
    oracle_path.write_text("# spec\n", encoding="utf-8")
    implementation_path.write_text("print('app')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "add investigation targets")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.setattr(
        apply_module,
        "_target_oracle_files",
        lambda *args, **kwargs: [
            apply_module._InvestigationTarget(oracle_path),
        ],
    )
    monkeypatch.setattr(
        apply_module,
        "_target_implementation_files",
        lambda *args, **kwargs: [
            apply_module._InvestigationTarget(implementation_path),
        ],
    )

    def fake_codex(
        repo_root: Path,
        prompt: str,
        *,
        purpose: str,
        **kwargs: object,
    ) -> str:
        """run_codex_exec の完了通知と同じイベントだけを worker thread で記録する。"""
        log_event(
            "codex_exec_call",
            {
                "purpose": purpose,
                "log_path": str(
                    repo_root / ".cmoc" / "logs" / "codex_exec" / "fake.log"
                ),
                "elapsed_seconds": 0.1,
                "returncode": 0,
            },
        )
        return json.dumps({"git_head_commit_hash": None, "fixing_points": []})

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_codex)

    with subcommand_log(repo):
        result = apply_module._investigate_discrepancies(
            repo,
            head,
            head,
            timer=StepTimer("test"),
            step_path=((1, 1),),
            repeat_improove_fixing_list=0,
            scope="full",
        )

    log_file = next((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    events = [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").splitlines()
    ]
    codex_events = [
        event for event in events if event["event"] == "codex_exec_call"
    ]
    assert result == []
    assert sorted(event["purpose"] for event in codex_events) == [
        "oracle 調査 oracles/docs/spec.md",
        "実装調査 src/app.py",
    ]


def test_apply_discrepancy_schema_rejects_incomplete_items() -> None:
    """不整合調査 JSON は仕様 schema の必須項目不足を意味的失敗として扱う。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "git_head_commit_hash": None,
                "fixing_points": [
                    {
                        "title": "missing fields",
                    }
                ]
            }
        )


def test_apply_discrepancy_schema_requires_git_head_commit_hash() -> None:
    """不整合調査 JSON は top-level の HEAD hash key 欠落を拒否する。"""
    assert set(_DISCREPANCY_OUTPUT_SCHEMA["required"]) == {
        "git_head_commit_hash",
        "fixing_points",
    }

    with pytest.raises(ValueError, match="git_head_commit_hash"):
        _validate_discrepancy_payload({"fixing_points": []})


def test_apply_discrepancy_schema_accepts_fixing_points() -> None:
    """要修正点 JSON は fixing_points と evidences 形式を受け付ける。"""
    _validate_discrepancy_payload(json.loads(_discrepancy_json("fix")))


def test_apply_discrepancy_schema_rejects_relative_evidence_path() -> None:
    """要修正点 JSON の evidence path は絶対パスでなければ拒否する。"""
    payload = json.loads(_discrepancy_json("fix"))
    payload["fixing_points"][0]["evidences"][0]["path"] = "oracles/spec.md"

    with pytest.raises(ValueError, match="must be an absolute path"):
        _validate_discrepancy_payload(payload)


def test_apply_discrepancy_schema_rejects_near_miss_keys() -> None:
    """似た名前のキーでも不整合調査 schema と一致しなければ拒否する。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "git_head_commit_hash": None,
                "fixing_points": [
                    {
                        "title": "near miss",
                        "evidence": [
                            {
                                "path": "/repo/src/app.py",
                                "line_start": 10,
                                "line_end": 12,
                                "summary": "summary",
                            }
                        ],
                        "expected_by_oracle": "requirement",
                        "observed_implementation": "observed",
                        "reason": "reason",
                        "suggested_fix": "fix",
                    }
                ]
            }
        )


def test_session_join_merges_current_session_branch_and_deletes_it(
    tmp_path: Path,
) -> None:
    """`cmoc session join` は記録済み home branch へ session を merge する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    target_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")

    cmoc_session_join_impl(repo)

    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == target_branch
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert state["session"]["state"] == "joined"
    assert "cmoc/session/2026-05-10_22-21_10_000000123" not in branches


def test_session_join_recovers_null_session_home_branch(
    tmp_path: Path,
) -> None:
    """fresh fork 後の null home branch でも session join できる。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")
    _git(repo, "commit", "-m", "feature")

    cmoc_session_join_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert state_after["session"]["state"] == "joined"
    assert state_after["session"]["session_home_branch"] == home_branch


def test_session_join_dirty_worktree_does_not_record_recovered_home_branch(
    tmp_path: Path,
) -> None:
    """dirty な session branch では復元 home branch を永続化しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    state_before = json.loads(state_path.read_text(encoding="utf-8"))
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert "未コミットの変更" in error.value.message
    assert state_after == state_before
    assert state_after["session"]["session_home_branch"] is None


def test_session_join_ensures_cmoc_ignored_before_switch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """tracked `.cmoc` state を補修 commit してから home branch へ merge する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_000000123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    state = json.loads((repo / state_path).read_text(encoding="utf-8"))
    assert captured.err == ""
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "joined"
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert home_branch in _git(repo, "branch", "--format=%(refname:short)").stdout


def test_session_join_ensures_cmoc_ignored_after_switch_to_home_branch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """home branch 側の tracked `.cmoc` も merge 前に補修する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / ".cmoc").mkdir()
    (repo / ".cmoc" / "home.log").write_text("home log\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/home.log")
    _git(repo, "commit", "-m", "track home cmoc log")
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")
    _git(repo, "commit", "-m", "feature")

    cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert captured.err == ""
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_join_rejects_non_session_branch_before_git_merge(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """通常 branch 上では session join を開始しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    target_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "checkout", "-b", "feature")
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")
    _git(repo, "checkout", target_branch)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    assert "session branch 上" in error.value.message
    assert f"現在の branch: {target_branch}" in error.value.detail
    assert (repo / "feature.txt").exists() is False
    assert "feature" in branches
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert "手動解消が必要です" not in captured.err


def test_session_join_precondition_failure_does_not_print_manual_resolution(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """merge 開始前の事前条件失敗では merge state 手動解決を案内しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    )
    state["apply"]["oracle_snapshot_commit"] = _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert "apply run" in error.value.message
    assert "手動解消が必要です" not in captured.err


def test_session_join_switch_failure_prints_manual_resolution(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """副作用段階の switch 失敗では merge 前でも手動解決を案内する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    home_branch = state["session"]["session_home_branch"]
    original_run_git = session_join_module.run_git

    def fail_switch_to_home_branch(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """home branch への switch 失敗を模擬する。"""
        if args == ["switch", home_branch]:
            raise subprocess.CalledProcessError(
                128,
                ["git", *args],
                output="",
                stderr="fatal: cannot switch branch",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_join_module,
        "run_git",
        fail_switch_to_home_branch,
    )

    with pytest.raises(subprocess.CalledProcessError):
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert "手動解消が必要です" in captured.err
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch


def test_session_join_stops_non_conflict_merge_failure_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """conflict ではない merge 失敗では Codex を呼ばず手動解決にする。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    original_run_git = session_join_module.run_git
    codex_calls: list[str] = []

    def fail_merge_without_unmerged_paths(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """merge の非 conflict 失敗を模擬する。"""
        if args == ["merge", "--no-ff", session_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                128,
                stdout="",
                stderr="fatal: refusing to merge unrelated histories",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(
        session_join_module,
        "run_git",
        fail_merge_without_unmerged_paths,
    )
    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "merge conflict は検出されませんでした" in error.value.message
    assert "fatal: refusing to merge unrelated histories" in error.value.detail
    assert "手動解消が必要です" in captured.err
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_join_rejects_binary_conflict_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """binary conflict は marker 解消対象にせず手動解消にする。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    (repo / "image.bin").write_bytes(b"base\0content\n")
    _git(repo, "add", ".gitignore", "image.bin")
    _git(repo, "commit", "-m", "prepare binary session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "image.bin").write_bytes(b"session\0content\n")
    _git(repo, "add", "image.bin")
    _git(repo, "commit", "-m", "session binary change")
    _git(repo, "switch", home_branch)
    (repo / "image.bin").write_bytes(b"home\0content\n")
    _git(repo, "add", "image.bin")
    _git(repo, "commit", "-m", "home binary change")
    _git(repo, "switch", session_branch)
    codex_calls: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict marker を持たない" in error.value.message
    assert "image.bin" in error.value.detail
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == (
        "image.bin\n"
    )


def test_session_join_rejects_modify_delete_conflict_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """delete/modify conflict は marker 不在なので手動解消にする。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    (repo / "deleted.txt").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "deleted.txt")
    _git(repo, "commit", "-m", "prepare modify delete session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "deleted.txt").write_text("session\n", encoding="utf-8")
    _git(repo, "add", "deleted.txt")
    _git(repo, "commit", "-m", "session modifies file")
    _git(repo, "switch", home_branch)
    (repo / "deleted.txt").unlink()
    _git(repo, "rm", "deleted.txt")
    _git(repo, "commit", "-m", "home deletes file")
    _git(repo, "switch", session_branch)
    codex_calls: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict marker を持たない" in error.value.message
    assert "deleted.txt" in error.value.detail
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == (
        "deleted.txt\n"
    )


def test_session_join_rejects_codex_change_outside_conflict_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が conflict 対象外を変更した場合は merge commit しない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """conflict を解消しつつ、対象外ファイルを誤って変更する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / ".gitignore").write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict 対象外" in error.value.message
    assert ".gitignore" in error.value.detail
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_rewrite_of_auto_merged_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """同じ status の非 conflict path でも内容変更は検出する。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """自動 merge 済みファイルを status 変化なしで書き換える。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / "auto.txt").write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert "auto.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_rewrite_of_auto_merged_special_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """改行や tab を含む非 conflict path の内容変更も検出する。"""
    auto_path = "dir/auto\nname\tfile.txt"
    repo = _repo_with_session_join_conflict(tmp_path, auto_path=auto_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """特殊 path の自動 merge 済みファイルを書き換える。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / auto_path).write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert auto_path in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_staged_rewrite_of_auto_merged_memo(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """memo 内容を読まずに staged auto merge の書き換えを検出する。"""
    repo = _repo_with_session_join_conflict(tmp_path, auto_path="memo/note.md")

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """禁止違反として memo を変更し、git add で status を戻す。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / "memo" / "note.md").write_text(
            "tampered\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "memo/note.md")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert "memo/note.md" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_allows_oracle_conflict_path_in_codex_guard(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """session join は conflict 対象 oracle path を Codex guard 例外へ渡す。"""
    repo = _repo_with_session_join_oracle_conflict(tmp_path)
    captured_allowed_paths: list[str] = []

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """oracle conflict を解消し、guard 例外対象を記録する。"""
        del prompt
        allowed = kwargs.get("allowed_uncommitted_oracle_paths")
        assert isinstance(allowed, list)
        captured_allowed_paths.extend(allowed)
        (repo_root / "oracles" / "spec.md").write_text(
            "resolved oracle\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert captured_allowed_paths == ["oracles/spec.md"]
    assert state["session"]["state"] == "joined"
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == (
        "resolved oracle\n"
    )


def test_session_join_allows_clean_auto_merged_root_forbidden_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """conflict 対象外で自動 merge 済みの README 変更は merge 成果物に含める。"""
    repo = _repo_with_session_join_conflict(tmp_path, auto_path="README.md")

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """本物の Codex CLI なしで conflict 対象だけを解消する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["session"]["state"] == "joined"
    assert (repo / "README.md").read_text(encoding="utf-8") == "session auto\n"
    assert _git(repo, "status", "--porcelain").stdout == ""


@pytest.mark.parametrize("root_doc_path", ["README.md", "AGENTS.md"])
def test_session_join_rejects_root_doc_file_conflict_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    root_doc_path: str,
) -> None:
    """README/AGENTS の conflict は Codex CLI に渡さず手動解決にする。"""
    repo = _repo_with_session_join_root_doc_conflict(tmp_path, root_doc_path)
    codex_calls: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "Codex CLI に依頼できない禁止領域" in error.value.message
    assert root_doc_path in error.value.detail
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()


def test_session_join_ignores_markers_outside_conflict_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """conflict 対象外の通常内容にある marker 風文字列では止めない。"""
    repo = _repo_with_session_join_conflict(tmp_path)
    (repo / "literal_markers.txt").write_text(
        "<<<<<<< sample\n"
        "left\n"
        "=======\n"
        "right\n"
        ">>>>>>> sample\n",
        encoding="utf-8",
    )
    _git(repo, "add", "literal_markers.txt")
    _git(repo, "commit", "-m", "add literal marker sample")

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """本物の Codex CLI なしで conflict 対象だけを解消する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["session"]["state"] == "joined"
    assert (repo / "literal_markers.txt").read_text(encoding="utf-8").startswith(
        "<<<<<<< sample\n"
    )


def test_session_join_rejects_remaining_diff3_base_marker(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """diff3/zdiff3 の base marker が残る場合も merge commit しない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """base marker だけが残る不完全な conflict 解消を模擬する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text(
            "resolved\n"
            "||||||| base\n"
            "base text still present\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict marker" in error.value.message
    assert "conflict.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_change_in_forbidden_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が禁止領域を作成した場合も merge commit しない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """conflict 解消後に禁止 path を誤って作る。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / ".agents").mkdir()
        (repo_root / ".agents" / "note.txt").write_text(
            "forbidden\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert ".agents/note.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_created_merge_commit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が git add/commit まで進めた場合は cmoc の commit に進まない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として merge commit を作成する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        _git(repo_root, "add", "conflict.txt")
        _git(repo_root, "commit", "--no-edit")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "merge state" in error.value.message
    assert "head:" in error.value.detail
    assert "merge_head:" in error.value.detail
    assert state["session"]["state"] == "active"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip().startswith(
        "Merge branch"
    )


def test_session_join_rejects_codex_staged_conflict_resolution(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が git add だけ実行した場合も cmoc の add/commit に進まない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として conflict 対象を stage する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        _git(repo_root, "add", "conflict.txt")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "merge state" in error.value.message
    assert "unmerged_index: changed" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_aborted_merge(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が merge state を中止した場合は後続の add/commit に進まない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として merge を abort する。"""
        del prompt, kwargs
        _git(repo_root, "merge", "--abort")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "merge state" in error.value.message
    assert "merge_head:" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_switched_branch_after_abort(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が branch を移動した場合は現在 branch の変化を明示検出する。"""
    repo = _repo_with_session_join_conflict(tmp_path)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として merge を abort して session branch へ戻る。"""
        del prompt, kwargs
        _git(repo_root, "merge", "--abort")
        _git(repo_root, "switch", session_branch)

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "merge state" in error.value.message
    assert "branch:" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch


def test_session_abandon_marks_state_and_force_deletes_branch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc session abandon` は session branch を merge せず破棄する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "session-only feature")

    cmoc_session_abandon_impl(repo)

    captured = capsys.readouterr()
    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "abandoned"
    assert state["session"].get("joined_at") is None
    assert "cmoc/session/2026-05-10_22-21_10_000000123" not in branches
    assert (repo / "feature.txt").exists() is False
    assert (
        "abandoned session branch: cmoc/session/2026-05-10_22-21_10_000000123"
        in captured.out
    )


def test_session_abandon_recovers_null_session_home_branch(
    tmp_path: Path,
) -> None:
    """fresh fork 後の null home branch でも session abandon できる。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    (repo / "feature.txt").write_text("session only\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")
    _git(repo, "commit", "-m", "session only")

    cmoc_session_abandon_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert (repo / "feature.txt").exists() is False
    assert state_after["session"]["state"] == "abandoned"
    assert state_after["session"]["session_home_branch"] == home_branch
    assert "cmoc/session/2026-05-10_22-21_10_000000123" not in branches


def test_session_abandon_dirty_worktree_does_not_record_recovered_home_branch(
    tmp_path: Path,
) -> None:
    """dirty な session branch では復元 home branch を永続化しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    state_before = json.loads(state_path.read_text(encoding="utf-8"))
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "未コミットの変更" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state_after == state_before
    assert state_after["session"]["session_home_branch"] is None
    assert "cmoc/session/2026-05-10_22-21_10_000000123" in branches


def test_session_abandon_ensures_cmoc_ignored_before_cleanup(
    tmp_path: Path,
) -> None:
    """tracked `.cmoc` state を補修し、home branch 側も ignore 保証する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_000000123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    cmoc_session_abandon_impl(repo)

    state = json.loads((repo / state_path).read_text(encoding="utf-8"))
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "abandoned"
    assert session_branch not in branches
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_abandon_rejects_apply_run_before_cleanup(
    tmp_path: Path,
) -> None:
    """apply run が ready でなければ branch/state を変更しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    )
    state["apply"]["oracle_snapshot_commit"] = _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    assert "apply run" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state_after["session"]["state"] == "active"
    assert "cmoc/session/2026-05-10_22-21_10_000000123" in branches


def test_session_abandon_rejects_uncommitted_changes_before_switch(
    tmp_path: Path,
) -> None:
    """未コミット差分がある場合は home branch へ戻らず停止する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "未コミットの変更" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state["session"]["state"] == "active"


def test_session_abandon_reports_home_switch_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """home branch への switch 失敗も cleanup 失敗として再実行を促す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_run_git = session_abandon_module.run_git

    def fail_home_switch(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """cleanup 最初の home branch switch 失敗を模擬する。"""
        if args == ["switch", home_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake home switch failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(session_abandon_module, "run_git", fail_home_switch)

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "cleanup failure" in error.value.detail
    assert "fake home switch failure" in error.value.detail
    assert "rollback failure" not in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_abandon_rolls_back_cmoc_repair_commit_on_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`.cmoc` 補修後の失敗では、session branch HEAD も元へ戻す。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    original_run_git = session_abandon_module.run_git

    def fail_home_switch_after_repair(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """`.cmoc` 補修 commit の直後に home branch switch 失敗を模擬する。"""
        if args == ["switch", home_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake home switch failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_abandon_module,
        "run_git",
        fail_home_switch_after_repair,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "rollback failure" not in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == original_session_head
    assert (repo / ".gitignore").exists() is False
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert state["session"]["state"] == "active"


def test_session_abandon_rolls_back_home_repair_commit_on_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """home branch 側の `.cmoc` 補修 commit も cleanup 失敗時に戻す。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    original_home_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    original_run_git = session_abandon_module.run_git

    def fail_branch_delete_after_home_repair(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """home branch の `.cmoc` 補修 commit 後に branch 削除失敗を模擬する。"""
        if args == ["branch", "-D", session_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake branch delete failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_abandon_module,
        "run_git",
        fail_branch_delete_after_home_repair,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "rollback failure" not in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == original_session_head
    assert _git(repo, "rev-parse", home_branch).stdout.strip() == original_home_head
    assert (repo / ".gitignore").exists() is False
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert state["session"]["state"] == "active"


def test_session_abandon_reports_rollback_switch_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """checkout 復旧失敗も active state に戻し、再実行を促す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_run_git = session_abandon_module.run_git

    def fail_cleanup_and_restore_switch(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """branch 削除失敗と session branch への復旧失敗を模擬する。"""
        if args == ["branch", "-D", session_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake branch delete failure",
            )
        if args == ["switch", session_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                stdout="",
                stderr="fake switch failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_abandon_module,
        "run_git",
        fail_cleanup_and_restore_switch,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "cleanup failure" in error.value.detail
    assert "fake branch delete failure" in error.value.detail
    assert "rollback failure" in error.value.detail
    assert "fake switch failure" in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_abandon_reports_state_restore_failure_after_branch_delete_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """branch 削除失敗後の active rollback 保存失敗を detail に含める。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_run_git = session_abandon_module.run_git
    original_write_session_state = session_abandon_module.write_session_state
    restore_switches: list[list[str]] = []

    def fail_branch_delete(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """cleanup の branch 削除失敗と rollback switch 呼び出しを観測する。"""
        if args == ["branch", "-D", session_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake branch delete failure",
            )
        if args == ["switch", session_branch]:
            restore_switches.append(args)
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def fail_active_state_restore(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
    ) -> Path:
        """active への rollback 保存失敗を模擬する。"""
        session = state.get("session")
        if isinstance(session, dict) and session.get("state") == "active":
            raise OSError("fake state restore failure")
        return original_write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(session_abandon_module, "run_git", fail_branch_delete)
    monkeypatch.setattr(
        session_abandon_module,
        "write_session_state",
        fail_active_state_restore,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "cleanup failure" in error.value.detail
    assert "fake branch delete failure" in error.value.detail
    assert "rollback failure" in error.value.detail
    assert "fake state restore failure" in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert restore_switches == [["switch", session_branch]]
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert state["session"]["state"] == "abandoned"
    assert session_branch in branches


def test_session_abandon_does_not_delete_branch_when_abandoned_save_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """abandoned 保存失敗時は branch 削除前に停止し、再実行可能に戻す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    delete_calls: list[list[str]] = []
    original_run_git = session_abandon_module.run_git
    original_write_session_state = session_abandon_module.write_session_state

    def observe_branch_delete(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """state 保存失敗時に branch 削除へ進まないことを観測する。"""
        if args == ["branch", "-D", session_branch]:
            delete_calls.append(args)
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def fail_abandoned_state_save(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
    ) -> Path:
        """cleanup 終盤の abandoned 保存失敗を模擬する。"""
        session = state.get("session")
        if isinstance(session, dict) and session.get("state") == "abandoned":
            raise OSError("fake abandoned save failure")
        return original_write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(session_abandon_module, "run_git", observe_branch_delete)
    monkeypatch.setattr(
        session_abandon_module,
        "write_session_state",
        fail_abandoned_state_save,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "fake abandoned save failure" in error.value.detail
    assert "rollback failure" not in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert delete_calls == []
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == original_session_head
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_main_typer_functions_delegate_only_to_impls() -> None:
    """Typer 対応関数は共通 runner ではなく対応する impl 呼び出しだけを持つ。"""
    import main

    source = inspect.getsource(main)
    review_oracles_source = inspect.getsource(main.review_oracles_command)

    assert "def _run_command" not in source
    assert "_run_command(" not in source
    assert "cmoc_init_impl()" in source
    assert "cmoc_indexing_impl()" in source
    assert "cmoc_session_fork_impl()" in source
    assert "importlib.util" not in source
    assert "spec_from_file_location" not in source
    assert (
        "from sub_commands.review.oracles import cmoc_review_oracles_impl"
        in source
    )
    assert "from sub_commands.indexing import cmoc_indexing_impl" in source
    assert "eval-oracles.py" not in source
    assert "eval_oracles_source" not in review_oracles_source
    assert "cmoc_review_oracles_impl(" in source
    assert "scope=scope" in source
    assert "enumerate_findings_loop=enumerate_findings_loop" in source
    assert "merge_findings_loop=merge_findings_loop" in source
    assert "refine_findings_loop=refine_findings_loop" in source
    assert "repeat_investigate_and_fix=repeat_investigate_and_fix" in source
    assert "repeat_improove_fixing_list=repeat_improove_fixing_list" in source
    assert "cmoc_session_join_impl()" in source
    assert "cmoc_session_abandon_impl()" in source
    assert "cmoc_apply_abandon_impl()" in source


def test_cmoc_help_uses_cmoc_command_name() -> None:
    """PATH 経由の `cmoc --help` は Usage に cmoc を表示する。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main", "--help"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "Usage: cmoc [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "session" in result.stdout
    assert "apply" in result.stdout
    assert "review" in result.stdout
    assert "indexing" in result.stdout
    assert re.search(r"\bbranch\b", result.stdout) is None
    assert re.search(r"\bmerge\b", result.stdout) is None
    assert re.search(r"\beval-oracle(?!s)\b", result.stdout) is None


def test_cmoc_review_oracles_command_and_compat_alias_are_registered() -> None:
    """`review oracles` を正名にし、既存 alias も残す。"""
    repo_root = Path(__file__).resolve().parents[1]
    env = {"PYTHONPATH": str(repo_root / "src")}
    review = subprocess.run(
        [sys.executable, "-m", "main", "review", "oracles", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    plural_alias = subprocess.run(
        [sys.executable, "-m", "main", "eval-oracles", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    singular = subprocess.run(
        [sys.executable, "-m", "main", "eval-oracle", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert review.returncode == 0
    assert plural_alias.returncode == 0
    assert singular.returncode == 0
    assert "Usage: cmoc review oracles [OPTIONS]" in review.stdout
    assert "--scope" in review.stdout
    assert "-s" in review.stdout
    assert "--enumerate-findings" in review.stdout
    assert "--merge-findings-loop" in review.stdout
    assert "--refine-findings-loop" in review.stdout
    assert "--full" not in review.stdout
    assert "--repeat-improve-issu" not in review.stdout
    assert "Usage: cmoc eval-oracles [OPTIONS]" in plural_alias.stdout
    assert "Usage: cmoc eval-oracle [OPTIONS]" in singular.stdout
    assert review.stderr == ""
    assert plural_alias.stderr == ""
    assert singular.stderr == ""


def test_cmoc_indexing_command_is_registered_and_takes_no_arguments() -> None:
    """`cmoc indexing` は root 直下の引数なしサブコマンドとして登録される。"""
    repo_root = Path(__file__).resolve().parents[1]
    env = {"PYTHONPATH": str(repo_root / "src")}
    help_result = subprocess.run(
        [sys.executable, "-m", "main", "indexing", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    extra_arg_result = subprocess.run(
        [sys.executable, "-m", "main", "indexing", "unexpected"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert help_result.returncode == 0
    assert "Usage: cmoc indexing [OPTIONS]" in help_result.stdout
    assert help_result.stderr == ""
    assert extra_arg_result.returncode == 2
    assert extra_arg_result.stderr == ""
    _assert_markdown_error_report(extra_arg_result.stdout)
    assert "Got unexpected extra argument" in extra_arg_result.stdout


def test_cmoc_apply_fork_help_exposes_oracle_repeat_options() -> None:
    """`cmoc apply fork --help` は oracle で定義された正式オプションを表示する。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main", "apply", "fork", "--help"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "--apply-loop" in result.stdout
    assert "--improove-fixing" in result.stdout
    assert "--scope" in result.stdout
    assert "-s" in result.stdout
    assert "--full" not in result.stdout


def test_cmoc_apply_fork_repeat_validation_reports_oracle_option_names() -> None:
    """apply fork の回数検証メッセージは oracle の正式オプション名を案内する。"""
    with pytest.raises(CmocError) as apply_loop_error:
        apply_module._validate_repeat_options(-1, 0)
    assert "--apply-loop" in "\n".join(apply_loop_error.value.actions)
    assert "--repeat-investigate-and-fix" not in "\n".join(
        apply_loop_error.value.actions,
    )

    with pytest.raises(CmocError) as fixing_list_loop_error:
        apply_module._validate_repeat_options(0, -1)
    assert "--improove-fixing-list-loop" in "\n".join(
        fixing_list_loop_error.value.actions,
    )
    assert "--repeat-improove-fixing-list" not in "\n".join(
        fixing_list_loop_error.value.actions,
    )


def test_cmoc_review_oracles_rejects_too_many_refine_findings_loops() -> None:
    """CLI 入口でも所見リスト検証ループの最大 3 回制限を検証する。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "main",
            "review",
            "oracles",
            "--refine-findings-loop",
            "4",
        ],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode != 0
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "4 is not in the range 0<=x<=3" in result.stdout


def test_cmoc_session_and_apply_workflow_commands_are_registered() -> None:
    """公開 CLI は session/apply の階層コマンドを登録する。"""
    repo_root = Path(__file__).resolve().parents[1]
    env = {"PYTHONPATH": str(repo_root / "src")}
    commands = [
        ("session", "fork"),
        ("session", "join"),
        ("session", "abandon"),
        ("apply", "fork"),
        ("apply", "join"),
        ("apply", "abandon"),
    ]

    for command_group, command_name in commands:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "main",
                command_group,
                command_name,
                "--help",
            ],
            cwd=repo_root,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert result.returncode == 0
        assert (
            f"Usage: cmoc {command_group} {command_name} [OPTIONS]"
            in result.stdout
        )
        assert result.stderr == ""


def test_main_returns_nonzero_for_subcommand_error() -> None:
    """サブコマンド内エラーはプロセス終了コードへ反映される。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "main",
            "apply",
            "fork",
            "--repeat-investigate-and-fix",
            "-1",
        ],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "# Command completion report" in result.stdout


def test_main_reports_no_args_error_with_non_empty_detail() -> None:
    """引数なし起動も help と混ざらない stdout エラーレポートにする。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 2
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "## Summary\nコマンドが指定されていません。" in result.stdout
    assert "- 利用可能なコマンドを確認するには `cmoc --help` を実行してください。" in result.stdout
    assert "`cmoc indexing`" in result.stdout
    assert "## Detail\ncmoc がサブコマンドなしで起動されました。" in result.stdout
    assert "Traceback (most recent call last):" in result.stdout
    assert "raise _missing_command_error(\"cmoc\")" in result.stdout
    assert "Traceback is not available for this exception." not in result.stdout
    assert "Usage: cmoc [OPTIONS] COMMAND [ARGS]..." not in result.stdout


def test_main_delegates_root_completion_probe_to_typer() -> None:
    """root 補完プローブでは cmoc 独自エラーレポートを出さない。"""
    result = _run_completion_probe([], "cmoc ", 1)

    assert result.returncode == 0
    assert result.stderr == ""
    assert "ERROR" not in result.stdout
    assert "## Summary" not in result.stdout
    assert "init" in result.stdout
    assert "indexing" in result.stdout
    assert "session" in result.stdout
    assert "apply" in result.stdout
    assert "review" in result.stdout


@pytest.mark.parametrize("command_group", ["session", "apply", "review"])
def test_main_reports_command_group_without_subcommand_as_single_error_report(
    command_group: str,
) -> None:
    """command group だけの起動も help と混ぜず stdout に報告する。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main", command_group],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 2
    assert result.stderr == ""
    assert result.stdout.count("ERROR") == 1
    _assert_markdown_error_report(result.stdout)
    assert "## Summary\nコマンドが指定されていません。" in result.stdout
    assert (
        f"- 利用可能なコマンドを確認するには `cmoc {command_group} --help` を実行してください。"
        in result.stdout
    )
    assert (
        f"## Detail\ncmoc {command_group} がサブコマンドなしで起動されました。"
        in result.stdout
    )
    assert "Traceback (most recent call last):" in result.stdout
    assert "Traceback is not available for this exception." not in result.stdout
    assert f"Usage: cmoc {command_group}" not in result.stdout


@pytest.mark.parametrize(
    ("command_group", "expected_commands"),
    [
        ("session", ["fork", "join", "abandon"]),
        ("apply", ["fork", "join", "abandon"]),
        ("review", ["oracles"]),
    ],
)
def test_main_delegates_group_completion_probe_to_typer(
    command_group: str,
    expected_commands: list[str],
) -> None:
    """command group 直下の補完プローブでも独自エラーを出さない。"""
    result = _run_completion_probe(
        [command_group],
        f"cmoc {command_group} ",
        2,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert "ERROR" not in result.stdout
    assert "## Summary" not in result.stdout
    for expected_command in expected_commands:
        assert expected_command in result.stdout


@pytest.mark.parametrize("complete_value", ["", "bash_complete", "invalid"])
def test_main_silently_exits_for_unsupported_completion_instruction(
    complete_value: str,
) -> None:
    """未対応の補完指示では通常 parse error を出さず静かに終了する。"""
    result = _run_completion_probe(
        [],
        "cmoc ",
        1,
        complete_value=complete_value,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_format_error_report_fills_empty_generic_detail() -> None:
    """通常例外の文字列表現が空でも Detail を空欄にしない。"""
    error = Exception()

    report = format_error_report(error)

    _assert_markdown_error_report(report)
    assert "## Summary\nException" in report
    assert (
        "- 入力値が誤っている場合は、コマンド引数を修正してから cmoc を再実行してください。"
        in report
    )
    assert (
        "- リポジトリ状態が原因の場合は、Detail と Call stack を確認して作業ツリーや設定を修正してください。"
        in report
    )
    assert "## Detail\nbuiltins.Exception がメッセージなしで発生しました。" in report


def test_format_error_report_includes_called_process_output() -> None:
    """git 失敗時は capture 済みの stderr/stdout を Detail に含める。"""
    error = subprocess.CalledProcessError(
        returncode=128,
        cmd=["git", "switch", "missing branch"],
        output="stdout diagnostic\n",
        stderr="fatal: invalid reference: missing branch\n",
    )

    report = format_error_report(error)

    _assert_markdown_error_report(report)
    assert "## Summary\nCalledProcessError" in report
    assert "## Detail" in report
    assert "returncode:\n128" in report
    assert "cmd:\ngit switch 'missing branch'" in report
    assert "stderr:\nfatal: invalid reference: missing branch" in report
    assert "stdout:\nstdout diagnostic" in report


def test_format_error_report_uses_passed_exception_traceback() -> None:
    """except 外でも、渡された例外自身の traceback を表示する。"""

    def raise_target_error() -> None:
        raise RuntimeError("target failure")

    try:
        raise_target_error()
    except RuntimeError as captured:
        error = captured

    try:
        raise ValueError("unrelated failure")
    except ValueError:
        report = format_error_report(error)

    assert "RuntimeError: target failure" in report
    assert "raise_target_error()" in report
    assert 'raise RuntimeError("target failure")' in report
    assert "ValueError: unrelated failure" not in report


def test_format_error_report_describes_missing_traceback() -> None:
    """未 raise の例外では NoneType ではなく traceback 不在を明示する。"""
    error = RuntimeError("not raised")

    report = format_error_report(error)

    assert "RuntimeError: not raised" not in report
    assert "NoneType: None" not in report
    assert "Traceback is not available for this exception." in report


def test_user_facing_error_text_does_not_keep_known_english_phrases() -> None:
    """共通エラーレポートに渡す説明・次アクションを日本語方針で固定する。"""
    repo_root = Path(__file__).resolve().parents[1]
    target_paths = [
        repo_root / "src" / "commons" / "errors.py",
        repo_root / "src" / "commons" / "repo.py",
        repo_root / "src" / "sub_commands" / "apply" / "fork.py",
        repo_root / "src" / "sub_commands" / "session" / "abandon.py",
        repo_root / "src" / "sub_commands" / "session" / "join.py",
    ]
    forbidden_fragments = [
        "Git repository root was not found.",
        "Move into a git-managed repository.",
        "Uncommitted changes exist.",
        "Commit or stash",
        "cmoc apply must be run on a cmoc managed branch.",
        "Run `cmoc session fork` first.",
        "Failed to resolve cmoc managed branch automatically.",
        "Pass the cmoc managed branch name explicitly.",
        "Inspect git status manually.",
        "Resolve remaining conflict markers manually.",
        "Manual resolution is required.",
    ]
    source_text = "\n".join(
        path.read_text(encoding="utf-8") for path in target_paths
    )

    for fragment in forbidden_fragments:
        assert fragment not in source_text


def test_bin_cmoc_requires_venv_python() -> None:
    """ランチャーは system python3 へフォールバックせず、エラーは stdout へ出す。"""
    repo_root = Path(__file__).resolve().parents[1]
    launcher = (repo_root / "bin" / "cmoc").read_text(encoding="utf-8")

    assert launcher.startswith("#!/bin/sh")
    assert "#!/usr/bin/env python3" not in launcher
    assert 'exec "$venv_python"' in launcher
    assert "} >&2" not in launcher


def test_test_sh_uses_own_worktree_bin_before_venv(tmp_path: Path) -> None:
    """test.sh は自身の worktree の bin/cmoc を PATH で優先する。"""
    repo_root = Path(__file__).resolve().parents[1]
    outside = tmp_path / "outside"
    fake_venv_bin = tmp_path / "fake-venv" / "bin"
    fake_venv_bin.mkdir(parents=True)
    outside.mkdir()
    (fake_venv_bin / "cmoc").write_text(
        "#!/bin/sh\nprintf '%s\\n' fake-venv-cmoc\n",
        encoding="utf-8",
    )
    (fake_venv_bin / "cmoc").chmod(0o755)

    result = subprocess.run(
        [
            "bash",
            "-c",
            (
                "set -eu\n"
                "cd \"$1\"\n"
                "PATH=\"$2:$PATH\"\n"
                ". \"$3/test.sh\"\n"
                "printf '%s\\n' \"$CMOC_ROOT\"\n"
                "printf '%s\\n' \"${PATH%%:*}\"\n"
                "without_first=${PATH#*:}\n"
                "printf '%s\\n' \"${without_first%%:*}\"\n"
                "command -v cmoc\n"
            ),
            "bash",
            str(outside),
            str(fake_venv_bin),
            str(repo_root),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    lines = result.stdout.splitlines()
    assert result.stderr == ""
    assert lines == [
        str(repo_root),
        str(repo_root / "bin"),
        str(repo_root / ".venv" / "bin"),
        str(repo_root / "bin" / "cmoc"),
    ]


def test_bin_cmoc_reports_missing_venv_to_stdout(tmp_path: Path) -> None:
    """仮想環境が無い場合も共通エラーレポートを stdout へ出す。"""
    repo_root = Path(__file__).resolve().parents[1]
    launcher = tmp_path / "repo" / "bin" / "cmoc"
    launcher.parent.mkdir(parents=True)
    launcher.write_text(
        (repo_root / "bin" / "cmoc").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    result = subprocess.run(
        [str(launcher), "--help"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "仮想環境 Python" in result.stdout
    assert "at print_missing_venv_error" in result.stdout
    assert "at require_venv_python" in result.stdout
    assert "at main" in result.stdout
    assert "仮想環境 Python の実行可能性チェック" not in result.stdout


@pytest.mark.parametrize("complete_value", ["complete_bash", ""])
def test_bin_cmoc_suppresses_missing_venv_report_for_completion_probe(
    tmp_path: Path,
    complete_value: str,
) -> None:
    """補完プローブでは venv 欠落時も独自エラーレポートを混ぜない。"""
    repo_root = Path(__file__).resolve().parents[1]
    launcher = tmp_path / "repo" / "bin" / "cmoc"
    launcher.parent.mkdir(parents=True)
    launcher.write_text(
        (repo_root / "bin" / "cmoc").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    result = subprocess.run(
        [str(launcher)],
        check=False,
        env={
            "_CMOC_COMPLETE": complete_value,
            "COMP_WORDS": "cmoc ",
            "COMP_CWORD": "1",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    assert result.stdout == ""


@pytest.mark.parametrize(
    "relative_path",
    [
        ".cmoc/state.json",
        ".agents/config.json",
        "memo/note.md",
    ],
)
def test_session_join_forbidden_conflict_paths_exclude_root_docs(
    relative_path: str,
) -> None:
    """session join は編集禁止 path の conflict を Codex に渡さない。"""
    assert session_join_module._is_forbidden_conflict_path(relative_path)


@pytest.mark.parametrize("relative_path", ["README.md", "AGENTS.md"])
def test_session_join_root_docs_are_forbidden_conflict_paths(
    relative_path: str,
) -> None:
    """README/AGENTS の conflict は marker 解消対象にしない。"""
    assert session_join_module._is_forbidden_conflict_path(relative_path)


def test_session_join_conflict_prompt_allows_marker_only_oracle_fix() -> None:
    """conflict 対象 oracle file は marker 解消に限って編集できる。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["app.py", "oracles/spec.md"])

    assert "あなたは merge conflict 解消担当です。" in prompt
    assert "cmoc session join" not in prompt
    assert "`/repo/oracles` は編集禁止です。" not in prompt
    assert "`/repo/.cmoc` は編集禁止です。" in prompt
    assert "`/repo/README.md` は編集禁止です。" in prompt
    assert "`/repo/AGENTS.md` は編集禁止です。" in prompt
    assert "['/repo/app.py', '/repo/oracles/spec.md']" in prompt
    assert "['app.py" not in prompt
    assert "conflict marker 解消に限って編集できます" in prompt
    assert "意味的な仕様改訂" in prompt
    assert "conflict 対象外 oracle file の編集は禁止" in prompt
    assert "解決内容と未解決ファイルの有無を報告" in prompt


def test_session_join_conflict_prompt_keeps_root_docs_forbidden() -> None:
    """README/AGENTS は conflict prompt でも編集禁止として指示する。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["README.md", "AGENTS.md"])

    assert "`/repo/README.md` は編集禁止です。" in prompt
    assert "`/repo/AGENTS.md` は編集禁止です。" in prompt
    assert "['/repo/README.md', '/repo/AGENTS.md']" in prompt
    assert "root document file は conflict marker 解消に限って編集できます" not in prompt
    assert "conflict 対象外 root document file の編集は禁止" not in prompt


def test_files_with_conflict_markers_checks_requested_paths_only(
    tmp_path: Path,
) -> None:
    """marker 検査は渡された対象一覧だけを見る。"""
    repo = _init_repo(tmp_path)
    conflicted = repo / "conflicted.txt"
    unrelated = repo / "unrelated.txt"
    conflicted.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )
    unrelated.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )
    _git(repo, "add", "conflicted.txt", "unrelated.txt")
    _git(repo, "commit", "-m", "add tracked files")

    assert _files_with_conflict_markers(repo, ["conflicted.txt"]) == [
        "conflicted.txt"
    ]


def _discrepancy_json(suggested_fix: str) -> str:
    """テスト用の valid な不整合 JSON を返す。"""
    return json.dumps(
        {
            "git_head_commit_hash": None,
            "fixing_points": [
                {
                    "title": "t",
                    "evidences": [
                        {
                            "path": "/repo/oracles/spec.md",
                            "line_start": 1,
                            "line_end": 1,
                            "summary": "spec",
                        }
                    ],
                    "oracle_requirement": "r",
                    "observed_implementation": "o",
                    "reason": "x",
                    "suggested_fix": suggested_fix,
                }
            ]
        }
    )


def _change_summary_json() -> str:
    """テスト用の valid な変更要約 JSON を返す。"""
    return json.dumps(
        {
            "changes": [
                {
                    "category": "実装修正",
                    "summary": "テスト用の変更内容を整理しました。",
                    "changed_paths": ["app.py"],
                }
            ]
        }
    )


def _apply_report(prompt: str, result_label: str, counts: list[int]) -> str:
    """apply report prompt から branch 名を抜き出した valid report を返す。"""
    match = re.search(r"ブランチ `([^`]+)`", prompt)
    branch_name = match.group(1) if match else "cmoc/apply/session/run"
    count_lines = [
        f"{index} 回目: {count} 件"
        for index, count in enumerate(counts, start=1)
    ]
    if result_label == "未収束":
        count_lines.append("まだ要修正点が残っている可能性があります。")
    return "\n".join(
        [
            "## 作業結果",
            result_label,
            "## 要修正点件数の推移",
            *count_lines,
            f"## ブランチ {branch_name} 上の全変更内容",
            "- カテゴリ: 実装修正",
            "  - テスト用の変更内容を整理しました。",
        ]
    )


def _eval_oracle_issue(
    severity: str,
    title: str,
    oracle_path: Path,
    line_start: int | None,
    line_end: int | None,
    referenced_paths: list[Path] | None = None,
) -> dict[str, object]:
    """テスト用の valid な eval-oracles issue item を返す。"""
    references = referenced_paths or [oracle_path]
    return {
        "severity": severity,
        "title": title,
        "oracle_path": str(oracle_path.resolve()),
        "oracle_line_start": line_start,
        "oracle_line_end": line_end,
        "referenced_paths": [str(path.resolve()) for path in references],
        "affected_workflow": "cmoc review oracles",
        "requirement": f"{title} requirement",
        "problem": f"{title} problem",
        "reason": f"{title} reason",
        "suggested_oracle_change": f"{title} change",
        "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
    }


def _init_repo(tmp_path: Path) -> Path:
    """テスト用 git repo を作り、初期 commit を置く。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "initial")
    return repo


def _checkout_session_branch(repo: Path) -> None:
    """テスト用 cmoc session branch に移動し、state を作る。"""
    session_id = "2026-05-10_22-21_10_000000123"
    branch_name = f"cmoc/session/{session_id}"
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "-b", branch_name)
    write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": home_branch,
                "session_start_commit": base_commit,
                "last_joined_apply_oracle_snapshot_commit": None,
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )
    exclude = repo / ".git" / "info" / "exclude"
    exclude.write_text(f"{exclude.read_text(encoding='utf-8')}\n.cmoc/\n")


def _prepare_review_oracles_session(repo: Path) -> None:
    """review oracles 実行用に clean な session branch へ移動する。"""
    gitignore = repo / ".gitignore"
    content = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if "/.cmoc/" not in content.splitlines():
        prefix = content
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        gitignore.write_text(f"{prefix}/.cmoc/\n", encoding="utf-8")

    if _git(repo, "status", "--porcelain").stdout.strip():
        _git(repo, "add", "-A")
        _git(repo, "commit", "-m", "prepare review oracles")

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    if not branch_name.startswith("cmoc/session/"):
        _checkout_session_branch(repo)


def _repo_with_session_join_conflict(
    tmp_path: Path,
    auto_path: str = "auto.txt",
) -> Path:
    """session join で conflict と自動 merge path が発生する repo を作る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    (repo / "conflict.txt").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "conflict.txt")
    _git(repo, "commit", "-m", "prepare session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "conflict.txt").write_text("session\n", encoding="utf-8")
    auto_file = repo / auto_path
    auto_file.parent.mkdir(parents=True, exist_ok=True)
    auto_file.write_text("session auto\n", encoding="utf-8")
    _git(repo, "add", "conflict.txt", auto_path)
    _git(repo, "commit", "-m", "session change")
    _git(repo, "switch", home_branch)
    (repo / "conflict.txt").write_text("home\n", encoding="utf-8")
    _git(repo, "add", "conflict.txt")
    _git(repo, "commit", "-m", "home change")
    _git(repo, "switch", session_branch)
    return repo


def _repo_with_session_join_oracle_conflict(tmp_path: Path) -> Path:
    """session join で oracle file conflict が発生する repo を作る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("base oracle\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "oracles/spec.md")
    _git(repo, "commit", "-m", "prepare oracle session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (oracle_root / "spec.md").write_text("session oracle\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "session oracle change")
    _git(repo, "switch", home_branch)
    (oracle_root / "spec.md").write_text("home oracle\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "home oracle change")
    _git(repo, "switch", session_branch)
    return repo


def _repo_with_session_join_root_doc_conflict(
    tmp_path: Path,
    relative_path: str,
) -> Path:
    """session join で root doc file conflict が発生する repo を作る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / relative_path
    target.write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", relative_path)
    _git(repo, "commit", "-m", "prepare root doc session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    target.write_text("session\n", encoding="utf-8")
    _git(repo, "add", relative_path)
    _git(repo, "commit", "-m", "session change")
    _git(repo, "switch", home_branch)
    target.write_text("home\n", encoding="utf-8")
    _git(repo, "add", relative_path)
    _git(repo, "commit", "-m", "home change")
    _git(repo, "switch", session_branch)
    return repo


def _add_oracle_snapshot(repo: Path) -> str:
    """テスト用 oracle snapshot commit を作る。"""
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "add oracle")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _create_completed_apply_run(
    repo: Path,
    oracle_snapshot: str,
    *,
    report_text: str | None = None,
) -> tuple[str, Path, Path]:
    """completed apply run の branch/worktree/state を作る。"""
    session_id = "2026-05-10_22-21_10_000000123"
    apply_branch = f"cmoc/apply/{session_id}/2026-05-10_22-22_10_000000123"
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / session_id
        / "2026-05-10_22-22_10_000000123"
    )
    report_path = repo / ".cmoc" / "reports" / "apply" / "fork" / "report.md"
    report_path.parent.mkdir(parents=True)
    if report_text is None:
        report_text = "\n".join(
            [
                "---",
                f'cmoc_apply_branch: "{apply_branch}"',
                'result: "収束"',
                "---",
                "",
                "## 作業結果",
                "収束",
                "",
            ]
        )
    report_path.write_text(report_text, encoding="utf-8")
    _git(repo, "branch", apply_branch, oracle_snapshot)
    _git(repo, "worktree", "add", str(apply_worktree), apply_branch)
    state = json.loads(
        (repo / ".cmoc" / "sessions" / f"{session_id}.json").read_text(
            encoding="utf-8"
        )
    )
    state["session"]["session_home_branch"] = None
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "apply_worktree": str(apply_worktree),
        "oracle_snapshot_commit": oracle_snapshot,
        "completed": True,
        "discrepancy_counts": [0],
        "report_path": str(report_path),
    }
    write_session_state(repo, session_id, state)
    return apply_branch, apply_worktree, report_path


def _session_state_paths(repo: Path) -> list[Path]:
    """テスト repo の session state file 一覧を返す。"""
    session_root = repo / ".cmoc" / "sessions"
    if not session_root.exists():
        return []
    return sorted(session_root.glob("*.json"))


def _run_completion_probe(
    arguments: list[str],
    comp_words: str,
    comp_cword: int,
    *,
    complete_value: str = "complete_bash",
) -> subprocess.CompletedProcess[str]:
    """main module を Click/Typer 補完プローブとして実行する。"""
    repo_root = Path(__file__).resolve().parents[1]
    return subprocess.run(
        [sys.executable, "-m", "main", *arguments],
        cwd=repo_root,
        env={
            "PYTHONPATH": str(repo_root / "src"),
            "_CMOC_COMPLETE": complete_value,
            "COMP_WORDS": comp_words,
            "COMP_CWORD": str(comp_cword),
        },
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """git をテスト repo で実行する。"""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
