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
- `{{work-root}}/oracle/doc/app_spec/doctor_preprocess.md`
- `{{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/doctor.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md`
- `{{work-root}}/oracle/src/oracle/other/cmoc_config.py`
"""

import json
import multiprocessing
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner, terminal_primary_report
from _git_support import make_repo, run_git
from oracle.other.document_search import INITIAL_SEARCH_MATERIALS

import commons.runtime_doctor as doctor_module
import commons.runtime_feedback_store as feedback_store_module
from commons.runtime_config import config_to_dict
from commons.runtime_document_search import DocumentSearch, SearchError
from commons.runtime_errors import CmocError
from commons.runtime_feedback import ReporterAvailabilityError
from commons.runtime_refactor import RefactorState
from config.cmoc_config import CmocConfig
from main import app


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
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が Git 状態、config、refactor state を修復する。"""

    root = make_repo(tmp_path)

    monkeypatch.chdir(root)
    result = run_doctor(root)

    report = terminal_primary_report(result)
    assert report.parent == root / ".cmoc" / "gu" / "report" / "doctor"
    rendered_report = report.read_text(encoding="utf-8")
    assert 'terminal_classification: "natural_completion"' in rendered_report
    assert "exit_code: 0" in rendered_report
    assert "doctor preprocess" in rendered_report
    assert "## 検索索引の同期" in rendered_report
    assert "実効閲覧範囲" in rendered_report
    assert "逐次反映と再利用" in rendered_report
    assert "診断用サブコマンドログ" in rendered_report

    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert run_git(root, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    agents_gitkeep = root / ".agents" / ".gitkeep"
    assert agents_gitkeep.is_file()
    assert agents_gitkeep.read_text() == ""
    repair_commit_paths = run_git(
        root, "show", "--name-only", "--format=", "HEAD"
    ).stdout
    assert ".gitignore" in repair_commit_paths
    assert ".agents/.gitkeep" in repair_commit_paths
    assert ".cmoc/gt/config.json" in repair_commit_paths
    assert ".cmoc/gt/realization/refactor/state.json" in repair_commit_paths
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
            "investigation_required": True,
            "last_investigation_result": "not_investigated",
            "last_investigated_sha256": None,
            "last_investigated_at": None,
        }
        for entry in state.values()
    )


def test_doctor_syncs_document_edits_and_deletions_without_committing_them(
    tmp_path: Path,
) -> None:
    """手動同期が保存済みの編集・削除を反映し、利用者の差分を commit しない。"""
    root = make_repo(tmp_path)
    document = root / "oracle/doc/source.md"
    document.parent.mkdir()
    original = "# original document\n"
    document.write_text(original)
    run_git(root, "add", "oracle/doc/source.md")
    run_git(root, "commit", "-m", "add search document")
    run_doctor(root)

    document.write_text("# updated document\n")
    updated = terminal_primary_report(run_doctor(root)).read_text()

    assert 'doctor_sync_status: "updated"' in updated
    assert '"changed": 1' in updated
    assert document.read_text() == "# updated document\n"
    assert run_git(root, "show", "HEAD:oracle/doc/source.md").stdout == original

    unchanged = terminal_primary_report(run_doctor(root)).read_text()
    assert 'doctor_sync_status: "unchanged"' in unchanged

    document.unlink()
    deleted = terminal_primary_report(run_doctor(root)).read_text()
    state = json.loads((root / ".cmoc/gt/realization/refactor/state.json").read_text())

    assert 'doctor_sync_status: "updated"' in deleted
    assert '"deleted": 1' in deleted
    assert "oracle/doc/source.md" not in state
    assert not document.exists()
    assert run_git(root, "show", "HEAD:oracle/doc/source.md").stdout == original


