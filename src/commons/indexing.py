"""`INDEX.md` メンテナンス処理。"""

import codecs
import hashlib
import re
import subprocess
from pathlib import Path

from .codex import (
    INDEX_GENERATION_MODEL,
    INDEX_GENERATION_REASONING_EFFORT,
    parse_json_object,
    run_codex_exec,
)
from .repo import ensure_cmoc_ignored

_INDEX_DIRECTORY_EXCLUDED_NAMES: set[str] = {"build", "tmp", "__pycache__"}
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


def maintain_indexes(repo_root: Path) -> bool:
    """配置対象ディレクトリへ `INDEX.md` を用意し、必要なら自動コミットする。"""
    # `.cmoc` の ignore 保証を先に行い、INDEX メンテ差分と一緒に扱う。
    changed_paths: list[str] = []
    if ensure_cmoc_ignored(repo_root):
        changed_paths.append(".gitignore")
        changed_paths.append(".cmoc")

    # 深い階層から順に INDEX.md を更新し、親の hash が最新子目次を反映するようにする。
    directories = _index_directories(repo_root)
    for directory in sorted(
        directories,
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if _write_index_if_needed(repo_root, directory):
            changed_paths.append(
                (directory / "INDEX.md").relative_to(repo_root).as_posix()
            )

    # 自動コミット対象は INDEX メンテナンスで触ったパスだけに限定する。
    if changed_paths:
        from .repo import commit_if_changed

        commit_if_changed(repo_root, changed_paths, "Maintain INDEX.md files")
    return bool(changed_paths)


def _index_directories(repo_root: Path) -> list[Path]:
    """仕様の除外条件に従って INDEX.md 配置対象を列挙する。"""
    # repo root とその配下ディレクトリを配置候補として集める。
    result: list[Path] = []
    directories = [repo_root]
    for current, dir_names, _file_names in repo_root.walk():
        dir_names[:] = [
            name
            for name in dir_names
            if not _should_prune_index_directory(repo_root, current / name)
        ]
        directories.extend(current / name for name in dir_names)

    # 配置対象ディレクトリ専用の除外条件を適用する。
    for directory in directories:
        relative_parts = directory.relative_to(repo_root).parts
        if any(
            part.startswith(".") or part in _INDEX_DIRECTORY_EXCLUDED_NAMES
            for part in relative_parts
        ):
            continue
        if _is_repo_memo(repo_root, directory):
            continue
        if _is_gitignored(repo_root, directory):
            continue
        result.append(directory)
    return result


def _write_index_if_needed(repo_root: Path, directory: Path) -> bool:
    """現在の直下項目から INDEX.md を更新し、差分があれば書く。"""
    # 既存 INDEX.md の内容と、再利用可能な目次ブロックを読み込む。
    index_path = directory / "INDEX.md"
    index_exists = index_path.exists()
    old_content = (
        index_path.read_text(encoding="utf-8") if index_exists else ""
    )
    existing_entries = _parse_index_entries(old_content)
    entries: list[str] = []

    # 目次作成対象の除外条件だけを使い、配置対象除外名とは切り分ける。
    for child in sorted(directory.iterdir(), key=lambda path: path.name):
        if (
            child.name == "INDEX.md"
            or child.name.startswith(".")
            or _is_repo_memo(repo_root, child)
        ):
            continue
        if _is_gitignored(repo_root, child):
            continue
        if _looks_binary(child):
            continue

        digest = _hash_path(repo_root, child)
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

    if index_exists and old_content == new_content:
        return False
    index_path.write_text(new_content, encoding="utf-8")
    return True


def _entry_for(repo_root: Path, path: Path, digest: str) -> str:
    """1 件分の目次情報を Codex CLI の Structured Output から作る。"""
    # INDEX 生成用の Codex 呼び出しは、事前 INDEX メンテナンスの例外として扱う。
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _index_prompt(repo_root, path, digest),
            purpose=f"generate INDEX entry for {path.relative_to(repo_root)}",
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
            f"# `{path.name}`",
            "",
            "## Summary",
            "",
            *_bullet_lines(summary),
            "",
            "## Read this when",
            "",
            *_bullet_lines(read_when),
            "",
            "## Do not read this when",
            "",
            *_bullet_lines(do_not_read_when),
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


def _hash_path(repo_root: Path, path: Path) -> str:
    """ファイルまたは直下項目ハッシュ連結から sha256 を計算する。"""
    # ファイルは内容 bytes をそのまま hash 化する。
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()

    # ディレクトリは目次作成対象と同じ除外条件で子 hash を連結する。
    child_hashes = []
    for child in sorted(path.iterdir(), key=lambda item: item.name):
        if (
            child.name == "INDEX.md"
            or child.name.startswith(".")
            or _is_repo_memo(repo_root, child)
            or _is_gitignored(repo_root, child)
            or _looks_binary(child)
        ):
            continue
        child_hashes.append(_hash_path(repo_root, child))
    return hashlib.sha256("".join(child_hashes).encode("utf-8")).hexdigest()


def _looks_binary(path: Path) -> bool:
    """バイナリらしいファイルを簡易判定する。"""
    # ディレクトリはバイナリ判定の対象外にする。
    if path.is_dir():
        return False

    # NUL byte と UTF-8 decode 可否を組み合わせてテキスト性を判定する。
    sample = path.read_bytes()[:4096]
    if b"\0" in sample:
        return True
    try:
        decoder = codecs.getincrementaldecoder("utf-8")()
        decoder.decode(sample, final=False)
    except UnicodeDecodeError:
        return True
    return False


def _should_prune_index_directory(repo_root: Path, directory: Path) -> bool:
    """探索時に配下を読まない INDEX 配置除外ディレクトリか判定する。"""
    # root 直下 memo と、名前ベース除外ディレクトリの配下は探索しない。
    name = directory.name
    return (
        name.startswith(".")
        or name in _INDEX_DIRECTORY_EXCLUDED_NAMES
        or _is_repo_memo(repo_root, directory)
    )


def _is_repo_memo(repo_root: Path, path: Path) -> bool:
    """`<repo-root>/memo` そのものか判定する。"""
    # memo 禁止は repo root 直下だけに適用する。
    return path == repo_root / "memo"


def _is_gitignored(repo_root: Path, path: Path) -> bool:
    """gitignore 対象のファイル・ディレクトリか判定する。"""
    # tracked 状態に依存せず .gitignore pattern への一致だけを見る。
    relative = path.relative_to(repo_root).as_posix()
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", "--", relative],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode == 0


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


def _parse_index_entries(content: str) -> dict[str, str]:
    """既存 INDEX.md を項目名ごとのブロックへ分解する。"""
    # 見出し位置を先に集め、次の見出し直前までを 1 ブロックとして切り出す。
    entries: dict[str, str] = {}
    matches = list(re.finditer(r"(?m)^# `([^`]+)`\n", content))
    for index, match in enumerate(matches):
        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(content)
        )
        entries[match.group(1)] = content[start:end].strip()
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
    expected_heading = f"# `{name}`"
    if not entry.startswith(expected_heading + "\n"):
        return False

    pattern = re.compile(
        r"\A"
        rf"\# `{re.escape(name)}`\n\n"
        r"## Summary\n\n"
        r"(?P<summary>(?:- .*\n)*)"
        r"\n"
        r"## Read this when\n\n"
        r"(?P<read>(?:- .*\n)*)"
        r"\n"
        r"## Do not read this when\n\n"
        r"(?P<skip>(?:- .*\n)*)"
        r"\n"
        r"## hash\n\n"
        rf"- {digest}"
        r"\Z"
    )
    return pattern.match(entry) is not None
