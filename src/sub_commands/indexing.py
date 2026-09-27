"""現在の work-root の文書検索索引を明示的に同期する。"""

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
from commons.runtime_document_search_scope import oracle_doc_scope, scope_identity
from commons.runtime_errors import CmocError
from commons.runtime_primary_report import (
    current_primary_report_fields,
    update_primary_report_fields,
)


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
    doctor_fields = current_primary_report_fields()
    doctor_result = doctor_fields.get("doctor_sync_result")
    update_primary_report_fields(
        work_root=str(root),
        indexing_status="not_started" if doctor_result is None else "started",
        index_identity=doctor_fields.get("doctor_index_identity"),
        sync_result=doctor_result,
    )
    start_subcommand_step(2, "文書検索索引を同期", "synchronize document search")
    scope = oracle_doc_scope()
    update_primary_report_fields(scope_identity=scope_identity(scope))
    search = DocumentSearch(
        root, scope, load_config(root).document_search, use_saved_config=True
    )
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
            indexing_sync_progress=search.sync_progress,
        )
        raise CmocError(
            "文書検索索引の同期に失敗しました。",
            [
                f"対象 work-root ({root}) で cmoc doctor を実行してください。"
                if exc.code in {"NOT_READY", "MODEL_IDENTITY_MISMATCH"}
                else "文書検索の設定、資材、許可対象ファイルを確認してください。"
            ],
            f"code: {exc.code}\nreason: {exc}",
        ) from exc
    finally:
        search.close()
    combined = asdict(result)
    if (
        isinstance(doctor_result, dict)
        and doctor_result.get("identity") == result.identity
    ):
        for key in ("added", "changed", "deleted", "blanked", "reused_embeddings"):
            combined[key] += doctor_result[key]
        combined["elapsed_seconds"] += doctor_result["elapsed_seconds"]
        if doctor_result["status"] == "updated":
            combined["status"] = "updated"
    update_primary_report_fields(
        indexing_status=combined["status"],
        index_identity=result.identity,
        sync_result=combined,
        indexing_sync_progress=search.sync_progress,
    )
    return TerminalResult(
        details=(("index_identity", result.identity), ("sync_result", combined))
    )
