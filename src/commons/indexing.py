import fcntl
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from acp.builder.indexing.index_entry import build_indexing_index_entry_parameter
from cmoc_runtime import (
    CmocError,
    file_sha256,
    is_binary,
    is_git_ignored,
    is_root_memo,
    load_config,
    repo_root,
    run_git,
    text_sha256,
)
from commons.runtime_codex_preflight import configure_indexing_preflight


CodexExec = Callable[..., object]
INDEX_ENTRY_KEYS = {"summary", "read_this_when", "do_not_read_this_when"}


@dataclass
class _IndexDirectoryPlan:
    directory: Path
    entries: list[str | None]
    missing_children: list[tuple[int, Path, str]]


def enable_indexing_preflight() -> None:
    """Codex 呼び出し前に indexing を走らせる preflight を登録する。"""
    configure_indexing_preflight(
        lambda root, codex_exec: run_indexing_preflight(root, codex_exec)
    )


def run_indexing_preflight(root: Path, codex_exec: CodexExec) -> None:
    """Codex 呼び出し前に INDEX.md を最新化し、必要な更新 commit を作る。"""
    with indexing_lock(root):
        commit_index_updates(root, update_indexes(root, codex_exec))


@contextmanager
def indexing_lock(root: Path) -> Iterator[None]:
    """repository ごとの INDEX.md 更新を直列化する排他 lock を保持する。"""
    lock_path = indexing_lock_path(root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def indexing_lock_path(root: Path) -> Path:
    """Git 管理領域内の indexing 用 lock file path を取得する。"""
    path = run_git(
        ["rev-parse", "--git-path", "cmoc-indexing.lock"], root
    ).stdout.strip()
    return root / path


def commit_index_updates(root: Path, updated: list[Path]) -> None:
    """INDEX.md の更新差分だけを indexing commit として保存する。"""
    index_paths = [str(path.relative_to(root)) for path in updated]
    if index_paths:
        run_git(["add", "--", *index_paths], root)
    if not index_paths:
        return
    diff = run_git(["diff", "--cached", "--quiet", "--", *index_paths], root, check=False)
    if diff.returncode == 1:
        run_git(["commit", "-m", "cmoc indexing", "--", *index_paths], root)


def update_indexes(root: Path, codex_exec: CodexExec | None = None) -> list[Path]:
    """INDEX.md を深い directory から順に検査・再生成する。"""
    config_root = repo_root(root)
    dirs = indexable_directories(root)
    dirs.append(root)
    updated: list[Path] = []
    dirs_by_depth: dict[int, list[Path]] = {}
    for directory in dirs:
        depth = len(directory.relative_to(root).parts)
        dirs_by_depth.setdefault(depth, []).append(directory)
    for depth in sorted(dirs_by_depth, reverse=True):
        plans = [
            _plan_index_directory(root, directory)
            for directory in dirs_by_depth[depth]
        ]
        missing = [(plan, item) for plan in plans for item in plan.missing_children]
        if missing:
            load_config(config_root)
            for plan, (index, child, digest) in missing:
                plan.entries[index] = build_index_entry(
                    root,
                    child,
                    digest=digest,
                    codex_exec=codex_exec,
                )
        for plan in plans:
            entries = [entry for entry in plan.entries if entry is not None]
            content = "\n\n".join(entries)
            if content:
                content += "\n"
            index_path = plan.directory / "INDEX.md"
            if not index_path.exists() or index_path.read_text() != content:
                index_path.write_text(content)
                updated.append(index_path)
    return updated


def _plan_index_directory(root: Path, directory: Path) -> _IndexDirectoryPlan:
    """既存 entry の再利用可否と生成対象を判定する。"""
    existing_entries = parse_index_entries(directory / "INDEX.md")
    entries: list[str | None] = []
    missing_children: list[tuple[int, Path, str]] = []
    for child in indexable_children(root, directory):
        digest = index_target_hash(root, child)
        existing_entry = existing_entries.get(child.name)
        if existing_entry and existing_entry["hash"] == digest:
            entries.append(existing_entry["text"])
        else:
            entries.append(None)
            missing_children.append((len(entries) - 1, child, digest))
    return _IndexDirectoryPlan(directory, entries, missing_children)


def indexable_directories(root: Path) -> list[Path]:
    """INDEX.md 配置対象 directory を、除外 directory 配下へ降りずに列挙する。"""
    dirs: list[Path] = []
    stack = [root]
    while stack:
        directory = stack.pop()
        for child in sorted(directory.iterdir(), key=lambda p: p.name, reverse=True):
            if not child.is_dir() or child.is_symlink() or child.name.startswith("."):
                continue
            if is_root_memo(root, child) or is_git_ignored(root, child):
                continue
            dirs.append(child)
            stack.append(child)
    return dirs


def parse_index_entries(index_path: Path) -> dict[str, dict[str, str]]:
    """既存 INDEX.md から entry 名、本文、hash を抽出する。"""
    if not index_path.exists():
        return {}
    entries: dict[str, dict[str, str]] = {}
    current_name: str | None = None
    current_lines: list[str] = []
    for line in index_path.read_text().splitlines():
        if line.startswith("# `") and line.endswith("`"):
            if current_name is not None:
                text = "\n".join(current_lines).rstrip()
                entries[current_name] = {
                    "text": text,
                    "hash": extract_valid_index_entry_hash(text, current_name),
                }
            current_name = line.removeprefix("# `").removesuffix("`")
            current_lines = [line]
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        text = "\n".join(current_lines).rstrip()
        entries[current_name] = {
            "text": text,
            "hash": extract_valid_index_entry_hash(text, current_name),
        }
    return entries


def extract_valid_index_entry_hash(entry_text: str, entry_name: str) -> str:
    """必須形式を満たす INDEX.md entry から hash 文字列を得る。"""
    lines = entry_text.splitlines()
    if not lines or lines[0] != f"# `{entry_name}`":
        return ""
    required_sections = [
        "## Summary",
        "## Read this when",
        "## Do not read this when",
        "## hash",
    ]
    section_positions = [
        lines.index(section) for section in required_sections if section in lines
    ]
    if len(section_positions) != len(required_sections) or section_positions != sorted(
        section_positions
    ):
        return ""
    # <work-root>/oracle/doc/app_spec/indexing.md defines an entry as title plus
    # fixed sections; preserving fresh malformed text here would skip regeneration.
    if any(line.strip() for line in lines[1 : section_positions[0]]):
        return ""
    for start, end in zip(section_positions[:3], section_positions[1:]):
        section_lines = [line.strip() for line in lines[start + 1 : end] if line.strip()]
        # <work-root>/oracle/doc/app_spec/indexing.md requires each entry
        # section to be bullet-only.
        if not section_lines or any(not line.startswith("- ") for line in section_lines):
            return ""
    for idx, line in enumerate(lines):
        if line == "## hash":
            hash_lines = [
                candidate.strip() for candidate in lines[idx + 1 :] if candidate.strip()
            ]
            if len(hash_lines) != 1:
                return ""
            hash_line = hash_lines[0]
            if hash_line.startswith("- "):
                digest = hash_line.removeprefix("- ").strip()
                if len(digest) == 64 and all(c in "0123456789abcdef" for c in digest):
                    return digest
    return ""


def indexable_children(root: Path, directory: Path) -> list[Path]:
    """directory 直下の INDEX.md 目次作成対象を列挙する。"""
    children: list[Path] = []
    for child in sorted(directory.iterdir(), key=lambda p: p.name):
        if child.name == "INDEX.md" or child.name.startswith("."):
            continue
        # <work-root>/oracle/doc/app_spec/indexing.md requires indexing
        # maintenance to finish before agent calls; symlink cycles cannot be
        # valid traversal targets for that contract.
        if child.is_symlink():
            continue
        if is_root_memo(root, child):
            continue
        if is_git_ignored(root, child) or (child.is_file() and is_binary(child)):
            continue
        children.append(child)
    return children


def build_index_entry(
    root: Path,
    path: Path,
    digest: str | None = None,
    codex_exec: CodexExec | None = None,
) -> str:
    """Codex CLI に対象 1 件の INDEX.md entry を生成させる。"""
    if codex_exec is None:
        raise CmocError(
            "INDEX.md entry 生成用の Codex 実行関数が指定されていません。",
            ["cmoc indexing を通常の CLI 経由で再実行してください。"],
            str(path),
        )
    content = target_content_for_indexing(path)
    log_root = repo_root(root)
    result = codex_exec(
        build_indexing_index_entry_parameter(path, content),
        # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
        # <work-root>/oracle/doc/app_spec/run_isolation.md
        # INDEX 更新対象は worktree root のまま、Codex のログ/state 保存先は
        # run worktree 側へ流れないよう repo root に固定する。
        root=log_root,
        cwd=root,
        config=load_config(log_root),
        purpose=f"indexing index entry for {path}",
    ).output_json
    return render_index_entry(root, path, result or {}, digest=digest).rstrip()


def target_content_for_indexing(path: Path) -> str:
    """INDEX entry 生成 prompt に渡す対象内容を取り出す。"""
    if path.is_file():
        return path.read_text(errors="ignore")
    index_path = path / "INDEX.md"
    if index_path.exists():
        return index_path.read_text(errors="ignore")
    return "\n".join(child.name for child in sorted(path.iterdir(), key=lambda p: p.name))


def index_target_hash(root: Path, path: Path) -> str:
    """INDEX.md entry の鮮度判定に使う対象 hash を計算する。"""
    if path.is_file():
        return file_sha256(path)
    parts = []
    for child in indexable_children(root, path):
        child_hash = index_target_hash(root, child)
        kind = "dir" if child.is_dir() else "file"
        parts.append(
            f"{kind}\0{child.relative_to(root)}\0{child_hash}\n"
        )
    return text_sha256("".join(parts))


def render_index_entry(
    root: Path,
    path: Path,
    entry: dict | None = None,
    digest: str | None = None,
) -> str:
    """Structured Output から INDEX.md entry Markdown を生成する。"""
    if not isinstance(entry, dict) or set(entry) != INDEX_ENTRY_KEYS:
        raise CmocError(
            "INDEX.md entry 生成結果が不正です。",
            ["cmoc indexing を再実行してください。"],
            f"{path.relative_to(root)}: entry の項目が schema と一致していません。",
        )
    digest = digest or index_target_hash(root, path)
    summary = entry_list(root, path, entry, "summary")
    read_this_when = entry_list(root, path, entry, "read_this_when")
    do_not_read_this_when = entry_list(root, path, entry, "do_not_read_this_when")
    return "\n".join(
        [
            f"# `{path.name}`",
            "",
            "## Summary",
            *[f"- {item}" for item in summary],
            "",
            "## Read this when",
            *[f"- {item}" for item in read_this_when],
            "",
            "## Do not read this when",
            *[f"- {item}" for item in do_not_read_this_when],
            "",
            "## hash",
            f"- {digest}",
            "",
        ]
    )


def entry_list(root: Path, path: Path, entry: dict | None, key: str) -> list[str]:
    """Structured Output の必須 list[str] 項目を検証して取り出す。"""
    value = entry.get(key) if isinstance(entry, dict) else None
    # <work-root>/oracle/doc/app_spec/indexing.md and
    # <work-root>/oracle/src/oracle/prompt_builder/parts/index_entry_standard.py
    # require bullet-only semantic entries that are useful before reading the target.
    if (
        isinstance(value, list)
        and value
        and all(
            isinstance(item, str)
            and item.strip()
            and "\n" not in item
            and "\r" not in item
            for item in value
        )
    ):
        return value
    raise CmocError(
        "INDEX.md entry 生成結果が不正です。",
        ["cmoc indexing を再実行してください。"],
        f"{path.relative_to(root)}: `{key}` は 1 件以上の 1 行文字列配列である必要があります。",
    )
