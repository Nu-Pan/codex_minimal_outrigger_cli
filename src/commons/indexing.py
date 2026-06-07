"""`INDEX.md` メンテナンス処理。"""

import codecs
import concurrent.futures
import fcntl
import hashlib
import json
import os
import re
import subprocess
import tempfile
import threading
from collections.abc import Iterable
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import copy_context
from pathlib import Path
from urllib.parse import unquote_to_bytes

from .codex import (
    INDEX_GENERATION_MODEL,
    INDEX_GENERATION_REASONING_EFFORT,
    parse_json_object,
    run_codex_exec,
)
from .errors import CmocError

_BINARY_DETECTION_CHUNK_SIZE = 8192
_EMPTY_FILE_DIGEST = hashlib.sha256(b"cmoc-index-empty-file\0").hexdigest()
_EMPTY_DIRECTORY_DIGEST = hashlib.sha256(
    b"cmoc-index-empty-directory\0"
).hexdigest()
_INDEX_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "read_this_when", "do_not_read_this_when"],
    "properties": {
        "summary": {
            "type": "array",
            "items": {"type": "string"},
        },
        "read_this_when": {
            "type": "array",
            "items": {"type": "string"},
        },
        "do_not_read_this_when": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


def maintain_indexes(
    repo_root: Path,
    *,
    excluded_index_roots: Iterable[Path | str] | None = None,
) -> bool:
    """配置対象ディレクトリへ `INDEX.md` を用意し、必要なら自動コミットする。"""
    with _locked_index_maintenance(repo_root):
        return _maintain_indexes_unlocked(
            repo_root,
            excluded_index_roots=excluded_index_roots,
        )


def find_index_inconsistencies(
    repo_root: Path,
    *,
    index_roots: Iterable[Path | str] | None = None,
    excluded_index_roots: Iterable[Path | str] | None = None,
) -> list[str]:
    """`INDEX.md` を更新せず、配置対象と entry/hash の不整合を返す。"""
    gitignore_matcher = _GitignoreMatcher(repo_root)
    excluded_roots = _normalize_excluded_index_roots(
        repo_root,
        excluded_index_roots,
    )
    directories = _index_directories(
        repo_root,
        gitignore_matcher,
        excluded_index_roots=excluded_roots,
    )
    included_roots = _normalize_optional_index_roots(repo_root, index_roots)
    if included_roots is not None:
        directories = [
            directory
            for directory in directories
            if _is_under_any_path(directory, included_roots)
        ]

    inconsistencies: list[str] = []
    for directory in sorted(directories):
        inconsistencies.extend(
            _index_directory_inconsistencies(
                repo_root,
                directory,
                gitignore_matcher,
            )
        )
    return inconsistencies


def is_maintained_index_path(
    repo_root: Path,
    relative_path: str,
    *,
    excluded_index_roots: Iterable[Path | str] | None = None,
) -> bool:
    """`maintain_indexes` が配置し得る `INDEX.md` path か判定する。"""
    path = Path(relative_path)
    if path.is_absolute() or path.name != "INDEX.md":
        return False
    if any(part in {"", ".", ".."} for part in path.parts):
        return False

    index_path = repo_root / path
    directory = index_path.parent
    try:
        directory.relative_to(repo_root)
    except ValueError:
        return False

    excluded_roots = _normalize_excluded_index_roots(
        repo_root,
        excluded_index_roots,
    )
    if _is_under_any_path(directory, excluded_roots):
        return False
    if _has_pruned_index_directory_ancestor(repo_root, directory):
        return False

    gitignored_paths = _GitignoreMatcher(repo_root).ignored_paths([directory])
    return directory not in gitignored_paths


def is_maintained_index_path_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_path: str,
    *,
    excluded_index_roots: Iterable[Path | str] | None = None,
) -> bool:
    """指定 commit 時点で `maintain_indexes` が配置し得る `INDEX.md` path か判定する。"""
    path = Path(relative_path)
    if path.is_absolute() or path.name != "INDEX.md":
        return False
    if any(part in {"", ".", ".."} for part in path.parts):
        return False

    directory = path.parent
    excluded_roots = _normalize_excluded_index_roots(
        repo_root,
        excluded_index_roots,
    )
    if _is_under_any_path(repo_root / directory, excluded_roots):
        return False
    if _has_pruned_index_directory_ancestor_at_commit(
        repo_root,
        commit_hash,
        directory,
    ):
        return False

    candidates = []
    if directory.as_posix() != ".":
        candidates.append(directory.as_posix())

    ignored = _gitignored_paths_at_commit(repo_root, commit_hash, candidates)
    return directory.as_posix() not in ignored


