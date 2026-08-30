"""editor input handoff target の lifecycle と上書き境界を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/editor_input_handoff.md
- {{work-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json
"""

import json
import socket
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_editor_input_handoff_mcp as handoff_mcp
from commons.runtime_editor_input_handoff import (
    EditorInputHandoffTarget,
    start_editor_input_handoff,
)
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    EDITOR_INPUT_REPOSITORY_ENV,
    read_handoff_response,
)

_SKELETON = "# skeleton\n\n{{original-prompt-here}}\n"


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
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.connect(str(target.socket_path))
            connection.sendall(json.dumps(request).encode("utf-8") + b"\n")
            mismatch = read_handoff_response(connection)
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
    closer = threading.Thread(target=lambda: (target.close(), closed.set()))
    closer.start()
    assert not closed.wait(0.05)
    release.set()
    submitter.join(timeout=2)
    closer.join(timeout=2)

    assert closed.is_set()
    assert submission_result == [{"status": "accepted"}]
    assert editor_work.read_text(encoding="utf-8") == "drained"
    assert not target.socket_path.exists()
