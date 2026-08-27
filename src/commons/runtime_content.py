import hashlib
import os
import tempfile
from pathlib import Path


def file_sha256(path: Path) -> str:
    """ファイル内容の SHA-256 digest を返す。

    {{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md の
    「分類結果」では regular file だけが state 同期対象になる。symlink を扱う
    他の caller では、link 先を追跡せず Git が保持する link 文字列を hash する。
    """
    content = os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()
    return hashlib.sha256(content).hexdigest()


def text_sha256(text: str) -> str:
    """文字列を UTF-8 として扱った SHA-256 digest を返す。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_hashed_file(directory: Path, prefix: str, suffix: str, content: str) -> Path:
    """出力 directory を作成し、内容 hash を名前に含む file を保存する。"""
    digest = text_sha256(content)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{prefix}{digest}{suffix}"
    content_bytes = content.encode("utf-8")
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md の schema store は、
    # symlink のリンク先ではなく、指定された hash path 自体へ保存する。
    if not path.is_symlink():
        if path.is_dir():
            raise IsADirectoryError(path)
        if path.is_file() and path.read_bytes() == content_bytes:
            return path

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=directory, prefix=f".{path.name}.", delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(content_bytes)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return path


def is_binary(path: Path) -> bool:
    """先頭 chunk の NUL byte と読み取り可否で binary file を粗く判定する。"""
    try:
        with path.open("rb") as file:
            chunk = file.read(4096)
    except OSError:
        return True
    return b"\0" in chunk