def _maintain_indexes_unlocked(
    repo_root: Path,
    *,
    excluded_index_roots: Iterable[Path | str] | None = None,
) -> bool:
    """排他取得後に `INDEX.md` メンテナンス本体を実行する。"""
    changed_paths: list[str] = []
    gitignore_matcher = _GitignoreMatcher(repo_root)
    excluded_roots = _normalize_excluded_index_roots(
        repo_root,
        excluded_index_roots,
    )

    # 深い階層から depth ごとの barrier を置いて INDEX.md を更新し、親が子の
    # 最新目次を参照できる順序を保つ。
    directories = _index_directories(
        repo_root,
        gitignore_matcher,
        excluded_roots,
    )
    directories_by_depth: dict[int, list[Path]] = {}
    for directory in directories:
        directories_by_depth.setdefault(len(directory.parts), []).append(
            directory
        )
    for depth in sorted(directories_by_depth, reverse=True):
        depth_directories = sorted(directories_by_depth[depth])
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=_index_worker_count(len(depth_directories))
        ) as executor:
            future_by_directory = {
                executor.submit(
                    copy_context().run,
                    _write_index_if_needed,
                    repo_root,
                    directory,
                    gitignore_matcher,
                ): directory
                for directory in depth_directories
            }
            for future in concurrent.futures.as_completed(
                future_by_directory
            ):
                directory = future_by_directory[future]
                if future.result():
                    changed_paths.append(
                        (directory / "INDEX.md")
                        .relative_to(repo_root)
                        .as_posix()
                    )

    # 自動コミット対象は INDEX メンテナンスで触ったパスだけに限定する。
    if changed_paths:
        from .repo import commit_if_changed

        commit_if_changed(
            repo_root,
            sorted(changed_paths),
            "Maintain INDEX.md files",
        )
    inconsistencies = find_index_inconsistencies(
        repo_root,
        excluded_index_roots=excluded_roots,
    )
    if inconsistencies:
        raise CmocError(
            "INDEX.md メンテナンス後の機械的チェックに失敗しました。",
            [
                "Detail の不整合一覧を確認し、INDEX.md 生成処理を修正してから再実行してください。",
                "一時的なファイル変更が同時に起きていないか確認してください。",
            ],
            "\n".join(inconsistencies),
        )
    return bool(changed_paths)


