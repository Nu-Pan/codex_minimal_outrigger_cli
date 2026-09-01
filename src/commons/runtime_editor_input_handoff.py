"""prompt editor input handoff の一時 target と IPC 境界。"""

import json
import os
import secrets
import socket
import stat
import threading
import time
from pathlib import Path

from .runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS,
    EDITOR_INPUT_HANDOFF_HOST,
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    EDITOR_INPUT_HANDOFF_TOKEN_BYTES,
    EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS,
    authenticate_editor_input_handoff_server,
    build_editor_input_handoff_target_id,
    overwrite_input_is_valid,
)
from .runtime_errors import CmocError
from .runtime_paths import editor_work_dir


def validate_editor_work_file(root: Path, path: Path) -> None:
    """対象を所定 editor work directory 内の regular non-symlink file に限る。"""
    expected_dir = editor_work_dir(root)
    try:
        resolved_dir = expected_dir.resolve(strict=True)
        mode = path.lstat().st_mode
    except (OSError, RuntimeError) as exc:
        raise _invalid_editor_work_file(path, "path is not readable") from exc
    if not stat.S_ISREG(mode):
        raise _invalid_editor_work_file(path, "path is not a regular file")
    try:
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_dir)
    except (OSError, RuntimeError, ValueError) as exc:
        raise _invalid_editor_work_file(
            path,
            f"path is outside editor work directory: {expected_dir}",
        ) from exc


def _invalid_editor_work_file(path: Path, reason: str) -> CmocError:
    """不正な editor work file 用の利用者向けエラーを構築する。"""
    return CmocError(
        "editor work file を読み取れません。",
        ["復旧用に残った editor work file を確認してから再実行してください。"],
        f"path: {path}\nreason: {reason}",
    )


def _accepted() -> dict[str, object]:
    """content を含まない handoff 成功結果を返す。"""
    return {"status": "accepted"}


def _rejected(code: str, message: str, retryable: bool) -> dict[str, object]:
    """content を含まない handoff 失敗結果を返す。"""
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


