"""現在の work-root の文書検索索引を明示的に同期する。"""

import hashlib
import json
import time
from dataclasses import asdict

from cmoc_runtime import (
    TerminalResult,
    load_config,
    run_cli_subcommand,
    start_subcommand_step,
    work_root,
)
from commons.runtime_document_search import DocumentSearch, SearchError
from commons.runtime_document_search_scope import oracle_doc_scope
from commons.runtime_errors import CmocError
from commons.runtime_primary_report import update_primary_report_fields


def cmoc_indexing_impl() -> None:
    """doctor 後、既存差分に触れず文書検索索引を同期する。"""
    run_cli_subcommand(
        _cmoc_indexing_body,
        command_name="indexing",
        command_argv=["cmoc", "indexing"],
        total_steps=2,
        use_work_root_runtime=True,
    )


def _cmoc_indexing_body() -> TerminalResult:
    """共通検索処理の同期結果を primary report に渡す。"""
    root = work_root()
    update_primary_report_fields(
        work_root=str(root),
        indexing_status="not_started",
        index_identity=None,
        sync_result=None,
    )
    start_subcommand_step(2, "文書検索索引を同期", "synchronize document search")
    scope = oracle_doc_scope()
    scope_identity = hashlib.sha256(
        json.dumps(asdict(scope), sort_keys=True).encode("utf-8")
    ).hexdigest()
    update_primary_report_fields(scope_identity=scope_identity)
    search = DocumentSearch(root, scope, load_config(root).document_search)
    update_primary_report_fields(indexing_status="started")
    started = time.monotonic()
    try:
        result = search.synchronize()
    except SearchError as exc:
        update_primary_report_fields(
            indexing_status="failed",
            failure_code=exc.code,
            failure_reason=str(exc),
            elapsed_seconds=time.monotonic() - started,
        )
        raise CmocError(
            "文書検索索引の同期に失敗しました。",
            ["文書検索の設定、資材、許可対象ファイルを確認してください。"],
            f"code: {exc.code}\nreason: {exc}",
        ) from exc
    finally:
        search.close()
    update_primary_report_fields(
        indexing_status=result.status,
        index_identity=result.identity,
        sync_result=asdict(result),
    )
    return TerminalResult(
        details=(("index_identity", result.identity), ("sync_result", asdict(result)))
    )
