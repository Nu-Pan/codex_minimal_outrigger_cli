"""cmoc レポートファイルの保存ヘルパー。"""

from collections.abc import Callable
from pathlib import Path
from time import sleep

from .timestamps import make_timestamp


def write_timestamped_report(
    report_dir: Path,
    build_report: Callable[[str], str],
) -> Path:
    """未使用の `<time-stamp>.md` を排他的に作成してレポートを保存する。"""
    report_dir.mkdir(parents=True, exist_ok=True)
    for _ in range(1000):
        generated_at = make_timestamp()
        report_path = report_dir / f"{generated_at}.md"
        created = False
        try:
            with report_path.open("x", encoding="utf-8") as report_file:
                created = True
                report_file.write(build_report(generated_at))
            return report_path
        except FileExistsError:
            sleep(0.001)
        except Exception:
            if created:
                report_path.unlink(missing_ok=True)
            raise
    raise RuntimeError("未使用の timestamp report path を作成できませんでした。")
