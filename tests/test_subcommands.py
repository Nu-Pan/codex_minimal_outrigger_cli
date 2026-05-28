"""サブコマンド本体の決定論的な制御ロジックのテスト。"""

import ast
import inspect
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import typer
from pytest import MonkeyPatch

import sub_commands.apply.fork as apply_module
import sub_commands.apply.join as apply_join_module
import sub_commands.eval_oracles as eval_oracles_module
import sub_commands.session.abandon as session_abandon_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module
import commons.repo as repo_module
from commons.codex import COST_PERFORMANCE_MODEL
from commons.codex import COST_PERFORMANCE_REASONING_EFFORT
from commons.codex import COMMIT_MESSAGE_MODEL
from commons.codex import COMMIT_MESSAGE_REASONING_EFFORT
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.errors import format_error_report
from commons.repo import write_apply_process_id
from commons.repo import write_session_state
from commons.timing import StepTimer, start_step
from sub_commands.apply.fork import cmoc_apply_impl
from sub_commands.apply.fork import _apply_prompt
from sub_commands.apply.fork import _DISCREPANCY_OUTPUT_SCHEMA
from sub_commands.apply.fork import _commit_all_changes
from sub_commands.apply.fork import _organize_prompt
from sub_commands.apply.fork import _validate_discrepancy_payload
from sub_commands.apply.abandon import cmoc_apply_abandon_impl
from sub_commands.apply.join import cmoc_apply_join_impl
from sub_commands.eval_oracles import cmoc_eval_oracles_impl
from sub_commands.eval_oracles import _evaluation_prompt
from sub_commands.eval_oracles import _improvement_prompt
from sub_commands.init import cmoc_init_impl
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl
from sub_commands.session.join import _conflict_prompt
from sub_commands.session.join import _files_with_conflict_markers


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


