"""タイムスタンプ仕様のテスト。"""

import os
import time
from datetime import datetime, timezone
from inspect import getsourcelines
from pathlib import Path

import pytest

from commons.timing import current_timer, format_duration, report_current_timer
from commons.timestamps import console_timestamp, is_timestamp, make_timestamp


def test_make_timestamp_uses_required_format() -> None:
    """ゼロ埋めされた cmoc timestamp を生成する。"""
    assert make_timestamp(datetime(2026, 5, 4, 3, 2, 1, 987654)) == (
        "2026-05-04_03-02_01_000000987"
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
            "2026-05-04_03-02_01_000000987"
        )
    finally:
        if original_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = original_tz
        tzset()


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-05-04_03-02_01_000000987", True),
        ("2026-02-29_03-02_01_000000987", False),
        ("2028-02-29_03-02_01_000000987", True),
        ("2026-00-04_03-02_01_000000987", False),
        ("2026-13-04_03-02_01_000000987", False),
        ("2026-05-00_03-02_01_000000987", False),
        ("2026-05-32_03-02_01_000000987", False),
        ("2026-05-04_24-02_01_000000987", False),
        ("2026-05-04_03-60_01_000000987", False),
        ("2026-05-04_03-02_60_000000987", False),
        ("2026-05-04_03-02_01_000000999", True),
        ("2026-05-04_03-02_01_000001000", False),
        ("2026-05-04_03-02_01_987", False),
        ("2026-05-04_03-02-01_000000987", False),
        ("run-1", False),
    ],
)
def test_is_timestamp(value: str, expected: bool) -> None:
    """cmoc timestamp 形式だけを受け入れる。"""
    assert is_timestamp(value) is expected


def test_console_timestamp_uses_required_log_format() -> None:
    """コンソールログ用 timestamp を公開 API で生成する。"""
    assert console_timestamp(datetime(2026, 5, 4, 3, 2, 1, 987654)) == (
        "2026/05/04 03:02:01.987"
    )


def test_timing_does_not_import_private_subcommand_log_timestamp() -> None:
    """timing は subcommand_log の非公開 timestamp helper に依存しない。"""
    import commons.timing as timing_module

    source = Path(timing_module.__file__).read_text(encoding="utf-8")
    forbidden_name = "_" + "console_timestamp"
    assert forbidden_name not in source


def test_format_duration_uses_required_stdout_format() -> None:
    """時間表示は hour/min/sec と 1 桁小数切り捨てで出す。"""
    assert format_duration(0.199) == " 0h  0m  0.1s"
    assert format_duration(3661.987) == " 1h  1m  1.9s"


def test_timing_helpers_are_ordered_caller_first() -> None:
    """同一ファイル内の呼び出し関係は caller first, callee last で並べる。"""
    _, report_line = getsourcelines(report_current_timer)
    _, current_line = getsourcelines(current_timer)

    assert report_line < current_line
