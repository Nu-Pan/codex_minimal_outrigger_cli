from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

import typer

from acp.builder.indexing.index_entry import build_indexing_index_entry_parameter
from basic.acp import AgentCallParameter
from cmoc_runtime import (
    CmocError,
    file_sha256,
    is_binary,
    is_git_ignored,
    load_config,
    require_clean_worktree,
    run_git,
    text_sha256,
    work_root,
)


CodexExec = Callable[..., object]


def cmoc_indexing_impl(
    initial_status: str | None = None,
    codex_exec: CodexExec | None = None,
) -> None:
    """現在の work root に対して INDEX.md の maintenance を実行する。"""
    root = work_root()
    require_clean_worktree(root, initial_status)
    updated = update_indexes(root, codex_exec)
    commit_index_updates(root, updated)
    typer.echo(f"# cmoc indexing\n- updated_index_count: `{len(updated)}`")


def run_indexing_preflight(root: Path, codex_exec: CodexExec) -> None:
    commit_index_updates(root, update_indexes(root, codex_exec))


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
    dirs = indexable_directories(root)
    dirs.append(root)
    dirs.sort(key=lambda p: len(p.relative_to(root).parts), reverse=True)
    updated: list[Path] = []
    for directory in dirs:
        existing_entries = parse_index_entries(directory / "INDEX.md")
        entries = []
        missing_children: list[tuple[Path, str]] = []
        for child in indexable_children(root, directory):
            digest = index_target_hash(root, child)
            existing_entry = existing_entries.get(child.name)
            if existing_entry and existing_entry["hash"] == digest:
                entries.append(existing_entry["text"])
            else:
                entries.append(None)
                missing_children.append((child, digest))
        if missing_children:
            config = load_config(root)
            with ThreadPoolExecutor(max_workers=max(1, config.num_parallel)) as executor:
                generated_entries = list(
                    executor.map(
                        lambda item: build_index_entry(
                            root, item[0], digest=item[1], codex_exec=codex_exec
                        ),
                        missing_children,
                    )
                )
            generated_iter = iter(generated_entries)
            entries = [entry if entry is not None else next(generated_iter) for entry in entries]
        content = "\n\n".join(entries)
        if content:
            content += "\n"
        index_path = directory / "INDEX.md"
        if not index_path.exists() or index_path.read_text() != content:
            index_path.write_text(content)
            updated.append(index_path)
    return updated


def indexable_directories(root: Path) -> list[Path]:
    """INDEX.md 配置対象 directory を、除外 directory 配下へ降りずに列挙する。"""
    dirs: list[Path] = []
    stack = [root]
    while stack:
        directory = stack.pop()
        for child in sorted(directory.iterdir(), key=lambda p: p.name, reverse=True):
            if not child.is_dir() or child.name.startswith("."):
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
    for idx, line in enumerate(lines):
        if line == "## hash":
            hash_lines = [
                candidate.strip() for candidate in lines[idx + 1 :] if candidate.strip()
            ]
            if not hash_lines:
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
        if is_root_memo(root, child):
            continue
        if is_git_ignored(root, child) or (child.is_file() and is_binary(child)):
            continue
        children.append(child)
    return children


def is_root_memo(root: Path, path: Path) -> bool:
    """INDEX.md 対象から除外する `<work-root>/memo` 配下か判定する。"""
    memo = (root / "memo").resolve()
    resolved = path.resolve()
    return resolved == memo or memo in resolved.parents


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
    result = codex_exec(
        build_indexing_index_entry_parameter(path, content),
        root=root,
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
        parts.append(f"{'dir' if child.is_dir() else 'file'}\0{child.relative_to(root)}\0{child_hash}\n")
    return text_sha256("".join(parts))


def render_index_entry(root: Path, path: Path, entry: dict | None = None, digest: str | None = None) -> str:
    """Structured Output から INDEX.md entry Markdown を生成する。"""
    entry = entry or {}
    digest = digest or index_target_hash(root, path)
    rel = path.relative_to(root)
    summary = entry_list(entry, "summary", [f"`{rel}` の INDEX.md エントリーです。"])
    read_this_when = entry_list(entry, "read_this_when", [f"`{rel}` の内容を確認する必要があるとき。"])
    do_not_read_this_when = entry_list(entry, "do_not_read_this_when", ["より具体的な下位ファイルを直接読むべき対象が分かっているとき。"])
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


def entry_list(entry: dict, key: str, fallback: list[str]) -> list[str]:
    """Structured Output の list[str] 項目を fallback 付きで取り出す。"""
    value = entry.get(key)
    if isinstance(value, list) and all(isinstance(item, str) for item in value) and value:
        return value
    return fallback
