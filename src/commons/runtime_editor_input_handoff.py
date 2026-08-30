"""prompt editor input handoff の一時 target と IPC 境界。"""

import json
import os
import secrets
import socket
import stat
import threading
from pathlib import Path

from .runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    editor_input_handoff_socket_path,
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
        self.target_id = f"eit_{secrets.token_hex(16)}"
        self.socket_path = editor_input_handoff_socket_path(
            self.repository,
            self.target_id,
        )
        self._state_lock = threading.Lock()
        self._listener: socket.socket | None = None
        self._server_thread: threading.Thread | None = None
        self._current_connection: socket.socket | None = None
        self._current_submission_accepted = False
        self._accepting = False
        self._closed = False

    def start(self) -> None:
        """owner-only Unix socket で active target を開始する。"""
        validate_editor_work_file(self.repository, self.editor_work_path)
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        bound = False
        try:
            listener.bind(str(self.socket_path))
            bound = True
            os.chmod(self.socket_path, 0o600)
            listener.listen()
            listener.settimeout(0.1)
        except BaseException:
            listener.close()
            if bound:
                self.socket_path.unlink(missing_ok=True)
            raise
        with self._state_lock:
            self._listener = listener
            self._accepting = True
        self._server_thread = threading.Thread(
            target=self._serve,
            name=f"cmoc-editor-input-{self.target_id}",
            daemon=True,
        )
        self._server_thread.start()

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
        self.socket_path.unlink(missing_ok=True)

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
                    connection.settimeout(10)
                    result = self._handle_connection(connection)
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

    def _handle_connection(self, connection: socket.socket) -> dict[str, object]:
        """一つの IPC request を検証し、active target へ適用する。"""
        try:
            request_data = b""
            while b"\n" not in request_data:
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
        raise CmocError(
            "editor input handoff target を開始できませんでした。",
            ["一時 socket の状態を確認してから cmoc コマンドを再実行してください。"],
            f"socket: {target.socket_path}",
        ) from exc
    return target
