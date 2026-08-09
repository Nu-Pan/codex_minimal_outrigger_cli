"""feedback raw observation の検査と durable store を扱う。

この file は 16,000 文字を超えるが、schema 検査、secret masking、path 正規化、
fingerprint、content hash、atomic publish、および未処理件数は、同じ immutable raw
observation の byte 表現と保存先を共有する。分割すると受理時と report 時で raw
record の同一性判定が重複するため、raw observation store の境界にまとめる。

対応する oracle file:

- `{{work-root}}/oracle/doc/app_spec/feedback_observation.md`
- `{{work-root}}/oracle/doc/app_spec/feedback_state.md`
"""

import fcntl
import hashlib
import json
import os
import re
import secrets
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

OBSERVATION_SCHEMA_VERSION = 1
REPORTER_PROTOCOL_VERSION = "1"
REPORTER_VERSION = "1"
_MAX_PAYLOAD_BYTES = 32 * 1024
_PATH_EVIDENCE_KINDS = {"file", "oracle", "log"}
_UUID7_BODY_PATTERN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)


class FeedbackRejected(Exception):
    """reporter submission の domain rejection を表す。"""

    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        """公開する rejection code と再試行可否を保持する。"""
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable

    def result(self) -> dict[str, object]:
        """MCP tool result に載せる domain object を返す。"""
        return {
            "status": "rejected",
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }


def rfc3339_now() -> str:
    """UTC の RFC 3339 timestamp を生成する。"""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def uuid7_prefixed(prefix: str) -> str:
    """Python 3.12 上で UUIDv7 と prefix を組み合わせた ID を生成する。"""
    # UUIDv7 の上位 48 bit に Unix epoch millisecond を置く。
    unix_ms = int(time.time() * 1000) & ((1 << 48) - 1)
    value = unix_ms << 80
    value |= 0x7 << 76
    value |= secrets.randbits(12) << 64
    value |= 0b10 << 62
    value |= secrets.randbits(62)
    return f"{prefix}{uuid.UUID(int=value)}"


def is_uuid7_prefixed(value: object, prefix: str) -> bool:
    """指定 prefix と lowercase UUIDv7 だけから成る ID かを返す。"""
    return (
        isinstance(value, str)
        and re.fullmatch(
            re.escape(prefix) + _UUID7_BODY_PATTERN.pattern,
            value,
        )
        is not None
    )


def is_observation_id(value: object) -> bool:
    """reporter UUIDv7 または machine rule hash の observation ID かを返す。"""
    return is_uuid7_prefixed(value, "fbo_") or (
        isinstance(value, str) and re.fullmatch(r"fbo_[0-9a-f]{32}", value) is not None
    )


def canonical_json_bytes(value: object) -> bytes:
    """hash と重複判定に使用する canonical UTF-8 JSON を返す。"""
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    """byte 列の lowercase SHA256 を返す。"""
    return hashlib.sha256(value).hexdigest()


@lru_cache(maxsize=1)
def reporter_input_schema() -> dict[str, Any]:
    """oracle package resource から reporter input schema を読む。"""
    # schema field を realization へ複製しない。
    schema_text = (
        resources.files("oracle.feedback")
        .joinpath("reporter_input.json")
        .read_text(encoding="utf-8")
    )
    loaded = json.loads(schema_text)
    if not isinstance(loaded, dict):
        raise TypeError("feedback reporter schema must be a JSON object")
    Draft202012Validator.check_schema(loaded)
    return loaded


@lru_cache(maxsize=1)
def _reporter_validator() -> Draft202012Validator:
    """正本 schema から受け入れ検査用 validator を構築する。"""
    return Draft202012Validator(reporter_input_schema())


def reporter_input_validation_errors(payload: object) -> list[str]:
    """正本 reporter schema に対する違反を JSON pointer 付きで返す。"""
    errors = sorted(
        _reporter_validator().iter_errors(payload),
        key=lambda item: tuple(str(part) for part in item.path),
    )
    return [
        f"/{'/'.join(str(part) for part in error.path)}: {error.message}"
        for error in errors
    ]


