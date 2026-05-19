"""タイムスタンプ仕様のテスト。"""

from datetime import datetime

from commons.timing import format_duration
from commons.timestamps import make_timestamp


def test_make_timestamp_uses_required_format() -> None:
    """ゼロ埋めされた cmoc timestamp を生成する。"""
    assert make_timestamp(datetime(2026, 5, 4, 3, 2, 1, 987654)) == (
        "2026-05-04_03-02_01_987"
    )


def test_format_duration_uses_required_stdout_format() -> None:
    """時間表示は hour/min/sec と 1 桁小数切り捨てで出す。"""
    assert format_duration(0.199) == " 0h  0m  0.1s"
    assert format_duration(3661.987) == " 1h  1m  1.9s"
