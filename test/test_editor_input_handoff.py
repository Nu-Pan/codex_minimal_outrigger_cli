"""editor input handoff target の lifecycle と上書き境界を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/editor_input_handoff.md
- {{work-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json
"""

import json
import socket
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_editor_input_handoff as handoff_module
import commons.runtime_editor_input_handoff_mcp as handoff_mcp
from commons.runtime_editor_input_handoff import (
    EditorInputHandoffTarget,
    start_editor_input_handoff,
)
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    EDITOR_INPUT_HANDOFF_TOKEN_BYTES,
    EDITOR_INPUT_REPOSITORY_ENV,
    authenticate_editor_input_handoff_client,
    authenticate_editor_input_handoff_server,
    build_editor_input_handoff_target_id,
    parse_editor_input_handoff_target_id,
    read_handoff_response,
)

_SKELETON = "# skeleton\n\n{{original-prompt-here}}\n"


def _start_slow_trickle(
    connection: socket.socket,
    byte: bytes,
    interval_seconds: float,
) -> tuple[threading.Event, threading.Thread]:
    """socket timeout より短い間隔で一 byte ずつ送り続ける。"""
    stopped = threading.Event()

    def send_slowly() -> None:
        while not stopped.wait(interval_seconds):
            try:
                connection.sendall(byte)
            except OSError:
                return

    connection.sendall(byte)
    thread = threading.Thread(target=send_slowly)
    thread.start()
    return stopped, thread


def test_editor_wait_accepts_only_active_repository_target_and_last_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """表示 target だけを待機中に受理し、最後の全面上書きを確定入力にする。"""
    editor_work, input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    displayed: list[str] = []
    results: list[dict[str, object]] = []
    monkeypatch.setattr(
        prompt_editor_input_module,
        "_select_editor",
        lambda: ["fake-editor"],
    )
    monkeypatch.setattr(
        prompt_editor_input_module,
        "print",
        lambda message, **_kwargs: displayed.append(str(message)),
        raising=False,
    )

    def fake_run(_argv: list[str]) -> SimpleNamespace:
        """editor 待機中に別 process 相当の MCP submission を送る。"""
        target_id = displayed[0].removeprefix("editor input handoff target ID: ")
        monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path / "other"))
        results.append(
            handoff_mcp._submit({"target_id": target_id, "content": "wrong repository"})
        )
        monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
        results.append(
            handoff_mcp._submit({"target_id": target_id, "content": "first"})
        )
        results.append(
            handoff_mcp._submit({"target_id": target_id, "content": "final input\n"})
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)
    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        editor_work,
        _SKELETON,
    )

    target_id = displayed[0].removeprefix("editor input handoff target ID: ")
    assert target_id.startswith("eit_")
    assert results[0]["status"] == "rejected"
    assert results[1:] == [{"status": "accepted"}, {"status": "accepted"}]
    assert "final input" not in json.dumps(results, ensure_ascii=False)
    assert editor_work.read_text(encoding="utf-8") == "final input\n"

    inactive = handoff_mcp._submit(
        {"target_id": target_id, "content": "must not be applied"}
    )
    assert inactive["status"] == "rejected"
    assert editor_work.read_text(encoding="utf-8") == "final input\n"
    assert (
        prompt_editor_input_module.collect_prompt_editor_input(
            tmp_path,
            editor_work,
            input_copy,
        )
        == "final input"
    )
    prompt_editor_input_module.finalize_prompt_editor_input(editor_work)


def test_handoff_revalidates_file_and_repository_on_each_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """repository 不一致と symlink 化を拒否し、リンク先へ書き込まない。"""
    editor_work, _input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    editor_work.write_text("initial", encoding="utf-8")
    target = start_editor_input_handoff(tmp_path, editor_work)
    try:
        request = {
            "protocol": EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
            "repository": str((tmp_path / "other").resolve()),
            "payload": {"target_id": target.target_id, "content": "wrong repo"},
        }
        route = parse_editor_input_handoff_target_id(tmp_path, target.target_id)
        assert route is not None
        address, token = route
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(2)
            connection.connect(address)
            assert authenticate_editor_input_handoff_client(connection, token, 2)
            connection.sendall(json.dumps(request).encode("utf-8") + b"\n")
            mismatch = read_handoff_response(connection, 2)
        assert mismatch is not None
        assert mismatch["code"] == "repository_mismatch"
        assert editor_work.read_text(encoding="utf-8") == "initial"

        outside = tmp_path / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        editor_work.unlink()
        editor_work.symlink_to(outside)
        monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
        rejected = handoff_mcp._submit(
            {"target_id": target.target_id, "content": "must not escape"}
        )
        assert rejected["status"] == "rejected"
        assert rejected["code"] == "write_failed"
        assert outside.read_text(encoding="utf-8") == "outside"
        assert "must not escape" not in json.dumps(rejected)
    finally:
        target.close()


