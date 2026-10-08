"""Repository ごとに共有する、種類別の単調増加 ID を発行する。"""

import re
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from .runtime_paths import untracked_data_dir

_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
_LIMIT = 36**6
_PREFIXES = frozenset(
    {"exec", "sess", "run", "ac", "cc", "eit", "fbr", "fbg", "fbc", "fbo"}
)
_ID_PATTERN = re.compile(
    r"(?P<prefix>exec|sess|run|ac|cc|eit|fbr|fbg|fbc|fbo)_"
    r"(?P<sequence>[0-9a-z]{6})_"
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})_"
    r"(?P<time>[0-9]{2}-[0-9]{2})"
)


def is_common_id(value: object, prefix: str) -> bool:
    """指定種類の canonical ID か判定する。"""
    if prefix not in _PREFIXES or not isinstance(value, str):
        return False
    match = _ID_PATTERN.fullmatch(value)
    if match is None or match.group("prefix") != prefix:
        return False
    try:
        datetime.strptime(
            f"{match.group('date')}_{match.group('time')}", "%Y-%m-%d_%H-%M"
        )
    except ValueError:
        return False
    return True


def new_id(repository: Path, prefix: str) -> str:
    """SQLite の排他 transaction で通番を確定し、ローカル発行時刻を付ける。"""
    if prefix not in _PREFIXES:
        raise ValueError(f"unknown ID prefix: {prefix}")
    state_dir = untracked_data_dir(repository) / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    database = state_dir / "id_sequences.sqlite3"
    with closing(
        sqlite3.connect(database, timeout=30, isolation_level=None)
    ) as connection:
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS sequence "
                "(prefix TEXT PRIMARY KEY, next_value INTEGER NOT NULL)"
            )
            row = connection.execute(
                "SELECT next_value FROM sequence WHERE prefix = ?", (prefix,)
            ).fetchone()
            sequence = int(row[0]) if row else 0
            if sequence >= _LIMIT:
                raise OverflowError(f"{prefix} ID sequence exhausted")
            connection.execute(
                "INSERT INTO sequence(prefix, next_value) VALUES (?, ?) "
                "ON CONFLICT(prefix) DO UPDATE SET next_value = excluded.next_value",
                (prefix, sequence + 1),
            )
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
    issued_at = datetime.now().strftime("%Y-%m-%d_%H-%M")
    digits = ""
    for _ in range(6):
        sequence, remainder = divmod(sequence, 36)
        digits = _ALPHABET[remainder] + digits
    return f"{prefix}_{digits}_{issued_at}"