@contextmanager
def _locked_index_maintenance(repo_root: Path) -> Iterator[None]:
    """同一 git repository 内の INDEX メンテナンスを直列化する。"""
    lock_path = _index_maintenance_lock_path(repo_root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _index_maintenance_lock_path(repo_root: Path) -> Path:
    """INDEX メンテナンス用 lock file の repo-local path を返す。"""
    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        ],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        common_dir_text = result.stdout.removesuffix("\n")
        if common_dir_text:
            return Path(common_dir_text) / "cmoc-index-maintenance.lock"

    raise CmocError(
        "INDEX.md メンテナンス用 lock file path の取得に失敗しました。",
        [
            "git repository 内で cmoc を再実行してください。",
            "git rev-parse --git-common-dir が失敗する場合は、git repository の状態を確認してください。",
        ],
        detail=(
            "git rev-parse --path-format=absolute --git-common-dir "
            f"failed in {repo_root}.\n"
            f"exit_code: {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        ),
    )


def _index_directories(
    repo_root: Path,
    gitignore_matcher: "_GitignoreMatcher",
    excluded_index_roots: set[Path],
) -> list[Path]:
    """仕様の除外条件に従って INDEX.md 配置対象を列挙する。"""

    def raise_walk_error(error: OSError) -> None:
        """Path.walk の探索 failure を cmoc error として中断する。"""
        error_path = Path(error.filename) if error.filename else repo_root
        _raise_index_io_error("directory tree の探索", error_path, error)

    # repo root とその配下ディレクトリを配置候補として集める。
    result: list[Path] = []
    directories = [repo_root]
    for current, dir_names, _file_names in repo_root.walk(
        on_error=raise_walk_error
    ):
        child_directories = [
            current / name
            for name in dir_names
            if not _should_prune_index_directory(repo_root, current / name)
        ]
        gitignored_directories = gitignore_matcher.ignored_paths(
            child_directories
        )
        dir_names[:] = [
            path.name
            for path in child_directories
            if path not in gitignored_directories
        ]
        directories.extend(current / name for name in dir_names)

    # 配置対象ディレクトリ専用の除外条件を適用する。
    gitignored_directories = gitignore_matcher.ignored_paths(directories)
    for directory in directories:
        if _is_under_any_path(directory, excluded_index_roots):
            continue
        relative_parts = directory.relative_to(repo_root).parts
        if any(part.startswith(".") for part in relative_parts):
            continue
        if _is_repo_memo(repo_root, directory):
            continue
        if directory in gitignored_directories:
            continue
        result.append(directory)
    return result


def _normalize_excluded_index_roots(
    repo_root: Path,
    excluded_index_roots: Iterable[Path | str] | None,
) -> set[Path]:
    """INDEX.md を書かない root 群を repo 内の絶対 path に正規化する。"""
    if excluded_index_roots is None:
        return set()
    normalized_roots: set[Path] = set()
    for root in excluded_index_roots:
        path = Path(root)
        if not path.is_absolute():
            path = repo_root / path
        try:
            relative = path.resolve().relative_to(repo_root.resolve())
        except ValueError:
            continue
        normalized_roots.add(repo_root / relative)
    return normalized_roots


def _normalize_optional_index_roots(
    repo_root: Path,
    index_roots: Iterable[Path | str] | None,
) -> set[Path] | None:
    """検査対象 root 群を repo 内の絶対 path に正規化する。"""
    if index_roots is None:
        return None
    return _normalize_excluded_index_roots(repo_root, index_roots)


def _is_under_any_path(path: Path, roots: set[Path]) -> bool:
    """path が指定 root のいずれか自身または配下か判定する。"""
    for root in roots:
        if path == root:
            return True
        try:
            path.relative_to(root)
        except ValueError:
            continue
        return True
    return False


def _write_index_if_needed(
    repo_root: Path,
    directory: Path,
    gitignore_matcher: "_GitignoreMatcher",
) -> bool:
    """現在の直下項目から INDEX.md を更新し、差分があれば書く。"""
    # 既存 INDEX.md の内容と、再利用可能な目次ブロックを読み込む。
    index_path = directory / "INDEX.md"
    old_content = _read_existing_index_content(index_path)
    existing_entries = _parse_index_entries(old_content or "")
    entry_items: list[str | tuple[Path, str]] = []

    # 目次作成対象の除外条件だけを使い、配置対象除外名とは切り分ける。
    try:
        children = sorted(directory.iterdir(), key=lambda path: path.name)
    except OSError as error:
        _raise_index_io_error("directory の直下項目列挙", directory, error)
    for child in _index_entry_targets(repo_root, children, gitignore_matcher):
        digest = _hash_path(repo_root, child, gitignore_matcher)
        if digest is None:
            continue
        existing = existing_entries.get(child.name)
        if (
            existing is not None
            and _entry_hash(existing) == digest
            and _entry_format_is_valid(repo_root, existing, child.name, digest)
        ):
            entry_items.append(existing)
        else:
            entry_items.append((child, digest))

    entries = _resolve_index_entries(repo_root, entry_items)

    # 生成内容が空でも、INDEX.md が無ければ新規作成する。
    new_content = "\n\n".join(entries)
    if new_content:
        new_content += "\n"

    if (
        old_content is not None
        and index_path.exists()
        and old_content == new_content
    ):
        return False
    try:
        _replace_index_file(index_path, new_content)
    except OSError as error:
        _raise_index_io_error("INDEX.md の置換", index_path, error)
    return True


def _index_directory_inconsistencies(
    repo_root: Path,
    directory: Path,
    gitignore_matcher: "_GitignoreMatcher",
) -> list[str]:
    """1 directory の `INDEX.md` と直下目次対象の不整合を返す。"""
    index_path = directory / "INDEX.md"
    relative_index = index_path.relative_to(repo_root).as_posix()
    old_content = _read_existing_index_content(index_path)
    if old_content is None:
        return [f"{relative_index}: invalid INDEX.md content"]
    if not index_path.exists():
        return [f"{relative_index}: missing INDEX.md"]

    existing_entries = _parse_index_entries(old_content)
    current_entries: dict[str, str] = {}
    try:
        children = sorted(directory.iterdir(), key=lambda path: path.name)
    except OSError as error:
        _raise_index_io_error("directory の直下項目列挙", directory, error)
    for child in _index_entry_targets(repo_root, children, gitignore_matcher):
        digest = _hash_path(repo_root, child, gitignore_matcher)
        if digest is not None:
            current_entries[child.name] = digest

    inconsistencies: list[str] = []
    for name, digest in sorted(current_entries.items()):
        existing = existing_entries.get(name)
        if existing is None:
            inconsistencies.append(
                f"{relative_index}: missing entry for {name}"
            )
            continue
        if _entry_hash(existing) != digest:
            inconsistencies.append(f"{relative_index}: stale hash for {name}")
            continue
        if not _entry_format_is_valid(repo_root, existing, name, digest):
            inconsistencies.append(
                f"{relative_index}: invalid entry for {name}"
            )
    for name in sorted(set(existing_entries) - set(current_entries)):
        inconsistencies.append(f"{relative_index}: extra entry for {name}")
    return inconsistencies


def _resolve_index_entries(
    repo_root: Path,
    entry_items: list[str | tuple[Path, str]],
) -> list[str]:
    """既存 entry は再利用し、生成が必要な entry は同一 INDEX 内で並列生成する。"""
    pending_count = sum(
        1 for item in entry_items if not isinstance(item, str)
    )
    if pending_count == 0:
        return [item for item in entry_items if isinstance(item, str)]
    results: dict[int, str] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=_index_worker_count(pending_count)
    ) as executor:
        future_by_position = {
            executor.submit(
                copy_context().run,
                _entry_for,
                repo_root,
                item[0],
                item[1],
            ): position
            for position, item in enumerate(entry_items)
            if not isinstance(item, str)
        }
        for future in concurrent.futures.as_completed(future_by_position):
            results[future_by_position[future]] = future.result()

    entries: list[str] = []
    for position, item in enumerate(entry_items):
        if isinstance(item, str):
            entries.append(item)
        else:
            entries.append(results[position])
    return entries