def test_doctor_sync_log_records_each_run_and_current_work(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """初回・無変更・削除の件数と結果を、同じ実行の開始/終端に対応付ける。"""
    root = make_repo(tmp_path)
    document = root / "oracle/doc/source.md"
    document.parent.mkdir()
    document.write_text("# source\n")
    run_git(root, "add", "oracle/doc/source.md")
    run_git(root, "commit", "-m", "add search document")
    monkeypatch.chdir(root)
    log_dir = root / ".cmoc/gu/log/sub_command"

    for expected, edit in (
        (("updated", 1, 1, 1, 0), None),
        (("unchanged", 1, 0, 0, 1), None),
        (("updated", 0, 1, 0, 0), document.unlink),
    ):
        if edit is not None:
            edit()
        previous = set(log_dir.glob("*.jsonl"))
        result = run_doctor(root)
        events = _new_subcommand_events(root, previous)
        starts = [e for e in events if e["event"] == "document_search_sync_started"]
        finishes = [e for e in events if e["event"] == "document_search_sync_finished"]
        assert len(starts) == len(finishes) == 1
        start, finish = starts[0], finishes[0]
        assert events.index(start) < events.index(finish) < len(events) - 1
        assert start["sync_id"] == finish["sync_id"]
        assert start["invocation_id"] == finish["invocation_id"]
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


def test_doctor_preprocess_follows_repair_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が oracle の ignore、agents、config、state 順に修復する。"""
    root = make_repo(tmp_path)
    events: list[str] = []
    original_ignore = doctor_module.ensure_cmoc_ignored
    original_agents = doctor_module._ensure_agents_tracked
    original_config = doctor_module.sync_config
    original_state = doctor_module.sync_refactor_state

    def observe_ignore(path: Path) -> None:
        """ignore 修復の呼び出し順を記録する。"""
        events.append("ignore")
        original_ignore(path)

    def observe_agents(path: Path) -> bool:
        """agents 修復の呼び出し順を記録する。"""
        events.append("agents")
        return original_agents(path)

    def observe_config(path: Path, **kwargs):
        """config 修復の呼び出し順を記録する。"""
        events.append("config")
        return original_config(path, **kwargs)

    def observe_state(path: Path, *, sync_entries: bool = True) -> RefactorState:
        """refactor state 修復の呼び出し順を記録する。"""
        events.append("state")
        return original_state(path, sync_entries=sync_entries)

    def observe_reporter() -> None:
        """reporter 事前検証の呼び出し順を記録する。"""
        events.append("reporter")

    monkeypatch.setattr(doctor_module, "ensure_cmoc_ignored", observe_ignore)
    monkeypatch.setattr(doctor_module, "_ensure_agents_tracked", observe_agents)
    monkeypatch.setattr(doctor_module, "sync_config", observe_config)
    monkeypatch.setattr(doctor_module, "sync_refactor_state", observe_state)
    monkeypatch.setattr(
        doctor_module,
        "validate_feedback_reporter_availability",
        observe_reporter,
    )

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert events == ["ignore", "agents", "config", "state", "reporter"]


def test_doctor_preprocess_continues_with_degraded_reporter(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """reporter 利用不能を warning と event に留めて本命処理を続ける。"""
    root = make_repo(tmp_path)

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


def test_doctor_preprocess_propagates_interrupt_during_reporter_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """reporter 事前検証中のユーザー中断を degraded warning に変換しない。"""
    root = make_repo(tmp_path)

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


def test_doctor_preprocess_propagates_unexpected_reporter_probe_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """予期しない reporter 検証エラーを利用不能 warning に変換しない。"""
    root = make_repo(tmp_path)

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


def test_doctor_preprocess_propagates_interrupt_during_reporter_schema_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """reporter schema の予期しない中断も利用不能 warning に変換しない。"""
    root = make_repo(tmp_path)

    def interrupt() -> None:
        """reporter schema 読み込み中の Ctrl+C を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(feedback_store_module, "reporter_input_schema", interrupt)

    with pytest.raises(KeyboardInterrupt):
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)


