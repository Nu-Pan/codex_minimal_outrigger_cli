"""`commons.indexing` の INDEX entry と traversal の直接テストをまとめる。

render/parse/update_indexes の入力検証、hash 再利用、directory traversal、並列生成を
CLI lifecycle から分離して検証する。根拠は
`{{work-root}}/oracle/doc/app_spec/indexing.md`、
`{{work-root}}/oracle/doc/app_spec/sub_command/indexing.md`、
`{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.json`、
`{{work-root}}/oracle/src/oracle/prompt_builder/parts/index_entry_standard.py`。
"""

import json
import threading
from collections.abc import Callable
from pathlib import Path

import pytest
from _codex_support import setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import make_repo

import cmoc_runtime
import commons.indexing as indexing_common
import commons.runtime_codex_preflight as codex_preflight
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)


def _render_test_entry(root: Path, path: Path, digest: str | None = None) -> str:
    return indexing_common.render_index_entry(
        root,
        path,
        {
            "summary": [path.name],
            "read_this_when": [path.name],
            "do_not_read_this_when": [path.name],
        },
        digest=digest,
    ).rstrip()


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
            "unexpected text",
            "## Summary",
            "- valid summary",
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
        [
            "# `README.md`",
            "",
            "## Summary",
            "- valid summary",
            "broken continuation",
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
        [
            "# `README.md`",
            "",
            "## Summary",
            "- valid summary",
            "",
            "## Read this when",
            "- read README.md",
            "",
            "## Do not read this when",
            "- skip README.md",
            "",
            "## hash",
            "- {digest}",
            "broken hash line",
            "",
        ],
        [
            "# `README.md`",
            "",
            "## Summary",
            "- valid summary",
            "",
            "## Read this when",
            "- read README.md",
            "",
            "## Do not read this when",
            "- skip README.md",
            "",
            "## hash",
            "- {digest}",
            "- 0000000000000000000000000000000000000000000000000000000000000000",
            "",
        ],
    ],
)
def test_update_indexes_regenerates_malformed_fresh_hash_entry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, entry_lines: list[str]
) -> None:
    """malformed な fresh hash entry を再生成する。"""
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
        """INDEX entry 生成結果を固定する fake。"""
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
        {
            "summary": ["summary"],
            "read_this_when": ["read"],
            "do_not_read_this_when": [1],
        },
        {
            "summary": ["summary"],
            "read_this_when": ["read"],
            "do_not_read_this_when": ["skip"],
            "extra": ["ignored"],
        },
    ],
)
def test_render_index_entry_rejects_schema_mismatched_entries(
    tmp_path: Path, entry: dict[str, object] | None
) -> None:
    """schema と一致しない INDEX entry を拒否する。"""
    root = make_repo(tmp_path)
    readme = root / "README.md"

    with pytest.raises(cmoc_runtime.CmocError):
        indexing_common.render_index_entry(root, readme, entry)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("summary", []),
        ("summary", [""]),
        ("summary", ["   "]),
        ("summary", ["line1\nline2"]),
        ("summary", ["line1\rline2"]),
        ("read_this_when", []),
        ("read_this_when", [""]),
        ("do_not_read_this_when", []),
        ("do_not_read_this_when", ["\t"]),
    ],
)
def test_render_index_entry_rejects_empty_blank_or_multiline_semantic_items(
    tmp_path: Path, key: str, value: list[str]
) -> None:
    """空白または複数行の semantic item を拒否する。"""
    root = make_repo(tmp_path)
    readme = root / "README.md"
    entry = {
        "summary": ["summary"],
        "read_this_when": ["read"],
        "do_not_read_this_when": ["skip"],
    }
    entry[key] = value

    with pytest.raises(cmoc_runtime.CmocError):
        indexing_common.render_index_entry(root, readme, entry)


def test_update_indexes_creates_empty_index_for_empty_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """空ディレクトリにも空の INDEX.md を作成する。"""
    root = make_repo(tmp_path)
    empty_dir = root / "empty"
    empty_dir.mkdir()
    cmoc_runtime.sync_config(root)

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        """INDEX entry 生成結果を固定する fake。"""
        return _render_test_entry(update_root, path, digest)

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    # {{work-root}}/oracle/doc/app_spec/indexing.md requires INDEX.md placement
    # per target directory, even when there are no indexable children.
    assert empty_dir / "INDEX.md" in updated
    assert (empty_dir / "INDEX.md").read_text() == ""


