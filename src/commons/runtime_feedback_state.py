"""feedback の repository-local active state と publication を扱う。

この module は report cut、active generation、current pointer、および cleanup の
相互参照を同じ integrity boundary で検証する。publication point を複数 module へ
分散させると、異常終了時に切替前後の state を混在させるため一箇所に保つ。

対応する oracle file:

- `{{work-root}}/oracle/doc/app_spec/feedback_observation.md`
- `{{work-root}}/oracle/doc/app_spec/feedback_state.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`
"""

import base64
import fcntl
import hashlib
import json
import os
import re
import secrets
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .runtime_errors import CmocError
from .runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    is_observation_id,
    is_uuid7_prefixed,
    machine_observation_id,
    parse_rfc3339,
    reporter_input_validation_errors,
    sha256_bytes,
    uuid7_prefixed,
    write_immutable_bytes,
    write_immutable_json,
)

JsonObject = dict[str, Any]

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


@dataclass(frozen=True)
class ActiveState:
    """current pointer から検証済み active generation をまとめる。"""

    current: JsonObject | None
    generation_manifest: JsonObject | None
    issues: dict[str, JsonObject]
    machine_aggregates: dict[str, JsonObject]
    cleanup_manifest: JsonObject | None
    cleanup_manifest_path: Path | None


def active_root(repo: Path) -> Path:
    """active generation と current pointer の root を返す。"""
    return feedback_root(repo) / "active"


def current_pointer_path(repo: Path) -> Path:
    """唯一の current pointer path を返す。"""
    return active_root(repo) / "current.json"


def generation_root(repo: Path) -> Path:
    """active generation artifact の root を返す。"""
    return active_root(repo) / "generation"


def generation_directory(repo: Path, generation_id: str) -> Path:
    """UUIDv7 generation ID に対応する directory を返す。"""
    if not is_uuid7_prefixed(generation_id, "fbg_"):
        raise ValueError(f"invalid feedback generation ID: {generation_id!r}")
    return generation_root(repo) / generation_id


def report_work_root(repo: Path) -> Path:
    """実行中または再開中の report cut root を返す。"""
    return feedback_root(repo) / "work"


def report_cut_directory(repo: Path, report_cut_id: str) -> Path:
    """UUIDv7 report cut ID に対応する一時 directory を返す。"""
    if not is_uuid7_prefixed(report_cut_id, "fbc_"):
        raise ValueError(f"invalid feedback report cut ID: {report_cut_id!r}")
    return report_work_root(repo) / report_cut_id


def report_cut_manifest_path(repo: Path, report_cut_id: str) -> Path:
    """report cut の mutable manifest path を返す。"""
    return report_cut_directory(repo, report_cut_id) / "manifest.json"


def normalization_checkpoint_path(
    repo: Path, report_cut_id: str, observation_id: str
) -> Path:
    """cut-scoped normalization checkpoint path を返す。"""
    if not is_observation_id(observation_id):
        raise ValueError(f"invalid observation ID: {observation_id!r}")
    return (
        report_cut_directory(repo, report_cut_id)
        / "checkpoint"
        / "normalization"
        / f"{observation_id}.json"
    )


def verification_checkpoint_path(
    repo: Path, report_cut_id: str, candidate_id: str
) -> Path:
    """cut-scoped verification checkpoint path を返す。"""
    if re.fullmatch(r"fbi_[a-z2-7]{26}", candidate_id) is None:
        raise ValueError(f"invalid feedback issue ID: {candidate_id!r}")
    return (
        report_cut_directory(repo, report_cut_id)
        / "checkpoint"
        / "verification"
        / f"{candidate_id}.json"
    )


def new_report_cut_id() -> str:
    """新しい report cut 用 UUIDv7 ID を返す。"""
    return uuid7_prefixed("fbc_")


def new_generation_id() -> str:
    """新しい active generation 用 UUIDv7 ID を返す。"""
    return uuid7_prefixed("fbg_")


def issue_id(canonical_key: str) -> str:
    """canonical issue key から安定した lowercase base32 ID を返す。"""
    digest = hashlib.sha256(canonical_key.encode("utf-8")).digest()
    encoded = base64.b32encode(digest).decode("ascii").lower().rstrip("=")
    return f"fbi_{encoded[:26]}"


def machine_aggregate_id(canonical_key: str) -> str:
    """machine canonical key から bounded aggregate ID を返す。"""
    digest = hashlib.sha256(canonical_key.encode("utf-8")).hexdigest()
    return f"fba_{digest}"


def machine_canonical_key(observation: JsonObject) -> str:
    """allowlist machine observation から canonical issue key を返す。"""
    payload = observation.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("machine observation payload must be an object")
    values = (
        payload.get("rule_id"),
        payload.get("subject_type"),
        payload.get("normalized_subject_id"),
    )
    if not all(isinstance(value, str) for value in values):
        raise ValueError("machine observation key fields must be strings")
    return "\0".join(str(value) for value in values)


def _is_machine_canonical_key(value: str, rule_id: str | None = None) -> bool:
    """allowlist rule の低カーディナリティ canonical key かを返す。"""
    parts = value.split("\0")
    if len(parts) != 3:
        return False
    key_rule_id, subject_type, normalized_subject_id = parts
    if rule_id is not None and key_rule_id != rule_id:
        return False
    contract = _MACHINE_RULE_CONTRACTS.get(key_rule_id)
    if contract is None or subject_type != contract[2] or not normalized_subject_id:
        return False
    if key_rule_id != "feedback.reporter_unavailable.v1":
        return True
    component, separator, failure_code = normalized_subject_id.partition(":")
    return (
        separator == ":"
        and component in _MACHINE_REPORTER_COMPONENTS
        and failure_code in _MACHINE_REPORTER_FAILURE_CODES
    )


def agent_canonical_key(observation_id: str) -> str:
    """新規 agent issue の最初の observation から canonical key を返す。"""
    if not is_observation_id(observation_id):
        raise ValueError(f"invalid observation ID: {observation_id!r}")
    return f"agent\0{observation_id}"


def validate_observation_envelope(
    observation: JsonObject,
    *,
    expected_repo_root: Path | None = None,
) -> list[str]:
    """raw observation の安定 envelope field を検査する。"""
    # トップレベルと共通 field を先に検査し、後続検査の型前提を固定する。
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

    # collector context と producer version を source 非依存で検査する。
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

    # source 固有 payload と raw evidence の対応を検査する。
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

    # 観測時点に解決済みの path は現在の symlink 状態で再解決しない。
    if isinstance(context, dict) and isinstance(fingerprints, list):
        repo_value = context.get("repo_root")
        if isinstance(repo_value, str) and Path(repo_value).is_absolute():
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
    """timezone を持つ RFC 3339 timestamp かを返す。"""
    try:
        parse_rfc3339(value)
        return True
    except ValueError:
        return False


def _is_version_one(value: object) -> bool:
    """JSON number の version 1 だけを受理する。"""
    return type(value) is int and value == 1


def _field_set(record: JsonObject, expected: set[str]) -> list[str]:
    """不足 field と追加 field を安定順で返す。"""
    errors = [f"{name}: missing" for name in sorted(expected - record.keys())]
    errors.extend(
        f"{name}: additional property" for name in sorted(record.keys() - expected)
    )
    return errors


def _is_string_list(value: object, *, non_empty: bool = False) -> bool:
    """重複のない string 配列かを返す。"""
    return (
        isinstance(value, list)
        and (not non_empty or bool(value))
        and all(isinstance(item, str) for item in value)
        and len(value) == len(set(value))
    )


def _validate_observation_context(context: JsonObject) -> list[str]:
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
    # path と必須 context は空文字を含め string 型として検査する。
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


def _validate_observation_versions(versions: JsonObject, source: object) -> list[str]:
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


def _validate_machine_observation(observation: JsonObject) -> list[str]:
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

    # ID、version、および source event の相互参照を検査する。
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

    # allowlist rule 固有の低カーディナリティ contract を検査する。
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
            errors.extend(
                _validate_machine_rule_fields(str(rule_id_value), payload, event_fields)
            )
    return errors


