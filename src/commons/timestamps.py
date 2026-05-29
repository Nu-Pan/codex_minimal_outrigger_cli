"""cmoc 仕様のタイムスタンプ生成。"""

from datetime import datetime


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
