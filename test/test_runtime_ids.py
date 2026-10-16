"""Repository 共通 ID の発行順と種類別採番を検証する。

process 間の共有・永続性とログ削除後の非再利用は test_codex_runtime_paths.py の
test_codex_call_ids_are_process_safe_on_same_timestamp でログとの結合も検証する。
"""

import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

import pytest

import commons.runtime_ids as runtime_ids


@pytest.mark.parametrize(
    ("issued_at", "valid"),
    [
        ("0001-01-01_00-00", True),
        ("2000-02-29_23-59", True),
        ("9999-12-31_23-59", True),
        ("0000-01-01_00-00", False),
        ("1900-02-29_00-00", False),
        ("2026-02-29_00-00", False),
        ("2026-04-31_00-00", False),
        ("2026-00-01_00-00", False),
        ("2026-13-01_00-00", False),
        ("2026-01-00_00-00", False),
        ("2026-01-32_00-00", False),
        ("2026-01-01_24-00", False),
        ("2026-01-01_00-60", False),
    ],
)
def test_common_id_requires_real_calendar_datetime(issued_at: str, valid: bool) -> None:
    """固定書式に一致しても、実在しない暦日や時刻は受理しない。"""
    assert runtime_ids.is_common_id(f"exec_000000_{issued_at}", "exec") is valid


def test_ids_keep_issue_order_when_clock_moves_backward(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """年の固定幅と、発行時刻の巻き戻りに依存しない採番順を保つ。"""
    times = iter(
        [
            datetime(1, 2, 3, 4, 5),
            datetime(1, 2, 3, 4, 4),
            datetime(1, 2, 3, 4, 3),
            datetime(1, 2, 3, 4, 2),
        ]
    )

    class Clock(datetime):
        @staticmethod
        def now() -> datetime:
            return next(times)

    monkeypatch.setattr(runtime_ids, "datetime", Clock)
    first = runtime_ids.new_id(tmp_path, "exec")
    second = runtime_ids.new_id(tmp_path, "exec")
    independent = runtime_ids.new_id(tmp_path, "cc")

    assert first == "exec_000000_0001-02-03_04-05"
    assert second == "exec_000001_0001-02-03_04-04"
    assert independent == "cc_000000_0001-02-03_04-03"
    assert first < second
    assert runtime_ids.is_common_id(second, "exec")
    assert not runtime_ids.is_common_id(second, "cc")
    assert runtime_ids.new_id(tmp_path / "other-repository", "exec").startswith(
        "exec_000000_"
    )


@pytest.mark.parametrize(
    ("sequence", "before", "after"),
    [(9, "000009", "00000a"), (35, "00000z", "000010")],
)
def test_sequence_crosses_base36_boundaries(
    tmp_path: Path, sequence: int, before: str, after: str
) -> None:
    """数字から英字への遷移と桁上がりでも、固定幅と辞書順を保つ。"""
    runtime_ids.new_id(tmp_path, "sess")
    # 途中の通番を発行せず、永続状態を境界直前へ進める。
    database = tmp_path / ".cmoc/gu/state/id_sequences.sqlite3"
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            "UPDATE sequence SET next_value = ? WHERE prefix = ?", (sequence, "sess")
        )
        connection.commit()

    first = runtime_ids.new_id(tmp_path, "sess")
    second = runtime_ids.new_id(tmp_path, "sess")

    assert first.startswith(f"sess_{before}_")
    assert second.startswith(f"sess_{after}_")
    assert first < second
