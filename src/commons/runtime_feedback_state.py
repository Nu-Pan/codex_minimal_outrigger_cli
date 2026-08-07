"""feedback の repository-local normalized state を扱う。

この file は 16,000 文字を超えるが、record 構築、content-addressed ID、schema 検査、
record 間参照、および effective record 選択は、append-only state の同じ不変条件を
共有する。検査と読み取りを分けると、一方だけが新しい record field や選択規則へ
追従する危険があるため、state model として一箇所に保つ。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/feedback_state.md`。
"""

import base64
import fcntl
import hashlib
import json
import os
import re
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .runtime_errors import CmocError
from .runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    is_observation_id,
    is_uuid7_prefixed,
    machine_observation_id,
    migration_root,
    normalization_checkpoint_root,
    normalization_recovery_root,
    normalization_unit_root,
    observation_root,
    parse_rfc3339,
    recover_immutable_bytes_from_temporary,
    report_recovery_root,
    report_snapshot_root,
    reporter_input_schema,
    reporter_input_validation_errors,
    sha256_bytes,
    state_snapshot_root,
    uuid7_prefixed,
    write_immutable_json,
)


@dataclass
class IssueView:
    """report と normalization candidate が共有する effective issue state。"""

    issue_id: str
    identity: dict[str, Any]
    revision: dict[str, Any]
    occurrences: list[dict[str, Any]]
    assessment: dict[str, Any] | None
    disposition: dict[str, Any] | None
    revisions: list[dict[str, Any]] = field(default_factory=list)
    assessments: list[dict[str, Any]] = field(default_factory=list)
    dispositions: list[dict[str, Any]] = field(default_factory=list)


_MACHINE_RULE_CONTRACTS: dict[str, tuple[str, str, str]] = {
    "feedback.reporter_unavailable.v1": (
        "feedback.reporter_unavailable",
        "tooling",
        "reporter_component",
    ),
    "codex.structured_output_validation_exhausted.v1": (
        "codex.structured_output_validation_exhausted",
        "tooling",
        "agent_call_kind",
    ),
}
_MACHINE_REPORTER_COMPONENTS = {"reporter", "collector", "transport"}
_MACHINE_REPORTER_FAILURE_CODES = {
    "missing",
    "version_mismatch",
    "collector_unavailable",
    "transport_unavailable",
    "protocol_error",
}


def _record_id(prefix: str, body: dict[str, Any]) -> str:
    """ID field を除いた record body の canonical SHA256 を返す。"""
    return f"{prefix}{sha256_bytes(canonical_json_bytes(body))}"


def issue_id(canonical_key: str) -> str:
    """canonical issue key から安定した lowercase base32 ID を返す。"""
    digest = hashlib.sha256(canonical_key.encode("utf-8")).digest()
    encoded = base64.b32encode(digest).decode("ascii").lower().rstrip("=")
    return f"fbi_{encoded[:26]}"


def machine_canonical_key(observation: dict[str, Any]) -> str:
    """machine rule payload から canonical issue key を構築する。"""
    payload = observation.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("machine observation payload must be an object")
    rule_id = payload.get("rule_id")
    subject_type = payload.get("subject_type")
    normalized_subject_id = payload.get("normalized_subject_id")
    if not all(
        isinstance(value, str) and value
        for value in (rule_id, subject_type, normalized_subject_id)
    ):
        raise ValueError("machine observation canonical key fields are invalid")
    assert isinstance(rule_id, str)
    assert isinstance(subject_type, str)
    assert isinstance(normalized_subject_id, str)
    return "\0".join((rule_id, subject_type, normalized_subject_id))


def agent_canonical_key(observation_id: str) -> str:
    """agent report から新規 issue を作る canonical key を返す。"""
    return f"agent\0{observation_id}"


def _is_machine_canonical_key(value: str) -> bool:
    """rule registry に適合する machine issue canonical key かを返す。"""
    parts = value.split("\0")
    if len(parts) != 3:
        return False
    rule_id, subject_type, normalized_subject_id = parts
    contract = _MACHINE_RULE_CONTRACTS.get(rule_id)
    if contract is None or subject_type != contract[2] or not normalized_subject_id:
        return False
    if rule_id != "feedback.reporter_unavailable.v1":
        return True
    component, separator, failure_code = normalized_subject_id.partition(":")
    return (
        separator == ":"
        and component in _MACHINE_REPORTER_COMPONENTS
        and failure_code in _MACHINE_REPORTER_FAILURE_CODES
    )


def issue_directory(repo: Path, current_issue_id: str) -> Path:
    """issue ごとの append-only record directory を返す。"""
    return feedback_root(repo) / "issue" / current_issue_id


def identity_record(
    current_issue_id: str,
    canonical_key: str,
    origin: str,
    observation_id: str,
    created_at: str,
) -> dict[str, Any]:
    """初回作成後に変更しない issue identity を構築する。"""
    return {
        "schema_version": 1,
        "issue_id": current_issue_id,
        "origin": origin,
        "canonical_key": canonical_key,
        "created_from_observation_id": observation_id,
        "created_at": created_at,
    }


def revision_record(
    current_issue_id: str,
    created_at: str,
    source_observation_ids: list[str],
    category: str,
    summary: str,
    human_action: str,
    impact: str,
    cause_assessment: dict[str, str],
    related_issue_ids: list[str],
) -> dict[str, Any]:
    """normalized issue 内容の immutable revision を構築する。"""
    body: dict[str, Any] = {
        "schema_version": 1,
        "issue_id": current_issue_id,
        "created_at": created_at,
        "source_observation_ids": sorted(set(source_observation_ids)),
        "category": category,
        "summary": summary,
        "human_action": human_action,
        "impact": impact,
        "cause_assessment": cause_assessment,
        "related_issue_ids": sorted(set(related_issue_ids)),
    }
    return {"revision_id": _record_id("", body), **body}


def occurrence_record(
    current_issue_id: str,
    observation: dict[str, Any],
    observation_sha256: str,
) -> dict[str, Any]:
    """raw observation と issue の対応を表す occurrence を構築する。"""
    context = observation.get("context")
    if not isinstance(context, dict):
        context = {}
    return {
        "schema_version": 1,
        "issue_id": current_issue_id,
        "observation_id": observation["observation_id"],
        "observation_sha256": observation_sha256,
        "observed_at": observation["observed_at"],
        "cmoc_session_id": context.get("cmoc_session_id"),
        "subcommand_invocation_id": context.get("subcommand_invocation_id"),
        "log_paths": context.get("log_paths", []),
    }


def assessment_record(
    current_issue_id: str,
    assessed_at: str,
    presence: str,
    freshness: str,
    reason_code: str,
    reason: str,
    compared_fingerprints: list[dict[str, Any]],
) -> dict[str, Any]:
    """human disposition と独立した machine assessment を構築する。"""
    body: dict[str, Any] = {
        "schema_version": 1,
        "issue_id": current_issue_id,
        "assessed_at": assessed_at,
        "presence": presence,
        "freshness": freshness,
        "reason_code": reason_code,
        "reason": reason,
        "compared_fingerprints": compared_fingerprints,
    }
    return {"assessment_id": _record_id("", body), **body}


def ingestion_record(
    observation_id: str,
    observation_sha256: str,
    processed_at: str,
    normalization_unit_id: str,
    normalizer_version: str,
    status: str,
    issue_ids: list[str],
    validation_errors: list[str],
) -> dict[str, Any]:
    """一 observation の増分処理結果を表す receipt を構築する。"""
    return {
        "schema_version": 1,
        "observation_id": observation_id,
        "observation_sha256": observation_sha256,
        "processed_at": processed_at,
        "normalization_unit_id": normalization_unit_id,
        "normalizer_version": normalizer_version,
        "status": status,
        "issue_ids": issue_ids,
        "validation_errors": validation_errors,
    }


def report_record(
    *,
    report_id: str,
    generated_at: str,
    report_snapshot_sha256: str,
    report_snapshot_observation_count: int,
    processed_observation_count: int,
    deferred_observation_count: int,
    report_path: Path,
    report_sha256: str,
    result: str,
    normalization_unit_ids: list[str],
    state_snapshot_id: str | None,
    previous_successful_report_id: str | None,
) -> dict[str, Any]:
    """feedback report と二種類の snapshot を結び付ける record を返す。"""
    return {
        "schema_version": 2,
        "report_id": report_id,
        "generated_at": generated_at,
        "report_snapshot_sha256": report_snapshot_sha256,
        "report_snapshot_observation_count": report_snapshot_observation_count,
        "processed_observation_count": processed_observation_count,
        "deferred_observation_count": deferred_observation_count,
        "report_path": str(report_path.resolve()),
        "report_sha256": report_sha256,
        "result": result,
        "normalization_unit_ids": normalization_unit_ids,
        "state_snapshot_id": state_snapshot_id,
        "previous_successful_report_id": previous_successful_report_id,
    }


def record_path(repo: Path, record: dict[str, Any], kind: str) -> Path:
    """record kind と ID から repository-local path を返す。"""
    root = feedback_root(repo)
    current_issue_id = record.get("issue_id")
    if kind == "identity":
        assert isinstance(current_issue_id, str)
        return issue_directory(repo, current_issue_id) / "identity.json"
    id_fields = {
        "revision": "revision_id",
        "occurrence": "observation_id",
        "assessment": "assessment_id",
        "disposition": "decision_id",
        "ingestion": "observation_id",
        "report": "report_id",
    }
    if kind not in id_fields:
        raise ValueError(f"unknown feedback record kind: {kind}")
    record_id_value = record.get(id_fields[kind])
    if not isinstance(record_id_value, str):
        raise ValueError(f"feedback {kind} record ID is invalid")
    if kind in {"revision", "occurrence", "assessment", "disposition"}:
        assert isinstance(current_issue_id, str)
        return (
            issue_directory(repo, current_issue_id) / kind / (f"{record_id_value}.json")
        )
    return root / kind / f"{record_id_value}.json"


def write_feedback_record(path: Path, record: dict[str, Any]) -> bool:
    """append-only record を canonical form で durable 保存する。"""
    content = canonical_json_bytes(record)
    try:
        existed = path.is_file() and path.read_bytes() == content
        write_immutable_json(path, record)
        return not existed
    except Exception as exc:
        if isinstance(exc, CmocError):
            raise
        raise CmocError(
            "feedback append-only record を durable に保存できません。",
            ["record path と filesystem の整合性を確認してください。"],
            str(path),
        ) from exc


def validate_observation_envelope(
    observation: dict[str, Any],
    *,
    expected_repo_root: Path | None = None,
) -> list[str]:
    """raw observation の安定 envelope field を検査する。"""
    errors = _field_set(
        observation,
        {
            "schema_version",
            "observation_id",
            "source",
            "observed_at",
            "context",
            "versions",
            "payload",
            "evidence_fingerprints",
            "source_event",
        },
    )
    if not _is_version_one(observation.get("schema_version")):
        errors.append("/schema_version: expected 1")
    observation_id_value = observation.get("observation_id")
    if not is_observation_id(observation_id_value):
        errors.append("/observation_id: invalid ID")
    if observation.get("source") not in {"agent_report", "machine_rule"}:
        errors.append("/source: unsupported value")
    observed_at = observation.get("observed_at")
    if not isinstance(observed_at, str) or not _is_timestamp(observed_at):
        errors.append("/observed_at: timezone-aware RFC 3339 timestamp required")

    context = observation.get("context")
    if not isinstance(context, dict):
        errors.append("/context: expected object")
    else:
        errors.extend(_validate_observation_context(context))
        if expected_repo_root is not None:
            repo_value = context.get("repo_root")
            if not isinstance(repo_value, str) or Path(repo_value).resolve(
                strict=False
            ) != expected_repo_root.resolve(strict=False):
                errors.append("/context/repo_root: does not match current repository")
    versions = observation.get("versions")
    if not isinstance(versions, dict):
        errors.append("/versions: expected object")
    else:
        errors.extend(
            _validate_observation_versions(versions, observation.get("source"))
        )
    fingerprints = observation.get("evidence_fingerprints")
    if not isinstance(fingerprints, list):
        errors.append("/evidence_fingerprints: expected array")
    else:
        for index, fingerprint in enumerate(fingerprints):
            errors.extend(_validate_evidence_fingerprint(fingerprint, index))

    if observation.get("source") == "machine_rule" and not isinstance(
        observation.get("source_event"), dict
    ):
        errors.append("/source_event: machine observation requires object")
    elif observation.get("source") == "machine_rule":
        errors.extend(_validate_machine_observation(observation))
    elif observation.get("source") == "agent_report":
        if not is_uuid7_prefixed(observation_id_value, "fbo_"):
            errors.append("/observation_id: agent report requires UUIDv7")
        if observation.get("source_event") is not None:
            errors.append("/source_event: agent observation requires null")
        if isinstance(context, dict):
            for name in ("agent_call_id", "agent_call_kind", "codex_call_id"):
                if not isinstance(context.get(name), str) or not context.get(name):
                    errors.append(f"/context/{name}: agent observation requires string")
        payload = observation.get("payload")
        if not isinstance(payload, dict):
            errors.append("/payload: expected object")
        else:
            errors.extend(reporter_input_validation_errors(payload))
            if isinstance(fingerprints, list):
                expected_indexes = {
                    index
                    for index, item in enumerate(payload.get("evidence", []))
                    if isinstance(item, dict)
                    and item.get("kind") in {"file", "oracle", "log"}
                }
                actual_indexes = {
                    item.get("evidence_index")
                    for item in fingerprints
                    if isinstance(item, dict)
                }
                if actual_indexes != expected_indexes:
                    errors.append(
                        "/evidence_fingerprints: path evidence indexes do not match payload"
                    )
    if isinstance(context, dict) and isinstance(fingerprints, list):
        repo_value = context.get("repo_root")
        if isinstance(repo_value, str) and Path(repo_value).is_absolute():
            # raw fingerprint は観測時点で symlink 解決済みである。現在の filesystem
            # 状態で再解決すると、後日の symlink 変更を raw schema 違反にしてしまう。
            repo_path = Path(os.path.abspath(repo_value))
            for index, fingerprint in enumerate(fingerprints):
                if not isinstance(fingerprint, dict):
                    continue
                normalized = fingerprint.get("normalized_path")
                if isinstance(normalized, str):
                    candidate = Path(os.path.abspath(normalized))
                    if candidate != repo_path and repo_path not in candidate.parents:
                        errors.append(
                            f"/evidence_fingerprints/{index}/normalized_path: outside repo"
                        )
    return errors


