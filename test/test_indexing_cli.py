"""INDEX.md 生成・更新と conflict 解決の CLI 境界を検証する。

このファイルは 16,000 文字を超えるが、責務境界は indexing preflight と
indexing subcommand が routing document を更新する外部挙動に閉じている。
対象列挙、hash 再利用、Codex 生成、commit 条件、linked worktree、INDEX.md conflict
解決は同じ routing 更新ワークフローの観測点であり、分割すると fixture と git 状態の
読み取り文脈が分散する。現状は indexing CLI 回帰として一箇所に保つ方が凝集性が高い。
"""

import json
import subprocess
import threading
import time
from collections.abc import Callable
from pathlib import Path

import pytest
import cmoc_runtime
import commons.indexing as indexing_common
from basic.acp import AgentCallParameter, ModelClass

from _support import (
    current_branch,
    make_repo,
    run_git,
    runner,
)
from main import app
import sub_commands.apply.join as apply_module
import sub_commands.indexing as indexing_module


def test_resolve_index_conflicts_deletes_index_and_commits(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    home_branch = current_branch(root)
    (root / "INDEX.md").write_text("base\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    run_git(root, "switch", "-c", "side")
    (root / "INDEX.md").write_text("side\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "side index")
    run_git(root, "switch", home_branch)
    (root / "INDEX.md").write_text("home\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "home index")
    merge = subprocess.run(
        ["git", "merge", "--no-ff", "side"], cwd=root, text=True, capture_output=True
    )
    assert merge.returncode != 0

    resolved = apply_module.resolve_index_conflicts(root)

    assert resolved is True
    assert not (root / "INDEX.md").exists()
    assert (
        subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            cwd=root,
            text=True,
            capture_output=True,
        ).stdout.strip()
        == ""
    )
    assert "Merge branch 'side'" in run_git(root, "log", "-1", "--pretty=%B").stdout

def test_indexing_uses_codex_index_entry_builder_and_commits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        calls.append(kwargs["purpose"])
        assert parameter.structured_output_schema_path.name == "index_entry.json"
        return FakeCodexResult()

    monkeypatch.setattr(indexing_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls
    root_index = root / "INDEX.md"
    assert root_index.is_file()
    rendered = root_index.read_text()
    assert "generated summary" in rendered
    assert "generated read condition" in rendered
    assert "generated skip condition" in rendered
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert "cmoc indexing" in run_git(root, "log", "--oneline", "-1").stdout


def test_indexing_uninitialized_clean_repo_fails_with_subcommand_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "cmoc init を実行してから再実行してください。" in result.stdout
    assert "cmoc init を実行してから再実行してください。" not in result.stderr
    assert not (root / ".gitignore").exists()
    assert not (root / "INDEX.md").exists()
    log_path = next((root / ".cmoc" / "log" / "sub_command").glob("*.jsonl"))
    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert records[0]["event"] == "command_invoked"
    assert records[-1]["event"] == "command_finished"
    assert records[-1]["returncode"] == 1
    assert run_git(root, "status", "--short").stdout.strip() == "?? .cmoc/"


def test_indexing_targets_current_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    main_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    linked = root / ".cmoc" / "worktrees" / "indexing"
    run_git(root, "worktree", "add", "-b", "linked-indexing", str(linked), "HEAD")

    class FakeCodexResult:
        output_json = {
            "summary": ["linked summary"],
            "read_this_when": ["linked read condition"],
            "do_not_read_this_when": ["linked skip condition"],
        }

    monkeypatch.setattr(
        indexing_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (linked / "INDEX.md").is_file()
    assert not (root / "INDEX.md").exists()
    assert run_git(linked, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == main_head
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_indexing_rejects_dirty_current_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    linked = root / ".cmoc" / "worktrees" / "dirty-indexing"
    run_git(root, "worktree", "add", "-b", "dirty-indexing", str(linked), "HEAD")
    (linked / "README.md").write_text("# repo\n\nlinked change\n")
    head_before = run_git(linked, "rev-parse", "HEAD").stdout.strip()

    def fail_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        raise AssertionError("dirty linked worktree must stop before indexing")

    monkeypatch.setattr(indexing_module, "update_indexes", fail_update_indexes)
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "git 未コミット差分が存在します。" in result.stdout
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert run_git(linked, "rev-parse", "HEAD").stdout.strip() == head_before
    assert not (linked / "INDEX.md").exists()
    assert run_git(linked, "status", "--short").stdout == " M README.md\n"


def test_indexing_preflight_in_apply_worktree_uses_repo_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    config = cmoc_runtime.sync_config(root)
    config.codex.model[ModelClass.EFFICIENCY] = "CUSTOM-INDEXING-EFFICIENCY"
    cmoc_runtime.write_config(root / ".cmoc" / "config.json", config)
    apply_worktree = root / ".cmoc" / "worktrees" / "session" / "run"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "apply-indexing-config",
        str(apply_worktree),
        "HEAD",
    )
    seen_models: list[str] = []

    class FakeCodexResult:
        output_json = {
            "summary": ["summary"],
            "read_this_when": ["read"],
            "do_not_read_this_when": ["skip"],
        }

    def fake_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        seen_models.append(kwargs["config"].codex.model[ModelClass.EFFICIENCY])
        assert kwargs["root"] == root
        assert kwargs["cwd"] == apply_worktree
        return FakeCodexResult()

    indexing_common.run_indexing_preflight(apply_worktree, fake_codex_exec)

    assert seen_models
    assert set(seen_models) == {"CUSTOM-INDEXING-EFFICIENCY"}
    assert (apply_worktree / "INDEX.md").is_file()
    assert not (apply_worktree / ".cmoc" / "config.json").exists()


def test_indexing_skips_codex_when_existing_hashes_are_fresh(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0

    class FakeCodexResult:
        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    monkeypatch.setattr(
        indexing_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    first = runner.invoke(app, ["indexing"], catch_exceptions=False)
    assert first.exit_code == 0
    root_index_before = (root / "INDEX.md").read_text()
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()

    calls: list[str] = []

    def fail_if_called(parameter: AgentCallParameter, **kwargs: object) -> None:
        calls.append(kwargs["purpose"])
        raise AssertionError("fresh INDEX.md should not require Codex")

    monkeypatch.setattr(indexing_module, "run_codex_exec", fail_if_called)
    second = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert second.exit_code == 0
    assert calls == []
    assert (root / "INDEX.md").read_text() == root_index_before
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_commit_index_updates_commits_only_index_paths(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    index_path.write_text("# generated\n")
    (root / ".gitignore").write_text("/.cmoc/\n")

    indexing_common.commit_index_updates(root, [index_path])

    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.strip()
    assert committed_paths == "INDEX.md"
    assert run_git(root, "status", "--short").stdout.strip() == "?? .gitignore"


def test_indexing_rejects_existing_non_index_diff_without_index_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    (root / "README.md").write_text("# repo\n\nchanged\n")
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
    calls: list[Path] = []

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        calls.append(update_root)
        raise AssertionError("dirty cmoc indexing must stop before updating INDEX.md")

    monkeypatch.setattr(indexing_common, "update_indexes", fake_update_indexes)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "git 未コミット差分が存在します。" not in result.stderr
    assert calls == []
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert not (root / "INDEX.md").exists()
    assert run_git(root, "status", "--short").stdout == " M README.md\n"


def test_indexing_preflight_allows_existing_non_index_diff_and_commits_only_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    (root / "README.md").write_text("# repo\n\nchanged\n")

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    monkeypatch.setattr(indexing_common, "update_indexes", fake_update_indexes)

    indexing_common.run_indexing_preflight(root, lambda *args, **kwargs: None)

    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.splitlines()
    assert committed_paths == ["INDEX.md"]
    assert run_git(root, "status", "--short").stdout == " M README.md\n"


@pytest.mark.parametrize(
    "entry_lines",
    [
        [
            "# `README.md`",
            "",
            "## hash",
            "- {digest}",
            "",
        ],
        [
            "# `README.md`",
            "",
            "## Summary",
            "",
            "## Read this when",
            "- read README.md",
            "",
            "## Do not read this when",
            "- skip README.md",
            "",
            "## hash",
            "- {digest}",
            "",
        ],
    ],
)
def test_update_indexes_regenerates_malformed_fresh_hash_entry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, entry_lines: list[str]
) -> None:
    root = make_repo(tmp_path)
    cmoc_runtime.sync_config(root)
    readme = root / "README.md"
    digest = indexing_common.index_target_hash(root, readme)
    (root / "INDEX.md").write_text(
        "\n".join(line.format(digest=digest) for line in entry_lines)
    )

    calls: list[Path] = []

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        calls.append(path)
        return indexing_common.render_index_entry(
            update_root,
            path,
            {
                "summary": [f"generated {path.name}"],
                "read_this_when": [f"read {path.name}"],
                "do_not_read_this_when": [f"skip {path.name}"],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert root / "INDEX.md" in updated
    assert readme in calls
    rendered = (root / "INDEX.md").read_text()
    assert "generated README.md" in rendered
    assert "## Summary" in rendered
    assert "## Read this when" in rendered
    assert "## Do not read this when" in rendered


@pytest.mark.parametrize(
    "entry",
    [
        None,
        {},
        {"summary": ["summary"], "read_this_when": ["read"], "do_not_read_this_when": [1]},
    ],
)
def test_render_index_entry_rejects_missing_or_non_string_semantic_fields(
    tmp_path: Path, entry: dict[str, object] | None
) -> None:
    root = make_repo(tmp_path)
    readme = root / "README.md"

    with pytest.raises(cmoc_runtime.CmocError):
        indexing_common.render_index_entry(root, readme, entry)


@pytest.mark.parametrize(
    "entry",
    [
        {"summary": [], "read_this_when": ["read"], "do_not_read_this_when": ["skip"]},
        {"summary": [""], "read_this_when": ["read"], "do_not_read_this_when": ["skip"]},
        {"summary": ["   "], "read_this_when": ["read"], "do_not_read_this_when": ["skip"]},
        {"summary": ["summary"], "read_this_when": [], "do_not_read_this_when": ["skip"]},
        {"summary": ["summary"], "read_this_when": [""], "do_not_read_this_when": ["skip"]},
        {"summary": ["summary"], "read_this_when": ["read"], "do_not_read_this_when": []},
        {"summary": ["summary"], "read_this_when": ["read"], "do_not_read_this_when": ["\t"]},
    ],
)
def test_render_index_entry_rejects_empty_semantic_lists(
    tmp_path: Path, entry: dict[str, object]
) -> None:
    root = make_repo(tmp_path)
    readme = root / "README.md"

    with pytest.raises(cmoc_runtime.CmocError):
        indexing_common.render_index_entry(root, readme, entry)


def test_update_indexes_generates_sibling_entries_in_parallel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    (docs / "a.txt").write_text("a\n")
    (docs / "b.txt").write_text("b\n")
    cmoc_runtime.sync_config(root)
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        nonlocal active, max_active
        if path.parent == docs:
            with lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.05)
            with lock:
                active -= 1
        return indexing_common.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert docs / "INDEX.md" in updated
    assert max_active >= 2


def test_update_indexes_indexes_nested_memo_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    root_memo = root / "memo"
    root_memo_child = root_memo / "child"
    nested_memo = root / "docs" / "memo"
    root_memo_child.mkdir(parents=True)
    nested_memo.mkdir(parents=True)
    (root_memo / "private.txt").write_text("private\n")
    (root_memo_child / "deeper.txt").write_text("deeper\n")
    (nested_memo / "note.txt").write_text("note\n")
    cmoc_runtime.sync_config(root)

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        return indexing_common.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert root_memo / "INDEX.md" not in updated
    assert not (root_memo / "INDEX.md").exists()
    assert root_memo_child / "INDEX.md" not in updated
    assert not (root_memo_child / "INDEX.md").exists()
    assert nested_memo / "INDEX.md" in updated
    assert (nested_memo / "INDEX.md").is_file()
    assert "# `memo`" in (root / "docs" / "INDEX.md").read_text()