def test_doctor_preprocess_waits_for_common_repository_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree と repository で共有する doctor lock の解放待ちを検証する。"""

    root = make_repo(tmp_path)
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
    lock_attempted = threading.Event()
    original_flock = doctor_module.fcntl.flock

    def observe_lock_attempt(fd: int, operation: int) -> None:
        """doctor が排他 lock を取得しようとしたことをテストへ通知する。"""

        if operation & doctor_module.fcntl.LOCK_EX:
            lock_attempted.set()
        original_flock(fd, operation)

    monkeypatch.setattr(doctor_module.fcntl, "flock", observe_lock_attempt)
    process.start()
    released = False
    try:
        assert ready_parent.recv() is True
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                doctor_module.run_doctor_preprocess,
                linked,
                explicit_doctor=True,
            )
            assert lock_attempted.wait(timeout=3)
            assert not future.done()
            release_parent.send(True)
            released = True
            future.result(timeout=3)
    finally:
        if process.is_alive() and not released:
            release_parent.send(True)
        process.join(timeout=3)
        if process.is_alive():
            process.terminate()
            process.join()


def test_doctor_restores_preexisting_index_when_repair_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor の修復失敗時も、呼び出し前の staged index を保持する。"""

    root = make_repo(tmp_path)
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
        preserved_runtime_paths: set[str],
    ) -> None:
        """repair commit の失敗を再現する。"""
        del include_config, include_gu_ignore, preserved_runtime_paths
        raise RuntimeError("repair commit failure")

    monkeypatch.setattr(doctor_module, "_commit_doctor_repairs_from_head", fail_commit)

    with pytest.raises(RuntimeError, match="repair commit failure"):
        doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "write-tree").stdout.strip() == expected_index_tree
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "staged.txt"
    ]


