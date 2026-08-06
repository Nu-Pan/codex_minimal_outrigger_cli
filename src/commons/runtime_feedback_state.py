"""feedback の append-only tracked normalized state を扱う。

この file は 16,000 文字を超えるが、record 構築、content-addressed ID、schema 検査、
record 間参照、および effective record 選択は、append-only state の同じ不変条件を
共有する。検査と読み取りを分けると、一方だけが新しい record field や選択規則へ
追従する危険があるため、tracked state model として一箇所に保つ。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/feedback_state.md`。
"""

import base64
import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .runtime_errors import CmocError
from .runtime_feedback_store import (
    canonical_json_bytes,
    is_observation_id,
    is_uuid7_prefixed,
    machine_observation_id,
    parse_rfc3339,
    read_json_object,
    reporter_input_schema,
    reporter_input_validation_errors,
    sha256_bytes,
    tracked_feedback_root,
    uuid7_prefixed,
)
from .runtime_git import run_git


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


def issue_directory(worktree: Path, current_issue_id: str) -> Path:
    """issue ごとの append-only record directory を返す。"""
    return tracked_feedback_root(worktree) / "issue" / current_issue_id


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
    snapshot_manifest_sha256: str,
    snapshot_observation_count: int,
    processed_observation_count: int,
    deferred_observation_count: int,
    report_path: Path,
    report_sha256: str,
    result: str,
    state_commit_ids: list[str],
) -> dict[str, Any]:
    """feedback report と処理 snapshot を結び付ける tracked record を返す。"""
    return {
        "schema_version": 1,
        "report_id": report_id,
        "generated_at": generated_at,
        "snapshot_manifest_sha256": snapshot_manifest_sha256,
        "snapshot_observation_count": snapshot_observation_count,
        "processed_observation_count": processed_observation_count,
        "deferred_observation_count": deferred_observation_count,
        "report_path": str(report_path.resolve()),
        "report_sha256": report_sha256,
        "result": result,
        "state_commit_ids": state_commit_ids,
    }


def record_path(worktree: Path, record: dict[str, Any], kind: str) -> Path:
    """record kind と ID から仕様上の tracked path を返す。"""
    root = tracked_feedback_root(worktree)
    current_issue_id = record.get("issue_id")
    if kind == "identity":
        assert isinstance(current_issue_id, str)
        return issue_directory(worktree, current_issue_id) / "identity.json"
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
            issue_directory(worktree, current_issue_id)
            / kind
            / (f"{record_id_value}.json")
        )
    return root / kind / f"{record_id_value}.json"


def write_tracked_record(path: Path, record: dict[str, Any]) -> bool:
    """append-only record を canonical form で作成し、既存差異を拒否する。"""
    content = canonical_json_bytes(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as output:
            output.write(content)
        return True
    except FileExistsError:
        if path.read_bytes() != content:
            raise CmocError(
                "feedback append-only record が既存内容と競合しています。",
                ["record path と branch merge 状態を人間が確認してください。"],
                str(path),
            )
        return False


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
    if observation.get("schema_version") != 1:
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
    if versions.get("observation_schema") != 1:
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
    if payload.get("rule_version") != 1:
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
    if source_event.get("event_schema_version") != 1:
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
    rule_contracts = {
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
    contract = rule_contracts.get(str(rule_id_value))
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
                if component not in {"reporter", "collector", "transport"}:
                    errors.append("/payload/event_fields/component: unsupported value")
                if failure_code not in {
                    "missing",
                    "version_mismatch",
                    "collector_unavailable",
                    "transport_unavailable",
                    "protocol_error",
                }:
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


def validate_tracked_feedback_state(worktree: Path) -> None:
    """既存 tracked state の JSON object と conflict marker を検査する。"""
    root = tracked_feedback_root(worktree)
    if not root.exists():
        return
    if root.is_symlink() or not root.is_dir():
        raise CmocError(
            "tracked feedback state root が通常 directory ではありません。",
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
            "tracked feedback state に未定義 file または symlink があります。",
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
                "tracked feedback state が不正です。",
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
    return [] if record.get("schema_version") == 1 else ["schema_version must be 1"]


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
            "tracked feedback state の record 関係が不正です。",
            ["欠落または不整合な append-only record を確認してください。"],
            "\n".join(errors),
        )


def _load_records(directory: Path) -> list[dict[str, Any]]:
    """directory 直下の JSON object record を path 順で読む。"""
    if not directory.is_dir():
        return []
    return [read_json_object(path) for path in sorted(directory.glob("*.json"))]


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


def load_issue_views(worktree: Path) -> dict[str, IssueView]:
    """tracked record 集合から effective issue view を構築する。"""
    issue_root = tracked_feedback_root(worktree) / "issue"
    if not issue_root.is_dir():
        return {}
    views: dict[str, IssueView] = {}
    for directory in sorted(path for path in issue_root.iterdir() if path.is_dir()):
        identity_path = directory / "identity.json"
        if not identity_path.is_file():
            continue
        identity = read_json_object(identity_path)
        revisions = _load_records(directory / "revision")
        if not revisions:
            continue
        occurrences = _load_records(directory / "occurrence")
        assessments = _load_records(directory / "assessment")
        dispositions = _load_records(directory / "disposition")
        current_issue_id = str(identity.get("issue_id", directory.name))
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


def load_issue_views_at_commit(
    worktree: Path,
    commit: str,
) -> dict[str, IssueView]:
    """指定 commit の tracked feedback tree から effective view を読む。"""
    prefix = ".cmoc/gt/ar/feedback/issue"
    listed = run_git(
        ["ls-tree", "-r", "--name-only", commit, "--", prefix],
        worktree,
    ).stdout.splitlines()
    grouped: dict[str, dict[str, Any]] = {}
    for relative in listed:
        parts = Path(relative).parts
        if len(parts) < 6 or parts[:5] != (".cmoc", "gt", "ar", "feedback", "issue"):
            continue
        current_issue_id = parts[5]
        bucket = grouped.setdefault(
            current_issue_id,
            {
                "identity": None,
                "revision": [],
                "occurrence": [],
                "assessment": [],
                "disposition": [],
            },
        )
        content = run_git(["show", f"{commit}:{relative}"], worktree).stdout
        record = json.loads(content)
        if not isinstance(record, dict):
            continue
        if len(parts) == 7 and parts[6] == "identity.json":
            bucket["identity"] = record
        elif len(parts) == 8 and parts[6] in {
            "revision",
            "occurrence",
            "assessment",
            "disposition",
        }:
            records = bucket[parts[6]]
            assert isinstance(records, list)
            records.append(record)
    views: dict[str, IssueView] = {}
    for current_issue_id, bucket in grouped.items():
        identity = bucket["identity"]
        revisions = bucket["revision"]
        occurrences = bucket["occurrence"]
        assessments = bucket["assessment"]
        dispositions = bucket["disposition"]
        if (
            not isinstance(identity, dict)
            or not isinstance(revisions, list)
            or not revisions
        ):
            continue
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
