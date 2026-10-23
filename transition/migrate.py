"""人間が手順書から実行する、一回限りの配置移設・パス更新・文書 ID の補助処理。"""

import argparse
import difflib
import hashlib
import json
import os
import posixpath
import re
import stat
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token

# receipt と旧パスの解釈に使うため、移設後も移設元の名前を保持する。
_MOVES = {"oracle/src": "reference/src", "oracle/doc": "spec"}
_RECEIPT = "transition/work/move.json"
_ID = re.compile(r"\[(DECI|SPEC)-([^\]\s]+)\]")
_HEADING_ID = re.compile(r"^\[(DECI|SPEC)-([^\]\s]+)\](?:\s|$)")
_ATX = re.compile(r"^( {0,3}#{1,6})([ \t]+|$)")
_PROTECTED = {".git", ".agents", ".codex", ".cmoc", "AGENTS.md"}
_PATH_TARGETS = (
    "spec",
    "reference",
    "decision",
    "src",
    "test",
    "bin",
    "README.md",
    "pyproject.toml",
    ".gitignore",
    "codex_minimal_outrigger_cli.code-workspace",
)
_PATH_EXCLUDED = _PROTECTED | {
    "memo",
    "transition",
    ".aws",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
_MARKDOWN_DESTINATION = re.compile(
    r"(?P<before>\]\([ \t]*|^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*)"
    r"(?P<target><[^<>\n]+>|[^\s<>()]+)(?=[ \t]*(?:[\"']|\)|$))",
    re.MULTILINE,
)
_OLD_PATH = re.compile(
    r"oracle[/\\]+(?:doc|src|test)\b"
    r"|[\"']oracle[\"']\s*(?:/|,|\+)\s*[\"'](?:doc|src|test)[\"']"
)


class MigrationError(Exception):
    """移行元・移行先を人間が確認する必要がある状態。"""


def _path(root: Path, relative: str) -> Path:
    # 固定配置先の途中にある symlink も追跡しない。
    path = root
    parts = Path(relative).parts
    for index, part in enumerate(parts):
        path /= part
        if path.is_symlink():
            raise MigrationError(f"Symlink is not supported: {path}")
        if index < len(parts) - 1 and path.exists() and not path.is_dir():
            raise MigrationError(f"Expected a parent directory: {path}")
    return path


def _entries(directory: Path, *, excluded: set[str] | None = None) -> list[Path]:
    # rename が保護対象や特殊ファイルを一緒に運ばないよう全体を先に確認する。
    if not directory.is_dir() or directory.is_symlink():
        raise MigrationError(f"Expected a regular directory: {directory}")
    entries: list[Path] = []
    for child in sorted(directory.iterdir()):
        if excluded is not None and child.name in excluded:
            continue
        mode = child.lstat().st_mode
        if child.name in _PROTECTED:
            raise MigrationError(f"Protected entry inside migration tree: {child}")
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise MigrationError(f"Special file or symlink is not supported: {child}")
        entries.append(child)
        if stat.S_ISDIR(mode):
            entries.extend(_entries(child, excluded=excluded))
    return entries


def _fingerprint(directory: Path) -> str:
    # 内容、相対 path、permission、空 directory を含めて移設前後を比較する。
    digest = hashlib.sha256()
    for path in [directory, *_entries(directory)]:
        metadata = [
            path.relative_to(directory).as_posix(),
            stat.S_IMODE(path.stat().st_mode),
            (
                "directory"
                if path.is_dir()
                else hashlib.sha256(path.read_bytes()).hexdigest()
            ),
        ]
        digest.update(json.dumps(metadata, ensure_ascii=True).encode("ascii") + b"\n")
    return digest.hexdigest()


def _check_unmapped_oracle(root: Path) -> None:
    # oracle/test 等を暗黙に別の所有区分へ割り当てない。
    oracle = _path(root, "oracle")
    if not oracle.exists():
        return
    if not oracle.is_dir():
        raise MigrationError(f"Expected a directory: {oracle}")
    for child in oracle.iterdir():
        if child.name in {"src", "doc"}:
            continue
        if child.name == "test" and not _entries(child):
            continue
        raise MigrationError(f"No migration destination is defined for: {child}")


def _load_receipt(root: Path) -> dict[str, str] | None:
    # receipt の path を移設指示として使わず、固定 mapping の fingerprint だけを読む。
    receipt = _path(root, _RECEIPT)
    if not receipt.exists():
        return None
    value = json.loads(receipt.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("version") != 1:
        raise MigrationError(f"Invalid move receipt: {receipt}")
    trees = value.get("trees")
    if not isinstance(trees, dict) or set(trees) != set(_MOVES):
        raise MigrationError(f"Invalid move receipt: {receipt}")
    fingerprints: dict[str, str] = {}
    for source, fingerprint in trees.items():
        if not isinstance(fingerprint, str) or not re.fullmatch(
            r"[0-9a-f]{64}", fingerprint
        ):
            raise MigrationError(f"Invalid move fingerprint: {source}")
        fingerprints[source] = fingerprint
    return fingerprints


def _move_plan(root: Path) -> tuple[dict[str, str], list[tuple[Path, Path]]]:
    # 全組合せの確認が終わるまで、directory 作成も rename も行わない。
    _check_unmapped_oracle(root)
    receipt = _load_receipt(root)
    fingerprints: dict[str, str] = {}
    pending: list[tuple[Path, Path]] = []
    for source_name, target_name in _MOVES.items():
        source, target = _path(root, source_name), _path(root, target_name)
        if source.exists() and not target.exists():
            location = source
            pending.append((source, target))
        elif receipt is not None and not source.exists() and target.exists():
            location = target
        else:
            raise MigrationError(
                f"Expected one source or a receipted target: {source} -> {target}"
            )
        fingerprint = _fingerprint(location)
        if receipt is not None and fingerprint != receipt[source_name]:
            raise MigrationError(f"Tree changed since move started: {location}")
        fingerprints[source_name] = fingerprint
    return fingerprints, pending


def _plan(root: Path) -> None:
    # 移設済み部分も同じ検査で確認し、未完了の rename を表示する。
    _, pending = _move_plan(root)
    for source, target in pending:
        print(f"MOVE {source.relative_to(root)} -> {target.relative_to(root)}")
    if not pending:
        print("Layout already moved; source contents verified.")


def _move(root: Path) -> None:
    # 中断後も同じ内容から再開できるよう、rename より先に receipt を確定する。
    fingerprints, pending = _move_plan(root)
    receipt = _path(root, _RECEIPT)
    if not receipt.exists():
        receipt.parent.mkdir(parents=True, exist_ok=True)
        with receipt.open("x", encoding="utf-8") as stream:
            json.dump({"version": 1, "trees": fingerprints}, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    for source, target in pending:
        # 単独実行を前提とするが、既存の移設先を上書きしない。
        _path(root, target.relative_to(root).as_posix())
        if target.exists():
            raise MigrationError(f"Destination appeared during move: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
    for relative in ("oracle/test", "oracle"):
        path = _path(root, relative)
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    _verify_move(root)


def _verify_move(root: Path) -> None:
    # この検査は移設直後用であり、その後の人間による reference 編集とは分ける。
    if _load_receipt(root) is None:
        raise MigrationError("No move receipt exists.")
    _, pending = _move_plan(root)
    if pending:
        raise MigrationError(
            "Move is incomplete; rerun the move command before editing files."
        )
    print("Move verified: paths, contents and permissions match the receipt.")
    print("This verifies relocation only, not the new cmoc behavior.")


def _documents(root: Path, kind: str) -> list[Path]:
    # 移行用の採番・検査は明示された文書 tree に限定する。
    directory = _path(root, kind)
    if kind == "decision" and not directory.exists():
        return []
    documents = [
        path for path in _entries(directory) if path.is_file() and path.suffix == ".md"
    ]
    if not documents and kind != "decision":
        raise MigrationError(f"No Markdown documents found: {directory}")
    return documents


def _parse(path: Path) -> tuple[str, list[Token]]:
    # fence、inline code、setext 見出しの区別には既存の Markdown parser を使う。
    with path.open(encoding="utf-8", newline="") as stream:
        content = stream.read()
    return content, MarkdownIt().parse(content)


def _heading_ids(tokens: list[Token]) -> list[tuple[int, str]]:
    # heading_open の次の inline token が表示上の見出しを保持する。
    headings: list[tuple[int, str]] = []
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.map is not None:
            headings.append((token.map[0], tokens[index + 1].content))
    return headings


def _replace_text(path: Path, content: str) -> None:
    # 書込み中の停止で元文書が空・途中の本文になることを避ける。
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(stat.S_IMODE(path.stat().st_mode))
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _remap_path(name: str, mapping: dict[str, str]) -> str:
    # directory 名の一部や Python package 名だけを置換しない。
    for source, target in mapping.items():
        if name == source or name.startswith(source + "/"):
            return target + name[len(source) :]
    return name


def _accessible_link(name: str) -> bool:
    # 移設によって一時的に root 外を指す旧相対 path は、存在確認せず扱う。
    return (
        name != ".."
        and not name.startswith("../")
        and not name.startswith("/")
        and not _PATH_EXCLUDED.intersection(Path(name).parts)
    )


def _rebase_link(root: Path, relative: str, destination: str) -> tuple[str, str | None]:
    # 移設前の file から解決した行き先を、移設後の file からの相対 path にする。
    angled = destination.startswith("<") and destination.endswith(">")
    value = destination[1:-1] if angled else destination
    try:
        url = urlsplit(value)
    except ValueError:
        return destination, "Unrecognized link destination"
    if url.scheme or url.netloc or not url.path or url.path.startswith(("/", "{{")):
        return destination, None
    if "\\" in url.path:
        return destination, "Backslash link requires review"
    origin = _remap_path(
        relative, {target: source for source, target in _MOVES.items()}
    )
    old_target = posixpath.normpath(
        posixpath.join(posixpath.dirname(origin), unquote(url.path))
    )
    target = _remap_path(old_target, _MOVES)
    current = posixpath.normpath(
        posixpath.join(posixpath.dirname(relative), unquote(url.path))
    )
    if current == target:
        return destination, None
    target_exists = _accessible_link(target) and _path(root, target).exists()
    current_exists = _accessible_link(current) and _path(root, current).exists()
    if current_exists:
        # 既に新配置を指すリンクを再実行で再度 rebasing しない。両方存在すれば採否を委ねる。
        reason = "Relative link has two possible targets" if target_exists else None
        return destination, reason
    if not target_exists:
        return destination, "Relative link target could not be resolved within the root"
    rebased = posixpath.relpath(target, posixpath.dirname(relative) or ".")
    updated = urlunsplit(("", "", quote(rebased, safe="/"), url.query, url.fragment))
    return (f"<{updated}>" if angled else updated), None


def _rewrite_path_text(root: Path, path: Path, content: str) -> tuple[str, list[str]]:
    relative = path.relative_to(root).as_posix()
    reviews: list[str] = []
    roots = (
        "{{work-root}}/",
        "{{cmoc-root}}/",
        "{{repo-root}}/",
        root.as_posix() + "/",
        "./",
    )
    literal = re.compile(
        r"(?<![\w./\\:{}-])(?P<root>"
        + "|".join(re.escape(prefix) for prefix in roots)
        + r")?(?P<source>oracle/(?:doc|src))(?![\w.-])"
    )

    def replace_literals(text: str) -> str:
        return literal.sub(
            lambda match: (match["root"] or "") + _MOVES[match["source"]], text
        )

    if path.suffix == ".md":
        parts: list[str] = []
        end = 0
        for match in _MARKDOWN_DESTINATION.finditer(content):
            parts.append(replace_literals(content[end : match.start("target")]))
            destination = match["target"]
            if destination.lstrip("<").startswith(roots[:-1]):
                destination = replace_literals(destination)
            else:
                destination, reason = _rebase_link(root, relative, destination)
                if reason:
                    line = content.count("\n", 0, match.start()) + 1
                    reviews.append(f"REVIEW {relative}:{line}: {reason}")
            parts.append(destination)
            end = match.end("target")
        parts.append(replace_literals(content[end:]))
        updated = "".join(parts)
    else:
        updated = replace_literals(content)
    for line, text in enumerate(updated.splitlines(), 1):
        if _OLD_PATH.search(text):
            reviews.append(f"REVIEW {relative}:{line}: Old or constructed path remains")
    return updated, reviews


def _rewrite_paths(root: Path, *, apply: bool) -> None:
    # 移設の byte 単位検査と分け、候補を全て読んでから書き込む。
    if _load_receipt(root) is None:
        raise MigrationError("No move receipt exists.")
    for source, target in _MOVES.items():
        if _path(root, source).exists() or not _path(root, target).is_dir():
            raise MigrationError("Complete the move before rewriting paths.")
    edits: list[tuple[Path, str, str]] = []
    reviews: list[str] = []
    for name in _PATH_TARGETS:
        path = _path(root, name)
        if not path.exists():
            continue
        paths = _entries(path, excluded=_PATH_EXCLUDED) if path.is_dir() else [path]
        for file in paths:
            if file.is_dir():
                continue
            if not file.is_file():
                raise MigrationError(f"Expected a regular file: {file}")
            relative = file.relative_to(root).as_posix()
            data = file.read_bytes()
            try:
                content = data.decode("utf-8")
            except UnicodeDecodeError:
                reviews.append(f"SKIP {relative}: Not UTF-8 text")
                continue
            if "\0" in content:
                reviews.append(f"SKIP {relative}: Binary content")
                continue
            updated, notices = _rewrite_path_text(root, file, content)
            reviews.extend(notices)
            if updated != content:
                edits.append((file, content, updated))
    for file, before, after in edits:
        relative = file.relative_to(root).as_posix()
        if apply:
            _replace_text(file, after)
            print(f"REWROTE {relative}")
        else:
            print(
                "".join(
                    difflib.unified_diff(
                        before.splitlines(keepends=True),
                        after.splitlines(keepends=True),
                        fromfile=relative,
                        tofile=relative,
                    )
                ),
                end="",
            )
    for review in reviews:
        print(review)
    action = "Rewrote" if apply else "Would rewrite"
    print(f"{action} paths in {len(edits)} files; {len(reviews)} review/skip notices.")
    print("Path rewriting does not verify semantic conformance or runtime behavior.")


def _number_specs(root: Path) -> None:
    # 既存 ID を保持し、全 file の不整合を確認してから不足分だけを採番する。
    parsed = [(path, *_parse(path)) for path in _documents(root, "spec")]
    used: set[str] = set()
    for path, _, tokens in parsed:
        for line, heading in _heading_ids(tokens):
            match = _HEADING_ID.match(heading)
            if match:
                identifier = f"{match[1]}-{match[2]}"
                if match[1] != "SPEC" or identifier in used:
                    raise MigrationError(
                        f"Wrong or duplicate heading ID: {path}:{line + 1}"
                    )
                used.add(identifier)
            elif heading.startswith(("[SPEC-", "[DECI-")):
                raise MigrationError(f"Malformed heading ID: {path}:{line + 1}")
    updates: list[tuple[Path, str]] = []
    next_number = 0
    for path, content, tokens in parsed:
        lines = content.splitlines(keepends=True)
        for line, heading in _heading_ids(tokens):
            if _HEADING_ID.match(heading):
                continue
            while f"SPEC-{next_number:06d}" in used:
                next_number += 1
            if next_number > 999999:
                raise MigrationError("SPEC ID space exhausted.")
            identifier = f"SPEC-{next_number:06d}"
            used.add(identifier)
            source = lines[line]
            match = _ATX.match(source.rstrip("\r\n"))
            if match:
                prefix = match[1] + (match[2] or " ")
                lines[line] = prefix + f"[{identifier}] " + source[match.end() :]
            elif (
                line + 1 < len(lines)
                and source.strip() == heading
                and lines[line + 1].strip().startswith(("=", "-"))
            ):
                lines[line] = f"[{identifier}] " + source
            else:
                raise MigrationError(
                    f"Number this nested or multiline heading manually: {path}:{line + 1}"
                )
        updated = "".join(lines)
        if updated != content:
            updates.append((path, updated))
    for path, content in updates:
        _replace_text(path, content)
        print(f"NUMBERED {path.relative_to(root)}")
    print(
        f"Updated {len(updates)} spec files. Decision and reference files were not edited."
    )


def _text_tokens(tokens: list[Token]) -> list[str]:
    # コード例の ID を文書参照と取り違えない。
    text: list[str] = []
    for token in tokens:
        if token.type == "text":
            text.append(token.content)
        if token.children:
            text.extend(_text_tokens(token.children))
    return text


def _check_docs(root: Path) -> None:
    # 自然言語の適合性は判定せず、定義と参照の機械的な整合性だけを調べる。
    definitions: dict[str, str] = {}
    references: list[tuple[Path, str]] = []
    errors: list[str] = []
    for kind, prefix in (("decision", "DECI"), ("spec", "SPEC")):
        for path in _documents(root, kind):
            content, tokens = _parse(path)
            if kind == "decision" and not content.strip():
                continue
            headings = _heading_ids(tokens)
            if not headings:
                errors.append(f"No heading: {path.relative_to(root)}")
            for line, heading in headings:
                location = f"{path.relative_to(root)}:{line + 1}"
                match = _HEADING_ID.match(heading)
                if match is None or match[1] != prefix:
                    errors.append(
                        f"Expected a leading [{prefix}-...] heading ID: {location}"
                    )
                    continue
                identifier = f"{match[1]}-{match[2]}"
                if identifier in definitions:
                    errors.append(
                        f"Duplicate {identifier}: {location}, {definitions[identifier]}"
                    )
                definitions[identifier] = location
            for content in _text_tokens(tokens):
                references.extend(
                    (path, f"{match[1]}-{match[2]}") for match in _ID.finditer(content)
                )
    for path, identifier in references:
        if identifier not in definitions:
            errors.append(f"Unresolved [{identifier}]: {path.relative_to(root)}")
    if errors:
        raise MigrationError("\n".join(errors))
    print(f"Document IDs verified: {len(definitions)} definitions.")
    print(
        "Semantic conformance, reference authority and runtime behavior require separate review."
    )


def main() -> int:
    """配置元の repository に対し、明示された一つの移行操作だけを行う。"""
    # cmoc を import・起動せず、Git metadata や管理 state にも触れない。
    commands = {
        "plan": _plan,
        "move": _move,
        "verify-move": _verify_move,
        "plan-paths": lambda root: _rewrite_paths(root, apply=False),
        "rewrite-paths": lambda root: _rewrite_paths(root, apply=True),
        "number-specs": _number_specs,
        "check-docs": _check_docs,
    }
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=commands)
    args = parser.parse_args()
    try:
        commands[args.command](Path(__file__).resolve().parent.parent)
    except (MigrationError, OSError, ValueError) as error:
        print(f"Migration stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