def test_target_close_drains_an_accepted_submission(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """受付済み上書きが完了するまで close が target を破棄しない。"""
    editor_work, _input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    editor_work.write_text("initial", encoding="utf-8")
    entered = threading.Event()
    release = threading.Event()
    original_overwrite = EditorInputHandoffTarget._overwrite

    def delayed_overwrite(self: EditorInputHandoffTarget, content: str) -> None:
        """accepted 状態を保持したまま test が許可するまで write を待つ。"""
        entered.set()
        assert release.wait(2)
        original_overwrite(self, content)

    monkeypatch.setattr(EditorInputHandoffTarget, "_overwrite", delayed_overwrite)
    target = start_editor_input_handoff(tmp_path, editor_work)
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    submission_result: list[dict[str, object]] = []
    submitter = threading.Thread(
        target=lambda: submission_result.append(
            handoff_mcp._submit({"target_id": target.target_id, "content": "drained"})
        )
    )
    submitter.start()
    assert entered.wait(2)

    closed = threading.Event()

    def close_target() -> None:
        """close 完了を test thread へ通知する。"""
        target.close()
        closed.set()

    closer = threading.Thread(target=close_target)
    closer.start()
    assert not closed.wait(0.05)
    release.set()
    submitter.join(timeout=2)
    closer.join(timeout=2)

    assert closed.is_set()
    assert submission_result == [{"status": "accepted"}]
    assert editor_work.read_text(encoding="utf-8") == "drained"
    inactive = handoff_mcp._submit(
        {"target_id": target.target_id, "content": "must not be applied"}
    )
    assert inactive["status"] == "rejected"
    assert editor_work.read_text(encoding="utf-8") == "drained"


def test_client_does_not_send_content_to_unauthenticated_listener(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """server proof が不正なら request body を loopback peer へ渡さない。"""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen()
    address = listener.getsockname()
    assert isinstance(address, tuple)
    port = address[1]
    assert isinstance(port, int)
    target_token = b"\x01" * EDITOR_INPUT_HANDOFF_TOKEN_BYTES
    wrong_token = b"\x02" * EDITOR_INPUT_HANDOFF_TOKEN_BYTES
    target_id = build_editor_input_handoff_target_id(tmp_path, port, target_token)
    observed: list[tuple[bool, bytes]] = []

    def serve_without_capability() -> None:
        """別 capability の proof 後に client から届く byte を記録する。"""
        with listener:
            connection, _ = listener.accept()
            with connection:
                connection.settimeout(2)
                authenticated = authenticate_editor_input_handoff_server(
                    connection,
                    wrong_token,
                    2,
                )
                connection.shutdown(socket.SHUT_WR)
                observed.append((authenticated, connection.recv(8192)))

    server_thread = threading.Thread(target=serve_without_capability)
    server_thread.start()
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))

    result = handoff_mcp._submit({"target_id": target_id, "content": "private content"})
    server_thread.join(timeout=2)

    assert not server_thread.is_alive()
    assert observed == [(False, b"")]
    assert result["status"] == "rejected"
    assert result["code"] == "transport_unavailable"
    assert "private content" not in json.dumps(result)


def test_target_deadline_releases_unauthenticated_slow_trickle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """proof の slow-trickle を絶対期限で切り、次の submission を処理する。"""
    editor_work, _input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    monkeypatch.setattr(
        handoff_module,
        "EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS",
        0.2,
    )
    target = start_editor_input_handoff(tmp_path, editor_work)
    route = parse_editor_input_handoff_target_id(tmp_path, target.target_id)
    assert route is not None
    address, _token = route
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stalled:
            stalled.settimeout(2)
            stalled.connect(address)
            assert stalled.recv(1)
            stopped, trickler = _start_slow_trickle(stalled, b"x", 0.05)
            try:
                time.sleep(0.3)
                monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
                result = handoff_mcp._submit(
                    {"target_id": target.target_id, "content": "after deadline"}
                )
            finally:
                stopped.set()
                trickler.join(timeout=2)
        assert result == {"status": "accepted"}
        assert editor_work.read_text(encoding="utf-8") == "after deadline"
    finally:
        target.close()


def test_target_deadline_releases_authenticated_request_slow_trickle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """認証後 request の slow-trickle を切り、次の submission を処理する。"""
    editor_work, _input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    monkeypatch.setattr(
        handoff_module,
        "EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS",
        0.2,
    )
    target = start_editor_input_handoff(tmp_path, editor_work)
    route = parse_editor_input_handoff_target_id(tmp_path, target.target_id)
    assert route is not None
    address, token = route
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stalled:
            stalled.settimeout(2)
            stalled.connect(address)
            assert authenticate_editor_input_handoff_client(stalled, token, 2)
            stopped, trickler = _start_slow_trickle(stalled, b"x", 0.05)
            try:
                time.sleep(0.3)
                monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
                result = handoff_mcp._submit(
                    {"target_id": target.target_id, "content": "after deadline"}
                )
            finally:
                stopped.set()
                trickler.join(timeout=2)
        assert result == {"status": "accepted"}
        assert editor_work.read_text(encoding="utf-8") == "after deadline"
    finally:
        target.close()