def test_doctor_preserves_preexisting_unmerged_index(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が既存の unmerged index を検査・解消せず保持する。"""

    root = make_repo(tmp_path)
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


def test_doctor_repairs_missing_index_without_dropping_tracked_files(
    tmp_path: Path,
) -> None:
    """欠落した Git index を復元し、既存の tracked file を保持する。"""

    root = make_repo(tmp_path)
    (root / ".git" / "index").unlink()

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    tracked = set(run_git(root, "ls-files").stdout.splitlines())
    assert {"README.md", "oracle/spec.md"} <= tracked
    assert run_git(root, "status", "--short").stdout == ""


@pytest.mark.parametrize("index_flag", ["--assume-unchanged", "--skip-worktree"])
def test_doctor_preserves_preexisting_index_flags(
    tmp_path: Path,
    index_flag: str,
) -> None:
    """doctor が内容以外の Git index flag も保持する。"""

    root = make_repo(tmp_path)
    run_git(root, "update-index", index_flag, "README.md")
    before = run_git(root, "ls-files", "-v", "README.md").stdout

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "ls-files", "-v", "README.md").stdout == before


def test_doctor_preserves_preexisting_intent_to_add_index_file(tmp_path: Path) -> None:
    """doctor が intent-to-add の通常 file を未追跡へ戻さない。"""

    root = make_repo(tmp_path)
    path = root / "new.txt"
    path.write_text("new\n")
    run_git(root, "add", "-N", "new.txt")
    before_entry = run_git(root, "ls-files", "--stage", "new.txt").stdout
    before_status = run_git(root, "status", "--short").stdout

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "ls-files", "--stage", "new.txt").stdout == before_entry
    assert run_git(root, "status", "--short").stdout == before_status


def test_doctor_generates_and_tracks_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor が既定 config を生成し、Git index へ追跡することを検証する。"""

    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "config.json"
    monkeypatch.chdir(root)

    result = run_doctor(root)

    assert config_path.is_file()
    assert (
        run_git(root, "ls-files", "--", ".cmoc/gt/config.json").stdout.strip()
        == ".cmoc/gt/config.json"
    )
    assert json.loads(config_path.read_text())["codex"]["num_try_falv_recovery"] == 1
    assert json.loads(config_path.read_text())["codex"]["model_providers"] == {
        "openai": {"settings": {}}
    }
    assert (
        ".cmoc/gt/config.json"
        in run_git(root, "show", "--name-only", "--format=", "HEAD").stdout.splitlines()
    )
    report = terminal_primary_report(result).read_text()
    assert str(config_path) in report
    assert "document_search.chunk_tokens: `512`" in report
    assert "- 検証: `成功`" in report
    assert "- 保存: `True`" in report


def test_normal_preprocess_rejects_unset_search_without_rewriting_config(
    tmp_path: Path,
) -> None:
    """通常起動では不足した設定を補完せず、仕事の開始前に診断する。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = '{"num_parallel": 3, "document_search": null}\n'
    path.write_text(original)

    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)

    assert str(path) in exc_info.value.detail
    assert "document_search" in exc_info.value.detail
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert path.read_text() == original


def test_doctor_reports_unsaved_inconsistent_search_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補完候補が衝突した場合、doctor report に値と非保存を残す。"""
    root = make_repo(tmp_path)
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


def test_doctor_generates_config_under_broad_cmoc_ignore(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """広い `.cmoc/` ignore があっても生成 config を追跡可能に修復することを検証する。"""

    root = make_repo(tmp_path)
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


def test_doctor_does_not_commit_preexisting_staged_config_change(
    tmp_path: Path,
) -> None:
    """doctor が事前に stage された人間の config 変更を修復 commit に混ぜない。"""

    root = make_repo(tmp_path)
    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """両 worktree の非追跡保証と current の tracked runtime を修復する。"""

    root = make_repo(tmp_path)
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


def test_doctor_syncs_default_config_without_overwriting_human_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """既存 config の人間による値を保ったまま不足する既定値を同期することを検証する。"""

    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "config.json"
    config_path.parent.mkdir(parents=True)
    data = config_to_dict(CmocConfig())
    data["num_parallel"] = 3
    data["codex"]["model_providers"]["custom"] = {"settings": {}}
    data["codex"]["num_try_falv_recovery"] = 4
    data["codex"]["agent_calls"]["build_tui_launch_tui_parameter"] = {
        "model_provider": "custom",
        "model": "CUSTOM",
        "reasoning_effort": "CUSTOM-EFFORT",
    }
    data.pop("document_search")
    config_path.write_text(json.dumps(data) + "\n")
    monkeypatch.chdir(root)

    run_doctor(root)
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model_providers"] == {
        "openai": {"settings": {}},
        "custom": {"settings": {}},
    }
    assert data["codex"]["agent_calls"]["build_tui_launch_tui_parameter"] == {
        "model_provider": "custom",
        "model": "CUSTOM",
        "reasoning_effort": "CUSTOM-EFFORT",
    }
    default_call = CmocConfig().codex.agent_calls[
        "build_feedback_normalize_issue_parameter"
    ]
    assert data["codex"]["agent_calls"]["build_feedback_normalize_issue_parameter"] == {
        "model_provider": default_call.model_provider,
        "model": default_call.model,
        "reasoning_effort": default_call.reasoning_effort,
    }
    assert data["codex"]["num_try_falv_recovery"] == 4
    assert "model" not in data["codex"]
    assert "reasoning_effort" not in data["codex"]
    assert "apply_fork" not in data


def test_doctor_preprocess_untracks_existing_cmoc_local_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """既に追跡された `.cmoc/gu` のファイルを実体を残して index から外すことを検証する。"""

    root = make_repo(tmp_path)
    local_path = root / ".cmoc" / "gu" / "cache.json"
    local_path.parent.mkdir(parents=True)
    local_path.write_text("{}\n")
    run_git(root, "add", "-f", ".cmoc/gu/cache.json")
    run_git(root, "commit", "-m", "track old cmoc local cache")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert local_path.is_file()
    assert local_path.read_text() == "{}\n"


def test_doctor_preprocess_does_not_restore_preexisting_staged_cmoc_local_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """事前に stage された `.cmoc/gu` の変更を doctor が復元・上書きしないことを検証する。"""

    root = make_repo(tmp_path)
    local_path = root / ".cmoc" / "gu" / "cache.json"
    local_path.parent.mkdir(parents=True)
    local_path.write_text('{"old": true}\n')
    run_git(root, "add", "-f", ".cmoc/gu/cache.json")
    run_git(root, "commit", "-m", "track old cmoc local cache")
    local_path.write_text('{"new": true}\n')
    run_git(root, "add", "-f", ".cmoc/gu/cache.json")
    monkeypatch.chdir(root)
    local_path.write_text('{"working": true}\n')

    run_doctor(root)

    assert local_path.read_text() == '{"working": true}\n'
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(root, "diff", "--cached", "--name-only").stdout.strip() == ""


def test_doctor_commits_generated_gitkeep_without_committing_staged_agents_deletion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """生成した `.agents/.gitkeep` だけを修復 commit し、既存の削除 stage を保つことを検証する。"""

    root = make_repo(tmp_path)
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


def test_doctor_preserves_existing_untracked_gitkeep_content(
    tmp_path: Path,
) -> None:
    """既存の未追跡 `.agents/.gitkeep` を空内容へ置き換えず追跡する。"""

    root = make_repo(tmp_path)
    gitkeep = root / ".agents" / ".gitkeep"
    gitkeep.parent.mkdir()
    gitkeep.write_text("human content\n")

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert run_git(root, "show", "HEAD:.agents/.gitkeep").stdout == "human content\n"
    assert gitkeep.read_text() == "human content\n"
    assert run_git(root, "status", "--short").stdout == ""


@pytest.mark.parametrize("index_flag", [None, "--skip-worktree"])
def test_doctor_restores_missing_tracked_gitkeep(
    tmp_path: Path,
    index_flag: str | None,
) -> None:
    """tracked な `.agents/.gitkeep` の unstaged deletion を復元する。"""

    root = make_repo(tmp_path)
    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)
    gitkeep = root / ".agents" / ".gitkeep"
    if index_flag is not None:
        run_git(root, "update-index", index_flag, ".agents/.gitkeep")
    before_flags = run_git(root, "ls-files", "-v", ".agents/.gitkeep").stdout
    gitkeep.unlink()

    doctor_module.run_doctor_preprocess(root, explicit_doctor=True)

    assert gitkeep.read_text() == ""
    assert run_git(root, "status", "--short").stdout == ""
    assert run_git(root, "ls-files", "-v", ".agents/.gitkeep").stdout == before_flags


