"""feedback collector、call capability、および detector を統合する。

この file は 16,000 文字を超えるが、capability の発行、request の並行受付、
call 単位の drain、degraded event、および detector は、一つの invocation-scoped
collector の生存期間と非致命境界を共有する。分割すると、受付停止中の context と
detector が参照する collector の有効性を複数 module で同期する必要が生じるため、
collector lifecycle として一箇所に保つ。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/feedback_observation.md`。
"""

import json
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import typer

from .runtime_feedback_store import (
    REPORTER_PROTOCOL_VERSION,
    FeedbackRejected,
    parse_rfc3339,
    rfc3339_now,
    store_agent_observation,
    store_machine_observation,
    uuid7_prefixed,
)
from .runtime_git import current_branch, head_commit
from .runtime_logging import SubcommandLogger, current_subcommand_logger

FEEDBACK_CAPABILITY_ENV = "CMOC_FEEDBACK_CAPABILITY"
FEEDBACK_COLLECTOR_ENV = "CMOC_FEEDBACK_COLLECTOR_SOCKET"
FEEDBACK_PROTOCOL_ENV = "CMOC_FEEDBACK_PROTOCOL_VERSION"
_MAX_COLLECTOR_REQUEST_BYTES = 64 * 1024
_CURRENT_FEEDBACK_INVOCATION: ContextVar["FeedbackInvocation | None"] = ContextVar(
    "CURRENT_FEEDBACK_INVOCATION", default=None
)


def _is_git_object_id(value: object) -> bool:
    """feedback context に保存できる Git object ID かを返す。"""
    return (
        isinstance(value, str)
        and len(value) in {40, 64}
        and all(character in "0123456789abcdef" for character in value)
    )


class ReporterAvailabilityError(RuntimeError):
    """doctor が stable component/failure code へ変換できる事前検証失敗。"""

    def __init__(self, component: str, failure_code: str, message: str) -> None:
        """失敗した component と安定 code を保持する。"""
        super().__init__(message)
        self.component = component
        self.failure_code = failure_code


@dataclass
class _CallContext:
    """一つの Codex call に拘束された capability context。"""

    capability: str = field(repr=False)
    context: dict[str, Any]
    accepting: bool = True
    inflight: int = 0
    accepted_paths: list[Path] = field(default_factory=list)
    accepted_times: deque[float] = field(default_factory=deque)
    pending_times: list[float] = field(default_factory=list)


class FeedbackCall:
    """Codex call の reporter environment と終了順序を管理する。"""

    def __init__(
        self,
        invocation: "FeedbackInvocation | None",
        call_context: _CallContext | None,
    ) -> None:
        """collector 登録済み context または degraded context を保持する。"""
        self._invocation = invocation
        self._call_context = call_context
        self._closed = False

    @property
    def codex_call_id(self) -> str | None:
        """登録済み Codex call ID を返す。"""
        if self._call_context is None:
            return None
        value = self._call_context.context.get("codex_call_id")
        return value if isinstance(value, str) else None

    def subprocess_env(self, base: dict[str, str]) -> dict[str, str]:
        """capability を argv へ載せず MCP process へ継承する環境を返す。"""
        if self._invocation is None or self._call_context is None:
            return base
        return {
            **base,
            FEEDBACK_CAPABILITY_ENV: self._call_context.capability,
            FEEDBACK_COLLECTOR_ENV: str(self._invocation.socket_path),
            FEEDBACK_PROTOCOL_ENV: REPORTER_PROTOCOL_VERSION,
        }

    def close(self) -> None:
        """新規受付停止、drain、capability 無効化を順に実行する。"""
        if self._closed:
            return
        self._closed = True
        if self._invocation is not None and self._call_context is not None:
            try:
                self._invocation.close_call(self._call_context)
            except Exception:
                # reporter lifecycle の失敗を本命 Codex call の戻り値へ伝播させない。
                emit_reporter_unavailable("collector", "transport_unavailable")

    def __enter__(self) -> "FeedbackCall":
        """Codex subprocess scope へ入る。"""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        """subprocess 終了理由にかかわらず call context を drain する。"""
        self.close()