def _validate_machine_rule_fields(
    rule_id_value: str, payload: JsonObject, event_fields: JsonObject
) -> list[str]:
    """初期 allowlist の rule 固有 field を検査する。"""
    errors: list[str] = []
    if rule_id_value == "feedback.reporter_unavailable.v1":
        component = event_fields.get("component")
        failure_code = event_fields.get("failure_code")
        if component not in _MACHINE_REPORTER_COMPONENTS:
            errors.append("/payload/event_fields/component: unsupported value")
        if failure_code not in _MACHINE_REPORTER_FAILURE_CODES:
            errors.append("/payload/event_fields/failure_code: unsupported value")
        if payload.get("normalized_subject_id") != f"{component}:{failure_code}":
            errors.append("/payload/normalized_subject_id: does not match event")
        return errors

    agent_call_kind = event_fields.get("agent_call_kind")
    if not isinstance(agent_call_kind, str) or not agent_call_kind:
        errors.append("/payload/event_fields/agent_call_kind: expected string")
    if payload.get("normalized_subject_id") != agent_call_kind:
        errors.append("/payload/normalized_subject_id: does not match event")
    schema_sha = event_fields.get("schema_sha256")
    if not isinstance(schema_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", schema_sha):
        errors.append("/payload/event_fields/schema_sha256: expected SHA256")
    if event_fields.get("last_failure_stage") not in {
        "json_parse",
        "schema_validation",
        "deterministic_postcondition",
        "resume_unavailable",
        "artifact_changed",
    }:
        errors.append("/payload/event_fields/last_failure_stage: unsupported value")
    return errors


@contextmanager
def feedback_writer_lock(repo: Path) -> Iterator[None]:
    """repository ごとの feedback writer を非待機で排他する。"""
    # root までの symlink を拒否して、lock と state の所有 repository を一致させる。
    repository = repo.resolve(strict=False)
    root = feedback_root(repository)
    current = root
    while current != repository:
        if current.is_symlink():
            raise _corruption("feedback state root が symlink です。", current)
        current = current.parent
    lock_path = root / ".writer.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if lock_path.is_symlink() or (lock_path.exists() and not lock_path.is_file()):
        raise _corruption(
            "feedback writer lock path が通常 file ではありません。", lock_path
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


def _corruption(summary: str, path: Path, detail: str | None = None) -> CmocError:
    """feedback state corruption を一貫した利用者向け error にする。"""
    return CmocError(
        summary,
        ["repository-local feedback state を人間が確認してください。"],
        detail or str(path),
    )


def _has_symlink_component(path: Path) -> bool:
    """lexical path の既存 component に symlink があるかを返す。"""
    current = path.absolute()
    while current != current.parent:
        if current.is_symlink():
            return True
        current = current.parent
    return False


def _read_canonical_object(path: Path, description: str) -> JsonObject:
    """通常 file の canonical JSON object を読む。"""
    if _has_symlink_component(path) or not path.is_file():
        raise _corruption(f"{description} が通常 file ではありません。", path)
    try:
        content = path.read_bytes()
        value = json.loads(content)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _corruption(
            f"{description} を canonical JSON として読めません。", path
        ) from exc
    if not isinstance(value, dict) or canonical_json_bytes(value) != content:
        raise _corruption(
            f"{description} が canonical JSON object ではありません。", path
        )
    return value


def _atomic_write_json(path: Path, value: JsonObject) -> str:
    """mutable pointer／manifest を sibling temporary から durable に置換する。"""
    content = canonical_json_bytes(value)
    if _has_symlink_component(path):
        raise _corruption("feedback state path が symlink を含みます。", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise _corruption("feedback state path が通常 file ではありません。", path)
    temporary = path.parent / f".{path.name}.{secrets.token_hex(12)}.tmp"
    try:
        with temporary.open("xb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        _flush_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)
    return sha256_bytes(content)


def _flush_directory(directory: Path) -> None:
    """directory entry の変更を durable にする。"""
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _relative_path(repo: Path, path: Path) -> str:
    """repository 内 path を canonical POSIX relative path にする。"""
    repository = repo.resolve(strict=False)
    candidate = path.resolve(strict=False)
    try:
        return candidate.relative_to(repository).as_posix()
    except ValueError as exc:
        raise _corruption(
            "feedback state の参照 path が repository 外です。", path
        ) from exc


def _resolve_reference_path(
    repo: Path, raw_path: object, expected_root: Path, description: str
) -> Path:
    """state 内の repository-relative path を期待 root 内へ解決する。"""
    if not isinstance(raw_path, str) or not raw_path or Path(raw_path).is_absolute():
        raise _corruption(
            f"{description} path が不正です。", expected_root, repr(raw_path)
        )
    repository = repo.resolve(strict=False)
    candidate = (repository / raw_path).resolve(strict=False)
    expected = expected_root.resolve(strict=False)
    if candidate != expected and expected not in candidate.parents:
        raise _corruption(f"{description} path が期待 root 外です。", candidate)
    return candidate


def artifact_reference(repo: Path, path: Path) -> JsonObject:
    """存在する通常 file の path と SHA256 reference を返す。"""
    if _has_symlink_component(path) or not path.is_file():
        raise _corruption("feedback artifact が通常 file ではありません。", path)
    return {
        "path": _relative_path(repo, path),
        "sha256": sha256_bytes(path.read_bytes()),
    }


def _validate_artifact_reference(
    repo: Path,
    reference: object,
    *,
    expected_root: Path,
    description: str,
) -> Path:
    """artifact reference の field、path、および hash を検証する。"""
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
        raise _corruption(f"{description} reference が不正です。", expected_root)
    path = _resolve_reference_path(
        repo, reference.get("path"), expected_root, description
    )
    digest = reference.get("sha256")
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise _corruption(f"{description} SHA256 が不正です。", path)
    if _has_symlink_component(path) or not path.is_file():
        raise _corruption(f"{description} が存在する通常 file ではありません。", path)
    if sha256_bytes(path.read_bytes()) != digest:
        raise _corruption(f"{description} の SHA256 が一致しません。", path)
    return path


def _require_exact_fields(
    value: object, fields: set[str], path: Path, description: str
) -> JsonObject:
    """永続 object が exact field set を持つことを要求する。"""
    if not isinstance(value, dict) or set(value) != fields:
        raise _corruption(
            f"{description} の field set が不正です。",
            path,
            f"expected: {sorted(fields)!r}\nobserved: {sorted(value) if isinstance(value, dict) else type(value).__name__}",
        )
    return value


def _require_timestamp(value: object, path: Path, description: str) -> str:
    """timezone-aware RFC 3339 timestamp を要求する。"""
    if not isinstance(value, str) or not _is_timestamp(value):
        raise _corruption(f"{description} timestamp が不正です。", path, repr(value))
    return value


def _require_nonnegative_integer(value: object, path: Path, description: str) -> int:
    """bool ではない非負 integer を要求する。"""
    if type(value) is not int or value < 0:
        raise _corruption(
            f"{description} が非負 integer ではありません。", path, repr(value)
        )
    return value


def _validate_active_issue(record: JsonObject, path: Path) -> None:
    """compact active issue record の schema と identity を検査する。"""
    _require_exact_fields(
        record,
        {
            "schema_version",
            "issue_id",
            "origin",
            "canonical_key",
            "category",
            "summary",
            "impact",
            "occurrence_count",
            "affected_session_count",
            "session_digest",
            "first_observed_at",
            "last_observed_at",
            "representative_evidence",
            "reference_targets",
            "latest_fingerprints",
            "verification",
            "machine_state",
        },
        path,
        "active issue record",
    )
    if not _is_version_one(record.get("schema_version")):
        raise _corruption("active issue schema version が不正です。", path)
    current_issue_id = record.get("issue_id")
    canonical_key = record.get("canonical_key")
    if (
        not isinstance(current_issue_id, str)
        or not isinstance(canonical_key, str)
        or issue_id(canonical_key) != current_issue_id
        or path.stem != current_issue_id
    ):
        raise _corruption(
            "active issue identity が canonical key と一致しません。", path
        )
    if record.get("origin") not in {"agent_report", "machine_rule"}:
        raise _corruption("active issue origin が不正です。", path)
    if record.get("origin") == "agent_report" and (
        not canonical_key.startswith("agent\0")
        or not is_observation_id(canonical_key.removeprefix("agent\0"))
    ):
        raise _corruption("agent active issue canonical key が不正です。", path)
    if record.get("origin") == "machine_rule" and not _is_machine_canonical_key(
        canonical_key
    ):
        raise _corruption("machine active issue canonical key が不正です。", path)
    for name in ("category", "summary", "impact"):
        if not isinstance(record.get(name), str) or not record[name]:
            raise _corruption(
                f"active issue {name} が空でない string ではありません。", path
            )
    occurrence_count = _require_nonnegative_integer(
        record.get("occurrence_count"), path, "active issue occurrence_count"
    )
    if occurrence_count < 1:
        raise _corruption(
            "active issue occurrence_count は 1 以上である必要があります。", path
        )
    affected_session_count = _require_nonnegative_integer(
        record.get("affected_session_count"),
        path,
        "active issue affected_session_count",
    )
    if affected_session_count > occurrence_count:
        raise _corruption(
            "active issue affected session 数が occurrence 数を超えています。", path
        )
    first = _require_timestamp(
        record.get("first_observed_at"), path, "first_observed_at"
    )
    last = _require_timestamp(record.get("last_observed_at"), path, "last_observed_at")
    if parse_rfc3339(first) > parse_rfc3339(last):
        raise _corruption("active issue の観測時刻順が逆転しています。", path)

    # bounded field は schema-fixed 上限と型を state 読み取り時に確認する。
    for name in ("representative_evidence", "reference_targets", "latest_fingerprints"):
        value = record.get(name)
        if (
            not isinstance(value, list)
            or len(value) > 5
            or not all(isinstance(item, dict) for item in value)
        ):
            raise _corruption(
                f"active issue {name} が bounded object array ではありません。", path
            )
    reference_targets = record["reference_targets"]
    assert isinstance(reference_targets, list)
    for target in reference_targets:
        assert isinstance(target, dict)
        target_path = target.get("path")
        if (
            set(target) != {"path", "kind", "location"}
            or not isinstance(target_path, str)
            or not target_path
            or Path(target_path).is_absolute()
            or ".." in Path(target_path).parts
        ):
            raise _corruption("active issue reference target が不正です。", path)
    latest_fingerprints = record["latest_fingerprints"]
    assert isinstance(latest_fingerprints, list)
    fingerprint_errors = [
        error
        for index, fingerprint in enumerate(latest_fingerprints)
        for error in _validate_evidence_fingerprint(fingerprint, index)
    ]
    if fingerprint_errors:
        raise _corruption(
            "active issue fingerprint が不正です。",
            path,
            "\n".join(fingerprint_errors),
        )
    session_digest = _require_exact_fields(
        record.get("session_digest"), {"values", "saturated"}, path, "session digest"
    )
    values = session_digest.get("values")
    if (
        not isinstance(values, list)
        or not _is_string_list(values)
        or not isinstance(session_digest.get("saturated"), bool)
        or len(values) > 64
        or values != sorted(set(values))
        or not all(re.fullmatch(r"[0-9a-f]{64}", value) for value in values)
    ):
        raise _corruption("active issue session digest が不正です。", path)
    saturated = session_digest["saturated"]
    if (not saturated and affected_session_count != len(values)) or (
        saturated and affected_session_count < len(values)
    ):
        raise _corruption("active issue session count と digest が一致しません。", path)
    verification = _require_exact_fields(
        record.get("verification"),
        {"report_cut_id", "verified_at", "reason", "current_evidence", "human_action"},
        path,
        "active issue verification",
    )
    if not is_uuid7_prefixed(verification.get("report_cut_id"), "fbc_"):
        raise _corruption(
            "active issue verification の report cut ID が不正です。", path
        )
    _require_timestamp(
        verification.get("verified_at"), path, "verification verified_at"
    )
    if not isinstance(verification.get("reason"), str) or not verification["reason"]:
        raise _corruption("active issue verification reason が空です。", path)
    evidence = verification.get("current_evidence")
    if (
        not isinstance(evidence, list)
        or not evidence
        or len(evidence) > 5
        or not all(isinstance(item, dict) for item in evidence)
    ):
        raise _corruption("active issue current evidence が不正です。", path)
    for item in evidence:
        assert isinstance(item, dict)
        required = {"kind", "location", "finding"}
        allowed = required | {
            "path",
            "state",
            "sha256",
            "probe_id",
            "observation_id",
            "summary",
        }
        if (
            not required.issubset(item)
            or not set(item).issubset(allowed)
            or not all(isinstance(item[name], str) and item[name] for name in required)
            or "reference_id" in item
            or "content" in item
        ):
            raise _corruption("active issue current evidence entry が不正です。", path)
    if (
        not isinstance(verification.get("human_action"), str)
        or not verification["human_action"]
    ):
        raise _corruption("active issue human action が空です。", path)
    machine_state = record.get("machine_state")
    if record.get("origin") == "machine_rule":
        if machine_state is None:
            return
        if not isinstance(machine_state, dict):
            raise _corruption(
                "machine active issue の machine_state が不正です。", path
            )
        aggregate_id_value = machine_state.get("aggregate_id")
        if not isinstance(aggregate_id_value, str):
            raise _corruption("machine active issue aggregate ID が不正です。", path)
        aggregate_path = (
            path.parent.parent / "machine_aggregate" / f"{aggregate_id_value}.json"
        )
        _validate_machine_aggregate(machine_state, aggregate_path)
        if machine_state.get("canonical_key") != canonical_key:
            raise _corruption(
                "machine active issue aggregate identity が一致しません。", path
            )
    if record.get("origin") == "agent_report" and machine_state is not None:
        raise _corruption(
            "agent active issue の machine_state は null である必要があります。", path
        )


def _validate_machine_aggregate(record: JsonObject, path: Path) -> None:
    """threshold 未満 machine aggregate の compact schema を検査する。"""
    _require_exact_fields(
        record,
        {
            "schema_version",
            "aggregate_id",
            "rule_id",
            "canonical_key",
            "category",
            "summary",
            "impact",
            "human_action",
            "window_start",
            "window_end",
            "occurrence_count",
            "affected_session_count",
            "threshold_counts",
            "time_buckets",
            "scope_digest",
            "agent_call_digest",
            "scope_saturated",
            "agent_call_saturated",
            "first_observed_at",
            "last_observed_at",
            "representative_evidence",
            "latest_fingerprints",
        },
        path,
        "machine aggregate record",
    )
    if not _is_version_one(record.get("schema_version")):
        raise _corruption("machine aggregate schema version が不正です。", path)
    canonical_key = record.get("canonical_key")
    aggregate_id_value = record.get("aggregate_id")
    rule_id_value = record.get("rule_id")
    if (
        not isinstance(canonical_key, str)
        or machine_aggregate_id(canonical_key) != aggregate_id_value
        or path.stem != aggregate_id_value
        or not isinstance(rule_id_value, str)
        or not _is_machine_canonical_key(canonical_key, rule_id_value)
    ):
        raise _corruption(
            "machine aggregate identity が canonical key と一致しません。", path
        )
    if rule_id_value not in _MACHINE_RULE_CONTRACTS:
        raise _corruption("machine aggregate rule が allowlist 外です。", path)
    if record.get("category") != _MACHINE_RULE_CONTRACTS[rule_id_value][1]:
        raise _corruption("machine aggregate category が rule と一致しません。", path)
    for name in ("category", "summary", "impact", "human_action"):
        if not isinstance(record.get(name), str) or not record[name]:
            raise _corruption(f"machine aggregate {name} が空です。", path)
    window_start = _require_timestamp(
        record.get("window_start"), path, "machine aggregate window_start"
    )
    window_end = _require_timestamp(
        record.get("window_end"), path, "machine aggregate window_end"
    )
    first = _require_timestamp(
        record.get("first_observed_at"), path, "machine aggregate first_observed_at"
    )
    last = _require_timestamp(
        record.get("last_observed_at"), path, "machine aggregate last_observed_at"
    )
    if parse_rfc3339(window_start) >= parse_rfc3339(window_end) or parse_rfc3339(
        first
    ) > parse_rfc3339(last):
        raise _corruption("machine aggregate の時刻順が不正です。", path)
    occurrence_count = _require_nonnegative_integer(
        record.get("occurrence_count"), path, "machine aggregate occurrence_count"
    )
    affected_session_count = _require_nonnegative_integer(
        record.get("affected_session_count"),
        path,
        "machine aggregate affected_session_count",
    )
    if occurrence_count < 1 or affected_session_count > occurrence_count:
        raise _corruption("machine aggregate count が不正です。", path)
    threshold_counts = _require_exact_fields(
        record.get("threshold_counts"),
        {"recurrence_scope", "agent_call"},
        path,
        "machine aggregate threshold counts",
    )
    for name in ("recurrence_scope", "agent_call"):
        count = _require_nonnegative_integer(
            threshold_counts.get(name), path, f"machine aggregate {name} count"
        )
        if count > 64:
            raise _corruption(
                "machine aggregate threshold count が上限を超えています。", path
            )
    for name in ("time_buckets", "scope_digest", "agent_call_digest"):
        value = record.get(name)
        if not isinstance(value, list) or len(value) > 64:
            raise _corruption(
                f"machine aggregate {name} が bounded array ではありません。", path
            )
    if not isinstance(record.get("scope_saturated"), bool) or not isinstance(
        record.get("agent_call_saturated"), bool
    ):
        raise _corruption("machine aggregate saturation marker が不正です。", path)
    for name in ("scope_digest", "agent_call_digest"):
        digest = record[name]
        assert isinstance(digest, list)
        digest_values: list[str] = []
        for item in digest:
            entry = _require_exact_fields(
                item,
                {"value", "last_observed_at"},
                path,
                f"machine aggregate {name} entry",
            )
            digest_value = entry.get("value")
            if (
                not isinstance(digest_value, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest_value) is None
            ):
                raise _corruption(f"machine aggregate {name} value が不正です。", path)
            _require_timestamp(
                entry.get("last_observed_at"),
                path,
                f"machine aggregate {name} timestamp",
            )
            digest_values.append(digest_value)
        if digest_values != sorted(set(digest_values)):
            raise _corruption(
                f"machine aggregate {name} が一意な辞書順ではありません。", path
            )
    if threshold_counts["recurrence_scope"] != len(
        record["scope_digest"]
    ) or threshold_counts["agent_call"] != len(record["agent_call_digest"]):
        raise _corruption(
            "machine aggregate threshold count と digest が一致しません。", path
        )
    buckets = record["time_buckets"]
    assert isinstance(buckets, list)
    bucket_days: list[str] = []
    bucket_occurrence_count = 0
    for item in buckets:
        bucket = _require_exact_fields(
            item,
            {
                "day",
                "count",
                "first_observed_at",
                "last_observed_at",
                "scope_digest",
                "agent_call_digest",
                "scope_saturated",
                "agent_call_saturated",
            },
            path,
            "machine aggregate time bucket",
        )
        day = bucket.get("day")
        count = _require_nonnegative_integer(
            bucket.get("count"), path, "machine aggregate bucket count"
        )
        bucket_first = _require_timestamp(
            bucket.get("first_observed_at"), path, "machine aggregate bucket first"
        )
        bucket_last = _require_timestamp(
            bucket.get("last_observed_at"), path, "machine aggregate bucket last"
        )
        if (
            not isinstance(day, str)
            or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day) is None
            or count < 1
            or parse_rfc3339(bucket_first) > parse_rfc3339(bucket_last)
        ):
            raise _corruption("machine aggregate time bucket が不正です。", path)
        for digest_name in ("scope_digest", "agent_call_digest"):
            digest = bucket.get(digest_name)
            saturation_name = digest_name.replace("_digest", "_saturated")
            if (
                not isinstance(digest, list)
                or len(digest) > 64
                or not isinstance(bucket.get(saturation_name), bool)
            ):
                raise _corruption("machine aggregate bucket digest が不正です。", path)
            bucket_digest_values: list[str] = []
            for digest_item in digest:
                entry = _require_exact_fields(
                    digest_item,
                    {"value", "last_observed_at"},
                    path,
                    "machine aggregate bucket digest entry",
                )
                digest_value = entry.get("value")
                if (
                    not isinstance(digest_value, str)
                    or re.fullmatch(r"[0-9a-f]{64}", digest_value) is None
                ):
                    raise _corruption(
                        "machine aggregate bucket digest value が不正です。", path
                    )
                _require_timestamp(
                    entry.get("last_observed_at"),
                    path,
                    "machine aggregate bucket digest timestamp",
                )
                bucket_digest_values.append(digest_value)
            if bucket_digest_values != sorted(set(bucket_digest_values)):
                raise _corruption(
                    "machine aggregate bucket digest が canonical ではありません。",
                    path,
                )
        bucket_days.append(day)
        bucket_occurrence_count += count
    if (
        bucket_days != sorted(set(bucket_days))
        or bucket_occurrence_count != occurrence_count
    ):
        raise _corruption("machine aggregate bucket 集計が一致しません。", path)
    for name in ("representative_evidence", "latest_fingerprints"):
        if (
            not isinstance(record.get(name), list)
            or len(record[name]) > 5
            or not all(isinstance(item, dict) for item in record[name])
        ):
            raise _corruption(
                f"machine aggregate {name} が bounded array ではありません。", path
            )


def _machine_aggregate_reaches_threshold(record: JsonObject) -> bool:
    """allowlist rule の threshold を compact count から決定論的に判定する。"""
    counts = record.get("threshold_counts")
    if not isinstance(counts, dict):
        return False
    recurrence_scope = counts.get("recurrence_scope")
    agent_call = counts.get("agent_call")
    if record.get("rule_id") == "feedback.reporter_unavailable.v1":
        return type(recurrence_scope) is int and recurrence_scope >= 2
    if record.get("rule_id") == "codex.structured_output_validation_exhausted.v1":
        return (
            type(recurrence_scope) is int
            and recurrence_scope >= 2
            and type(agent_call) is int
            and agent_call >= 2
        )
    return False


def _load_generation(
    repo: Path, manifest_path: Path, expected_generation_id: str | None = None
) -> tuple[JsonObject, dict[str, JsonObject], dict[str, JsonObject]]:
    """generation manifest と列挙 record を hash 付きで読み込む。"""
    manifest = _read_canonical_object(manifest_path, "active generation manifest")
    _require_exact_fields(
        manifest,
        {
            "schema_version",
            "generation_id",
            "report_cut_id",
            "created_at",
            "issues",
            "machine_aggregates",
        },
        manifest_path,
        "active generation manifest",
    )
    generation_id_value = manifest.get("generation_id")
    if (
        not _is_version_one(manifest.get("schema_version"))
        or not is_uuid7_prefixed(generation_id_value, "fbg_")
        or (
            expected_generation_id is not None
            and generation_id_value != expected_generation_id
        )
        or manifest_path.parent.name != generation_id_value
    ):
        raise _corruption(
            "active generation manifest identity が不正です。", manifest_path
        )
    if not is_uuid7_prefixed(manifest.get("report_cut_id"), "fbc_"):
        raise _corruption(
            "active generation の report cut ID が不正です。", manifest_path
        )
    _require_timestamp(
        manifest.get("created_at"), manifest_path, "active generation created_at"
    )
    issue_refs = manifest.get("issues")
    aggregate_refs = manifest.get("machine_aggregates")
    if not isinstance(issue_refs, list) or not isinstance(aggregate_refs, list):
        raise _corruption(
            "active generation record references が array ではありません。",
            manifest_path,
        )

    # manifest の canonical order と各 record の identity/hash を検証する。
    issues: dict[str, JsonObject] = {}
    issue_keys: list[str] = []
    expected_issue_root = manifest_path.parent / "issue"
    for reference in issue_refs:
        item = _require_exact_fields(
            reference,
            {"issue_id", "path", "sha256"},
            manifest_path,
            "active issue reference",
        )
        current_issue_id = item.get("issue_id")
        if not isinstance(current_issue_id, str):
            raise _corruption(
                "active issue reference ID が string ではありません。", manifest_path
            )
        path = _validate_artifact_reference(
            repo,
            {"path": item.get("path"), "sha256": item.get("sha256")},
            expected_root=expected_issue_root,
            description="active issue",
        )
        record = _read_canonical_object(path, "active issue record")
        _validate_active_issue(record, path)
        if record.get("issue_id") != current_issue_id or current_issue_id in issues:
            raise _corruption("active issue reference identity が一致しません。", path)
        issues[current_issue_id] = record
        issue_keys.append(current_issue_id)
    if issue_keys != sorted(issue_keys):
        raise _corruption(
            "active issue references が issue ID 順ではありません。", manifest_path
        )

    aggregates: dict[str, JsonObject] = {}
    aggregate_keys: list[str] = []
    expected_aggregate_root = manifest_path.parent / "machine_aggregate"
    for reference in aggregate_refs:
        item = _require_exact_fields(
            reference,
            {"canonical_key", "path", "sha256"},
            manifest_path,
            "machine aggregate reference",
        )
        canonical_key = item.get("canonical_key")
        if not isinstance(canonical_key, str):
            raise _corruption(
                "machine aggregate canonical key が string ではありません。",
                manifest_path,
            )
        path = _validate_artifact_reference(
            repo,
            {"path": item.get("path"), "sha256": item.get("sha256")},
            expected_root=expected_aggregate_root,
            description="machine aggregate",
        )
        record = _read_canonical_object(path, "machine aggregate record")
        _validate_machine_aggregate(record, path)
        if _machine_aggregate_reaches_threshold(record):
            raise _corruption(
                "threshold 到達済み machine aggregate が active aggregate に残っています。",
                path,
            )
        if record.get("canonical_key") != canonical_key or canonical_key in aggregates:
            raise _corruption(
                "machine aggregate reference identity が一致しません。", path
            )
        aggregates[canonical_key] = record
        aggregate_keys.append(canonical_key)
    if aggregate_keys != sorted(aggregate_keys):
        raise _corruption(
            "machine aggregate references が canonical key 順ではありません。",
            manifest_path,
        )
    return manifest, issues, aggregates


def load_active_state(repo: Path) -> ActiveState:
    """current pointer が選ぶ正常な active state と cleanup state を読む。"""
    pointer_path = current_pointer_path(repo)
    if not pointer_path.exists() and not pointer_path.is_symlink():
        return ActiveState(None, None, {}, {}, None, None)
    pointer = _read_canonical_object(pointer_path, "feedback current pointer")
    _require_exact_fields(
        pointer,
        {
            "schema_version",
            "generation_id",
            "generation_manifest_path",
            "generation_manifest_sha256",
            "report_cut_id",
            "report_cut_manifest_sha256",
            "report_path",
            "report_sha256",
            "published_at",
            "result",
        },
        pointer_path,
        "feedback current pointer",
    )
    if not _is_version_one(pointer.get("schema_version")):
        raise _corruption(
            "feedback current pointer schema version が不正です。", pointer_path
        )
    generation_id_value = pointer.get("generation_id")
    report_cut_id_value = pointer.get("report_cut_id")
    if not is_uuid7_prefixed(generation_id_value, "fbg_") or not is_uuid7_prefixed(
        report_cut_id_value, "fbc_"
    ):
        raise _corruption("feedback current pointer の ID が不正です。", pointer_path)
    if pointer.get("result") not in {"ok", "attention"}:
        raise _corruption("feedback current pointer result が不正です。", pointer_path)
    report_cut_manifest_hash = pointer.get("report_cut_manifest_sha256")
    if (
        not isinstance(report_cut_manifest_hash, str)
        or re.fullmatch(r"[0-9a-f]{64}", report_cut_manifest_hash) is None
    ):
        raise _corruption(
            "feedback current pointer の report cut hash が不正です。", pointer_path
        )
    _require_timestamp(
        pointer.get("published_at"), pointer_path, "feedback publication"
    )

    # pointer が参照する generation と Markdown report を両方検証する。
    generation_path = _validate_artifact_reference(
        repo,
        {
            "path": pointer.get("generation_manifest_path"),
            "sha256": pointer.get("generation_manifest_sha256"),
        },
        expected_root=generation_directory(repo, str(generation_id_value)),
        description="current generation manifest",
    )
    generation_manifest, issues, aggregates = _load_generation(
        repo, generation_path, str(generation_id_value)
    )
    if generation_manifest.get("report_cut_id") != report_cut_id_value:
        raise _corruption(
            "current generation と report cut が一致しません。", generation_path
        )
    _validate_artifact_reference(
        repo,
        {"path": pointer.get("report_path"), "sha256": pointer.get("report_sha256")},
        expected_root=repo / ".cmoc" / "gu" / "ar" / "report" / "feedback",
        description="current feedback Markdown report",
    )

    # cleanup manifest は切替後に残っている場合だけ hash 一致を要求する。
    cut_path = report_cut_manifest_path(repo, str(report_cut_id_value))
    cleanup_manifest: JsonObject | None = None
    cleanup_path: Path | None = None
    if cut_path.exists() or cut_path.is_symlink():
        cleanup_manifest = _read_canonical_object(
            cut_path, "published report cut manifest"
        )
        if sha256_bytes(cut_path.read_bytes()) != pointer.get(
            "report_cut_manifest_sha256"
        ):
            raise _corruption(
                "published report cut manifest hash が current pointer と一致しません。",
                cut_path,
            )
        _validate_report_cut_manifest(
            repo,
            cleanup_manifest,
            cut_path,
            allow_missing_cleanup_targets=True,
        )
        if cleanup_manifest.get("report_cut_id") != report_cut_id_value:
            raise _corruption(
                "published report cut ID が current pointer と一致しません。", cut_path
            )
        processing = cleanup_manifest.get("processing")
        if (
            not isinstance(processing, dict)
            or processing.get("status") != "publication_ready"
        ):
            raise _corruption(
                "current pointer が未 publication の report cut を参照しています。",
                cut_path,
            )
        cleanup_path = cut_path
    return ActiveState(
        pointer, generation_manifest, issues, aggregates, cleanup_manifest, cleanup_path
    )


def _validate_report_cut_manifest(
    repo: Path,
    manifest: JsonObject,
    path: Path,
    *,
    allow_missing_cleanup_targets: bool = False,
) -> None:
    """report cut manifest の固定入力と mutable section の schema を検査する。"""
    _require_exact_fields(
        manifest,
        {
            "schema_version",
            "report_cut_id",
            "cut_at",
            "inputs",
            "processing",
            "publication",
        },
        path,
        "report cut manifest",
    )
    report_cut_id_value = manifest.get("report_cut_id")
    if (
        not _is_version_one(manifest.get("schema_version"))
        or not is_uuid7_prefixed(report_cut_id_value, "fbc_")
        or path.parent.name != report_cut_id_value
    ):
        raise _corruption("report cut manifest identity が不正です。", path)
    _require_timestamp(manifest.get("cut_at"), path, "report cut")
    inputs = _require_exact_fields(
        manifest.get("inputs"),
        {"observations", "current", "references", "versions"},
        path,
        "report cut inputs",
    )
    observations = inputs.get("observations")
    if not isinstance(observations, list):
        raise _corruption("report cut observations が array ではありません。", path)
    observed_entries: list[tuple[str, str, str]] = []
    hashes_by_id: dict[str, str] = {}
    for entry in observations:
        item = _require_exact_fields(
            entry, {"observation_id", "path", "sha256"}, path, "report cut observation"
        )
        observation_id_value = item.get("observation_id")
        if not is_observation_id(observation_id_value):
            raise _corruption("report cut observation ID が不正です。", path)
        _validate_report_cut_artifact_reference(
            repo,
            {"path": item.get("path"), "sha256": item.get("sha256")},
            expected_root=feedback_root(repo) / "observation" / "v1",
            description="pending observation",
            allow_missing=allow_missing_cleanup_targets,
        )
        observation_path_value = str(item.get("path"))
        observation_hash = str(item.get("sha256"))
        previous_hash = hashes_by_id.setdefault(
            str(observation_id_value), observation_hash
        )
        if previous_hash != observation_hash:
            raise _corruption("同じ observation ID に異なる hash があります。", path)
        observed_entries.append(
            (str(observation_id_value), observation_path_value, observation_hash)
        )
    if observed_entries != sorted(observed_entries):
        raise _corruption("report cut observations が ID/path 順ではありません。", path)
    current_input = inputs.get("current")
    if current_input is not None:
        _validate_report_cut_current_input(
            repo,
            current_input,
            path,
            allow_missing=allow_missing_cleanup_targets,
        )
    references = inputs.get("references")
    if not isinstance(references, list) or not all(
        isinstance(item, dict) for item in references
    ):
        raise _corruption(
            "report cut references が object array ではありません。", path
        )
    reference_ids = [item.get("reference_id") for item in references]
    if (
        not all(isinstance(item, str) and item for item in reference_ids)
        or reference_ids != sorted(reference_ids)
        or len(reference_ids) != len(set(reference_ids))
    ):
        raise _corruption(
            "report cut reference ID が一意な辞書順ではありません。", path
        )
    for reference in references:
        assert isinstance(reference, dict)
        _validate_report_cut_reference(reference, path)
    versions = inputs.get("versions")
    if (
        not isinstance(versions, dict)
        or set(versions)
        != {
            "normalization_builder",
            "normalization_schema",
            "verification_builder",
            "verification_schema",
            "deterministic_processing",
        }
        or not all(
            isinstance(key, str)
            and isinstance(value, str)
            and re.fullmatch(r"[0-9a-f]{64}", value)
            for key, value in versions.items()
        )
    ):
        raise _corruption(
            "report cut processing versions が SHA256 object ではありません。", path
        )
    processing = _require_exact_fields(
        manifest.get("processing"),
        {"status", "normalization_checkpoints", "verification_checkpoints", "failure"},
        path,
        "report cut processing",
    )
    if processing.get("status") not in {
        "ready",
        "processing",
        "interrupted",
        "failed",
        "inconclusive",
        "staging",
        "publication_ready",
    }:
        raise _corruption("report cut processing status が不正です。", path)
    checkpoint_contracts = (
        (
            "normalization_checkpoints",
            "observation_id",
            report_cut_directory(repo, str(report_cut_id_value))
            / "checkpoint"
            / "normalization",
            is_observation_id,
        ),
        (
            "verification_checkpoints",
            "candidate_id",
            report_cut_directory(repo, str(report_cut_id_value))
            / "checkpoint"
            / "verification",
            lambda value: (
                isinstance(value, str)
                and re.fullmatch(r"fbi_[a-z2-7]{26}", value) is not None
            ),
        ),
    )
    for name, id_name, expected_root, identity_validator in checkpoint_contracts:
        entries = processing.get(name)
        if not isinstance(entries, list):
            raise _corruption(f"report cut {name} が array ではありません。", path)
        identifiers: list[str] = []
        for entry in entries:
            item = _require_exact_fields(
                entry,
                {id_name, "path", "sha256"},
                path,
                f"report cut {name} entry",
            )
            identifier = item.get(id_name)
            if not identity_validator(identifier):
                raise _corruption(f"report cut {name} identity が不正です。", path)
            checkpoint_path = _validate_report_cut_artifact_reference(
                repo,
                {"path": item.get("path"), "sha256": item.get("sha256")},
                expected_root=expected_root,
                description=f"report cut {name}",
                allow_missing=allow_missing_cleanup_targets,
            )
            if checkpoint_path.exists():
                checkpoint = _read_canonical_object(
                    checkpoint_path, f"report cut {name} checkpoint"
                )
                _validate_report_cut_checkpoint(
                    checkpoint,
                    checkpoint_path,
                    expected_kind=(
                        "normalization"
                        if name == "normalization_checkpoints"
                        else "verification"
                    ),
                    expected_report_cut_id=str(report_cut_id_value),
                    expected_candidate_id=str(identifier),
                )
            identifiers.append(str(identifier))
        if identifiers != sorted(identifiers) or len(identifiers) != len(
            set(identifiers)
        ):
            raise _corruption(f"report cut {name} が一意な ID 順ではありません。", path)
    if processing.get("failure") is not None and not isinstance(
        processing.get("failure"), str
    ):
        raise _corruption(
            "report cut failure が string または null ではありません。", path
        )
    publication = manifest.get("publication")
    if publication is not None:
        _validate_publication_section(
            repo,
            publication,
            path,
            inputs=inputs,
            processing=processing,
        )
    if (
        processing.get("status") in {"staging", "publication_ready"}
        and publication is None
    ):
        raise _corruption(
            "publication 段階の report cut に成果物参照がありません。", path
        )


def _validate_report_cut_current_input(
    repo: Path,
    value: object,
    path: Path,
    *,
    allow_missing: bool,
) -> None:
    """cut 開始時の pointer と generation artifact references を検証する。"""
    current = _require_exact_fields(
        value,
        {"pointer", "generation_manifest", "issues", "machine_aggregates"},
        path,
        "report cut current input",
    )
    pointer = _require_exact_fields(
        current.get("pointer"),
        {"value", "path", "sha256"},
        path,
        "report cut current pointer input",
    )
    pointer_value = pointer.get("value")
    pointer_hash = pointer.get("sha256")
    if (
        not isinstance(pointer_value, dict)
        or not isinstance(pointer_hash, str)
        or sha256_bytes(canonical_json_bytes(pointer_value)) != pointer_hash
    ):
        raise _corruption("report cut current pointer snapshot が不正です。", path)
    _require_exact_fields(
        pointer_value,
        {
            "schema_version",
            "generation_id",
            "generation_manifest_path",
            "generation_manifest_sha256",
            "report_cut_id",
            "report_cut_manifest_sha256",
            "report_path",
            "report_sha256",
            "published_at",
            "result",
        },
        path,
        "report cut current pointer value",
    )
    generation_id_value = pointer_value.get("generation_id")
    if (
        not _is_version_one(pointer_value.get("schema_version"))
        or not is_uuid7_prefixed(generation_id_value, "fbg_")
        or not is_uuid7_prefixed(pointer_value.get("report_cut_id"), "fbc_")
        or pointer_value.get("result") not in {"ok", "attention"}
    ):
        raise _corruption("report cut current pointer value が不正です。", path)
    _require_timestamp(
        pointer_value.get("published_at"), path, "report cut current publication"
    )
    for name in (
        "generation_manifest_sha256",
        "report_cut_manifest_sha256",
        "report_sha256",
    ):
        digest = pointer_value.get(name)
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise _corruption(f"report cut current {name} が不正です。", path)
    pointer_target = _resolve_reference_path(
        repo, pointer.get("path"), active_root(repo), "report cut current pointer"
    )
    if pointer_target != current_pointer_path(repo):
        raise _corruption("report cut current pointer path が不正です。", path)
    if not allow_missing:
        _validate_artifact_reference(
            repo,
            {"path": pointer.get("path"), "sha256": pointer_hash},
            expected_root=active_root(repo),
            description="report cut current pointer",
        )
    generation_reference = current.get("generation_manifest")
    shaped_generation_reference = _artifact_reference_shape(
        generation_reference, path, "current generation"
    )
    if shaped_generation_reference != {
        "path": pointer_value.get("generation_manifest_path"),
        "sha256": pointer_value.get("generation_manifest_sha256"),
    }:
        raise _corruption(
            "report cut current generation と pointer snapshot が一致しません。", path
        )
    generation_path = _validate_report_cut_artifact_reference(
        repo,
        shaped_generation_reference,
        expected_root=generation_directory(repo, str(generation_id_value)),
        description="report cut current generation",
        allow_missing=allow_missing,
    )
    if generation_path.name != "manifest.json":
        raise _corruption("report cut current generation path が不正です。", path)
    _validate_report_cut_artifact_reference(
        repo,
        {
            "path": pointer_value.get("report_path"),
            "sha256": pointer_value.get("report_sha256"),
        },
        expected_root=repo / ".cmoc" / "gu" / "ar" / "report" / "feedback",
        description="report cut current Markdown report",
        allow_missing=False,
    )
    contracts = (
        ("issues", "issue_id"),
        ("machine_aggregates", "canonical_key"),
    )
    reference_groups: dict[str, list[JsonObject]] = {}
    for name, identity_name in contracts:
        references = current.get(name)
        if not isinstance(references, list):
            raise _corruption(
                f"report cut current {name} が array ではありません。", path
            )
        identities: list[str] = []
        for reference in references:
            item = _require_exact_fields(
                reference,
                {identity_name, "path", "sha256"},
                path,
                f"report cut current {name} reference",
            )
            identity = item.get(identity_name)
            if (
                not isinstance(identity, str)
                or not identity
                or (
                    identity_name == "issue_id"
                    and re.fullmatch(r"fbi_[a-z2-7]{26}", identity) is None
                )
                or (
                    identity_name == "canonical_key"
                    and not _is_machine_canonical_key(identity)
                )
            ):
                raise _corruption(
                    f"report cut current {name} identity が不正です。", path
                )
            _validate_report_cut_artifact_reference(
                repo,
                {"path": item.get("path"), "sha256": item.get("sha256")},
                expected_root=generation_root(repo),
                description=f"report cut current {name}",
                allow_missing=allow_missing,
            )
            identities.append(identity)
        if identities != sorted(set(identities)):
            raise _corruption(
                f"report cut current {name} が一意な辞書順ではありません。", path
            )
        reference_groups[name] = references
    if not allow_missing:
        generation_manifest, _issues, _aggregates = _load_generation(
            repo, generation_path, str(generation_id_value)
        )
        if (
            generation_manifest.get("report_cut_id")
            != pointer_value.get("report_cut_id")
            or generation_manifest.get("issues") != reference_groups["issues"]
            or generation_manifest.get("machine_aggregates")
            != reference_groups["machine_aggregates"]
        ):
            raise _corruption(
                "report cut current input が generation manifest と一致しません。",
                generation_path,
            )


def _validate_report_cut_reference(reference: JsonObject, path: Path) -> None:
    """agent に渡す固定 reference の closed variant schema を検証する。"""
    reference_id = reference.get("reference_id")
    kind = reference.get("kind")
    subjects = reference.get("subjects")
    if (
        not isinstance(reference_id, str)
        or re.fullmatch(r"[A-Za-z0-9._:-]{1,200}", reference_id) is None
        or not isinstance(subjects, list)
        or not _is_string_list(subjects, non_empty=True)
        or subjects != sorted(set(subjects))
    ):
        raise _corruption("report cut reference identity が不正です。", path)
    common = {"reference_id", "kind", "subjects"}
    if kind == "observation":
        if set(reference) != common | {"observation_id", "summary", "evidence"}:
            raise _corruption(
                "report cut observation reference field が不正です。", path
            )
        if (
            not is_observation_id(reference.get("observation_id"))
            or not isinstance(reference.get("summary"), str)
            or not isinstance(reference.get("evidence"), list)
        ):
            raise _corruption("report cut observation reference が不正です。", path)
        return
    if kind == "repository_content":
        expected = common | {"path", "state", "sha256", "content", "truncated"}
        if (
            set(reference) != expected
            or reference.get("state") != "hashed"
            or not isinstance(reference.get("content"), str)
            or not isinstance(reference.get("truncated"), bool)
        ):
            raise _corruption(
                "report cut repository content reference が不正です。", path
            )
    elif kind == "current_fingerprint":
        expected = common | {"path", "state", "sha256"}
        if set(reference) != expected or reference.get("state") not in {
            "hashed",
            "missing",
            "not_file",
            "unreadable",
        }:
            raise _corruption("report cut fingerprint reference が不正です。", path)
    elif kind == "probe_result":
        if not common | {"probe_id"} <= set(reference) or not isinstance(
            reference.get("probe_id"), str
        ):
            raise _corruption("report cut probe reference が不正です。", path)
        return
    else:
        raise _corruption("report cut reference kind が不正です。", path)
    reference_path = reference.get("path")
    digest = reference.get("sha256")
    if (
        not isinstance(reference_path, str)
        or not reference_path
        or Path(reference_path).is_absolute()
        or ".." in Path(reference_path).parts
        or (
            reference.get("state") == "hashed"
            and (
                not isinstance(digest, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            )
        )
        or (reference.get("state") != "hashed" and digest is not None)
    ):
        raise _corruption("report cut repository reference value が不正です。", path)


def _validate_report_cut_checkpoint(
    checkpoint: JsonObject,
    path: Path,
    *,
    expected_kind: str,
    expected_report_cut_id: str,
    expected_candidate_id: str,
) -> None:
    """formal normalization／verification checkpoint の content hash を検証する。"""
    _require_exact_fields(
        checkpoint,
        {
            "schema_version",
            "kind",
            "report_cut_id",
            "candidate_id",
            "input_sha256",
            "builder_sha256",
            "schema_sha256",
            "structured_output",
            "output_sha256",
        },
        path,
        "report cut checkpoint",
    )
    output = checkpoint.get("structured_output")
    if (
        not _is_version_one(checkpoint.get("schema_version"))
        or checkpoint.get("kind") != expected_kind
        or checkpoint.get("report_cut_id") != expected_report_cut_id
        or checkpoint.get("candidate_id") != expected_candidate_id
        or not isinstance(output, dict)
    ):
        raise _corruption("report cut checkpoint identity が不正です。", path)
    for name in ("input_sha256", "builder_sha256", "schema_sha256", "output_sha256"):
        value = checkpoint.get(name)
        if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise _corruption(f"report cut checkpoint {name} が不正です。", path)
    if sha256_bytes(canonical_json_bytes(output)) != checkpoint["output_sha256"]:
        raise _corruption("report cut checkpoint output hash が一致しません。", path)


def _artifact_reference_shape(
    value: object, path: Path, description: str
) -> JsonObject:
    """path/SHA256 の closed object を existence 検査前に返す。"""
    reference = _require_exact_fields(
        value, {"path", "sha256"}, path, f"{description} reference"
    )
    if not isinstance(reference.get("path"), str) or not isinstance(
        reference.get("sha256"), str
    ):
        raise _corruption(f"{description} reference field が不正です。", path)
    return reference


def _validate_report_cut_artifact_reference(
    repo: Path,
    reference: JsonObject,
    *,
    expected_root: Path,
    description: str,
    allow_missing: bool,
) -> Path:
    """publication 後 cleanup では missing を完了済みとして許す artifact 検証。"""
    if set(reference) != {"path", "sha256"}:
        raise _corruption(f"{description} reference が不正です。", expected_root)
    target = _resolve_reference_path(
        repo, reference.get("path"), expected_root, description
    )
    digest = reference.get("sha256")
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise _corruption(f"{description} SHA256 が不正です。", target)
    if not target.exists() and not target.is_symlink() and allow_missing:
        return target
    return _validate_artifact_reference(
        repo,
        reference,
        expected_root=expected_root,
        description=description,
    )


def _validate_publication_section(
    repo: Path,
    value: object,
    path: Path,
    *,
    inputs: JsonObject,
    processing: JsonObject,
) -> None:
    """staged publication と cleanup target の閉じた schema を検査する。"""
    publication = _require_exact_fields(
        value,
        {
            "generation_id",
            "generation_manifest",
            "generation_artifacts",
            "report",
            "generated_at",
            "result",
            "cleanup",
        },
        path,
        "report cut publication",
    )
    if not is_uuid7_prefixed(publication.get("generation_id"), "fbg_"):
        raise _corruption("publication generation ID が不正です。", path)
    _require_timestamp(
        publication.get("generated_at"), path, "publication generated_at"
    )
    if publication.get("result") not in {"ok", "attention"}:
        raise _corruption("publication result が不正です。", path)
    generation_id_value = str(publication["generation_id"])
    generation_reference = _artifact_reference_shape(
        publication.get("generation_manifest"), path, "publication generation manifest"
    )
    report_reference = _artifact_reference_shape(
        publication.get("report"), path, "publication report"
    )
    generation_artifacts_value = publication.get("generation_artifacts")
    if not isinstance(generation_artifacts_value, list) or not all(
        isinstance(item, dict) and set(item) == {"path", "sha256"}
        for item in generation_artifacts_value
    ):
        raise _corruption("publication generation_artifacts が不正です。", path)
    generation_artifacts = [
        _artifact_reference_shape(item, path, "publication generation artifact")
        for item in generation_artifacts_value
    ]
    generation_paths = [str(item["path"]) for item in generation_artifacts]
    if (
        not generation_artifacts
        or generation_paths != sorted(set(generation_paths))
        or generation_artifacts[-1] != generation_reference
    ):
        raise _corruption(
            "publication generation artifact 一覧が canonical ではありません。", path
        )
    staged_missing = processing.get("status") != "publication_ready"
    expected_generation_root = generation_directory(repo, generation_id_value)
    for reference in generation_artifacts:
        _validate_report_cut_artifact_reference(
            repo,
            reference,
            expected_root=expected_generation_root,
            description="publication generation artifact",
            allow_missing=staged_missing,
        )
    generation_manifest_path = _resolve_reference_path(
        repo,
        generation_reference["path"],
        expected_generation_root,
        "publication generation manifest",
    )
    if generation_manifest_path.name != "manifest.json":
        raise _corruption("publication generation manifest path が不正です。", path)
    report_path = _validate_report_cut_artifact_reference(
        repo,
        report_reference,
        expected_root=repo / ".cmoc" / "gu" / "ar" / "report" / "feedback",
        description="publication Markdown report",
        allow_missing=staged_missing,
    )
    if report_path.suffix != ".md":
        raise _corruption("publication Markdown report path が不正です。", report_path)
    if not staged_missing:
        _require_only_expected_files(
            expected_generation_root,
            {
                (repo / str(reference["path"])).resolve(strict=False)
                for reference in generation_artifacts
            },
            "publication generation",
        )
        loaded, _issues, _aggregates = _load_generation(
            repo, generation_manifest_path, generation_id_value
        )
        if loaded.get("report_cut_id") != path.parent.name:
            raise _corruption(
                "publication generation の report cut ID が一致しません。",
                generation_manifest_path,
            )
        expected_generation_artifacts = [
            {"path": item.get("path"), "sha256": item.get("sha256")}
            for name in ("issues", "machine_aggregates")
            for item in loaded.get(name, [])
            if isinstance(item, dict)
        ]
        expected_generation_artifacts.append(generation_reference)
        if generation_artifacts != expected_generation_artifacts:
            raise _corruption(
                "publication generation artifact が manifest の列挙と一致しません。",
                generation_manifest_path,
            )
    cleanup = _require_exact_fields(
        publication.get("cleanup"),
        {"observations", "old_generation", "work_artifacts"},
        path,
        "publication cleanup",
    )
    cleanup_lists: dict[str, list[JsonObject]] = {}
    for name in ("observations", "old_generation", "work_artifacts"):
        entries = cleanup.get(name)
        if not isinstance(entries, list) or not all(
            isinstance(item, dict) and set(item) == {"path", "sha256"}
            for item in entries
        ):
            raise _corruption(
                f"publication cleanup {name} が artifact reference array ではありません。",
                path,
            )
        shaped = [
            _artifact_reference_shape(item, path, f"publication cleanup {name}")
            for item in entries
        ]
        paths = [str(item["path"]) for item in shaped]
        if len(paths) != len(set(paths)) or (
            name != "observations" and paths != sorted(paths)
        ):
            raise _corruption(
                f"publication cleanup {name} が一意な path 順ではありません。",
                path,
            )
        cleanup_lists[name] = shaped

    observation_inputs = inputs.get("observations")
    if not isinstance(observation_inputs, list):
        raise _corruption("report cut observations が array ではありません。", path)
    expected_observations = [
        {"path": item.get("path"), "sha256": item.get("sha256")}
        for item in observation_inputs
        if isinstance(item, dict)
    ]
    current_input = inputs.get("current")
    expected_old_generation: list[JsonObject] = []
    if isinstance(current_input, dict):
        for name in ("issues", "machine_aggregates"):
            references = current_input.get(name)
            if not isinstance(references, list):
                raise _corruption(f"report cut current {name} が不正です。", path)
            expected_old_generation.extend(
                {"path": item.get("path"), "sha256": item.get("sha256")}
                for item in references
                if isinstance(item, dict)
            )
        generation = current_input.get("generation_manifest")
        if isinstance(generation, dict):
            expected_old_generation.append(
                {"path": generation.get("path"), "sha256": generation.get("sha256")}
            )
    expected_old_generation.sort(key=lambda item: str(item["path"]))
    expected_work: list[JsonObject] = []
    for name in ("normalization_checkpoints", "verification_checkpoints"):
        entries = processing.get(name)
        if not isinstance(entries, list):
            raise _corruption(f"report cut {name} が不正です。", path)
        expected_work.extend(
            {"path": item.get("path"), "sha256": item.get("sha256")}
            for item in entries
            if isinstance(item, dict)
        )
    expected_work.sort(key=lambda item: str(item["path"]))
    expected_cleanup = {
        "observations": expected_observations,
        "old_generation": expected_old_generation,
        "work_artifacts": expected_work,
    }
    if cleanup_lists != expected_cleanup:
        raise _corruption(
            "publication cleanup target が report cut の固定入力と一致しません。",
            path,
        )


def load_report_cut(repo: Path) -> tuple[JsonObject, Path] | None:
    """repository に高々一件ある再開対象 report cut を検証して返す。"""
    root = report_work_root(repo)
    if not root.exists() and not root.is_symlink():
        return None
    if _has_symlink_component(root) or not root.is_dir():
        raise _corruption(
            "feedback report work root が通常 directory ではありません。", root
        )
    directories = sorted(
        path for path in root.iterdir() if path.is_dir() and not path.is_symlink()
    )
    unexpected = [path for path in root.iterdir() if path not in directories]
    if unexpected:
        raise _corruption(
            "feedback report work root に未定義 artifact があります。", unexpected[0]
        )
    if len(directories) > 1:
        raise _corruption("再開対象の feedback report cut が複数あります。", root)
    if not directories:
        return None
    manifest_path = directories[0] / "manifest.json"
    manifest = _read_canonical_object(manifest_path, "report cut manifest")
    _validate_report_cut_manifest(
        repo,
        manifest,
        manifest_path,
        allow_missing_cleanup_targets=_current_pointer_selects_cut(
            repo, manifest, manifest_path
        ),
    )
    return manifest, manifest_path


def _current_pointer_selects_cut(
    repo: Path, manifest: JsonObject, manifest_path: Path
) -> bool:
    """manifest が current pointer 切替後の cleanup manifest かを byte hash で判定する。"""
    pointer_path = current_pointer_path(repo)
    if not pointer_path.exists() and not pointer_path.is_symlink():
        return False
    pointer = _read_canonical_object(pointer_path, "feedback current pointer")
    return pointer.get("report_cut_id") == manifest.get(
        "report_cut_id"
    ) and pointer.get("report_cut_manifest_sha256") == sha256_bytes(
        manifest_path.read_bytes()
    )


def write_report_cut_manifest(repo: Path, manifest: JsonObject) -> tuple[Path, str]:
    """固定入力を維持したまま report cut manifest を atomic update する。"""
    report_cut_id_value = manifest.get("report_cut_id")
    if not isinstance(report_cut_id_value, str):
        raise ValueError("report cut manifest requires report_cut_id")
    path = report_cut_manifest_path(repo, report_cut_id_value)
    _validate_report_cut_manifest_for_write(manifest, path)
    if path.exists() or path.is_symlink():
        previous = _read_canonical_object(path, "report cut manifest")
        _validate_report_cut_manifest(repo, previous, path)
        if previous.get("inputs") != manifest.get("inputs") or previous.get(
            "cut_at"
        ) != manifest.get("cut_at"):
            raise _corruption("report cut の固定入力を更新しようとしました。", path)
        current = load_active_state(repo).current
        if current is not None and current.get("report_cut_id") == report_cut_id_value:
            raise _corruption(
                "publication 済み report cut manifest は更新できません。", path
            )
    digest = _atomic_write_json(path, manifest)
    return path, digest


def recover_report_cut_checkpoint_references(
    repo: Path, manifest: JsonObject, manifest_path: Path
) -> bool:
    """formal checkpoint 保存後の停止で欠けた manifest reference を復元する。"""
    processing = manifest.get("processing")
    if not isinstance(processing, dict):
        raise _corruption("report cut processing が不正です。", manifest_path)
    report_cut_id_value = str(manifest.get("report_cut_id"))
    changed = False
    contracts = (
        (
            "normalization_checkpoints",
            "observation_id",
            "normalization",
            manifest_path.parent / "checkpoint" / "normalization",
            normalization_checkpoint_path,
        ),
        (
            "verification_checkpoints",
            "candidate_id",
            "verification",
            manifest_path.parent / "checkpoint" / "verification",
            verification_checkpoint_path,
        ),
    )
    for list_name, id_name, kind, root, expected_path_function in contracts:
        entries = processing.get(list_name)
        if not isinstance(entries, list):
            raise _corruption(f"report cut {list_name} が不正です。", manifest_path)
        by_id = {
            str(item[id_name]): item
            for item in entries
            if isinstance(item, dict) and isinstance(item.get(id_name), str)
        }
        if not root.exists() and not root.is_symlink():
            continue
        if root.is_symlink() or not root.is_dir():
            raise _corruption("feedback checkpoint root が不正です。", root)
        for checkpoint_path_value in sorted(root.rglob("*")):
            if (
                checkpoint_path_value.is_dir()
                and not checkpoint_path_value.is_symlink()
            ):
                continue
            identity = checkpoint_path_value.stem
            try:
                expected_path = expected_path_function(
                    repo, report_cut_id_value, identity
                )
            except ValueError as exc:
                raise _corruption(
                    "feedback checkpoint path が不正です。", checkpoint_path_value
                ) from exc
            if (
                checkpoint_path_value.is_symlink()
                or not checkpoint_path_value.is_file()
                or checkpoint_path_value != expected_path
            ):
                raise _corruption(
                    "feedback checkpoint path が不正です。", checkpoint_path_value
                )
            checkpoint = _read_canonical_object(
                checkpoint_path_value, "formal feedback checkpoint"
            )
            _validate_report_cut_checkpoint(
                checkpoint,
                checkpoint_path_value,
                expected_kind=kind,
                expected_report_cut_id=report_cut_id_value,
                expected_candidate_id=identity,
            )
            reference = artifact_reference(repo, checkpoint_path_value)
            expected_entry = {id_name: identity, **reference}
            existing = by_id.get(identity)
            if existing is not None:
                if existing != expected_entry:
                    raise _corruption(
                        "feedback checkpoint reference が file と一致しません。",
                        checkpoint_path_value,
                    )
                continue
            if manifest.get("publication") is not None:
                raise _corruption(
                    "staged publication に未列挙 checkpoint があります。",
                    checkpoint_path_value,
                )
            entries.append(expected_entry)
            by_id[identity] = expected_entry
            changed = True
        entries.sort(key=lambda item: str(item[id_name]))
    if changed:
        write_report_cut_manifest(repo, manifest)
    return changed


def _validate_report_cut_manifest_for_write(manifest: JsonObject, path: Path) -> None:
    """未保存 artifact を含む manifest の構造だけを write 前に検査する。"""
    # path/hash の存在検査は staged artifact の write 前には成立しないため、
    # canonical JSON 化とトップレベルの閉じた schema をここで先に確認する。
    try:
        canonical_json_bytes(manifest)
    except (TypeError, UnicodeError, ValueError) as exc:
        raise _corruption(
            "report cut manifest を canonical JSON 化できません。", path
        ) from exc
    if set(manifest) != {
        "schema_version",
        "report_cut_id",
        "cut_at",
        "inputs",
        "processing",
        "publication",
    }:
        raise _corruption("report cut manifest の top-level field が不正です。", path)
    if not _is_version_one(manifest.get("schema_version")) or not is_uuid7_prefixed(
        manifest.get("report_cut_id"), "fbc_"
    ):
        raise _corruption("report cut manifest identity が不正です。", path)


def write_checkpoint(repo: Path, path: Path, checkpoint: JsonObject) -> JsonObject:
    """正式な call result checkpoint を immutable に保存して参照を返す。"""
    digest = write_immutable_json(path, checkpoint)
    return {"path": _relative_path(repo, path), "sha256": digest}


def read_checkpoint(
    repo: Path, reference: object, expected_root: Path, description: str
) -> JsonObject:
    """manifest が参照する正式な checkpoint を hash 検証して読む。"""
    path = _validate_artifact_reference(
        repo, reference, expected_root=expected_root, description=description
    )
    return _read_canonical_object(path, description)


def validate_feedback_state(repo: Path) -> ActiveState:
    """current state、cleanup、および単一 work cut の整合性を検証する。"""
    state = load_active_state(repo)
    work = load_report_cut(repo)
    if state.cleanup_manifest_path is not None:
        if work is None or work[1] != state.cleanup_manifest_path:
            raise _corruption(
                "current pointer の cleanup manifest を一意に解決できません。",
                state.cleanup_manifest_path,
            )
    elif work is not None:
        processing = work[0].get("processing")
        if isinstance(processing, dict) and processing.get("status") == "published":
            raise _corruption(
                "未定義の published report cut status があります。", work[1]
            )
    _validate_active_artifact_inventory(repo, state, work)
    return state


def _validate_active_artifact_inventory(
    repo: Path,
    state: ActiveState,
    work: tuple[JsonObject, Path] | None,
) -> None:
    """current／staged／cleanup 対象以外の active artifact を拒否する。"""
    root = active_root(repo)
    if not root.exists() and not root.is_symlink():
        return
    allowed: set[Path] = set()
    pointer_path = current_pointer_path(repo)
    if pointer_path.exists() or pointer_path.is_symlink():
        allowed.add(pointer_path.resolve(strict=False))
    for reference in current_generation_artifacts(repo, state):
        target = _resolve_reference_path(
            repo,
            reference.get("path"),
            generation_root(repo),
            "current generation inventory",
        )
        allowed.add(target.resolve(strict=False))
    if work is not None:
        publication = work[0].get("publication")
        if isinstance(publication, dict):
            generation_references = publication.get("generation_artifacts")
            if not isinstance(generation_references, list):
                raise _corruption(
                    "staged generation artifact 一覧が不正です。", work[1]
                )
            for reference in generation_references:
                if not isinstance(reference, dict):
                    raise _corruption(
                        "staged generation artifact reference が不正です。", work[1]
                    )
                target = _resolve_reference_path(
                    repo,
                    reference.get("path"),
                    generation_root(repo),
                    "staged generation inventory",
                )
                allowed.add(target.resolve(strict=False))
            cleanup = publication.get("cleanup")
            old_generation = (
                cleanup.get("old_generation") if isinstance(cleanup, dict) else None
            )
            if not isinstance(old_generation, list):
                raise _corruption(
                    "staged publication の旧 generation cleanup が不正です。",
                    work[1],
                )
            for reference in old_generation:
                if not isinstance(reference, dict):
                    raise _corruption(
                        "旧 generation cleanup reference が不正です。", work[1]
                    )
                target = _resolve_reference_path(
                    repo,
                    reference.get("path"),
                    generation_root(repo),
                    "old generation inventory",
                )
                allowed.add(target.resolve(strict=False))
    _require_only_expected_files(root, allowed, "feedback active state")


def published_cleanup_observation_ids(repo: Path) -> set[str]:
    """切替済み cleanup manifest が処理済みと列挙する observation ID を返す。"""
    state = load_active_state(repo)
    manifest = state.cleanup_manifest
    if manifest is None:
        return set()
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        raise _corruption(
            "published report cut に publication section がありません。",
            state.cleanup_manifest_path or feedback_root(repo),
        )
    cleanup = publication.get("cleanup")
    if not isinstance(cleanup, dict) or not isinstance(
        cleanup.get("observations"), list
    ):
        raise _corruption(
            "published report cut cleanup が不正です。",
            state.cleanup_manifest_path or feedback_root(repo),
        )
    return {
        Path(str(reference["path"])).stem
        for reference in cleanup["observations"]
        if isinstance(reference, dict) and isinstance(reference.get("path"), str)
    }


def generation_artifacts(
    repo: Path,
    *,
    generation_id: str,
    report_cut_id: str,
    created_at: str,
    issues: dict[str, JsonObject],
    machine_aggregates: dict[str, JsonObject],
) -> tuple[JsonObject, tuple[tuple[Path, bytes], ...], JsonObject]:
    """新 generation の全 immutable byte 列と manifest reference を構築する。"""
    directory = generation_directory(repo, generation_id)
    if not is_uuid7_prefixed(report_cut_id, "fbc_"):
        raise ValueError(f"invalid feedback report cut ID: {report_cut_id!r}")
    _require_timestamp(created_at, directory, "active generation created_at")

    # record byte 列を先に確定し、manifest はその hash だけを列挙する。
    artifacts: list[tuple[Path, bytes]] = []
    issue_references: list[JsonObject] = []
    for current_issue_id, record in sorted(issues.items()):
        path = directory / "issue" / f"{current_issue_id}.json"
        _validate_active_issue(record, path)
        content = canonical_json_bytes(record)
        artifacts.append((path, content))
        issue_references.append(
            {
                "issue_id": current_issue_id,
                "path": _relative_path(repo, path),
                "sha256": sha256_bytes(content),
            }
        )
    aggregate_references: list[JsonObject] = []
    for canonical_key, record in sorted(machine_aggregates.items()):
        aggregate_id_value = str(record.get("aggregate_id"))
        path = directory / "machine_aggregate" / f"{aggregate_id_value}.json"
        _validate_machine_aggregate(record, path)
        if _machine_aggregate_reaches_threshold(record):
            raise ValueError(
                "threshold-reaching machine aggregate cannot be stored below threshold"
            )
        if record.get("canonical_key") != canonical_key:
            raise ValueError("machine aggregate map key differs from canonical_key")
        content = canonical_json_bytes(record)
        artifacts.append((path, content))
        aggregate_references.append(
            {
                "canonical_key": canonical_key,
                "path": _relative_path(repo, path),
                "sha256": sha256_bytes(content),
            }
        )
    manifest = {
        "schema_version": 1,
        "generation_id": generation_id,
        "report_cut_id": report_cut_id,
        "created_at": created_at,
        "issues": issue_references,
        "machine_aggregates": aggregate_references,
    }
    manifest_path = directory / "manifest.json"
    manifest_content = canonical_json_bytes(manifest)
    artifacts.append((manifest_path, manifest_content))
    reference = {
        "path": _relative_path(repo, manifest_path),
        "sha256": sha256_bytes(manifest_content),
    }
    return manifest, tuple(artifacts), reference


def publish_generation_artifacts(
    repo: Path,
    manifest: JsonObject,
    artifacts: tuple[tuple[Path, bytes], ...],
) -> Path:
    """generation records を保存し、manifest を最後に publication する。"""
    if not artifacts:
        raise ValueError("generation artifacts must include a manifest")
    manifest_path = artifacts[-1][0]
    if manifest_path.name != "manifest.json":
        raise ValueError("generation manifest must be the final artifact")
    # manifest より前の record を durable 保存してから publication marker を置く。
    for path, content in artifacts[:-1]:
        write_immutable_bytes(path, content)
    write_immutable_bytes(manifest_path, artifacts[-1][1])
    _require_only_expected_files(
        manifest_path.parent,
        {path.resolve(strict=False) for path, _content in artifacts},
        "new active generation",
    )
    loaded, _issues, _aggregates = _load_generation(
        repo, manifest_path, str(manifest.get("generation_id"))
    )
    if loaded != manifest:
        raise _corruption(
            "保存後の generation manifest が準備内容と異なります。", manifest_path
        )
    return manifest_path


def current_generation_artifacts(repo: Path, state: ActiveState) -> list[JsonObject]:
    """current generation を cleanup するための全 file reference を返す。"""
    if state.current is None or state.generation_manifest is None:
        return []
    manifest = state.generation_manifest
    references: list[JsonObject] = []
    for group in (manifest.get("issues"), manifest.get("machine_aggregates")):
        if not isinstance(group, list):
            raise _corruption(
                "current generation references が不正です。", current_pointer_path(repo)
            )
        for item in group:
            if not isinstance(item, dict):
                raise _corruption(
                    "current generation reference が object ではありません。",
                    current_pointer_path(repo),
                )
            references.append({"path": item.get("path"), "sha256": item.get("sha256")})
    references.append(
        {
            "path": state.current.get("generation_manifest_path"),
            "sha256": state.current.get("generation_manifest_sha256"),
        }
    )
    return references


def publish_current_pointer(
    repo: Path,
    *,
    generation_id: str,
    generation_manifest: JsonObject,
    report_cut_id: str,
    report_cut_manifest_sha256: str,
    report: JsonObject,
    published_at: str,
    result: str,
) -> JsonObject:
    """generation と Markdown report の検証後に current pointer を切り替える。"""
    if result not in {"ok", "attention"}:
        raise ValueError(f"invalid normal feedback result: {result!r}")
    _require_timestamp(published_at, current_pointer_path(repo), "feedback publication")
    generation_path = _validate_artifact_reference(
        repo,
        generation_manifest,
        expected_root=generation_directory(repo, generation_id),
        description="new generation manifest",
    )
    loaded_manifest, _issues, _aggregates = _load_generation(
        repo, generation_path, generation_id
    )
    if loaded_manifest.get("report_cut_id") != report_cut_id:
        raise _corruption(
            "new generation の report cut ID が一致しません。", generation_path
        )
    _validate_artifact_reference(
        repo,
        report,
        expected_root=repo / ".cmoc" / "gu" / "ar" / "report" / "feedback",
        description="new feedback Markdown report",
    )
    if re.fullmatch(r"[0-9a-f]{64}", report_cut_manifest_sha256) is None:
        raise ValueError("report cut manifest SHA256 is invalid")
    pointer = {
        "schema_version": 1,
        "generation_id": generation_id,
        "generation_manifest_path": generation_manifest["path"],
        "generation_manifest_sha256": generation_manifest["sha256"],
        "report_cut_id": report_cut_id,
        "report_cut_manifest_sha256": report_cut_manifest_sha256,
        "report_path": report["path"],
        "report_sha256": report["sha256"],
        "published_at": published_at,
        "result": result,
    }
    _atomic_write_json(current_pointer_path(repo), pointer)
    # publication point の再読みにより pointer と両成果物をまとめて検証する。
    loaded_state = load_active_state(repo)
    if loaded_state.current != pointer:
        raise _corruption(
            "切替後の feedback current pointer が一致しません。",
            current_pointer_path(repo),
        )
    return pointer


def cleanup_published_report(repo: Path) -> bool:
    """current pointer 切替後の cleanup を manifest 順で idempotent に完了する。"""
    state = load_active_state(repo)
    manifest = state.cleanup_manifest
    manifest_path = state.cleanup_manifest_path
    if manifest is None or manifest_path is None:
        return False
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        raise _corruption(
            "published report cut に publication section がありません。", manifest_path
        )
    cleanup = publication.get("cleanup")
    if not isinstance(cleanup, dict):
        raise _corruption(
            "published report cut cleanup が object ではありません。", manifest_path
        )
    cut_directory = manifest_path.parent

    # manifest を最後まで recovery source として残せるよう、未知の work file を
    # いずれかの削除より先に検出する。
    expected_work_paths = {manifest_path.resolve(strict=False)}
    for reference in _reference_list(cleanup, "work_artifacts", manifest_path):
        target = _resolve_reference_path(
            repo,
            reference.get("path"),
            cut_directory,
            "completed report cut artifact",
        )
        expected_work_paths.add(target.resolve(strict=False))
    _require_only_expected_files(
        cut_directory, expected_work_paths, "published report cut"
    )

    # raw observation は publication point 後にだけ削除する。
    for reference in _reference_list(cleanup, "observations", manifest_path):
        _unlink_artifact_reference(
            repo,
            reference,
            expected_root=feedback_root(repo) / "observation" / "v1",
            description="processed observation",
        )

    # 切替前の generation は manifest に列挙した file だけを削除する。
    for reference in _reference_list(cleanup, "old_generation", manifest_path):
        _unlink_artifact_reference(
            repo,
            reference,
            expected_root=generation_root(repo),
            description="old active generation artifact",
        )

    # checkpoint を削除し、cleanup manifest 自体を最後まで保持する。
    for reference in _reference_list(cleanup, "work_artifacts", manifest_path):
        _unlink_artifact_reference(
            repo,
            reference,
            expected_root=cut_directory,
            description="completed report cut artifact",
        )
    _prune_empty_directories(generation_root(repo), generation_root(repo))
    _durable_unlink(manifest_path)
    _prune_empty_directories(cut_directory, report_work_root(repo))
    return True


def _reference_list(container: JsonObject, name: str, path: Path) -> list[JsonObject]:
    """cleanup section の artifact reference array を型付きで返す。"""
    value = container.get(name)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise _corruption(
            f"cleanup {name} が artifact reference array ではありません。", path
        )
    return value


def _unlink_artifact_reference(
    repo: Path,
    reference: JsonObject,
    *,
    expected_root: Path,
    description: str,
) -> None:
    """hash が一致する cleanup target を missing-ok で durable unlink する。"""
    if set(reference) != {"path", "sha256"}:
        raise _corruption(f"{description} reference が不正です。", expected_root)
    path = _resolve_reference_path(
        repo, reference.get("path"), expected_root, description
    )
    if not path.exists() and not path.is_symlink():
        return
    if _has_symlink_component(path) or not path.is_file():
        raise _corruption(f"{description} が通常 file ではありません。", path)
    expected_hash = reference.get("sha256")
    if (
        not isinstance(expected_hash, str)
        or sha256_bytes(path.read_bytes()) != expected_hash
    ):
        raise _corruption(
            f"{description} の hash が cleanup manifest と一致しません。", path
        )
    _durable_unlink(path)


def _durable_unlink(path: Path) -> None:
    """通常 file を unlink して parent directory を flush する。"""
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or not path.is_file():
        raise _corruption("削除対象が通常 file ではありません。", path)
    path.unlink()
    _flush_directory(path.parent)


def _prune_empty_directories(start: Path, stop: Path) -> None:
    """start から stop までの空 directory だけを深い順に削除する。"""
    if not start.exists() or start.is_symlink() or not start.is_dir():
        return
    directories = sorted(
        (path for path in start.rglob("*") if path.is_dir() and not path.is_symlink()),
        key=lambda item: len(item.parts),
        reverse=True,
    )
    directories.append(start)
    stop_resolved = stop.resolve(strict=False)
    for directory in directories:
        candidate = directory.resolve(strict=False)
        if candidate != stop_resolved and stop_resolved not in candidate.parents:
            continue
        try:
            directory.rmdir()
        except OSError:
            continue
        if directory.parent.exists():
            _flush_directory(directory.parent)


def discard_report_cut(repo: Path, manifest: JsonObject, manifest_path: Path) -> None:
    """publication されていない inconclusive／obsolete cut を安全に破棄する。"""
    state = load_active_state(repo)
    if state.current is not None and state.current.get("report_cut_id") == manifest.get(
        "report_cut_id"
    ):
        raise _corruption(
            "current pointer が参照する report cut は discard できません。",
            manifest_path,
        )

    # staging 済み artifact は manifest が明示する path/hash だけを削除する。
    allowed_work_paths = {manifest_path.resolve(strict=False)}
    processing = manifest.get("processing")
    if not isinstance(processing, dict):
        raise _corruption(
            "discard 対象 report cut processing が不正です。", manifest_path
        )
    for name in ("normalization_checkpoints", "verification_checkpoints"):
        references = processing.get(name)
        if not isinstance(references, list):
            raise _corruption(f"discard 対象 {name} が不正です。", manifest_path)
        for reference in references:
            if not isinstance(reference, dict):
                raise _corruption(
                    f"discard 対象 {name} reference が不正です。", manifest_path
                )
            target = _resolve_reference_path(
                repo,
                reference.get("path"),
                manifest_path.parent,
                f"discard {name}",
            )
            allowed_work_paths.add(target.resolve(strict=False))

    publication = manifest.get("publication")
    if isinstance(publication, dict):
        generation_references = publication.get("generation_artifacts")
        if not isinstance(generation_references, list):
            raise _corruption(
                "staged generation artifact 一覧が不正です。", manifest_path
            )
        generation_paths = [
            _resolve_reference_path(
                repo,
                reference.get("path") if isinstance(reference, dict) else None,
                generation_root(repo),
                "staged generation artifact",
            )
            for reference in generation_references
        ]
        if generation_paths:
            generation_directory_path = generation_paths[0].parent
            while generation_directory_path.parent != generation_root(repo):
                generation_directory_path = generation_directory_path.parent
            _require_only_expected_files(
                generation_directory_path,
                {path.resolve(strict=False) for path in generation_paths},
                "staged generation",
            )
        for reference in generation_references:
            if not isinstance(reference, dict):
                raise _corruption(
                    "staged generation artifact reference が不正です。", manifest_path
                )
            _unlink_artifact_reference(
                repo,
                reference,
                expected_root=generation_root(repo),
                description="staged generation artifact",
            )
        if generation_paths:
            _prune_empty_directories(generation_directory_path, generation_root(repo))
        report_reference = publication.get("report")
        if isinstance(report_reference, dict):
            report_path = _resolve_reference_path(
                repo,
                report_reference.get("path"),
                repo / ".cmoc" / "gu" / "ar" / "report" / "feedback",
                "staged feedback report",
            )
            if report_path.exists() or report_path.is_symlink():
                _unlink_artifact_reference(
                    repo,
                    report_reference,
                    expected_root=repo / ".cmoc" / "gu" / "ar" / "report" / "feedback",
                    description="staged feedback report",
                )

    # work directory 内に manifest が列挙していない file があれば推測削除しない。
    _require_only_expected_files(
        manifest_path.parent,
        allowed_work_paths,
        "report cut",
    )
    for name in ("normalization_checkpoints", "verification_checkpoints"):
        references = processing[name]
        assert isinstance(references, list)
        for reference in references:
            assert isinstance(reference, dict)
            _unlink_artifact_reference(
                repo,
                {"path": reference.get("path"), "sha256": reference.get("sha256")},
                expected_root=manifest_path.parent,
                description=f"discard {name}",
            )
    _durable_unlink(manifest_path)
    _prune_empty_directories(manifest_path.parent, report_work_root(repo))


def _require_only_expected_files(
    root: Path, expected: set[Path], description: str
) -> None:
    """destructive cleanup 前に root 内 file がすべて manifest 由来か検査する。"""
    if not root.exists() and not root.is_symlink():
        return
    if root.is_symlink() or not root.is_dir():
        raise _corruption(f"{description} root が通常 directory ではありません。", root)
    for path in root.rglob("*"):
        if path.is_dir() and not path.is_symlink():
            continue
        if (
            path.is_symlink()
            or not path.is_file()
            or path.resolve(strict=False) not in expected
        ):
            raise _corruption(f"{description} に未定義 artifact があります。", path)