def test_run_command_tees_subcommand_output_and_summary(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """共通入口はコンソールログと JSONL イベントログを出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(resolved_repo: Path) -> int:
        """正常終了するサブコマンド本体として tee 対象の進捗を出す。"""
        assert resolved_repo == repo
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "first step")
        return 2

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    log_files = list((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    log_events = [
        json.loads(line)
        for line in log_files[0].read_text(encoding="utf-8").splitlines()
    ]
    assert exit_info.value.exit_code == 2
    assert captured.err == ""
    assert len(log_files) == 1
    assert "(1/1) first step" in captured.out
    assert "sample (1/1) first step" not in captured.out
    assert "# Command completion report" in captured.out
    assert captured.out.index("# Command completion report") < captured.out.index(
        "sample step timings:"
    )
    assert "sample step timings:" in captured.out
    assert "- first step:" in captured.out
    assert "subcommand total elapsed:" in captured.out
    assert "subcommand quota wait elapsed:" in captured.out
    assert "subcommand return code: 2" in captured.out
    assert any(
        event["event"] == "step_start"
        and event["step"] == "first step"
        and event["step_index"] == "1/1"
        for event in log_events
    )
    assert any(
        event["event"] == "subcommand_end" and event["returncode"] == 2
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
    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert "(5/6, 2/3, 1/4) nested step" in captured.out
    assert any(
        event["event"] == "step_start"
        and event["step"] == "nested step"
        and event["step_index"] == "5/6, 2/3, 1/4"
        for event in log_events
    )


def test_run_command_logs_summary_on_exception(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """例外終了時も stdout へエラーレポートと終了集計を出す。"""
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
    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 1
    assert captured.err == ""
    assert "ERROR" in captured.out
    assert "RuntimeError" in captured.out
    assert "boom" in captured.out
    assert "# Command completion report" in captured.out
    assert "subcommand return code: 1" in captured.out
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert any(
        event["event"] == "step_start" and event["step"] == "failing step"
        for event in log_events
    )
    assert any(
        event["event"] == "subcommand_end" and event["returncode"] == 1
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
    assert "ERROR" in captured.out
    assert "Summary:" in captured.out
    assert "サブコマンドがエラー終了しました。" in captured.out
    assert "Next actions:" in captured.out
    assert "Detail:" in captured.out
    assert "typer.Exit(7)" in captured.out
    assert "Call stack:" in captured.out
    assert "# Command completion report" in captured.out
    assert "subcommand return code: 7" in captured.out
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert any(
        event["event"] == "subcommand_end" and event["returncode"] == 7
        for event in log_events
    )


def test_run_command_reports_repo_root_resolution_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """repo root 解決失敗も共通エラーレポートと終了集計を stdout に出す。"""
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
    assert "ERROR" in captured.out
    assert "Summary:" in captured.out
    assert "Git リポジトリのルートが見つかりませんでした。" in captured.out
    assert "Next actions:" in captured.out
    assert "Detail:" in captured.out
    assert f"開始パス: {tmp_path.resolve()}" in captured.out
    assert "Call stack:" in captured.out
    assert "# Command completion report" in captured.out
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


def test_session_fork_creates_session_branch_and_records_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc session fork` は session branch 作成と state 記録を行う。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    record_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(record_path.read_text(encoding="utf-8"))
    assert branch_name.startswith("cmoc/session/")
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] in {"main", "master"}
    assert state["session"]["session_start_commit"] == base_commit
    assert state["apply"] == {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    output = capsys.readouterr().out
    assert "(1/4) validate repository state" in output
    assert "session fork (1/4) validate repository state" not in output
    assert "create session branch attempt (1/10)" in output


def test_session_fork_repairs_missing_cmoc_ignore_before_clean_check(
    tmp_path: Path,
) -> None:
    """`.cmoc` ignore 不足は補修し、その差分を通常の未コミット差分として扱う。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert ".gitignore" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert (repo / ".gitignore").read_text(encoding="utf-8") == "/.cmoc/\n"
    assert _git(repo, "status", "--porcelain", "--", ".gitignore").stdout == (
        "?? .gitignore\n"
    )
    assert _session_state_paths(repo) == []


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
    _git(repo, "checkout", "-b", "cmoc/session/existing")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "cmoc 管理 branch" in error.value.message
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert branches.count("cmoc/session/") == 1
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
    write_session_state(
        repo,
        "existing",
        {
            "session": {
                "state": "active",
                "session_home_branch": home_branch,
                "session_start_commit": start_commit,
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
    assert error.value.detail == "existing"
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / "existing.json",
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


def test_session_fork_from_linked_worktree_records_state_in_common_root(
    tmp_path: Path,
) -> None:
    """linked worktree で作った session state も共有 root 側へ保存する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")

    cmoc_session_fork_impl(linked)

    branch_name = _git(linked, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    assert (
        repo / ".cmoc" / "sessions" / f"{session_id}.json"
    ).exists()
    assert not (
        linked / ".cmoc" / "sessions" / f"{session_id}.json"
    ).exists()


def test_session_fork_from_linked_worktree_rejects_common_active_session(
    tmp_path: Path,
) -> None:
    """active session 判定は linked worktree ごとに分離しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")
    start_commit = _git(linked, "rev-parse", "HEAD").stdout.strip()
    write_session_state(
        repo,
        "existing",
        {
            "session": {
                "state": "active",
                "session_home_branch": "feature",
                "session_start_commit": start_commit,
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
    assert error.value.detail == "existing"
    assert _git(linked, "branch", "--show-current").stdout.strip() == "feature"
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / "existing.json",
    ]


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
    session_id = "2026-05-10_22-21_10_123"
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

    maintain_calls: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review oracles 冒頭の INDEX.md メンテナンスを記録する。"""
        maintain_calls.append(repo_root)
        return False

    monkeypatch.setattr(
        eval_oracles_module,
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

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert maintain_calls == [repo]
    assert codex_kwargs[0]["expect_json"] is True
    assert codex_kwargs[0]["output_schema"] == (
        eval_oracles_module._EVALUATION_OUTPUT_SCHEMA
    )
    assert codex_kwargs[0]["skip_index_maintenance"] is True
    assert "json_validator" in codex_kwargs[0]
    assert "mode: full" in report
    assert "result: ok" in report
    assert "## Fatal issues" in report
    assert "No issues." in report
    assert "## Specification-only basis" not in report


def test_eval_oracles_writes_error_report_when_evaluation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価処理に失敗した場合も `result: error` レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価中に失敗する Codex 実行を模擬する。"""
        raise RuntimeError("fake evaluation failure")

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake evaluation failure"):
        cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert "result: error" in report
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


def test_eval_oracles_writes_error_report_when_preparation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """前処理に失敗した場合も、取得済み範囲で error レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    def fake_maintain_indexes(_repo_root: Path) -> bool:
        """INDEX.md メンテナンス中の失敗を模擬する。"""
        raise RuntimeError("fake preparation failure")

    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(RuntimeError, match="fake preparation failure"):
        cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert "result: error" in report
    assert "mode: unknown" in report
    assert "branch: null" in report
    assert "head_commit: null" in report
    assert "deleted_oracles_detected: null" in report
    assert "oracle_count_total: null" in report
    assert "oracle_count_evaluated: 0" in report
    assert "- Failed stage: `maintain INDEX.md files`" in report
    assert "| - | No completed evaluations. | - |" in report
    assert "No requested oracle files remained unevaluated." in report


def test_eval_oracles_error_report_separates_unevaluated_files(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """途中失敗時、未評価 file を issue 0 の評価済み行として表示しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_a = oracle_root / "a.md"
    oracle_b = oracle_root / "b.md"
    oracle_a.write_text("a\n", encoding="utf-8")
    oracle_b.write_text("b\n", encoding="utf-8")

    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    calls = 0

    def fake_codex(*args: object, **kwargs: object) -> str:
        """1 件目だけ成功し、2 件目の評価で失敗する。"""
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("fake second evaluation failure")
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake second evaluation failure"):
        cmoc_eval_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert "oracle_count_total: 2" in report
    assert "oracle_count_evaluated: 1" in report
    assert "## Specification-only basis" not in report
    assert "| 1 | `oracles/a.md` | 0 |" in report
    assert "| 2 | `oracles/b.md` | 0 |" not in report
    assert "Not evaluated oracle files:" in report
    assert "1. `oracles/b.md`" in report


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

    monkeypatch.setattr(
        eval_oracles_module,
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

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)
    monkeypatch.setattr(
        eval_oracles_module,
        "_write_report",
        fake_write_report,
    )

    with pytest.raises(OSError, match="fake report failure"):
        cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert "result: error" in report
    assert "oracle_count_evaluated: 1" in report
    assert "- Failed stage: `write report`" in report
    assert "- Exception type: `OSError`" in report
    assert "- Exception message: `fake report failure`" in report
    assert "成功評価ではありません" in report
    assert "今回評価した範囲では問題点が検出されませんでした" not in report
    assert "## Specification-only basis" not in report


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

    monkeypatch.setattr(
        eval_oracles_module,
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

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    for field in [
        "schema_version: 1",
        "command: cmoc review oracles",
        "generated_at:",
        f"repo_root: {repo.resolve()}",
        f"oracle_root: {oracle_root.resolve()}",
        "mode: full",
        "full_requested: true",
        "branch:",
        "is_cmoc_branch: false",
        "base_commit: null",
        "head_commit:",
        "deleted_oracles_detected: false",
        "oracle_count_total: 2",
        "oracle_count_evaluated: 2",
        "fatal_issue_count: 2",
        "warning_issue_count: 2",
        "inconclusive_issue_count: 1",
        "result: fatal",
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

    monkeypatch.setattr(
        eval_oracles_module,
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
        if "問題点リスト改善" in purpose:
            return json.dumps(
                {"issues": [issue("Improved warning")]},
                ensure_ascii=False,
            )
        return json.dumps({"issues": [issue("Raw warning")]}, ensure_ascii=False)

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True, repeat_improve_issues_list=2)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert calls == [
        "oracle 評価 oracles/spec.md",
        "oracle 問題点リスト改善 1",
        "oracle 問題点リスト改善 2",
    ]
    assert [
        kwargs["skip_index_maintenance"] for kwargs in codex_kwargs
    ] == [True, True, True]
    assert "Improved warning" in report
    assert "Raw warning" not in report


def test_review_oracles_rejects_improved_issue_for_unevaluated_oracle(
    tmp_path: Path,
) -> None:
    """改善後 issue は評価対象外 oracle へ黙って再配布しない。"""
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

    with pytest.raises(
        ValueError,
        match="oracle_path must match an evaluated oracle file",
    ):
        eval_oracles_module._validate_issues_payload(
            {"issues": [improved_issue]},
            repo,
            {evaluated_oracle.resolve()},
        )

    with pytest.raises(
        ValueError,
        match="oracle_path must match an evaluated oracle file",
    ):
        eval_oracles_module._redistribute_improved_issues(
            evaluations,
            [improved_issue],
        )


def test_eval_oracles_result_precedence() -> None:
    """result は評価対象数と severity 件数から機械的に決まる。"""
    assert eval_oracles_module._evaluation_result(
        0,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "no_targets"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 1, "inconclusive": 1, "warning": 1},
    ) == "fatal"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 1, "warning": 1},
    ) == "inconclusive"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 1},
    ) == "warning"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "ok"


def test_eval_oracles_payload_accepts_existing_oracle_and_index_paths(
    tmp_path: Path,
) -> None:
    """評価 payload は issue 単位の実在 oracle / INDEX file 参照を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")

    eval_oracles_module._validate_evaluation_payload(
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
        eval_oracles_module._validate_evaluation_payload(
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
        eval_oracles_module._validate_evaluation_payload(
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
        eval_oracles_module._validate_evaluation_payload(
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
        eval_oracles_module._validate_evaluation_payload(
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
        eval_oracles_module._validate_evaluation_payload(
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


def test_eval_oracles_payload_rejects_missing_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path も実在する oracle / INDEX file として検査する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    missing_oracle = oracle_root / "missing.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("fatal", "fatal", missing_oracle, 1, 1)

    with pytest.raises(ValueError, match="issues\\[0\\]\\.oracle_path must exist"):
        eval_oracles_module._validate_evaluation_payload(
            {
                "issues": [issue],
            },
            repo,
            oracle,
        )


def test_eval_oracles_verdict_text_distinguishes_error() -> None:
    """error や未知の result を ok 相当の Verdict にしない。"""
    ok_verdict = eval_oracles_module._verdict_text("ok")
    error_verdict = eval_oracles_module._verdict_text("error")
    unknown_verdict = eval_oracles_module._verdict_text("unexpected")

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

    evaluated_prompts: list[str] = []
    monkeypatch.setattr(
        eval_oracles_module,
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

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=False)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    report = reports[0].read_text(encoding="utf-8")
    assert len(evaluated_prompts) == 1
    assert str(changed_oracle) in evaluated_prompts[0]
    assert str(unchanged_oracle) not in evaluated_prompts[0]
    assert "mode: partial" in report
    assert "deleted_oracles_detected: true" in report
    assert "oracle_count: 1" in report


def test_eval_oracles_full_mode_reports_deleted_oracles_on_session_branch(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """session branch 上では full mode でも削除済み oracle 有無を metadata に出す。"""
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

    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """full mode の既存 oracle 評価結果を返す。"""
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert "mode: full" in report
    assert "full_requested: true" in report
    assert "is_cmoc_branch: true" in report
    assert "deleted_oracles_detected: true" in report
    assert "| 1 | `oracles/existing.md` | 0 |" in report


def test_eval_oracles_uses_full_mode_on_apply_branch(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply branch 上の `eval-oracles` は `--full` なしでも全体評価する。"""
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
        "cmoc/apply/2026-05-10_22-21_10_123/2026-05-10_22-22_10_123",
    )
    changed_oracle.write_text("after\n", encoding="utf-8")

    monkeypatch.setattr(
        eval_oracles_module,
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

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=False)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert evaluated_targets == [changed_oracle, unchanged_oracle]
    assert "mode: full" in report
    assert "full_requested: false" in report
    assert "is_cmoc_branch: true" in report
    assert "base_commit: null" in report
    assert "deleted_oracles_detected: false" in report
    assert "oracle_count: 2" in report


def test_eval_oracles_body_uses_importable_module_name() -> None:
    """`eval-oracles` の本体は通常 import 可能なモジュールに置く。"""
    repo_root = Path(__file__).resolve().parents[1]

    body = repo_root / "src" / "sub_commands" / "eval_oracles.py"
    legacy = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    body_text = body.read_text(encoding="utf-8")
    assert "def cmoc_eval_oracles_impl" in body_text
    assert "spec_from_file_location" not in body_text
    assert not legacy.exists()


def test_eval_oracles_validation_helpers_are_ordered_caller_first() -> None:
    """同一ファイル内の validation helper は caller first に並べる。"""
    repo_root = Path(__file__).resolve().parents[1]
    source = (
        repo_root / "src" / "sub_commands" / "eval_oracles.py"
    ).read_text(encoding="utf-8")

    callee = source.index("def _require_absolute_oracle_path(")
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
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt
    assert "各 issue の referenced_paths には参照した oracle / INDEX" in prompt
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
    assert "関連 oracle を選定してください。" in prompt
    assert "`/repo/oracles` 外のファイルは一切参照禁止です。" in prompt
    assert "`oracles/INDEX.md`" not in prompt
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt


def test_eval_oracles_prompt_orders_completion_before_details() -> None:
    """評価 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア仕様のレビュー担当です。"
    assert lines[1] == (
        "`/repo` 内の oracle ファイル `/repo/oracles/spec.md` を評価してください。"
    )
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "issues には検出した問題点を入れ、問題がない場合は空配列を返してください。"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert exit_code == 0
    assert len(reports) == 1
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_123/"
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
        / "apply"
        / "2026-05-10_22-21_10_123"
        / apply_run_id
    )
    assert apply_worktree.is_dir()
    assert set(state["apply"]) == {
        "state",
        "apply_branch",
        "oracle_snapshot_commit",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert report_text.startswith("---\n")
    assert "cmoc_session_id: \"2026-05-10_22-21_10_123\"" in report_text
    assert "cmoc_apply_run_id: " in report_text
    assert (
        "cmoc_session_branch: \"cmoc/session/2026-05-10_22-21_10_123\""
        in report_text
    )
    assert (
        "cmoc_apply_branch: \"cmoc/apply/2026-05-10_22-21_10_123/"
        in report_text
    )
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
        kwargs["model"] == COST_PERFORMANCE_MODEL
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs["reasoning_effort"] == COST_PERFORMANCE_REASONING_EFFORT
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    apply_run_id = state["apply"]["apply_branch"].rsplit("/", 1)[1]
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "apply"
        / "2026-05-10_22-21_10_123"
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
    assert report_kwargs[0]["skip_index_maintenance"] is True
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

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査中に session branch を進め、調査自体は収束させる。"""
        nonlocal advanced_session
        if kwargs.get("expect_json") is True:
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()
    assert "joined apply branch:" in output


def test_apply_join_cleans_worktree_created_from_linked_worktree(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """linked worktree で fork した apply run も common root 側で cleanup する。"""
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

    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    apply_branch = state["apply"]["apply_branch"]
    apply_run_id = apply_branch.rsplit("/", 1)[1]
    apply_worktree = (
        repo / ".cmoc" / "worktrees" / "apply" / session_id / apply_run_id
    )
    linked_apply_worktree = (
        linked / ".cmoc" / "worktrees" / "apply" / session_id / apply_run_id
    )
    reports = list((repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md"))
    assert exit_code == 0
    assert apply_worktree.is_dir()
    assert not linked_apply_worktree.exists()
    assert len(reports) == 1
    assert f'apply_worktree_path: "{apply_worktree}"' in reports[0].read_text(
        encoding="utf-8"
    )

    _git(linked, "switch", "feature")
    _git(repo, "switch", session_branch)
    cmoc_apply_join_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_join_keeps_artifacts_when_report_result_is_missing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """result 保存済みを確認できない場合、merge 後も apply artifacts は残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    expected_apply_branch = (
        "cmoc/apply/2026-05-10_22-21_10_123/2026-05-10_22-22_10_123"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert apply_branch in _git(repo, "branch", "--list", apply_branch).stdout
    assert apply_worktree.exists()
    assert report_path.exists()
    assert "warning: apply cleanup skipped:" in output


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    """apply worktree 内のログ用 `.cmoc` ではなく main worktree の state を読む。"""
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    assert f"{apply_branch}: oracles/spec.md" in error_info.value.detail
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    _git(apply_worktree, "add", "memo/note.md")
    _git(apply_worktree, "commit", "-m", "edit non implementation file")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert f"{apply_branch}: memo/note.md" in error_info.value.detail
    assert not (repo / "memo" / "note.md").exists()
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


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


def test_apply_join_stops_on_apply_branch_oracles_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の oracles/INDEX.md 差分は想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "oracles" / "INDEX.md").write_text(
        "index\n",
        encoding="utf-8",
    )
    _git(apply_worktree, "add", "oracles/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain oracle index")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert f"{apply_branch}: oracles/INDEX.md" in error_info.value.detail


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == "index\n"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    assert f"{session_branch}: oracles/ignored.md" in error_info.value.detail


def test_apply_join_force_resolve_keeps_expected_apply_index_diff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply branch 側の想定内 INDEX.md 差分を維持する。"""
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "INDEX.md").read_text(encoding="utf-8") == "index\n"
    assert not (repo / "memo" / "note.md").exists()
    assert state["apply"]["state"] == "ready"
    assert f"- {apply_branch}: memo/note.md" in output


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert not (repo / "INDEX.md").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert "auto-resolved INDEX.md conflicts:" in output
    assert "- INDEX.md" in output


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict" in error_info.value.message
    assert "feature.txt" in error_info.value.detail
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_apply_branch_rename_from_oracles(
    tmp_path: Path,
) -> None:
    """apply branch 側の oracle から実装側への rename は停止対象にする。"""
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

    assert "想定外の差分" in error_info.value.message
    assert f"{apply_branch}: oracles/spec.md" in error_info.value.detail
    assert not (repo / "feature.txt").exists()
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_force_resolves_apply_branch_non_implementation_diff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply branch 側の非実装ファイル変更を revert して merge する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "memo/note.md", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected memo")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "memo" / "note.md").exists()
    assert state["apply"]["state"] == "ready"
    assert f"- {apply_branch}: memo/note.md" in output


def test_apply_join_force_resolves_with_missing_apply_worktree(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply worktree 欠落時も一時 worktree で revert する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "memo/note.md", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected memo")
    _git(repo, "worktree", "remove", "--force", str(apply_worktree))

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "memo" / "note.md").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert list((repo / ".cmoc" / "worktrees" / "tmp").glob("*")) == []
    assert f"- {apply_branch}: memo/note.md" in output


def test_apply_join_force_resolves_apply_branch_copy_from_oracles(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは oracle 由来 copy entry 全体を snapshot へ戻す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert not (repo / "feature.txt").exists()
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert state["apply"]["state"] == "ready"
    assert f"- {apply_branch}: oracles/spec.md" in output


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()
    assert not (repo / "feature.txt").exists()
    assert f"abandoned apply branch: {apply_branch}" in output
    assert f"abandoned apply worktree: {apply_worktree}" in output
    assert "previous apply.state: completed" in output
    assert "current apply.state: ready" in output


def test_apply_abandon_accepts_apply_branch_worktree(
    tmp_path: Path,
) -> None:
    """apply worktree 上から実行しても main worktree の state を更新する。"""
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    """ログ用 `.cmoc` がある apply worktree からでも main worktree の state を更新する。"""
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_123", state)
    write_apply_process_id(repo, "2026-05-10_22-21_10_123", process.pid)

    try:
        cmoc_apply_abandon_impl(repo)
    finally:
        process.wait(timeout=5)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert process.returncode is not None
    assert state["apply"]["state"] == "ready"
    assert "process_id" not in state["apply"]
    assert not (
        repo / ".cmoc" / "runtime" / "apply" / "2026-05-10_22-21_10_123.pid"
    ).exists()
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_accepts_stale_running_state_without_process_id(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """古い running state に process id が無い場合も stale として cleanup する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_123", state)

    cmoc_apply_abandon_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "running apply process id was not recorded" in output
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


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
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
        if kwargs.get("expect_json") is True:
            return _discrepancy_json("f")
        return _apply_report(str(args[1]), "未収束", [1, 1])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=2)

    assert exit_code == 2
    assert (
        "実装ループ (2/2) 要修正点: 1"
        in capsys.readouterr().out
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert codex_prompts
    assert "## 作業結果\n未収束" in report_text
    assert "まだ要修正点が残っている可能性" in report_text


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
    apply_prompts: list[str] = []
    organize_results = [
        _discrepancy_json("first improvement"),
        _discrepancy_json("second improvement"),
        _discrepancy_json("second improvement"),
    ]

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査、改善、修正、レポートの呼び出しを purpose で分岐する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith("実装調査"):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
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
    assert exit_code == 2
    assert len(organize_prompts) == 3
    assert "(5/6, 1/1, 4/5, 3/3) 要修正点リスト改善" in output
    assert "(5/6, 1/1, 5/5, 1/1) 要修正点適用" in output
    assert "要修正点リスト改善ループ (3/3) 要修正点: 1" in output
    assert "second improvement" in apply_prompts[0]
    assert "initial" in organize_prompts[0]
    assert "first improvement" in organize_prompts[1]


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
        if purpose.startswith("oracle 調査") or purpose.startswith("実装調査"):
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
    assert "実装ループ (1/1) 要修正点: 0" in output
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
        if purpose.startswith("oracle 調査") or purpose.startswith("実装調査"):
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
    ) == 2

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
        if purpose.startswith("oracle 調査") or purpose.startswith("実装調査"):
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

    assert cmoc_apply_impl(repo, repeat_investigate_and_fix=1) == 2

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
        "cmoc/session/2026-05-10_22-21_10_123"
    )


def test_organize_prompt_includes_fixing_list_quality_requirements(
    tmp_path: Path,
) -> None:
    """要修正点リスト改善 prompt は oracle の品質観点を明示する。"""
    prompt = _organize_prompt(
        tmp_path,
        json.loads(_discrepancy_json("fix"))["fixing_points"],
        "cmoc/session/2026-05-10_22-21_10_123",
        "1111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222",
    )

    assert "内容の品質に明確な問題がない" in prompt
    assert "重複する要修正点は 1 件にマージ" in prompt
    assert "矛盾する修正方針は矛盾しない内容に調整" in prompt
    assert "git ブランチ `cmoc/session/2026-05-10_22-21_10_123`" in prompt
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
    assert f"`{tmp_path / 'README.md'}` は編集禁止です。" in prompt
    assert f"`{tmp_path / 'AGENTS.md'}` は編集禁止です。" in prompt


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
        "`/repo` の実装を、oracle 要求に追従するようベストエフォートで更新してください。"
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


def test_apply_rejects_incomplete_change_summary_from_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """report 失敗時も完了済み apply run を error へ戻さない。"""
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    report_dir = repo / ".cmoc" / "reports" / "apply" / "fork"
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_123/"
    )
    reports = list(report_dir.glob("*.md"))
    assert len(reports) == 1
    report_text = reports[0].read_text(encoding="utf-8")
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()
    session_head_at_finish = _git(repo, "rev-parse", "HEAD").stdout.strip()
    captured = capsys.readouterr()
    assert str(reports[0]) in captured.out
    assert "result: \"エラー\"" in report_text
    assert f"session_head_at_apply_start: \"{session_head}\"" in report_text
    assert (
        f"session_head_at_apply_finish: \"{session_head_at_finish}\""
        in report_text
    )
    assert session_head != session_head_at_finish
    assert session_head != apply_head
    assert f"session_head_at_apply_finish: \"{apply_head}\"" not in report_text
    assert "## 作業結果" in report_text
    assert "エラー" in report_text
    assert "## エラー詳細" in report_text
    assert "- Failed stage: `write report`" in report_text
    assert "- Exception type: `CmocError`" in report_text
    assert "apply report の生成に必要な変更要約が不足しています。" in report_text
    assert "## 要修正点件数の推移" in report_text
    assert "- 1 回目: 0 件" in report_text
    assert "カテゴリ: 変更ファイル一覧" in report_text
    assert "docs/INDEX.md" in report_text
    assert "Codex CLI による意味論的カテゴリ別要約には失敗しました。" in report_text


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    captured = capsys.readouterr()

    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_123/"
    )
    assert len(reports) == 1
    assert str(reports[0]) in captured.out
    report_text = reports[0].read_text(encoding="utf-8")
    assert "result: \"エラー\"" in report_text
    assert "cmoc_apply_run_id: " in report_text
    assert (
        "cmoc_apply_branch: \"cmoc/apply/2026-05-10_22-21_10_123/"
        in report_text
    )
    assert "apply_worktree_path: " in report_text
    assert "- Failed stage: `maintain INDEX.md files`" in report_text
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
    """`cmoc apply` は開始前の未コミット実装差分を拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert "app.py" in error.value.detail
    assert (repo / ".gitignore").read_text(encoding="utf-8") == "/.cmoc/\n"
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


def test_apply_rejects_tracked_cmoc_before_worktree_creation(
    tmp_path: Path,
) -> None:
    """apply fork は state 読み取り前に `.cmoc` 非追跡を保証する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert ".gitignore" in error.value.detail
    assert state_path in error.value.detail
    assert (repo / ".gitignore").read_text(encoding="utf-8") == "/.cmoc/\n"
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" not in branches


def test_apply_ensures_cmoc_ignore_before_session_state_read(
    tmp_path: Path,
) -> None:
    """ignore 保証が済む前に `.cmoc/sessions` の壊れた state を読まない。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc/session/2026-05-10_22-21_10_123")
    broken_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert ".gitignore" in error.value.detail
    assert "JSON が不正" not in error.value.message
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    apply_branch = state["apply"]["apply_branch"]
    assert "fake running write failure" in str(error.value)
    assert state["apply"]["state"] == "error"
    assert isinstance(apply_branch, str)
    assert apply_branch.startswith("cmoc/apply/2026-05-10_22-21_10_123/")
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert calls == 2


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
    ) -> tuple[str, str, Path]:
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    captured = capsys.readouterr()
    assert "fake worktree creation failure" in str(error.value)
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "error",
    }
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
        / "apply"
        / "2026-05-10_22-21_10_123"
        / apply_run_id
    )
    assert f"apply_worktree_path: \"{planned_apply_worktree}\"" in report_text
    assert f"apply_worktree_path: \"{repo}\"" not in report_text


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
                "## ブランチ cmoc/session/2026-05-10_22-21_10_123 上の全変更内容",
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
                "## ブランチ cmoc/session/2026-05-10_22-21_10_123 上の全変更内容",
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


def test_commit_all_changes_rechecks_forbidden_paths_after_index_update(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス後に禁止領域差分が出た場合は commit 前に止める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンス時に禁止領域差分を作る fake。"""
        oracle_index = repo_root / "oracles" / "INDEX.md"
        oracle_index.parent.mkdir()
        oracle_index.write_text("forbidden\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError):
        _commit_all_changes(repo)

    assert _git(repo, "status", "--porcelain").stdout


def test_apply_implementation_files_at_commit_excludes_root_memo(
    tmp_path: Path,
) -> None:
    """apply の実装調査対象は read-only 禁止領域の root memo を含めない。"""
    repo = _init_repo(tmp_path)
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
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

    assert "memo/note.md" not in relative_paths
    assert relative_paths == ["README.md", "app.py", "docs/memo/note.md"]


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
    assert implementation_paths == [".gitignore", "README.md", "kept.py"]


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


def test_apply_partial_targets_include_deleted_and_reverted_paths(
    tmp_path: Path,
) -> None:
    """部分 apply は削除済みと存在する履歴変更 path を対象にする。"""
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

    assert oracle_targets == {
        "oracles/obsolete.md": True,
        "oracles/spec.md": False,
    }
    assert implementation_targets == {
        "app.py": False,
        "obsolete.py": True,
    }


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


def test_apply_deleted_investigation_target_prompt_mentions_history(
    tmp_path: Path,
) -> None:
    """削除済み調査起点は存在しない path として履歴確認を促す。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "deleted.py",
        deleted_at_snapshot=True,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "deleted.py") + "` を起点" in prompt
    assert "oracle snapshot 時点では存在しません" in prompt
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


@pytest.mark.parametrize("forbidden_file", ["README.md", "AGENTS.md"])
def test_commit_all_changes_rejects_root_readme_and_agents_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    forbidden_file: str,
) -> None:
    """root README/AGENTS は workspace-write の編集禁止 path として検出する。"""
    repo = _init_repo(tmp_path)
    (repo / forbidden_file).write_text("tampered\n", encoding="utf-8")
    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert forbidden_file in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == target_branch
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert state["session"]["state"] == "joined"
    assert "cmoc/session/2026-05-10_22-21_10_123" not in branches


def test_session_join_ensures_cmoc_ignored_before_switch(
    tmp_path: Path,
) -> None:
    """tracked `.cmoc` state を補修し、発生差分を検出して switch 前に止める。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    status = _git(repo, "status", "--porcelain").stdout
    assert "未コミットの変更" in error.value.message
    assert ".gitignore" in error.value.detail
    assert state_path in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert ".gitignore" in status
    assert state_path in status
    assert home_branch in _git(repo, "branch", "--format=%(refname:short)").stdout


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
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        "cmoc/apply/2026-05-10_22-21_10_123/2026-05-10_22-22_10_123"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "merge conflict は検出されませんでした" in error.value.message
    assert "fatal: refusing to merge unrelated histories" in error.value.detail
    assert "手動解消が必要です" in captured.err
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert session_branch in branches


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
        (repo_root / "README.md").write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict 対象外" in error.value.message
    assert "README.md" in error.value.detail
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert captured_allowed_paths == ["oracles/spec.md"]
    assert state["session"]["state"] == "joined"
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == (
        "resolved oracle\n"
    )


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["session"]["state"] == "joined"
    assert (repo / "literal_markers.txt").read_text(encoding="utf-8").startswith(
        "<<<<<<< sample\n"
    )


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

    assert "禁止領域" in error.value.message
    assert ".agents/note.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "abandoned"
    assert state["session"].get("joined_at") is None
    assert "cmoc/session/2026-05-10_22-21_10_123" not in branches
    assert (repo / "feature.txt").exists() is False
    assert (
        "abandoned session branch: cmoc/session/2026-05-10_22-21_10_123"
        in captured.out
    )


def test_session_abandon_ensures_cmoc_ignored_before_cleanup(
    tmp_path: Path,
) -> None:
    """tracked `.cmoc` state を補修し、発生差分を検出して cleanup 前に止める。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    status = _git(repo, "status", "--porcelain").stdout
    assert "未コミットの変更" in error.value.message
    assert ".gitignore" in error.value.detail
    assert state_path in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert ".gitignore" in status
    assert state_path in status


def test_session_abandon_rejects_apply_run_before_cleanup(
    tmp_path: Path,
) -> None:
    """apply run が ready でなければ branch/state を変更しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        "cmoc/apply/2026-05-10_22-21_10_123/2026-05-10_22-22_10_123"
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
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert state_after["session"]["state"] == "active"
    assert "cmoc/session/2026-05-10_22-21_10_123" in branches


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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    assert "未コミットの変更" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
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
    session_branch = "cmoc/session/2026-05-10_22-21_10_123"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
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


def test_session_abandon_reports_rollback_switch_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """cleanup 後の branch 復旧失敗は再実行可能状態として隠さない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_123"
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "rollback にも失敗" in error.value.message
    assert "cleanup failure" in error.value.detail
    assert "fake branch delete failure" in error.value.detail
    assert "rollback failure" in error.value.detail
    assert "fake switch failure" in error.value.detail
    assert "再実行は避けてください" in error.value.actions[1]
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_abandon_restores_branch_when_state_restore_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """state 復旧失敗時も session branch への復旧 switch は試行する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_123"
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
        """abandoned 保存は通し、active への rollback 保存だけ失敗させる。"""
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
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "rollback にも失敗" in error.value.message
    assert "cleanup failure" in error.value.detail
    assert "fake branch delete failure" in error.value.detail
    assert "rollback failure: state restore failed" in error.value.detail
    assert "fake state restore failure" in error.value.detail
    assert "再実行は避けてください" in error.value.actions[1]
    assert restore_switches == [["switch", session_branch]]
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert state["session"]["state"] == "abandoned"
    assert session_branch in branches


def test_main_typer_functions_delegate_only_to_impls() -> None:
    """Typer 対応関数は共通 runner ではなく対応する impl 呼び出しだけを持つ。"""
    import main

    source = inspect.getsource(main)
    eval_oracles_source = inspect.getsource(main.eval_oracles_command)

    assert "def _run_command" not in source
    assert "_run_command(" not in source
    assert "cmoc_init_impl()" in source
    assert "cmoc_session_fork_impl()" in source
    assert "importlib.util" not in source
    assert "spec_from_file_location" not in source
    assert "from sub_commands.eval_oracles import cmoc_eval_oracles_impl" in source
    assert "eval-oracles.py" not in source
    assert "eval_oracles_source" not in eval_oracles_source
    assert "cmoc_eval_oracles_impl(" in source
    assert "repeat_improve_issues_list=repeat_improve_issues_list" in source
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
    assert "--repeat-improve-issu" in review.stdout
    assert "Usage: cmoc eval-oracles [OPTIONS]" in plural_alias.stdout
    assert "Usage: cmoc eval-oracle [OPTIONS]" in singular.stdout
    assert review.stderr == ""
    assert plural_alias.stderr == ""
    assert singular.stderr == ""


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

    assert "--repeat-investigate-and-fix" in result.stdout
    assert "--repeat-improove-fixing-list" in result.stdout
    assert "--full" in result.stdout


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
    assert "ERROR" in result.stdout
    assert "Summary:" in result.stdout


def test_main_reports_no_args_error_with_non_empty_detail() -> None:
    """引数なし起動も詳細説明を含む共通エラーレポートにする。"""
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
    assert "ERROR" in result.stdout
    assert "Summary:\nコマンドが指定されていません。" in result.stdout
    assert "Next actions:" in result.stdout
    assert "- 利用可能なコマンドを確認するには `cmoc --help` を実行してください。" in result.stdout
    assert "Detail:\ncmoc がサブコマンドなしで起動されました。" in result.stdout
    assert "Call stack:" in result.stdout


def test_format_error_report_fills_empty_generic_detail() -> None:
    """通常例外の文字列表現が空でも Detail を空欄にしない。"""
    error = Exception()

    report = format_error_report(error)

    assert "Summary:\nException" in report
    assert (
        "- 入力値が誤っている場合は、コマンド引数を修正してから cmoc を再実行してください。"
        in report
    )
    assert (
        "- リポジトリ状態が原因の場合は、Detail と Call stack を確認して作業ツリーや設定を修正してください。"
        in report
    )
    assert "Detail:\nbuiltins.Exception がメッセージなしで発生しました。" in report
    assert "Call stack:" in report


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
    """ランチャーは system python3 へフォールバックしない。"""
    repo_root = Path(__file__).resolve().parents[1]
    launcher = (repo_root / "bin" / "cmoc").read_text(encoding="utf-8")

    assert launcher.startswith("#!/bin/sh")
    assert "#!/usr/bin/env python3" not in launcher
    assert 'exec "$venv_python"' in launcher
    assert "} >&2" not in launcher


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
    assert "ERROR" in result.stdout
    assert "Summary:" in result.stdout
    assert "Next actions:" in result.stdout
    assert "Detail:" in result.stdout
    assert "Call stack:" in result.stdout
    assert "仮想環境 Python" in result.stdout
    assert "at print_missing_venv_error" in result.stdout
    assert "at require_venv_python" in result.stdout
    assert "at main" in result.stdout
    assert "仮想環境 Python の実行可能性チェック" not in result.stdout


def test_session_join_conflict_prompt_allows_marker_only_oracle_fix() -> None:
    """conflict 対象 oracle file は marker 解消に限って編集できる。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["app.py", "oracles/spec.md"])

    assert "`/repo/oracles` は編集禁止です。" not in prompt
    assert "['/repo/app.py', '/repo/oracles/spec.md']" in prompt
    assert "['app.py" not in prompt
    assert "conflict marker 解消に限って編集できます" in prompt
    assert "意味的な仕様改訂" in prompt
    assert "conflict 対象外 oracle file の編集は禁止" in prompt
    assert "解決内容と未解決ファイルの有無を報告" in prompt


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
    session_id = "2026-05-10_22-21_10_123"
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


def _repo_with_session_join_conflict(tmp_path: Path) -> Path:
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
    (repo / "auto.txt").write_text("session auto\n", encoding="utf-8")
    _git(repo, "add", "conflict.txt", "auto.txt")
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
    session_id = "2026-05-10_22-21_10_123"
    apply_branch = f"cmoc/apply/{session_id}/2026-05-10_22-22_10_123"
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "apply"
        / session_id
        / "2026-05-10_22-22_10_123"
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