def _index_worker_count(item_count: int) -> int:
    """INDEX 生成用の bounded worker 数を返す。"""
    if item_count <= 0:
        return 1
    return min(item_count, 32)


def _read_existing_index_content(index_path: Path) -> str | None:
    """既存 INDEX.md の通常ファイル内容を読み、再利用不可なら None を返す。"""
    # INDEX.md symlink や読み取り不能な内容は再利用せず、後段で通常ファイルへ
    # 置き換える。
    if index_path.is_symlink():
        return None
    if not index_path.exists():
        return ""
    if not index_path.is_file():
        raise CmocError(
            "INDEX.md が通常ファイルではありません。",
            [
                "該当 path のファイル種別を確認してください。",
                "通常ファイルとして再作成してから cmoc を再実行してください。",
            ],
            str(index_path),
        )
    try:
        return index_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except OSError as error:
        _raise_index_io_error("既存 INDEX.md の読み取り", index_path, error)


def _replace_index_file(index_path: Path, content: str) -> None:
    """INDEX.md を同一ディレクトリ内の一時ファイルから通常ファイルへ置換する。"""
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=index_path.parent,
            prefix=".INDEX.md.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_file.write(content)
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, index_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _entry_for(repo_root: Path, path: Path, digest: str) -> str:
    """1 件分の目次情報を Codex CLI の Structured Output から作る。"""
    # INDEX 生成用の Codex 呼び出しは、事前 INDEX メンテナンスの例外として扱う。
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _index_prompt(repo_root, path, digest),
            purpose=f"INDEX entry 生成 {_display_index_path(repo_root, path)}",
            read_only=True,
            expect_json=True,
            output_schema=_INDEX_OUTPUT_SCHEMA,
            json_validator=_validate_index_payload,
            skip_index_maintenance=True,
            model=INDEX_GENERATION_MODEL,
            reasoning_effort=INDEX_GENERATION_REASONING_EFFORT,
        )
    )

    # schema 検査済み payload を Markdown 目次ブロックへ変換する。
    summary = _string_list(payload.get("summary"))
    read_when = _string_list(payload.get("read_this_when"))
    do_not_read_when = _string_list(payload.get("do_not_read_this_when"))

    return "\n".join(
        [
            f"# `{_encode_index_token(path.name)}`",
            "",
            "## Summary",
            "",
            *_bullet_lines(_safe_index_texts(repo_root, summary)),
            "",
            "## Read this when",
            "",
            *_bullet_lines(_safe_index_texts(repo_root, read_when)),
            "",
            "## Do not read this when",
            "",
            *_bullet_lines(_safe_index_texts(repo_root, do_not_read_when)),
            "",
            "## hash",
            "",
            f"- {digest}",
        ]
    )


def _index_prompt(repo_root: Path, path: Path, digest: str) -> str:
    """INDEX 目次情報生成用の Codex prompt を作る。"""
    # Codex 側には hash を返させず、cmoc が計算した値だけを後段で埋め込む。
    concrete_path = _json_concrete_index_path(path)
    return "\n".join(
        [
            "あなたはリポジトリのルーティング文書を作るアシスタントです。",
            "対象 path は次の JSON string をデコードした絶対 path です: "
            f"{concrete_path}",
            "その対象 path の `INDEX.md` 目次情報を作成してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "summary、read_this_when、do_not_read_this_when はそれぞれ",
            "日本語の文字列配列にしてください。",
            "content_hash などの余計なプロパティは返さないでください。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
            f"内容ハッシュは `{digest}` です。再計算も返却もしないでください。",
        ]
    )


