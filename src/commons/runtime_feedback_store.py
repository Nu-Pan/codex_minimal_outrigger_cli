"""feedback raw observation の検査と durable store を扱う。

この file は 16,000 文字を超えるが、schema 検査、secret masking、path 正規化、
fingerprint、content hash、atomic publish、および未処理件数は、同じ immutable raw
observation の byte 表現と保存先を共有する。分割すると受理時と report 時で raw
record の同一性判定が重複するため、raw observation store の境界にまとめる。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/feedback_observation.md`。
"""

import fcntl
import hashlib
import json
import os
import re
import secrets
import time
import uuid
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
    """repository 共通の feedback raw data root を返す。"""
    return repo / ".cmoc" / "gu" / "ar" / "feedback"


def observation_root(repo: Path) -> Path:
    """schema version 1 の raw observation root を返す。"""
    return feedback_root(repo) / "observation" / "v1"


def report_snapshot_root(repo: Path) -> Path:
    """feedback report の untracked snapshot manifest root を返す。"""
    return feedback_root(repo) / "report_snapshot"


def normalization_checkpoint_root(repo: Path) -> Path:
    """normalization agent call checkpoint root を返す。"""
    return feedback_root(repo) / "normalization_checkpoint"


def tracked_feedback_root(worktree: Path) -> Path:
    """git 追跡対象の normalized feedback state root を返す。"""
    return worktree / ".cmoc" / "gt" / "ar" / "feedback"


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


def _atomic_create(path: Path, content: bytes) -> bool:
    """durable な sibling temporary file を排他的な atomic rename で publish する。"""
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
            if os.path.lexists(path):
                return False
            os.rename(temporary, path)
            os.fsync(directory_fd)
        finally:
            fcntl.flock(directory_fd, fcntl.LOCK_UN)
            os.close(directory_fd)
        return True
    finally:
        temporary.unlink(missing_ok=True)


def write_immutable_json(path: Path, value: dict[str, Any]) -> str:
    """同一内容だけを再利用できる immutable JSON record を保存する。"""
    content = canonical_json_bytes(value)
    digest = sha256_bytes(content)
    if _atomic_create(path, content):
        return digest
    try:
        current = path.read_bytes()
    except OSError as exc:
        raise FeedbackRejected(
            "context_invalid", f"existing observation cannot be read: {path}"
        ) from exc
    if sha256_bytes(current) != digest:
        raise FeedbackRejected(
            "context_invalid", f"observation ID collision or corruption: {path}"
        )
    return digest


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
    payload_bytes = canonical_json_bytes(payload)[:-1]
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
    masked_payload_bytes = canonical_json_bytes(masked_value)[:-1]
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
    path = observation_path(repo, observation_id, observed_at)
    write_immutable_json(path, envelope)
    return {
        "status": "accepted",
        "observation_id": observation_id,
        "redaction_count": redaction_count,
    }, path.resolve()


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
    path = observation_path(repo, observation_id, observed_at)
    write_immutable_json(path, envelope)
    return observation_id, path.resolve()


def iter_observation_paths(repo: Path) -> list[Path]:
    """存在する raw observation file を path 順で列挙する。"""
    root = observation_root(repo)
    if not root.is_dir():
        return []
    return sorted(path for path in root.rglob("fbo_*.json") if path.is_file())


def read_json_object(path: Path) -> dict[str, Any]:
    """UTF-8 JSON file を object として読む。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON top-level must be an object: {path}")
    return value


def ingestion_receipt_path(worktree: Path, observation_id: str) -> Path:
    """observation ごとの tracked ingestion receipt path を返す。"""
    return tracked_feedback_root(worktree) / "ingestion" / f"{observation_id}.json"


def unprocessed_observation_paths(repo: Path, worktree: Path) -> list[Path]:
    """現在 branch に ingestion receipt がない raw observation を返す。"""
    paths: list[Path] = []
    for path in iter_observation_paths(repo):
        observation_id = path.stem
        if not ingestion_receipt_path(worktree, observation_id).is_file():
            paths.append(path)
    return paths


def feedback_completion_counts(
    repo: Path, worktree: Path
) -> tuple[int, int, list[str]]:
    """通常サブコマンド完了時の raw observation 件数と warning を返す。"""
    unprocessed = unprocessed_observation_paths(repo, worktree)
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    report_dir = tracked_feedback_root(worktree) / "report"
    if report_dir.is_dir():
        for path in report_dir.glob("fbr_*.json"):
            try:
                record = read_json_object(path)
            except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
                continue
            if record.get("result") in {"ok", "attention"}:
                records.append(record)
    if not records:
        increased = len(unprocessed)
    else:
        latest = max(
            records,
            key=lambda record: (
                _best_effort_timestamp(record.get("generated_at")),
                str(record.get("report_id", "")),
            ),
        )
        report_id = latest.get("report_id")
        manifest_path = report_snapshot_root(repo) / f"{report_id}.json"
        try:
            expected_manifest_sha = latest.get("snapshot_manifest_sha256")
            if (
                not isinstance(expected_manifest_sha, str)
                or sha256_bytes(manifest_path.read_bytes()) != expected_manifest_sha
            ):
                raise ValueError("snapshot manifest hash differs from report record")
            manifest = read_json_object(manifest_path)
            if manifest.get("report_id") != report_id:
                raise ValueError("snapshot report ID differs from report record")
            entries = manifest.get("observations")
            if not isinstance(entries, list):
                raise ValueError("snapshot observations are missing")
            previous_ids = {
                entry.get("observation_id")
                for entry in entries
                if isinstance(entry, dict)
                and isinstance(entry.get("observation_id"), str)
            }
            increased = sum(path.stem not in previous_ids for path in unprocessed)
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
            increased = len(unprocessed)
            warnings.append(
                "前回 feedback report の snapshot manifest がないため未処理件数を使用しました。"
            )

    # notification threshold は詳細を展開せず report 実行だけを促す。
    oldest_age_days: float | None = None
    for path in unprocessed:
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
    if len(unprocessed) >= 100 or (
        oldest_age_days is not None and oldest_age_days >= 7
    ):
        warnings.append(
            "未処理 feedback が蓄積しています。`cmoc feedback report` を実行してください。"
        )
    return len(unprocessed), increased, warnings


def _best_effort_timestamp(value: object) -> datetime:
    """不正 record を件数表示だけで致命化せず時刻比較する key を返す。"""
    if isinstance(value, str):
        try:
            return parse_rfc3339(value).astimezone(timezone.utc)
        except ValueError:
            pass
    return datetime.min.replace(tzinfo=timezone.utc)
