import hashlib
from pathlib import Path


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write_hashed_file(directory: Path, prefix: str, suffix: str, content: str) -> Path:
    digest = text_sha256(content)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{prefix}{digest}{suffix}"
    if not path.exists() or path.read_text() != content:
        path.write_text(content)
    return path


def write_hashed_file_in_existing_dir(
    directory: Path, prefix: str, suffix: str, content: str
) -> Path:
    digest = text_sha256(content)
    path = directory / f"{prefix}{digest}{suffix}"
    if not path.exists() or path.read_text() != content:
        path.write_text(content)
    return path


def is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return True
    return b"\0" in chunk
