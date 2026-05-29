"""レポートファイル保存ヘルパーのテスト。"""

from pathlib import Path

from pytest import MonkeyPatch

from commons import report_files
from commons.report_files import write_timestamped_report


def test_write_timestamped_report_retries_without_overwriting(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """timestamp 衝突時は既存 report を上書きせず別名で保存する。"""
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    existing = report_dir / "2026-05-04_03-02_01_000000987.md"
    existing.write_text("existing report\n", encoding="utf-8")
    timestamps = iter(
        [
            "2026-05-04_03-02_01_000000987",
            "2026-05-04_03-02_01_000000988",
        ]
    )
    monkeypatch.setattr(
        report_files,
        "make_timestamp",
        lambda: next(timestamps),
    )

    created = write_timestamped_report(
        report_dir,
        lambda generated_at: f"generated_at: {generated_at}\n",
    )

    assert created == report_dir / "2026-05-04_03-02_01_000000988.md"
    assert existing.read_text(encoding="utf-8") == "existing report\n"
    assert created.read_text(encoding="utf-8") == (
        "generated_at: 2026-05-04_03-02_01_000000988\n"
    )