def _is_timestamp(value: str) -> bool:
    """timezone を持つ ISO 8601/RFC 3339 timestamp かを返す。"""
    try:
        parse_rfc3339(value)
        return True
    except ValueError:
        return False


def _is_version_one(value: object) -> bool:
    """JSON number の version 1 だけを受理する。"""
    return type(value) is int and value == 1


def _validate_observation_context(context: dict[str, Any]) -> list[str]:
    """collector が付与する version 1 context を検査する。"""
    errors = _field_set(
        context,
        {
            "repo_root",
            "work_root",
            "head_commit",
            "cmoc_session_id",
            "run_id",
            "run_kind",
            "subcommand",
            "subcommand_invocation_id",
            "agent_call_id",
            "agent_call_kind",
            "codex_call_id",
            "codex_session_id",
            "log_paths",
        },
    )
    for name in (
        "repo_root",
        "work_root",
        "head_commit",
        "subcommand",
        "subcommand_invocation_id",
    ):
        if not isinstance(context.get(name), str):
            errors.append(f"/context/{name}: expected string")
    for name in ("repo_root", "work_root"):
        value = context.get(name)
        if isinstance(value, str) and not Path(value).is_absolute():
            errors.append(f"/context/{name}: expected absolute path")
    head = context.get("head_commit")
    if isinstance(head, str) and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head):
        errors.append("/context/head_commit: expected Git object ID")
    for name in (
        "cmoc_session_id",
        "run_id",
        "agent_call_id",
        "agent_call_kind",
        "codex_call_id",
        "codex_session_id",
    ):
        if context.get(name) is not None and not isinstance(context.get(name), str):
            errors.append(f"/context/{name}: expected string or null")
    if context.get("run_kind") not in {
        None,
        "realization_apply",
        "realization_refactor",
    }:
        errors.append("/context/run_kind: unsupported value")
    if not _is_string_list(context.get("log_paths")):
        errors.append("/context/log_paths: expected unique string array")
    elif any(not Path(value).is_absolute() for value in context["log_paths"]):
        errors.append("/context/log_paths: expected absolute paths")
    return errors


def _validate_observation_versions(
    versions: dict[str, Any],
    source: object,
) -> list[str]:
    """raw envelope の producer/schema version を検査する。"""
    errors = _field_set(
        versions,
        {"reporter", "reporter_protocol", "observation_schema", "rule_id"},
    )
    if not _is_version_one(versions.get("observation_schema")):
        errors.append("/versions/observation_schema: expected 1")
    if source == "agent_report":
        for name in ("reporter", "reporter_protocol"):
            if not isinstance(versions.get(name), str):
                errors.append(f"/versions/{name}: expected string")
        if versions.get("rule_id") is not None:
            errors.append("/versions/rule_id: agent observation requires null")
    elif source == "machine_rule":
        if (
            versions.get("reporter") is not None
            or versions.get("reporter_protocol") is not None
        ):
            errors.append(
                "/versions: machine observation requires null reporter versions"
            )
        if not isinstance(versions.get("rule_id"), str):
            errors.append("/versions/rule_id: expected string")
    return errors


def _validate_evidence_fingerprint(value: object, index: int) -> list[str]:
    """raw evidence fingerprint entry を検査する。"""
    prefix = f"/evidence_fingerprints/{index}"
    if not isinstance(value, dict):
        return [f"{prefix}: expected object"]
    errors = [
        f"{prefix}/{error}"
        for error in _field_set(
            value, {"evidence_index", "normalized_path", "state", "sha256"}
        )
    ]
    evidence_index = value.get("evidence_index")
    if (
        not isinstance(evidence_index, int)
        or isinstance(evidence_index, bool)
        or evidence_index < 0
    ):
        errors.append(f"{prefix}/evidence_index: expected non-negative integer")
    if not isinstance(value.get("normalized_path"), str):
        errors.append(f"{prefix}/normalized_path: expected string")
    elif not Path(value["normalized_path"]).is_absolute():
        errors.append(f"{prefix}/normalized_path: expected absolute path")
    state = value.get("state")
    if state not in {"hashed", "missing", "not_file", "unreadable"}:
        errors.append(f"{prefix}/state: unsupported value")
    digest = value.get("sha256")
    if state == "hashed":
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"{prefix}/sha256: hashed state requires SHA256")
    elif digest is not None:
        errors.append(f"{prefix}/sha256: non-hashed state requires null")
    return errors


def _validate_machine_observation(observation: dict[str, Any]) -> list[str]:
    """allowlist detector が作る payload と source event を検査する。"""
    errors: list[str] = []
    payload = observation.get("payload")
    if not isinstance(payload, dict):
        return ["/payload: machine observation requires object"]
    errors.extend(
        f"/payload/{error}"
        for error in _field_set(
            payload,
            {
                "rule_id",
                "rule_version",
                "category",
                "subject_type",
                "normalized_subject_id",
                "summary",
                "impact",
                "human_action",
                "event_fields",
            },
        )
    )
    for name in (
        "rule_id",
        "category",
        "subject_type",
        "normalized_subject_id",
        "summary",
        "impact",
        "human_action",
    ):
        if not isinstance(payload.get(name), str):
            errors.append(f"/payload/{name}: expected string")
    if not _is_version_one(payload.get("rule_version")):
        errors.append("/payload/rule_version: expected 1")
    if not isinstance(payload.get("event_fields"), dict):
        errors.append("/payload/event_fields: expected object")
    source_event = observation.get("source_event")
    if not isinstance(source_event, dict):
        return errors
    errors.extend(
        f"/source_event/{error}"
        for error in _field_set(
            source_event,
            {
                "event_id",
                "event_type",
                "event_schema_version",
                "log_path",
                "event_sha256",
            },
        )
    )
    for name in ("event_id", "event_type", "log_path", "event_sha256"):
        if not isinstance(source_event.get(name), str):
            errors.append(f"/source_event/{name}: expected string")
    if not _is_version_one(source_event.get("event_schema_version")):
        errors.append("/source_event/event_schema_version: expected 1")
    event_sha = source_event.get("event_sha256")
    if isinstance(event_sha, str) and not re.fullmatch(r"[0-9a-f]{64}", event_sha):
        errors.append("/source_event/event_sha256: expected SHA256")
    log_path = source_event.get("log_path")
    if isinstance(log_path, str) and not Path(log_path).is_absolute():
        errors.append("/source_event/log_path: expected absolute path")
    rule_id_value = payload.get("rule_id")
    event_id_value = source_event.get("event_id")
    observation_id_value = observation.get("observation_id")
    if isinstance(rule_id_value, str) and isinstance(event_id_value, str):
        if (
            machine_observation_id(rule_id_value, event_id_value)
            != observation_id_value
        ):
            errors.append("/observation_id: machine ID does not match rule/event")
    versions = observation.get("versions")
    if isinstance(versions, dict) and versions.get("rule_id") != rule_id_value:
        errors.append("/versions/rule_id: does not match payload rule_id")
    event_fields = payload.get("event_fields")
    if isinstance(event_fields, dict):
        for envelope_name, event_name in (
            ("event_id", "event_id"),
            ("event_type", "event_type"),
            ("event_schema_version", "event_schema_version"),
        ):
            if source_event.get(envelope_name) != event_fields.get(event_name):
                errors.append(
                    f"/source_event/{envelope_name}: does not match event_fields"
                )
        if observation.get("observed_at") != event_fields.get("occurred_at"):
            errors.append("/observed_at: does not match source event")
    contract = _MACHINE_RULE_CONTRACTS.get(str(rule_id_value))
    if contract is None:
        errors.append("/payload/rule_id: rule is not allowlisted")
    else:
        expected_event, expected_category, expected_subject = contract
        if source_event.get("event_type") != expected_event:
            errors.append("/source_event/event_type: does not match rule")
        if payload.get("category") != expected_category:
            errors.append("/payload/category: does not match rule")
        if payload.get("subject_type") != expected_subject:
            errors.append("/payload/subject_type: does not match rule")
        if isinstance(event_fields, dict):
            if rule_id_value == "feedback.reporter_unavailable.v1":
                component = event_fields.get("component")
                failure_code = event_fields.get("failure_code")
                if component not in _MACHINE_REPORTER_COMPONENTS:
                    errors.append("/payload/event_fields/component: unsupported value")
                if failure_code not in _MACHINE_REPORTER_FAILURE_CODES:
                    errors.append(
                        "/payload/event_fields/failure_code: unsupported value"
                    )
                if (
                    payload.get("normalized_subject_id")
                    != f"{component}:{failure_code}"
                ):
                    errors.append(
                        "/payload/normalized_subject_id: does not match event"
                    )
            else:
                agent_call_kind = event_fields.get("agent_call_kind")
                if not isinstance(agent_call_kind, str) or not agent_call_kind:
                    errors.append(
                        "/payload/event_fields/agent_call_kind: expected string"
                    )
                if payload.get("normalized_subject_id") != agent_call_kind:
                    errors.append(
                        "/payload/normalized_subject_id: does not match event"
                    )
                schema_sha = event_fields.get("schema_sha256")
                if not isinstance(schema_sha, str) or not re.fullmatch(
                    r"[0-9a-f]{64}", schema_sha
                ):
                    errors.append(
                        "/payload/event_fields/schema_sha256: expected SHA256"
                    )
                if event_fields.get("last_failure_stage") not in {
                    "json_parse",
                    "schema_validation",
                    "deterministic_postcondition",
                    "resume_unavailable",
                    "artifact_changed",
                }:
                    errors.append(
                        "/payload/event_fields/last_failure_stage: unsupported value"
                    )
    return errors


def legacy_feedback_root(worktree: Path) -> Path:
    """一回限りの移行元である tracked state root を返す。"""
    return worktree / ".cmoc" / "gt" / "ar" / "feedback"


def validate_legacy_feedback_state(worktree: Path) -> None:
    """移行前の tracked state の JSON object と参照整合性を検査する。"""
    root = legacy_feedback_root(worktree)
    if not root.exists():
        return
    if root.is_symlink() or not root.is_dir():
        raise CmocError(
            "legacy feedback state root が通常 directory ではありません。",
            ["feedback state path を確認してください。"],
            str(root),
        )
    unsupported = [
        path
        for path in root.rglob("*")
        if (path.is_symlink() or (path.is_file() and path.suffix != ".json"))
    ]
    if unsupported:
        raise CmocError(
            "legacy feedback state に未定義 file または symlink があります。",
            ["append-only JSON record 以外の path を確認してください。"],
            "\n".join(str(path) for path in unsupported),
        )
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.rglob("*.json")):
        try:
            content = path.read_text(encoding="utf-8")
            # Git の marker は行頭に現れる。canonical JSON の文字列値に含まれる
            # marker 風の文字列は、未解決 conflict ではない。
            if any(
                line.startswith(("<<<<<<<", "|||||||", "=======", ">>>>>>>"))
                for line in content.splitlines()
            ):
                raise ValueError("unresolved conflict marker")
            value = json.loads(content)
            if not isinstance(value, dict):
                raise ValueError("JSON object required")
            if content.encode("utf-8") != canonical_json_bytes(value):
                raise ValueError("canonical JSON form required")
            errors = _validate_tracked_record(root, path, value)
            if errors:
                raise ValueError("; ".join(errors))
            records.append((path, value))
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            raise CmocError(
                "legacy feedback state が不正です。",
                ["schema 違反または conflict marker を解消してください。"],
                f"path: {path}\nerror: {exc}",
            ) from exc
    _validate_tracked_record_relations(root, records)


def _field_set(record: dict[str, Any], expected: set[str]) -> list[str]:
    """record の不足 field と未定義 field を返す。"""
    actual = set(record)
    errors = [f"missing field: {name}" for name in sorted(expected - actual)]
    errors.extend(f"unknown field: {name}" for name in sorted(actual - expected))
    return errors


def _is_string_list(value: object, *, non_empty: bool = False) -> bool:
    """重複のない文字列配列かを返す。"""
    if not isinstance(value, list) or (non_empty and not value):
        return False
    return all(isinstance(item, str) for item in value) and len(value) == len(
        set(value)
    )


def _validate_common_fields(record: dict[str, Any]) -> list[str]:
    """全 tracked record に共通する schema version を検査する。"""
    return (
        []
        if _is_version_one(record.get("schema_version"))
        else ["schema_version must be 1"]
    )


def _require_timestamp(
    record: dict[str, Any],
    name: str,
    errors: list[str],
) -> None:
    """record の必須 timestamp field を RFC 3339 として検査する。"""
    value = record.get(name)
    if not isinstance(value, str) or not _is_timestamp(value):
        errors.append(f"{name} is not an RFC 3339 timestamp")


def _validate_tracked_record(
    root: Path,
    path: Path,
    record: dict[str, Any],
) -> list[str]:
    """path から record kind を確定し、schema と path/ID 対応を検査する。"""
    relative = path.relative_to(root)
    parts = relative.parts
    errors = _validate_common_fields(record)
    kind = ""
    path_id = path.stem
    if len(parts) == 3 and parts[0] == "issue" and parts[2] == "identity.json":
        kind = "identity"
        path_id = parts[1]
    elif (
        len(parts) == 4
        and parts[0] == "issue"
        and parts[2]
        in {
            "revision",
            "occurrence",
            "assessment",
            "disposition",
        }
    ):
        kind = parts[2]
        if record.get("issue_id") != parts[1]:
            errors.append("issue_id does not match path")
    elif len(parts) == 2 and parts[0] in {"ingestion", "report"}:
        kind = parts[0]
    else:
        return [*errors, "unsupported tracked feedback record path"]

    validators = {
        "identity": _validate_identity_record,
        "revision": _validate_revision_record,
        "occurrence": _validate_occurrence_record,
        "assessment": _validate_assessment_record,
        "disposition": _validate_disposition_record,
        "ingestion": _validate_ingestion_record,
        "report": _validate_report_record,
    }
    errors.extend(validators[kind](record, path_id))
    return errors