def feedback_root(repo: Path) -> Path:
    """repository 共通の feedback 永続データ root を返す。"""
    return repo / ".cmoc" / "gu" / "ar" / "feedback"


def observation_root(repo: Path) -> Path:
    """schema version 1 の raw observation root を返す。"""
    return feedback_root(repo) / "observation" / "v1"


@contextmanager
def observation_publication_lock(repo: Path) -> Iterator[None]:
    """collector publication と report cut inventory の短い境界を直列化する。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    root = feedback_root(repo)
    if _has_symlink_component(root):
        raise FeedbackRejected(
            "context_invalid", f"feedback storage path uses a symlink: {root}"
        )
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / ".observation.lock"
    if lock_path.is_symlink() or (lock_path.exists() and not lock_path.is_file()):
        raise FeedbackRejected(
            "context_invalid", f"observation lock is not a regular file: {lock_path}"
        )
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def parse_rfc3339(value: str) -> datetime:
    """timezone-aware RFC 3339 timestamp を datetime として検査する。"""
    if (
        re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
            value,
        )
        is None
    ):
        raise ValueError("timestamp must use RFC 3339 syntax")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("observed_at must include a timezone")
    return parsed


def observation_path(repo: Path, observation_id: str, observed_at: str) -> Path:
    """observation ID と発生日時から immutable raw file path を返す。"""
    if not is_observation_id(observation_id):
        raise ValueError(f"invalid observation ID: {observation_id!r}")
    occurred = parse_rfc3339(observed_at)
    return (
        observation_root(repo)
        / f"{occurred.year:04d}"
        / f"{occurred.month:02d}"
        / f"{occurred.day:02d}"
        / f"{observation_id}.json"
    )


def _has_symlink_component(path: Path) -> bool:
    """path の lexical component に symlink が含まれるかを返す。"""
    current = path.absolute()
    while current != current.parent:
        if current.is_symlink():
            return True
        current = current.parent
    return False


def _atomic_create(path: Path, content: bytes) -> bool:
    """durable な sibling temporary file を排他的な atomic rename で publish する。"""
    if _has_symlink_component(path):
        raise FeedbackRejected(
            "context_invalid", f"feedback storage path uses a symlink: {path}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.{secrets.token_hex(12)}.tmp"
    try:
        # 完成した inode だけを final name から観測できるよう先に fsync する。
        with temporary.open("xb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            # 同じ保存 directory を使う collector process 間で存在確認と rename を
            # 直列化し、既存 immutable record を上書きしない。
            fcntl.flock(directory_fd, fcntl.LOCK_EX)
            temporary_prefix = f".{path.name}."
            sibling_temporaries = [
                candidate
                for candidate in path.parent.iterdir()
                if candidate.name.startswith(temporary_prefix)
                and candidate.name.endswith(".tmp")
            ]
            for candidate in sibling_temporaries:
                if (
                    candidate.is_symlink()
                    or not candidate.is_file()
                    or candidate.read_bytes() != content
                ):
                    raise FeedbackRejected(
                        "context_invalid",
                        f"feedback temporary record differs or is not regular: {candidate}",
                    )
            if os.path.lexists(path):
                if path.is_symlink() or not path.is_file():
                    raise FeedbackRejected(
                        "context_invalid",
                        f"feedback record path is not a regular file: {path}",
                    )
                for candidate in sibling_temporaries:
                    candidate.unlink(missing_ok=True)
                os.fsync(directory_fd)
                return False
            os.rename(temporary, path)
            for candidate in sibling_temporaries:
                if candidate != temporary:
                    candidate.unlink(missing_ok=True)
            os.fsync(directory_fd)
        finally:
            fcntl.flock(directory_fd, fcntl.LOCK_UN)
            os.close(directory_fd)
        return True
    finally:
        temporary.unlink(missing_ok=True)


def write_immutable_bytes(path: Path, content: bytes) -> str:
    """同一 byte 列だけを再利用できる durable file を保存する。"""
    digest = sha256_bytes(content)
    if _atomic_create(path, content):
        return digest
    try:
        current = path.read_bytes()
    except OSError as exc:
        raise FeedbackRejected(
            "context_invalid", f"existing feedback record cannot be read: {path}"
        ) from exc
    if sha256_bytes(current) != digest:
        raise FeedbackRejected(
            "context_invalid", f"immutable feedback record differs: {path}"
        )
    return digest


def recover_immutable_bytes_from_temporary(
    path: Path,
    expected_sha256: str,
) -> bool:
    """完全な sibling temporary file を期待 hash の immutable file へ回収する。"""
    if _has_symlink_component(path):
        raise FeedbackRejected(
            "context_invalid", f"feedback storage path uses a symlink: {path}"
        )
    if not path.parent.is_dir():
        return False
    prefix = f".{path.name}."
    candidates = [
        candidate
        for candidate in path.parent.iterdir()
        if candidate.name.startswith(prefix) and candidate.name.endswith(".tmp")
    ]
    if not candidates:
        return False
    if os.path.lexists(path):
        if path.is_symlink() or not path.is_file():
            raise FeedbackRejected(
                "context_invalid", f"feedback record path is not regular: {path}"
            )
        content = path.read_bytes()
        if sha256_bytes(content) != expected_sha256:
            raise FeedbackRejected(
                "context_invalid", f"feedback record hash differs: {path}"
            )
        write_immutable_bytes(path, content)
        return True
    contents: list[bytes] = []
    for candidate in candidates:
        if candidate.is_symlink() or not candidate.is_file():
            raise FeedbackRejected(
                "context_invalid",
                f"feedback temporary record is not regular: {candidate}",
            )
        content = candidate.read_bytes()
        if sha256_bytes(content) != expected_sha256:
            raise FeedbackRejected(
                "context_invalid",
                f"feedback temporary record hash differs: {candidate}",
            )
        contents.append(content)
    if any(content != contents[0] for content in contents[1:]):
        raise FeedbackRejected(
            "context_invalid",
            f"feedback temporary records differ for: {path}",
        )
    write_immutable_bytes(path, contents[0])
    return True


def write_immutable_json(path: Path, value: dict[str, Any]) -> str:
    """同一内容だけを再利用できる immutable JSON record を保存する。"""
    return write_immutable_bytes(path, canonical_json_bytes(value))


def _store_observation(
    repo: Path,
    observation_id: str,
    observed_at: str,
    envelope: dict[str, Any],
) -> Path:
    """observation ID の重複を全日付 directory で検査して保存する。"""
    path = observation_path(repo, observation_id, observed_at)
    try:
        content = canonical_json_bytes(envelope)
    except (TypeError, UnicodeError, ValueError) as exc:
        raise FeedbackRejected(
            "context_invalid", "observation must be valid UTF-8 JSON"
        ) from exc
    digest = sha256_bytes(content)
    root = observation_root(repo)
    if _has_symlink_component(root):
        raise FeedbackRejected(
            "context_invalid", f"feedback storage path uses a symlink: {root}"
        )
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise FeedbackRejected(
            "context_invalid", f"feedback observation root is unavailable: {root}"
        ) from exc

    with observation_publication_lock(repo):
        directory_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            fcntl.flock(directory_fd, fcntl.LOCK_EX)
            for existing in root.rglob(path.name):
                if existing == path:
                    continue
                if _has_symlink_component(existing) or not existing.is_file():
                    raise FeedbackRejected(
                        "context_invalid",
                        f"observation ID path is not a regular file: {existing}",
                    )
                try:
                    existing_content = existing.read_bytes()
                except OSError as exc:
                    raise FeedbackRejected(
                        "context_invalid",
                        f"existing observation cannot be read: {existing}",
                    ) from exc
                if sha256_bytes(existing_content) != digest:
                    raise FeedbackRejected(
                        "context_invalid",
                        f"observation ID collision or corruption: {existing}",
                    )
                return existing.resolve()
            write_immutable_json(path, envelope)
            return path.resolve()
        finally:
            fcntl.flock(directory_fd, fcntl.LOCK_UN)
            os.close(directory_fd)


_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private_key",
        re.compile(
            r"-----BEGIN (?:ENCRYPTED |RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY(?: BLOCK)?-----.*?"
            r"-----END (?:ENCRYPTED |RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY(?: BLOCK)?-----",
            re.DOTALL,
        ),
    ),
    (
        "authorization",
        re.compile(r"(?im)\bAuthorization\s*:\s*[^\r\n]+"),
    ),
    (
        "credential",
        re.compile(
            r"(?<![A-Za-z0-9])(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|"
            r"github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})"
        ),
    ),
)


def _mask_text(value: str) -> tuple[str, int]:
    """高確度の secret pattern だけを定型 marker へ置換する。"""
    masked = value
    count = 0
    for kind, pattern in _SECRET_PATTERNS:
        masked, replacements = pattern.subn(f"[REDACTED:{kind}]", masked)
        count += replacements
    return masked, count


def mask_feedback_text(value: str) -> str:
    """report cut に保存する text へ raw observation と同じ secret masking を適用する。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    return _mask_text(value)[0]


