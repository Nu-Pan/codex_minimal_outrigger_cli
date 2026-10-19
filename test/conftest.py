"""共通 fixture で CLI repository と外部副作用を隔離する。"""

import json
import os
import shutil
from itertools import count
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from _acp_builder_support import oracle_schema_path
from _git_support import SESSION_BRANCH, SESSION_ID, current_branch, init_repo, run_git
from oracle.editor_input_handoff.body import EditorInputHandoffSource

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_cli as runtime_cli
import commons.runtime_codex_exec as runtime_codex_exec
import commons.runtime_doctor as runtime_doctor
import commons.runtime_document_search as runtime_document_search
import commons.runtime_document_search_observation as observation_module
import commons.runtime_download_asset_cache as asset_cache_module
import commons.runtime_editor_input_handoff_protocol as handoff_protocol
import commons.runtime_feedback as runtime_feedback
import commons.runtime_feedback_run_state as feedback_run_state
import commons.runtime_feedback_state as feedback_state
import commons.runtime_feedback_store as feedback_store
import commons.runtime_logging as runtime_logging
import commons.runtime_primary_report_review as report_review
import commons.runtime_windows_toast as runtime_windows_toast
import sub_commands.feedback.remediation as remediation_module
from commons.runtime_config import write_config
from commons.runtime_document_search_types import SEARCH_MATERIALS
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_SOURCE_ENV
from commons.runtime_refactor import sync_refactor_state, write_refactor_state
from commons.runtime_state import SessionPart, SessionState, state_path, write_state
from config.cmoc_config import CmocConfig


@pytest.fixture(scope="session")
def _empty_repository_seed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """履歴不要な test に複製する空の Git repository を一度だけ初期化する。"""
    root = tmp_path_factory.mktemp("empty-repository-seed")
    init_repo(root)
    return root


@pytest.fixture
def cli_repository(tmp_path: Path, _empty_repository_seed: Path) -> Path:
    """履歴を参照しない CLI lifecycle test に実 Git root を用意する。"""
    # Git の初期化だけを共有し、設定・index・refs は各 test 内に独立して複製する。
    return shutil.copytree(_empty_repository_seed, tmp_path / "repo")


@pytest.fixture(scope="session")
def _committed_repository_seed(
    tmp_path_factory: pytest.TempPathFactory, _empty_repository_seed: Path
) -> Path:
    """HEAD だけが必要な test に複製する初期履歴を一度だけ作る。"""
    # 修復や linked metadata の作成は各ケースで行い、準備用の init・commit を共有する。
    root = shutil.copytree(
        _empty_repository_seed,
        tmp_path_factory.mktemp("committed-repository-seed") / "repo",
    )
    run_git(root, "commit", "--allow-empty", "-m", "initial")
    return root


@pytest.fixture
def committed_repository(tmp_path: Path, _committed_repository_seed: Path) -> Path:
    """独立した index・refs・設定を持つ実 repository を各 test 内に用意する。"""
    # hardlink や linked worktree を使わず、変更可能な Git metadata もすべて複製する。
    return shutil.copytree(_committed_repository_seed, tmp_path / "repo")


def _prepare_run_session(
    root: Path,
    *,
    with_content: bool,
    with_managed_files: bool = False,
) -> Path:
    """必要な初期内容と設定を一つの commit に揃えて session を用意する。"""
    # doctor と公開 CLI の session 作成は統合 test に残し、ここでは前提だけ作る。
    init_repo(root)
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    for relative in ("oracle/doc", "oracle/src", "oracle/test", "src", "test"):
        (root / relative).mkdir(parents=True, exist_ok=True)
    if with_content:
        # 初期内容を session fork 後に追加する履歴は利用側の検査に不要。
        # apply の比較範囲は test_realization_apply_fork_and_run_join_use_common_state で検査する。
        (root / "README.md").write_text("# repo\n")
        (root / "oracle/spec.md").write_text("# spec\n")
    # CLI preflight が必要とする設定を正規の型で用意し、doctor 修復は本処理に残す。
    write_config(root / ".cmoc/gt/config.json", CmocConfig())
    if with_managed_files:
        # HEAD を固定する検査には、管理物も初期 commit に揃えて修復 commit を省く。
        agents = root / ".agents"
        agents.mkdir()
        (agents / ".gitkeep").touch()
        # state 自身を含む entry 集合を、初期内容がすべて揃ってから同期する。
        write_refactor_state(root, {})
        sync_refactor_state(root)
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "session seed")
    home_branch = current_branch(root)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "switch", "-c", SESSION_BRANCH, fork_commit)
    path = state_path(root, SESSION_ID)
    write_state(
        path,
        SessionState(
            session=SessionPart(
                session_home_branch=home_branch, session_fork_commit=fork_commit
            )
        ),
    )
    return root