def _hash_path(
    repo_root: Path,
    path: Path,
    gitignore_matcher: "_GitignoreMatcher",
) -> str | None:
    """ファイル内容または直下項目 serialization から sha256 を計算する。"""
    # 空 file/directory は種別を含む sentinel hash で衝突を避ける。
    # 非空ファイルは既存 INDEX との互換性を保つため内容 bytes をそのまま hash 化する。
    if path.is_file():
        try:
            content = path.read_bytes()
        except OSError as error:
            _raise_index_io_error("ファイル内容の hash 計算", path, error)
        if not content:
            return _EMPTY_FILE_DIGEST
        return hashlib.sha256(content).hexdigest()

    if not path.is_dir():
        return None

    # ディレクトリは直下目次対象の type/path/hash を文字列として連結する。
    serialized_entries: list[str] = []
    try:
        children = sorted(
            path.iterdir(),
            key=lambda item: item.relative_to(repo_root).as_posix(),
        )
    except OSError as error:
        _raise_index_io_error("directory 内容の hash 計算", path, error)
    for child in _index_entry_targets(repo_root, children, gitignore_matcher):
        entry_type = "directory" if child.is_dir() else "file"
        relative_path = child.relative_to(repo_root).as_posix()
        content_hash = _hash_path(repo_root, child, gitignore_matcher)
        if content_hash is None:
            continue
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


def _index_entry_targets(
    repo_root: Path,
    paths: list[Path],
    gitignore_matcher: "_GitignoreMatcher",
) -> list[Path]:
    """INDEX 目次情報と directory hash に含める直下項目を返す。"""
    gitignored_paths = gitignore_matcher.ignored_paths(paths)
    return [
        path
        for path in paths
        if _is_index_entry_target(repo_root, path, gitignored_paths)
    ]


def _is_index_entry_target(
    repo_root: Path,
    path: Path,
    gitignored_paths: set[Path],
) -> bool:
    """INDEX 目次情報と directory hash に含める直下項目か判定する。"""
    # symlink は repo 外混入や循環の入口になるため、実体種別を見ずに除外する。
    if path.is_symlink():
        return False
    if (
        path.name == "INDEX.md"
        or path.name.startswith(".")
        or _is_repo_memo(repo_root, path)
    ):
        return False
    if path in gitignored_paths:
        return False
    if not path.is_file() and not path.is_dir():
        return False
    if _looks_binary(path):
        return False
    return True


def _index_entry_kind(path: Path) -> str:
    """INDEX entry 再利用判定用の現在種別を返す。"""
    return "directory" if path.is_dir() else "file"


def _looks_binary(path: Path) -> bool:
    """バイナリらしいファイルを簡易判定する。"""
    # ディレクトリはバイナリ判定の対象外にする。
    if path.is_dir():
        return False

    # NUL byte と UTF-8 decode 可否を組み合わせてテキスト性を判定する。
    decoder = codecs.getincrementaldecoder("utf-8")()
    try:
        with path.open("rb") as file:
            for chunk in iter(
                lambda: file.read(_BINARY_DETECTION_CHUNK_SIZE),
                b"",
            ):
                if b"\0" in chunk:
                    return True
                decoder.decode(chunk, final=False)
        decoder.decode(b"", final=True)
    except UnicodeDecodeError:
        return True
    except OSError as error:
        _raise_index_io_error("バイナリ判定", path, error)
    return False


def _raise_index_io_error(
    operation: str,
    path: Path,
    error: OSError,
) -> None:
    """INDEX メンテナンス中の I/O failure をユーザー向け CmocError にする。"""
    raise CmocError(
        "INDEX.md メンテナンス中にファイルシステム操作へ失敗しました。",
        [
            "Detail の path と OS エラーを確認し、権限やファイル種別を修正してから cmoc を再実行してください。",
            "一時的な I/O 障害の場合は、対象ファイルやディレクトリにアクセスできる状態で cmoc を再実行してください。",
        ],
        f"operation: {operation}\npath: {path}\nerror: {error}",
    ) from error


def _should_prune_index_directory(repo_root: Path, directory: Path) -> bool:
    """探索時に配下を読まない INDEX 配置除外ディレクトリか判定する。"""
    name = directory.name
    return (
        directory.is_symlink()
        or name.startswith(".")
        or _is_repo_memo(repo_root, directory)
    )


def _has_pruned_index_directory_ancestor(
    repo_root: Path,
    directory: Path,
) -> bool:
    """探索時に prune される ancestor 配下の INDEX 配置か判定する。"""
    try:
        relative_parts = directory.relative_to(repo_root).parts
    except ValueError:
        return True
    for depth in range(1, len(relative_parts) + 1):
        ancestor = repo_root.joinpath(*relative_parts[:depth])
        if _should_prune_index_directory(repo_root, ancestor):
            return True
    return False


def _has_pruned_index_directory_ancestor_at_commit(
    repo_root: Path,
    commit_hash: str,
    directory: Path,
) -> bool:
    """指定 commit 時点で prune される ancestor 配下の INDEX 配置か判定する。"""
    relative_parts = directory.parts
    for depth in range(1, len(relative_parts) + 1):
        ancestor = Path(*relative_parts[:depth])
        if (
            ancestor.name.startswith(".")
            or ancestor.as_posix() == "memo"
            or not _is_tree_path_at_commit(repo_root, commit_hash, ancestor)
        ):
            return True
    return False


