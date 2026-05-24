"""タイムスタンプ仕様のテスト。"""

import os
import time
from datetime import datetime, timezone
from inspect import getsourcelines

import pytest

from commons.timing import current_timer, format_duration, report_current_timer
from commons.timestamps import make_timestamp


def test_make_timestamp_uses_required_format() -> None:
    """ゼロ埋めされた cmoc timestamp を生成する。"""
    assert make_timestamp(datetime(2026, 5, 4, 3, 2, 1, 987654)) == (
        "2026-05-04_03-02_01_987"
    )


def test_make_timestamp_converts_aware_datetime_to_local_timezone() -> None:
    """aware datetime はローカルタイムゾーンに変換してから整形する。"""
    tzset = getattr(time, "tzset", None)
    if tzset is None:
        pytest.skip("time.tzset is not available on this platform")

    original_tz = os.environ.get("TZ")
    os.environ["TZ"] = "Asia/Tokyo"
    tzset()

    try:
        timestamp = datetime(2026, 5, 3, 18, 2, 1, 987654, timezone.utc)
        assert make_timestamp(timestamp) == (
            "2026-05-04_03-02_01_987"
        )
    finally:
        if original_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = original_tz
        tzset()


def test_format_duration_uses_required_stdout_format() -> None:
    """時間表示は hour/min/sec と 1 桁小数切り捨てで出す。"""
    assert format_duration(0.199) == " 0h  0m  0.1s"
    assert format_duration(3661.987) == " 1h  1m  1.9s"


def test_timing_helpers_are_ordered_caller_first() -> None:
    """同一ファイル内の呼び出し関係は caller first, callee last で並べる。"""
    _, report_line = getsourcelines(report_current_timer)
    _, current_line = getsourcelines(current_timer)

    assert report_line < current_line