def _copy_run_session(
    seed: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, str, Path]:
    """空 directory も複製し、各 test の index・refs・state を独立させる。"""
    root = shutil.copytree(seed, tmp_path / "repo")
    monkeypatch.chdir(root)
    return root, SESSION_BRANCH, state_path(root, SESSION_ID)


@pytest.fixture(scope="session")
def _ready_run_session_seed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """run の前提だけの init・commit・branch 作成を一度だけ行う。"""
    return _prepare_run_session(
        tmp_path_factory.mktemp("run-session-seed"), with_content=False
    )


@pytest.fixture
def ready_run_session(
    tmp_path: Path, _ready_run_session_seed: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, str, Path]:
    """run lifecycle の検査に必要な clean session と保存済み state を用意する。"""
    return _copy_run_session(_ready_run_session_seed, tmp_path, monkeypatch)


@pytest.fixture(scope="session")
def _ready_content_session_seed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """oracle・realization の初期内容を含む履歴も一度だけ作る。"""
    return _prepare_run_session(
        tmp_path_factory.mktemp("content-session-seed"), with_content=True
    )


@pytest.fixture
def ready_content_session(
    tmp_path: Path, _ready_content_session_seed: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, str, Path]:
    """run の検査に使う oracle と realization の初期内容を用意する。"""
    return _copy_run_session(_ready_content_session_seed, tmp_path, monkeypatch)


@pytest.fixture(scope="session")
def _ready_join_session_seed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """join の前提となる初期履歴・管理物・state を一度だけ作る。"""
    # fixture では doctor 全体を実行しない。修復・索引同期は CLI 本処理と
    # test_doctor_cli.py に残し、join 前後の HEAD と state の比較条件を保つ。
    return _prepare_run_session(
        tmp_path_factory.mktemp("join-session-seed"),
        with_content=True,
        with_managed_files=True,
    )


@pytest.fixture
def ready_join_session(
    tmp_path: Path, _ready_join_session_seed: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, str, Path]:
    """同期済み管理物と独立した Git metadata を各 test の session に複製する。"""
    return _copy_run_session(_ready_join_session_seed, tmp_path, monkeypatch)


@pytest.fixture
def feedback_remediation_request_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    """fake 応答の state 検査には、issue 入力・cwd・正本 schema だけを渡す。"""
    # prompt と起動設定は test_feedback.py の builder 専用ケース、実 Git と
    # remediation 呼び出しの結合は後続 wave test に残す。応答は正本 schema で検査する。
    schema = oracle_schema_path("feedback", "remediate_issue.json")
    monkeypatch.setattr(
        remediation_module,
        "build_feedback_issue_remediation_request",
        lambda text, root: SimpleNamespace(
            prompt=text, agent_call_cwd=root, structured_output_schema_path=schema
        ),
    )