def test_update_indexes_generates_sibling_entries_in_stable_render_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """兄弟ファイルの INDEX entry を安定した順序で生成する。"""
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    (docs / "a.txt").write_text("a\n")
    (docs / "b.txt").write_text("b\n")
    cmoc_runtime.sync_config(root)
    calls: list[str] = []

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        """INDEX entry 生成結果を固定する fake。"""
        if path.parent == docs:
            calls.append(path.name)
        return _render_test_entry(update_root, path, digest)

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert docs / "INDEX.md" in updated
    assert sorted(calls) == ["a.txt", "b.txt"]
    rendered = (docs / "INDEX.md").read_text()
    assert rendered.index("# `a.txt`") < rendered.index("# `b.txt`")


def test_update_indexes_propagates_subcommand_logger_to_codex_workers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """並列 worker の Codex event を親サブコマンドログへ記録する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    root = make_repo(tmp_path)
    cmoc_runtime.sync_config(root)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            'output.write_text(\'{"summary": ["summary"], "read_this_when": ["read"], "do_not_read_this_when": ["skip"]}\')',
            'print(\'{"type":"turn.completed"}\')',
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    logger = SubcommandLogger(root, "indexing")
    token = set_current_subcommand_logger(logger)

    try:
        indexing_common.update_indexes(root, codex_preflight.run_codex_exec)
    finally:
        reset_current_subcommand_logger(token)

    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert codex_events
    assert all(event["status"] == "succeeded" for event in codex_events)


def test_update_indexes_generates_non_ancestor_indexes_in_parallel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """祖先関係のない INDEX 更新を並列に実行する。"""
    root = make_repo(tmp_path)
    first = root / "first"
    second = root / "second"
    first.mkdir()
    second.mkdir()
    (first / "a.txt").write_text("a\n")
    (second / "b.txt").write_text("b\n")
    cmoc_runtime.sync_config(root)
    calls: list[tuple[str, str]] = []
    sibling_barrier = threading.Barrier(2)

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        """INDEX entry 生成結果を固定する fake。"""
        if path.parent in {first, second}:
            calls.append((path.parent.name, path.name))
            sibling_barrier.wait(timeout=2)
        return _render_test_entry(update_root, path, digest)

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert first / "INDEX.md" in updated
    assert second / "INDEX.md" in updated
    assert sorted(calls) == [("first", "a.txt"), ("second", "b.txt")]


def test_update_indexes_avoids_worker_threads_during_pushd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """隔離 run の cwd lock と INDEX worker が循環待ちにならない。"""
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    (docs / "a.txt").write_text("a\n")
    (docs / "b.txt").write_text("b\n")
    cmoc_runtime.sync_config(root)
    calling_thread = threading.get_ident()
    call_threads: list[int] = []

    class FakeCodexResult:
        """INDEX entry 用の固定 Structured Output を返す。"""

        output_json = {
            "summary": ["summary"],
            "read_this_when": ["read"],
            "do_not_read_this_when": ["skip"],
        }

    class RejectingThreadPoolExecutor:
        """pushd 中に worker pool が作られた時点で回帰を検出する。"""

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError("pushd must not submit INDEX work to another thread")

    def fake_codex_exec(_parameter: object, **_kwargs: object) -> FakeCodexResult:
        call_threads.append(threading.get_ident())
        return FakeCodexResult()

    monkeypatch.setattr(
        indexing_common, "ThreadPoolExecutor", RejectingThreadPoolExecutor
    )

    with cmoc_runtime.pushd(root):
        updated = indexing_common.update_indexes(root, fake_codex_exec)

    assert docs / "INDEX.md" in updated
    assert call_threads
    assert set(call_threads) == {calling_thread}


def test_update_indexes_indexes_nested_memo_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """nested memo directory の INDEX 方針を検証する。"""
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
        """INDEX entry 生成結果を固定する fake。"""
        return _render_test_entry(update_root, path, digest)

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert root_memo / "INDEX.md" not in updated
    assert not (root_memo / "INDEX.md").exists()
    assert root_memo_child / "INDEX.md" not in updated
    assert not (root_memo_child / "INDEX.md").exists()
    assert nested_memo / "INDEX.md" in updated
    assert (nested_memo / "INDEX.md").is_file()
    assert "# `memo`" in (root / "docs" / "INDEX.md").read_text()


def test_update_indexes_skips_directory_symlink_cycle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """directory symlink cycle を辿らずに indexing する。"""
    root = make_repo(tmp_path)
    (root / "loop").symlink_to(root, target_is_directory=True)
    cmoc_runtime.sync_config(root)
    calls: list[Path] = []

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec: Callable[..., object] | None = None,
    ) -> str:
        """INDEX entry 生成結果を固定する fake。"""
        calls.append(path)
        return _render_test_entry(update_root, path, digest)

    monkeypatch.setattr(indexing_common, "build_index_entry", fake_build_index_entry)

    updated = indexing_common.update_indexes(root)

    assert root / "INDEX.md" in updated
    assert root / "loop" not in calls
    assert "# `loop`" not in (root / "INDEX.md").read_text()
