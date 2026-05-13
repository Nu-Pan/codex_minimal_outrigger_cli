"""`INDEX.md` メンテナンスの簡易実装。"""

import hashlib
import subprocess
from pathlib import Path

from .codex import parse_json_object, run_codex_exec
from .repo import ensure_cmoc_ignored

_EXCLUDED_NAMES = {"memo", "build", "tmp", "__pycache__"}


def maintain_indexes(repo_root: Path, *, commit_changes: bool = True) -> bool:
    """配置対象ディレクトリへ `INDEX.md` を用意し、必要なら自動コミットする。"""
    ensure_cmoc_ignored(repo_root)
    directories = _index_directories(repo_root)
    changed = False
    for directory in sorted(directories, key=lambda path: len(path.parts), reverse=True):
        if _write_index_if_needed(repo_root, directory):
            changed = True

    if changed and commit_changes:
        from .repo import commit_if_changed

        commit_if_changed(repo_root, ["."], "Maintain INDEX.md files")
    return changed


def _index_directories(repo_root: Path) -> list[Path]:
    """仕様の除外条件に従って INDEX.md 配置対象を列挙する。"""
    result: list[Path] = []
    for directory in [repo_root, *[path for path in repo_root.rglob("*") if path.is_dir()]]:
        relative_parts = directory.relative_to(repo_root).parts
        if any(part.startswith(".") or part in _EXCLUDED_NAMES for part in relative_parts):
            continue
        if _is_gitignored(repo_root, directory):
            continue
        result.append(directory)
    return result


def _write_index_if_needed(repo_root: Path, directory: Path) -> bool:
    """現在の直下項目から INDEX.md を生成し、差分があれば書く。"""
    entries = []
    for child in sorted(directory.iterdir(), key=lambda path: path.name):
        if child.name == "INDEX.md" or child.name.startswith(".") or child.name in _EXCLUDED_NAMES:
            continue
        if _is_gitignored(repo_root, child):
            continue
        if _looks_binary(child):
            continue
        entries.append(_entry_for(repo_root, child))
    new_content = "\n\n".join(entries)
    if new_content:
        new_content += "\n"

    index_path = directory / "INDEX.md"
    old_content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    if old_content == new_content:
        return False
    index_path.write_text(new_content, encoding="utf-8")
    return True


def _entry_for(repo_root: Path, path: Path) -> str:
    """1 件分の目次情報を Codex CLI の Structured Output から作る。"""
    digest = _hash_path(path)
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _index_prompt(path, digest),
            read_only=True,
            expect_json=True,
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


def _index_prompt(path: Path, digest: str) -> str:
    """INDEX 目次情報生成用の Codex prompt を作る。"""
    return "\n".join(
        [
            "You are a repository documentation assistant.",
            f"Create routing metadata for `{path}`.",
            "Return only JSON matching this schema:",
            "{",
            '  "type": "object",',
            '  "additionalProperties": false,',
            '  "required": ["summary", "read_this_when", "do_not_read_this_when"],',
            '  "properties": {',
            '    "summary": { "type": "array", "items": { "type": "string" } },',
            '    "read_this_when": { "type": "array", "items": { "type": "string" } },',
            '    "do_not_read_this_when": { "type": "array", "items": { "type": "string" } }',
            "  }",
            "}",
            "Do not return content_hash or any other extra property.",
            "The task is complete when summary, read_this_when, and do_not_read_this_when are returned.",
            f"The content hash is `{digest}` and must not be recalculated or returned.",
        ]
    )


def _hash_path(path: Path) -> str:
    """ファイルまたは直下項目ハッシュ連結から sha256 を計算する。"""
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    child_hashes = []
    for child in sorted(path.iterdir(), key=lambda item: item.name):
        if child.name == "INDEX.md" or child.name.startswith(".") or _looks_binary(child):
            continue
        child_hashes.append(_hash_path(child))
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


def _string_list(value: object) -> list[str]:
    """JSON 値を文字列配列として検査する。"""
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("Expected list[str].")
    return value


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


def _bullet_lines(values: list[str]) -> list[str]:
    """Markdown 箇条書きへ変換する。"""
    return [f"- {value}" for value in values]