@pytest.fixture
def feedback_publication_session(
    ready_join_session: tuple[Path, str, Path],
    feedback_without_transport: None,
    nonpersistent_feedback_ids: None,
    feedback_remediation_request_stub: None,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """案件の publication 検査には、修復不要の session と同期を待たない保存を使う。"""
    # doctor の修復・設定検査は test_doctor_cli.py、feedback との結合は
    # test_feedback.py の repairs_sequential_waves_and_preserves_late_intake に残す。
    # fsync の順序・失敗・再保存は test_feedback_store.py、実同期との結合は
    # 上記の wave test に残す。write・rename・hash 検査と recovery は実行する。
    monkeypatch.setattr("os.fsync", lambda _fd: None)
    # Git・判定根拠・join・publication・cleanup は製品の処理を検査する。
    monkeypatch.setattr(
        remediation_module, "doctor_preprocess_for_join", lambda **_kwargs: None
    )
    root, _session_branch, _state_path = ready_join_session
    return root


@pytest.fixture
def nonpersistent_execution_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    """採番を検査しない CLI test に、保存を伴わない実行 ID を用意する。"""
    # 永続採番は test_runtime_ids.py、logger との結合は test_runtime_cli.py の
    # test_subcommand_logger_keeps_one_file_per_execution に残し、ID の対応は実検査する。
    ids = count()
    monkeypatch.setattr(
        runtime_logging,
        "new_id",
        lambda _root, prefix: f"{prefix}_{next(ids):06d}_2000-01-01_00-00",
    )


@pytest.fixture
def nonpersistent_feedback_ids(
    nonpersistent_execution_ids: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """publication・close の検査に、保存を伴わない feedback ID を用意する。"""
    # SQLite の FULL 同期は os.fsync の置換では省けない。永続採番は
    # test_runtime_ids.py と test_codex_runtime_paths.py、feedback との結合は
    # test_feedback.py の後続 wave test と test_feedback_close.py の reported_case に残す。
    # 各検査では ID の対応・再発時の非再利用・recovery での固定 target を保つ。
    for module in (
        feedback_run_state,
        feedback_state,
        feedback_store,
        remediation_module,
    ):
        monkeypatch.setattr(module, "new_id", runtime_logging.new_id)


@pytest.fixture
def nonpersistent_codex_ids(
    nonpersistent_execution_ids: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """永続採番を検査しない exec test で、実行・agent・Codex call ID を生成する。"""
    # 永続採番は test_runtime_ids.py、実採番と log の結合・process 間の共有は
    # test_codex_runtime_paths.py に残し、ログ間の ID 対応はここでも検査する。
    monkeypatch.setattr(runtime_codex_exec, "new_id", runtime_logging.new_id)


@pytest.fixture
def nonpersistent_handoff_ids(
    nonpersistent_execution_ids: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """採番を検査しない handoff test で、実行・target ID の永続保存を省く。"""
    # 永続採番は test_runtime_ids.py、実採番と target の結合は
    # test_editor_input_handoff.py の editor 待機ケースに残す。
    # route の保存・解決・削除と TCP lifecycle は実処理を通す。
    monkeypatch.setattr(handoff_protocol, "new_id", runtime_logging.new_id)


@pytest.fixture
def cli_terminal_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_execution_ids: None,
) -> Path:
    """表示・通知・前処理失敗に不要な外部処理と永続採番を準備しない。"""
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
    # pending の inventory・件数・通知境界は test_feedback.py、結果の引き渡しは
    # test_runtime_cli.py に残し、表示・report の検査で空の store を毎回検証しない。
    monkeypatch.setattr(
        runtime_cli, "feedback_completion_counts", lambda _root: (0, [])
    )
    return root


@pytest.fixture
def input_path(tmp_path: Path) -> Path:
    """予約・採番を検査しないケースには、所定 directory の通常 file だけ用意する。"""
    path = tmp_path / ".cmoc/gu/log/editor_input/input.md"
    path.parent.mkdir(parents=True)
    path.touch()
    return path


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
def unsynced_search_storage(monkeypatch):
    """耐久性を判定しない検索 test では、初期化・更新時のディスク同期を省く。"""
    # 実 sqlite-vec、ファイルへの保存、commit/rollback は維持する。
    # 途中保存・再開・別 worktree での再利用は、この fixture を使わず検査する。
    sqlite = runtime_document_search.sqlite3

    def connect_unsynced(*args, **kwargs):
        connection = sqlite.connect(*args, **kwargs)
        # 索引・cache のテーブル作成も同期を伴うため、作成前の接続で設定する。
        connection.execute("pragma synchronous = off")
        return connection

    # 他 module の採番 DB や、test が直接開く検証用 connection には適用しない。
    monkeypatch.setattr(
        runtime_document_search,
        "sqlite3",
        SimpleNamespace(**(vars(sqlite) | {"connect": connect_unsynced})),
    )


@pytest.fixture
def document_repository(tmp_path, monkeypatch):
    """Git 検査以外の検索契約に、検証済みの root・文書集合を渡す。"""
    root = tmp_path / "repo"
    docs = root / "oracle/doc"
    docs.mkdir(parents=True)
    (docs / "allowed.md").write_text("# 許可された原文\n最初の内容\n")

    def repository_root(work_root):
        assert work_root == root
        return root

    def enumerate_documents(work_root):
        assert work_root == root
        return sorted(docs.glob("*.md")), []

    # Git 分類・root 解決・非追跡検査は実 repository の同期・再利用 test に残す。
    # 本文・位置の再確認、索引 identity・lease・保存・検索と MCP 応答は製品経路を通す。
    monkeypatch.setattr(runtime_document_search, "repo_root", repository_root)
    monkeypatch.setattr(
        runtime_document_search, "require_cmoc_ignored", lambda _root: None
    )
    monkeypatch.setattr(
        runtime_document_search,
        "enumerate_oracle_and_realization_files",
        enumerate_documents,
    )
    return root


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
def primary_report_review_runner(monkeypatch):
    """一般の CLI 検査では確認の起動準備と応答を置換し、実 runner を渡す。"""
    # 専用の review_runtime は正本 builder と実 runner を戻して、prompt・schema・
    # 起動設定・回復・補正・取消を検査する。一般の CLI 検査では消費されない
    # prompt の構築と Git 探索を省き、入力固定・report の組み立てと保存は実行する。
    runner = report_review.run_codex_exec
    monkeypatch.setattr(
        report_review,
        "build_primary_report_review_request",
        lambda **_kwargs: object(),
    )
    monkeypatch.setattr(
        report_review,
        "run_codex_exec",
        lambda *_args, **_kwargs: SimpleNamespace(
            output_json={"result": {"status": "no_findings", "findings": []}}
        ),
    )
    return runner


@pytest.fixture
def primary_report_review_builder(primary_report_review_runner, monkeypatch):
    """確認の起動引数や Git 境界を検査するケースでは正本 builder を使う。"""
    from oracle.acp_builder.primary_report_review import (
        build_primary_report_review_request,
    )

    monkeypatch.setattr(
        report_review,
        "build_primary_report_review_request",
        build_primary_report_review_request,
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


@pytest.fixture
def doctor_without_index_sync(monkeypatch: pytest.MonkeyPatch) -> None:
    """Git 修復・reporter 分岐の検査では、参照しない検索索引の生成・永続化を省く。"""
    # 実同期との結合は test_doctor_cli.py の初回修復、配置先復元、worktree 分離に残す。
    # 更新・削除・再利用とログ/report は
    # test_doctor_sync_preserves_user_changes_and_correlates_logs_and_reports、
    # 失敗・取消の進捗は test_doctor_reports_persisted_chunks_when_sync_fails で検査する。
    # 設定・state の同期、Git index の退避・復元と修復 commit は実処理を通す。
    monkeypatch.setattr(
        runtime_doctor, "_synchronize_document_search_index", lambda *_args: None
    )


@pytest.fixture
def feedback_without_transport(monkeypatch):
    """保存済み観測と fake 応答による state 検査では TCP の準備を省く。"""
    # stdio・TCP の受理・拒否・drain と linked worktree からの追加観測は
    # test_feedback.py の transport・後続 wave 結合 test で検証する。
    monkeypatch.setattr(
        runtime_cli, "start_feedback_invocation", lambda *_args: (None, None)
    )
    monkeypatch.setattr(
        runtime_doctor, "validate_feedback_reporter_availability", lambda: None
    )


@pytest.fixture(autouse=True)
def real_stdio_reporter_probe(monkeypatch):
    """stdio 起動の検証を専用ケースへ集約し、実際の検査関数を渡す。"""
    # schema・TCP collector の検査は、transport を使う CLI test でも実行する。
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
