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

正本仕様: `{{work-root}}/oracle/doc/app_spec/doctor_preprocess.md`,
`{{work-root}}/oracle/doc/app_spec/sub_command/doctor.md`。
"""

import json
import multiprocessing
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _cli_support import run_doctor
from _git_support import make_repo, run_git

import commons.runtime_doctor as doctor_module


def hold_doctor_lock(lock_path: Path, ready: Connection, release: Connection) -> None:
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
    run_doctor(root)

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
        != 0
    )


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
        target=hold_doctor_lock,
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
    ) -> None:
        """repair commit の失敗を再現する。"""
        raise RuntimeError("repair commit failure")

    monkeypatch.setattr(doctor_module, "_commit_doctor_repairs_from_head", fail_commit)

    with pytest.raises(RuntimeError, match="repair commit failure"):
        doctor_module.run_doctor_preprocess(root)

    assert run_git(root, "write-tree").stdout.strip() == expected_index_tree
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "staged.txt"
    ]


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
    assert json.loads(config_path.read_text())["codex"]["model_providers"] == {}
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
    assert check_ignore.returncode != 0


def test_doctor_preprocess_targets_current_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree 起点の doctor が repository と worktree の状態を正しく修復することを検証する。"""

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
        run_git(
            linked, "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"
        ).returncode
        == 0
    )
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert run_git(root, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
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
                    "model": {
                        "mainstream": {
                            "model_provider": "custom",
                            "model": "CUSTOM",
                        }
                    },
                },
            }
        )
        + "\n"
    )
    monkeypatch.chdir(root)

    run_doctor(root)
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model_providers"] == {"custom": {"settings": {}}}
    assert data["codex"]["model"]["mainstream"] == {
        "model_provider": "custom",
        "model": "CUSTOM",
    }
    assert data["codex"]["model"]["efficiency"] == {
        "model_provider": None,
        "model": "gpt-5.6-luna",
    }
    assert "num_try_falv_recovery" not in data["codex"]
    assert data["codex"]["reasoning_effort"]["low"] == "low"
    assert data["codex"]["reasoning_effort"]["xhigh"] == "xhigh"
    assert data["codex"]["reasoning_effort"]["max"] == "max"
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
