"""INDEX.md メンテナンス処理のテスト。"""

import errno
import hashlib
import json
import os
import socket
import subprocess
import threading
from multiprocessing import Process
from pathlib import Path
from time import monotonic
from time import sleep

import pytest
from pytest import MonkeyPatch

from commons.errors import CmocError
from commons.indexing import _INDEX_OUTPUT_SCHEMA
from commons.indexing import _index_maintenance_lock_path
from commons.indexing import _locked_index_maintenance
from commons.indexing import find_index_inconsistencies
from commons.indexing import is_maintained_index_path
from commons.indexing import is_maintained_index_path_at_commit
from commons.indexing import maintain_indexes
from commons.subcommand_log import log_event
from commons.subcommand_log import subcommand_log

_EMPTY_FILE_DIGEST = hashlib.sha256(b"cmoc-index-empty-file\0").hexdigest()
_EMPTY_DIRECTORY_DIGEST = hashlib.sha256(
    b"cmoc-index-empty-directory\0"
).hexdigest()


def test_maintain_indexes_generates_routing_entries_and_respects_gitignore(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md は直下項目ごとに生成され、gitignore 対象は除外される。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "content")
    codex_prompts: list[str] = []
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の Structured Output を返す fake Codex CLI。"""
        codex_prompts.append(str(args[1]))
        codex_kwargs.append(kwargs)
        return json.dumps(
            {
                "summary": ["kept summary"],
                "read_this_when": ["read kept"],
                "do_not_read_this_when": ["skip kept"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "# `kept.txt`" in content
    assert "kept summary" in content
    assert "cmoc-index-kind" not in content
    assert "# `ignored.txt`" not in content
    readme_path = json.dumps((repo / "README.md").resolve().as_posix())
    kept_path = json.dumps((repo / "kept.txt").resolve().as_posix())
    assert any(readme_path in prompt for prompt in codex_prompts)
    assert any(kept_path in prompt for prompt in codex_prompts)
    assert not any("`README.md` の `INDEX.md`" in prompt for prompt in codex_prompts)
    assert not any("`kept.txt` の `INDEX.md`" in prompt for prompt in codex_prompts)
    assert codex_kwargs
    assert all(
        kwargs["output_schema"] == _INDEX_OUTPUT_SCHEMA
        for kwargs in codex_kwargs
    )
    assert all(kwargs["model"] == "gpt-5.4-mini" for kwargs in codex_kwargs)
    assert all(
        kwargs["reasoning_effort"] == "medium" for kwargs in codex_kwargs
    )


def test_maintain_indexes_prompts_with_recoverable_json_path_for_symbols(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """prompt の対象 path は記号を INDEX token 化せず JSON string で渡す。"""
    repo = _init_repo(tmp_path)
    target = repo / "a%b`c.txt"
    target.write_text("symbols\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "symbol path")
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成 prompt を記録する fake Codex CLI。"""
        del kwargs
        codex_prompts.append(str(args[1]))
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    expected_json_path = json.dumps(target.resolve().as_posix())

    assert changed is True
    assert "# `a%25b%60c.txt`" in content
    assert any(expected_json_path in prompt for prompt in codex_prompts)
    assert not any("a%25b%60c.txt" in prompt for prompt in codex_prompts)


def test_maintain_indexes_refreshes_stale_oracle_routing_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """古い oracles/app_specs 導線は hash が同じでも実在 path へ更新する。"""
    repo = _init_repo(tmp_path)
    (repo / "README.md").write_text(
        "基本ワークフローは oracles/app_specs/usage.md を参照\n",
        encoding="utf-8",
    )
    current_usage = repo / "oracles/docs/app_specs/usage.md"
    current_usage.parent.mkdir(parents=True)
    current_usage.write_text("usage\n", encoding="utf-8")
    readme_digest = hashlib.sha256((repo / "README.md").read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- README summary",
                "",
                "## Read this when",
                "",
                "- 基本ワークフローの入口として `oracles/app_specs/usage.md` を読むとき",
                "",
                "## Do not read this when",
                "",
                "- skip",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "stale index")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """古い path を返す INDEX 生成応答も実在 path へ正規化される。"""
        del args, kwargs
        return json.dumps(
            {
                "summary": ["README summary"],
                "read_this_when": [
                    "基本ワークフローの入口として `oracles/app_specs/usage.md` を読むとき"
                ],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "oracles/app_specs/" not in content
    assert "oracles/docs/app_specs/usage.md" in content


@pytest.mark.parametrize(
    ("relative_path", "expected"),
    [
        ("INDEX.md", True),
        ("docs/INDEX.md", True),
        ("docs/memo/INDEX.md", True),
        ("memo/INDEX.md", False),
        ("memo/sub/INDEX.md", False),
        ("oracles/INDEX.md", True),
        ("oracles/nested/INDEX.md", True),
        (".cmoc/INDEX.md", False),
        (".agents/INDEX.md", False),
        (".git/INDEX.md", False),
        ("build/INDEX.md", True),
        ("tmp/INDEX.md", True),
        ("__pycache__/INDEX.md", True),
        ("docs/readme.md", False),
    ],
)
def test_is_maintained_index_path_matches_index_placement_rules(
    tmp_path: Path,
    relative_path: str,
    expected: bool,
) -> None:
    """INDEX.md path 判定は配置対象外 root を許可しない。"""
    repo = _init_repo(tmp_path)

    assert is_maintained_index_path(repo, relative_path) is expected


def test_is_maintained_index_path_allows_ignored_index_file(
    tmp_path: Path,
) -> None:
    """INDEX.md file 自体が ignored でも配置対象 directory なら許可する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("INDEX.md\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore index")

    assert is_maintained_index_path(repo, "INDEX.md") is True


def test_is_maintained_index_path_at_commit_allows_ignored_index_file(
    tmp_path: Path,
) -> None:
    """commit 時点判定も INDEX.md file 自身の ignore では除外しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "INDEX.md\ndocs/INDEX.md\n",
        encoding="utf-8",
    )
    docs = repo / "docs"
    docs.mkdir()
    (docs / "target.txt").write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "docs/target.txt")
    _git(repo, "commit", "-m", "ignore index")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    assert (
        is_maintained_index_path_at_commit(repo, commit_hash, "INDEX.md")
        is True
    )
    assert (
        is_maintained_index_path_at_commit(repo, commit_hash, "docs/INDEX.md")
        is True
    )