def _validate_identity_record(record: dict[str, Any], path_id: str) -> list[str]:
    """immutable issue identity の schema を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "issue_id",
            "origin",
            "canonical_key",
            "created_from_observation_id",
            "created_at",
        },
    )
    string_fields = (
        "issue_id",
        "canonical_key",
        "created_from_observation_id",
        "created_at",
    )
    if not all(isinstance(record.get(name), str) for name in string_fields):
        errors.append("identity string field is invalid")
    if record.get("origin") not in {"agent_report", "machine_rule"}:
        errors.append("origin is invalid")
    canonical_key = record.get("canonical_key")
    if isinstance(canonical_key, str) and issue_id(canonical_key) != path_id:
        errors.append("canonical_key hash does not match issue path")
    if record.get("issue_id") != path_id:
        errors.append("issue_id does not match path")
    if not re.fullmatch(r"fbi_[a-z2-7]{26}", str(record.get("issue_id", ""))):
        errors.append("issue_id is invalid")
    if not is_observation_id(record.get("created_from_observation_id")):
        errors.append("created_from_observation_id is invalid")
    if record.get("origin") == "agent_report" and not is_uuid7_prefixed(
        record.get("created_from_observation_id"), "fbo_"
    ):
        errors.append("agent issue requires reporter UUIDv7 observation")
    if (
        record.get("origin") == "machine_rule"
        and re.fullmatch(
            r"fbo_[0-9a-f]{32}", str(record.get("created_from_observation_id", ""))
        )
        is None
    ):
        errors.append("machine issue requires deterministic observation ID")
    created_from = record.get("created_from_observation_id")
    if (
        record.get("origin") == "agent_report"
        and isinstance(canonical_key, str)
        and isinstance(created_from, str)
        and canonical_key != agent_canonical_key(created_from)
    ):
        errors.append("agent canonical_key does not match created observation")
    if (
        record.get("origin") == "machine_rule"
        and isinstance(canonical_key, str)
        and not _is_machine_canonical_key(canonical_key)
    ):
        errors.append("machine canonical_key does not match rule registry")
    _require_timestamp(record, "created_at", errors)
    return errors


def _validate_revision_record(record: dict[str, Any], path_id: str) -> list[str]:
    """issue revision の schema と content-addressed ID を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "revision_id",
            "issue_id",
            "created_at",
            "source_observation_ids",
            "category",
            "summary",
            "human_action",
            "impact",
            "cause_assessment",
            "related_issue_ids",
        },
    )
    if record.get("revision_id") != path_id or not re.fullmatch(
        r"[0-9a-f]{64}", str(record.get("revision_id", ""))
    ):
        errors.append("revision_id is invalid")
    body = {key: value for key, value in record.items() if key != "revision_id"}
    if record.get("revision_id") != sha256_bytes(canonical_json_bytes(body)):
        errors.append("revision_id hash does not match record")
    if not _is_string_list(record.get("source_observation_ids"), non_empty=True):
        errors.append("source_observation_ids is invalid")
    if not _is_string_list(record.get("related_issue_ids")):
        errors.append("related_issue_ids is invalid")
    string_fields = (
        "issue_id",
        "created_at",
        "category",
        "summary",
        "human_action",
        "impact",
    )
    if not all(isinstance(record.get(name), str) for name in string_fields):
        errors.append("revision string field is invalid")
    category_schema = reporter_input_schema().get("properties", {}).get("category", {})
    categories = (
        category_schema.get("enum", []) if isinstance(category_schema, dict) else []
    )
    if record.get("category") not in categories:
        errors.append("revision category is invalid")
    cause = record.get("cause_assessment")
    if not isinstance(cause, dict) or set(cause) != {"certainty", "description"}:
        errors.append("cause_assessment is invalid")
    elif cause.get("certainty") not in {
        "supported",
        "suspected",
        "unknown",
    } or not isinstance(cause.get("description"), str):
        errors.append("cause_assessment value is invalid")
    _require_timestamp(record, "created_at", errors)
    return errors


def _validate_occurrence_record(record: dict[str, Any], path_id: str) -> list[str]:
    """observation occurrence の schema を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "issue_id",
            "observation_id",
            "observation_sha256",
            "observed_at",
            "cmoc_session_id",
            "subcommand_invocation_id",
            "log_paths",
        },
    )
    if record.get("observation_id") != path_id:
        errors.append("observation_id does not match path")
    if not is_observation_id(record.get("observation_id")):
        errors.append("observation_id is invalid")
    string_fields = (
        "issue_id",
        "observation_id",
        "observation_sha256",
        "observed_at",
        "subcommand_invocation_id",
    )
    if not all(isinstance(record.get(name), str) for name in string_fields):
        errors.append("occurrence string field is invalid")
    session_id = record.get("cmoc_session_id")
    if session_id is not None and not isinstance(session_id, str):
        errors.append("cmoc_session_id is invalid")
    if not _is_string_list(record.get("log_paths")):
        errors.append("log_paths is invalid")
    elif any(not Path(value).is_absolute() for value in record["log_paths"]):
        errors.append("log_paths contains non-absolute path")
    if not re.fullmatch(r"[0-9a-f]{64}", str(record.get("observation_sha256", ""))):
        errors.append("observation_sha256 is invalid")
    _require_timestamp(record, "observed_at", errors)
    return errors


def _validate_assessment_record(record: dict[str, Any], path_id: str) -> list[str]:
    """machine assessment の schema と content-addressed ID を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "assessment_id",
            "issue_id",
            "assessed_at",
            "presence",
            "freshness",
            "reason_code",
            "reason",
            "compared_fingerprints",
        },
    )
    if record.get("assessment_id") != path_id or not re.fullmatch(
        r"[0-9a-f]{64}", str(record.get("assessment_id", ""))
    ):
        errors.append("assessment_id is invalid")
    body = {key: value for key, value in record.items() if key != "assessment_id"}
    if record.get("assessment_id") != sha256_bytes(canonical_json_bytes(body)):
        errors.append("assessment_id hash does not match record")
    if record.get("presence") not in {"unknown", "likely_present", "likely_absent"}:
        errors.append("presence is invalid")
    if record.get("freshness") not in {"current", "needs_revalidation", "unavailable"}:
        errors.append("freshness is invalid")
    if record.get("reason_code") not in {
        "observation_matches_current",
        "normalizer_assessment",
        "fingerprint_changed",
        "fingerprint_unavailable",
    }:
        errors.append("reason_code is invalid")
    compared_fingerprints = record.get("compared_fingerprints")
    if not isinstance(compared_fingerprints, list):
        errors.append("compared_fingerprints is invalid")
    else:
        for index, fingerprint in enumerate(compared_fingerprints):
            errors.extend(_validate_compared_fingerprint(fingerprint, index))
    if not all(
        isinstance(record.get(name), str)
        for name in ("issue_id", "assessed_at", "reason")
    ):
        errors.append("assessment string field is invalid")
    _require_timestamp(record, "assessed_at", errors)
    return errors


def _validate_compared_fingerprint(value: object, index: int) -> list[str]:
    """assessment が保持する過去値と現在値の比較 record を検査する。"""
    prefix = f"compared_fingerprints[{index}]"
    if not isinstance(value, dict):
        return [f"{prefix} is not an object"]
    errors = [
        f"{prefix}: {error}"
        for error in _field_set(
            value,
            {"path", "old_sha256", "current_sha256", "state"},
        )
    ]
    path = value.get("path")
    if not isinstance(path, str) or not Path(path).is_absolute():
        errors.append(f"{prefix}.path is invalid")
    for name in ("old_sha256", "current_sha256"):
        digest = value.get(name)
        if digest is not None and (
            not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        ):
            errors.append(f"{prefix}.{name} is invalid")
    state = value.get("state")
    if state not in {"hashed", "missing", "not_file", "unreadable"}:
        errors.append(f"{prefix}.state is invalid")
    if state == "hashed" and value.get("current_sha256") is None:
        errors.append(f"{prefix}.current_sha256 is required for hashed state")
    if state != "hashed" and value.get("current_sha256") is not None:
        errors.append(f"{prefix}.current_sha256 must be null for non-hashed state")
    return errors


def _validate_disposition_record(record: dict[str, Any], path_id: str) -> list[str]:
    """人間が作成する disposition record の schema を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "decision_id",
            "issue_id",
            "decided_at",
            "state",
            "note",
            "superseded_by",
        },
    )
    if record.get("decision_id") != path_id or not is_uuid7_prefixed(
        record.get("decision_id"), "fbd_"
    ):
        errors.append("decision_id is invalid")
    if record.get("state") not in {
        "open",
        "acknowledged",
        "resolved",
        "ignored",
        "superseded",
    }:
        errors.append("disposition state is invalid")
    superseded_by = record.get("superseded_by")
    if record.get("state") == "superseded":
        if not isinstance(superseded_by, str) or superseded_by == record.get(
            "issue_id"
        ):
            errors.append("superseded disposition requires another issue ID")
    elif superseded_by is not None:
        errors.append("superseded_by must be null unless state is superseded")
    if not all(
        isinstance(record.get(name), str)
        for name in ("decision_id", "issue_id", "decided_at", "note")
    ):
        errors.append("disposition string field is invalid")
    _require_timestamp(record, "decided_at", errors)
    return errors


def _validate_ingestion_record(record: dict[str, Any], path_id: str) -> list[str]:
    """observation 単位の ingestion receipt schema を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "observation_id",
            "observation_sha256",
            "processed_at",
            "normalization_unit_id",
            "normalizer_version",
            "status",
            "issue_ids",
            "validation_errors",
        },
    )
    if record.get("observation_id") != path_id:
        errors.append("observation_id does not match path")
    if not is_observation_id(record.get("observation_id")):
        errors.append("observation_id is invalid")
    if record.get("status") not in {"integrated", "invalid"}:
        errors.append("ingestion status is invalid")
    issue_ids = record.get("issue_ids")
    validation_errors = record.get("validation_errors")
    if not _is_string_list(issue_ids) or not _is_string_list(validation_errors):
        errors.append("ingestion arrays are invalid")
    elif record.get("status") == "integrated" and (not issue_ids or validation_errors):
        errors.append("integrated ingestion arrays are inconsistent")
    elif record.get("status") == "invalid" and (issue_ids or not validation_errors):
        errors.append("invalid ingestion arrays are inconsistent")
    string_fields = (
        "observation_id",
        "observation_sha256",
        "processed_at",
        "normalization_unit_id",
        "normalizer_version",
    )
    if not all(isinstance(record.get(name), str) for name in string_fields):
        errors.append("ingestion string field is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", str(record.get("observation_sha256", ""))):
        errors.append("observation_sha256 is invalid")
    _require_timestamp(record, "processed_at", errors)
    if not re.fullmatch(
        r"fbu_[0-9a-f]{64}", str(record.get("normalization_unit_id", ""))
    ):
        errors.append("normalization_unit_id is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", str(record.get("normalizer_version", ""))):
        errors.append("normalizer_version is invalid")
    return errors


def _validate_report_record(record: dict[str, Any], path_id: str) -> list[str]:
    """feedback report record の schema を検査する。"""
    errors = _field_set(
        record,
        {
            "schema_version",
            "report_id",
            "generated_at",
            "snapshot_manifest_sha256",
            "snapshot_observation_count",
            "processed_observation_count",
            "deferred_observation_count",
            "report_path",
            "report_sha256",
            "result",
            "state_commit_ids",
        },
    )
    if record.get("report_id") != path_id or not is_uuid7_prefixed(
        record.get("report_id"), "fbr_"
    ):
        errors.append("report_id is invalid")
    if record.get("result") not in {
        "ok",
        "attention",
        "partial",
        "interrupted",
        "error",
    }:
        errors.append("report result is invalid")
    for name in (
        "snapshot_observation_count",
        "processed_observation_count",
        "deferred_observation_count",
    ):
        value = record.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{name} is invalid")
    if not _is_string_list(record.get("state_commit_ids")):
        errors.append("state_commit_ids is invalid")
    string_fields = (
        "report_id",
        "generated_at",
        "snapshot_manifest_sha256",
        "report_path",
        "report_sha256",
    )
    if not all(isinstance(record.get(name), str) for name in string_fields):
        errors.append("report string field is invalid")
    for name in ("snapshot_manifest_sha256", "report_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", str(record.get(name, ""))):
            errors.append(f"{name} is invalid")
    _require_timestamp(record, "generated_at", errors)
    report_path_value = record.get("report_path")
    if isinstance(report_path_value, str) and not Path(report_path_value).is_absolute():
        errors.append("report_path is not absolute")
    state_commit_ids = record.get("state_commit_ids")
    if isinstance(state_commit_ids, list) and any(
        not isinstance(value, str)
        or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) is None
        for value in state_commit_ids
    ):
        errors.append("state_commit_ids contains invalid Git object ID")
    return errors


