"""サブコマンド本体の決定論的な制御ロジックのテスト。"""

import ast
import inspect
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
import typer
from pytest import MonkeyPatch

import sub_commands.session_abandon as session_abandon_module
import sub_commands.session_fork as session_fork_module
from commons.codex import COST_PERFORMANCE_MODEL
from commons.codex import COST_PERFORMANCE_REASONING_EFFORT
from commons.codex import COMMIT_MESSAGE_MODEL
from commons.codex import COMMIT_MESSAGE_REASONING_EFFORT
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.errors import format_error_report
from commons.repo import write_session_state
from commons.timing import StepTimer, start_step
from sub_commands.apply import cmoc_apply_impl
from sub_commands.apply import _apply_prompt
from sub_commands.apply import _DISCREPANCY_OUTPUT_SCHEMA
from sub_commands.apply import _commit_all_changes
from sub_commands.apply import _organize_prompt
from sub_commands.apply import _validate_discrepancy_payload
from sub_commands.apply_abandon import cmoc_apply_abandon_impl
from sub_commands.apply_join import cmoc_apply_join_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.session_abandon import cmoc_session_abandon_impl
from sub_commands.session_fork import cmoc_session_fork_impl
from sub_commands.session_join import cmoc_session_join_impl
from sub_commands.session_join import _conflict_prompt
from sub_commands.session_join import _files_with_conflict_markers