class FeedbackInvocation:
    """サブコマンド invocation に一つだけ存在する collector。"""

    def __init__(
        self,
        repo: Path,
        worktree: Path,
        command: str,
        logger: SubcommandLogger,
    ) -> None:
        """collector の保存 context と IPC endpoint を初期化する。"""
        self.repo = repo.resolve()
        self.worktree = worktree.resolve()
        self.command = command
        self.logger = logger
        self.invocation_id = logger.invocation_id
        self.socket_path = Path(tempfile.gettempdir()) / (
            f"cmoc-feedback-{os.getuid()}-{secrets.token_hex(8)}.sock"
        )
        self._condition = threading.Condition()
        self._calls: dict[str, _CallContext] = {}
        self._accepted_agent: list[tuple[str, Path]] = []
        self._listener: socket.socket | None = None
        self._server_thread: threading.Thread | None = None
        self._worker_threads: set[threading.Thread] = set()
        self._stopping = False
        self._base_context = self._resolve_base_context()

    def _resolve_base_context(self) -> dict[str, Any]:
        """現在 branch から session/run context を best effort で確定する。"""
        session_id: str | None = None
        run_id: str | None = None
        run_kind: str | None = None
        try:
            branch = current_branch(self.worktree)
            if branch.startswith("cmoc/session/"):
                session_id = branch.split("/", 2)[2]
            elif branch.startswith("cmoc/run/"):
                parts = branch.split("/")
                if len(parts) == 4:
                    session_id = parts[2]
                    run_id = parts[3]
            # session state の破損は feedback 自体を本命 workload の blocker にしない。
            if session_id is not None:
                from .runtime_state import load_state_for_branch

                _, _, state = load_state_for_branch(self.repo, branch)
                run_kind = state.run.kind
        except Exception:
            pass
        try:
            commit = head_commit(self.worktree)
        except Exception:
            commit = ""
        return {
            "repo_root": str(self.repo),
            "work_root": str(self.worktree),
            "head_commit": commit,
            "cmoc_session_id": session_id,
            "run_id": run_id,
            "run_kind": run_kind,
            "subcommand": self.command,
            "subcommand_invocation_id": self.invocation_id,
        }

    def start(self) -> None:
        """owner-only Unix socket で invocation-scoped collector を開始する。"""
        self.socket_path.unlink(missing_ok=True)
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            listener.bind(str(self.socket_path))
            os.chmod(self.socket_path, 0o600)
            listener.listen()
            listener.settimeout(0.2)
        except BaseException:
            listener.close()
            self.socket_path.unlink(missing_ok=True)
            raise
        self._listener = listener
        self._server_thread = threading.Thread(
            target=self._serve,
            name=f"cmoc-feedback-{self.invocation_id}",
            daemon=True,
        )
        self._server_thread.start()

    def stop(self) -> None:
        """全 call を drain し、collector IPC と temporary socket を閉じる。"""
        with self._condition:
            self._stopping = True
            contexts = list(self._calls.values())
            for context in contexts:
                context.accepting = False
        for context in contexts:
            self.close_call(context)
        listener = self._listener
        if listener is not None:
            listener.close()
        if self._server_thread is not None and self._server_thread.is_alive():
            self._server_thread.join(timeout=5)
        with self._condition:
            workers = list(self._worker_threads)
        for worker in workers:
            if worker.is_alive():
                worker.join(timeout=5)
        self.socket_path.unlink(missing_ok=True)

    def _serve(self) -> None:
        """接続ごとに独立 worker を起動して parallel Codex call を分離する。"""
        assert self._listener is not None
        while True:
            with self._condition:
                if self._stopping:
                    return
            try:
                connection, _ = self._listener.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            worker = threading.Thread(
                target=self._handle_connection,
                args=(connection,),
                daemon=True,
            )
            with self._condition:
                self._worker_threads.add(worker)
            worker.start()

    def _handle_connection(self, connection: socket.socket) -> None:
        """一つの reporter request を domain result へ変換する。"""
        try:
            with connection:
                try:
                    request_data = b""
                    while b"\n" not in request_data:
                        chunk = connection.recv(8192)
                        if not chunk:
                            break
                        request_data += chunk
                        if len(request_data) > _MAX_COLLECTOR_REQUEST_BYTES:
                            raise FeedbackRejected(
                                "payload_too_large",
                                "collector request exceeds 64 KiB",
                            )
                    request = json.loads(request_data.split(b"\n", 1)[0])
                    result = self._submit_request(request)
                except FeedbackRejected as exc:
                    result = exc.result()
                except BaseException:
                    result = FeedbackRejected(
                        "transport_unavailable",
                        "collector could not process the request",
                        retryable=True,
                    ).result()
                connection.sendall(
                    json.dumps(
                        result, ensure_ascii=False, separators=(",", ":")
                    ).encode("utf-8")
                    + b"\n"
                )
        finally:
            current = threading.current_thread()
            with self._condition:
                self._worker_threads.discard(current)
                self._condition.notify_all()

    def register_call(
        self,
        *,
        agent_call_id: str,
        agent_call_kind: str,
        codex_call_id: str,
        codex_session_id: str | None = None,
        log_paths: list[Path],
    ) -> _CallContext:
        """Codex call 専用 capability と保存 context を登録する。"""
        capability = secrets.token_urlsafe(32)
        try:
            current_head = head_commit(self.worktree)
        except Exception:
            current_head = self._base_context["head_commit"]
        resolved_log_paths = list(
            dict.fromkeys(
                str(path.resolve()) for path in [self.logger.path, *log_paths]
            )
        )
        context = {
            **self._base_context,
            # doctor preprocess が invocation 開始後に repair commit を作り得るため、
            # observation 発生時点に最も近い Codex call 開始時の HEAD を使う。
            "head_commit": current_head,
            "agent_call_id": agent_call_id,
            "agent_call_kind": agent_call_kind,
            "codex_call_id": codex_call_id,
            "codex_session_id": codex_session_id,
            "log_paths": resolved_log_paths,
        }
        call_context = _CallContext(capability=capability, context=context)
        with self._condition:
            if self._stopping:
                raise RuntimeError("feedback collector is stopping")
            self._calls[capability] = call_context
        return call_context

    def close_call(self, context: _CallContext) -> None:
        """対象 capability だけの受付を止め、処理中 request を drain する。"""
        with self._condition:
            current = self._calls.get(context.capability)
            if current is None:
                return
            current.accepting = False
            self._condition.wait_for(lambda: current.inflight == 0)
            self._calls.pop(context.capability, None)

    def _submit_request(self, request: object) -> dict[str, object]:
        """capability context で agent payload を検査・保存する。"""
        if not isinstance(request, dict):
            raise FeedbackRejected(
                "context_invalid", "collector request must be object"
            )
        if request.get("protocol") != REPORTER_PROTOCOL_VERSION:
            raise FeedbackRejected("protocol_mismatch", "reporter protocol mismatch")
        capability = request.get("capability")
        payload = request.get("payload")
        if not isinstance(capability, str):
            raise FeedbackRejected("context_invalid", "capability is missing")

        # rate limit の slot を予約し、並列 submission でも上限を越えないようにする。
        reserved_at = time.monotonic()
        with self._condition:
            context = self._calls.get(capability)
            if context is None or not context.accepting:
                raise FeedbackRejected("context_invalid", "call context is unavailable")
            cutoff = reserved_at - 60
            while context.accepted_times and context.accepted_times[0] < cutoff:
                context.accepted_times.popleft()
            if len(context.accepted_paths) + len(context.pending_times) >= 8:
                raise FeedbackRejected(
                    "rate_limited", "accepted observation limit reached", retryable=True
                )
            # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
            # 保留中の予約も上限に含める。永続保存が rate window より長くかかることがあり、
            # 開始時刻で保留予約を失効させると、同じ 60 秒間に 3 件を超えて受理できる。
            if len(context.accepted_times) + len(context.pending_times) >= 3:
                raise FeedbackRejected(
                    "rate_limited",
                    "60 second observation limit reached",
                    retryable=True,
                )
            context.pending_times.append(reserved_at)
            context.inflight += 1
        try:
            storage_context = dict(context.context)
            try:
                storage_context["head_commit"] = head_commit(self.worktree)
            except Exception:
                if not _is_git_object_id(storage_context.get("head_commit")):
                    raise FeedbackRejected(
                        "context_invalid",
                        "collector cannot determine the current HEAD commit",
                    )
            if not _is_git_object_id(storage_context.get("head_commit")):
                raise FeedbackRejected(
                    "context_invalid",
                    "collector context has an invalid HEAD commit",
                )
            result, path = store_agent_observation(self.repo, storage_context, payload)
            accepted_at = time.monotonic()
            with self._condition:
                cutoff = accepted_at - 60
                while context.accepted_times and context.accepted_times[0] < cutoff:
                    context.accepted_times.popleft()
                context.accepted_times.append(accepted_at)
                context.accepted_paths.append(path)
                observation_id = result["observation_id"]
                assert isinstance(observation_id, str)
                self._accepted_agent.append((observation_id, path))
            return result
        finally:
            with self._condition:
                if reserved_at in context.pending_times:
                    context.pending_times.remove(reserved_at)
                context.inflight -= 1
                self._condition.notify_all()

    def accepted_agent_observations(self) -> list[dict[str, str]]:
        """この invocation で reporter が accepted を得た observation を返す。"""
        with self._condition:
            return [
                {"observation_id": observation_id, "path": str(path)}
                for observation_id, path in self._accepted_agent
            ]

    def detect_event(self, event: dict[str, Any], log_path: Path) -> None:
        """allowlist 済み stable event を machine observation へ変換する。"""
        event_type = event.get("event_type")
        version = event.get("event_schema_version")
        event_id = event.get("event_id")
        occurred_at = event.get("occurred_at")
        invocation_id = event.get("subcommand_invocation_id")
        if (
            type(version) is not int
            or version != 1
            or not isinstance(event_id, str)
            or not event_id
            or not isinstance(occurred_at, str)
            or not isinstance(invocation_id, str)
            or not invocation_id
            or invocation_id != self.invocation_id
        ):
            return
        try:
            parse_rfc3339(occurred_at)
        except ValueError:
            return
        if event_type == "feedback.reporter_unavailable":
            component = event.get("component")
            failure_code = event.get("failure_code")
            if component not in {
                "reporter",
                "collector",
                "transport",
            } or failure_code not in {
                "missing",
                "version_mismatch",
                "collector_unavailable",
                "transport_unavailable",
                "protocol_error",
            }:
                return
            rule = {
                "rule_id": "feedback.reporter_unavailable.v1",
                "category": "tooling",
                "subject_type": "reporter_component",
                "normalized_subject_id": f"{component}:{failure_code}",
                "summary": "feedback reporter または collector が反復して利用できない。",
                "impact": "agent の自己申告 observation が欠落し、人間対応対象の発見が不完全になる。",
                "human_action": "doctor の結果、reporter/collector version、transport を確認する。",
            }
        elif event_type == "codex.structured_output_validation_exhausted":
            agent_call_kind = event.get("agent_call_kind")
            if not isinstance(agent_call_kind, str) or not agent_call_kind:
                return
            schema_sha256 = event.get("schema_sha256")
            if (
                not isinstance(schema_sha256, str)
                or len(schema_sha256) != 64
                or any(
                    character not in "0123456789abcdef" for character in schema_sha256
                )
            ):
                return
            if event.get("last_failure_stage") not in {
                "json_parse",
                "schema_validation",
                "deterministic_postcondition",
                "resume_unavailable",
                "artifact_changed",
            }:
                return
            if not all(
                isinstance(event.get(name), str) and event.get(name)
                for name in ("agent_call_id", "codex_call_id")
            ):
                return
            rule = {
                "rule_id": "codex.structured_output_validation_exhausted.v1",
                "category": "tooling",
                "subject_type": "agent_call_kind",
                "normalized_subject_id": agent_call_kind,
                "summary": "同じ agent call kind で Structured Output の受理失敗が反復している。",
                "impact": "補正 call の quota を消費した後に workload が失敗し、同じ作業が反復する。",
                "human_action": "対応する builder、schema、および決定論的事後条件を確認する。",
            }
        else:
            return

        # event の安定 context を優先し、未指定 field だけ invocation context で補う。
        context_log_paths = [str(log_path.resolve())]
        call_log_path = event.get("call_log_path")
        if isinstance(call_log_path, str) and Path(call_log_path).is_absolute():
            context_log_paths.append(str(Path(call_log_path).resolve()))
        context = {
            **self._base_context,
            "agent_call_id": event.get("agent_call_id"),
            "agent_call_kind": event.get("agent_call_kind"),
            "codex_call_id": event.get("codex_call_id"),
            "codex_session_id": event.get("codex_session_id"),
            "log_paths": list(dict.fromkeys(context_log_paths)),
        }
        try:
            context["head_commit"] = head_commit(self.worktree)
        except Exception:
            if not _is_git_object_id(context.get("head_commit")):
                raise FeedbackRejected(
                    "context_invalid",
                    "collector cannot determine the current HEAD commit",
                )
        if not _is_git_object_id(context.get("head_commit")):
            raise FeedbackRejected(
                "context_invalid",
                "collector context has an invalid HEAD commit",
            )
        store_machine_observation(
            self.repo,
            context,
            event=event,
            log_path=log_path,
            **rule,
        )


