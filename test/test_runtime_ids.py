"""Repository 共通 ID の発行順と種類別採番を検証する。"""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pytest

import commons.runtime_ids as runtime_ids


def test_ids_keep_issue_order_when_clock_moves_backward(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """発行時刻が巻き戻っても、同種 ID の辞書順と発行順が一致する。"""
    times = iter(
        [
            datetime(2026, 9, 29, 15, 4),
            datetime(2026, 9, 29, 15, 3),
            datetime(2026, 9, 29, 15, 2),
            datetime(2026, 9, 29, 15, 1),
        ]
    )

    class Clock:
        @staticmethod
        def now() -> datetime:
            return next(times)

        @staticmethod
        def strptime(value: str, format_string: str) -> datetime:
            return datetime.strptime(value, format_string)

    monkeypatch.setattr(runtime_ids, "datetime", Clock)
    first = runtime_ids.new_id(tmp_path, "exec")
    second = runtime_ids.new_id(tmp_path, "exec")
    independent = runtime_ids.new_id(tmp_path, "cc")

    assert first == "exec_000000_2026-09-29_15-04"
    assert second == "exec_000001_2026-09-29_15-03"
    assert independent == "cc_000000_2026-09-29_15-02"
    assert first < second
    assert runtime_ids.is_common_id(second, "exec")
    assert not runtime_ids.is_common_id(second, "cc")
    assert runtime_ids.new_id(tmp_path / "other-repository", "exec").startswith(
        "exec_000000_"
    )


def test_sequence_survives_artifact_removal(tmp_path: Path) -> None:
    """ログなどの成果物が存在しなくても、確定済み番号を再利用しない。"""
    first = runtime_ids.new_id(tmp_path, "sess")
    artifact = tmp_path / ".cmoc/gu/log/sub_command" / f"{first}.jsonl"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("{}\n")
    artifact.unlink()
    second = runtime_ids.new_id(tmp_path, "sess")

    assert first.startswith("sess_000000_")
    assert second.startswith("sess_000001_")
    assert runtime_ids.is_common_id(second, "sess")
    for _ in range(34):
        last = runtime_ids.new_id(tmp_path, "sess")
    assert last.startswith("sess_00000z_")
    assert runtime_ids.new_id(tmp_path, "sess").startswith("sess_000010_")


def test_parallel_processes_share_one_sequence(tmp_path: Path) -> None:
    """同じ repository の別 process が同時に発行しても通番が重複しない。"""
    source_root = Path(runtime_ids.__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(source_root), environment.get("PYTHONPATH")) if part
    )
    script = (
        "import sys; from pathlib import Path; "
        "from commons.runtime_ids import new_id; "
        "print('\\n'.join(new_id(Path(sys.argv[1]), 'cc') for _ in range(8)))"
    )

    def issue_batch(_: int) -> list[str]:
        process = subprocess.run(
            [sys.executable, "-c", script, str(tmp_path)],
            env=environment,
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
        return process.stdout.splitlines()

    with ThreadPoolExecutor(max_workers=4) as pool:
        issued = [item for batch in pool.map(issue_batch, range(4)) for item in batch]

    assert len(issued) == 32
    assert sorted(int(item.split("_")[1], 36) for item in issued) == list(range(32))
    assert runtime_ids.new_id(tmp_path, "cc").startswith("cc_00000w_")