@pytest.mark.parametrize("symlinked_path", ["agents", "gitkeep"])
def test_doctor_rejects_symlinked_agents_paths(
    tmp_path: Path,
    symlinked_path: str,
) -> None:
    """doctor が .agents 外への symlink 経由書き込みを拒否する。"""
    root = make_repo(tmp_path)
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


def test_doctor_repair_commit_does_not_include_preexisting_staged_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor の修復 commit が事前に stage された利用者変更を取り込まないことを検証する。"""

    root = make_repo(tmp_path)
    user_file = root / "user.txt"
    user_file.write_text("user change\n")
    run_git(root, "add", "user.txt")
    monkeypatch.chdir(root)

    run_doctor(root)

    committed_paths = run_git(root, "show", "--name-only", "--format=", "HEAD").stdout
    assert "user.txt" not in committed_paths
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "user.txt"
    ]


def test_doctor_repair_commit_does_not_include_preexisting_staged_gitignore(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor の `.gitignore` 修復 commit が事前の stage 内容を上書きしないことを検証する。"""

    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    gitignore.write_text("human-rule\n")
    run_git(root, "add", ".gitignore")
    monkeypatch.chdir(root)

    run_doctor(root)

    committed_gitignore = run_git(root, "show", "HEAD:.gitignore").stdout
    assert "human-rule" not in committed_gitignore
    assert "/.cmoc/gu/" in committed_gitignore
    assert gitignore.read_text() == "human-rule\n\n/.cmoc/gu/\n"
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        ".gitignore"
    ]
    assert "human-rule" in run_git(root, "diff", "--cached").stdout


def test_doctor_preprocess_preserves_unstaged_hunks_on_repaired_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """修復対象 path にある staged と unstaged の差分をそれぞれ保つことを検証する。"""

    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    gitignore.write_text("staged-rule\n")
    run_git(root, "add", ".gitignore")
    gitignore.write_text("staged-rule\nunstaged-rule\n")
    monkeypatch.chdir(root)

    run_doctor(root)

    cached_diff = run_git(root, "diff", "--cached").stdout
    unstaged_diff = run_git(root, "diff").stdout
    assert "staged-rule" in cached_diff
    assert "unstaged-rule" not in cached_diff
    assert "unstaged-rule" in unstaged_diff
    assert gitignore.read_text() == "staged-rule\nunstaged-rule\n\n/.cmoc/gu/\n"


