"""タイムスタンプ仕様のテスト。"""

from datetime import datetime

from commons.timestamps import make_timestamp


def test_make_timestamp_uses_required_format() -> None:
    """ゼロ埋めされた cmoc timestamp を生成する。"""
    assert make_timestamp(datetime(2026, 5, 4, 3, 2, 1, 987654)) == (
        "2026-05-04_03-02_01_987"
    )