def _is_tree_path_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_path: Path,
) -> bool:
    """指定 commit の tree 上で relative path が directory か判定する。"""
    from .repo import run_git

    result = run_git(
        repo_root,
        [
            "ls-tree",
            "-z",
            commit_hash,
            "--",
            relative_path.as_posix(),
        ],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "commit 時点の INDEX.md 配置対象判定に失敗しました。",
            [
                "対象 commit と git repository の状態を確認してから cmoc を再実行してください。",
                "git ls-tree が失敗する場合は、対象 branch や commit hash が存在するか確認してください。",
            ],
            result.stderr.strip(),
        )

    entries = [entry for entry in result.stdout.split("\0") if entry]
    if len(entries) != 1:
        return False
    metadata, _separator, _path = entries[0].partition("\t")
    fields = metadata.split()
    return len(fields) >= 2 and fields[1] == "tree"


def _is_repo_memo(repo_root: Path, path: Path) -> bool:
    """`<repo-root>/memo` そのものか判定する。"""
    # memo 禁止は repo root 直下だけに適用する。
    return path == repo_root / "memo"


class _GitignoreMatcher:
    """実 repository の ignore 判定を batched/cached で提供する。"""

    def __init__(self, repo_root: Path) -> None:
        """repo root と判定 cache を初期化する。"""
        self._repo_root = repo_root
        self._cache: dict[str, bool] = {}
        self._lock = threading.Lock()

    def ignored_paths(self, paths: list[Path]) -> set[Path]:
        """gitignore 対象の path 集合を返す。"""
        relatives_by_path = {
            path: path.relative_to(self._repo_root).as_posix()
            for path in paths
        }
        with self._lock:
            unknown_relatives = sorted(
                {
                    relative
                    for relative in relatives_by_path.values()
                    if relative not in self._cache
                }
            )
        if unknown_relatives:
            checked = self._check_ignored(unknown_relatives)
            with self._lock:
                self._cache.update(checked)
        with self._lock:
            ignored_relatives = {
                relative
                for relative in relatives_by_path.values()
                if self._cache[relative]
            }
        return {
            path
            for path, relative in relatives_by_path.items()
            if relative in ignored_relatives
        }

    def _check_ignored(self, relatives: list[str]) -> dict[str, bool]:
        """実 repository の Git ignore 判定をまとめて実行する。"""
        result = subprocess.run(
            [
                "git",
                "-c",
                f"core.excludesFile={os.devnull}",
                "check-ignore",
                "-z",
                "--no-index",
                "--stdin",
            ],
            cwd=self._repo_root,
            check=False,
            input=b"\0".join(os.fsencode(relative) for relative in relatives)
            + b"\0",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_gitignore_git_env(),
        )
        if result.returncode not in {0, 1}:
            raise CmocError(
                ".gitignore の評価に失敗しました。",
                [
                    ".gitignore や .git/info/exclude の構文を確認してから "
                    "cmoc を再実行してください。",
                    "一時的に ignore rule を単純化してから cmoc を再実行してください。",
                ],
                result.stderr.decode(errors="replace").strip(),
            )
        ignored = {
            os.fsdecode(relative)
            for relative in result.stdout.split(b"\0")
            if relative
        }
        return {relative: relative in ignored for relative in relatives}