def start_feedback_invocation(
    repo: Path,
    worktree: Path,
    command: str,
    logger: SubcommandLogger,
) -> tuple[FeedbackInvocation | None, Token[FeedbackInvocation | None]]:
    """collector を開始し、失敗時は degraded context を設定する。"""
    invocation: FeedbackInvocation | None = None
    try:
        invocation = FeedbackInvocation(repo, worktree, command, logger)
        invocation.start()
    except Exception:
        _discard_failed_feedback_invocation(invocation)
        emit_reporter_unavailable("collector", "collector_unavailable", logger)
        invocation = None
    except BaseException:
        _discard_failed_feedback_invocation(invocation)
        raise
    token = _CURRENT_FEEDBACK_INVOCATION.set(invocation)
    return invocation, token


def _discard_failed_feedback_invocation(
    invocation: FeedbackInvocation | None,
) -> None:
    """起動途中の collector を中断時も残さず破棄する。"""
    if invocation is None:
        return
    try:
        invocation.stop()
    except Exception:
        pass


def stop_feedback_invocation(
    invocation: FeedbackInvocation | None,
    token: Token[FeedbackInvocation | None],
) -> None:
    """invocation collector を停止して current context を復元する。"""
    try:
        if invocation is not None:
            try:
                invocation.stop()
            except Exception:
                emit_reporter_unavailable("collector", "transport_unavailable")
    finally:
        _CURRENT_FEEDBACK_INVOCATION.reset(token)


