"""doctor preprocess の共有 lifecycle を外部挙動から検証する統合テスト。

doctor preprocess は `.cmoc/gu`、`.agents`、config、refactor state を同じ
repository/worktree 前提で修復し、必要な差分を commit する。このファイルは
CLI と直接呼び出しの両方で、その lifecycle と pre-existing Git index の保持を
一続きの文脈で確認する。

lock・CLI/config・Git index はテスト観点としては分かれるが、各ケース
が同じ `make_repo`、linked worktree、共有 doctor lock、preprocess の副作用を
前提にする。ファイルを分割すると、これらの fixture と lifecycle の説明を
複数のモジュールで重複して読む必要があり、局所的な読解量が増えるため、
責務を doctor preprocess の外部契約に限定して一つに保つ。

正本仕様:
- `{{work-root}}/spec/app_spec/doctor_preprocess.md`
- `{{work-root}}/spec/app_spec/oracle_and_realization_file_enumeration.md`
- `{{work-root}}/spec/app_spec/sub_command/doctor.md`
- `{{work-root}}/spec/app_spec/sub_command/realization_refactor.md`
- `{{work-root}}/reference/src/oracle/other/cmoc_config.py`
"""

import json
import multiprocessing
import shutil
import signal
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner, seed_search_config, terminal_primary_report
from _command_support import write_python_executable
from _git_support import init_repo, make_repo, run_git

import commons.runtime_cli as cli_module
import commons.runtime_doctor as doctor_module
from commons.runtime_config import config_to_dict
from commons.runtime_document_search import DocumentSearch, SearchError
from commons.runtime_document_search_types import SEARCH_MATERIALS
from commons.runtime_errors import CmocError
from commons.runtime_feedback import (
    ReporterAvailabilityError,
    start_feedback_invocation,
    validate_feedback_reporter_availability,
)
from commons.runtime_paths import ensure_work_directories
from commons.runtime_refactor import RefactorState
from config.cmoc_config import CmocConfig
from main import app

# TCP collector の起動・protocol 検査は初回修復 test と test_feedback.py に残す。
# Git・配置先・索引のケースでは、既存 fixture で transport の準備と終了待ちを省く。
# 永続採番は test_runtime_ids.py、logger との結合は test_runtime_cli.py に残す。
# doctor では実ログと report の対応を保ち、採番 DB の準備・同期書き込みを省く。
pytestmark = pytest.mark.usefixtures(
    "feedback_without_transport", "nonpersistent_execution_ids"
)

_WORK_DIRECTORIES = ("spec", "reference/src", "reference/test", "src", "test")


@pytest.fixture(scope="module")
def _initial_repository_seed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """修復前の追跡 file と初期履歴を一度だけ作る。"""
    return make_repo(tmp_path_factory.mktemp("doctor-initial-seed"))


@pytest.fixture
def initial_repository(tmp_path: Path, _initial_repository_seed: Path) -> Path:
    """修復・index 検査に同じ初期履歴を渡し、変更可能な状態は独立させる。"""
    # init・add・commit は共有し、修復・競合・index の変更は各ケースで実行する。
    # hardlink や linked worktree を使わず、設定・index・refs も独立して複製する。
    return shutil.copytree(_initial_repository_seed, tmp_path / "repo")


@pytest.fixture(scope="module")
def _repair_paths_repository_seed(
    tmp_path_factory: pytest.TempPathFactory, _empty_repository_seed: Path
) -> Path:
    """先行差分の判定に使う通常 file と履歴を一度だけ用意する。"""
    # 設定の意味検証は行わず、Git の差分・競合 entry を調べる前提だけを共有する。
    root = shutil.copytree(
        _empty_repository_seed,
        tmp_path_factory.mktemp("doctor-repair-paths-seed") / "repo",
    )
    (root / "README.md").write_text("# repo\n")
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    paths = (doctor_module.config_path(root), doctor_module.refactor_state_path(root))
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n")
    run_git(
        root,
        "add",
        "-f",
        "README.md",
        ".gitignore",
        *(str(p.relative_to(root)) for p in paths),
    )
    run_git(root, "commit", "-m", "track repair targets")
    return root


@pytest.fixture
def repair_paths_repository(
    tmp_path: Path, _repair_paths_repository_seed: Path
) -> Path:
    """差分のない初期内容を複製し、各ケースの index・refs・設定を独立させる。"""
    return shutil.copytree(_repair_paths_repository_seed, tmp_path / "repo")


@pytest.fixture(scope="module")
def _managed_repository_seed(
    tmp_path_factory: pytest.TempPathFactory, _empty_repository_seed: Path
) -> Path:
    """既存管理物の列挙・設定保存・初期 commit を一度だけ用意する。"""
    # 初回修復と索引同期は専用ケースに残し、既存ファイルへの操作は各テストで行う。
    root = shutil.copytree(
        _empty_repository_seed,
        tmp_path_factory.mktemp("doctor-managed-seed") / "repo",
    )
    for relative in _WORK_DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    (root / ".agents").mkdir()
    (root / ".agents/.gitkeep").write_text("")
    seed_search_config(root)
    doctor_module.sync_refactor_state(root)
    run_git(root, "add", ".gitignore", ".agents", ".cmoc/gt")
    run_git(root, "commit", "-m", "prepare management files")
    return root


@pytest.fixture
def managed_repository(tmp_path: Path, _managed_repository_seed: Path) -> Path:
    """修復済みの管理物と独立した Git index・refs・設定を各テストへ渡す。"""
    # hardlink や linked worktree を使わず、中断・修復時の変更を他ケースへ持ち越さない。
    return shutil.copytree(_managed_repository_seed, tmp_path / "repo")


