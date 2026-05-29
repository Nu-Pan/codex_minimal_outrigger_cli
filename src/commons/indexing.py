"""`INDEX.md` メンテナンス処理。"""

import codecs
import hashlib
import os
import re
import subprocess
import tempfile
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import unquote

from .codex import (
    INDEX_GENERATION_MODEL,
    INDEX_GENERATION_REASONING_EFFORT,
    parse_json_object,
    run_codex_exec,
)
from .errors import CmocError

_INDEX_DIRECTORY_EXCLUDED_NAMES: set[str] = {"build", "tmp", "__pycache__"}
_BINARY_DETECTION_CHUNK_SIZE = 8192
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
    changed_paths: list[str] = []
    gitignore_matcher = _GitignoreMatcher(repo_root)
    excluded_roots = _normalize_excluded_index_roots(
        repo_root,
        excluded_index_roots,
    )

    # 深い階層から順に INDEX.md を更新し、親の hash が最新子目次を反映するようにする。
    directories = _index_directories(
        repo_root,
        gitignore_matcher,
        excluded_roots,
    )
    for directory in sorted(
        directories,
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if _write_index_if_needed(repo_root, directory, gitignore_matcher):
            changed_paths.append(
                (directory / "INDEX.md").relative_to(repo_root).as_posix()
            )

    # 自動コミット対象は INDEX メンテナンスで触ったパスだけに限定する。
    if changed_paths:
        from .repo import commit_if_changed

        commit_if_changed(repo_root, changed_paths, "Maintain INDEX.md files")
    return bool(changed_paths)


def _index_directories(
    repo_root: Path,
    gitignore_matcher: "_GitignoreMatcher",
    excluded_index_roots: set[Path],
) -> list[Path]:
    """仕様の除外条件に従って INDEX.md 配置対象を列挙する。"""
    # repo root とその配下ディレクトリを配置候補として集める。
    result: list[Path] = []
    directories = [repo_root]
    for current, dir_names, _file_names in repo_root.walk():
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
        if any(
            part.startswith(".") or part in _INDEX_DIRECTORY_EXCLUDED_NAMES
            for part in relative_parts
        ):
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
    entries: list[str] = []

    # 目次作成対象の除外条件だけを使い、配置対象除外名とは切り分ける。
    children = sorted(directory.iterdir(), key=lambda path: path.name)
    for child in _index_entry_targets(repo_root, children, gitignore_matcher):
        digest = _hash_path(repo_root, child, gitignore_matcher)
        existing = existing_entries.get(child.name)
        if (
            existing is not None
            and _entry_hash(existing) == digest
            and _entry_format_is_valid(existing, child.name, digest)
        ):
            entries.append(existing)
        else:
            entries.append(_entry_for(repo_root, child, digest))

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
    _replace_index_file(index_path, new_content)
    return True


def _read_existing_index_content(index_path: Path) -> str | None:
    """既存 INDEX.md の通常ファイル内容を読み、symlink は再利用しない。"""
    # INDEX.md symlink はリンク先を読まず、後段で通常ファイルへ置き換える。
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
    except (OSError, UnicodeDecodeError):
        return ""


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
            purpose=f"INDEX entry 生成 {path.relative_to(repo_root)}",
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
            *_bullet_lines(_safe_index_texts(summary)),
            "",
            "## Read this when",
            "",
            *_bullet_lines(_safe_index_texts(read_when)),
            "",
            "## Do not read this when",
            "",
            *_bullet_lines(_safe_index_texts(do_not_read_when)),
            "",
            "## hash",
            "",
            f"- {digest}",
        ]
    )