def current_feedback_invocation() -> FeedbackInvocation | None:
    """現在のサブコマンド collector を返す。"""
    return _CURRENT_FEEDBACK_INVOCATION.get()


def begin_feedback_call(
    *,
    agent_call_id: str,
    agent_call_kind: str,
    codex_call_id: str,
    codex_session_id: str | None = None,
    log_paths: list[Path],
) -> FeedbackCall:
    """Codex call context を登録し、利用不能なら nonfatal degraded call を返す。"""
    invocation = current_feedback_invocation()
    if invocation is None:
        # managed CLI invocation では collector start または doctor がすでに warning/event
        # を記録する。runtime helper の直接利用では重複 warning を新設しない。
        return FeedbackCall(None, None)
    try:
        context = invocation.register_call(
            agent_call_id=agent_call_id,
            agent_call_kind=agent_call_kind,
            codex_call_id=codex_call_id,
            codex_session_id=codex_session_id,
            log_paths=log_paths,
        )
    except Exception:
        emit_reporter_unavailable("collector", "collector_unavailable")
        return FeedbackCall(None, None)
    return FeedbackCall(invocation, context)


def accepted_feedback_observations() -> list[dict[str, str]]:
    """現在 invocation の accepted reporter observations を返す。"""
    invocation = current_feedback_invocation()
    return invocation.accepted_agent_observations() if invocation is not None else []


