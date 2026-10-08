"""手動 close の固定入力と publication 後の cleanup を検証する。"""

import json
from pathlib import Path
from typing import Any

from .runtime_errors import CmocError
from .runtime_feedback_history import validate_history_record
from .runtime_feedback_state import (
    _corruption,
    _durable_unlink,
    _has_symlink_component,
    _prune_empty_directories,
    _read_canonical_object,
    _require_exact_fields,
    _require_only_expected_files,
    _require_timestamp,
    _resolve_reference_path,
    _unlink_artifact_reference,
    _validate_active_issue,
    _validate_artifact_reference,
    artifact_reference,
    generation_directory,
    generation_root,
    load_active_state,
    publish_current_pointer,
    publish_generation_artifacts,
)
from .runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    is_uuid7_prefixed,
    sha256_bytes,
    write_immutable_bytes,
)
from .runtime_ids import is_common_id


def close_work_path(repo: Path) -> Path:
    """Repository 内で単一の未完了 close を保持する場所を返す。"""
    # Writer lock を解放した後も、この記録を越えて新規処理を始めない。
    return feedback_root(repo) / "work" / "close" / "operation.json"


def load_close_work(repo: Path) -> dict[str, Any] | None:
    """固定入力と byte 列の対応を検証し、未完了 close を読む。"""
    # 対象と理由は初回保存後に変えず、再開の成否は pointer から判定する。
    path = close_work_path(repo)
    if _has_symlink_component(path.parent) or (
        path.parent.exists() and not path.parent.is_dir()
    ):
        raise _corruption("feedback close work root が不正です。", path.parent)
    if not path.exists() and not path.is_symlink():
        if path.parent.exists():
            _require_only_expected_files(path.parent, set(), "feedback close work")
        return None
    _require_only_expected_files(path.parent, {path.resolve()}, "feedback close work")
    record = _read_canonical_object(path, "feedback close work")
    _require_exact_fields(
        record,
        {
            "schema_version",
            "operation_id",
            "execution_id",
            "case_id",
            "reason",
            "closed_at",
            "base_current",
            "before",
            "before_sha256",
            "generation",
            "artifacts",
            "history",
            "report",
            "old_generation",
        },
        path,
        "feedback close work",
    )
    if (
        type(record["schema_version"]) is not int
        or record["schema_version"] != 1
        or not is_uuid7_prefixed(record["operation_id"], "fbc_")
        or not is_common_id(record["execution_id"], "exec")
        or not is_common_id(record["case_id"], "fbc")
        or not isinstance(record["reason"], str)
        or not record["reason"].strip()
        or not isinstance(record["base_current"], dict)
    ):
        raise _corruption("feedback close 固定入力が不正です。", path)
    _require_timestamp(record["closed_at"], path, "close closed_at")
    before = record["before"]
    if (
        not isinstance(before, dict)
        or before.get("case_id") != record["case_id"]
        or sha256_bytes(canonical_json_bytes(before)) != record["before_sha256"]
    ):
        raise _corruption("feedback close 対象 record/hash が不正です。", path)
    _validate_active_issue(
        before, path.parent / "issue" / f"{before.get('issue_id')}.json"
    )
    if before["verification"]["status"] != "inconclusive":
        raise _corruption(
            "feedback close 対象の判定が inconclusive ではありません。", path
        )
    generation = record["generation"]
    if (
        not isinstance(generation, dict)
        or not is_common_id(generation.get("generation_id"), "fbg")
        or generation.get("report_cut_id") != record["operation_id"]
        or generation.get("base_current") != record["base_current"]
        or generation.get("source")
        != {
            "kind": "close",
            "id": record["operation_id"],
            "execution_id": record["execution_id"],
        }
    ):
        raise _corruption("feedback close generation 対応が不正です。", path)
    artifacts = record["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        raise _corruption("feedback close artifacts が不正です。", path)
    directory = generation_directory(repo, generation["generation_id"])
    references = []
    for artifact in artifacts:
        references.append(_validate_saved_bytes(repo, artifact, directory, path))
        target = repo / artifact["path"]
        if target.name != "manifest.json":
            value = json.loads(artifact["content"])
            if target.parent == directory / "issue":
                _validate_active_issue(value, target)
                if value["case_id"] == record["case_id"]:
                    raise _corruption(
                        "close 対象が次の generation に残っています。", target
                    )
    expected = [
        {key: entry[key] for key in ("path", "sha256")}
        for name in ("issues", "machine_aggregates")
        for entry in generation.get(name, [])
    ]
    content = canonical_json_bytes(generation)
    expected.append(
        {
            "path": (directory / "manifest.json").relative_to(repo).as_posix(),
            "sha256": sha256_bytes(content),
        }
    )
    if references != expected or artifacts[-1]["content"].encode() != content:
        raise _corruption("feedback close generation artifacts が一致しません。", path)
    history = record["history"]
    history_reference = _validate_saved_bytes(
        repo, history, feedback_root(repo) / "history", path
    )
    history_record = json.loads(history["content"])
    validate_history_record(history_record, repo / history["path"])
    event = history_record["events"][0]
    if (
        history_record["generation_id"] != generation["generation_id"]
        or history_record["source"] != generation["source"]
        or generation["history"][-1] != history_reference
        or event["before"] != before
        or event["human_reason"] != record["reason"]
    ):
        raise _corruption("feedback close history 対応が不正です。", path)
    report_root = repo / ".cmoc/gu/report/feedback/close"
    report_reference = _validate_saved_bytes(repo, record["report"], report_root, path)
    if (
        report_reference["path"]
        != f".cmoc/gu/report/feedback/close/{record['execution_id']}.md"
        or history_record["report"] != report_reference["path"]
    ):
        raise _corruption("feedback close report target が不正です。", path)
    if not isinstance(record["old_generation"], list):
        raise _corruption("feedback close cleanup references が不正です。", path)
    for reference in record["old_generation"]:
        target = _resolve_reference_path(
            repo, reference.get("path"), generation_root(repo), "close old generation"
        )
        if not target.is_relative_to(
            generation_directory(repo, record["base_current"]["generation_id"])
        ):
            raise _corruption(
                "feedback close cleanup が base generation 外です。", target
            )
        if target.exists() or target.is_symlink():
            _validate_artifact_reference(
                repo,
                reference,
                expected_root=generation_root(repo),
                description="close old generation",
            )
    return record


def _validate_saved_bytes(
    repo: Path, value: object, root: Path, path: Path
) -> dict[str, Any]:
    artifact = _require_exact_fields(
        value, {"path", "sha256", "content"}, path, "close fixed artifact"
    )
    if (
        not isinstance(artifact["content"], str)
        or sha256_bytes(artifact["content"].encode()) != artifact["sha256"]
    ):
        raise _corruption("feedback close artifact bytes/hash が不正です。", path)
    target = _resolve_reference_path(
        repo, artifact["path"], root, "close fixed artifact"
    )
    reference = {key: artifact[key] for key in ("path", "sha256")}
    if target.exists() or target.is_symlink():
        _validate_artifact_reference(
            repo, reference, expected_root=root, description="close fixed artifact"
        )
    return reference


def require_no_pending_close(repo: Path) -> None:
    """別の writer に未完了 close の再実行を案内する。"""
    # Report は close の固定入力を書き換えて復旧しない。
    record = load_close_work(repo)
    if record is not None:
        raise CmocError(
            "未完了の feedback close があります。",
            [
                f"同じ案件 {record['case_id']} と保存済み理由で `cmoc feedback close` を再実行してください。"
            ],
            str(close_work_path(repo)),
        )


def complete_close(repo: Path, record: dict[str, Any]) -> Path:
    """固定 artifact を公開し、確定後の旧 generation cleanup だけを再開する。"""
    # Publication point を通過していたら終了操作を再適用しない。
    path = close_work_path(repo)
    if load_close_work(repo) != record:
        raise _corruption("feedback close の固定記録が変化しています。", path)
    state = load_active_state(repo)
    generation = record["generation"]
    published = (
        state.current is not None
        and state.current["generation_id"] == generation["generation_id"]
    )
    if not published:
        if (
            state.current != record["base_current"]
            or state.issues.get(record["before"]["issue_id"]) != record["before"]
        ):
            raise _corruption(
                "feedback close base current/対象が変化しています。", path
            )
        write_immutable_bytes(
            repo / record["history"]["path"], record["history"]["content"].encode()
        )
        publish_generation_artifacts(
            repo,
            generation,
            tuple(
                (repo / item["path"], item["content"].encode())
                for item in record["artifacts"]
            ),
        )
        write_immutable_bytes(
            repo / record["report"]["path"], record["report"]["content"].encode()
        )
        from .runtime_feedback_history import state_summary

        next_issues = {
            json.loads(item["content"])["issue_id"]: json.loads(item["content"])
            for item in record["artifacts"]
            if (repo / item["path"]).parent
            == generation_directory(repo, generation["generation_id"]) / "issue"
        }
        publish_current_pointer(
            repo,
            generation_id=generation["generation_id"],
            generation_manifest={
                key: record["artifacts"][-1][key] for key in ("path", "sha256")
            },
            report_cut_id=record["operation_id"],
            report_cut_manifest_sha256=sha256_bytes(path.read_bytes()),
            report={key: record["report"][key] for key in ("path", "sha256")},
            published_at=record["closed_at"],
            result=state_summary(next_issues),
        )
        state = load_active_state(repo)
    if (
        state.current is None
        or state.current["report_cut_manifest_sha256"]
        != sha256_bytes(path.read_bytes())
        or {
            "path": state.current["report_path"],
            "sha256": state.current["report_sha256"],
        }
        != {key: record["report"][key] for key in ("path", "sha256")}
    ):
        raise _corruption("feedback close publication point を確認できません。", path)
    # 対象を広げず、途中で削除済みの artifact も正常として扱う。
    for reference in record["old_generation"]:
        _unlink_artifact_reference(
            repo,
            reference,
            expected_root=generation_root(repo),
            description="close old generation",
        )
    _prune_empty_directories(generation_root(repo), generation_root(repo))
    report_path = repo / str(record["report"]["path"])
    if artifact_reference(repo, report_path) != {
        key: record["report"][key] for key in ("path", "sha256")
    }:
        raise _corruption("feedback close report hash が不正です。", report_path)
    _durable_unlink(path)
    _prune_empty_directories(path.parent, path.parent)
    return report_path