def _index_prompt(repo_root: Path, path: Path, digest: str) -> str:
    """INDEX 目次情報生成用の Codex prompt を作る。"""
    # Codex 側には hash を返させず、cmoc が計算した値だけを後段で埋め込む。
    return "\n".join(
        [
            "あなたはリポジトリのルーティング文書を作るアシスタントです。",
            f"`{path}` の `INDEX.md` 目次情報を作成してください。",
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
) -> str:
    """ファイル内容または直下項目 serialization から sha256 を計算する。"""
    # ファイルは内容 bytes をそのまま hash 化する。
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()

    # ディレクトリは直下目次対象の type/path/hash を安定形式で連結する。
    serialized_entries: list[str] = []
    children = sorted(
        path.iterdir(),
        key=lambda item: item.relative_to(repo_root).as_posix(),
    )
    for child in _index_entry_targets(repo_root, children, gitignore_matcher):
        entry_type = "directory" if child.is_dir() else "file"
        relative_path = child.relative_to(repo_root).as_posix()
        content_hash = _hash_path(repo_root, child, gitignore_matcher)
        serialized_entries.append(
            f"{entry_type}\0{relative_path}\0{content_hash}\n"
        )
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
    if _looks_binary(path):
        return False
    return True


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
    return False


def _should_prune_index_directory(repo_root: Path, directory: Path) -> bool:
    """探索時に配下を読まない INDEX 配置除外ディレクトリか判定する。"""
    # root 直下 memo と、名前ベース除外ディレクトリの配下は探索しない。
    name = directory.name
    return (
        directory.is_symlink()
        or name.startswith(".")
        or name in _INDEX_DIRECTORY_EXCLUDED_NAMES
        or _is_repo_memo(repo_root, directory)
    )


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

    def ignored_paths(self, paths: list[Path]) -> set[Path]:
        """gitignore 対象の path 集合を返す。"""
        relatives_by_path = {
            path: path.relative_to(self._repo_root).as_posix()
            for path in paths
        }
        unknown_relatives = sorted(
            {
                relative
                for relative in relatives_by_path.values()
                if relative not in self._cache
            }
        )
        if unknown_relatives:
            self._cache.update(self._check_ignored(unknown_relatives))
        return {
            path
            for path, relative in relatives_by_path.items()
            if self._cache[relative]
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


def _safe_index_texts(values: list[str]) -> list[str]:
    """Markdown の 1 行 bullet として扱える文字列へ正規化する。"""
    # Structured Output 由来の説明文が block 境界を壊さないようにする。
    return [_safe_index_text(value) for value in values]


def _safe_index_text(value: str) -> str:
    """INDEX.md の固定フォーマットを壊さない 1 行文字列へ変換する。"""
    # 改行や制御文字は Markdown block の構造を壊すため空白へ寄せる。
    text = "".join(
        character if _is_index_text_character(character) else " "
        for character in value
    )
    text = re.sub(r"\s+", " ", text).strip()
    # Structured Output の項目文字列は「本文」として扱い、Markdown bullet は
    # cmoc 側で 1 つだけ付与する。
    return re.sub(r"^(?:[-*+]\s+)+", "", text).strip()


def _is_index_text_character(character: str) -> bool:
    """INDEX.md の説明行へそのまま置ける文字か判定する。"""
    # Unicode の通常文字は維持し、ASCII 制御文字だけを除外する。
    return ord(character) >= 0x20 and ord(character) != 0x7F


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
                f"%{byte:02X}" for byte in character.encode("utf-8")
            )
        else:
            encoded_parts.append(character)
    return "".join(encoded_parts)


def _decode_index_token(value: str) -> str:
    """heading 内 token を元のファイル・ディレクトリ名へ戻す。"""
    return unquote(value, encoding="utf-8", errors="strict")


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
    match = re.search(r"(?m)^## hash\n\n- ([0-9a-f]{64})$", entry)
    if match is None:
        return None
    return match.group(1)


def _entry_format_is_valid(entry: str, name: str, digest: str) -> bool:
    """既存目次ブロックが仕様の固定フォーマットに一致するか判定する。"""
    # 見出しと 4 セクションの順序、説明欄の bullet 形式まで検査する。
    # Structured Output schema は空配列を許容するため、bullet 0 件も有効。
    if _entry_has_known_command_typo(entry):
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


def _entry_has_known_command_typo(entry: str) -> bool:
    """既知の cmoc コマンド名 typo を含む古い routing entry を弾く。"""
    # `cmo apply fork` のような誤誘導は hash が最新でも再生成対象にする。
    return (
        re.search(
            r"(?<![A-Za-z0-9_-])cmo\s+(?:init|session|review|apply)\b",
            entry,
        )
        is not None
    )