def validate_feedback_reporter_availability() -> None:
    """doctor から reporter schema、protocol、collector を非破壊で検査する。"""
    from .runtime_feedback_store import reporter_input_schema

    try:
        expected_schema = reporter_input_schema()
    except Exception as exc:
        raise ReporterAvailabilityError(
            "reporter", "version_mismatch", "feedback reporter schema is invalid"
        ) from exc
    invocation = current_feedback_invocation()
    if invocation is None or not invocation.socket_path.is_socket():
        raise ReporterAvailabilityError(
            "collector", "collector_unavailable", "feedback collector is unavailable"
        )
    from .runtime_feedback_reporter import MCP_PROTOCOL_VERSION

    if MCP_PROTOCOL_VERSION != REPORTER_PROTOCOL_VERSION:
        raise ReporterAvailabilityError(
            "reporter", "version_mismatch", "feedback reporter protocol mismatch"
        )
    _validate_collector_protocol(invocation.socket_path)
    _validate_stdio_reporter(expected_schema, invocation.worktree)


def _validate_collector_protocol(socket_path: Path) -> None:
    """保存を行わない unknown capability request で collector framing を確認する。"""
    request = {
        "protocol": REPORTER_PROTOCOL_VERSION,
        "capability": "doctor-probe-invalid-capability",
        "payload": {},
    }
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(2)
            connection.connect(str(socket_path))
            connection.sendall(
                json.dumps(request, separators=(",", ":")).encode("utf-8") + b"\n"
            )
            response = b""
            while b"\n" not in response:
                chunk = connection.recv(8192)
                if not chunk:
                    break
                response += chunk
        value = json.loads(response.split(b"\n", 1)[0])
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise ReporterAvailabilityError(
            "collector", "protocol_error", "feedback collector protocol probe failed"
        ) from exc
    if not isinstance(value, dict) or value.get("code") != "context_invalid":
        raise ReporterAvailabilityError(
            "collector", "protocol_error", "feedback collector protocol is incompatible"
        )