def _load_eval_oracles_module() -> ModuleType:
    """ハイフン付きファイル名の eval-oracles 本体モジュールを読む。"""
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    spec = importlib.util.spec_from_file_location(
        "sub_commands.eval-oracles",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load subcommand module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


eval_oracles_module = _load_eval_oracles_module()
cmoc_eval_oracles_impl = eval_oracles_module.cmoc_eval_oracles_impl
_evaluation_prompt = eval_oracles_module._evaluation_prompt


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


def test_run_command_tees_subcommand_output_and_summary(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """共通入口はサブコマンド呼び出しログを stdout とファイルへ tee する。"""
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
    log_files = list((repo / ".cmoc" / "logs" / "sub_commands").glob("*.log"))
    log_content = log_files[0].read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 2
    assert captured.err == ""
    assert len(log_files) == 1
    assert "(1/1) first step" in captured.out
    assert "sample (1/1) first step" not in captured.out
    assert "(1/1) first step" in log_content
    assert "sample (1/1) first step" not in log_content
    assert "== Command completion report ==" in captured.out
    assert "== Command completion report ==" in log_content
    assert log_content.index("== Command completion report ==") < log_content.index(
        "sample step timings:"
    )
    assert "sample step timings:" in log_content
    assert "- first step:" in log_content
    assert "subcommand total elapsed:" in log_content
    assert "subcommand quota wait elapsed:" in log_content
    assert "subcommand return code: 2" in log_content
    assert "/.cmoc/logs/" in (repo / ".git" / "info" / "exclude").read_text(
        encoding="utf-8"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_run_command_logs_summary_on_exception(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """例外終了時も可能な範囲の経過時間と戻り値をログに残す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> None:
        """例外終了するサブコマンド本体として途中進捗を出す。"""
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "failing step")
        raise RuntimeError("boom")

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.log")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 1
    assert "ERROR" in log_content
    assert "boom" in log_content
    assert "(1/1) failing step" in log_content
    assert "sample (1/1) failing step" not in log_content
    assert "== Command completion report ==" in log_content
    assert log_content.index("== Command completion report ==") < log_content.index(
        "sample step timings:"
    )
    assert "sample step timings:" in log_content
    assert "- failing step:" in log_content
    assert "subcommand return code: 1" in log_content


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
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.log")
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
    assert "== Command completion report ==" in captured.out
    assert "subcommand return code: 7" in captured.out
    assert "ERROR" in log_content
    assert "typer.Exit(7)" in log_content
    assert "== Command completion report ==" in log_content
    assert "subcommand return code: 7" in log_content


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


def test_session_fork_rejects_uninitialized_cmoc_without_side_effects(
    tmp_path: Path,
) -> None:
    """`cmoc init` 未実行なら `.gitignore` を補修せずに停止する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert ".cmoc" in error.value.message
    assert "cmoc init" in "\n".join(error.value.actions)
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert _session_state_paths(repo) == []


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


def test_eval_oracles_writes_report_with_fake_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc eval-oracles --full` は oracle 評価レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """不整合なしの oracle 評価結果を返す Codex 実行を模擬する。"""
        codex_kwargs.append(kwargs)
        return json.dumps(
            {
                "target_oracle_path": str((oracle_root / "spec.md").resolve()),
                "referenced_paths": [
                    str((oracle_root / "spec.md").resolve()),
                ],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert codex_kwargs[0]["expect_json"] is True
    assert codex_kwargs[0]["output_schema"] == (
        eval_oracles_module._EVALUATION_OUTPUT_SCHEMA
    )
    assert "json_validator" in codex_kwargs[0]
    assert "mode: full" in report
    assert "result: ok" in report
    assert "## Fatal issues" in report
    assert "No issues." in report
    assert "## Specification-only basis" in report
    assert (
        "| 1 | `oracles/spec.md` | oracles 配下の仕様だけを参照しました。 |"
        in report
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

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert "result: error" in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 0" in report
    assert "- Failed stage: `evaluate oracle files`" in report
    assert "- Exception type: `RuntimeError`" in report
    assert "- Exception message: `fake evaluation failure`" in report
    assert "# cmoc eval-oracles report" in report
    assert "## Summary" in report
    assert "## Verdict" in report
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

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
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
            {
                "target_oracle_path": str(oracle_a.resolve()),
                "referenced_paths": [str(oracle_a.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake second evaluation failure"):
        cmoc_eval_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert "oracle_count_total: 2" in report
    assert "oracle_count_evaluated: 1" in report
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
            {
                "target_oracle_path": str(oracle_file.resolve()),
                "referenced_paths": [str(oracle_file.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
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

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert "result: error" in report
    assert "oracle_count_evaluated: 1" in report
    assert "- Failed stage: `write report`" in report
    assert "- Exception type: `OSError`" in report
    assert "- Exception message: `fake report failure`" in report
    assert "成功評価ではありません" in report
    assert "今回評価した範囲では問題点が検出されませんでした" not in report
    assert "## Specification-only basis" in report
    assert (
        "| 1 | `oracles/spec.md` | oracles 配下の仕様だけを参照しました。 |"
        in report
    )


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
                    "target_oracle_path": str(oracle_a.resolve()),
                    "referenced_paths": [
                        str(oracle_a.resolve()),
                        str(oracle_index.resolve()),
                        str(oracle_a.resolve()),
                    ],
                    "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                    "issues": [
                        _eval_oracle_issue(
                            "warning",
                            "A warning",
                            oracle_a,
                            3,
                            4,
                        ),
                        _eval_oracle_issue(
                            "fatal",
                            "A fatal",
                            oracle_a,
                            5,
                            5,
                        ),
                    ],
                },
                ensure_ascii=False,
            )
        return json.dumps(
            {
                "target_oracle_path": str(oracle_b.resolve()),
                "referenced_paths": [
                    str(oracle_b.resolve()),
                    str(oracle_index.resolve()),
                ],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [
                    _eval_oracle_issue(
                        "inconclusive",
                        "B inconclusive",
                        oracle_b,
                        None,
                        None,
                    ),
                    _eval_oracle_issue(
                        "fatal",
                        "B fatal",
                        oracle_b,
                        8,
                        9,
                    ),
                    _eval_oracle_issue(
                        "warning",
                        "B warning",
                        oracle_b,
                        10,
                        10,
                    ),
                ],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    for field in [
        "schema_version: 1",
        "command: cmoc eval-oracles",
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
        "# cmoc eval-oracles report",
        "## Summary",
        "## Verdict",
        "## Evaluated oracle files",
        "## Fatal issues",
        "## Inconclusive issues",
        "## Warnings",
        "## Referenced files",
        "## Specification-only basis",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
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
    assert "| No. | Referenced file |" in report
    assert "| No. | Oracle file | Specification-only basis |" in report
    assert (
        "| 1 | `oracles/a.md` | oracles 配下の仕様だけを参照しました。 |"
        in report
    )
    assert (
        "| 2 | `oracles/b.md` | oracles 配下の仕様だけを参照しました。 |"
        in report
    )
    assert "| 1 | `oracles/a.md` |" in report
    assert "| 2 | `oracles/INDEX.md` |" in report
    assert "| 3 | `oracles/b.md` |" in report
    assert report.count("| 2 | `oracles/INDEX.md` |") == 1


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
            {
                "target_oracle_path": str(changed_oracle.resolve()),
                "referenced_paths": [str(changed_oracle.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=False)

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
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
            {
                "target_oracle_path": str(existing_oracle.resolve()),
                "referenced_paths": [str(existing_oracle.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert "mode: full" in report
    assert "full_requested: true" in report
    assert "is_cmoc_branch: true" in report
    assert "deleted_oracles_detected: true" in report
    assert "| 1 | `oracles/existing.md` | 0 |" in report


def test_eval_oracles_body_uses_subcommand_file_name() -> None:
    """`eval-oracles` の本体はサブコマンド名と同じファイル名に置く。"""
    repo_root = Path(__file__).resolve().parents[1]

    body = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    legacy = repo_root / "src" / "sub_commands" / "eval_oracles.py"
    body_text = body.read_text(encoding="utf-8")
    assert "def cmoc_eval_oracles_impl" in body_text
    assert "spec_from_file_location" not in body_text
    assert not legacy.exists()


def test_eval_oracles_validation_helpers_are_ordered_caller_first() -> None:
    """同一ファイル内の validation helper は caller first に並べる。"""
    repo_root = Path(__file__).resolve().parents[1]
    source = (
        repo_root / "src" / "sub_commands" / "eval-oracles.py"
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
    assert "referenced_paths には参照した oracle / INDEX ファイルの絶対パス" in prompt
    assert "Structured Output schema に一致する JSON" in prompt
    assert "仕様だけから判断・実装したとき" in prompt


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
        "target_oracle_path には評価対象 oracle ファイルの絶対パスを返してください。"
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

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )
    codex_kwargs: list[dict[str, object]] = []
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        codex_kwargs.append(kwargs)
        codex_prompts.append(str(args[1]))
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return _apply_report(str(args[1]), "収束", [0])

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

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
        if str(kwargs.get("purpose", "")).startswith("investigate ")
    ]
    investigation_purposes = [
        str(kwargs.get("purpose", "")) for kwargs in investigation_kwargs
    ]
    assert investigation_kwargs
    assert any(
        purpose.startswith("investigate oracle ")
        for purpose in investigation_purposes
    )
    assert any(
        purpose.startswith("investigate implementation ")
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
        if kwargs.get("purpose") == "write apply report"
    ]
    assert len(report_kwargs) == 1
    assert report_kwargs[0]["model"] == COST_PERFORMANCE_MODEL
    assert (
        report_kwargs[0]["reasoning_effort"]
        == COST_PERFORMANCE_REASONING_EFFORT
    )
    assert "作業結果区分: 収束" in codex_prompts[-1]
    assert "今回の apply run で行った変更内容" in codex_prompts[-1]
    assert (
        "この `cmoc apply fork` が実際に行った作業内容だけ"
        in codex_prompts[-1]
    )
    assert (
        "今回の自動適用処理以前の作業も含めてください"
        not in codex_prompts[-1]
    )
    assert "変更内容の意味論に基づき" in codex_prompts[-1]
    assert "「カテゴリ」という語" in codex_prompts[-1]


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
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """常に不整合を返し、指定回数で incomplete になることを見やすくする。"""
        codex_prompts.append(str(args[1]))
        if kwargs.get("expect_json") is True:
            return _discrepancy_json("f")
        return _apply_report(str(args[1]), "未収束", [1, 1])

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=2)

    assert exit_code == 2
    assert (
        "implementation loop (2/2) discrepancies: 1"
        in capsys.readouterr().out
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert "作業結果区分: 未収束" in codex_prompts[-1]
    assert "まだ要修正点が残っている可能性" in codex_prompts[-1]
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
        "sub_commands.apply.maintain_indexes",
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
        if purpose.startswith("investigate"):
            return _discrepancy_json("initial")
        if purpose == "organize discrepancies":
            organize_prompts.append(str(args[1]))
            return organize_results.pop(0)
        if purpose.startswith("apply discrepancy"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "write apply report":
            return _apply_report(str(args[1]), "未収束", [1])
        return ""

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=3,
    )

    output = capsys.readouterr().out
    assert exit_code == 2
    assert len(organize_prompts) == 3
    assert "fixing list improvement loop (3/3) discrepancies: 1" in output
    assert "second improvement" in apply_prompts[0]
    assert "initial" in organize_prompts[0]
    assert "first improvement" in organize_prompts[1]


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
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )
    apply_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は null の hash を返し、修正依頼 prompt を記録する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("investigate"):
            return _discrepancy_json("fill hash")
        if purpose.startswith("apply discrepancy"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "write apply report":
            return _apply_report(str(args[1]), "未収束", [2])
        return ""

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

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
        "sub_commands.apply.maintain_indexes",
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
        if purpose.startswith("investigate"):
            return two_discrepancies_json
        if purpose == "organize discrepancies":
            return two_discrepancies_json
        if purpose.startswith("apply discrepancy"):
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
        if purpose == "generate commit message":
            commit_message_count += 1
            commit_message_options.append(
                (
                    kwargs.get("model"),
                    kwargs.get("reasoning_effort"),
                )
            )
            return f"Apply fix {commit_message_count}"
        if purpose == "write apply report":
            return _apply_report(str(args[1]), "未収束", [2])
        return ""

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

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


def test_apply_rejects_incomplete_report_from_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """必須内容を欠く apply レポートは保存せずエラーにする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は収束、レポートは必須項目不足にする。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "収束\ncomplete report"

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_123.json"
        ).read_text(encoding="utf-8")
    )
    report_dir = repo / ".cmoc" / "reports" / "apply" / "fork"
    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_123/"
    )
    assert not report_dir.exists() or list(report_dir.glob("*.md")) == []


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


def test_apply_rejects_tracked_cmoc_before_worktree_creation(
    tmp_path: Path,
) -> None:
    """apply fork は worktree 作成前に `.cmoc` 非追跡を副作用なしで検証する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert ".cmoc" in error.value.message
    assert state_path in error.value.detail
    assert not (repo / ".gitignore").exists()
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == f"{state_path}\n"
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" not in branches


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
        "sub_commands.apply.maintain_indexes",
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

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

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
        "sub_commands.apply.maintain_indexes",
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

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

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
        "sub_commands.apply.maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError):
        _commit_all_changes(repo)

    assert _git(repo, "status", "--porcelain").stdout


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


def test_session_join_rejects_tracked_cmoc_without_side_effects(
    tmp_path: Path,
) -> None:
    """未初期化の tracked `.cmoc` state は補修せず merge 前に止める。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert ".cmoc" in error.value.message
    assert state_path in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == f"{state_path}\n"
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
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert "apply run" in error.value.message
    assert "手動解消が必要です" not in captured.err


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


def test_session_abandon_rejects_tracked_cmoc_without_side_effects(
    tmp_path: Path,
) -> None:
    """tracked `.cmoc` state は補修せず cleanup 前に止める。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    assert ".cmoc" in error.value.message
    assert state_path in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_123"
    )
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == f"{state_path}\n"


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
    state["apply"]["state"] = "active"
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


def test_main_typer_functions_delegate_only_to_impls() -> None:
    """Typer 対応関数は共通 runner ではなく対応する impl 呼び出しだけを持つ。"""
    import main

    source = inspect.getsource(main)
    eval_oracles_source = inspect.getsource(main.eval_oracles_command)

    assert "def _run_command" not in source
    assert "_run_command(" not in source
    assert "cmoc_init_impl()" in source
    assert "cmoc_session_fork_impl()" in source
    assert (
        '"sub_commands.eval-oracles"'
        in source
    )
    assert "from sub_commands.eval_oracles" not in eval_oracles_source
    assert '"eval-oracles.py"' in source
    assert "cmoc_eval_oracles_impl(full=full)" in source
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
    assert "eval-oracles" in result.stdout
    assert re.search(r"\bbranch\b", result.stdout) is None
    assert re.search(r"\bmerge\b", result.stdout) is None
    assert re.search(r"\beval-oracle(?!s)\b", result.stdout) is None


def test_cmoc_eval_oracles_command_and_compat_alias_are_registered() -> None:
    """`eval-oracles` を正名にし、既存の `eval-oracle` も alias として残す。"""
    repo_root = Path(__file__).resolve().parents[1]
    env = {"PYTHONPATH": str(repo_root / "src")}
    plural = subprocess.run(
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
    assert plural.returncode == 0
    assert singular.returncode == 0
    assert "Usage: cmoc eval-oracles [OPTIONS]" in plural.stdout
    assert "Usage: cmoc eval-oracle [OPTIONS]" in singular.stdout
    assert plural.stderr == ""
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


def test_user_facing_error_text_does_not_keep_known_english_phrases() -> None:
    """共通エラーレポートに渡す説明・次アクションを日本語方針で固定する。"""
    repo_root = Path(__file__).resolve().parents[1]
    target_paths = [
        repo_root / "src" / "commons" / "errors.py",
        repo_root / "src" / "commons" / "repo.py",
        repo_root / "src" / "sub_commands" / "apply.py",
        repo_root / "src" / "sub_commands" / "session_abandon.py",
        repo_root / "src" / "sub_commands" / "session_join.py",
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


def test_files_with_conflict_markers_checks_all_tracked_files(
    tmp_path: Path,
) -> None:
    """marker 検査は渡された対象一覧に限定せず git 管理対象全体を見る。"""
    repo = _init_repo(tmp_path)
    conflicted = repo / "conflicted.txt"
    unrelated = repo / "unrelated.txt"
    conflicted.write_text("resolved\n", encoding="utf-8")
    unrelated.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )
    _git(repo, "add", "conflicted.txt", "unrelated.txt")
    _git(repo, "commit", "-m", "add tracked files")

    assert _files_with_conflict_markers(repo, ["conflicted.txt"]) == [
        "unrelated.txt"
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
            "カテゴリ: 実装修正",
        ]
    )


def _eval_oracle_issue(
    severity: str,
    title: str,
    oracle_path: Path,
    line_start: int | None,
    line_end: int | None,
) -> dict[str, object]:
    """テスト用の valid な eval-oracles issue item を返す。"""
    return {
        "severity": severity,
        "title": title,
        "oracle_path": str(oracle_path.resolve()),
        "oracle_line_start": line_start,
        "oracle_line_end": line_end,
        "affected_workflow": "cmoc eval-oracles",
        "requirement": f"{title} requirement",
        "problem": f"{title} problem",
        "reason": f"{title} reason",
        "suggested_oracle_change": f"{title} change",
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
    report_path.write_text("report\n", encoding="utf-8")
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
