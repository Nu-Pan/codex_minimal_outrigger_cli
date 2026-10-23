"""固定した Codex session ID の使用を process 終了確認まで確保する。"""

import fcntl
import hashlib
import os
from pathlib import Path
from typing import IO

from .runtime_errors import CmocError


class CodexSessionLease:
    """repository をまたいだ同じ CODEX_HOME・session の競合を拒否する。"""

    def __init__(self, codex_home: Path) -> None:
        """ID の取得前から初回 exec と TUI の終了まで同じ所有者を使う。"""
        # cwd や repository が異なっても、同じ実体の home を同じ key にする。
        self._home = codex_home.resolve()
        self._session_id: str | None = None
        self._file: IO[str] | None = None
        self._stopped = True

    def acquire(self, session_id: str) -> None:
        """初めて取得した ID を確保し、自動移行中はその確保を引き継ぐ。"""
        # 同じ呼び出しからの再確認は許容し、別会話への置き換えはしない。
        if self._session_id == session_id:
            return
        if self._session_id is not None:
            raise ValueError("initial session ID changed")
        directory = Path("/tmp") / f"cmoc-codex-sessions-{os.getuid()}"
        directory.mkdir(mode=0o700, exist_ok=True)
        if directory.is_symlink() or directory.stat().st_uid != os.getuid():
            raise OSError(f"session lock directory is not owned: {directory}")
        digest = hashlib.sha256(f"{self._home}\0{session_id}".encode()).hexdigest()
        path = directory / f"{digest}.lock"
        descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        stream = os.fdopen(descriptor, "r+", encoding="utf-8")
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if stream.read():
                raise BlockingIOError("previous process exit is unconfirmed")
            stream.write("active\n")
            stream.flush()
        except BaseException as exc:
            stream.close()
            if isinstance(exc, BlockingIOError):
                raise CmocError(
                    "同じ Codex session ID が使用中、または終了未確認です。",
                    ["先行する実行と関連 process の終了記録を確認してください。"],
                    f"CODEX_HOME: {self._home}\nsession_id: {session_id}\nlock: {path}",
                ) from exc
            raise
        self._file = stream
        self._session_id = session_id

    def process_started(self) -> None:
        """使用中 process の停止はまだ確認できていないと記録する。"""
        # 起動前や停止確認後の状態からだけ、未確認へ進める。
        self._stopped = False

    def process_stopped(self) -> None:
        """process の終了コードを取得できた経路からだけ解放を許可する。"""
        # 初回終了後も lease 自体は次の TUI へ保持する。
        self._stopped = True

    def close(self) -> None:
        """停止確認済みなら解放し、未確認なら拒否用の記録を残す。"""
        # parent の強制終了や停止確認失敗を、時間経過だけで解除しない。
        if self._file is not None:
            try:
                if self._stopped:
                    self._file.seek(0)
                    self._file.truncate()
                    self._file.flush()
            finally:
                self._file.close()
                self._file = None