def _validate_stdio_reporter(
    expected_schema: dict[str, Any], reporter_cwd: Path
) -> None:
    """local stdio MCP process を起動し、公開 tool 面と schema を確認する。"""
    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    # reporter process の起動先は、他の process の cwd と区別できる内部名で扱う。
    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "cmoc-doctor", "version": "1"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]
    stdin_text = "".join(
        json.dumps(request, separators=(",", ":")) + "\n" for request in requests
    )
    try:
        result = subprocess.run(
            [sys.executable, "-m", "commons.runtime_feedback_reporter"],
            cwd=reporter_cwd,
            input=stdin_text,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=5,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ReporterAvailabilityError(
            "reporter", "missing", "feedback reporter cannot be started"
        ) from exc
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ReporterAvailabilityError(
            "transport", "transport_unavailable", "feedback reporter startup failed"
        ) from exc
    if result.returncode != 0:
        raise ReporterAvailabilityError(
            "reporter", "missing", "feedback reporter process exited during startup"
        )
    try:
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        initialize = next(value for value in responses if value.get("id") == 1)
        tools_list = next(value for value in responses if value.get("id") == 2)
        server_info = initialize["result"]["serverInfo"]
        tools = tools_list["result"]["tools"]
        if (
            not isinstance(server_info, dict)
            or not isinstance(tools, list)
            or len(tools) != 1
            or not isinstance(tools[0], dict)
        ):
            raise TypeError("MCP response has an invalid result shape")
    except (
        AttributeError,
        KeyError,
        TypeError,
        ValueError,
        StopIteration,
        json.JSONDecodeError,
    ) as exc:
        raise ReporterAvailabilityError(
            "reporter", "protocol_error", "feedback reporter returned invalid MCP data"
        ) from exc
    if (
        server_info.get("version") != REPORTER_PROTOCOL_VERSION
        or tools[0].get("name") != "submit_observation"
        or tools[0].get("inputSchema") != expected_schema
    ):
        raise ReporterAvailabilityError(
            "reporter",
            "version_mismatch",
            "feedback reporter interface is incompatible",
        )


def emit_reporter_unavailable(
    component: str,
    failure_code: str,
    logger: SubcommandLogger | None = None,
) -> None:
    """reporter 利用不能を stable event と warning に留める。"""
    logger = logger or current_subcommand_logger()
    if logger is not None:
        try:
            logger.event(
                "feedback.reporter_unavailable",
                event_schema_version=1,
                event_id=uuid7_prefixed("evt_"),
                event_type="feedback.reporter_unavailable",
                occurred_at=rfc3339_now(),
                subcommand_invocation_id=logger.invocation_id,
                component=component,
                failure_code=failure_code,
            )
        except Exception:
            pass
    try:
        typer.echo(
            f"warning: feedback {component} unavailable ({failure_code})",
        )
    except Exception:
        pass


def detect_feedback_event(event: dict[str, Any], log_path: Path) -> None:
    """flush 済み event を current collector の allowlist detector へ渡す。"""
    invocation = current_feedback_invocation()
    if invocation is None:
        return
    invocation.detect_event(event, log_path)