class EditorInputHandoffTarget:
    """一つの editor work file だけを editor 待機中に公開する target。"""

    def __init__(self, repository: Path, editor_work_path: Path) -> None:
        """target identity と一時 transport state を初期化する。"""
        self.repository = repository.resolve()
        self.editor_work_path = editor_work_path
        self._token = secrets.token_bytes(EDITOR_INPUT_HANDOFF_TOKEN_BYTES)
        self._target_id: str | None = None
        self._state_lock = threading.Lock()
        self._listener: socket.socket | None = None
        self._server_thread: threading.Thread | None = None
        self._current_connection: socket.socket | None = None
        self._current_submission_accepted = False
        self._accepting = False
        self._closed = False

    @property
    def target_id(self) -> str:
        """active target の opaque capability-bearing ID を返す。"""
        if self._target_id is None:
            raise RuntimeError("editor input handoff target is not active")
        return self._target_id

    def start(self) -> None:
        """認証付き loopback TCP で active target を開始する。"""
        validate_editor_work_file(self.repository, self.editor_work_path)
        # Codex CLI 0.151.0 の ProxyRouted sandbox は AF_INET を許可し、
        # AF_UNIX socket の生成を拒否する。
        # https://github.com/openai/codex/blob/78c290807ce710180111df227df3b7a4fe845452/codex-rs/linux-sandbox/src/landlock.rs#L170-L248
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listener.bind((EDITOR_INPUT_HANDOFF_HOST, 0))
            listener.listen()
            listener.settimeout(0.1)
            bound_address = listener.getsockname()
            assert isinstance(bound_address, tuple)
            port = bound_address[1]
            assert isinstance(port, int)
            target_id = build_editor_input_handoff_target_id(
                self.repository,
                port,
                self._token,
            )
        except BaseException:
            listener.close()
            raise
        with self._state_lock:
            self._listener = listener
            self._target_id = target_id
            self._accepting = True
        self._server_thread = threading.Thread(
            target=self._serve,
            name=f"cmoc-editor-input-loopback-{port}",
            daemon=True,
        )
        try:
            self._server_thread.start()
        except BaseException:
            with self._state_lock:
                self._accepting = False
                self._listener = None
                self._server_thread = None
            listener.close()
            raise

    def close(self) -> None:
        """新規受付を止め、受付済み submission 完了後に target を無効化する。"""
        with self._state_lock:
            if self._closed:
                return
            self._closed = True
            self._accepting = False
            listener = self._listener
            pending_connection = (
                self._current_connection
                if not self._current_submission_accepted
                else None
            )
        if listener is not None:
            listener.close()
        if pending_connection is not None:
            try:
                pending_connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        if self._server_thread is not None:
            self._server_thread.join()

    def _serve(self) -> None:
        """submission を一接続ずつ処理して同一 target の上書きを直列化する。"""
        assert self._listener is not None
        while True:
            with self._state_lock:
                if not self._accepting:
                    return
            try:
                connection, _ = self._listener.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            with self._state_lock:
                if not self._accepting:
                    connection.close()
                    return
                self._current_connection = connection
                self._current_submission_accepted = False
            try:
                with connection:
                    if not authenticate_editor_input_handoff_server(
                        connection,
                        self._token,
                        EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS,
                    ):
                        continue
                    result = self._handle_connection(
                        connection,
                        EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS,
                    )
                    connection.settimeout(
                        EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS
                    )
                    connection.sendall(
                        json.dumps(
                            result,
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ).encode("utf-8")
                        + b"\n"
                    )
            except OSError:
                pass
            finally:
                with self._state_lock:
                    self._current_connection = None
                    self._current_submission_accepted = False

    def _handle_connection(
        self,
        connection: socket.socket,
        timeout_seconds: float,
    ) -> dict[str, object]:
        """一つの IPC request を検証し、active target へ適用する。"""
        try:
            deadline = time.monotonic() + timeout_seconds
            request_data = b""
            while b"\n" not in request_data:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("editor input handoff deadline exceeded")
                connection.settimeout(remaining)
                chunk = connection.recv(8192)
                if not chunk:
                    break
                request_data += chunk
            request = json.loads(request_data.split(b"\n", 1)[0])
        except (OSError, UnicodeError, json.JSONDecodeError):
            return _rejected("protocol_mismatch", "invalid handoff request", False)
        if not isinstance(request, dict):
            return _rejected("protocol_mismatch", "invalid handoff request", False)
        if request.get("protocol") != EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION:
            return _rejected("protocol_mismatch", "handoff protocol mismatch", False)
        if request.get("repository") != str(self.repository):
            return _rejected(
                "repository_mismatch",
                "target belongs to a different repository",
                False,
            )
        payload = request.get("payload")
        if not overwrite_input_is_valid(payload):
            return _rejected("invalid_input", "tool input does not match schema", False)
        assert isinstance(payload, dict)
        if payload["target_id"] != self.target_id:
            return _rejected("target_unavailable", "target is not active", False)
        with self._state_lock:
            if not self._accepting:
                return _rejected("target_unavailable", "target is not active", False)
            self._current_submission_accepted = True
        content = payload["content"]
        assert isinstance(content, str)
        try:
            self._overwrite(content)
        except (CmocError, OSError, UnicodeError):
            return _rejected("write_failed", "editor input overwrite failed", False)
        return _accepted()

    def _overwrite(self, content: str) -> None:
        """target を再検証し、同じ regular file 全体を UTF-8 content で置換する。"""
        content_bytes = content.encode("utf-8")
        validate_editor_work_file(self.repository, self.editor_work_path)
        flags = (
            os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(self.editor_work_path, flags)
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise OSError("editor input target is not a regular file")
            os.ftruncate(descriptor, 0)
            remaining = memoryview(content_bytes)
            while remaining:
                written = os.write(descriptor, remaining)
                if written == 0:
                    raise OSError("editor input overwrite made no progress")
                remaining = remaining[written:]
        finally:
            os.close(descriptor)


def start_editor_input_handoff(
    repository: Path,
    editor_work_path: Path,
) -> EditorInputHandoffTarget:
    """editor 待機期間に使う一時 handoff target を開始する。"""
    target = EditorInputHandoffTarget(repository, editor_work_path)
    try:
        target.start()
    except Exception as exc:
        target.close()
        raise CmocError(
            "editor input handoff target を開始できませんでした。",
            [
                "local transport の状態を確認してから cmoc コマンドを再実行してください。"
            ],
            f"transport: {EDITOR_INPUT_HANDOFF_HOST} の一時 port",
        ) from exc
    return target
