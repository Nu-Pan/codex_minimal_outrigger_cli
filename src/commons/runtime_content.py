import hashlib
from pathlib import Path


def file_sha256(path: Path) -> str:
    """ファイル内容の SHA-256 digest を返す。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(text: str) -> str:
    """文字列を UTF-8 として扱った SHA-256 digest を返す。"""
    return hashlib.sha256(text.encode()).hexdigest()


def write_hashed_file(directory: Path, prefix: str, suffix: str, content: str) -> Path:
    """出力 directory を作成し、内容 hash を名前に含む file を保存する。"""
    digest = text_sha256(content)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{prefix}{digest}{suffix}"
    if not path.exists() or path.read_text() != content:
        path.write_text(content)
    return path


def is_binary(path: Path) -> bool:
    """先頭 chunk の NUL byte と読み取り可否で binary file を粗く判定する。"""
    try:
        with path.open("rb") as file:
            chunk = file.read(4096)
    except OSError:
        return True
    return b"\0" in chunk
