"""Publication に結び付けた案件履歴と入力消費を保持する。

根拠: oracle/doc/app_spec/feedback_state.md の「history の保存と参照」
および「入力の消費と cleanup」。履歴は候補の再構築には使わない。
"""

import re
from pathlib import Path
from typing import Any

from .runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    is_uuid7_prefixed,
    sha256_bytes,
)
from .runtime_ids import is_common_id


def history_artifact(
    repo: Path, record: dict[str, Any]
) -> tuple[Path, bytes, dict[str, Any]]:
    """Generation ごとの immutable な履歴 byte 列と参照を作る。"""
    # 履歴の公開は generation と同じ pointer 切替まで保留する。
    path = feedback_root(repo) / "history" / f"{record['generation_id']}.json"
    validate_history_record(record, path)
    content = canonical_json_bytes(record)
    return (
        path,
        content,
        {
            "path": path.relative_to(repo).as_posix(),
            "sha256": sha256_bytes(content),
        },
    )


def validate_history_record(record: dict[str, Any], path: Path) -> None:
    """履歴の案件・判定・消費参照を閉じた schema で検証する。"""
    from .runtime_feedback_state import (
        _corruption,
        _require_exact_fields,
        _require_timestamp,
        _validate_active_issue,
    )
    from .runtime_feedback_store import is_observation_id

    # 削除済み generation や work artifact に依存する検査は行わない。
    _require_exact_fields(
        record,
        {
            "schema_version",
            "generation_id",
            "source",
            "created_at",
            "report",
            "log",
            "events",
            "observations",
        },
        path,
        "feedback history",
    )
    if (
        type(record["schema_version"]) is not int
        or record["schema_version"] != 1
        or not is_common_id(record["generation_id"], "fbg")
        or path.name != f"{record['generation_id']}.json"
    ):
        raise _corruption("feedback history identity が不正です。", path)
    _require_timestamp(record["created_at"], path, "history created_at")
    source = _require_exact_fields(
        record["source"], {"kind", "id", "execution_id"}, path, "history source"
    )
    if (
        not is_uuid7_prefixed(source["id"], "fbc_")
        or source["kind"] not in {"report", "close"}
        or not is_common_id(source["execution_id"], "exec")
    ):
        raise _corruption("feedback history source が不正です。", path)
    for name in ("report", "log"):
        value = record[name]
        if (
            not isinstance(value, str)
            or Path(value).is_absolute()
            or ".." in Path(value).parts
            or not value.startswith(".cmoc/gu/")
        ):
            raise _corruption(f"feedback history {name} が不正です。", path)
    if not isinstance(record["events"], list) or not isinstance(
        record["observations"], list
    ):
        raise _corruption("feedback history entries が不正です。", path)
    event_ids: set[str] = set()
    for event in record["events"]:
        event = _require_exact_fields(
            event,
            {
                "kind",
                "case_id",
                "issue_id",
                "before",
                "after",
                "agent_result",
                "human_reason",
            },
            path,
            "history event",
        )
        identity = event["issue_id"]
        case = event["case_id"]
        if (
            not isinstance(identity, str)
            or re.fullmatch(r"fbi_[a-z2-7]{26}", identity) is None
            or identity in event_ids
            or (case is not None and not is_common_id(case, "fbc"))
            or event["kind"]
            not in {"created", "updated", "resolved", "result", "manual_close"}
        ):
            raise _corruption("feedback history event identity が不正です。", path)
        event_ids.add(identity)
        for name in ("before", "after"):
            value = event[name]
            if value is not None:
                if (
                    not isinstance(value, dict)
                    or value.get("issue_id") != identity
                    or value.get("case_id") != case
                ):
                    raise _corruption("feedback history record 対応が不正です。", path)
                _validate_active_issue(
                    value, path.parent / "issue" / f"{identity}.json"
                )
        if event["kind"] == "manual_close":
            if (
                event["before"] is None
                or event["after"] is not None
                or event["agent_result"] is not None
                or not isinstance(event["human_reason"], str)
                or not event["human_reason"].strip()
                or event["before"]["verification"]["status"] != "inconclusive"
            ):
                raise _corruption("手動 close history が不正です。", path)
        else:
            result = event["agent_result"]
            if (
                not isinstance(result, dict)
                or result.get("status")
                not in {
                    "fixed",
                    "already_resolved",
                    "not_actionable",
                    "human_required",
                    "inconclusive",
                }
                or not isinstance(result.get("reason"), str)
                or not result["reason"].strip()
                or event["human_reason"] is not None
            ):
                raise _corruption("agent result history が不正です。", path)
    consumed: set[str] = set()
    for entry in record["observations"]:
        entry = _require_exact_fields(
            entry,
            {"observation_id", "path", "sha256", "issue_ids", "aggregate_keys"},
            path,
            "history consumed input",
        )
        identity = entry["observation_id"]
        if (
            not is_observation_id(identity)
            or identity in consumed
            or not isinstance(entry["path"], str)
            or not entry["path"].startswith(".cmoc/gu/feedback/observation/v1/")
            or ".." in Path(entry["path"]).parts
            or Path(entry["path"]).stem != identity
            or not isinstance(entry["sha256"], str)
            or re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is None
            or not isinstance(entry["issue_ids"], list)
            or not all(
                isinstance(identity, str) and identity in event_ids
                for identity in entry["issue_ids"]
            )
            or not isinstance(entry["aggregate_keys"], list)
            or not all(isinstance(key, str) for key in entry["aggregate_keys"])
            or (not entry["issue_ids"] and not entry["aggregate_keys"])
        ):
            raise _corruption("feedback history consumed input が不正です。", path)
        consumed.add(identity)
    if source["kind"] == "close" and (
        record["observations"]
        or len(record["events"]) != 1
        or record["events"][0]["kind"] != "manual_close"
    ):
        raise _corruption(
            "close が新しい入力や agent result を履歴へ追加しています。", path
        )


def load_history(repo: Path, references: object) -> list[dict[str, Any]]:
    """Generation が選ぶ確定済み履歴だけを hash 検証して読む。"""
    from .runtime_feedback_state import (
        _corruption,
        _read_canonical_object,
        _validate_artifact_reference,
    )

    # Directory に存在するだけの staged history は採用しない。
    if not isinstance(references, list):
        raise _corruption(
            "feedback history references が不正です。", feedback_root(repo)
        )
    records = []
    paths: set[Path] = set()
    for reference in references:
        target = _validate_artifact_reference(
            repo,
            reference,
            expected_root=feedback_root(repo) / "history",
            description="feedback history",
        )
        if (
            target in paths
            or target.parent != (feedback_root(repo) / "history").resolve()
        ):
            raise _corruption("feedback history path が重複または不正です。", target)
        paths.add(target)
        record = _read_canonical_object(target, "feedback history")
        validate_history_record(record, target)
        records.append(record)
    return records


def state_summary(issues: dict[str, dict[str, Any]]) -> str:
    """最新の active 判定から結果の要約を返す。"""
    # Invocation の成否はこの集約と独立して扱う。
    if any(
        issue["verification"]["status"] == "inconclusive" for issue in issues.values()
    ):
        return "incomplete"
    return "attention" if issues else "ok"