def _validate_tracked_record_relations(
    root: Path,
    records: list[tuple[Path, dict[str, Any]]],
) -> None:
    """issue 内 record の参照関係を検査する。"""
    occurrence_ids: dict[str, set[str]] = {}
    occurrence_hashes: dict[tuple[str, str], str] = {}
    revisions: list[tuple[Path, dict[str, Any]]] = []
    ingestions: list[tuple[Path, dict[str, Any]]] = []
    dispositions: list[tuple[Path, dict[str, Any]]] = []
    identities: set[str] = set()
    identity_records: dict[str, dict[str, Any]] = {}
    for path, record in records:
        relative = path.relative_to(root).parts
        if len(relative) >= 3 and relative[0] == "issue":
            current_issue_id = relative[1]
            if relative[2] == "identity.json":
                identities.add(current_issue_id)
                identity_records[current_issue_id] = record
            elif relative[2] == "occurrence":
                occurrence_ids.setdefault(current_issue_id, set()).add(
                    str(record["observation_id"])
                )
                occurrence_hashes[(current_issue_id, str(record["observation_id"]))] = (
                    str(record["observation_sha256"])
                )
            elif relative[2] == "revision":
                revisions.append((path, record))
            elif relative[2] == "disposition":
                dispositions.append((path, record))
        elif len(relative) == 2 and relative[0] == "ingestion":
            ingestions.append((path, record))
    errors: list[str] = []
    issue_directories = {
        path.relative_to(root).parts[1]
        for path, _record in records
        if len(path.relative_to(root).parts) >= 3
        and path.relative_to(root).parts[0] == "issue"
    }
    for current_issue_id in sorted(issue_directories - identities):
        errors.append(f"issue/{current_issue_id}: identity.json is missing")
    for current_issue_id, identity in identity_records.items():
        created_from = str(identity["created_from_observation_id"])
        if created_from not in occurrence_ids.get(current_issue_id, set()):
            errors.append(
                f"issue/{current_issue_id}: created observation has no occurrence"
            )
    for path, revision in revisions:
        current_issue_id = str(revision["issue_id"])
        identity_record_value = identity_records.get(current_issue_id)
        if (
            isinstance(identity_record_value, dict)
            and identity_record_value.get("origin") == "machine_rule"
        ):
            canonical_key = identity_record_value.get("canonical_key")
            rule_id = (
                canonical_key.split("\0", 1)[0]
                if isinstance(canonical_key, str)
                else ""
            )
            contract = _MACHINE_RULE_CONTRACTS.get(rule_id)
            if contract is not None and revision.get("category") != contract[1]:
                errors.append(
                    f"{path}: machine issue category does not match rule registry"
                )
        unknown = set(revision["source_observation_ids"]) - occurrence_ids.get(
            current_issue_id, set()
        )
        if unknown:
            errors.append(
                f"{path}: source observations have no occurrence: {sorted(unknown)}"
            )
        unknown_related = set(revision["related_issue_ids"]) - identities
        if unknown_related:
            errors.append(
                f"{path}: related issues do not exist: {sorted(unknown_related)}"
            )
    for path, disposition in dispositions:
        target = disposition.get("superseded_by")
        if target is not None and target not in identities:
            errors.append(f"{path}: superseded issue does not exist: {target}")
    for path, ingestion in ingestions:
        if ingestion.get("status") != "integrated":
            continue
        observation_id_value = str(ingestion["observation_id"])
        observation_hash = str(ingestion["observation_sha256"])
        for current_issue_id in ingestion["issue_ids"]:
            if current_issue_id not in identities:
                errors.append(
                    f"{path}: integrated issue does not exist: {current_issue_id}"
                )
                continue
            occurrence_hash = occurrence_hashes.get(
                (current_issue_id, observation_id_value)
            )
            if occurrence_hash != observation_hash:
                errors.append(
                    f"{path}: integrated issue occurrence/hash is missing or different: "
                    f"{current_issue_id}"
                )
    if errors:
        raise CmocError(
            "feedback state の record 関係が不正です。",
            ["欠落または不整合な append-only record を確認してください。"],
            "\n".join(errors),
        )


@dataclass(frozen=True)
class EffectiveFeedbackState:
    """manifest または migration receipt で確定した record 集合。"""

    records: dict[str, dict[str, Any]]
    unit_manifests: dict[str, dict[str, Any]]
    migration_receipt: dict[str, Any]


def migration_receipt_path(repo: Path) -> Path:
    """旧 state 移行の完了を表す immutable receipt path を返す。"""
    return migration_root(repo) / "receipt.json"