def test_is_maintained_index_path_at_commit_respects_nested_gitignore(
    tmp_path: Path,
) -> None:
    """commit 時点判定は下位 `.gitignore` の directory 除外も使う。"""
    repo = _init_repo(tmp_path)
    docs = repo / "docs"
    ignored = docs / "ignored"
    kept = docs / "kept"
    ignored.mkdir(parents=True)
    kept.mkdir()
    (docs / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    (ignored / "target.txt").write_text("ignored\n", encoding="utf-8")
    (kept / "target.txt").write_text("kept\n", encoding="utf-8")
    _git(
        repo,
        "add",
        "-f",
        "docs/.gitignore",
        "docs/ignored/target.txt",
        "docs/kept/target.txt",
    )
    _git(repo, "commit", "-m", "add nested gitignore")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    assert (
        is_maintained_index_path_at_commit(
            repo,
            commit_hash,
            "docs/ignored/INDEX.md",
        )
        is False
    )
    assert (
        is_maintained_index_path_at_commit(
            repo,
            commit_hash,
            "docs/kept/INDEX.md",
        )
        is True
    )


def test_is_maintained_index_path_at_commit_uses_commit_tree_for_symlink_prune(
    tmp_path: Path,
) -> None:
    """snapshot の通常 directory は現 worktree で symlink でも配置対象にする。"""
    repo = _init_repo(tmp_path)
    docs = repo / "docs"
    docs.mkdir()
    (docs / "target.txt").write_text("target\n", encoding="utf-8")
    _git(repo, "add", "docs/target.txt")
    _git(repo, "commit", "-m", "add docs directory")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (docs / "target.txt").unlink()
    docs.rmdir()
    os.symlink("elsewhere", docs, target_is_directory=True)

    assert (
        is_maintained_index_path_at_commit(repo, commit_hash, "docs/INDEX.md")
        is True
    )


def test_is_maintained_index_path_at_commit_excludes_snapshot_symlink_ancestor(
    tmp_path: Path,
) -> None:
    """snapshot の symlink ancestor は現 worktree で通常 directory でも除外する。"""
    repo = _init_repo(tmp_path)
    docs = repo / "docs"
    os.symlink("elsewhere", docs, target_is_directory=True)
    _git(repo, "add", "docs")
    _git(repo, "commit", "-m", "add docs symlink")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    docs.unlink()
    docs.mkdir()
    (docs / "target.txt").write_text("target\n", encoding="utf-8")

    assert (
        is_maintained_index_path_at_commit(repo, commit_hash, "docs/INDEX.md")
        is False
    )


def test_maintain_indexes_reports_directory_iteration_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """直下項目列挙の I/O failure は no-op にせず CmocError にする。"""
    repo = _init_repo(tmp_path)
    original_iterdir = Path.iterdir

    def failing_iterdir(path: Path) -> object:
        """repo root の直下列挙だけを失敗させる。"""
        if path == repo:
            raise OSError("cannot list directory")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", failing_iterdir)

    with pytest.raises(CmocError) as error:
        maintain_indexes(repo)

    assert "ファイルシステム操作へ失敗" in error.value.message
    assert "直下項目列挙" in error.value.detail
    assert str(repo) in error.value.detail


def test_maintain_indexes_reports_directory_walk_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """配置対象 directory 探索の I/O failure は silent skip にしない。"""
    repo = _init_repo(tmp_path)
    blocked = repo / "blocked"

    def failing_walk(path: Path, *args: object, **kwargs: object) -> object:
        """Path.walk の on_error 経由で探索失敗を通知する。"""
        assert path == repo
        on_error = kwargs.get("on_error")
        assert on_error is not None
        on_error(
            OSError(errno.EACCES, "Permission denied", blocked.as_posix())
        )
        return iter(())

    monkeypatch.setattr(Path, "walk", failing_walk)

    with pytest.raises(CmocError) as error:
        maintain_indexes(repo)

    assert "ファイルシステム操作へ失敗" in error.value.message
    assert "directory tree の探索" in error.value.detail
    assert str(blocked) in error.value.detail


def test_maintain_indexes_reports_index_replace_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md 置換の I/O failure は成功相当の no-op にしない。"""
    repo = _init_repo(tmp_path)
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "target")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    def failing_replace(source: object, destination: object) -> None:
        """INDEX.md 置換を失敗させる。"""
        raise OSError(f"cannot replace {destination}")

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)
    monkeypatch.setattr("commons.indexing.os.replace", failing_replace)

    with pytest.raises(CmocError) as error:
        maintain_indexes(repo)

    assert "INDEX.md の置換" in error.value.detail
    assert str(repo / "INDEX.md") in error.value.detail


def test_maintain_indexes_reports_file_hash_read_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """hash 計算用の file read failure は対象除外にせず CmocError にする。"""
    repo = _init_repo(tmp_path)
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "target")
    original_read_bytes = Path.read_bytes

    def failing_read_bytes(path: Path) -> bytes:
        """対象ファイルの hash read だけを失敗させる。"""
        if path == target:
            raise OSError("cannot read target")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", failing_read_bytes)

    with pytest.raises(CmocError) as error:
        maintain_indexes(repo)

    assert "ファイル内容の hash 計算" in error.value.detail
    assert str(target) in error.value.detail


def test_maintain_indexes_reports_binary_detection_open_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """binary 判定の open failure は binary 扱いで除外しない。"""
    repo = _init_repo(tmp_path)
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "target")
    original_open = Path.open

    def failing_open(path: Path, *args: object, **kwargs: object) -> object:
        """対象ファイルの binary 判定 open だけを失敗させる。"""
        if path == target and args[:1] == ("rb",):
            raise OSError("cannot open target")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", failing_open)

    with pytest.raises(CmocError) as error:
        maintain_indexes(repo)

    assert "バイナリ判定" in error.value.detail
    assert str(target) in error.value.detail


def test_maintain_indexes_generates_entries_in_parallel_with_stable_order(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """同じ INDEX.md 内の entry 生成は並列化しつつ辞書順を保つ。"""
    repo = _init_repo(tmp_path)
    for name in ["a.txt", "b.txt", "c.txt"]:
        (repo / name).write_text(f"{name}\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "parallel entries")
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_codex(*args: object, **kwargs: object) -> str:
        """同時実行数を記録する fake Codex CLI。"""
        nonlocal active, max_active
        purpose = str(kwargs["purpose"])
        with lock:
            active += 1
            max_active = max(max_active, active)
        sleep(0.05)
        with lock:
            active -= 1
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert max_active > 1
    assert content.index("# `README.md`") < content.index("# `a.txt`")
    assert content.index("# `a.txt`") < content.index("# `b.txt`")
    assert content.index("# `b.txt`") < content.index("# `c.txt`")


def test_maintain_indexes_parallel_entries_record_worker_codex_events(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """並列 INDEX entry 生成の worker 内 Codex 呼び出しも JSONL に残す。"""
    repo = _init_repo(tmp_path)
    for name in ["a.txt", "b.txt"]:
        (repo / name).write_text(f"{name}\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "parallel log events")

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
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    with subcommand_log(repo):
        changed = maintain_indexes(repo)

    log_file = next((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    events = [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").splitlines()
    ]
    codex_events = [
        event for event in events if event["event"] == "codex_exec_call"
    ]
    assert changed is True
    assert len(codex_events) >= 2
    assert all(event["returncode"] == 0 for event in codex_events)


def test_maintain_indexes_parallelizes_unrelated_indexes_at_same_depth(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """祖先・子孫関係にない同 depth の INDEX.md は並列処理する。"""
    repo = _init_repo(tmp_path)
    left = repo / "left"
    right = repo / "right"
    left.mkdir()
    right.mkdir()
    (left / "note.txt").write_text("left\n", encoding="utf-8")
    (right / "note.txt").write_text("right\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "sibling indexes")
    active_sibling_entries = 0
    max_active_sibling_entries = 0
    lock = threading.Lock()

    def fake_codex(*args: object, **kwargs: object) -> str:
        """同 depth sibling の entry 生成の重なりを記録する。"""
        nonlocal active_sibling_entries, max_active_sibling_entries
        purpose = str(kwargs["purpose"])
        is_sibling_entry = purpose in {
            "INDEX entry 生成 left/note.txt",
            "INDEX entry 生成 right/note.txt",
        }
        if is_sibling_entry:
            with lock:
                active_sibling_entries += 1
                max_active_sibling_entries = max(
                    max_active_sibling_entries,
                    active_sibling_entries,
                )
            sleep(0.05)
            with lock:
                active_sibling_entries -= 1
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    assert changed is True
    assert max_active_sibling_entries > 1


def test_index_maintenance_lock_serializes_processes(
    tmp_path: Path,
) -> None:
    """INDEX メンテナンス用 lock は別プロセスの同時実行を直列化する。"""
    repo = _init_repo(tmp_path)
    ready_path = tmp_path / "holder-ready"
    release_path = tmp_path / "holder-release"
    acquired_path = tmp_path / "contender-acquired"
    holder = Process(
        target=_hold_index_maintenance_lock,
        args=(repo, ready_path, release_path),
    )
    contender = Process(
        target=_record_index_maintenance_lock_acquisition,
        args=(repo, acquired_path),
    )

    try:
        holder.start()
        _wait_until_path_exists(ready_path)
        contender.start()
        sleep(0.2)

        assert not acquired_path.exists()

        release_path.write_text("release\n", encoding="utf-8")
        holder.join(5)
        contender.join(5)

        assert holder.exitcode == 0
        assert contender.exitcode == 0
        assert acquired_path.read_text(encoding="utf-8") == "acquired\n"
    finally:
        for process in (holder, contender):
            if process.is_alive():
                process.terminate()
                process.join(5)


def test_index_maintenance_lock_path_preserves_git_stdout_spaces(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """git 管理 directory path の空白は lock path でも保持する。"""
    common_dir_text = " /tmp/cmoc common dir "

    def fake_run(
        *args: object,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """空白を含む git stdout を返す。"""
        return subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=f"{common_dir_text}\n",
            stderr="",
        )

    monkeypatch.setattr("commons.indexing.subprocess.run", fake_run)

    lock_path = _index_maintenance_lock_path(tmp_path)

    assert lock_path == Path(common_dir_text) / "cmoc-index-maintenance.lock"


def test_index_maintenance_lock_path_is_shared_by_linked_worktrees(
    tmp_path: Path,
) -> None:
    """linked worktree でも同一 repository の lock path を共有する。"""
    repo = _init_repo(tmp_path)
    linked_worktree = tmp_path / "linked-worktree"
    _git(
        repo,
        "worktree",
        "add",
        "-b",
        "linked-worktree-test",
        linked_worktree.as_posix(),
        "HEAD",
    )

    assert _index_maintenance_lock_path(linked_worktree) == (
        _index_maintenance_lock_path(repo)
    )


def test_index_maintenance_lock_path_fails_without_git_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """git 管理 directory を取得できない場合は誤った fallback を使わない。"""

    def fake_run(
        *args: object,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """git rev-parse の失敗を返す。"""
        return subprocess.CompletedProcess(
            args=[],
            returncode=128,
            stdout="",
            stderr="fatal: not a git repository\n",
        )

    monkeypatch.setattr("commons.indexing.subprocess.run", fake_run)

    with pytest.raises(CmocError) as error:
        _index_maintenance_lock_path(tmp_path)

    assert "git-common-dir" in error.value.detail
    assert str(tmp_path / ".git" / "cmoc-index-maintenance.lock") not in (
        error.value.detail
    )


def test_maintain_indexes_uses_local_exclude_but_ignores_external_excludes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX 生成対象は `.git/info/exclude` を反映し、global/system は無視する。"""
    global_ignore = tmp_path / "global-excludes"
    global_ignore.write_text("/global-only.txt\n", encoding="utf-8")
    global_config = tmp_path / "global-gitconfig"
    global_config.write_text(
        f"[core]\n\texcludesFile = {global_ignore.as_posix()}\n",
        encoding="utf-8",
    )
    external_ignore = tmp_path / "system-excludes"
    external_ignore.write_text("/system-only.txt\n", encoding="utf-8")
    system_config = tmp_path / "system-gitconfig"
    system_config.write_text(
        f"[core]\n\texcludesFile = {external_ignore.as_posix()}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", global_config.as_posix())
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", system_config.as_posix())

    repo = _init_repo(tmp_path)
    (repo / ".git" / "info" / "exclude").write_text(
        "/local-only.txt\n",
        encoding="utf-8",
    )
    (repo / ".gitignore").write_text("# repo rules only\n", encoding="utf-8")
    (repo / "global-only.txt").write_text("kept\n", encoding="utf-8")
    (repo / "local-only.txt").write_text("kept\n", encoding="utf-8")
    (repo / "system-only.txt").write_text("kept\n", encoding="utf-8")

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

    changed = maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "# `global-only.txt`" in content
    assert "# `local-only.txt`" not in content
    assert "# `system-only.txt`" in content


def test_maintain_indexes_respects_gitignore_for_newline_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """newline を含む path でも gitignore 判定の path 境界を保つ。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored*\n", encoding="utf-8")
    kept = repo / "kept\nname.txt"
    ignored = repo / "ignored\nname.txt"
    kept.write_text("kept\n", encoding="utf-8")
    ignored.write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "kept\nname.txt")
    _git(repo, "commit", "-m", "newline paths")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成対象を記録する fake Codex CLI。"""
        purposes.append(str(kwargs["purpose"]))
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `kept%0Aname.txt`" in content
    assert "# `ignored%0Aname.txt`" not in content
    assert all("ignored\nname.txt" not in purpose for purpose in purposes)

    def fail_codex(*args: object, **kwargs: object) -> str:
        """newline path の最新 INDEX では呼ばれてはいけない。"""
        raise AssertionError(
            "codex exec should not be called for current newline path INDEX"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    assert maintain_indexes(repo) is False


def test_maintain_indexes_round_trips_non_utf8_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """非 UTF-8 filename でも INDEX 生成と再利用を停止せず行う。"""
    repo = _init_repo(tmp_path)
    raw_dir_name = b"bad_\xff_dir"
    raw_file_name = b"note_\xfe.txt"
    raw_dir = os.fsencode(repo) + b"/" + raw_dir_name
    os.mkdir(raw_dir)
    _write_bytes_file(raw_dir + b"/" + raw_file_name, b"note\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "non utf8 paths")
    prompts: list[str] = []
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """非 UTF-8 path の安全な表示だけを受け取る fake Codex CLI。"""
        prompts.append(str(args[1]))
        purposes.append(str(kwargs["purpose"]))
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    root_index = (repo / "INDEX.md").read_text(encoding="utf-8")
    bad_dir = repo / os.fsdecode(raw_dir_name)
    child_index = (bad_dir / "INDEX.md").read_text(encoding="utf-8")
    bad_dir_digest = _directory_digest(repo, bad_dir)
    note_digest = hashlib.sha256(b"note\n").hexdigest()

    assert changed is True
    assert "# `bad_%FF_dir`" in root_index
    assert "# `note_%FE.txt`" in child_index
    assert f"- {bad_dir_digest}" in root_index
    assert f"- {note_digest}" in child_index
    assert any("bad_%FF_dir" in purpose for purpose in purposes)
    assert any(
        json.dumps(bad_dir.resolve().as_posix()) in prompt
        for prompt in prompts
    )
    assert not any(_has_surrogate(text) for text in [*prompts, *purposes])

    def fail_codex(*args: object, **kwargs: object) -> str:
        """非 UTF-8 path の最新 INDEX では呼ばれてはいけない。"""
        raise AssertionError(
            "codex exec should not be called for current non-UTF-8 path INDEX"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    assert maintain_indexes(repo) is False


def test_maintain_indexes_creates_empty_index_for_empty_directory(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """空の配置対象ディレクトリにも空の INDEX.md を新規作成する。"""
    repo = _init_repo(tmp_path)
    empty = repo / "empty"
    empty.mkdir()

    def fake_codex(*args: object, **kwargs: object) -> str:
        """root INDEX の既存ファイル向け Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    assert changed is True
    assert (empty / "INDEX.md").exists()
    assert (empty / "INDEX.md").read_text(encoding="utf-8") == ""


def test_maintain_indexes_replaces_non_utf8_empty_directory_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """空の配置対象ディレクトリでも非 UTF-8 INDEX.md は置き換える。"""
    repo = _init_repo(tmp_path)
    empty = repo / "empty"
    empty.mkdir()
    (empty / "INDEX.md").write_bytes(b"# broken\n\xff\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "broken empty directory index")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """root INDEX の empty entry 向け Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    assert changed is True
    assert (empty / "INDEX.md").read_text(encoding="utf-8") == ""
    index_mode = _git(repo, "ls-files", "-s", "empty/INDEX.md").stdout.split()
    assert index_mode[0] == "100644"


def test_maintain_indexes_skips_excluded_index_roots(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """除外 root 配下には INDEX.md を作成・更新しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    nested_oracle = oracle_root / "nested"
    nested_oracle.mkdir(parents=True)
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (nested_oracle / "more.md").write_text("more\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracles")

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

    changed = maintain_indexes(repo, excluded_index_roots=["oracles"])

    assert changed is True
    assert (repo / "INDEX.md").exists()
    assert not (oracle_root / "INDEX.md").exists()
    assert not (nested_oracle / "INDEX.md").exists()


def test_maintain_indexes_creates_missing_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """oracles 直下の INDEX.md 欠落は通常の配置対象として補正する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_docs = oracle_root / "docs"
    oracle_docs.mkdir(parents=True)
    (oracle_docs / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/docs/spec.md")
    _git(repo, "commit", "-m", "oracles without index")

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

    changed = maintain_indexes(repo)

    assert changed is True
    assert (oracle_root / "INDEX.md").exists()
    assert (oracle_docs / "INDEX.md").exists()
    assert "# `docs`" in (oracle_root / "INDEX.md").read_text(encoding="utf-8")


def test_maintain_indexes_repairs_oracle_tree_indexes_until_check_is_clean(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """missing/stale/extra が混在する oracles INDEX を修復後検査まで通す。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    app_specs = oracle_root / "docs" / "app_specs"
    app_oracles = app_specs / "oracles"
    schema_oracles = (
        oracle_root
        / "schemas"
        / "structured_output"
        / "review"
        / "oracles"
    )
    app_oracles.mkdir(parents=True)
    schema_oracles.mkdir(parents=True)
    (app_specs / "indexing.md").write_text("indexing spec\n", encoding="utf-8")
    (app_oracles / "enumerate.md").write_text("oracle spec\n", encoding="utf-8")
    (schema_oracles / "enumerate_findings.json").write_text(
        '{"type":"object"}\n',
        encoding="utf-8",
    )
    zero_digest = "0" * 64
    (oracle_root / "INDEX.md").write_text(
        _index_entry("docs", zero_digest),
        encoding="utf-8",
    )
    (app_specs / "INDEX.md").write_text(
        _index_entry("oracles.md", zero_digest),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "stale oracle tree indexes")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        purpose = str(kwargs["purpose"])
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    assert changed is True
    assert find_index_inconsistencies(repo, index_roots=["oracles"]) == []
    root_index = (oracle_root / "INDEX.md").read_text(encoding="utf-8")
    app_specs_index = (app_specs / "INDEX.md").read_text(encoding="utf-8")
    assert "# `docs`" in root_index
    assert "# `schemas`" in root_index
    assert "# `oracles`" in app_specs_index
    assert "# `oracles.md`" not in app_specs_index
    assert (schema_oracles / "INDEX.md").exists()


def test_find_index_inconsistencies_reports_missing_extra_and_stale_entries(
    tmp_path: Path,
) -> None:
    """INDEX 検査は更新せずに entry の過不足と hash 不一致を返す。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_docs = oracle_root / "docs"
    oracle_docs.mkdir(parents=True)
    (oracle_docs / "spec.md").write_text("spec\n", encoding="utf-8")
    zero_digest = "0" * 64
    (oracle_root / "INDEX.md").write_text(
        _index_entry("ghost.md", zero_digest),
        encoding="utf-8",
    )
    (oracle_docs / "INDEX.md").write_text(
        _index_entry("spec.md", zero_digest),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "stale oracle indexes")

    inconsistencies = find_index_inconsistencies(
        repo,
        index_roots=["oracles"],
    )

    assert "oracles/INDEX.md: missing entry for docs" in inconsistencies
    assert "oracles/INDEX.md: extra entry for ghost.md" in inconsistencies
    assert "oracles/docs/INDEX.md: stale hash for spec.md" in inconsistencies
    assert not (repo / "oracles" / "docs" / "spec.md").read_text(
        encoding="utf-8"
    ).startswith("#")


def test_maintain_indexes_places_indexes_in_generated_named_directories(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """build/tmp/__pycache__ も gitignore 対象でなければ配置対象にする。"""
    repo = _init_repo(tmp_path)
    build = repo / "build"
    tmp = repo / "tmp"
    pycache = repo / "__pycache__"
    build.mkdir()
    tmp.mkdir()
    pycache.mkdir()
    (build / "artifact.txt").write_text("artifact\n", encoding="utf-8")
    (tmp / "scratch.txt").write_text("scratch\n", encoding="utf-8")
    (pycache / "module.pyc.txt").write_text("pycache\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "generated dirs")

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

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `build`" in content
    assert "# `tmp`" in content
    assert "# `__pycache__`" in content
    assert (build / "INDEX.md").exists()
    assert (tmp / "INDEX.md").exists()
    assert (pycache / "INDEX.md").exists()


def test_maintain_indexes_excludes_gitignored_generated_named_directories(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """build/tmp/__pycache__ は .gitignore 対象の場合だけ配置対象から除外する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "build/\ntmp/\n__pycache__/\n",
        encoding="utf-8",
    )
    for name in ("build", "tmp", "__pycache__"):
        directory = repo / name
        directory.mkdir()
        (directory / "artifact.txt").write_text("artifact\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore generated dirs")

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

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `build`" not in content
    assert "# `tmp`" not in content
    assert "# `__pycache__`" not in content
    assert not (repo / "build" / "INDEX.md").exists()
    assert not (repo / "tmp" / "INDEX.md").exists()
    assert not (repo / "__pycache__" / "INDEX.md").exists()


def test_maintain_indexes_excludes_symlink_entries(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """symlink は repo 外混入や循環回避のため目次対象から除外する。"""
    repo = _init_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "external.txt").write_text("external\n", encoding="utf-8")
    (repo / "real.txt").write_text("real\n", encoding="utf-8")
    (repo / "linked-file.txt").symlink_to(outside / "external.txt")
    (repo / "linked-dir").symlink_to(outside, target_is_directory=True)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "symlinks")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成対象を記録する fake Codex CLI。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `real.txt`" in content
    assert "# `linked-file.txt`" not in content
    assert "# `linked-dir`" not in content
    assert not any("linked-file.txt" in purpose for purpose in purposes)
    assert not any("linked-dir" in purpose for purpose in purposes)


def test_maintain_indexes_excludes_special_files(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """通常ファイルでもディレクトリでもない entry は安全に除外する。"""
    repo = _init_repo(tmp_path)
    socket_path = repo / "control.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(str(socket_path))
        (repo / "real.txt").write_text("real\n", encoding="utf-8")
        _git(repo, "add", "real.txt")
        _git(repo, "commit", "-m", "real file")
        purposes: list[str] = []

        def fake_codex(*args: object, **kwargs: object) -> str:
            """INDEX 生成対象を記録する fake Codex CLI。"""
            purpose = str(kwargs["purpose"])
            purposes.append(purpose)
            return json.dumps(
                {
                    "summary": [purpose],
                    "read_this_when": ["read"],
                    "do_not_read_this_when": ["skip"],
                }
            )

        monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

        changed = maintain_indexes(repo)
        content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `real.txt`" in content
    assert "# `control.sock`" not in content
    assert not any("control.sock" in purpose for purpose in purposes)


def test_maintain_indexes_replaces_index_symlink_without_touching_target(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """既存 INDEX.md が symlink でもリンク先を書き換えない。"""
    repo = _init_repo(tmp_path)
    outside = tmp_path / "outside-index.md"
    outside.write_text("outside sentinel\n", encoding="utf-8")
    index_path = repo / "INDEX.md"
    index_path.symlink_to(outside)
    _git(repo, "add", "INDEX.md")
    _git(repo, "commit", "-m", "index symlink")

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

    changed = maintain_indexes(repo)
    content = index_path.read_text(encoding="utf-8")

    assert changed is True
    assert outside.read_text(encoding="utf-8") == "outside sentinel\n"
    assert not index_path.is_symlink()
    assert index_path.is_file()
    assert "# `README.md`" in content
    assert _git(repo, "ls-files", "-s", "INDEX.md").stdout.split()[0] == (
        "100644"
    )


def test_maintain_indexes_ignores_symlink_contents_in_directory_hash(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """directory hash は symlink 先の内容変更に影響されない。"""
    repo = _init_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    external = outside / "external.txt"
    external.write_text("before\n", encoding="utf-8")
    folder = repo / "folder"
    folder.mkdir()
    (folder / "real.txt").write_text("real\n", encoding="utf-8")
    (folder / "external-link.txt").symlink_to(external)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "folder symlink")

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
    maintain_indexes(repo)
    external.write_text("after\n", encoding="utf-8")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """symlink 先の変更だけでは呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for symlink target changes"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)
    folder_index = (folder / "INDEX.md").read_text(encoding="utf-8")

    assert changed is False
    assert "# `real.txt`" in folder_index
    assert "# `external-link.txt`" not in folder_index


def test_maintain_indexes_excludes_cyclic_symlink_from_directory_hash(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """循環 symlink は辿らず、通常項目だけを INDEX 化する。"""
    repo = _init_repo(tmp_path)
    folder = repo / "folder"
    folder.mkdir()
    (folder / "real.txt").write_text("real\n", encoding="utf-8")
    (folder / "loop").symlink_to(folder, target_is_directory=True)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "cyclic symlink")

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

    changed = maintain_indexes(repo)
    folder_index = (folder / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `real.txt`" in folder_index
    assert "# `loop`" not in folder_index


def test_maintain_indexes_excludes_non_utf8_binary_without_nul(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """NUL を含まない非 UTF-8 バイナリも INDEX 目次対象から除外する。"""
    repo = _init_repo(tmp_path)
    binary = repo / "image.bin"
    binary.write_bytes(bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x7F, 0x01]))
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "binary")

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

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `kept.txt`" in content
    assert "# `image.bin`" not in content


def test_maintain_indexes_excludes_binary_after_initial_chunk(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """先頭付近が UTF-8 でも後続に NUL があるファイルは目次対象から除外する。"""
    repo = _init_repo(tmp_path)
    binary = repo / "late_binary.dat"
    binary.write_bytes(b"a" * 4096 + b"\0")
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "late binary")

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

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `kept.txt`" in content
    assert "# `late_binary.dat`" not in content


def test_maintain_indexes_keeps_utf8_when_sample_ends_mid_character(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """sample 末尾で UTF-8 文字が途中切れしてもテキストとして扱う。"""
    repo = _init_repo(tmp_path)
    target = repo / "partial_boundary.md"
    target.write_bytes(b"a" * 4094 + "あ".encode("utf-8") + b"\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "utf8 boundary")

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

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `partial_boundary.md`" in content


def test_maintain_indexes_places_index_in_nested_memo_directory(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """配置除外の memo は repo root 直下だけに限定する。"""
    repo = _init_repo(tmp_path)
    nested_memo = repo / "docs" / "memo"
    nested_memo.mkdir(parents=True)
    (nested_memo / "note.md").write_text("note\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "nested memo")

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

    maintain_indexes(repo)

    assert (nested_memo / "INDEX.md").exists()


def test_maintain_indexes_regenerates_malformed_current_entry(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """hash が最新でも必須セクションが欠ける既存エントリは再生成する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "- stale summary",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "malformed index")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成されたことを識別できる Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["regenerated summary"],
                "read_this_when": ["read regenerated"],
                "do_not_read_this_when": ["skip regenerated"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "regenerated summary" in content
    assert "## Read this when" in content
    assert "## Do not read this when" in content


def test_maintain_indexes_regenerates_known_cmoc_command_typo(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """hash が最新でも既知の cmoc コマンド名 typo は再生成する。"""
    repo = _init_repo(tmp_path)
    target = repo / "apply_join.md"
    target.write_text("join spec\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `apply_join.md`",
                "",
                "## Summary",
                "",
                "- cmo apply fork からの合流仕様を扱います。",
                "",
                "## Read this when",
                "",
                "- apply join を確認するとき。",
                "",
                "## Do not read this when",
                "",
                "- unrelated.",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "stale command typo index")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成された routing 文を返す。"""
        return json.dumps(
            {
                "summary": ["cmoc apply fork からの合流仕様を扱います。"],
                "read_this_when": ["apply join を確認するとき。"],
                "do_not_read_this_when": ["unrelated."],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "cmo apply fork" not in content
    assert "cmoc apply fork" in content


def test_maintain_indexes_regenerates_stale_absolute_repository_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """hash が最新でも別 worktree の絶対 path は repo 相対 path へ更新する。"""
    repo = _init_repo(tmp_path)
    target = repo / "src/sub_commands/apply/join.py"
    target.parent.mkdir(parents=True)
    target.write_text("join implementation\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    stale_absolute_path = (
        tmp_path
        / "old-worktree"
        / "src/sub_commands/apply/join.py"
    ).as_posix()
    relative_path = "src/sub_commands/apply/join.py"
    (repo / "src/sub_commands/apply/INDEX.md").write_text(
        "\n".join(
            [
                "# `join.py`",
                "",
                "## Summary",
                "",
                f"- `{stale_absolute_path}` は `cmoc apply join` の本体です。",
                "",
                "## Read this when",
                "",
                f"- `{stale_absolute_path}` の merge 手順を確認するとき。",
                "",
                "## Do not read this when",
                "",
                "- unrelated.",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "stale absolute index path")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成時にも混入した絶対 path は正規化される。"""
        del args, kwargs
        return json.dumps(
            {
                "summary": [
                    f"`{stale_absolute_path}` は `cmoc apply join` の本体です。"
                ],
                "read_this_when": [
                    f"`{stale_absolute_path}` の merge 手順を確認するとき。"
                ],
                "do_not_read_this_when": ["unrelated."],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "src/sub_commands/apply/INDEX.md").read_text(
        encoding="utf-8"
    )

    assert changed is True
    assert stale_absolute_path not in content
    assert f"`{relative_path}` は `cmoc apply join` の本体です。" in content
    assert f"`{relative_path}` の merge 手順を確認するとき。" in content


def test_find_index_inconsistencies_keeps_relative_paths_and_root_placeholders_valid(
    tmp_path: Path,
) -> None:
    """相対 path や `<cmoc-root>/...` は古い絶対 path と誤判定しない。"""
    repo = _init_repo(tmp_path)
    (repo / "src").mkdir()
    target = repo / "src/tool.py"
    target.write_text("tool\n", encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "src/INDEX.md").write_text(
        "\n".join(
            [
                "# `tool.py`",
                "",
                "## Summary",
                "",
                "- `<cmoc-root>/src` と `src/tool.py` を案内します。",
                "",
                "## Read this when",
                "",
                "- `src/tool.py` の実装を確認するとき。",
                "",
                "## Do not read this when",
                "",
                "- `oracles/docs/app_specs/indexing.md` だけを読むとき。",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "relative index paths")

    content = (repo / "src/INDEX.md").read_text(encoding="utf-8")

    assert "`<cmoc-root>/src`" in content
    assert "`src/tool.py`" in content
    assert "`oracles/docs/app_specs/indexing.md`" in content
    assert "srcINDEX.md" not in content
    assert find_index_inconsistencies(repo, index_roots=["src"]) == []


def test_maintain_indexes_normalizes_known_cmoc_command_typo_in_generated_text(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """生成された routing 文の既知 command typo も INDEX.md へ残さない。"""
    repo = _init_repo(tmp_path)
    (repo / "apply_join.md").write_text(
        "cmo apply fork からの合流仕様を扱います。\n",
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "source command typo")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """仕様本文由来の typo を含む routing 文を返す。"""
        return json.dumps(
            {
                "summary": ["cmo apply fork からの合流仕様を扱います。"],
                "read_this_when": ["cmo apply join を確認するとき。"],
                "do_not_read_this_when": ["cmo apply 以外の仕様を見るとき。"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "cmo apply" not in content
    assert "cmoc apply fork" in content
    assert "cmoc apply join" in content


def test_maintain_indexes_regenerates_non_utf8_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """UTF-8 として読めない既存 INDEX.md は停止せず再生成する。"""
    repo = _init_repo(tmp_path)
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    (repo / "INDEX.md").write_bytes(b"# broken\n\xff\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "broken index")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成対象を記録できる Structured Output を返す。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `README.md`" in content
    assert "# `target.txt`" in content
    assert "INDEX entry 生成 README.md" in purposes
    assert "INDEX entry 生成 target.txt" in purposes


def test_maintain_indexes_retries_invalid_structured_output(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX 生成用 JSON の schema 不一致は run_codex_exec 側でリトライされる。"""
    repo = _init_repo(tmp_path)
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "content")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    state = tmp_path / "attempts.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -eq 1 ]; then",
                (
                    "  printf '%s\\n' > \"$LAST\" "
                    "'{\"content_hash\":\"abc\","
                    "\"summary\":\"not a list\","
                    "\"read_this_when\":[\"read\"],"
                    "\"do_not_read_this_when\":[\"skip\"]}'"
                ),
                "else",
                (
                    "  printf '%s\\n' > \"$LAST\" "
                    "'{\"summary\":[\"valid summary\"],"
                    "\"read_this_when\":[\"read\"],"
                    "\"do_not_read_this_when\":[\"skip\"]}'"
                ),
                "fi",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    changed = maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "valid summary" in content
    assert int(state.read_text(encoding="utf-8").strip()) >= 2


def test_maintain_indexes_does_not_call_codex_when_index_is_current(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md が最新なら機械的チェックだけで済ませ、Codex CLI を呼ばない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "- target summary",
                "",
                "## Read this when",
                "",
                "- read target",
                "",
                "## Do not read this when",
                "",
                "- skip target",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "content")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """最新 INDEX では呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for a fresh INDEX.md"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)

    assert changed is False


def test_maintain_indexes_does_not_call_codex_for_current_empty_entries(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """空 file/directory entry も最新なら Codex CLI を呼ばず再利用する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    empty_file = repo / "empty.txt"
    empty_file.write_bytes(b"")
    empty_dir = repo / "empty-dir"
    empty_dir.mkdir()
    (empty_dir / "INDEX.md").write_text("", encoding="utf-8")
    readme_digest = _file_digest(repo / "README.md")
    empty_file_digest = _file_digest(empty_file)
    empty_dir_digest = _directory_digest(repo, empty_dir)
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `empty-dir`",
                "",
                "## Summary",
                "",
                "- empty directory summary",
                "",
                "## Read this when",
                "",
                "- read empty directory",
                "",
                "## Do not read this when",
                "",
                "- skip empty directory",
                "",
                "## hash",
                "",
                f"- {empty_dir_digest}",
                "",
                "# `empty.txt`",
                "",
                "## Summary",
                "",
                "- empty file summary",
                "",
                "## Read this when",
                "",
                "- read empty file",
                "",
                "## Do not read this when",
                "",
                "- skip empty file",
                "",
                "## hash",
                "",
                f"- {empty_file_digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    original_content = (repo / "INDEX.md").read_text(encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "current empty entries")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """最新の空 entry では呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for current empty entries"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)

    assert changed is False
    assert (repo / "INDEX.md").read_text(encoding="utf-8") == original_content
    assert "cmoc-index-kind" not in original_content


def test_maintain_indexes_regenerates_entry_when_empty_file_becomes_directory(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """旧形式の空 file entry は空 directory への種別変更時に再生成する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target"
    target.write_bytes(b"")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    empty_digest = hashlib.sha256(b"").hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target`",
                "",
                "## Summary",
                "",
                "- old file summary",
                "",
                "## Read this when",
                "",
                "- read old file",
                "",
                "## Do not read this when",
                "",
                "- skip old file",
                "",
                "## hash",
                "",
                f"- {empty_digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old empty file index")

    target.unlink()
    target.mkdir()
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成対象を記録できる Structured Output を返す。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read regenerated"],
                "do_not_read_this_when": ["skip regenerated"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert purposes == ["INDEX entry 生成 target"]
    assert "- old file summary" not in content
    assert "- INDEX entry 生成 target" in content
    assert "cmoc-index-kind" not in content


def test_maintain_indexes_regenerates_entry_with_internal_kind_comment(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """仕様外の内部種別コメントを含む既存 entry は再生成する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "- old summary",
                "",
                "## Read this when",
                "",
                "- read old",
                "",
                "## Do not read this when",
                "",
                "- skip old",
                "",
                "## hash",
                "",
                f"- {digest}",
                "<!-- cmoc-index-kind: file -->",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "index with internal comment")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成されたことを識別できる Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["regenerated summary"],
                "read_this_when": ["read regenerated"],
                "do_not_read_this_when": ["skip regenerated"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "- old summary" not in content
    assert "- regenerated summary" in content
    assert "cmoc-index-kind" not in content


def test_maintain_indexes_round_trips_special_names_and_multiline_text(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """特殊文字を含む名前と説明文でも INDEX を再利用できる。"""
    repo = _init_repo(tmp_path)
    target = repo / "we`ird\n%.txt"
    target.write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "special file name")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """Markdown 境界に見える文字を含む Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["- first\n# `ghost`\nsecond"],
                "read_this_when": ["* read\r\nwhen"],
                "do_not_read_this_when": ["skip\twhen"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `we%60ird%0A%25.txt`" in content
    assert "# `we`ird" not in content
    assert "- first # `ghost` second" in content
    assert "- read when" in content
    assert "skip when" in content
    assert "- - first" not in content
    assert "- * read" not in content

    def fail_codex(*args: object, **kwargs: object) -> str:
        """特殊文字を含む最新 INDEX では呼ばれてはいけない。"""
        raise AssertionError(
            "codex exec should not be called for escaped current INDEX entries"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    assert maintain_indexes(repo) is False


def test_maintain_indexes_regenerates_parent_entry_after_child_rename(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """子の名前変更は親ディレクトリ hash を変え、親 entry を再生成する。"""
    repo = _init_repo(tmp_path)
    folder = repo / "folder"
    folder.mkdir()
    (folder / "before.txt").write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "nested content")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """呼び出し対象を記録できる Structured Output を返す。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)
    maintain_indexes(repo)

    purposes.clear()
    (folder / "before.txt").rename(folder / "after.txt")

    changed = maintain_indexes(repo)
    root_index = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "INDEX entry 生成 folder" in purposes
    assert "# `folder`" in root_index
    assert "- INDEX entry 生成 folder" in root_index


def test_maintain_indexes_propagates_nested_content_hash_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """深い leaf の内容変更は親 INDEX hash へ連鎖的に反映する。"""
    repo = _init_repo(tmp_path)
    parent = repo / "parent"
    child = parent / "child"
    child.mkdir(parents=True)
    leaf = child / "leaf.md"
    leaf.write_text("before\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "nested content")

    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """呼び出し対象を本文に入れ、再生成範囲を検証できるようにする。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)
    maintain_indexes(repo)

    purposes.clear()
    leaf.write_text("after\n", encoding="utf-8")

    changed = maintain_indexes(repo)
    leaf_digest = hashlib.sha256(leaf.read_bytes()).hexdigest()
    child_digest = _directory_digest(repo, child)
    parent_digest = _directory_digest(repo, parent)
    child_index = (child / "INDEX.md").read_text(encoding="utf-8")
    parent_index = (parent / "INDEX.md").read_text(encoding="utf-8")
    root_index = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert purposes == [
        "INDEX entry 生成 parent/child/leaf.md",
        "INDEX entry 生成 parent/child",
        "INDEX entry 生成 parent",
    ]
    assert f"- {leaf_digest}" in child_index
    assert f"- {child_digest}" in parent_index
    assert f"- {parent_digest}" in root_index


def test_maintain_indexes_reuses_current_index_with_empty_sections(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """schema 上有効な空配列由来の既存 INDEX は再生成しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "",
                "## Read this when",
                "",
                "",
                "## Do not read this when",
                "",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    original_content = (repo / "INDEX.md").read_text(encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "current empty index sections")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """空セクションの最新 INDEX では呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for empty INDEX sections"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)

    assert changed is False
    assert (repo / "INDEX.md").read_text(encoding="utf-8") == original_content


def test_maintain_indexes_commits_only_maintenance_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """自動コミットは INDEX.md などメンテナンス差分だけを対象にする。"""
    repo = _init_repo(tmp_path)
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    (repo / "user_work.txt").write_text("user work\n", encoding="utf-8")
    _git(repo, "add", "target.txt")
    _git(repo, "commit", "-m", "target")

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

    changed = maintain_indexes(repo)
    status = _git(repo, "status", "--porcelain").stdout
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "?? user_work.txt" in status
    assert "INDEX.md" in last_commit_paths
    assert "user_work.txt" not in last_commit_paths


def test_maintain_indexes_commits_ignored_new_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """ignored な新規 INDEX.md もメンテナンス差分として commit する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("INDEX.md\n", encoding="utf-8")
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "target.txt")
    _git(repo, "commit", "-m", "ignore index")

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

    changed = maintain_indexes(repo)
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "INDEX.md" in last_commit_paths
    assert _git(repo, "ls-files", "INDEX.md").stdout.strip() == "INDEX.md"


def test_maintain_indexes_stages_literal_index_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """特殊文字を含む INDEX.md path が別 path を巻き込まない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("docsX/\n", encoding="utf-8")
    literal_dir = repo / "docs*"
    ignored_dir = repo / "docsX"
    literal_dir.mkdir()
    ignored_dir.mkdir()
    (literal_dir / "target.txt").write_text("target\n", encoding="utf-8")
    (ignored_dir / "INDEX.md").write_text("user ignored\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "docs*/target.txt")
    _git(repo, "commit", "-m", "special path")

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

    changed = maintain_indexes(repo)
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "docs*/INDEX.md" in last_commit_paths
    assert "docsX/INDEX.md" not in last_commit_paths
    assert _git(repo, "ls-files", "docsX/INDEX.md").stdout.strip() == ""


def test_maintain_indexes_preserves_preexisting_staged_index_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """同じ INDEX.md の既存 staged-only 差分を自動 commit 後も残す。"""
    repo = _init_repo(tmp_path)
    target = repo / "target.txt"
    target.write_text("before\n", encoding="utf-8")
    _git(repo, "add", "target.txt")
    _git(repo, "commit", "-m", "target")

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

    maintain_indexes(repo)
    head_index = (repo / "INDEX.md").read_text(encoding="utf-8")
    (repo / "INDEX.md").write_text(
        "staged note\n" + head_index,
        encoding="utf-8",
    )
    _git(repo, "add", "INDEX.md")
    (repo / "INDEX.md").write_text(head_index, encoding="utf-8")
    target.write_text("after\n", encoding="utf-8")

    changed = maintain_indexes(repo)
    status = _git(repo, "status", "--porcelain").stdout
    staged_index = _git(repo, "diff", "--cached", "--", "INDEX.md").stdout
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "MM INDEX.md" in status
    assert "+staged note" in staged_index
    assert "INDEX.md" in last_commit_paths


def test_maintain_indexes_does_not_ensure_cmoc_ignore(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンスは `.cmoc` の ignore 保証を担当しない。"""
    repo = _init_repo(tmp_path)
    cmoc_log = repo / ".cmoc" / "log.txt"
    cmoc_log.parent.mkdir()
    cmoc_log.write_text("log\n", encoding="utf-8")
    _git(repo, "add", ".cmoc/log.txt")
    _git(repo, "commit", "-m", "tracked cmoc log")

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

    changed = maintain_indexes(repo)
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "ls-files", ".cmoc/log.txt").stdout.strip() == (
        ".cmoc/log.txt"
    )
    assert "INDEX.md" in last_commit_paths
    assert ".gitignore" not in last_commit_paths
    assert ".cmoc/log.txt" not in last_commit_paths


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


def _hold_index_maintenance_lock(
    repo: Path,
    ready_path: Path,
    release_path: Path,
) -> None:
    """テスト用に INDEX メンテナンス lock を保持する。"""
    with _locked_index_maintenance(repo):
        ready_path.write_text("ready\n", encoding="utf-8")
        while not release_path.exists():
            sleep(0.01)


def _record_index_maintenance_lock_acquisition(
    repo: Path,
    acquired_path: Path,
) -> None:
    """テスト用に INDEX メンテナンス lock の取得完了を記録する。"""
    with _locked_index_maintenance(repo):
        acquired_path.write_text("acquired\n", encoding="utf-8")


def _wait_until_path_exists(path: Path) -> None:
    """指定 path が作られるまで短時間待つ。"""
    deadline = monotonic() + 5
    while monotonic() < deadline:
        if path.exists():
            return
        sleep(0.01)
    raise AssertionError(f"{path} was not created")


def _write_bytes_file(path: bytes, content: bytes) -> None:
    """bytes path の通常ファイルへ bytes を書く。"""
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
    try:
        os.write(fd, content)
    finally:
        os.close(fd)


def _has_surrogate(value: str) -> bool:
    """文字列に surrogateescape 由来文字が残っているか判定する。"""
    return any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def _directory_digest(repo: Path, directory: Path) -> str:
    """テスト用に仕様の directory hash serialization を計算する。"""
    serialized_entries: list[str] = []
    for child in sorted(
        [
            path
            for path in directory.iterdir()
            if path.name != "INDEX.md" and not path.name.startswith(".")
        ],
        key=lambda path: path.relative_to(repo).as_posix(),
    ):
        entry_type = "directory" if child.is_dir() else "file"
        relative_path = child.relative_to(repo).as_posix()
        if child.is_dir():
            content_hash = _directory_digest(repo, child)
        else:
            content_hash = _file_digest(child)
        serialized_entries.append(
            (
                f"{entry_type}\0"
                f"{_directory_hash_relative_path(relative_path)}\0"
                f"{content_hash}\n"
            )
        )
    if not serialized_entries:
        return _EMPTY_DIRECTORY_DIGEST
    return hashlib.sha256(
        "".join(serialized_entries).encode("utf-8")
    ).hexdigest()


def _file_digest(path: Path) -> str:
    """テスト用に file hash を計算する。"""
    content = path.read_bytes()
    if not content:
        return _EMPTY_FILE_DIGEST
    return hashlib.sha256(content).hexdigest()


def _directory_hash_relative_path(value: str) -> str:
    """テスト用に directory hash の relative path 表現へ揃える。"""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return _encode_index_token_for_test(value)
    return value


def _encode_index_token_for_test(value: str) -> str:
    """テスト用に INDEX token と同じ可逆な 1 行 token を返す。"""
    encoded_parts: list[str] = []
    for character in value:
        codepoint = ord(character)
        if (
            character == "%"
            or character == "`"
            or codepoint < 0x20
            or codepoint == 0x7F
            or 0xD800 <= codepoint <= 0xDFFF
        ):
            encoded_parts.extend(
                f"%{byte:02X}" for byte in os.fsencode(character)
            )
        else:
            encoded_parts.append(character)
    return "".join(encoded_parts)


def _index_entry(name: str, digest: str) -> str:
    """テスト用の最小 INDEX entry を返す。"""
    return "\n".join(
        [
            f"# `{name}`",
            "",
            "## Summary",
            "",
            "- summary",
            "",
            "## Read this when",
            "",
            "- read",
            "",
            "## Do not read this when",
            "",
            "- skip",
            "",
            "## hash",
            "",
            f"- {digest}",
            "",
        ]
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
