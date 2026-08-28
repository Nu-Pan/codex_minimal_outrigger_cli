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
from _cli_support import run_doctor, terminal_primary_report
from _git_support import make_repo, run_git

import commons.runtime_doctor as doctor_module
import commons.runtime_feedback_store as feedback_store_module
from commons.runtime_errors import CmocError
from commons.runtime_feedback import ReporterAvailabilityError
from commons.runtime_refactor import RefactorState
from config.cmoc_config import CmocConfig


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
    assert report.parent == root / ".cmoc" / "gu" / "ar" / "report" / "doctor"
    rendered_report = report.read_text(encoding="utf-8")
    assert 'terminal_classification: "natural_completion"' in rendered_report
    assert "exit_code: 0" in rendered_report
    assert "doctor preprocess" in rendered_report
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
    assert ".cmoc/gt/ar/config.json" in repair_commit_paths
    assert ".cmoc/gt/ar/realization/refactor/state.json" in repair_commit_paths
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
            ["git", "check-ignore", "--no-index", "-q", ".cmoc/gt/ar/config.json"],
            cwd=root,
            check=False,
        ).returncode
        == 1
    )
    state_path = (
        root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    )
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

    def observe_config(path: Path) -> None:
        """config 修復の呼び出し順を記録する。"""
        events.append("config")
        original_config(path)

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

    doctor_module.run_doctor_preprocess(root)

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
    log_paths = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    )
    events = [
        json.loads(line) for path in log_paths for line in path.read_text().splitlines()
    ]
    assert any(
        event.get("event") == "feedback.reporter_unavailable"
        and event.get("component") == "reporter"
        and event.get("failure_code") == "missing"
        for event in events
    )
    assert run_git(root, "ls-files", "--", ".cmoc/gt/ar/config.json").stdout.strip()
    assert run_git(
        root,
        "ls-files",
        "--",
        ".cmoc/gt/ar/realization/refactor/state.json",
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
        doctor_module.run_doctor_preprocess(root)


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
        doctor_module.run_doctor_preprocess(root)


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
        doctor_module.run_doctor_preprocess(root)


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
        doctor_module.run_doctor_preprocess(root)

    assert run_git(root, "write-tree").stdout.strip() == expected_index_tree
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "staged.txt"
    ]


def test_doctor_repairs_missing_index_without_dropping_tracked_files(
    tmp_path: Path,
) -> None:
    """欠落した Git index を復元し、既存の tracked file を保持する。"""

    root = make_repo(tmp_path)
    (root / ".git" / "index").unlink()

    doctor_module.run_doctor_preprocess(root)

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

    doctor_module.run_doctor_preprocess(root)

    assert run_git(root, "ls-files", "-v", "README.md").stdout == before


def test_doctor_preserves_preexisting_intent_to_add_index_entry(tmp_path: Path) -> None:
    """doctor が intent-to-add の index entry を通常の未追跡へ戻さない。"""

    root = make_repo(tmp_path)
    path = root / "new.txt"
    path.write_text("new\n")
    run_git(root, "add", "-N", "new.txt")
    before_entry = run_git(root, "ls-files", "--stage", "new.txt").stdout
    before_status = run_git(root, "status", "--short").stdout

    doctor_module.run_doctor_preprocess(root)

    assert run_git(root, "ls-files", "--stage", "new.txt").stdout == before_entry
    assert run_git(root, "status", "--short").stdout == before_status