def _gitignore_git_env() -> dict[str, str]:
    """gitignore 評価用に外部 Git ignore 設定を遮断した env を返す。"""
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def _gitignored_paths_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_paths: list[str],
) -> set[str]:
    """指定 commit の全階層 `.gitignore` で ignore 対象 path を返す。"""
    if not relative_paths:
        return set()

    from .repo import run_git

    gitignore_paths = _ancestor_gitignore_paths(relative_paths)
    gitignores: dict[str, str] = {}
    for gitignore_path in gitignore_paths:
        result = run_git(
            repo_root,
            ["show", f"{commit_hash}:{gitignore_path}"],
            check=False,
        )
        if result.returncode == 0:
            gitignores[gitignore_path] = result.stdout

    if not gitignores:
        return set()

    env = _gitignore_git_env()
    with tempfile.TemporaryDirectory(prefix="cmoc-gitignore-commit-") as temp_name:
        temp_root = Path(temp_name)
        subprocess.run(
            ["git", "init", "-q"],
            cwd=temp_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        for gitignore_path, content in gitignores.items():
            target = temp_root / gitignore_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        for relative_path in relative_paths:
            target = temp_root / relative_path
            target.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            [
                "git",
                "-c",
                f"core.excludesFile={os.devnull}",
                "check-ignore",
                "-z",
                "--no-index",
                "--stdin",
            ],
            cwd=temp_root,
            check=False,
            input=b"\0".join(os.fsencode(path) for path in relative_paths)
            + b"\0",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

    if result.returncode not in {0, 1}:
        raise CmocError(
            ".gitignore の評価に失敗しました。",
            [
                ".gitignore の構文を確認してから cmoc を再実行してください。",
                "一時的に .gitignore を単純化してから cmoc を再実行してください。",
            ],
            result.stderr.decode(errors="replace").strip(),
        )
    return {
        os.fsdecode(path)
        for path in result.stdout.split(b"\0")
        if path
    }


def _ancestor_gitignore_paths(relative_paths: list[str]) -> list[str]:
    """path の ancestor にある `.gitignore` path を root から順に返す。"""
    gitignore_paths: set[str] = {".gitignore"}
    for relative_path in relative_paths:
        parts = Path(relative_path).parts
        for depth in range(1, len(parts)):
            gitignore_paths.add(Path(*parts[:depth], ".gitignore").as_posix())
    return sorted(gitignore_paths, key=lambda path: (path.count("/"), path))


def _validate_index_payload(value: object) -> None:
    """INDEX 生成用 Structured Output の schema を検査する。"""
    # top-level object と key 集合を先に検証する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")

    expected_keys = {"summary", "read_this_when", "do_not_read_this_when"}
    actual_keys = set(value)
    missing_keys = sorted(expected_keys - actual_keys)
    extra_keys = sorted(actual_keys - expected_keys)
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}.")
    if extra_keys:
        raise ValueError(f"Unexpected keys: {', '.join(extra_keys)}.")

    # 各プロパティは日本語文を格納する string 配列として扱う。
    for key in sorted(expected_keys):
        _string_list(value.get(key))


def _string_list(value: object) -> list[str]:
    """JSON 値を文字列配列として検査する。"""
    # schema validator とは別に Python 側で list[str] を保証する。
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("Expected list[str].")
    return value


def _bullet_lines(values: list[str]) -> list[str]:
    """Markdown 箇条書きへ変換する。"""
    # INDEX.md の各説明項目は Markdown bullet として出力する。
    return [f"- {value}" for value in values]


def _is_index_text_character(character: str) -> bool:
    """INDEX.md の説明行へそのまま置ける文字か判定する。"""
    # Unicode の通常文字は維持し、ASCII 制御文字と surrogate は除外する。
    codepoint = ord(character)
    return codepoint >= 0x20 and codepoint != 0x7F and not (
        0xD800 <= codepoint <= 0xDFFF
    )


def _display_index_path(repo_root: Path, path: Path) -> str:
    """Codex prompt やログ用途の repo 相対 path を安全な 1 行表現にする。"""
    return _encode_index_token(path.relative_to(repo_root).as_posix())


def _display_concrete_index_path(path: Path) -> str:
    """絶対 path を INDEX token と同じ安全な 1 行表現にする。"""
    return _encode_index_token(path.resolve().as_posix())


def _json_concrete_index_path(path: Path) -> str:
    """Codex prompt 用の絶対 path を可逆な JSON string にする。"""
    return json.dumps(path.resolve().as_posix())


def _encode_index_token(value: str) -> str:
    """heading 内の code span に置く名前を可逆な 1 行 token にする。"""
    # `%` は escape 導入子なので必ず符号化し、backtick と制御文字も避ける。
    encoded_parts: list[str] = []
    for character in value:
        if (
            character == "%"
            or character == "`"
            or not _is_index_text_character(character)
        ):
            encoded_parts.extend(
                f"%{byte:02X}" for byte in _filesystem_text_bytes(character)
            )
        else:
            encoded_parts.append(character)
    return "".join(encoded_parts)


def _decode_index_token(value: str) -> str:
    """heading 内 token を元のファイル・ディレクトリ名へ戻す。"""
    return os.fsdecode(unquote_to_bytes(value))


def _directory_hash_relative_path(value: str) -> str:
    """directory hash 用 relative path を UTF-8 文字列へ正規化する。"""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return _encode_index_token(value)
    return value


def _filesystem_text_bytes(value: str) -> bytes:
    """filesystem 由来文字列を surrogateescape を含めて bytes へ戻す。"""
    return os.fsencode(value)


def _parse_index_entries(content: str) -> dict[str, str]:
    """既存 INDEX.md を項目名ごとのブロックへ分解する。"""
    # 見出し位置を先に集め、次の見出し直前までを 1 ブロックとして切り出す。
    entries: dict[str, str] = {}
    matches = list(re.finditer(r"(?m)^# `([^`\n]*)`\n", content))
    for index, match in enumerate(matches):
        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(content)
        )
        try:
            name = _decode_index_token(match.group(1))
        except UnicodeDecodeError:
            continue
        entries[name] = content[start:end].strip()
    return entries