@pytest.fixture
def doctor_repair_events(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """配置先の検査と同じ前処理で、修復順序と毎回の reporter 検査も観測する。"""
    # 順序だけのために repository と doctor の全処理を重ねない。
    events: list[str] = []
    original_ignore = doctor_module.ensure_cmoc_ignored
    original_agents = doctor_module._ensure_agents_tracked
    original_config = doctor_module.sync_config
    original_state = doctor_module.sync_refactor_state

    def observe_ignore(path: Path) -> None:
        assert all((path / relative).is_dir() for relative in _WORK_DIRECTORIES)
        events.append("ignore")
        original_ignore(path)

    def observe_agents(path: Path) -> bool:
        events.append("agents")
        return original_agents(path)

    def observe_config(path: Path, **kwargs):
        events.append("config")
        return original_config(path, **kwargs)

    def observe_state(path: Path, *, sync_entries: bool = True) -> RefactorState:
        events.append("state")
        return original_state(path, sync_entries=sync_entries)

    def observe_reporter() -> None:
        events.append("reporter")

    monkeypatch.setattr(doctor_module, "ensure_cmoc_ignored", observe_ignore)
    monkeypatch.setattr(doctor_module, "_ensure_agents_tracked", observe_agents)
    monkeypatch.setattr(doctor_module, "sync_config", observe_config)
    monkeypatch.setattr(doctor_module, "sync_refactor_state", observe_state)
    monkeypatch.setattr(
        doctor_module, "validate_feedback_reporter_availability", observe_reporter
    )
    return events


def test_refactor_preprocess_interruption_preserves_user_changes(
    managed_repository, monkeypatch
):
    """前処理中の停止は未確定修復だけを戻し、既存の index・作業差分を保持する。"""
    root = managed_repository
    monkeypatch.chdir(root)
    ignore = root / ".gitignore"
    ignore.write_text(ignore.read_text() + "# staged by user\n")
    run_git(root, "add", ".gitignore")
    ignore.write_text(ignore.read_text() + "# unstaged by user\n")
    (root / ".agents/.gitkeep").unlink()
    for relative in ("reference/test", "src", "test"):
        (root / relative).rmdir()
    before = run_git(root, "diff", "--binary").stdout
    staged = run_git(root, "diff", "--cached", "--binary").stdout
    head = run_git(root, "rev-parse", "HEAD").stdout

    def interrupt_sync(*_args):
        signal.raise_signal(signal.SIGINT)

    monkeypatch.setattr(
        doctor_module, "_synchronize_document_search_index", interrupt_sync
    )
    result = runner.invoke(app, ["realization", "refactor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert run_git(root, "rev-parse", "HEAD").stdout == head
    assert run_git(root, "diff", "--binary").stdout == before
    assert run_git(root, "diff", "--cached", "--binary").stdout == staged
    assert all(
        not (root / relative).exists() for relative in ("reference/test", "src", "test")
    )
    report = terminal_primary_report(result).read_text()
    assert 'completion_reason: "user_interruption"' in report
    assert "run not established" in report
    assert "cmoc run join" not in result.output


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_refactor_preprocess_interruption_keeps_committed_repairs(
    cli_repository, monkeypatch
):
    """短い確定区間中の SIGINT は commit と index 復元を一体として完了する。"""
    # 検査する refactor 対象の commit で HEAD を用意し、準備だけの初期 commit を省く。
    root = cli_repository
    monkeypatch.chdir(root)
    # 設定と既存 state だけを用意し、state 更新の修復 commit は前処理に任せる。
    seed_search_config(root)
    doctor_module.sync_refactor_state(root)
    (root / "src").mkdir()
    (root / "src/new.py").write_text("VALUE = 1\n")
    run_git(root, "add", "src/new.py", ".cmoc/gt")
    run_git(root, "commit", "-m", "add refactor target")
    head = run_git(root, "rev-parse", "HEAD").stdout
    commit = doctor_module._commit_doctor_repairs

    def commit_then_interrupt(*args, **kwargs):
        commit(*args, **kwargs)
        signal.raise_signal(signal.SIGINT)

    monkeypatch.setattr(doctor_module, "_commit_doctor_repairs", commit_then_interrupt)
    result = runner.invoke(app, ["realization", "refactor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert run_git(root, "rev-parse", "HEAD").stdout != head
    assert run_git(root, "status", "--short").stdout == ""
    assert run_git(root, "ls-files", ".cmoc/gt/config.json").stdout.strip()
    assert run_git(
        root, "ls-files", ".cmoc/gt/realization/refactor/state.json"
    ).stdout.strip()
    assert "src/new.py" in json.loads(
        doctor_module.refactor_state_path(root).read_text()
    )
    assert "run not established" in terminal_primary_report(result).read_text()


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_refactor_preprocess_stop_restores_pending_linked_worktree_index(
    managed_repository, tmp_path, monkeypatch
):
    """main の修復確定後に停止しても、後続 worktree の準備中 index を戻す。"""
    root = managed_repository
    # linked 側は管理 file を checkout で受け取り、準備用 doctor を重ねない。
    (root / "README.md").write_text("# repo\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "track user change target")
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "linked-refactor", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    (root / ".gitignore").write_text("")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "require main ignore repair")
    (root / "README.md").write_text("staged by user\n")
    run_git(root, "add", "README.md")
    (root / "README.md").write_text("unstaged by user\n")
    run_git(linked, "rm", ".agents/.gitkeep")
    before = {
        worktree: (
            run_git(worktree, "diff", "--binary").stdout,
            run_git(worktree, "diff", "--cached", "--binary").stdout,
        )
        for worktree in (root, linked)
    }
    head = run_git(root, "rev-parse", "HEAD").stdout
    commit = doctor_module._commit_doctor_repairs

    def interrupt_after_main_commit(*args, **kwargs):
        assert args[0] == root
        commit(*args, **kwargs)
        signal.raise_signal(signal.SIGINT)

    monkeypatch.setattr(
        doctor_module, "_commit_doctor_repairs", interrupt_after_main_commit
    )
    result = runner.invoke(app, ["realization", "refactor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert run_git(root, "rev-parse", "HEAD").stdout != head
    for worktree, (unstaged, staged) in before.items():
        assert run_git(worktree, "diff", "--binary").stdout == unstaged
        assert run_git(worktree, "diff", "--cached", "--binary").stdout == staged
    assert not (linked / ".agents/.gitkeep").exists()
    assert "run not established" in terminal_primary_report(result).read_text()


def _new_subcommand_events(root: Path, previous: set[Path]) -> list[dict[str, object]]:
    """直前の CLI 呼び出しが保存した 1 本の診断ログを読む。"""
    log_dir = root / ".cmoc/gu/log/sub_command"
    [log_path] = set(log_dir.glob("*.jsonl")) - previous
    return [json.loads(line) for line in log_path.read_text().splitlines()]


def _hold_doctor_lock(lock_path: Path, ready: Connection, release: Connection) -> None:
    """別プロセスで共有 doctor lock を保持し、解放通知まで待機する。"""

    import fcntl

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        ready.send(True)
        release.recv()
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def test_doctor_preprocess_repairs_git_state(
    initial_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が共通修復と既定 config の生成・追跡・報告を完了する。"""

    root = initial_repository
    config_path = root / ".cmoc" / "gt" / "config.json"

    # 公開 doctor と実 collector の結合を、この初回修復ケースで一度検証する。
    monkeypatch.setattr(
        cli_module, "start_feedback_invocation", start_feedback_invocation
    )
    monkeypatch.setattr(
        doctor_module,
        "validate_feedback_reporter_availability",
        validate_feedback_reporter_availability,
    )
    monkeypatch.chdir(root)
    result = run_doctor(root)

    assert "feedback reporter unavailable" not in result.output
    assert not any(
        event["event"] == "feedback.reporter_unavailable"
        for event in _new_subcommand_events(root, set())
    )
    report = terminal_primary_report(result)
    assert report.parent == root / ".cmoc" / "gu" / "report" / "doctor"
    rendered_report = report.read_text(encoding="utf-8")
    assert 'terminal_classification: "natural_completion"' in rendered_report
    assert "exit_code: 0" in rendered_report
    assert "doctor preprocess" in rendered_report
    assert "## 検索索引の同期" in rendered_report
    assert "対象 work-root" in rendered_report
    assert "逐次反映と再利用" in rendered_report
    assert "診断用サブコマンドログ" in rendered_report
    assert str(config_path) in rendered_report
    assert "document_search.chunk_tokens: `512`" in rendered_report
    assert "- 検証: `成功`" in rendered_report
    assert "- 保存: `True`" in rendered_report

    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert run_git(root, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    agents_gitkeep = root / ".agents" / ".gitkeep"
    assert agents_gitkeep.is_file()
    assert agents_gitkeep.read_text() == ""
    repair_commit_paths = run_git(
        root, "show", "--name-only", "--format=", "HEAD"
    ).stdout.splitlines()
    assert ".gitignore" in repair_commit_paths
    assert ".agents/.gitkeep" in repair_commit_paths
    assert ".cmoc/gt/config.json" in repair_commit_paths
    assert ".cmoc/gt/realization/refactor/state.json" in repair_commit_paths
    assert config_path.is_file()
    assert run_git(root, "ls-files", "--", ".cmoc/gt/config.json").stdout.strip() == (
        ".cmoc/gt/config.json"
    )
    config = json.loads(config_path.read_text())
    assert config["codex"]["num_try_falv_recovery"] == 1
    assert config["codex"]["model_providers"] == {"openai": {"settings": {}}}
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout.strip() == ""
    assert (
        run_git(
            root,
            "check-ignore",
            "-q",
            ".cmoc/gu/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            ["git", "check-ignore", "--no-index", "-q", ".cmoc/gt/config.json"],
            cwd=root,
            check=False,
        ).returncode
        == 1
    )
    state_path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    state = json.loads(state_path.read_text())
    assert set(state) == {".gitignore", "README.md", "oracle/spec.md"}
    assert all(
        entry
        == {
            "last_investigated_at": None,
        }
        for entry in state.values()
    )
    assert all((root / relative).is_dir() for relative in _WORK_DIRECTORIES)
    assert all(not list((root / relative).iterdir()) for relative in _WORK_DIRECTORIES)


@pytest.mark.parametrize("explicit_doctor", [False, True])
@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preprocess_restores_empty_work_directories(
    cli_repository, explicit_doctor, doctor_repair_events
):
    """両入口で配置先と placeholder を復元し、再実行で既存内容・差分を保つ。"""
    # 修復済みの管理 file だけ用意し、配置先を作るための doctor 全体を重ねない。
    # 初期内容を最初の commit に揃え、参照しない空 commit を準備しない。
    root = cli_repository
    preserved = root / "src/kept.txt"
    preserved.parent.mkdir()
    preserved.write_text("kept content\n")
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    (root / ".agents").mkdir()
    gitkeep = root / ".agents/.gitkeep"
    gitkeep.write_text("")
    seed_search_config(root)
    doctor_module.sync_refactor_state(root)
    run_git(root, "add", ".gitignore", ".agents", ".cmoc/gt", "src")
    run_git(root, "commit", "-m", "prepare management files and kept content")
    head_before = run_git(root, "rev-parse", "HEAD").stdout
    preserved_before = (preserved.stat().st_ino, preserved.stat().st_mtime_ns)
    # placeholder 復元と index flag の保持も、この両入口の lifecycle で検査する。
    run_git(root, "update-index", "--skip-worktree", ".agents/.gitkeep")
    gitkeep.unlink()

    # 準備用の state 同期を除き、各前処理だけの順序を観測する。
    doctor_repair_events.clear()
    doctor_module.run_doctor_preprocess(root, explicit_doctor=explicit_doctor)

    expected_order = ["ignore", "agents", "config", "state", "reporter"]
    assert doctor_repair_events == expected_order
    assert gitkeep.read_text() == ""
    assert all((root / relative).is_dir() for relative in _WORK_DIRECTORIES)
    assert all(
        not list((root / relative).iterdir())
        for relative in _WORK_DIRECTORIES
        if relative != "src"
    )
    assert preserved.read_text() == "kept content\n"
    assert (preserved.stat().st_ino, preserved.stat().st_mtime_ns) == preserved_before
    directory_states = {
        relative: (
            (root / relative).stat().st_ino,
            (root / relative).stat().st_mtime_ns,
        )
        for relative in _WORK_DIRECTORIES
    }

    doctor_repair_events.clear()
    doctor_module.run_doctor_preprocess(root, explicit_doctor=explicit_doctor)

    assert doctor_repair_events == expected_order
    assert directory_states == {
        relative: (
            (root / relative).stat().st_ino,
            (root / relative).stat().st_mtime_ns,
        )
        for relative in _WORK_DIRECTORIES
    }
    assert run_git(root, "rev-parse", "HEAD").stdout == head_before
    assert run_git(root, "status", "--short").stdout == ""
    assert run_git(root, "ls-files", "-v", ".agents/.gitkeep").stdout == (
        "S .agents/.gitkeep\n"
    )
    assert run_git(root, "ls-files", "--", *_WORK_DIRECTORIES).stdout.splitlines() == [
        "src/kept.txt"
    ]


@pytest.mark.parametrize("relative", ["oracle", *_WORK_DIRECTORIES])
def test_work_directory_collisions_preserve_content_and_report_target(
    tmp_path, relative
):
    """全配置先と親の衝突を保持し、失敗した配置先と修復方法を診断する。"""
    # 配置先別の境界は共通 helper で検査し、Git・CLI の準備を重ねない。
    root = tmp_path
    collision = root / relative
    collision.parent.mkdir(parents=True, exist_ok=True)
    collision.write_text("keep collision\n")

    with pytest.raises(CmocError) as exc_info:
        ensure_work_directories(root)

    assert collision.read_text() == "keep collision\n"
    assert "作業用配置先" in exc_info.value.summary
    assert f"work-root: {root}" in exc_info.value.detail
    assert (
        f"path: {root / ('spec' if relative == 'oracle' else relative)}"
        in exc_info.value.detail
    )
    assert "reason:" in exc_info.value.detail
    assert "退避" in exc_info.value.next_actions[0]


def test_work_directory_validation_does_not_repair_missing_paths(tmp_path):
    """最終検証で失われた配置先を発見し、検証だけの呼び出しでは補完しない。"""
    ensure_work_directories(tmp_path)
    missing = tmp_path / "reference/test"
    missing.rmdir()

    with pytest.raises(CmocError) as exc_info:
        ensure_work_directories(tmp_path, create_missing=False)

    assert not missing.exists()
    assert f"work-root: {tmp_path}" in exc_info.value.detail
    assert f"path: {missing}" in exc_info.value.detail


@pytest.mark.parametrize("command", [("doctor",), ("session", "fork")])
def test_preprocess_rejects_work_directory_collisions(
    committed_repository, monkeypatch, command
):
    """通常起動と明示 doctor は衝突を診断して終了し、Git 状態を変更しない。"""
    # 全配置先の拒否は helper のケースに残し、両入口との結合だけを実 Git で確かめる。
    root = committed_repository
    collision = root / "reference/test"
    collision.parent.mkdir(parents=True)
    collision.write_text("keep collision\n")
    head_before = run_git(root, "rev-parse", "HEAD").stdout
    branch_before = run_git(root, "branch", "--show-current").stdout
    monkeypatch.chdir(root)

    result = runner.invoke(app, list(command), catch_exceptions=False)

    assert result.exit_code == 1
    assert collision.read_text() == "keep collision\n"
    assert run_git(root, "rev-parse", "HEAD").stdout == head_before
    assert run_git(root, "branch", "--show-current").stdout == branch_before
    report = terminal_primary_report(result).read_text()
    assert "作業用配置先" in report
    assert f"work-root: {root}" in report
    assert f"path: {collision}" in report
    assert "reason:" in report
    assert "退避" in report


def test_preprocess_reports_work_directory_permission_failure(
    cli_repository, monkeypatch
):
    """作成できない配置先を具体的に診断し、必須条件の失敗を伝える。"""
    # 作成失敗は index 修復より前に発生するため、Git root だけを用意する。
    root = cli_repository
    blocked = root / "reference/test"
    original_mkdir = Path.mkdir

    def deny_target(path, *args, **kwargs):
        if path == blocked:
            raise PermissionError("directory creation denied")
        return original_mkdir(path, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", deny_target)
    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)

    assert not blocked.exists()
    assert f"work-root: {root}" in exc_info.value.detail
    assert f"path: {blocked}" in exc_info.value.detail
    assert "directory creation denied" in exc_info.value.detail
    assert "権限" in exc_info.value.next_actions[0]


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_rechecks_work_directories_after_repair_commit(
    committed_repository, tmp_path, monkeypatch
):
    """修復 commit の hook が配置先をファイルに替えた場合、正常終了しない。"""
    root = committed_repository
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    hook = hooks / "pre-commit"
    hook.write_text(
        "#!/bin/sh\nset -eu\nrmdir reference/test\n"
        "printf 'late collision\\n' > reference/test\n"
    )
    hook.chmod(0o755)
    run_git(root, "config", "core.hooksPath", str(hooks))
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code == 1
    assert (root / "reference/test").read_text() == "late collision\n"
    report = terminal_primary_report(result).read_text()
    assert "作業用配置先" in report
    assert f"work-root: {root}" in report
    assert f"path: {root / 'reference/test'}" in report


def test_doctor_sync_preserves_user_changes_and_correlates_logs_and_reports(
    cli_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """設定を保持し、初回・編集・無変更・削除の索引同期と報告を確認する。"""
    # HEAD の文書だけを参照するため、初期内容を一つの commit に揃える。
    root = cli_repository
    # 設定保持も同じ CLI 起動で確認し、専用 repository と doctor 起動を重ねない。
    expected_config = config_to_dict(CmocConfig())
    expected_config["num_parallel"] = 3
    expected_config["codex"]["model_providers"]["custom"] = {"settings": {}}
    expected_config["codex"]["num_try_falv_recovery"] = 4
    expected_config["codex"]["agent_calls"]["build_tui_request"] = {
        "model_provider": "custom",
        "model": "CUSTOM",
        "reasoning_effort": "CUSTOM-EFFORT",
    }
    incomplete_config = dict(expected_config)
    incomplete_config.pop("document_search")
    config_path = root / ".cmoc/gt/config.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(incomplete_config) + "\n")

    document = root / "spec/source.md"
    document.parent.mkdir(parents=True)
    original = "# original document\n"
    updated = "# updated document\n"
    document.write_text(original)
    run_git(root, "add", "spec/source.md")
    run_git(root, "commit", "-m", "add search document")
    monkeypatch.chdir(root)
    log_dir = root / ".cmoc/gu/log/sub_command"

    for contents, expected, edit in (
        (original, ("updated", 1, 1, 1, 0), None),
        (updated, ("updated", 1, 1, 1, 0), lambda: document.write_text(updated)),
        (updated, ("unchanged", 1, 0, 0, 1), None),
        (None, ("updated", 0, 1, 0, 0), document.unlink),
    ):
        if edit is not None:
            edit()
        previous = set(log_dir.glob("*.jsonl"))
        result = run_doctor(root)
        # 初回の補完と再利用のいずれでも、明示値と残りの既定 call を保つ。
        saved_config = json.loads(config_path.read_text())
        assert saved_config == expected_config
        assert "model" not in saved_config["codex"]
        assert "reasoning_effort" not in saved_config["codex"]
        assert "apply_fork" not in saved_config

        events = _new_subcommand_events(root, previous)
        starts = [e for e in events if e["event"] == "document_search_sync_started"]
        finishes = [e for e in events if e["event"] == "document_search_sync_finished"]
        assert len(starts) == len(finishes) == 1
        start, finish = starts[0], finishes[0]
        assert events.index(start) < events.index(finish) < len(events) - 1
        assert start["sync_id"] == finish["sync_id"]
        assert start["execution_id"] == finish["execution_id"]
        assert start["command"] == finish["command"] == "doctor"
        assert start["work_root"] == finish["work_root"] == str(root)
        assert start["index_identity"] is None
        assert isinstance(finish["index_identity"], str)
        assert finish["counts_complete"] is True
        assert (
            finish["status"],
            finish["document_count"],
            finish["changed_document_count"],
            finish["persisted_chunk_count"],
            finish["reused_chunk_count"],
        ) == expected
        assert 0 <= finish["lock_wait_seconds"] <= finish["elapsed_seconds"]
        report = terminal_primary_report(result).read_text()
        assert f"診断ログ内の同期 ID: `{start['sync_id']}`" in report
        assert f'doctor_sync_status: "{expected[0]}"' in report
        assert run_git(root, "show", "HEAD:spec/source.md").stdout == original
        state = json.loads(
            (root / ".cmoc/gt/realization/refactor/state.json").read_text()
        )
        if contents is None:
            assert '"deleted": 1' in report
            assert not document.exists()
            assert "spec/source.md" not in state
        else:
            if edit is not None:
                assert '"changed": 1' in report
            assert document.read_text() == contents
            assert "spec/source.md" in state


@pytest.mark.parametrize("object_format", ["sha1", "sha256"])
def test_runtime_staging_reuses_unchanged_blobs_and_preserves_index_metadata(
    tmp_path, monkeypatch, object_format
):
    """同じ blob の再登録を省き、更新時も mode と保存対象外の entry を保つ。"""
    monkeypatch.setenv("GIT_DEFAULT_HASH", object_format)
    # hash 形式の設定後に初期化し、検査対象の config commit だけで HEAD を作る。
    root = tmp_path / "repo"
    root.mkdir()
    init_repo(root)
    assert (
        run_git(root, "rev-parse", "--show-object-format").stdout.strip()
        == object_format
    )
    config = doctor_module.config_path(root)
    state = doctor_module.refactor_state_path(root)
    original = '{"label": "共通"}\n'
    for path in (config, state):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(original)
    config_relative = str(config.relative_to(root))
    state_relative = str(state.relative_to(root))
    # HEAD と現在 index の mode を区別し、state は HEAD にない新規 file にする。
    run_git(root, "add", "-f", config_relative)
    run_git(root, "update-index", "--chmod=+x", config_relative)
    run_git(root, "commit", "-m", "track executable config")
    run_git(root, "update-index", "--chmod=-x", config_relative)
    run_git(root, "add", "-f", state_relative)
    run_git(root, "update-index", "--skip-worktree", state_relative)

    git_calls = 0
    original_run = doctor_module.subprocess.run

    def count_git_calls(argv, *args, **kwargs):
        nonlocal git_calls
        if argv[0] == "git":
            git_calls += 1
        return original_run(argv, *args, **kwargs)

    index_path = doctor_module._copy_current_index(root)
    try:
        before = index_path.read_bytes()
        with monkeypatch.context() as observed:
            observed.setattr(doctor_module.subprocess, "run", count_git_calls)
            doctor_module._stage_tracked_runtime_repair(
                root, index_path, include_gu_ignore=True
            )
        # 無変更の runtime と未追跡の管理領域は一度の列挙で足り、rm は不要。
        assert git_calls <= 1
        assert index_path.read_bytes() == before

        changed = '{"label": "変更"}\r\n'
        config.write_bytes(changed.encode("utf-8"))
        state.write_text("preserved staged entry\n")
        doctor_module._stage_tracked_runtime_repair(
            root, index_path, skip_paths={state_relative}
        )
        staged_config = doctor_module._run_git_with_index(
            ["show", f":{config_relative}"], root, index_path
        ).stdout
        staged_state = doctor_module._run_git_with_index(
            ["show", f":{state_relative}"], root, index_path
        ).stdout
        assert staged_config == changed.replace("\r\n", "\n")
        assert staged_state == original
        entries = doctor_module._run_git_with_index(
            ["ls-files", "--stage", "-v", "--", ".cmoc/gt"], root, index_path
        ).stdout.splitlines()
        assert any(line.startswith("H 100644 ") for line in entries)
        assert any(line.startswith("S 100644 ") for line in entries)

        # entry がない場合も同じ repository を使い、HEAD の mode と新規 mode を確かめる。
        doctor_module._run_git_with_index(
            ["update-index", "--force-remove", config_relative, state_relative],
            root,
            index_path,
        )
        git_calls = 0

        with monkeypatch.context() as observed:
            observed.setattr(doctor_module.subprocess, "run", count_git_calls)
            doctor_module._stage_tracked_runtime_repair(root, index_path)

        assert doctor_module._run_git_with_index(
            ["show", f":{config_relative}"], root, index_path
        ).stdout == changed.replace("\r\n", "\n")
        assert (
            doctor_module._run_git_with_index(
                ["show", f":{state_relative}"], root, index_path
            ).stdout
            == "preserved staged entry\n"
        )
        entries = doctor_module._run_git_with_index(
            ["ls-files", "--stage", "--", ".cmoc/gt"], root, index_path
        ).stdout.splitlines()
        assert {line.split("\t")[1]: line.split()[0] for line in entries} == {
            config_relative: "100755",
            state_relative: "100644",
        }
        # 欠落判定と HEAD mode は一括照会し、両 runtime の登録も一度に行う。
        assert git_calls <= 5

        # 既存の実行可能 entry を再更新するケースでも mode の保持を検査する。
        config.write_text(original)
        doctor_module._stage_tracked_runtime_repair(
            root, index_path, skip_paths={state_relative}
        )
        entry = doctor_module._run_git_with_index(
            ["ls-files", "--stage", "--", config_relative], root, index_path
        ).stdout
        assert entry.startswith("100755 ")
        assert (
            doctor_module._run_git_with_index(
                ["show", f":{config_relative}"], root, index_path
            ).stdout
            == original
        )

        # 別 root の修復では config/state を読まず、指定 index の管理物だけを外す。
        local = root / ".cmoc/gu/kept\tcache\n.bin"
        local.parent.mkdir(parents=True)
        local.write_bytes(b"\0kept cache\xff")
        doctor_module._run_git_with_index(
            ["add", "-f", "--", str(local.relative_to(root))], root, index_path
        )
        config.unlink()
        state.unlink()
        git_calls = 0
        with monkeypatch.context() as observed:
            observed.setattr(doctor_module.subprocess, "run", count_git_calls)
            doctor_module._stage_tracked_runtime_repair(
                root, index_path, include_config=False, include_gu_ignore=True
            )
        assert git_calls <= 2
        assert local.read_bytes() == b"\0kept cache\xff"
        assert not doctor_module._run_git_with_index(
            ["ls-files", "--", ".cmoc/gu"], root, index_path
        ).stdout
    finally:
        index_path.unlink(missing_ok=True)


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_rechecks_git_ignore_configuration_after_commit_hook(
    committed_repository, tmp_path
):
    """hook が excludesFile を変えても、最終検証は新しい ignore source を検査する。"""
    # hook の実行に必要な HEAD だけ用意し、無関係な追跡 file の準備を省く。
    root = committed_repository
    invalid_source = tmp_path / "ignore-directory"
    invalid_source.mkdir()
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    command = ["git", "config", "core.excludesFile", str(invalid_source)]
    write_python_executable(
        hooks / "post-commit",
        ["import subprocess", f"subprocess.run({command!r}, check=True)"],
    )
    run_git(root, "config", "core.hooksPath", str(hooks))

    with pytest.raises(CmocError) as caught:
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert str(invalid_source) in caught.value.detail
    assert run_git(root, "config", "core.excludesFile").stdout.strip() == str(
        invalid_source
    )


# reporter の分岐に索引の生成・永続化は不要。実同期から reporter までの結合は
# test_doctor_preprocess_repairs_git_state と同期結果・report の検査に残す。
@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preprocess_continues_with_degraded_reporter(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """reporter 利用不能を warning と event に留めて本命処理を続ける。"""
    # reporter の扱いは履歴内容を使わないため、空の HEAD だけ用意する。
    root = committed_repository

    def unavailable() -> None:
        """reporter の利用不能を再現する。"""
        raise ReporterAvailabilityError(
            "reporter", "missing", "feedback reporter cannot be started"
        )

    monkeypatch.setattr(
        doctor_module,
        "validate_feedback_reporter_availability",
        unavailable,
    )

    result = run_doctor(root)

    assert result.exit_code == 0
    assert "warning: feedback reporter unavailable (missing)" in result.stdout
    log_paths = list((root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl"))
    events = [
        json.loads(line) for path in log_paths for line in path.read_text().splitlines()
    ]
    assert any(
        event.get("event") == "feedback.reporter_unavailable"
        and event.get("component") == "reporter"
        and event.get("failure_code") == "missing"
        for event in events
    )
    assert run_git(root, "ls-files", "--", ".cmoc/gt/config.json").stdout.strip()
    assert run_git(
        root,
        "ls-files",
        "--",
        ".cmoc/gt/realization/refactor/state.json",
    ).stdout.strip()


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preprocess_propagates_interrupt_during_reporter_probe(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """reporter 事前検証中のユーザー中断を degraded warning に変換しない。"""
    root = committed_repository

    def interrupt() -> None:
        """reporter 検証中の Ctrl+C を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        doctor_module,
        "validate_feedback_reporter_availability",
        interrupt,
    )

    with pytest.raises(KeyboardInterrupt):
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preprocess_propagates_unexpected_reporter_probe_error(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """予期しない reporter 検証エラーを利用不能 warning に変換しない。"""
    root = committed_repository

    def fail_probe() -> None:
        """reporter 検証内部の予期しない失敗を再現する。"""
        raise RuntimeError("unexpected reporter probe failure")

    monkeypatch.setattr(
        doctor_module,
        "validate_feedback_reporter_availability",
        fail_probe,
    )

    with pytest.raises(RuntimeError, match="unexpected reporter probe failure"):
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)


def test_doctor_preprocess_waits_for_common_repository_lock(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree と repository で共有する doctor lock の解放待ちを検証する。"""

    # linked worktree に必要な HEAD だけ用意し、追跡 file の準備を省く。
    root = committed_repository
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-doctor-lock"
    run_git(root, "worktree", "add", "-b", "linked-doctor-lock", str(linked), "HEAD")
    lock_path = doctor_module.doctor_lock_path(root)
    assert doctor_module.doctor_lock_path(linked) == lock_path

    ready_parent, ready_child = multiprocessing.Pipe(duplex=False)
    release_child, release_parent = multiprocessing.Pipe(duplex=False)
    process = multiprocessing.Process(
        target=_hold_doctor_lock,
        args=(lock_path, ready_child, release_child),
    )
    lock_contended = threading.Event()
    original_flock = doctor_module.fcntl.flock

    def observe_lock_attempt(fd: int, operation: int) -> None:
        """実 lock の競合を確認してから、元の blocking 操作へ戻す。"""

        if operation & doctor_module.fcntl.LOCK_EX:
            try:
                original_flock(fd, operation | doctor_module.fcntl.LOCK_NB)
            except BlockingIOError:
                lock_contended.set()
            else:
                return
        original_flock(fd, operation)

    class _RepairBoundaryReached(Exception):
        pass

    def stop_before_repairs(checked_root: Path) -> None:
        # 修復・索引同期・commit は専用 test に残し、最初の修復境界で停止する。
        assert checked_root == linked.resolve()
        with lock_path.open("a+") as lock_file:
            with pytest.raises(BlockingIOError):
                original_flock(
                    lock_file.fileno(),
                    doctor_module.fcntl.LOCK_EX | doctor_module.fcntl.LOCK_NB,
                )
        raise _RepairBoundaryReached()

    process.start()
    released = False
    try:
        assert ready_parent.poll(timeout=3)
        assert ready_parent.recv() is True
        monkeypatch.setattr(doctor_module.fcntl, "flock", observe_lock_attempt)
        monkeypatch.setattr(
            doctor_module, "ensure_work_directories", stop_before_repairs
        )
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                doctor_module.run_doctor_preprocess,
                linked,
                explicit_doctor=True,
            )
            try:
                assert lock_contended.wait(timeout=3)
                assert not future.done()
            finally:
                # assertion が失敗しても、executor の終了待ちより先に holder を解放する。
                release_parent.send(True)
                released = True
            with pytest.raises(_RepairBoundaryReached):
                future.result(timeout=3)
    finally:
        if process.is_alive() and not released:
            release_parent.send(True)
        process.join(timeout=3)
        if process.is_alive():
            process.terminate()
            process.join()

    # 前処理の異常終了後も、同じ実 lock を取得できることを確認する。
    with lock_path.open("a+") as lock_file:
        original_flock(
            lock_file.fileno(),
            doctor_module.fcntl.LOCK_EX | doctor_module.fcntl.LOCK_NB,
        )


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_restores_preexisting_index_when_repair_fails(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor の修復失敗時も、呼び出し前の staged index を保持する。"""
    # 検査対象の staged file で実 index を作り、参照しない初期 file は追跡しない。
    root = committed_repository
    staged_file = root / "staged.txt"
    staged_file.write_text("staged\n")
    run_git(root, "add", "staged.txt")
    expected_index_tree = run_git(root, "write-tree").stdout.strip()

    def fail_commit(
        _root: Path,
        _agents_gitkeep_added: bool,
        *,
        include_config: bool,
        include_gu_ignore: bool,
        preserved_paths: set[str],
    ) -> None:
        """repair commit の失敗を再現する。"""
        del include_config, include_gu_ignore, preserved_paths
        raise RuntimeError("repair commit failure")

    monkeypatch.setattr(doctor_module, "_commit_doctor_repairs_from_head", fail_commit)

    with pytest.raises(RuntimeError, match="repair commit failure"):
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "write-tree").stdout.strip() == expected_index_tree
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "staged.txt"
    ]


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preserves_preexisting_unmerged_index(
    initial_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が既存の unmerged index を検査・解消せず保持する。"""

    root = initial_repository
    base_branch = run_git(root, "branch", "--show-current").stdout.strip()
    run_git(root, "checkout", "-b", "doctor-conflict-side")
    (root / "README.md").write_text("# side\n")
    run_git(root, "commit", "-am", "side change")
    run_git(root, "checkout", base_branch)
    (root / "README.md").write_text("# main\n")
    run_git(root, "commit", "-am", "main change")
    merge = subprocess.run(
        ["git", "merge", "doctor-conflict-side"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert merge.returncode != 0
    assert run_git(root, "ls-files", "--unmerged", "--", "README.md").stdout

    monkeypatch.chdir(root)
    run_doctor(root)

    assert run_git(root, "ls-files", "--unmerged", "--", "README.md").stdout


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_repairs_missing_index_without_dropping_tracked_files(
    initial_repository: Path,
) -> None:
    """欠落した Git index を復元し、既存の tracked file を保持する。"""

    root = initial_repository
    (root / ".git" / "index").unlink()

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    tracked = set(run_git(root, "ls-files").stdout.splitlines())
    assert {"README.md", "oracle/spec.md"} <= tracked
    assert run_git(root, "status", "--short").stdout == ""


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preserves_preexisting_index_flags_and_intent_to_add(
    initial_repository: Path,
) -> None:
    """doctor が二種類の index flag と intent-to-add をそれぞれ保持する。"""

    # 同じ index の退避・復元を検査するため、各状態を別 file に置き修復を一度にする。
    root = initial_repository
    flagged_paths = {
        "README.md": "--assume-unchanged",
        "oracle/spec.md": "--skip-worktree",
    }
    for relative, flag in flagged_paths.items():
        run_git(root, "update-index", flag, relative)
    before_flags = run_git(root, "ls-files", "-v", "--", *flagged_paths).stdout
    path = root / "new.txt"
    path.write_text("new\n")
    run_git(root, "add", "-N", "new.txt")
    before_entry = run_git(root, "ls-files", "--stage", "new.txt").stdout
    before_status = run_git(root, "status", "--short").stdout

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "ls-files", "-v", "--", *flagged_paths).stdout == before_flags
    assert run_git(root, "ls-files", "--stage", "new.txt").stdout == before_entry
    assert run_git(root, "status", "--short").stdout == before_status


def test_normal_preprocess_rejects_unset_search_without_rewriting_config(
    committed_repository: Path,
) -> None:
    """通常起動では不足した設定を補完せず、仕事の開始前に診断する。"""
    # 不正設定で停止するため、index 退避に必要な HEAD だけを用意する。
    root = committed_repository
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = '{"num_parallel": 3, "document_search": null}\n'
    path.write_text(original)

    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)

    assert str(path) in exc_info.value.detail
    assert "document_search" in exc_info.value.detail
    assert "手動" in exc_info.value.next_actions[0]
    assert path.read_text() == original


def test_doctor_rejects_null_search_without_filling_or_saving(
    committed_repository, monkeypatch
):
    root = committed_repository
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = '{"document_search": null}\n'
    path.write_text(original)
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code == 1, result.output
    assert "document_search" in result.output
    assert path.read_text() == original
    assert "- 保存: `False`" in terminal_primary_report(result).read_text()


def test_doctor_reports_unsaved_inconsistent_search_candidate(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補完候補が衝突した場合、doctor report に値と非保存を残す。"""
    root = committed_repository
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = '{"document_search": {"embedding_context_tokens": 256}}\n'
    path.write_text(original)
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code != 0
    report = terminal_primary_report(result).read_text()
    assert str(path) in report
    assert "document_search.chunk_tokens: `512`" in report
    assert "embedding_context_tokens=256" in report
    assert "- 保存: `False`" in report
    assert path.read_text() == original


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_generates_config_under_broad_cmoc_ignore(
    cli_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """広い `.cmoc/` ignore があっても生成 config を追跡可能に修復することを検証する。"""

    # ignore 規則を最初の commit に含め、準備だけの空 commit を作らない。
    root = cli_repository
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore cmoc working data")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert (
        run_git(root, "ls-files", "--", ".cmoc/gt/config.json").stdout.strip()
        == ".cmoc/gt/config.json"
    )
    check_ignore = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", ".cmoc/gt/config.json"],
        cwd=root,
        check=False,
    )
    assert check_ignore.returncode == 1


def test_preexisting_runtime_paths_use_original_index(repair_paths_repository):
    """対象の先行差分だけを元 index から選び、未追跡・staged deletion を除く。"""
    root = repair_paths_repository
    readme = root / "README.md"
    config = doctor_module.config_path(root)
    state = doctor_module.refactor_state_path(root)
    paths = [str(path.relative_to(root)) for path in (config, state)]
    readme.write_text("unrelated user change\n")
    index_path = doctor_module._copy_current_index(root)
    try:
        original_index = index_path.read_bytes()
        # repository と退避を共有し、各ケースでは保存済み index と作業内容だけを戻す。
        # 現在 index は最初に変え、全ケースで退避 index からの判定を検査する。
        run_git(root, "rm", "--cached", "-f", "--ignore-unmatch", "--", *paths)
        for change in (
            "clean",
            "staged",
            "unstaged",
            "mixed",
            "reverted_worktree",
            "staged_deletion",
            "unstaged_deletion",
            "untracked",
        ):
            index_path.write_bytes(original_index)
            config.write_text("{}\n")
            state.write_text("{}\n")
            if change == "untracked":
                # HEAD の変更は最後だけ行い、未追跡と staged deletion を区別する。
                run_git(root, "commit", "-m", "leave runtime files untracked")
                doctor_module._run_git_with_index(
                    ["rm", "--cached", *paths], root, index_path
                )

            expected = set()
            if change in {"staged", "mixed", "reverted_worktree"}:
                config.write_text('{"num_parallel": 99}\n')
                doctor_module._run_git_with_index(
                    ["add", "-f", paths[0]], root, index_path
                )
                expected.add(paths[0])
            if change == "mixed":
                config.write_text('{"num_parallel": 100}\n')
            if change == "reverted_worktree":
                config.write_text("{}\n")
            if change in {"unstaged", "mixed", "staged_deletion"}:
                state.write_text('{"prior": {}}\n')
                expected.add(paths[1])
            if change == "staged_deletion":
                doctor_module._run_git_with_index(
                    ["rm", "--cached", paths[0]], root, index_path
                )
            if change == "unstaged_deletion":
                state.unlink()
                expected.add(paths[1])

            before = index_path.read_bytes()
            assert (
                doctor_module._preexisting_repair_paths(root, index_path) == expected
            ), change
            assert index_path.read_bytes() == before, change
    finally:
        index_path.unlink(missing_ok=True)


@pytest.mark.parametrize("stages", [(1,), (1, 3)])
def test_preexisting_runtime_paths_preserves_unmerged_entries(
    repair_paths_repository, stages
):
    """DD/DU の削除 conflict は通常の staged deletion と区別して保存対象にする。"""
    root = repair_paths_repository
    config = doctor_module.config_path(root)
    relative = str(config.relative_to(root))
    blob = run_git(root, "rev-parse", f"HEAD:{relative}").stdout.strip()
    index_path = doctor_module._copy_current_index(root)
    try:
        # stage 0 を外し、both deleted / deleted by us の実 index entry を作る。
        entries = f"0 {'0' * len(blob)}\t{relative}\n" + "".join(
            f"100644 {blob} {stage}\t{relative}\n" for stage in stages
        )
        doctor_module._run_git_with_index(
            ["update-index", "--index-info"], root, index_path, input_text=entries
        )
        before = index_path.read_bytes()
        assert doctor_module._preexisting_repair_paths(root, index_path) == {relative}
        assert index_path.read_bytes() == before
    finally:
        index_path.unlink(missing_ok=True)


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_does_not_commit_preexisting_staged_config_change(
    managed_repository: Path,
) -> None:
    """doctor が事前に stage された人間の config 変更を修復 commit に混ぜない。"""

    root = managed_repository
    config_path = root / ".cmoc" / "gt" / "config.json"
    data = json.loads(config_path.read_text())
    data["num_parallel"] = 99
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    run_git(root, "add", ".cmoc/gt/config.json")
    before_head = run_git(root, "rev-parse", "HEAD").stdout.strip()

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == before_head
    assert (
        json.loads(run_git(root, "show", "HEAD:.cmoc/gt/config.json").stdout)[
            "num_parallel"
        ]
        != 99
    )
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        ".cmoc/gt/config.json"
    ]
    assert (
        json.loads(run_git(root, "show", ":.cmoc/gt/config.json").stdout)[
            "num_parallel"
        ]
        == 99
    )


def test_doctor_preprocess_separates_repo_and_linked_worktree_repairs(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """両 worktree の非追跡保証と current の tracked runtime を修復する。"""

    # worktree 分離には HEAD だけあれば足り、初期 file の内容は参照しない。
    root = committed_repository
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-doctor"
    run_git(root, "worktree", "add", "-b", "linked-doctor", str(linked), "HEAD")
    monkeypatch.chdir(linked)

    result = run_doctor(linked)

    assert result.exit_code == 0
    assert "/.cmoc/gu/" in (linked / ".gitignore").read_text()
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
            cwd=linked,
            check=False,
        ).returncode
        == 0
    )
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert run_git(root, "ls-files", "--", ".agents").stdout == ""
    assert (
        run_git(
            root,
            "check-ignore",
            "-q",
            ".cmoc/gu/worktree/linked-doctor",
        ).returncode
        == 0
    )
    assert (
        run_git(
            root, "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"
        ).returncode
        == 0
    )
    assert not (root / ".cmoc" / "gt" / "config.json").exists()
    assert list((root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl"))
    assert not (linked / ".cmoc" / "gu" / "log" / "sub_command").exists()
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert (linked / ".cmoc" / "gt" / "config.json").exists()
    assert f"- repo_root: `{root}`" in result.stdout
    assert all((linked / relative).is_dir() for relative in _WORK_DIRECTORIES)
    assert all(not (root / relative).exists() for relative in _WORK_DIRECTORIES)


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preprocess_untracks_existing_cmoc_local_files(
    cli_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """無変更と staged/unstaged 変更のある管理物を、実体を保って追跡から外す。"""

    # 同じ除外処理の入力を別 file に置き、repository 準備と doctor 起動を共有する。
    root = cli_repository
    unchanged = root / ".cmoc/gu/cache.json"
    changed = root / ".cmoc/gu/nested/changed.json"
    changed.parent.mkdir(parents=True)
    unchanged.write_text("{}\n")
    changed.write_text('{"old": true}\n')
    run_git(root, "add", "-f", ".cmoc/gu")
    run_git(root, "commit", "-m", "track old cmoc local cache")
    changed.write_text('{"new": true}\n')
    run_git(root, "add", "-f", ".cmoc/gu/nested/changed.json")
    changed.write_text('{"working": true}\n')
    monkeypatch.chdir(root)

    run_doctor(root)

    assert unchanged.read_text() == "{}\n"
    assert changed.read_text() == '{"working": true}\n'
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_commits_generated_gitkeep_without_committing_staged_agents_deletion(
    cli_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """生成した `.agents/.gitkeep` だけを修復 commit し、既存の削除 stage を保つことを検証する。"""

    root = cli_repository
    agents_file = root / ".agents" / "existing.txt"
    agents_file.parent.mkdir()
    agents_file.write_text("existing\n")
    run_git(root, "add", ".agents")
    run_git(root, "commit", "-m", "track agent file")
    agents_file.unlink()
    run_git(root, "add", "-u", ".agents")
    monkeypatch.chdir(root)

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    gitkeep = root / ".agents" / ".gitkeep"
    assert gitkeep.is_file()
    assert gitkeep.read_text() == ""
    repair_paths = run_git(
        root, "show", "--name-only", "--format=", "HEAD"
    ).stdout.splitlines()
    assert ".agents/.gitkeep" in repair_paths
    assert run_git(root, "diff", "--cached", "--name-status").stdout.splitlines() == [
        "D\t.agents/existing.txt"
    ]


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preserves_existing_untracked_gitkeep_content(
    committed_repository: Path,
) -> None:
    """既存の未追跡 `.agents/.gitkeep` を空内容へ置き換えず追跡する。"""

    root = committed_repository
    gitkeep = root / ".agents" / ".gitkeep"
    gitkeep.parent.mkdir()
    gitkeep.write_text("human content\n")

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "show", "HEAD:.agents/.gitkeep").stdout == "human content\n"
    assert gitkeep.read_text() == "human content\n"
    assert run_git(root, "status", "--short").stdout == ""


@pytest.mark.parametrize("staged_gitkeep_deletion", [False, True])
def test_agents_tracking_preserves_existing_files_and_index(
    cli_repository, monkeypatch, staged_gitkeep_deletion
):
    """別の追跡 file があれば placeholder を追加せず、既存の削除 stage も保つ。"""
    # HEAD は agent file の commit で用意し、config・索引同期・doctor 全体は準備しない。
    root = cli_repository
    kept = root / ".agents/kept.txt"
    kept.parent.mkdir()
    kept.write_text("tracked agent content\n")
    gitkeep = kept.parent / ".gitkeep"
    if staged_gitkeep_deletion:
        gitkeep.write_text("existing placeholder content\n")
    run_git(root, "add", ".agents")
    run_git(root, "commit", "-m", "track agent files")
    if staged_gitkeep_deletion:
        run_git(root, "rm", ".agents/.gitkeep")
    kept.write_text("unstaged agent content\n")
    kept_before = kept.stat().st_mtime_ns
    index = root / ".git/index"
    index_before = index.read_bytes()

    git_calls = 0
    original_run = doctor_module.subprocess.run

    def count_git_calls(argv, *args, **kwargs):
        nonlocal git_calls
        if argv[0] == "git":
            git_calls += 1
        return original_run(argv, *args, **kwargs)

    with monkeypatch.context() as observed:
        observed.setattr(doctor_module.subprocess, "run", count_git_calls)
        assert doctor_module._ensure_agents_tracked(root) is False

    # 列挙と HEAD の確認で足り、既存 placeholder の復元だけはもう一回必要。
    assert git_calls <= (3 if staged_gitkeep_deletion else 2)
    assert kept.read_text() == "unstaged agent content\n"
    assert kept.stat().st_mtime_ns == kept_before
    assert index.read_bytes() == index_before
    if staged_gitkeep_deletion:
        assert gitkeep.read_text() == "existing placeholder content\n"
    else:
        assert not gitkeep.exists()


@pytest.mark.parametrize("index_flag", [None, "--skip-worktree"])
def test_agents_tracking_restores_missing_tracked_gitkeep(
    cli_repository: Path,
    index_flag: str | None,
) -> None:
    """tracked placeholder の内容を復元し、通常 entry と skip-worktree を保つ。"""

    root = cli_repository
    # doctor 全体との結合は配置先復元の test に残し、ここでは復元の境界条件を扱う。
    gitkeep = root / ".agents" / ".gitkeep"
    gitkeep.parent.mkdir()
    gitkeep.write_text("tracked placeholder content\n")
    run_git(root, "add", ".agents/.gitkeep")
    run_git(root, "commit", "-m", "track agents placeholder")
    if index_flag is not None:
        run_git(root, "update-index", index_flag, ".agents/.gitkeep")
    before_flags = run_git(root, "ls-files", "-v", ".agents/.gitkeep").stdout
    index = root / ".git/index"
    before_index = index.read_bytes()
    gitkeep.unlink()

    assert doctor_module._ensure_agents_tracked(root) is False

    assert gitkeep.read_text() == "tracked placeholder content\n"
    assert index.read_bytes() == before_index
    assert run_git(root, "status", "--short").stdout == ""
    assert run_git(root, "ls-files", "-v", ".agents/.gitkeep").stdout == before_flags


@pytest.mark.parametrize("symlinked_path", ["agents", "gitkeep"])
def test_doctor_rejects_symlinked_agents_paths(
    committed_repository: Path,
    tmp_path: Path,
    symlinked_path: str,
) -> None:
    """doctor が .agents 外への symlink 経由書き込みを拒否する。"""
    root = committed_repository
    outside = tmp_path / "outside"
    if symlinked_path == "agents":
        outside.mkdir()
        (root / ".agents").symlink_to(outside, target_is_directory=True)
        outside_content = None
    else:
        outside.write_text("outside\n")
        (root / ".agents").mkdir()
        (root / ".agents" / ".gitkeep").symlink_to(outside)
        outside_content = outside.read_text()

    with pytest.raises(CmocError):
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert not (outside / ".gitkeep").exists()
    if outside_content is not None:
        assert outside.read_text() == outside_content


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_repair_separates_committed_staged_and_unstaged_gitignore(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """一度の修復で、commit・index・作業 file の差分の分離と保持を検証する。"""

    root = committed_repository
    gitignore = root / ".gitignore"
    gitignore.write_text("staged-rule\n")
    run_git(root, "add", ".gitignore")
    gitignore.write_text("staged-rule\nunstaged-rule\n")
    monkeypatch.chdir(root)

    run_doctor(root)

    # 各保存先の内容を比較し、利用者の hunk の commit 混入・消失・誤 stage を検出する。
    assert run_git(root, "show", "HEAD:.gitignore").stdout == "/.cmoc/gu/\n"
    assert run_git(root, "show", ":.gitignore").stdout == "staged-rule\n\n/.cmoc/gu/\n"
    assert gitignore.read_text() == "staged-rule\nunstaged-rule\n\n/.cmoc/gu/\n"
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        ".gitignore"
    ]


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preprocess_preserves_preexisting_staged_addition_and_rename(
    cli_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """利用者の追加・rename を修復 commit に混ぜず、元の staged 内容を保つ。"""

    root = cli_repository
    old_path = root / "old.txt"
    new_path = root / "new.txt"
    old_path.write_text("same content\n")
    run_git(root, "add", "old.txt")
    run_git(root, "commit", "-m", "add old file")
    old_path.rename(new_path)
    (root / "user.txt").write_text("user change\n")
    run_git(root, "add", "-A", "old.txt", "new.txt", "user.txt")
    monkeypatch.chdir(root)

    run_doctor(root)

    committed_paths = set(
        run_git(root, "show", "--name-only", "--format=", "HEAD").stdout.splitlines()
    )
    assert not {"old.txt", "new.txt", "user.txt"} & committed_paths
    assert run_git(root, "diff", "--cached", "--name-status").stdout.splitlines() == [
        "R100\told.txt\tnew.txt",
        "A\tuser.txt",
    ]
    assert run_git(root, "show", ":user.txt").stdout == "user change\n"
    assert run_git(root, "diff", "--name-status").stdout.strip() == ""


def test_repair_paths_share_one_query_and_preserve_saved_index(
    repair_paths_repository, tmp_path, monkeypatch
):
    """runtime 差分と ignore 削除を一度に判定し、退避 index 自体は変更しない。"""
    # 全対象を同じ index に置き、別 root の修復では runtime を保存対象に含めない。
    root = repair_paths_repository
    config = doctor_module.config_path(root)
    state = doctor_module.refactor_state_path(root)
    runtime_paths = {str(path.relative_to(root)) for path in (config, state)}
    config.write_text('{"staged": true}\n')
    run_git(root, "add", "-f", str(config.relative_to(root)))
    state.write_text('{"unstaged": true}\n')
    blob = run_git(root, "rev-parse", "HEAD:.gitignore").stdout.strip()
    original_index = (root / ".git/index").read_bytes()
    # 通常 index は退避 index と区別し、判定が渡された index を読むことも確認する。
    run_git(
        root, "update-index", "--force-remove", ".gitignore", *sorted(runtime_paths)
    )
    original_run = doctor_module.subprocess.run

    # HEAD と repository の準備は一度にし、各ケースでは退避 index だけを作り替える。
    for change in ("clean", "delete", "rename", "intent", "unmerged"):
        index_path = tmp_path / f"{change}.index"
        index_path.write_bytes(original_index)
        if change != "clean":
            doctor_module._run_git_with_index(
                ["update-index", "--force-remove", ".gitignore"], root, index_path
            )
        if change == "rename":
            doctor_module._stage_blobs(
                root, index_path, [("renamed-ignore", "100644", blob)]
            )
        elif change == "intent":
            doctor_module._run_git_with_index(
                ["add", "-N", ".gitignore"], root, index_path
            )
        elif change == "unmerged":
            doctor_module._run_git_with_index(
                ["update-index", "--index-info"],
                root,
                index_path,
                input_text=f"100644 {blob} 1\t.gitignore\n100644 {blob} 3\t.gitignore\n",
            )
        before = index_path.read_bytes()
        for include_config in (False, True):
            git_calls = 0

            def count_git_calls(argv, *args, **kwargs):
                nonlocal git_calls
                if argv[0] == "git":
                    git_calls += 1
                return original_run(argv, *args, **kwargs)

            expected = runtime_paths.copy() if include_config else set()
            if change in {"delete", "rename"}:
                expected.add(".gitignore")
            with monkeypatch.context() as observed:
                observed.setattr(doctor_module.subprocess, "run", count_git_calls)
                assert (
                    doctor_module._preexisting_repair_paths(
                        root, index_path, include_config=include_config
                    )
                    == expected
                ), (change, include_config)

            assert git_calls <= 1, (change, include_config)
            assert index_path.read_bytes() == before, (change, include_config)


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_preserves_preexisting_staged_gitignore_deletion(
    cli_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が既存 .gitignore の staged deletion も保持する。"""

    root = cli_repository
    monkeypatch.chdir(root)
    # staged deletion の前提には追跡済み ignore file があれば足りる。
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "track cmoc ignore rule")

    run_git(root, "rm", "--cached", "-f", "--", ".gitignore")
    before = run_git(root, "diff", "--cached", "--name-status").stdout

    run_doctor(root)

    assert run_git(root, "diff", "--cached", "--name-status").stdout == before
    assert run_git(root, "ls-files", "--stage", "--", ".gitignore").stdout == ""


@pytest.mark.parametrize(
    ("failure_code", "expected_status"),
    [("MODEL_FAILURE", "failed"), ("CANCELLED", "cancelled")],
)
def test_doctor_reports_persisted_chunks_when_sync_fails(
    cli_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_code: str,
    expected_status: str,
) -> None:
    """doctor の同期失敗は未完了とし、保存済み chunk の進捗を示す。"""
    # 索引対象の文書を初回 commit に置き、参照しない README と仕様 file を準備しない。
    root = cli_repository
    docs = root / "spec"
    docs.mkdir(parents=True)
    (docs / "sample.md").write_text("# 検索用の原文\n")
    run_git(root, "add", "spec")
    run_git(root, "commit", "-m", "add document")
    monkeypatch.chdir(root)
    vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)

    class StoppingWorker:
        def stream_chunks(
            self,
            documents,
            resumes,
            on_event,
            *,
            reusable_hashes,
            deadline,
            residency_fd,
            cancelled,
        ):
            assert deadline is None
            path, source = next(iter(documents.items()))
            on_event(
                {
                    "kind": "chunk",
                    "path": path,
                    "ordinal": 0,
                    "start": 0,
                    "end": len(source),
                    "embedding": vector,
                }
            )
            raise SearchError(failure_code, "stopped after first chunk")

    def failing_search(root, config, *, installation_root, use_saved_config):
        return DocumentSearch(
            root,
            config,
            worker=StoppingWorker(),
            installation_root=installation_root,
            use_saved_config=use_saved_config,
        )

    monkeypatch.setattr(doctor_module, "DocumentSearch", failing_search)
    result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code != 0
    report = terminal_primary_report(result).read_text()
    assert f'doctor_sync_status: "{expected_status}"' in report
    assert "persisted_chunks" in report
    assert "stopped after first chunk" in report
    assert f"実行状態: `{expected_status}`" in report
    events = _new_subcommand_events(root, set())
    start = next(e for e in events if e["event"] == "document_search_sync_started")
    finish = next(e for e in events if e["event"] == "document_search_sync_finished")
    assert start["sync_id"] == finish["sync_id"]
    assert finish["status"] == expected_status
    assert finish["failure_code"] == failure_code
    assert finish["counts_complete"] is False
    assert finish["document_count"] == 1
    assert finish["changed_document_count"] == 1
    assert finish["persisted_chunk_count"] == 1
    assert finish["reused_chunk_count"] == 0


def test_normal_preprocess_requires_validated_materials(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """通常起動は資材未検証なら本命処理前に doctor を案内する。"""
    root = committed_repository
    monkeypatch.chdir(root)
    # 保存済み設定だけを用意し、失敗点より後の索引同期・reporter を先行実行しない。
    config_path = doctor_module.config_path(root)
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config_to_dict(CmocConfig())) + "\n")

    def missing_materials(_root: Path, _config: object) -> Path:
        raise SearchError("NOT_READY", "validation record is missing")

    monkeypatch.setattr(
        doctor_module, "require_document_search_materials", missing_materials
    )
    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)

    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert "validation record is missing" in exc_info.value.detail


@pytest.mark.usefixtures("doctor_without_index_sync")
def test_doctor_repairs_shared_cmoc_root_in_its_own_repository(
    committed_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """別 installation の共有資材書込み前に、その所有 repository の非追跡を修復する。"""
    root = committed_repository
    # どちらも HEAD だけで足りる。設定・refs・index を共有せず、準備用 commit を省く。
    installation = shutil.copytree(root, tmp_path / "installation")
    monkeypatch.setattr(doctor_module, "_installation_root", lambda _root: installation)
    monkeypatch.chdir(root)

    result = run_doctor(root)

    assert (
        run_git(installation, "ls-files", ".gitignore").stdout.strip() == ".gitignore"
    )
    assert "/.cmoc/gu/" in (installation / ".gitignore").read_text()
    assert f'cmoc_root: "{installation}"' in terminal_primary_report(result).read_text()
    assert all((root / relative).is_dir() for relative in _WORK_DIRECTORIES)
    assert all(not (installation / relative).exists() for relative in _WORK_DIRECTORIES)

    run_git(installation, "rm", ".gitignore")
    run_git(installation, "commit", "-m", "remove shared ignore")
    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert str(installation) in exc_info.value.detail
    assert not (installation / ".gitignore").exists()
