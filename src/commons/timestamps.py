"""cmoc 仕様のタイムスタンプ生成。"""

import re
from datetime import datetime

TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}_\d{2}_\d{9}$"
)


def make_timestamp(now: datetime | None = None) -> str:
    """ローカル時刻から cmoc の `<time-stamp>` 文字列を作る。"""
    # aware datetime はローカルタイムゾーンへ変換し、naive datetime はローカル時刻として扱う。
    source = now if now is not None else datetime.now()
    current = source.astimezone()

    # 仕様上 msec は 9 桁のゼロ埋めにする。
    return (
        f"{current.year:04d}-{current.month:02d}-{current.day:02d}_"
        f"{current.hour:02d}-{current.minute:02d}_{current.second:02d}_"
        f"{current.microsecond // 1000:09d}"
    )


def is_timestamp(value: str) -> bool:
    """cmoc の `<time-stamp>` 形式か判定する。"""
    return bool(TIMESTAMP_PATTERN.fullmatch(value))