def _mask_payload(value: Any) -> tuple[Any, int]:
    """JSON value 内の文字列を再帰的に secret masking する。"""
    if isinstance(value, str):
        return _mask_text(value)
    if isinstance(value, list):
        masked_items: list[Any] = []
        total = 0
        for item in value:
            masked, count = _mask_payload(item)
            masked_items.append(masked)
            total += count
        return masked_items, total
    if isinstance(value, dict):
        masked_object: dict[str, Any] = {}
        total = 0
        for key, item in value.items():
            masked, count = _mask_payload(item)
            masked_object[key] = masked
            total += count
        return masked_object, total
    return value, 0


def _normalized_evidence_path(repo: Path, raw_path: str) -> Path:
    """evidence path を capability に拘束された repo 内へ正規化する。"""
    repo = repo.resolve()
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = repo / candidate
    # 存在する path は symlink 解決後、存在しない path は字句的に正規化する。
    if candidate.exists() or candidate.is_symlink():
        normalized = candidate.resolve(strict=False)
    else:
        normalized = Path(os.path.abspath(candidate))
    if normalized != repo and repo not in normalized.parents:
        raise FeedbackRejected(
            "path_outside_repo", f"evidence path is outside repository: {raw_path}"
        )
    return normalized


def _fingerprint(path: Path, evidence_index: int) -> dict[str, object]:
    """evidence file の現在 fingerprint と取得状態を返す。"""
    state = "missing"
    digest: str | None = None
    try:
        if not path.exists():
            state = "missing"
        elif not path.is_file():
            state = "not_file"
        else:
            digest = sha256_bytes(path.read_bytes())
            state = "hashed"
    except OSError:
        state = "unreadable"
        digest = None
    return {
        "evidence_index": evidence_index,
        "normalized_path": str(path),
        "state": state,
        "sha256": digest,
    }