def test_doctor_generates_and_tracks_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor が既定 config を生成し、Git index へ追跡することを検証する。"""

    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    monkeypatch.chdir(root)

    run_doctor(root)

    assert config_path.is_file()
    assert (
        run_git(root, "ls-files", "--", ".cmoc/gt/ar/config.json").stdout.strip()
        == ".cmoc/gt/ar/config.json"
    )
    assert "num_try_falv_recovery" not in json.loads(config_path.read_text())["codex"]
    assert json.loads(config_path.read_text())["codex"]["model_providers"] == {
        "codex": {"settings": {}}
    }
    assert (
        ".cmoc/gt/ar/config.json"
        in run_git(root, "show", "--name-only", "--format=", "HEAD").stdout.splitlines()
    )


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
        run_git(root, "ls-files", "--", ".cmoc/gt/ar/config.json").stdout.strip()
        == ".cmoc/gt/ar/config.json"
    )
    check_ignore = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", ".cmoc/gt/ar/config.json"],
        cwd=root,
        check=False,
    )
    assert check_ignore.returncode == 1


def test_doctor_does_not_commit_preexisting_staged_config_change(
    tmp_path: Path,
) -> None:
    """doctor が事前に stage された人間の config 変更を修復 commit に混ぜない。"""

    root = make_repo(tmp_path)
    doctor_module.run_doctor_preprocess(root)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    data = json.loads(config_path.read_text())
    data["num_parallel"] = 99
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    run_git(root, "add", ".cmoc/gt/ar/config.json")
    before_head = run_git(root, "rev-parse", "HEAD").stdout.strip()

    doctor_module.run_doctor_preprocess(root)

    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == before_head
    assert (
        json.loads(run_git(root, "show", "HEAD:.cmoc/gt/ar/config.json").stdout)[
            "num_parallel"
        ]
        != 99
    )
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        ".cmoc/gt/ar/config.json"
    ]
    assert (
        json.loads(run_git(root, "show", ":.cmoc/gt/ar/config.json").stdout)[
            "num_parallel"
        ]
        == 99
    )


def test_doctor_preprocess_separates_repo_and_linked_worktree_repairs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`.cmoc/gu` は repo root、tracked runtime は current worktree で修復する。"""

    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-doctor"
    run_git(root, "worktree", "add", "-b", "linked-doctor", str(linked), "HEAD")
    monkeypatch.chdir(linked)

    result = run_doctor(linked)

    assert result.exit_code == 0
    assert not (linked / ".gitignore").exists()
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
            cwd=linked,
            check=False,
        ).returncode
        != 0
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
    assert not (root / ".cmoc" / "gt" / "ar" / "config.json").exists()
    assert list((root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl"))
    assert not (linked / ".cmoc" / "gu" / "ar" / "log" / "sub_command").exists()
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert (linked / ".cmoc" / "gt" / "ar" / "config.json").exists()
    assert f"- repo_root: `{root}`" in result.stdout


def test_doctor_syncs_default_config_without_overwriting_human_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """既存 config の人間による値を保ったまま不足する既定値を同期することを検証する。"""

    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        json.dumps(
            {
                "num_parallel": 3,
                "codex": {
                    "model_providers": {"custom": {"settings": {}}},
                    "num_try_falv_recovery": 4,
                    "agent_calls": {
                        "build_tui_launch_tui_parameter": {
                            "model_provider": "custom",
                            "model": "CUSTOM",
                            "reasoning_effort": "CUSTOM-EFFORT",
                        }
                    },
                    "model": {"minimum": {"model": "LEGACY"}},
                    "reasoning_effort": {"low": "LEGACY"},
                },
            }
        )
        + "\n"
    )
    monkeypatch.chdir(root)

    run_doctor(root)
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model_providers"] == {
        "codex": {"settings": {}},
        "custom": {"settings": {}},
    }
    assert data["codex"]["agent_calls"]["build_tui_launch_tui_parameter"] == {
        "model_provider": "custom",
        "model": "CUSTOM",
        "reasoning_effort": "CUSTOM-EFFORT",
    }
    default_call = CmocConfig().codex.agent_calls[
        "build_indexing_index_entry_parameter"
    ]
    assert data["codex"]["agent_calls"][
        "build_indexing_index_entry_parameter"
    ] == {
        "model_provider": default_call.model_provider,
        "model": default_call.model,
        "reasoning_effort": default_call.reasoning_effort,
    }
    assert "num_try_falv_recovery" not in data["codex"]
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

    doctor_module.run_doctor_preprocess(root)

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

    doctor_module.run_doctor_preprocess(root)

    assert run_git(root, "show", "HEAD:.agents/.gitkeep").stdout == "human content\n"
    assert gitkeep.read_text() == "human content\n"
    assert run_git(root, "status", "--short").stdout == ""


def test_doctor_restores_missing_tracked_gitkeep(tmp_path: Path) -> None:
    """tracked な `.agents/.gitkeep` の unstaged deletion を復元する。"""

    root = make_repo(tmp_path)
    doctor_module.run_doctor_preprocess(root)
    gitkeep = root / ".agents" / ".gitkeep"
    gitkeep.unlink()

    doctor_module.run_doctor_preprocess(root)

    assert gitkeep.read_text() == ""
    assert run_git(root, "status", "--short").stdout == ""


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
        doctor_module.run_doctor_preprocess(root)

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
