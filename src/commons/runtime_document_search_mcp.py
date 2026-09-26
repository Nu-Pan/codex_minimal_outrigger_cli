"""call 固定 context で oracle 文書検索だけを公開する stdio MCP server。"""

import json
import queue
import signal
import sys
import threading
import time
from collections.abc import Mapping
from dataclasses import fields
from pathlib import Path
from typing import Any

from oracle.acp_builder.basic import DocumentSearchScope
from oracle.other.document_search import (
    SEARCH_MCP_SERVER,
    SEARCH_TOOL_INPUT_SCHEMA,
    SEARCH_TOOL_NAME,
    DocumentSearchConfig,
)

from .runtime_document_search import DocumentSearch, SearchError

MCP_PROTOCOL_VERSION = "2025-06-18"


def _invalid_params(request_id: object) -> dict[str, object]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32602, "message": "Invalid params"},
    }


def _tool_result(value: Mapping[str, object], *, error: bool) -> dict[str, object]:
    return {
        "content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}],
        "structuredContent": value,
        "isError": error,
    }


def _response(request: object, search: DocumentSearch) -> dict[str, object] | None:
    """単一の JSON-RPC request を処理し、notification には応答しない。"""
    if isinstance(request, dict) and "id" not in request:
        return None
    if (
        not isinstance(request, dict)
        or request.get("jsonrpc") != "2.0"
        or not isinstance(request.get("method"), str)
        or not (isinstance(request.get("id"), str) or type(request.get("id")) is int)
    ):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32600, "message": "Invalid Request"},
        }
    request_id = request["id"]
    method = request["method"]
    if method == "initialize":
        params = request.get("params")
        if not isinstance(params, dict) or not isinstance(
            params.get("protocolVersion"), str
        ):
            return _invalid_params(request_id)
        result: dict[str, object] = {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SEARCH_MCP_SERVER, "version": "1"},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": SEARCH_TOOL_NAME,
                    "description": "許可された oracle/doc Markdown の現在原文を意味検索する。",
                    "inputSchema": SEARCH_TOOL_INPUT_SCHEMA,
                    "annotations": {
                        "readOnlyHint": True,
                        "destructiveHint": False,
                        "idempotentHint": True,
                        "openWorldHint": False,
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = request.get("params")
        if not isinstance(params, dict) or params.get("name") != SEARCH_TOOL_NAME:
            return _invalid_params(request_id)
        arguments = params.get("arguments")
        if not isinstance(arguments, dict) or set(arguments) - {"query", "limit"}:
            return _invalid_params(request_id)
        query = arguments.get("query")
        limit = arguments.get("limit")
        if (
            not isinstance(query, str)
            or not query.strip()
            or ("limit" in arguments and (type(limit) is not int or limit < 1))
        ):
            return _invalid_params(request_id)
        try:
            found = search.search(query, limit)
        except SearchError as exc:
            result = _tool_result(
                {"status": "error", "code": exc.code, "message": str(exc)},
                error=True,
            )
        except Exception:
            result = _tool_result(
                {
                    "status": "error",
                    "code": "SYNC_FAILED",
                    "message": "document search failed",
                },
                error=True,
            )
        else:
            result = _tool_result(found, error=False)
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": "Method not found"},
        }
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _parse_context(raw: str) -> DocumentSearch:
    """信頼された起動引数以外から root と範囲を受け取らない。"""
    value: Any = json.loads(raw)
    if not isinstance(value, dict) or set(value) != {"work_root", "scope", "config"}:
        raise ValueError("invalid search context")
    root = value["work_root"]
    scope = value["scope"]
    tuning = value["config"]
    if not isinstance(root, str) or not Path(root).is_absolute():
        raise ValueError("invalid work root")
    if not isinstance(scope, dict) or set(scope) != {
        "allowed_files",
        "allowed_subtrees",
        "excluded_files",
        "excluded_subtrees",
    }:
        raise ValueError("invalid search scope")
    if any(not isinstance(items, list) for items in scope.values()):
        raise ValueError("invalid search scope")
    resolved_scope = DocumentSearchScope(
        **{name: tuple(items) for name, items in scope.items()}
    )
    if tuning is not None:
        names = {field.name for field in fields(DocumentSearchConfig)}
        if not isinstance(tuning, dict) or set(tuning) != names:
            raise ValueError("invalid document search config")
        tuning = DocumentSearchConfig(**tuning)
    return DocumentSearch(Path(root), resolved_scope, tuning)


def main() -> None:
    """stdio を protocol 専用にし、取消・EOF で実行中の要求を収束させる。"""
    if len(sys.argv) != 2:
        raise SystemExit(2)
    try:
        search = _parse_context(sys.argv[1])
    except (TypeError, ValueError, SearchError):
        raise SystemExit(2) from None
    pending: queue.Queue[tuple[bool, object, float] | None] = queue.Queue()
    state_lock = threading.RLock()
    closed = threading.Event()
    cancelled_ids: set[str | int] = set()
    queued_ids: set[str | int] = set()
    active: tuple[str | int, threading.Event] | None = None

    def close() -> None:
        closed.set()
        with state_lock:
            if active is not None:
                active[1].set()
        pending.put(None)

    def receive() -> None:
        try:
            for line in sys.stdin:
                received_at = time.monotonic()
                try:
                    request = json.loads(line)
                except ValueError:
                    pending.put((False, None, received_at))
                    continue
                if (
                    isinstance(request, dict)
                    and request.get("method") == "notifications/cancelled"
                ):
                    params = request.get("params")
                    request_id = (
                        params.get("requestId") if isinstance(params, dict) else None
                    )
                    if isinstance(request_id, (str, int)) and not isinstance(
                        request_id, bool
                    ):
                        with state_lock:
                            if active is not None and active[0] == request_id:
                                active[1].set()
                            elif request_id in queued_ids:
                                cancelled_ids.add(request_id)
                    continue
                if isinstance(request, dict):
                    request_id = request.get("id")
                    if isinstance(request_id, (str, int)) and not isinstance(
                        request_id, bool
                    ):
                        with state_lock:
                            queued_ids.add(request_id)
                pending.put((True, request, received_at))
        finally:
            close()

    signal.signal(signal.SIGTERM, lambda *_args: close())
    reader = threading.Thread(target=receive, daemon=True)
    reader.start()
    while True:
        item = pending.get()
        if item is None or closed.is_set():
            break
        parsed, request, received_at = item
        request_id = request.get("id") if isinstance(request, dict) else None
        cancellation = threading.Event()
        if isinstance(request_id, (str, int)) and not isinstance(request_id, bool):
            with state_lock:
                queued_ids.discard(request_id)
                active = (request_id, cancellation)
                if request_id in cancelled_ids:
                    cancellation.set()
                    cancelled_ids.discard(request_id)
        search.cancelled = cancellation
        search.request_started = received_at
        try:
            if not parsed:
                response: dict[str, object] | None = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
            else:
                response = _response(request, search)
        finally:
            search.cancelled = None
            search.request_started = None
            with state_lock:
                active = None
        if response is not None and not closed.is_set():
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    search.close()


if __name__ == "__main__":
    main()
