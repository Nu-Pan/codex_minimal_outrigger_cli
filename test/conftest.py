"""pytest process と子 process の Windows toast 外部副作用を隔離する。"""

import json
import os
from pathlib import Path

import pytest
from oracle.editor_input_handoff.body import EditorInputHandoffSource
from oracle.other.document_search import INITIAL_SEARCH_MATERIALS

import commons.runtime_doctor as runtime_doctor
import commons.runtime_document_search as runtime_document_search
import commons.runtime_windows_toast as runtime_windows_toast
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_SOURCE_ENV


@pytest.fixture(autouse=True)
def _isolate_windows_toast_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """test が利用者の Windows 通知履歴へ toast を残さないようにする。"""
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    # subprocess callback も同じ隔離先を使えるよう、PATH に fake transport を置く。
    executable = tmp_path / "toast-bin" / "powershell.exe"
    executable.parent.mkdir()
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", f"{executable.parent}:{os.environ.get('PATH', '')}")
    monkeypatch.setattr(runtime_windows_toast, "_WINDOWS_POWERSHELL", executable)
    monkeypatch.setattr(
        runtime_windows_toast,
        "_run_windows_toast_transport",
        lambda _title, _message: True,
    )


@pytest.fixture(autouse=True)
def _isolate_document_search_materials(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """一般 CLI test では大容量モデルと installation の共有領域に触れない。"""
    monkeypatch.setattr(runtime_doctor, "_installation_root", lambda root: root)
    monkeypatch.setattr(runtime_document_search, "cmoc_root", lambda: tmp_path)
    monkeypatch.setattr(runtime_doctor, "_check_common_environment", lambda: None)
    monkeypatch.setattr(
        runtime_doctor,
        "prepare_document_search_materials",
        lambda root, _config: {
            "status": "validated",
            "path": str(root / ".cmoc/gu/document_search/materials"),
            "models": "reused",
        },
    )
    monkeypatch.setattr(
        runtime_doctor,
        "require_document_search_materials",
        lambda root, _config: root / ".cmoc/gu/document_search/materials",
    )

    class _DoctorInference:
        """doctor 経路では実モデルを使わず、索引同期自体は実行する。"""

        def stream_chunks(
            self, documents, resumes, on_event, *, deadline, residency_fd, cancelled
        ):
            vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)
            for path, source in documents.items():
                if resumes[path] == 0:
                    on_event(
                        {
                            "kind": "chunk",
                            "path": path,
                            "ordinal": 0,
                            "start": 0,
                            "end": len(source),
                            "embedding": vector,
                        }
                    )
                on_event({"kind": "document_complete", "path": path, "chunk_count": 1})

    def doctor_search(root, scope, config, *, installation_root, use_saved_config):
        return runtime_document_search.DocumentSearch(
            root,
            scope,
            config,
            worker=_DoctorInference(),
            installation_root=installation_root,
            use_saved_config=use_saved_config,
        )

    monkeypatch.setattr(runtime_doctor, "DocumentSearch", doctor_search)


@pytest.fixture
def handoff_source(tmp_path, monkeypatch):
    """実行中の送信側 TUI に結び付いた MCP context を用意する。"""
    source = EditorInputHandoffSource(
        "oracle investigation", "sci_sender", "cdc_sender", tmp_path / "sender.jsonl"
    )
    monkeypatch.setenv(
        EDITOR_INPUT_SOURCE_ENV,
        json.dumps(
            {
                "subcommand": source.subcommand,
                "execution_id": source.execution_id,
                "codex_call_id": source.codex_call_id,
                "sub_command_log_path": str(source.sub_command_log_path),
            }
        ),
    )
    return source