@contextmanager
def feedback_writer_lock(repo: Path) -> Iterator[None]:
    """repository ごとの feedback writer を非待機で排他する。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    repository = repo.resolve(strict=False)
    root = feedback_root(repository)
    current = root
    while current != repository:
        if current.is_symlink():
            raise CmocError(
                "feedback state root は symlink 経由で更新できません。",
                ["repository-local state path を通常 directory に戻してください。"],
                str(current),
            )
        current = current.parent
    lock_path = root / ".writer.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if lock_path.is_symlink() or (lock_path.exists() and not lock_path.is_file()):
        raise CmocError(
            "feedback writer lock path が通常 file ではありません。",
            ["lock path を人間が確認してください。"],
            str(lock_path),
        )
    with lock_path.open("a+") as lock_file:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CmocError(
                "別の feedback writer が repository-local state を更新中です。",
                ["実行中の `cmoc feedback report` が終了してから再実行してください。"],
                str(lock_path),
            ) from exc
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _canonical_object(path: Path, description: str) -> dict[str, Any]:
    """canonical JSON object を読み、不正な durable artifact を拒否する。"""
    try:
        if path.is_symlink() or not path.is_file():
            raise ValueError("regular file required")
        content = path.read_bytes()
        value = json.loads(content)
        if not isinstance(value, dict):
            raise ValueError("JSON object required")
        if content != canonical_json_bytes(value):
            raise ValueError("canonical JSON form required")
        return value
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise CmocError(
            f"{description} が不正です。",
            ["schema、hash、および file 種別を確認してください。"],
            f"path: {path}\nerror: {exc}",
        ) from exc


def _record_reference(root: Path, path: Path) -> dict[str, str]:
    """feedback root 相対 path と現在 byte 列の SHA256 を返す。"""
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_bytes(path.read_bytes()),
    }


def _validate_reference(
    root: Path,
    reference: object,
    *,
    description: str,
) -> tuple[str, Path]:
    """root 内の immutable file 参照と hash を検査する。"""
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
        raise CmocError(
            f"{description} の file 参照が不正です。",
            ["manifest の path と SHA256 を確認してください。"],
            repr(reference),
        )
    relative = reference.get("path")
    expected = reference.get("sha256")
    if (
        not isinstance(relative, str)
        or not relative
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
        or not isinstance(expected, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected) is None
    ):
        raise CmocError(
            f"{description} の file 参照が不正です。",
            ["manifest の path と SHA256 を確認してください。"],
            repr(reference),
        )
    path = root / relative
    try:
        if path.is_symlink() or not path.is_file():
            raise ValueError("referenced path is not a regular file")
        actual = sha256_bytes(path.read_bytes())
    except (OSError, ValueError) as exc:
        raise CmocError(
            f"{description} の参照先が欠落しています。",
            ["手動対応が必要な path を確認してください。"],
            str(path),
        ) from exc
    if actual != expected:
        raise CmocError(
            f"{description} の SHA256 が一致しません。",
            ["改変された immutable file を人間が確認してください。"],
            f"path: {path}\nexpected: {expected}\nactual: {actual}",
        )
    return relative, path


def _record_kind(relative: str) -> str | None:
    """normalized record path から schema kind を返す。"""
    parts = Path(relative).parts
    if len(parts) == 3 and parts[0] == "issue" and parts[2] == "identity.json":
        return "identity"
    if (
        len(parts) == 4
        and parts[0] == "issue"
        and parts[2] in {"revision", "occurrence", "assessment", "disposition"}
    ):
        return parts[2]
    if len(parts) == 2 and parts[0] == "ingestion":
        return "ingestion"
    return None


def _validate_effective_record(
    root: Path,
    relative: str,
    record: dict[str, Any],
) -> None:
    """effective normalized record の path、schema、canonical form を検査する。"""
    kind = _record_kind(relative)
    path = root / relative
    if kind is None:
        raise CmocError(
            "normalization manifest が未定義 path を参照しています。",
            ["manifest と record path を確認してください。"],
            relative,
        )
    errors = _validate_tracked_record(root, path, record)
    if errors:
        raise CmocError(
            "repository-local feedback record が schema に適合しません。",
            ["record を自動上書きせず、手動で corruption を確認してください。"],
            f"path: {path}\nerrors: {'; '.join(errors)}",
        )


def _validate_checkpoint_reference(
    repo: Path,
    *,
    unit_id: str,
    observations: list[dict[str, Any]],
    candidate_revision_ids: list[str],
    schema_sha256: str,
    normalizer_version_value: str,
    checkpoint_sha256: object,
) -> None:
    """checkpoint の hash と unit 入力との対応を record 保存前に検査する。"""
    if checkpoint_sha256 is None:
        return
    checkpoint = normalization_checkpoint_root(repo) / f"{unit_id}.json"
    if (
        not isinstance(checkpoint_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", checkpoint_sha256) is None
        or checkpoint.is_symlink()
        or not checkpoint.is_file()
        or sha256_bytes(checkpoint.read_bytes()) != checkpoint_sha256
    ):
        raise CmocError(
            "normalization unit の checkpoint が欠落または不一致です。",
            ["手動対応が必要な checkpoint path を確認してください。"],
            str(checkpoint),
        )
    checkpoint_record = _canonical_object(
        checkpoint, "normalization agent output checkpoint"
    )
    if (
        set(checkpoint_record)
        != {
            "schema_version",
            "normalization_unit_id",
            "observation_sha256",
            "candidate_revision_ids",
            "schema_sha256",
            "normalizer_version",
            "structured_output",
        }
        or checkpoint_record.get("schema_version") != 1
        or checkpoint_record.get("normalization_unit_id") != unit_id
        or len(observations) != 1
        or checkpoint_record.get("observation_sha256")
        != observations[0].get("observation_sha256")
        or checkpoint_record.get("candidate_revision_ids")
        != sorted(candidate_revision_ids)
        or checkpoint_record.get("schema_sha256") != schema_sha256
        or checkpoint_record.get("normalizer_version") != normalizer_version_value
        or not isinstance(checkpoint_record.get("structured_output"), dict)
    ):
        raise CmocError(
            "normalization checkpoint が unit の入力と一致しません。",
            ["checkpoint と unit manifest を確認してください。"],
            str(checkpoint),
        )


def _validate_unit_manifest(
    repo: Path,
    path: Path,
) -> tuple[str, dict[str, Any], dict[str, dict[str, Any]]]:
    """unit manifest と全参照 record/checkpoint を検査する。"""
    manifest = _canonical_object(path, "normalization unit manifest")
    expected_fields = {
        "schema_version",
        "normalization_unit_id",
        "observations",
        "candidate_revision_ids",
        "normalizer_schema_sha256",
        "normalizer_version",
        "records",
        "checkpoint_sha256",
    }
    if set(manifest) != expected_fields or manifest.get("schema_version") != 1:
        raise CmocError(
            "normalization unit manifest の schema が不正です。",
            ["manifest field を確認してください。"],
            str(path),
        )
    unit_id = manifest.get("normalization_unit_id")
    observations = manifest.get("observations")
    candidate_ids = manifest.get("candidate_revision_ids")
    schema_sha = manifest.get("normalizer_schema_sha256")
    version = manifest.get("normalizer_version")
    references = manifest.get("records")
    if (
        not isinstance(unit_id, str)
        or path.stem != unit_id
        or not isinstance(observations, list)
        or not observations
        or not isinstance(candidate_ids, list)
        or any(not isinstance(value, str) for value in candidate_ids)
        or len(candidate_ids) != len(set(candidate_ids))
        or not isinstance(schema_sha, str)
        or re.fullmatch(r"[0-9a-f]{64}", schema_sha) is None
        or not isinstance(version, str)
        or re.fullmatch(r"[0-9a-f]{64}", version) is None
        or not isinstance(references, list)
        or not references
    ):
        raise CmocError(
            "normalization unit manifest の field が不正です。",
            ["unit の入力、schema hash、および record 参照を確認してください。"],
            str(path),
        )
    observation_ids: list[str] = []
    for item in observations:
        if (
            not isinstance(item, dict)
            or set(item) != {"observation_id", "observation_sha256"}
            or not is_observation_id(item.get("observation_id"))
            or not isinstance(item.get("observation_sha256"), str)
            or re.fullmatch(r"[0-9a-f]{64}", item["observation_sha256"]) is None
        ):
            raise CmocError(
                "normalization unit manifest の observation 参照が不正です。",
                ["observation ID と SHA256 を確認してください。"],
                f"path: {path}\nvalue: {item!r}",
            )
        observation_ids.append(str(item["observation_id"]))
    if (
        len(observation_ids) != len(set(observation_ids))
        or observations
        != sorted(observations, key=lambda item: str(item["observation_id"]))
        or candidate_ids != sorted(set(candidate_ids))
        or normalization_unit_id(
            observation_ids, [str(value) for value in candidate_ids], schema_sha
        )
        != unit_id
    ):
        raise CmocError(
            "normalization unit ID が manifest 入力と一致しません。",
            ["unit manifest の corruption を確認してください。"],
            str(path),
        )
    checkpoint_sha = manifest.get("checkpoint_sha256")
    _validate_checkpoint_reference(
        repo,
        unit_id=unit_id,
        observations=observations,
        candidate_revision_ids=[str(value) for value in candidate_ids],
        schema_sha256=schema_sha,
        normalizer_version_value=version,
        checkpoint_sha256=checkpoint_sha,
    )
    root = feedback_root(repo)
    records: dict[str, dict[str, Any]] = {}
    for reference in references:
        relative, record_path_value = _validate_reference(
            root, reference, description="normalization unit record"
        )
        if relative in records:
            raise CmocError(
                "normalization unit manifest に重複 record があります。",
                ["manifest を確認してください。"],
                relative,
            )
        record = _canonical_object(record_path_value, "normalization unit record")
        _validate_effective_record(root, relative, record)
        if _record_kind(relative) == "disposition":
            raise CmocError(
                "normalization unit は human disposition を生成できません。",
                ["human disposition writer と unit manifest を確認してください。"],
                relative,
            )
        if (
            _record_kind(relative) == "ingestion"
            and record.get("normalization_unit_id") != unit_id
        ):
            raise CmocError(
                "ingestion receipt の normalization unit ID が一致しません。",
                ["unit manifest と receipt を確認してください。"],
                relative,
            )
        records[relative] = record
    reference_paths = [
        str(reference.get("path"))
        for reference in references
        if isinstance(reference, dict)
    ]
    if reference_paths != sorted(reference_paths):
        raise CmocError(
            "normalization unit manifest の record 参照順が canonical ではありません。",
            ["manifest の record path 順を確認してください。"],
            str(path),
        )
    return unit_id, manifest, records


def _validate_migration_receipt(
    repo: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """migration receipt と取り込み済み record を検査する。"""
    path = migration_receipt_path(repo)
    receipt = _canonical_object(path, "feedback migration receipt")
    return validate_migration_artifacts(repo, receipt, source_path=path)


def validate_migration_artifacts(
    repo: Path,
    receipt: dict[str, Any],
    *,
    source_path: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """receipt 候補の schema と全 migration output を削除 commit 前に検査する。"""
    path = source_path
    required = {
        "schema_version",
        "migration_version",
        "completed_at",
        "source_branch",
        "source_commit",
        "source_tree",
        "candidates",
        "records",
        "legacy_reports",
        "baseline",
    }
    if (
        set(receipt) != required
        or receipt.get("schema_version") != 1
        or receipt.get("migration_version") != 1
        or not isinstance(receipt.get("source_branch"), str)
        or not receipt.get("source_branch")
        or not isinstance(receipt.get("completed_at"), str)
        or not _is_timestamp(receipt["completed_at"])
        or not isinstance(receipt.get("records"), list)
        or not isinstance(receipt.get("candidates"), list)
        or not isinstance(receipt.get("legacy_reports"), list)
    ):
        raise CmocError(
            "feedback migration receipt の schema が不正です。",
            ["receipt と migration archive を確認してください。"],
            str(path),
        )
    root = feedback_root(repo)
    candidates_by_branch: dict[str, dict[str, Any]] = {}
    for candidate in receipt["candidates"]:
        if (
            not isinstance(candidate, dict)
            or set(candidate) != {"branch", "commit", "tree", "files"}
            or not isinstance(candidate.get("branch"), str)
            or not candidate.get("branch")
            or re.fullmatch(
                r"[0-9a-f]{40}|[0-9a-f]{64}", str(candidate.get("commit", ""))
            )
            is None
            or re.fullmatch(
                r"[0-9a-f]{40}|[0-9a-f]{64}", str(candidate.get("tree", ""))
            )
            is None
            or not isinstance(candidate.get("files"), list)
        ):
            raise CmocError(
                "feedback migration candidate の schema が不正です。",
                ["migration archive metadata を確認してください。"],
                repr(candidate),
            )
        branch = str(candidate["branch"])
        if branch in candidates_by_branch:
            raise CmocError(
                "feedback migration candidate branch が重複しています。",
                ["migration receipt を確認してください。"],
                branch,
            )
        candidates_by_branch[branch] = candidate
        seen_legacy_paths: set[str] = set()
        for reference in candidate["files"]:
            if (
                not isinstance(reference, dict)
                or set(reference) != {"legacy_path", "archive_path", "sha256"}
                or not isinstance(reference.get("legacy_path"), str)
                or not isinstance(reference.get("archive_path"), str)
                or Path(str(reference.get("legacy_path"))).is_absolute()
                or ".." in Path(str(reference.get("legacy_path"))).parts
                or Path(str(reference.get("archive_path"))).is_absolute()
                or ".." in Path(str(reference.get("archive_path"))).parts
                or Path(str(reference.get("archive_path"))).parts[:3]
                != ("migration", "v1", "archive")
                or re.fullmatch(r"[0-9a-f]{64}", str(reference.get("sha256", "")))
                is None
            ):
                raise CmocError(
                    "feedback migration archive 参照が不正です。",
                    ["candidate file metadata を確認してください。"],
                    repr(reference),
                )
            legacy_path_value = str(reference["legacy_path"])
            if legacy_path_value in seen_legacy_paths:
                raise CmocError(
                    "feedback migration archive に重複 path があります。",
                    ["candidate file metadata を確認してください。"],
                    legacy_path_value,
                )
            seen_legacy_paths.add(legacy_path_value)
            expected_archive_path = (
                Path("migration")
                / "v1"
                / "archive"
                / hashlib.sha256(branch.encode("utf-8")).hexdigest()
                / str(candidate["tree"])
                / "tree"
                / legacy_path_value
            )
            if Path(str(reference["archive_path"])) != expected_archive_path:
                raise CmocError(
                    "feedback migration archive path が candidate と一致しません。",
                    ["branch、tree、legacy path の archive 対応を確認してください。"],
                    repr(reference),
                )
            archive_path = root / str(reference["archive_path"])
            if (
                archive_path.is_symlink()
                or not archive_path.is_file()
                or sha256_bytes(archive_path.read_bytes()) != reference["sha256"]
            ):
                raise CmocError(
                    "feedback migration archive が欠落または不一致です。",
                    ["migration archive を人間が確認してください。"],
                    str(archive_path),
                )

    source_commit = receipt.get("source_commit")
    source_tree = receipt.get("source_tree")
    source_candidate = candidates_by_branch.get(str(receipt["source_branch"]))
    if source_candidate is None:
        if candidates_by_branch or source_commit is not None or source_tree is not None:
            raise CmocError(
                "feedback migration source が candidate と一致しません。",
                ["source branch、commit、および tree を確認してください。"],
                str(path),
            )
    elif (
        source_candidate.get("commit") != source_commit
        or source_candidate.get("tree") != source_tree
    ):
        raise CmocError(
            "feedback migration source commit/tree が candidate と一致しません。",
            ["migration receipt を確認してください。"],
            str(path),
        )

    source_files = (
        {
            str(item["legacy_path"]): item
            for item in source_candidate["files"]
            if isinstance(item, dict)
        }
        if source_candidate is not None
        else {}
    )
    unsupported_source_paths = sorted(
        relative
        for relative in source_files
        if not relative.startswith(("issue/", "ingestion/", "report/"))
    )
    if unsupported_source_paths:
        raise CmocError(
            "feedback migration source に未定義 record path があります。",
            ["source archive を人間が確認してください。"],
            "\n".join(unsupported_source_paths),
        )
    records: dict[str, dict[str, Any]] = {}
    for reference in receipt["records"]:
        relative, record_path_value = _validate_reference(
            root, reference, description="migrated feedback record"
        )
        source_reference = source_files.get(relative)
        if source_reference is None or source_reference.get("sha256") != reference.get(
            "sha256"
        ):
            raise CmocError(
                "migrated feedback record が選択した source tree と一致しません。",
                ["migration receipt と source archive を確認してください。"],
                relative,
            )
        record = _canonical_object(record_path_value, "migrated feedback record")
        _validate_effective_record(root, relative, record)
        if relative in records:
            raise CmocError(
                "feedback migration receipt に重複 record があります。",
                ["migration receipt を確認してください。"],
                relative,
            )
        records[relative] = record
    expected_record_paths = {
        relative
        for relative in source_files
        if relative.startswith(("issue/", "ingestion/"))
    }
    if set(records) != expected_record_paths:
        raise CmocError(
            "feedback migration receipt の record 集合が source tree と一致しません。",
            ["欠落または余分な migrated record を確認してください。"],
            f"expected: {sorted(expected_record_paths)}\nactual: {sorted(records)}",
        )
    legacy_reports: dict[str, dict[str, Any]] = {}
    for metadata in receipt["legacy_reports"]:
        if (
            not isinstance(metadata, dict)
            or set(metadata)
            != {
                "report_id",
                "source_branch",
                "source_commit",
                "legacy_path",
                "archive_path",
                "sha256",
            }
            or not is_uuid7_prefixed(metadata.get("report_id"), "fbr_")
            or metadata.get("source_branch") != receipt["source_branch"]
            or metadata.get("source_commit") != source_commit
        ):
            raise CmocError(
                "legacy feedback report metadata が不正です。",
                ["migration receipt と archive を確認してください。"],
                repr(metadata),
            )
        report_id_value = str(metadata["report_id"])
        legacy_path_value = str(metadata["legacy_path"])
        source_reference = source_files.get(legacy_path_value)
        if (
            legacy_path_value != f"report/{report_id_value}.json"
            or source_reference is None
            or source_reference.get("archive_path") != metadata.get("archive_path")
            or source_reference.get("sha256") != metadata.get("sha256")
        ):
            raise CmocError(
                "legacy feedback report metadata が source archive と一致しません。",
                ["migration receipt と candidate archive を確認してください。"],
                repr(metadata),
            )
        archive_path = root / str(metadata.get("archive_path", ""))
        if (
            archive_path.is_symlink()
            or not archive_path.is_file()
            or sha256_bytes(archive_path.read_bytes()) != metadata.get("sha256")
        ):
            raise CmocError(
                "legacy feedback report archive が欠落または不一致です。",
                ["migration archive を人間が確認してください。"],
                str(archive_path),
            )
        legacy_record = _canonical_object(archive_path, "legacy feedback report")
        legacy_errors = _validate_report_record(legacy_record, report_id_value)
        if legacy_errors:
            raise CmocError(
                "legacy feedback report record の schema が不正です。",
                ["migration archive を人間が確認してください。"],
                "; ".join(legacy_errors),
            )
        legacy_snapshot = report_snapshot_root(repo) / f"{report_id_value}.json"
        legacy_markdown = Path(str(legacy_record["report_path"]))
        if (
            legacy_snapshot.is_symlink()
            or not legacy_snapshot.is_file()
            or sha256_bytes(legacy_snapshot.read_bytes())
            != legacy_record["snapshot_manifest_sha256"]
            or legacy_markdown.is_symlink()
            or not legacy_markdown.is_file()
            or sha256_bytes(legacy_markdown.read_bytes())
            != legacy_record["report_sha256"]
        ):
            raise CmocError(
                "legacy feedback report artifact が欠落または不一致です。",
                ["report snapshot と Markdown report を確認してください。"],
                report_id_value,
            )
        if report_id_value in legacy_reports:
            raise CmocError(
                "legacy feedback report metadata が重複しています。",
                ["migration receipt を確認してください。"],
                report_id_value,
            )
        legacy_reports[report_id_value] = legacy_record
    expected_legacy_report_paths = {
        relative for relative in source_files if relative.startswith("report/")
    }
    actual_legacy_report_paths = {
        str(metadata["legacy_path"])
        for metadata in receipt["legacy_reports"]
        if isinstance(metadata, dict)
    }
    if actual_legacy_report_paths != expected_legacy_report_paths:
        raise CmocError(
            "legacy feedback report metadata の集合が source tree と一致しません。",
            ["migration receipt と source archive を確認してください。"],
            f"expected: {sorted(expected_legacy_report_paths)}\nactual: {sorted(actual_legacy_report_paths)}",
        )
    baseline = receipt.get("baseline")
    normal_legacy_reports = [
        record
        for record in legacy_reports.values()
        if record.get("result") in {"ok", "attention"}
    ]
    expected_baseline_id = (
        str(
            max(
                normal_legacy_reports,
                key=lambda record: (
                    parse_rfc3339(str(record["generated_at"])),
                    str(record["report_id"]),
                ),
            )["report_id"]
        )
        if normal_legacy_reports
        else None
    )
    actual_baseline_id = (
        baseline.get("legacy_report_id") if isinstance(baseline, dict) else None
    )
    if actual_baseline_id != expected_baseline_id:
        raise CmocError(
            "feedback migration baseline が直前の正常 legacy report と一致しません。",
            ["legacy report の generated_at と report ID を確認してください。"],
            f"expected: {expected_baseline_id!r}\nactual: {actual_baseline_id!r}",
        )
    if baseline is not None:
        if (
            not isinstance(baseline, dict)
            or set(baseline) != {"legacy_report_id", "state_snapshot_id"}
            or not isinstance(baseline.get("legacy_report_id"), str)
            or not isinstance(baseline.get("state_snapshot_id"), str)
        ):
            raise CmocError(
                "feedback migration baseline が不正です。",
                ["legacy report と state snapshot の対応を確認してください。"],
                repr(baseline),
            )
        legacy_report = legacy_reports.get(str(baseline["legacy_report_id"]))
        if legacy_report is None or legacy_report.get("result") not in {
            "ok",
            "attention",
        }:
            raise CmocError(
                "feedback migration baseline が正常 legacy report を参照していません。",
                ["migration receipt の baseline を確認してください。"],
                repr(baseline),
            )
        _load_state_snapshot(repo, str(baseline["state_snapshot_id"]))
    return receipt, records


def load_effective_feedback_state(repo: Path) -> EffectiveFeedbackState:
    """valid な manifest/receipt が確定する normalized state を読む。"""
    receipt, records = _validate_migration_receipt(repo)
    manifests: dict[str, dict[str, Any]] = {}
    unit_root = normalization_unit_root(repo)
    if unit_root.exists() and (unit_root.is_symlink() or not unit_root.is_dir()):
        raise CmocError(
            "normalization unit root が通常 directory ではありません。",
            ["state root を確認してください。"],
            str(unit_root),
        )
    if unit_root.is_dir():
        for path in sorted(unit_root.glob("*.json")):
            unit_id, manifest, unit_records = _validate_unit_manifest(repo, path)
            manifests[unit_id] = manifest
            for relative, record in unit_records.items():
                existing = records.get(relative)
                if existing is not None and canonical_json_bytes(
                    existing
                ) != canonical_json_bytes(record):
                    raise CmocError(
                        "effective feedback record の参照が競合しています。",
                        ["unit manifest と migration receipt を確認してください。"],
                        relative,
                    )
                records[relative] = record

    # disposition は human writer が 1 record ごとに durable 確定する。
    issue_root = feedback_root(repo) / "issue"
    if issue_root.is_dir():
        for path in sorted(issue_root.glob("*/disposition/*.json")):
            relative = path.relative_to(feedback_root(repo)).as_posix()
            record = _canonical_object(path, "human disposition record")
            _validate_effective_record(feedback_root(repo), relative, record)
            records[relative] = record

    observation_hashes = {
        (str(record.get("observation_id")), str(record.get("observation_sha256")))
        for relative, record in records.items()
        if relative.startswith("ingestion/") or "/occurrence/" in relative
    }
    revision_ids = {
        str(record.get("revision_id"))
        for relative, record in records.items()
        if "/revision/" in relative
    }
    for unit_id, manifest in manifests.items():
        missing_observations = [
            item
            for item in manifest["observations"]
            if (
                str(item.get("observation_id")),
                str(item.get("observation_sha256")),
            )
            not in observation_hashes
        ]
        missing_candidates = sorted(
            set(str(value) for value in manifest["candidate_revision_ids"])
            - revision_ids
        )
        if missing_observations or missing_candidates:
            raise CmocError(
                "normalization unit manifest の入力参照が effective state に存在しません。",
                [
                    "unit manifest、occurrence、ingestion receipt、revision を確認してください。"
                ],
                (
                    f"unit: {unit_id}\n"
                    f"observations: {missing_observations!r}\n"
                    f"candidate revisions: {missing_candidates!r}"
                ),
            )

    relation_records = [
        (feedback_root(repo) / relative, record)
        for relative, record in sorted(records.items())
    ]
    _validate_tracked_record_relations(feedback_root(repo), relation_records)
    return EffectiveFeedbackState(records, manifests, receipt)


def _normalized_record_paths(repo: Path) -> set[str]:
    """manifest の有無にかかわらず実在する normalized artifact path を返す。"""
    root = feedback_root(repo)
    paths: set[str] = set()
    for directory in (root / "issue", root / "ingestion"):
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if path.is_dir() and not path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            paths.add(relative)
    return paths


def validate_feedback_state(repo: Path, *, require_no_orphans: bool = False) -> None:
    """effective state、unit、report、snapshot の schema/hash/参照を検査する。"""
    state = load_effective_feedback_state(repo)
    effective = set(state.records)
    orphans = sorted(_normalized_record_paths(repo) - effective)
    if require_no_orphans and orphans:
        raise CmocError(
            "manifest 確定前の orphan feedback record が残っています。",
            ["自動再開できない path を人間が確認してください。"],
            "\n".join(str(feedback_root(repo) / path) for path in orphans),
        )
    _validated_report_records(repo, state)


def effective_ingestion_receipts(repo: Path) -> dict[str, dict[str, Any]]:
    """effective ingestion receipt を observation ID で返す。"""
    state = load_effective_feedback_state(repo)
    return {
        str(record["observation_id"]): record
        for relative, record in state.records.items()
        if relative.startswith("ingestion/")
    }


def _durable_unlink(path: Path) -> None:
    """不要になった recovery metadata を削除し directory entry を flush する。"""
    if not path.exists():
        return
    path.unlink()
    directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _normalization_recovery(
    *,
    normalization_unit_id_value: str,
    observations: list[dict[str, str]],
    candidate_revision_ids: list[str],
    normalizer_schema_sha256: str,
    normalizer_version_value: str,
    records: list[tuple[str, dict[str, Any]]],
    checkpoint_sha256: str | None,
) -> dict[str, Any]:
    """未確定 unit を同じ byte 列で再開する recovery record を構築する。"""
    return {
        "schema_version": 1,
        "normalization_unit_id": normalization_unit_id_value,
        "observations": sorted(observations, key=lambda item: item["observation_id"]),
        "candidate_revision_ids": sorted(set(candidate_revision_ids)),
        "normalizer_schema_sha256": normalizer_schema_sha256,
        "normalizer_version": normalizer_version_value,
        "records": [{"kind": kind, "record": record} for kind, record in records],
        "checkpoint_sha256": checkpoint_sha256,
    }


def _load_normalization_recovery(
    path: Path,
) -> tuple[dict[str, Any], list[tuple[str, dict[str, Any]]]]:
    """normalization recovery record を検査して record payload を復元する。"""
    recovery = _canonical_object(path, "normalization unit recovery metadata")
    expected = {
        "schema_version",
        "normalization_unit_id",
        "observations",
        "candidate_revision_ids",
        "normalizer_schema_sha256",
        "normalizer_version",
        "records",
        "checkpoint_sha256",
    }
    record_entries = recovery.get("records")
    if (
        set(recovery) != expected
        or recovery.get("schema_version") != 1
        or recovery.get("normalization_unit_id") != path.stem
        or not isinstance(recovery.get("observations"), list)
        or not isinstance(recovery.get("candidate_revision_ids"), list)
        or not isinstance(record_entries, list)
        or not record_entries
    ):
        raise CmocError(
            "normalization unit recovery metadata の schema が不正です。",
            ["未確定 unit の recovery path を人間が確認してください。"],
            str(path),
        )
    records: list[tuple[str, dict[str, Any]]] = []
    for entry in record_entries:
        if (
            not isinstance(entry, dict)
            or set(entry) != {"kind", "record"}
            or not isinstance(entry.get("kind"), str)
            or not isinstance(entry.get("record"), dict)
        ):
            raise CmocError(
                "normalization recovery の record が不正です。",
                ["未確定 unit の recovery path を人間が確認してください。"],
                str(path),
            )
        records.append((str(entry["kind"]), entry["record"]))
    return recovery, records


def recover_normalization_units(repo: Path) -> list[str]:
    """durable recovery metadata がある未確定 unit を manifest まで確定する。"""
    recovered: list[str] = []
    root = normalization_recovery_root(repo)
    if root.exists() and (root.is_symlink() or not root.is_dir()):
        raise CmocError(
            "normalization recovery root が通常 directory ではありません。",
            ["手動対応が必要な recovery path を確認してください。"],
            str(root),
        )
    if not root.is_dir():
        return recovered
    unsupported = [
        path
        for path in root.iterdir()
        if path.is_symlink() or not path.is_file() or path.suffix != ".json"
    ]
    if unsupported:
        raise CmocError(
            "normalization recovery root に未定義 artifact があります。",
            ["手動対応が必要な recovery path を確認してください。"],
            "\n".join(str(path) for path in unsupported),
        )
    for path in sorted(root.glob("*.json")):
        recovery, records = _load_normalization_recovery(path)
        recovered.append(
            publish_normalization_unit(
                repo,
                normalization_unit_id_value=str(recovery["normalization_unit_id"]),
                observations=recovery["observations"],
                candidate_revision_ids=recovery["candidate_revision_ids"],
                normalizer_schema_sha256=str(recovery["normalizer_schema_sha256"]),
                normalizer_version_value=str(recovery["normalizer_version"]),
                records=records,
                checkpoint_sha256=recovery.get("checkpoint_sha256"),
            )
        )
    return recovered


def publish_normalization_unit(
    repo: Path,
    *,
    normalization_unit_id_value: str,
    observations: list[dict[str, str]],
    candidate_revision_ids: list[str],
    normalizer_schema_sha256: str,
    normalizer_version_value: str,
    records: list[tuple[str, dict[str, Any]]],
    checkpoint_sha256: str | None,
) -> str:
    """record を durable に保存し、unit manifest を最後に確定する。"""
    manifest_path = (
        normalization_unit_root(repo) / f"{normalization_unit_id_value}.json"
    )
    recovery_path = (
        normalization_recovery_root(repo) / f"{normalization_unit_id_value}.json"
    )
    if manifest_path.is_file():
        unit_id_value, existing_manifest, _records = _validate_unit_manifest(
            repo, manifest_path
        )
        expected_inputs = _normalization_recovery(
            normalization_unit_id_value=normalization_unit_id_value,
            observations=observations,
            candidate_revision_ids=candidate_revision_ids,
            normalizer_schema_sha256=normalizer_schema_sha256,
            normalizer_version_value=normalizer_version_value,
            records=records,
            checkpoint_sha256=checkpoint_sha256,
        )
        for name in (
            "observations",
            "candidate_revision_ids",
            "normalizer_schema_sha256",
            "normalizer_version",
            "checkpoint_sha256",
        ):
            if existing_manifest.get(name) != expected_inputs[name]:
                raise CmocError(
                    "確定済み normalization unit の入力が再実行時と異なります。",
                    ["raw observation と unit manifest を確認してください。"],
                    f"unit: {unit_id_value}\nfield: {name}",
                )
        _durable_unlink(recovery_path)
        return unit_id_value

    requested_recovery = _normalization_recovery(
        normalization_unit_id_value=normalization_unit_id_value,
        observations=observations,
        candidate_revision_ids=candidate_revision_ids,
        normalizer_schema_sha256=normalizer_schema_sha256,
        normalizer_version_value=normalizer_version_value,
        records=records,
        checkpoint_sha256=checkpoint_sha256,
    )
    if recovery_path.is_file():
        recovery, recovered_records = _load_normalization_recovery(recovery_path)
        for name in (
            "normalization_unit_id",
            "observations",
            "candidate_revision_ids",
            "normalizer_schema_sha256",
            "normalizer_version",
            "checkpoint_sha256",
        ):
            if recovery.get(name) != requested_recovery[name]:
                raise CmocError(
                    "未確定 normalization unit の recovery 入力が異なります。",
                    ["recovery metadata と現在の unit 入力を確認してください。"],
                    f"path: {recovery_path}\nfield: {name}",
                )
        records = recovered_records
    if (
        normalization_unit_id(
            [item["observation_id"] for item in observations],
            candidate_revision_ids,
            normalizer_schema_sha256,
        )
        != normalization_unit_id_value
    ):
        raise ValueError("normalization unit ID does not match its inputs")
    _validate_checkpoint_reference(
        repo,
        unit_id=normalization_unit_id_value,
        observations=observations,
        candidate_revision_ids=candidate_revision_ids,
        schema_sha256=normalizer_schema_sha256,
        normalizer_version_value=normalizer_version_value,
        checkpoint_sha256=checkpoint_sha256,
    )

    root = feedback_root(repo)
    if any(kind == "disposition" for kind, _record in records):
        raise CmocError(
            "normalization unit は human disposition を生成できません。",
            ["human disposition は人間の明示操作で別途保存してください。"],
            normalization_unit_id_value,
        )
    paths = [record_path(repo, record, kind) for kind, record in records]
    if len(paths) != len(set(paths)):
        raise CmocError(
            "normalization unit が同じ path を複数回生成しています。",
            ["unit の record 集合を確認してください。"],
            normalization_unit_id_value,
        )
    current = load_effective_feedback_state(repo)
    tentative = dict(current.records)
    for (kind, record), path in zip(records, paths, strict=True):
        relative = path.relative_to(root).as_posix()
        if kind != _record_kind(relative):
            raise ValueError(f"record kind does not match path: {relative}")
        _validate_effective_record(root, relative, record)
        existing = tentative.get(relative)
        if existing is not None and canonical_json_bytes(
            existing
        ) != canonical_json_bytes(record):
            raise CmocError(
                "normalization unit が既存 effective record と競合しています。",
                ["record path を人間が確認してください。"],
                relative,
            )
        tentative[relative] = record
    _validate_tracked_record_relations(
        root,
        [(root / relative, record) for relative, record in sorted(tentative.items())],
    )

    if not recovery_path.is_file():
        write_immutable_json(recovery_path, requested_recovery)

    references: list[dict[str, str]] = []
    for (_kind, record), path in zip(records, paths, strict=True):
        write_feedback_record(path, record)
        references.append(_record_reference(root, path))
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "normalization_unit_id": normalization_unit_id_value,
        "observations": sorted(observations, key=lambda item: item["observation_id"]),
        "candidate_revision_ids": sorted(set(candidate_revision_ids)),
        "normalizer_schema_sha256": normalizer_schema_sha256,
        "normalizer_version": normalizer_version_value,
        "records": sorted(references, key=lambda item: item["path"]),
        "checkpoint_sha256": checkpoint_sha256,
    }
    try:
        write_immutable_json(manifest_path, manifest)
    except Exception as exc:
        raise CmocError(
            "normalization unit manifest を durable に確定できません。",
            ["一部 record を effective state として扱わず、再実行してください。"],
            str(manifest_path),
        ) from exc
    _validate_unit_manifest(repo, manifest_path)
    _durable_unlink(recovery_path)
    return normalization_unit_id_value


def build_state_snapshot(
    repo: Path,
    *,
    created_at: str,
) -> tuple[dict[str, Any], str]:
    """現在の effective state から immutable state snapshot を作成する。"""
    state = load_effective_feedback_state(repo)
    return write_state_snapshot_from_records(
        repo,
        records=state.records,
        normalization_unit_ids=list(state.unit_manifests),
        created_at=created_at,
    )


def write_state_snapshot_from_records(
    repo: Path,
    *,
    records: dict[str, dict[str, Any]],
    normalization_unit_ids: list[str],
    created_at: str,
) -> tuple[dict[str, Any], str]:
    """検証済み record 集合から state snapshot を durable 保存する。"""
    state = EffectiveFeedbackState(records, {}, {})
    root = feedback_root(repo)
    for relative, record in state.records.items():
        _validate_effective_record(root, relative, record)
        path = root / relative
        if (
            path.is_symlink()
            or not path.is_file()
            or path.read_bytes() != canonical_json_bytes(record)
        ):
            raise CmocError(
                "state snapshot の source record が保存済み byte 列と一致しません。",
                ["snapshot source path を人間が確認してください。"],
                str(path),
            )
    _validate_tracked_record_relations(
        root,
        [
            (root / relative, record)
            for relative, record in sorted(state.records.items())
        ],
    )
    grouped: dict[str, dict[str, Any]] = {}
    ingestion: list[dict[str, str]] = []
    for relative in sorted(state.records):
        path = root / relative
        reference = _record_reference(root, path)
        parts = Path(relative).parts
        if parts[0] == "ingestion":
            ingestion.append(reference)
            continue
        if parts[0] != "issue":
            continue
        bucket = grouped.setdefault(
            parts[1],
            {
                "identity": None,
                "revision": [],
                "occurrence": [],
                "assessment": [],
                "disposition": [],
            },
        )
        kind = "identity" if parts[2] == "identity.json" else parts[2]
        if kind == "identity":
            bucket[kind] = reference
        else:
            bucket[kind].append(reference)
    views = load_issue_views(repo, state=state)
    issues: list[dict[str, Any]] = []
    for current_issue_id, view in sorted(views.items()):
        bucket = grouped[current_issue_id]

        def matching(
            kind: str, field_name: str, value: object
        ) -> dict[str, str] | None:
            if value is None:
                return None
            for reference in bucket[kind]:
                record = state.records[reference["path"]]
                if record.get(field_name) == value:
                    return reference
            raise AssertionError(f"effective {kind} reference is missing")

        issues.append(
            {
                "issue_id": current_issue_id,
                "identity": bucket["identity"],
                "effective_revision": matching(
                    "revision", "revision_id", view.revision.get("revision_id")
                ),
                "effective_assessment": matching(
                    "assessment",
                    "assessment_id",
                    view.assessment.get("assessment_id")
                    if view.assessment is not None
                    else None,
                ),
                "effective_disposition": matching(
                    "disposition",
                    "decision_id",
                    view.disposition.get("decision_id")
                    if view.disposition is not None
                    else None,
                ),
                "occurrences": sorted(
                    bucket["occurrence"], key=lambda item: item["path"]
                ),
            }
        )
    body: dict[str, Any] = {
        "schema_version": 1,
        "created_at": created_at,
        "normalization_unit_ids": sorted(set(normalization_unit_ids)),
        "ingestion_receipts": ingestion,
        "issues": issues,
    }
    snapshot_id = f"fbs_{sha256_bytes(canonical_json_bytes(body))}"
    snapshot = {"state_snapshot_id": snapshot_id, **body}
    path = state_snapshot_root(repo) / f"{snapshot_id}.json"
    try:
        digest = write_immutable_json(path, snapshot)
    except Exception as exc:
        raise CmocError(
            "feedback state snapshot を durable に保存できません。",
            ["snapshot path と filesystem を確認してください。"],
            str(path),
        ) from exc
    _load_state_snapshot(repo, snapshot_id)
    return snapshot, digest


def _load_state_snapshot(repo: Path, snapshot_id: str) -> dict[str, Any]:
    """state snapshot の content ID と全 record 参照を検査して読む。"""
    if re.fullmatch(r"fbs_[0-9a-f]{64}", snapshot_id) is None:
        raise CmocError("feedback state snapshot ID が不正です。", [], snapshot_id)
    path = state_snapshot_root(repo) / f"{snapshot_id}.json"
    snapshot = _canonical_object(path, "feedback state snapshot")
    required = {
        "schema_version",
        "state_snapshot_id",
        "created_at",
        "normalization_unit_ids",
        "ingestion_receipts",
        "issues",
    }
    body = {key: value for key, value in snapshot.items() if key != "state_snapshot_id"}
    if (
        set(snapshot) != required
        or snapshot.get("schema_version") != 1
        or snapshot.get("state_snapshot_id") != snapshot_id
        or f"fbs_{sha256_bytes(canonical_json_bytes(body))}" != snapshot_id
        or not isinstance(snapshot.get("created_at"), str)
        or not _is_timestamp(snapshot["created_at"])
        or not isinstance(snapshot.get("normalization_unit_ids"), list)
        or not isinstance(snapshot.get("ingestion_receipts"), list)
        or not isinstance(snapshot.get("issues"), list)
    ):
        raise CmocError(
            "feedback state snapshot の schema または content ID が不正です。",
            ["snapshot を人間が確認してください。"],
            str(path),
        )
    unit_ids = snapshot["normalization_unit_ids"]
    if unit_ids != sorted(set(unit_ids)) or any(
        not isinstance(value, str) or re.fullmatch(r"fbu_[0-9a-f]{64}", value) is None
        for value in unit_ids
    ):
        raise CmocError(
            "feedback state snapshot の normalization unit ID が不正です。",
            ["snapshot を人間が確認してください。"],
            str(path),
        )
    root = feedback_root(repo)
    ingestion_paths = [
        str(reference.get("path"))
        for reference in snapshot["ingestion_receipts"]
        if isinstance(reference, dict)
    ]
    if ingestion_paths != sorted(ingestion_paths):
        raise CmocError(
            "feedback state snapshot の ingestion receipt 順が canonical ではありません。",
            [],
            str(path),
        )
    typed_references: list[tuple[object, str, str | None]] = [
        (reference, "ingestion", None) for reference in snapshot["ingestion_receipts"]
    ]
    seen_issues: set[str] = set()
    issue_ids = [
        str(issue.get("issue_id"))
        for issue in snapshot["issues"]
        if isinstance(issue, dict)
    ]
    if issue_ids != sorted(issue_ids):
        raise CmocError(
            "feedback state snapshot の issue 順が canonical ではありません。",
            [],
            str(path),
        )
    for issue in snapshot["issues"]:
        if (
            not isinstance(issue, dict)
            or set(issue)
            != {
                "issue_id",
                "identity",
                "effective_revision",
                "effective_assessment",
                "effective_disposition",
                "occurrences",
            }
            or re.fullmatch(r"fbi_[a-z2-7]{26}", str(issue.get("issue_id", ""))) is None
            or issue.get("identity") is None
            or issue.get("effective_revision") is None
        ):
            raise CmocError(
                "feedback state snapshot の issue が不正です。", [], str(path)
            )
        current_issue_id = str(issue["issue_id"])
        if current_issue_id in seen_issues:
            raise CmocError(
                "feedback state snapshot の issue ID が重複しています。",
                [],
                current_issue_id,
            )
        seen_issues.add(current_issue_id)
        for name in (
            "identity",
            "effective_revision",
            "effective_assessment",
            "effective_disposition",
        ):
            value = issue.get(name)
            if value is not None:
                kind = {
                    "identity": "identity",
                    "effective_revision": "revision",
                    "effective_assessment": "assessment",
                    "effective_disposition": "disposition",
                }[name]
                typed_references.append((value, kind, current_issue_id))
        occurrences = issue.get("occurrences")
        if not isinstance(occurrences, list):
            raise CmocError(
                "feedback state snapshot の occurrence が不正です。", [], str(path)
            )
        occurrence_paths = [
            str(reference.get("path"))
            for reference in occurrences
            if isinstance(reference, dict)
        ]
        if occurrence_paths != sorted(occurrence_paths):
            raise CmocError(
                "feedback state snapshot の occurrence 順が canonical ではありません。",
                [],
                str(path),
            )
        typed_references.extend(
            (reference, "occurrence", current_issue_id) for reference in occurrences
        )
    seen_paths: set[str] = set()
    for reference, expected_kind, expected_issue_id in typed_references:
        relative, record_path_value = _validate_reference(
            root, reference, description="state snapshot record"
        )
        if relative in seen_paths or _record_kind(relative) != expected_kind:
            raise CmocError(
                "feedback state snapshot の record 参照が重複または kind 不一致です。",
                ["snapshot manifest を人間が確認してください。"],
                relative,
            )
        seen_paths.add(relative)
        record = _canonical_object(record_path_value, "state snapshot record")
        _validate_effective_record(root, relative, record)
        if (
            expected_issue_id is not None
            and record.get("issue_id") != expected_issue_id
        ):
            raise CmocError(
                "feedback state snapshot の issue 参照が別 issue を指しています。",
                ["snapshot manifest を人間が確認してください。"],
                relative,
            )
    return snapshot


def load_issue_views_from_snapshot(
    repo: Path, snapshot_id: str
) -> dict[str, IssueView]:
    """immutable state snapshot が指す effective issue view を復元する。"""
    snapshot = _load_state_snapshot(repo, snapshot_id)
    root = feedback_root(repo)
    views: dict[str, IssueView] = {}
    for issue in snapshot["issues"]:
        assert isinstance(issue, dict)

        def read_reference(reference: object) -> dict[str, Any] | None:
            if reference is None:
                return None
            _relative, path = _validate_reference(
                root, reference, description="state snapshot record"
            )
            return _canonical_object(path, "state snapshot record")

        identity = read_reference(issue.get("identity"))
        revision = read_reference(issue.get("effective_revision"))
        if identity is None or revision is None:
            raise CmocError(
                "feedback state snapshot の issue 参照が欠落しています。",
                [],
                repr(issue),
            )
        occurrences = [
            read_reference(reference) for reference in issue.get("occurrences", [])
        ]
        occurrence_records = [record for record in occurrences if record is not None]
        assessment = read_reference(issue.get("effective_assessment"))
        disposition = read_reference(issue.get("effective_disposition"))
        current_issue_id = str(issue.get("issue_id"))
        views[current_issue_id] = IssueView(
            current_issue_id,
            identity,
            revision,
            occurrence_records,
            assessment,
            disposition,
            [revision],
            [assessment] if assessment is not None else [],
            [disposition] if disposition is not None else [],
        )
    return views


def _validate_report_record_v2(record: dict[str, Any], path_id: str) -> list[str]:
    """repository-local report publication record の schema を検査する。"""
    expected = {
        "schema_version",
        "report_id",
        "generated_at",
        "report_snapshot_sha256",
        "report_snapshot_observation_count",
        "processed_observation_count",
        "deferred_observation_count",
        "report_path",
        "report_sha256",
        "result",
        "normalization_unit_ids",
        "state_snapshot_id",
        "previous_successful_report_id",
    }
    errors = _field_set(record, expected)
    if record.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if record.get("report_id") != path_id or not is_uuid7_prefixed(
        record.get("report_id"), "fbr_"
    ):
        errors.append("report_id is invalid")
    if record.get("result") not in {
        "ok",
        "attention",
        "partial",
        "interrupted",
        "error",
    }:
        errors.append("result is invalid")
    for name in (
        "report_snapshot_observation_count",
        "processed_observation_count",
        "deferred_observation_count",
    ):
        value = record.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{name} is invalid")
    normalization_ids = record.get("normalization_unit_ids")
    if not _is_string_list(normalization_ids) or (
        isinstance(normalization_ids, list)
        and (
            len(normalization_ids) != len(set(normalization_ids))
            or any(
                re.fullmatch(r"fbu_[0-9a-f]{64}", value) is None
                for value in normalization_ids
            )
        )
    ):
        errors.append("normalization_unit_ids is invalid")
    for name in ("report_snapshot_sha256", "report_sha256"):
        if re.fullmatch(r"[0-9a-f]{64}", str(record.get(name, ""))) is None:
            errors.append(f"{name} is invalid")
    _require_timestamp(record, "generated_at", errors)
    report_path_value = record.get("report_path")
    if (
        not isinstance(report_path_value, str)
        or not Path(report_path_value).is_absolute()
    ):
        errors.append("report_path is invalid")
    snapshot_id = record.get("state_snapshot_id")
    if snapshot_id is None:
        if record.get("result") != "error":
            errors.append("state_snapshot_id is required")
    elif (
        not isinstance(snapshot_id, str)
        or re.fullmatch(r"fbs_[0-9a-f]{64}", snapshot_id) is None
    ):
        errors.append("state_snapshot_id is invalid")
    previous = record.get("previous_successful_report_id")
    if previous is not None and (
        not isinstance(previous, str) or not is_uuid7_prefixed(previous, "fbr_")
    ):
        errors.append("previous_successful_report_id is invalid")
    return errors


def _validate_report_artifacts(
    repo: Path,
    state: EffectiveFeedbackState,
    record: dict[str, Any],
    *,
    require_markdown: bool,
) -> None:
    """report record が参照する snapshot、state、Markdown を検査する。"""
    report_id = str(record["report_id"])
    report_snapshot_path = report_snapshot_root(repo) / f"{report_id}.json"
    report_snapshot = _canonical_object(
        report_snapshot_path, "feedback report snapshot"
    )
    if (
        set(report_snapshot)
        != {"schema_version", "report_id", "generated_at", "observations"}
        or report_snapshot.get("schema_version") != 1
        or report_snapshot.get("report_id") != report_id
        or report_snapshot.get("generated_at") != record["generated_at"]
        or not isinstance(report_snapshot.get("observations"), list)
        or sha256_bytes(report_snapshot_path.read_bytes())
        != record["report_snapshot_sha256"]
        or len(report_snapshot["observations"])
        != record["report_snapshot_observation_count"]
    ):
        raise CmocError(
            "feedback report snapshot が report record と一致しません。",
            ["report snapshot と publication record を確認してください。"],
            str(report_snapshot_path),
        )
    raw_root = observation_root(repo).resolve()
    seen_observations: set[str] = set()
    for entry in report_snapshot["observations"]:
        if (
            not isinstance(entry, dict)
            or set(entry) != {"path", "observation_id", "sha256"}
            or not is_observation_id(entry.get("observation_id"))
            or not isinstance(entry.get("path"), str)
            or not isinstance(entry.get("sha256"), str)
            or re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is None
        ):
            raise CmocError(
                "feedback report snapshot の observation 参照が不正です。",
                ["report snapshot を人間が確認してください。"],
                repr(entry),
            )
        raw_path = Path(entry["path"])
        try:
            resolved = raw_path.resolve(strict=True)
            if (
                raw_path.is_symlink()
                or not raw_path.is_file()
                or raw_root not in resolved.parents
                or raw_path.stem != entry["observation_id"]
                or sha256_bytes(raw_path.read_bytes()) != entry["sha256"]
            ):
                raise ValueError("raw observation path or hash differs")
        except (OSError, ValueError) as exc:
            raise CmocError(
                "feedback report snapshot の raw observation を検証できません。",
                ["raw observation store の corruption を確認してください。"],
                str(raw_path),
            ) from exc
        observation_id_value = str(entry["observation_id"])
        if observation_id_value in seen_observations:
            raise CmocError(
                "feedback report snapshot に重複 observation があります。",
                ["report snapshot を人間が確認してください。"],
                observation_id_value,
            )
        seen_observations.add(observation_id_value)

    snapshot_id = record.get("state_snapshot_id")
    if isinstance(snapshot_id, str):
        state_snapshot = _load_state_snapshot(repo, snapshot_id)
        unknown_snapshot_units = set(state_snapshot["normalization_unit_ids"]) - set(
            state.unit_manifests
        )
        if unknown_snapshot_units:
            raise CmocError(
                "feedback state snapshot が未確定 normalization unit を参照しています。",
                ["state snapshot と unit manifest を確認してください。"],
                repr(sorted(unknown_snapshot_units)),
            )
    unknown_units = set(record["normalization_unit_ids"]) - set(state.unit_manifests)
    if unknown_units:
        raise CmocError(
            "feedback report が未確定 normalization unit を参照しています。",
            ["report record と unit manifest を確認してください。"],
            repr(sorted(unknown_units)),
        )

    report_path_value = Path(str(record["report_path"]))
    expected_directory = (
        repo / ".cmoc" / "gu" / "ar" / "report" / "feedback"
    ).resolve()
    if report_path_value.parent.resolve() != expected_directory:
        raise CmocError(
            "feedback Markdown report path が保存領域外です。",
            ["report publication metadata を確認してください。"],
            str(report_path_value),
        )
    if not require_markdown:
        return
    if (
        report_path_value.is_symlink()
        or not report_path_value.is_file()
        or sha256_bytes(report_path_value.read_bytes()) != record["report_sha256"]
    ):
        raise CmocError(
            "feedback Markdown report が欠落または不一致です。",
            ["report artifact と publication metadata を確認してください。"],
            str(report_path_value),
        )


def _validated_report_records(
    repo: Path,
    state: EffectiveFeedbackState | None = None,
    *,
    permitted_atomic_report_id: str | None = None,
) -> dict[str, dict[str, Any]]:
    """publication artifact を含む全 report record を検査する。"""
    state = state or load_effective_feedback_state(repo)
    directory = feedback_root(repo) / "report"
    records: dict[str, dict[str, Any]] = {}
    if directory.exists() and (directory.is_symlink() or not directory.is_dir()):
        raise CmocError(
            "feedback report record root が通常 directory ではありません。",
            ["report record root を人間が確認してください。"],
            str(directory),
        )
    if not directory.is_dir():
        return records
    permitted_prefix = (
        f".{permitted_atomic_report_id}.json."
        if permitted_atomic_report_id is not None
        else None
    )
    unsupported = []
    for path in directory.iterdir():
        permitted_temporary = (
            permitted_prefix is not None
            and path.name.startswith(permitted_prefix)
            and path.name.endswith(".tmp")
            and not path.is_symlink()
            and path.is_file()
        )
        if not permitted_temporary and (
            path.is_symlink() or not path.is_file() or path.suffix != ".json"
        ):
            unsupported.append(path)
    if unsupported:
        raise CmocError(
            "feedback report record root に未定義 artifact があります。",
            ["report record root を人間が確認してください。"],
            "\n".join(str(path) for path in unsupported),
        )
    for path in sorted(directory.glob("*.json")):
        record = _canonical_object(path, "feedback report record")
        errors = _validate_report_record_v2(record, path.stem)
        if errors:
            raise CmocError(
                "feedback report record の schema が不正です。",
                ["publication record を人間が確認してください。"],
                f"{path}: {'; '.join(errors)}",
            )
        report_id = str(record["report_id"])
        _validate_report_artifacts(repo, state, record, require_markdown=True)
        records[report_id] = record
    try:
        _successful_report_head(state.migration_receipt, records)
    except ValueError as exc:
        raise CmocError(
            "正常な local feedback report の連鎖が不正です。",
            ["report record の predecessor を人間が確認してください。"],
            str(exc),
        ) from exc
    return records


def _expected_report_predecessor(
    receipt: dict[str, Any],
    records: dict[str, dict[str, Any]],
) -> str | None:
    """現在の正常 report 連鎖から次 publication の predecessor を返す。"""
    head = _successful_report_head(receipt, records)
    if head is not None:
        return str(head["report_id"])
    baseline = receipt.get("baseline")
    return str(baseline["legacy_report_id"]) if isinstance(baseline, dict) else None


def prepare_report_publication(repo: Path, record: dict[str, Any]) -> Path:
    """Markdown 保存前に publication metadata を durable recovery として固定する。"""
    state = load_effective_feedback_state(repo)
    report_id = str(record.get("report_id", ""))
    errors = _validate_report_record_v2(record, report_id)
    if errors:
        raise CmocError(
            "feedback report publication metadata の schema が不正です。",
            ["report 生成処理を確認してください。"],
            "; ".join(errors),
        )
    records = _validated_report_records(
        repo,
        state,
        permitted_atomic_report_id=report_id,
    )
    if report_id in records:
        if canonical_json_bytes(records[report_id]) != canonical_json_bytes(record):
            raise CmocError(
                "同じ report ID の publication record が異なります。",
                ["report record の corruption を確認してください。"],
                report_id,
            )
        return record_path(repo, record, "report")
    expected = _expected_report_predecessor(state.migration_receipt, records)
    if record.get("previous_successful_report_id") != expected:
        raise CmocError(
            "feedback report の predecessor が現在の正常連鎖と一致しません。",
            ["同じ repository の report publication を直列化してください。"],
            f"expected: {expected!r}\nactual: {record.get('previous_successful_report_id')!r}",
        )
    _validate_report_artifacts(repo, state, record, require_markdown=False)
    recovery_path = report_recovery_root(repo) / f"{report_id}.json"
    write_immutable_json(recovery_path, record)
    return recovery_path


def publish_report_record(repo: Path, record: dict[str, Any]) -> Path:
    """artifact 検証後に report record を最後の publication artifact として保存する。"""
    report_id = str(record.get("report_id", ""))
    recovery_path = report_recovery_root(repo) / f"{report_id}.json"
    prepare_report_publication(repo, record)
    publication_path = record_path(repo, record, "report")
    if publication_path.is_file() and not recovery_path.is_file():
        return publication_path
    recovery = _canonical_object(recovery_path, "feedback report recovery metadata")
    if canonical_json_bytes(recovery) != canonical_json_bytes(record):
        raise CmocError(
            "feedback report recovery metadata が publication 内容と異なります。",
            ["report recovery path を人間が確認してください。"],
            str(recovery_path),
        )
    report_path_value = Path(str(record["report_path"]))
    try:
        recover_immutable_bytes_from_temporary(
            report_path_value,
            str(record["report_sha256"]),
        )
    except Exception as exc:
        raise CmocError(
            "feedback Markdown report の temporary file を安全に回収できません。",
            ["一致しない report artifact を人間が確認してください。"],
            str(report_path_value),
        ) from exc
    state = load_effective_feedback_state(repo)
    _validate_report_artifacts(repo, state, record, require_markdown=True)
    write_feedback_record(publication_path, record)
    _validated_report_records(repo, state)
    _durable_unlink(recovery_path)
    return publication_path


def recover_report_publications(repo: Path) -> list[str]:
    """中断後に artifact が揃った report publication だけを確定する。"""
    recovered: list[str] = []
    root = report_recovery_root(repo)
    if root.exists() and (root.is_symlink() or not root.is_dir()):
        raise CmocError(
            "feedback report recovery root が通常 directory ではありません。",
            ["手動対応が必要な path を確認してください。"],
            str(root),
        )
    if not root.is_dir():
        return recovered
    unsupported = [
        path
        for path in root.iterdir()
        if path.is_symlink() or not path.is_file() or path.suffix != ".json"
    ]
    if unsupported:
        raise CmocError(
            "feedback report recovery root に未定義 artifact があります。",
            ["手動対応が必要な path を確認してください。"],
            "\n".join(str(path) for path in unsupported),
        )
    for path in sorted(root.glob("*.json")):
        record = _canonical_object(path, "feedback report recovery metadata")
        publication = publish_report_record(repo, record)
        recovered.append(publication.stem)
    return recovered


def _successful_report_head(
    receipt: dict[str, Any],
    records: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """predecessor 連鎖を検査し、正常 report の先頭を返す。"""
    normal = {
        report_id: record
        for report_id, record in records.items()
        if record.get("result") in {"ok", "attention"}
    }
    baseline = receipt.get("baseline")
    baseline_id = (
        baseline.get("legacy_report_id") if isinstance(baseline, dict) else None
    )
    for report_id, record in records.items():
        if report_id in normal:
            continue
        previous = record.get("previous_successful_report_id")
        if previous is not None and previous not in normal and previous != baseline_id:
            raise ValueError(
                f"report {report_id} has unknown successful predecessor {previous}"
            )
    if not normal:
        return None
    children: dict[str, list[str]] = {}
    referenced: set[str] = set()
    for report_id, record in normal.items():
        previous = record.get("previous_successful_report_id")
        if previous is not None:
            children.setdefault(str(previous), []).append(report_id)
            if previous in normal:
                referenced.add(str(previous))
            elif previous != baseline_id:
                raise ValueError(
                    f"normal report {report_id} has unknown predecessor {previous}"
                )
    forks = {key: value for key, value in children.items() if len(value) > 1}
    if forks:
        raise ValueError(f"normal report chain forks: {forks}")
    heads = set(normal) - referenced
    if len(heads) != 1:
        raise ValueError(f"normal report chain has {len(heads)} heads")
    head_id = heads.pop()
    visited: set[str] = set()
    cursor: str | None = head_id
    while cursor in normal:
        if cursor in visited:
            raise ValueError("normal report chain contains a cycle")
        visited.add(cursor)
        previous = normal[cursor].get("previous_successful_report_id")
        cursor = str(previous) if previous is not None else None
    if cursor != baseline_id:
        raise ValueError(
            f"normal report chain terminates at {cursor!r}, expected {baseline_id!r}"
        )
    if visited != set(normal):
        raise ValueError("normal report chain is disconnected")
    return normal[head_id]


def latest_successful_report_record(repo: Path) -> dict[str, Any] | None:
    """一意な predecessor 連鎖の先頭にある正常 report を返す。"""
    state = load_effective_feedback_state(repo)
    records = _validated_report_records(repo, state)
    return _successful_report_head(state.migration_receipt, records)


def previous_successful_report_id(repo: Path) -> str | None:
    """新しい report が記録する predecessor ID を返す。"""
    latest = latest_successful_report_record(repo)
    if latest is not None:
        return str(latest["report_id"])
    receipt = load_effective_feedback_state(repo).migration_receipt
    baseline = receipt.get("baseline")
    return str(baseline["legacy_report_id"]) if isinstance(baseline, dict) else None


def previous_state_snapshot_id(repo: Path) -> str | None:
    """直前の正常 report に対応する state snapshot ID を返す。"""
    latest = latest_successful_report_record(repo)
    if latest is not None:
        value = latest.get("state_snapshot_id")
        return str(value) if isinstance(value, str) else None
    receipt = load_effective_feedback_state(repo).migration_receipt
    baseline = receipt.get("baseline")
    return str(baseline["state_snapshot_id"]) if isinstance(baseline, dict) else None


def _effective_revision(
    records: list[dict[str, Any]],
    occurrences: list[dict[str, Any]],
) -> dict[str, Any]:
    """observation 最大時刻、次に revision ID で effective revision を選ぶ。"""
    observed_at_by_id = {
        str(record.get("observation_id", "")): str(record.get("observed_at", ""))
        for record in occurrences
    }

    def key(record: dict[str, Any]) -> tuple[datetime, str]:
        source_ids = record.get("source_observation_ids", [])
        observed_values = [
            observed_at_by_id.get(str(value), "") for value in source_ids
        ]
        return (
            max(
                (_timestamp_key(value) for value in observed_values),
                default=_timestamp_key(""),
            ),
            str(record.get("revision_id", "")),
        )

    return max(records, key=key)


def _timestamp_key(value: object) -> datetime:
    """record 選択用に RFC 3339 を UTC-aware datetime へ変換する。"""
    if isinstance(value, str):
        try:
            return parse_rfc3339(value).astimezone(timezone.utc)
        except ValueError:
            pass
    return datetime.min.replace(tzinfo=timezone.utc)


def load_issue_views(
    repo: Path,
    *,
    state: EffectiveFeedbackState | None = None,
) -> dict[str, IssueView]:
    """manifest/receipt が指す record だけから effective issue view を構築する。"""
    state = state or load_effective_feedback_state(repo)
    grouped: dict[str, dict[str, Any]] = {}
    for relative, record in state.records.items():
        parts = Path(relative).parts
        if len(parts) < 3 or parts[0] != "issue":
            continue
        bucket = grouped.setdefault(
            parts[1],
            {
                "identity": None,
                "revision": [],
                "occurrence": [],
                "assessment": [],
                "disposition": [],
            },
        )
        kind = "identity" if parts[2] == "identity.json" else parts[2]
        if kind == "identity":
            bucket[kind] = record
        else:
            bucket[kind].append(record)
    views: dict[str, IssueView] = {}
    for current_issue_id, bucket in sorted(grouped.items()):
        identity = bucket["identity"]
        revisions = bucket["revision"]
        if (
            not isinstance(identity, dict)
            or not isinstance(revisions, list)
            or not revisions
        ):
            continue
        occurrences = bucket["occurrence"]
        assessments = bucket["assessment"]
        dispositions = bucket["disposition"]
        assert isinstance(occurrences, list)
        assert isinstance(assessments, list)
        assert isinstance(dispositions, list)
        views[current_issue_id] = _build_issue_view(
            current_issue_id,
            identity,
            revisions,
            occurrences,
            assessments,
            dispositions,
        )
    return views


def _build_issue_view(
    current_issue_id: str,
    identity: dict[str, Any],
    revisions: list[dict[str, Any]],
    occurrences: list[dict[str, Any]],
    assessments: list[dict[str, Any]],
    dispositions: list[dict[str, Any]],
) -> IssueView:
    """一 issue の record 集合から effective view を構築する。"""
    assessment = (
        max(
            assessments,
            key=lambda record: (
                _timestamp_key(record.get("assessed_at")),
                str(record.get("assessment_id", "")),
            ),
        )
        if assessments
        else None
    )
    disposition = (
        max(
            dispositions,
            key=lambda record: (
                _timestamp_key(record.get("decided_at")),
                str(record.get("decision_id", "")),
            ),
        )
        if dispositions
        else None
    )
    return IssueView(
        current_issue_id,
        identity,
        _effective_revision(revisions, occurrences),
        occurrences,
        assessment,
        disposition,
        revisions,
        assessments,
        dispositions,
    )


def normalizer_version(agent_used: bool) -> str:
    """agent builder/schema または deterministic schema version の hash を返す。"""
    if not agent_used:
        return sha256_bytes(b"cmoc-feedback-schema-v1")
    from oracle.acp_builder.feedback import normalize_issue

    source_path = Path(normalize_issue.__file__)
    schema_path = source_path.with_suffix(".json")
    digest = hashlib.sha256()
    for path in sorted((source_path, schema_path), key=str):
        digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
    return digest.hexdigest()


def normalization_unit_id(
    observation_ids: list[str],
    candidate_revision_ids: list[str],
    normalizer_schema_sha256: str,
) -> str:
    """入力と候補と schema から再開可能な normalization unit ID を返す。"""
    body = {
        "observation_ids": sorted(observation_ids),
        "candidate_revision_ids": sorted(candidate_revision_ids),
        "normalizer_schema_sha256": normalizer_schema_sha256,
    }
    return f"fbu_{sha256_bytes(canonical_json_bytes(body))}"


def new_report_id() -> str:
    """feedback report 用 UUIDv7 ID を返す。"""
    return uuid7_prefixed("fbr_")
