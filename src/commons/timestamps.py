"""cmoc 仕様のタイムスタンプ生成。"""

import re
from datetime import datetime

TIMESTAMP_PATTERN = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})_"
    r"(?P<hour>\d{2})-(?P<minute>\d{2})_(?P<second>\d{2})_"
    r"(?P<msec>\d{9})$"
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


def console_timestamp(now: datetime | None = None) -> str:
    """コンソールログ用のミリ秒付き日時を返す。"""
    # ログファイル名用とは別に、人間が読む stdout / JSONL 向けの形式へ整形する。
    source = now if now is not None else datetime.now()
    current = source.astimezone()
    return (
        f"{current.year:04d}/{current.month:02d}/{current.day:02d} "
        f"{current.hour:02d}:{current.minute:02d}:{current.second:02d}."
        f"{current.microsecond // 1000:03d}"
    )


def is_timestamp(value: str) -> bool:
    """cmoc の `<time-stamp>` 形式か判定する。"""
    match = TIMESTAMP_PATTERN.fullmatch(value)
    if match is None:
        return False

    msec = int(match["msec"])
    if msec > 999:
        return False

    try:
        datetime(
            int(match["year"]),
            int(match["month"]),
            int(match["day"]),
            int(match["hour"]),
            int(match["minute"]),
            int(match["second"]),
        )
    except ValueError:
        return False

    return True
