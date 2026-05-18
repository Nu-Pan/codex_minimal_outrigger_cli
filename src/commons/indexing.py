"""`INDEX.md` メンテナンス処理。"""

import hashlib
import re
import subprocess
from pathlib import Path

from .codex import parse_json_object, run_codex_exec
from .repo import ensure_cmoc_ignored

_EXCLUDED_NAMES = {"memo", "build", "tmp", "__pycache__"}
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


def maintain_indexes(repo_root: Path, *, commit_changes: bool = True) -> bool:
    """配置対象ディレクトリへ `INDEX.md` を用意し、必要なら自動コミットする。"""
    changed_paths: list[str] = []
    if ensure_cmoc_ignored(repo_root):
        changed_paths.append(".gitignore")
        changed_paths.append(".cmoc")
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

    if changed_paths and commit_changes:
        from .repo import commit_if_changed

        commit_if_changed(repo_root, changed_paths, "Maintain INDEX.md files")
    return bool(changed_paths)


def _index_directories(repo_root: Path) -> list[Path]:
    """仕様の除外条件に従って INDEX.md 配置対象を列挙する。"""
    result: list[Path] = []
    directories = [
        repo_root,
        *[path for path in repo_root.rglob("*") if path.is_dir()],
    ]
    for directory in directories:
        relative_parts = directory.relative_to(repo_root).parts
        if any(
            part.startswith(".") or part in _EXCLUDED_NAMES
            for part in relative_parts
        ):
            continue
        if _is_gitignored(repo_root, directory):
            continue
        result.append(directory)
    return result


def _write_index_if_needed(repo_root: Path, directory: Path) -> bool:
    """現在の直下項目から INDEX.md を更新し、差分があれば書く。"""
    index_path = directory / "INDEX.md"
    old_content = (
        index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    )
    existing_entries = _parse_index_entries(old_content)
    entries: list[str] = []

    for child in sorted(directory.iterdir(), key=lambda path: path.name):
        if (
            child.name == "INDEX.md"
            or child.name.startswith(".")
            or child.name in _EXCLUDED_NAMES
        ):
            continue
        if _is_gitignored(repo_root, child):
            continue
        if _looks_binary(child):
            continue

        digest = _hash_path(repo_root, child)
        existing = existing_entries.get(child.name)
        if existing is not None and _entry_hash(existing) == digest:
            entries.append(existing)
        else:
            entries.append(_entry_for(repo_root, child, digest))

    new_content = "\n\n".join(entries)
    if new_content:
        new_content += "\n"

    if old_content == new_content:
        return False
    index_path.write_text(new_content, encoding="utf-8")
    return True


def _entry_for(repo_root: Path, path: Path, digest: str) -> str:
    """1 件分の目次情報を Codex CLI の Structured Output から作る。"""
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _index_prompt(repo_root, path, digest),
            read_only=True,
            expect_json=True,
            output_schema=_INDEX_OUTPUT_SCHEMA,
            json_validator=_validate_index_payload,
        )
    )
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
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    child_hashes = []
    for child in sorted(path.iterdir(), key=lambda item: item.name):
        if (
            child.name == "INDEX.md"
            or child.name.startswith(".")
            or child.name in _EXCLUDED_NAMES
            or _is_gitignored(repo_root, child)
            or _looks_binary(child)
        ):
            continue
        child_hashes.append(_hash_path(repo_root, child))
    return hashlib.sha256("".join(child_hashes).encode("utf-8")).hexdigest()


def _looks_binary(path: Path) -> bool:
    """バイナリらしいファイルを簡易判定する。"""
    if path.is_dir():
        return False
    sample = path.read_bytes()[:1024]
    return b"\0" in sample


def _is_gitignored(repo_root: Path, path: Path) -> bool:
    """gitignore 対象のファイル・ディレクトリか判定する。"""
    relative = path.relative_to(repo_root).as_posix()
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", relative],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode == 0


def _validate_index_payload(value: object) -> None:
    """INDEX 生成用 Structured Output の schema を検査する。"""
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

    for key in sorted(expected_keys):
        _string_list(value.get(key))


def _string_list(value: object) -> list[str]:
    """JSON 値を文字列配列として検査する。"""
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("Expected list[str].")
    return value


def _bullet_lines(values: list[str]) -> list[str]:
    """Markdown 箇条書きへ変換する。"""
    return [f"- {value}" for value in values]


def _parse_index_entries(content: str) -> dict[str, str]:
    """既存 INDEX.md を項目名ごとのブロックへ分解する。"""
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
    match = re.search(r"(?m)^## hash\n\n- ([0-9a-f]{64})$", entry)
    if match is None:
        return None
    return match.group(1)