def validate_agent_payload(
    payload: object, repo: Path
) -> tuple[dict[str, Any], list[dict[str, object]], int]:
    """reporter input を schema、安全性、path 境界で検査する。"""
    if not isinstance(payload, dict):
        raise FeedbackRejected("schema_invalid", "payload must be a JSON object")
    try:
        payload_bytes = canonical_json_bytes(payload)[:-1]
    except (TypeError, UnicodeError, ValueError) as exc:
        raise FeedbackRejected(
            "schema_invalid", "payload must be valid UTF-8 JSON"
        ) from exc
    if len(payload_bytes) > _MAX_PAYLOAD_BYTES:
        raise FeedbackRejected("payload_too_large", "payload exceeds 32 KiB")
    if isinstance(payload.get("evidence"), list) and not payload["evidence"]:
        raise FeedbackRejected("evidence_empty", "evidence must not be empty")

    # schema の唯一の正本を使い、最初の違反だけを安定した domain result にする。
    errors = reporter_input_validation_errors(payload)
    if errors:
        raise FeedbackRejected("schema_invalid", errors[0])
    evidence = payload.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise FeedbackRejected("evidence_empty", "evidence must not be empty")

    # secret は schema 検査後に mask し、mask 後の payload を raw record に保存する。
    masked_value, redaction_count = _mask_payload(payload)
    if not isinstance(masked_value, dict):
        raise FeedbackRejected("suspected_secret", "payload could not be redacted")
    # 固定長の redaction marker が短い credential を置換すると、mask 前は
    # schema 内でも mask 後に field または payload size を超えることがある。
    try:
        masked_payload_bytes = canonical_json_bytes(masked_value)[:-1]
    except (TypeError, UnicodeError, ValueError) as exc:
        raise FeedbackRejected(
            "schema_invalid", "payload must be valid UTF-8 JSON"
        ) from exc
    if len(masked_payload_bytes) > _MAX_PAYLOAD_BYTES:
        raise FeedbackRejected("payload_too_large", "redacted payload exceeds 32 KiB")
    masked_errors = reporter_input_validation_errors(masked_value)
    if masked_errors:
        raise FeedbackRejected("schema_invalid", masked_errors[0])
    masked_evidence = masked_value.get("evidence")
    if not isinstance(masked_evidence, list) or not masked_evidence:
        raise FeedbackRejected("suspected_secret", "required evidence was redacted")
    meaningful_evidence = False
    redaction_marker = re.compile(r"\[REDACTED:[a-z_]+\]")
    for item in masked_evidence:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str) and redaction_marker.sub("", text).strip():
            meaningful_evidence = True
        path = item.get("path")
        if item.get("kind") in _PATH_EVIDENCE_KINDS and isinstance(path, str):
            if redaction_marker.sub("", path).strip():
                meaningful_evidence = True
    if not meaningful_evidence:
        raise FeedbackRejected(
            "suspected_secret", "required evidence has no meaning after redaction"
        )

    # path evidence だけを正規化し、payload 本文と fingerprint の両方へ反映する。
    fingerprints: list[dict[str, object]] = []
    for index, item in enumerate(masked_evidence):
        if not isinstance(item, dict):
            continue
        if item.get("kind") not in _PATH_EVIDENCE_KINDS:
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            raise FeedbackRejected("evidence_empty", "path evidence requires a path")
        normalized = _normalized_evidence_path(repo, raw_path)
        fingerprints.append(_fingerprint(normalized, index))
    return masked_value, fingerprints, redaction_count


