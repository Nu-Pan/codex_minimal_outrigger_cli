"""Collector の durable な受理順序と feedback intake 境界を管理する。

根拠: {{work-root}}/oracle/doc/app_spec/feedback_state.md の
「intake wave と high-watermark」。順序番号は時刻や directory の列挙順から推測しない。
"""

from pathlib import Path
from typing import Any

from .runtime_feedback_state import (
    _atomic_write_json,
    _corruption,
    _read_canonical_object,
    _resolve_reference_path,
    artifact_reference,
)
from .runtime_feedback_store import (
    feedback_root,
    is_observation_id,
    iter_observation_paths,
    observation_publication_lock,
    observation_root,
)


def _read_ledger(repo: Path) -> dict[str, Any]:
    """pending receipt と単調増加 counter の閉じた構造を検査する。"""
    path = feedback_root(repo) / "intake.json"
    if not path.exists() and not path.is_symlink():
        return {"schema_version": 1, "high_watermark": 0, "pending": {}}
    value = _read_canonical_object(path, "feedback intake ledger")
    if (
        set(value) != {"schema_version", "high_watermark", "pending"}
        or type(value.get("schema_version")) is not int
        or value["schema_version"] != 1
        or type(value.get("high_watermark")) is not int
        or value["high_watermark"] < 0
        or not isinstance(value.get("pending"), dict)
    ):
        raise _corruption("feedback intake ledger が不正です。", path)
    sequences: set[int] = set()
    for identity, receipt in value["pending"].items():
        if (
            not is_observation_id(identity)
            or not isinstance(receipt, dict)
            or set(receipt) != {"sequence", "path", "sha256"}
            or type(receipt.get("sequence")) is not int
            or not 0 < receipt["sequence"] <= value["high_watermark"]
            or receipt["sequence"] in sequences
        ):
            raise _corruption("feedback intake receipt が不正です。", path)
        target = _resolve_reference_path(
            repo, receipt["path"], observation_root(repo), "intake receipt"
        )
        if target.stem != identity:
            raise _corruption("intake receipt の observation ID が一致しません。", path)
        sequences.add(receipt["sequence"])
    return value


def _register(repo: Path, ledger: dict[str, Any], path: Path) -> bool:
    """保存済み raw を一度だけ counter に登録する。呼び出し側が排他を保持する。"""
    reference = artifact_reference(repo, path)
    identity = path.stem
    if not is_observation_id(identity):
        raise _corruption("intake observation ID が不正です。", path)
    previous = ledger["pending"].get(identity)
    if previous is not None:
        if {key: previous[key] for key in ("path", "sha256")} != reference:
            raise _corruption(
                "intake receipt と raw observation が一致しません。", path
            )
        return False
    ledger["high_watermark"] += 1
    ledger["pending"][identity] = {"sequence": ledger["high_watermark"], **reference}
    return True


def record_observation_receipt(repo: Path, path: Path) -> None:
    """accepted を返す前に、保持中の collector 排他内で receipt を durable 保存する。"""
    ledger = _read_ledger(repo)
    if _register(repo, ledger, path):
        _atomic_write_json(feedback_root(repo) / "intake.json", ledger)


def capture_high_watermark(repo: Path, after: int) -> tuple[int, list[dict[str, Any]]]:
    """collector と同じ排他で durable receipt の上限と今回の入力を固定する。"""
    with observation_publication_lock(repo):
        ledger = _read_ledger(repo)
        changed = False
        # 導入前の raw と、raw 保存直後に停止した submission をこの境界で受理する。
        # 既存 raw の時刻を元の受理順序とみなさず、ledger への登録順を新規確定する。
        for path in iter_observation_paths(repo):
            changed = _register(repo, ledger, path) or changed
        if changed:
            _atomic_write_json(feedback_root(repo) / "intake.json", ledger)
        watermark = ledger["high_watermark"]
        if after < 0 or after > watermark:
            raise _corruption(
                "feedback high-watermark が逆行しています。", feedback_root(repo)
            )
        entries = []
        for identity, receipt in ledger["pending"].items():
            reference = {key: receipt[key] for key in ("path", "sha256")}
            if artifact_reference(repo, repo / receipt["path"]) != reference:
                raise _corruption(
                    "intake receipt の raw hash が一致しません。",
                    repo / receipt["path"],
                )
            if after < receipt["sequence"] <= watermark:
                entries.append({"observation_id": identity, **reference})
        return watermark, sorted(
            entries, key=lambda item: (item["observation_id"], item["path"])
        )


def forget_observation_receipt(repo: Path, reference: dict[str, Any]) -> None:
    """publication が指定した raw の receipt だけを削除する。排他は呼び出し側が保持する。"""
    ledger = _read_ledger(repo)
    identity = Path(reference["path"]).stem
    receipt = ledger["pending"].get(identity)
    if receipt is None:
        return
    if {key: receipt[key] for key in ("path", "sha256")} != reference:
        raise _corruption(
            "cleanup receipt hash が一致しません。", repo / reference["path"]
        )
    del ledger["pending"][identity]
    _atomic_write_json(feedback_root(repo) / "intake.json", ledger)