def _entry_hash(entry: str) -> str | None:
    """目次情報ブロックから hash 欄の値を読む。"""
    # 仕様上の hash 欄だけを最新判定に使う。
    match = re.search(r"(?m)^## hash\n\n- ([0-9a-f]{64})", entry)
    if match is None:
        return None
    return match.group(1)


def _entry_format_is_valid(
    repo_root: Path,
    entry: str,
    name: str,
    digest: str,
) -> bool:
    """既存目次ブロックが仕様の固定フォーマットに一致するか判定する。"""
    # 見出しと 4 セクションの順序、説明欄の bullet 形式まで検査する。
    # Structured Output schema は空配列を許容するため、bullet 0 件も有効。
    if _entry_has_known_stale_routing_text(repo_root, entry):
        return False

    encoded_name = _encode_index_token(name)
    expected_heading = f"# `{encoded_name}`"
    if not entry.startswith(expected_heading + "\n"):
        return False

    pattern = re.compile(
        r"\A"
        rf"\# `{re.escape(encoded_name)}`\n\n"
        r"## Summary\n\n"
        r"(?P<summary>(?:- [^\n]*\n)*)"
        r"\n"
        r"## Read this when\n\n"
        r"(?P<read>(?:- [^\n]*\n)*)"
        r"\n"
        r"## Do not read this when\n\n"
        r"(?P<skip>(?:- [^\n]*\n)*)"
        r"\n"
        r"## hash\n\n"
        rf"- {digest}"
        r"\Z"
    )
    return pattern.match(entry) is not None


def _entry_has_known_stale_routing_text(repo_root: Path, entry: str) -> bool:
    """既知の古い routing text を含む entry を弾く。"""
    # `cmo apply fork` のような誤誘導や、過去の仕様配置に基づく存在しない
    # oracles path、別 worktree の絶対 path は hash が最新でも再生成対象にする。
    return _normalize_known_index_routes(repo_root, entry) != entry


def _safe_index_texts(repo_root: Path, values: list[str]) -> list[str]:
    """Markdown の 1 行 bullet として扱える文字列へ正規化する。"""
    return [_safe_index_text(repo_root, value) for value in values]


def _safe_index_text(repo_root: Path, value: str) -> str:
    """INDEX.md の固定フォーマットを壊さない 1 行文字列へ変換する。"""
    # 改行や制御文字は Markdown block の構造を壊すため空白へ寄せる。
    text = "".join(
        character if _is_index_text_character(character) else " "
        for character in value
    )
    text = re.sub(r"\s+", " ", text).strip()
    text = _normalize_known_index_routes(repo_root, text)
    # Structured Output の項目文字列は「本文」として扱い、Markdown bullet は
    # cmoc 側で 1 つだけ付与する。
    return re.sub(r"^(?:[-*+]\s+)+", "", text).strip()


def _normalize_known_index_routes(repo_root: Path, text: str) -> str:
    """INDEX.md 用 text に含まれる既知の古い表記を現在の表記へ寄せる。"""
    text = _normalize_known_command_names(text)
    text = _normalize_absolute_repository_paths(repo_root, text)
    stale_prefix = "oracles/app_specs/"
    current_prefix = "oracles/docs/app_specs/"
    if stale_prefix not in text:
        return text
    if (repo_root / "oracles/app_specs").exists():
        return text
    if not (repo_root / "oracles/docs/app_specs").exists():
        return text
    return text.replace(stale_prefix, current_prefix)


def _normalize_absolute_repository_paths(repo_root: Path, text: str) -> str:
    """INDEX.md の説明文に混入した repository 絶対 path を相対 path へ寄せる。"""

    def replace(match: re.Match[str]) -> str:
        candidate = match.group(0)
        replacement = _relative_repository_path_for_text(repo_root, candidate)
        if replacement is None:
            return candidate
        return replacement

    return re.sub(r"/[A-Za-z0-9._~!$&'()*+,;=:@%/-]+", replace, text)


def _relative_repository_path_for_text(
    repo_root: Path,
    candidate: str,
) -> str | None:
    """説明文内の絶対 path が repo 内項目を指すなら repo 相対表記を返す。"""
    candidate_path = Path(candidate)
    resolved_repo_root = repo_root.resolve()
    try:
        return candidate_path.resolve().relative_to(resolved_repo_root).as_posix()
    except (OSError, ValueError):
        pass

    parts = candidate_path.parts
    for start in range(1, len(parts)):
        relative_candidate = Path(*parts[start:])
        if relative_candidate.parts and (repo_root / relative_candidate).exists():
            return relative_candidate.as_posix()
    return None


def _normalize_known_command_names(text: str) -> str:
    """存在しない過去の cmoc command 名を INDEX.md へ残さない。"""
    return re.sub(
        r"(?<![A-Za-z0-9_-])cmo(?=\s+(?:init|session|review|apply)\b)",
        "cmoc",
        text,
    )
