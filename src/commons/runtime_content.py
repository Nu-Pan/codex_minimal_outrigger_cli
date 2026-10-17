"""内容 hash を名前に含む file を保存する。"""

import hashlib
import os
import stat
import tempfile
from pathlib import Path


def write_hashed_file(directory: Path, prefix: str, suffix: str, content: str) -> Path:
    """出力 directory を作成し、内容 hash を名前に含む file を保存する。"""
    content_bytes = content.encode("utf-8")
    digest = hashlib.sha256(content_bytes).hexdigest()
    path = directory / f"{prefix}{digest}{suffix}"
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md の schema store は、
    # hash path 自体の種類を一度だけ調べ、symlink のリンク先は読まない。
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        pass
    else:
        if stat.S_ISDIR(mode):
            raise IsADirectoryError(path)
        if stat.S_ISREG(mode) and path.read_bytes() == content_bytes:
            return path

    # 正しい保存物を再利用するときは、既存 directory の作成・存在確認を省く。
    directory.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=directory, prefix=f".{path.name}.", delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(content_bytes)
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return path