def test_doctor_preprocess_preserves_preexisting_staged_rename(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor が事前に stage された rename の index 表現を保つことを検証する。"""

    root = make_repo(tmp_path)
    old_path = root / "old.txt"
    new_path = root / "new.txt"
    old_path.write_text("same content\n")
    run_git(root, "add", "old.txt")
    run_git(root, "commit", "-m", "add old file")
    old_path.rename(new_path)
    run_git(root, "add", "-A", "old.txt", "new.txt")
    monkeypatch.chdir(root)

    run_doctor(root)

    assert run_git(root, "diff", "--cached", "--name-status").stdout.splitlines() == [
        "R100\told.txt\tnew.txt"
    ]
    assert run_git(root, "diff", "--name-status").stdout.strip() == ""


def test_doctor_preserves_preexisting_staged_gitignore_deletion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """doctor が既存 .gitignore の staged deletion も保持する。"""

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)

    run_git(root, "rm", "--cached", "-f", "--", ".gitignore")
    before = run_git(root, "diff", "--cached", "--name-status").stdout

    run_doctor(root)

    assert run_git(root, "diff", "--cached", "--name-status").stdout == before
    assert run_git(root, "ls-files", "--stage", "--", ".gitignore").stdout == ""


def test_doctor_fails_when_real_model_validation_does_not_complete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """資材が取得済みでも実モデル検証失敗を正常終了として報告しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def fail_materials(_root: Path, _config: object) -> dict[str, str]:
        raise SearchError("MODEL_FAILURE", "rerank validation failed")

    monkeypatch.setattr(
        doctor_module, "prepare_document_search_materials", fail_materials
    )
    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code != 0
    report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert 'terminal_classification: "error"' in report
    assert "照合と実モデル検証: `失敗`" in report
    assert "rerank validation failed" in report
    assert "cmoc doctor を再実行" in report
    events = _new_subcommand_events(root, set())
    assert not any(
        event["event"].startswith("document_search_sync_") for event in events
    )


@pytest.mark.parametrize(
    ("failure_code", "expected_status"),
    [("MODEL_FAILURE", "failed"), ("CANCELLED", "cancelled")],
)
def test_doctor_reports_persisted_chunks_when_sync_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_code: str,
    expected_status: str,
) -> None:
    """doctor の同期失敗は未完了とし、保存済み chunk の進捗を示す。"""
    root = make_repo(tmp_path)
    docs = root / "oracle/doc"
    docs.mkdir()
    (docs / "sample.md").write_text("# 検索用の原文\n")
    run_git(root, "add", "oracle/doc")
    run_git(root, "commit", "-m", "add document")
    monkeypatch.chdir(root)
    vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)

    class StoppingWorker:
        def stream_chunks(
            self, documents, resumes, on_event, *, deadline, residency_fd, cancelled
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

    def failing_search(root, scope, config, *, installation_root, use_saved_config):
        return DocumentSearch(
            root,
            scope,
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """通常起動は資材未検証なら本命処理前に doctor を案内する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)

    def missing_materials(_root: Path, _config: object) -> Path:
        raise SearchError("NOT_READY", "validation record is missing")

    monkeypatch.setattr(
        doctor_module, "require_document_search_materials", missing_materials
    )
    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)

    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert "validation record is missing" in exc_info.value.detail


def test_doctor_repairs_shared_cmoc_root_in_its_own_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """別 installation の共有資材書込み前に、その所有 repository の非追跡を修復する。"""
    root = make_repo(tmp_path)
    installation_parent = tmp_path / "installation"
    installation_parent.mkdir()
    installation = make_repo(installation_parent)
    monkeypatch.setattr(doctor_module, "_installation_root", lambda _root: installation)
    monkeypatch.chdir(root)

    result = run_doctor(root)

    assert (
        run_git(installation, "ls-files", ".gitignore").stdout.strip() == ".gitignore"
    )
    assert "/.cmoc/gu/" in (installation / ".gitignore").read_text()
    assert f'cmoc_root: "{installation}"' in terminal_primary_report(result).read_text()

    run_git(installation, "rm", ".gitignore")
    run_git(installation, "commit", "-m", "remove shared ignore")
    with pytest.raises(CmocError) as exc_info:
        doctor_module.run_doctor_preprocess(root)
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert str(installation) in exc_info.value.detail
    assert not (installation / ".gitignore").exists()
