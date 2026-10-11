"""Repository ごとに共有する、種類別の単調増加 ID を発行する。"""

import re
from datetime import datetime
from pathlib import Path

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
        # 固定書式は検査済みなので、汎用書式解析を介さず暦と時刻を検査する。
        datetime.fromisoformat(
            f"{match.group('date')}T{match.group('time').replace('-', ':')}"
        )
    except ValueError:
        return False
    return True


def new_id(repository: Path, prefix: str) -> str:
    """SQLite の排他 transaction で通番を確定し、ローカル発行時刻を付ける。"""
    # ID 検査だけを使う reporter では、採番用の DB・path 解決を読み込まない。
    import sqlite3
    from contextlib import closing

    from .runtime_paths import untracked_data_dir

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
    # strftime の年幅は環境に依存するため、日時の各 field を直接ゼロ埋めする。
    now = datetime.now()
    issued_at = (
        f"{now.year:04d}-{now.month:02d}-{now.day:02d}_{now.hour:02d}-{now.minute:02d}"
    )
    digits = ""
    for _ in range(6):
        sequence, remainder = divmod(sequence, 36)
        digits = _ALPHABET[remainder] + digits
    return f"{prefix}_{digits}_{issued_at}"