def store_agent_observation(
    repo: Path,
    context: dict[str, Any],
    payload: object,
    *,
    observed_at: str | None = None,
    observation_id: str | None = None,
) -> tuple[dict[str, object], Path]:
    """検証済み agent observation を raw immutable record として保存する。"""
    masked, fingerprints, redaction_count = validate_agent_payload(payload, repo)
    observed_at = observed_at or rfc3339_now()
    observation_id = observation_id or uuid7_prefixed("fbo_")
    envelope: dict[str, Any] = {
        "schema_version": OBSERVATION_SCHEMA_VERSION,
        "observation_id": observation_id,
        "source": "agent_report",
        "observed_at": observed_at,
        "context": context,
        "versions": {
            "reporter": REPORTER_VERSION,
            "reporter_protocol": REPORTER_PROTOCOL_VERSION,
            "observation_schema": OBSERVATION_SCHEMA_VERSION,
            "rule_id": None,
        },
        "payload": masked,
        "evidence_fingerprints": fingerprints,
        "source_event": None,
    }
    path = _store_observation(repo, observation_id, observed_at, envelope)
    return {
        "status": "accepted",
        "observation_id": observation_id,
        "redaction_count": redaction_count,
    }, path


def machine_observation_id(rule_id: str, event_id: str) -> str:
    """同じ stable event の再検出で変わらない observation ID を返す。"""
    digest = hashlib.sha256(f"{rule_id}\0{event_id}".encode("utf-8")).hexdigest()
    return f"fbo_{digest[:32]}"


