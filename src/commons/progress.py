"""cmot の実行時進捗ログ。"""

import time


def progress(message: str) -> None:
    """ユーザー向けの短い進捗ログを標準出力へ流す。"""
    print(f"cmot: {message}", flush=True)


def start_timer() -> float:
    """所要時間計測用の開始時刻を返す。"""
    return time.monotonic()


def format_elapsed(started_at: float) -> str:
    """開始時刻からの経過時間をログ表示用に整形する。"""
    elapsed = time.monotonic() - started_at
    if elapsed < 60:
        return f"{elapsed:.1f}s"

    minutes = int(elapsed // 60)
    seconds = elapsed - (minutes * 60)
    return f"{minutes}m {seconds:.1f}s"
