"""共通 fixture で CLI repository と外部副作用を隔離する。"""

import json
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from _git_support import init_repo
from oracle.editor_input_handoff.body import EditorInputHandoffSource

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_cli as runtime_cli
import commons.runtime_doctor as runtime_doctor
import commons.runtime_document_search as runtime_document_search
import commons.runtime_document_search_observation as observation_module
import commons.runtime_download_asset_cache as asset_cache_module
import commons.runtime_feedback as runtime_feedback
import commons.runtime_windows_toast as runtime_windows_toast
from commons.runtime_document_search_types import SEARCH_MATERIALS
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_SOURCE_ENV


@pytest.fixture
def cli_repository(tmp_path: Path) -> Path:
    """履歴を参照しない CLI lifecycle test に実 Git root を用意する。"""
    # root 解決とログ・report 保存は実経路を通し、追跡ファイルと初期 commit は作らない。
    root = tmp_path / "repo"
    root.mkdir()
    init_repo(root)
    return root


@pytest.fixture
def cli_terminal_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """表示・通知・前処理失敗の検査では Git 探索と collector 起動を外す。"""
    # 実 Git の cwd・linked worktree 境界は test_runtime_cli.py で検証する。
    # collector の TCP 受付・保存・drain は test_feedback.py に残す。
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.chdir(root)
    monkeypatch.setattr(runtime_cli, "work_root", lambda: root)
    monkeypatch.setattr(runtime_cli, "repo_root", lambda: root)
    monkeypatch.setattr(
        runtime_cli, "start_feedback_invocation", lambda *_args: (None, None)
    )
    return root


@pytest.fixture
def handoff_start(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """保存・editor 制御の検査では TCP lifecycle を専用の結合テストへ委ねる。"""
    # 実 target の登録・guide・無効化は test_editor_input_handoff.py に残す。
    target = SimpleNamespace(target_id="eit_000000_2026-09-29_15-04", close=Mock())
    start = Mock(return_value=target)
    monkeypatch.setattr(prompt_editor_input_module, "start_editor_input_handoff", start)
    return start


@pytest.fixture(autouse=True)
def _isolate_download_asset_cache(request, monkeypatch):
    """固定 cache パスをテスト内に置換し、実ユーザーの保存物に触れない。"""
    # 保存先を使うまで tmp_path を作らず、ファイルを使わない test の準備を省く。
    monkeypatch.setattr(
        asset_cache_module,
        "asset_cache_directory",
        lambda: request.getfixturevalue("tmp_path") / "asset-cache",
    )


@pytest.fixture
def document_search_clock(monkeypatch):
    """検索の時計だけを操作し、process の停止待ちには実時間を使う。"""

    class Clock:
        now = 0.0

        def advance(self, seconds):
            self.now += seconds

    clock = Clock()
    monkeypatch.setattr(
        observation_module, "time", SimpleNamespace(monotonic=lambda: clock.now)
    )
    return clock


@pytest.fixture
def toast_clock(monkeypatch):
    """callback drain の時計だけを進め、process と thread の待機は実時間に保つ。"""
    clock = SimpleNamespace(now=100.0)

    def advance(seconds):
        clock.now += seconds

    clock.monotonic = lambda: clock.now
    clock.sleep = advance
    # 共有 time module を変更せず、通知 module 内の時計だけを置き換える。
    monkeypatch.setattr(runtime_windows_toast, "time", clock)
    return clock


@pytest.fixture(scope="session")
def _noop_external_commands(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """書き換えない外部コマンドの no-op をテストセッション内で共有する。"""
    # 被テスト cmoc の成果物は各 tmp_path に隔離し、固定の補助実行ファイルだけ共有する。
    executable = tmp_path_factory.mktemp("noop-commands") / "powershell.exe"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o555)
    # 子 process の editor も同じ no-op を使い、書き込みと chmod を一度にする。
    (executable.parent / "code").hardlink_to(executable)
    return executable.parent


@pytest.fixture(autouse=True)
def _isolate_windows_toast_transport(
    _noop_external_commands: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """test が利用者の Windows 通知履歴へ toast を残さないようにする。"""
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    # subprocess callback も同じ隔離先を使えるよう、PATH に fake transport を置く。
    executable = _noop_external_commands / "powershell.exe"
    monkeypatch.setenv("PATH", f"{executable.parent}:{os.environ.get('PATH', '')}")
    monkeypatch.setattr(runtime_windows_toast, "_WINDOWS_POWERSHELL", executable)
    monkeypatch.setattr(
        runtime_windows_toast,
        "_run_windows_toast_transport",
        lambda _title, _message: True,
    )


@pytest.fixture(autouse=True)
def _isolate_primary_report_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """通常の in-process test は保存した report の外部表示を起動しない。"""
    monkeypatch.setattr(
        runtime_cli, "open_primary_report_in_editor", lambda _path: None
    )


@pytest.fixture(autouse=True)
def _isolate_document_search_materials(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> None:
    """一般 CLI test では大容量モデルと installation の共有領域に触れない。"""
    monkeypatch.setattr(runtime_doctor, "_installation_root", lambda root: root)
    monkeypatch.setattr(
        runtime_document_search,
        "cmoc_root",
        lambda: request.getfixturevalue("tmp_path"),
    )
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
            self,
            documents,
            resumes,
            on_event,
            *,
            reusable_hashes,
            deadline,
            residency_fd,
            cancelled,
        ):
            vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)
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

    def doctor_search(root, config, *, installation_root, use_saved_config):
        return runtime_document_search.DocumentSearch(
            root,
            config,
            worker=_DoctorInference(),
            installation_root=installation_root,
            use_saved_config=use_saved_config,
        )

    monkeypatch.setattr(runtime_doctor, "DocumentSearch", doctor_search)


@pytest.fixture(autouse=True)
def real_stdio_reporter_probe(monkeypatch):
    """stdio 起動の検証を専用ケースへ集約し、実際の検査関数を渡す。"""
    # schema・TCP collector の検査は各 CLI test でも実行する。
    # test_feedback.py の正常起動・不正応答のケースだけが実 stdio 検査を使う。
    probe = runtime_feedback._validate_stdio_reporter
    monkeypatch.setattr(
        runtime_feedback, "_validate_stdio_reporter", lambda _schema, _root: None
    )
    return probe


@pytest.fixture
def handoff_source(tmp_path, monkeypatch):
    """実行中の送信側 TUI に結び付いた MCP context を用意する。"""
    source = EditorInputHandoffSource(
        "oracle investigation",
        "exec_000002_2026-09-29_15-04",
        "cc_000011_2026-09-29_15-04",
        tmp_path / "sender.jsonl",
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