def store_machine_observation(
    repo: Path,
    context: dict[str, Any],
    *,
    rule_id: str,
    category: str,
    subject_type: str,
    normalized_subject_id: str,
    summary: str,
    impact: str,
    human_action: str,
    event: dict[str, Any],
    log_path: Path,
) -> tuple[str, Path]:
    """allowlist rule の occurrence を deterministic raw record として保存する。"""
    event_id = event["event_id"]
    observed_at = event["occurred_at"]
    observation_id = machine_observation_id(rule_id, event_id)
    event_fields = {
        key: value
        for key, value in event.items()
        if key
        not in {
            "message",
            "stderr",
            "command_text",
        }
    }
    envelope: dict[str, Any] = {
        "schema_version": OBSERVATION_SCHEMA_VERSION,
        "observation_id": observation_id,
        "source": "machine_rule",
        "observed_at": observed_at,
        "context": context,
        "versions": {
            "reporter": None,
            "reporter_protocol": None,
            "observation_schema": OBSERVATION_SCHEMA_VERSION,
            "rule_id": rule_id,
        },
        "payload": {
            "rule_id": rule_id,
            "rule_version": 1,
            "category": category,
            "subject_type": subject_type,
            "normalized_subject_id": normalized_subject_id,
            "summary": summary,
            "impact": impact,
            "human_action": human_action,
            "event_fields": event_fields,
        },
        "evidence_fingerprints": [],
        "source_event": {
            "event_id": event_id,
            "event_type": event["event_type"],
            "event_schema_version": event["event_schema_version"],
            "log_path": str(log_path.resolve()),
            "event_sha256": sha256_bytes(canonical_json_bytes(event)),
        },
    }
    path = _store_observation(repo, observation_id, observed_at, envelope)
    return observation_id, path


def iter_observation_paths(repo: Path) -> list[Path]:
    """存在する raw observation file を path 順で列挙する。"""
    root = observation_root(repo)
    if _has_symlink_component(root) or not root.is_dir():
        return []
    return sorted(
        path
        for path in root.rglob("fbo_*.json")
        if not _has_symlink_component(path) and path.is_file()
    )


def read_json_object(path: Path) -> dict[str, Any]:
    """UTF-8 JSON file を object として読む。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON top-level must be an object: {path}")
    return value


def unprocessed_observation_paths(repo: Path) -> list[Path]:
    """raw store に残る pending observation を返す。"""
    # publication 後 cleanup 中の observation だけを処理済みとして除外する。
    from .runtime_feedback_state import published_cleanup_observation_ids

    root = observation_root(repo)
    if root.exists() or root.is_symlink():
        if _has_symlink_component(root) or not root.is_dir():
            raise ValueError(
                f"feedback observation root is not a regular directory: {root}"
            )
        for path in root.rglob("*"):
            if path.is_dir() and not path.is_symlink():
                continue
            if (
                _has_symlink_component(path)
                or not path.is_file()
                or path.suffix != ".json"
                or not path.name.startswith("fbo_")
            ):
                raise ValueError(
                    f"feedback observation store has an invalid artifact: {path}"
                )
    processed_ids = published_cleanup_observation_ids(repo)
    return [
        path for path in iter_observation_paths(repo) if path.stem not in processed_ids
    ]


def feedback_completion_counts(
    repo: Path,
) -> tuple[int | None, list[str]]:
    """通常サブコマンド完了時の pending observation 件数と warning を返す。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_observation.md
    try:
        pending = unprocessed_observation_paths(repo)
    except Exception as exc:
        return (
            None,
            [
                "repository-local feedback state を安全に検証できないため件数を計算できません。",
                f"feedback state: {exc}",
            ],
        )
    warnings: list[str] = []
    # notification threshold は詳細を展開せず report 実行だけを促す。
    oldest_age_days: float | None = None
    for path in pending:
        try:
            observation = read_json_object(path)
            observed_at = observation.get("observed_at")
            if not isinstance(observed_at, str):
                continue
            age = datetime.now(timezone.utc) - parse_rfc3339(observed_at).astimezone(
                timezone.utc
            )
            days = age.total_seconds() / 86400
            oldest_age_days = (
                days if oldest_age_days is None else max(oldest_age_days, days)
            )
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
            continue
    if len(pending) >= 100 or (oldest_age_days is not None and oldest_age_days >= 7):
        warnings.append(
            "pending feedback が蓄積しています。`cmoc feedback report` を実行してください。"
        )
    return len(pending), warnings
