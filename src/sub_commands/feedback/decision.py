"""Feedback の判定根拠と再確認履歴を扱う。

根拠: oracle/doc/app_spec/feedback.md の「用語と結果分類」。依存 path の申告を
完全とはみなさず、読める repository 入力全体を保守的な検証条件として記録する。
raw log と Git metadata は根拠の変更検知に混ぜない。
"""

import os
import stat
from pathlib import Path
from typing import Any

from cmoc_runtime import run_git
from commons.runtime_feedback_run_state import read_run_artifact
from commons.runtime_feedback_store import canonical_json_bytes, sha256_bytes
from commons.runtime_git import enumerate_oracle_and_realization_files


def worktree_inputs(worktree: Path) -> dict[str, str]:
    """tracked 入力と未 ignore の追加 file の内容・mode を読み取りだけで固定する。"""
    names = run_git(
        ["ls-files", "--cached", "--others", "--exclude-standard", "-z"], worktree
    ).stdout.split("\0")
    # nested repository 内の realization も、共通の owning-repository 分類に従う。
    oracle_files, realization_files = enumerate_oracle_and_realization_files(worktree)
    names.extend(
        path.relative_to(worktree).as_posix()
        for path in (*oracle_files, *realization_files)
    )
    files = {}
    for name in sorted(set(names) - {""}):
        parts = Path(name).parts
        if parts[0] == "memo" or ".git" in parts or parts[:2] == (".cmoc", "gu"):
            continue
        path = worktree / name
        # symlink の参照先や nested worktree を暗黙に読むことはしない。
        if any(
            parent.is_symlink()
            for parent in path.parents
            if parent != worktree and parent.is_relative_to(worktree)
        ):
            raise ValueError(f"feedback basis has a symlinked parent: {name}")
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            content = os.fsencode(os.readlink(path))
            git_mode = "120000"
        elif stat.S_ISREG(mode):
            content = path.read_bytes()
            # atomic writer の 0600 と checkout の 0644 は同じ Git 入力である。
            git_mode = "100755" if mode & stat.S_IXUSR else "100644"
        elif stat.S_ISDIR(mode):
            # gitlink の内容は上の共通列挙で捕捉する。未展開なら入力 file はない。
            continue
        else:
            raise ValueError(f"feedback basis is not a file: {name}")
        files[name] = sha256_bytes(git_mode.encode() + b"\0" + content)
    return files


def decision_state(files: dict[str, str], candidate: dict[str, Any]) -> dict[str, Any]:
    """occurrence 集計と cut 内の参照 ID を除いた判定入力を識別する。"""
    evidence = {
        name: candidate.get(name)
        for name in (
            "origin",
            "category",
            "summary",
            "impact",
            "representative_evidence",
            "reference_targets",
            "latest_fingerprints",
            "decision_evidence",
        )
    }
    return {"files": files, "evidence_sha256": state_hash(evidence)}


def state_hash(value: dict[str, Any]) -> str:
    """判定入力の canonical hash を返す。"""
    return sha256_bytes(canonical_json_bytes(value))


def basis_is_valid(basis: dict[str, Any], current: dict[str, Any]) -> bool:
    """通常の判定と、同じ入力状態の循環を根拠にした診断を区別する。"""
    return basis["state"] == current or state_hash(current) in basis["cycle_states"]


def issue_history(
    repo: Path, manifest: dict[str, Any], identity: str
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """同じ identity の正式 checkpoint を論理 call 順で読む。"""
    references = [
        item
        for item in manifest["processing"]["remediation_checkpoints"]
        if item["candidate_id"] == identity
    ]
    references.sort(key=lambda item: int(Path(item["path"]).stem.split(".")[1]))
    return [
        (
            reference,
            read_run_artifact(
                repo, {key: reference[key] for key in ("path", "sha256")}
            ),
        )
        for reference in references
    ]


def reconfirmation(
    history: list[tuple[dict[str, Any], dict[str, Any]]], current: dict[str, Any]
) -> dict[str, Any] | None:
    """再確認の理由、旧結果、入力状態の反復を agent と immutable wave へ渡す。"""
    if not history:
        return None
    reference, previous = history[-1]
    basis = previous["audit"]["decision_basis"]
    old = basis["state"]
    repeated = [
        index
        for index, (_, checkpoint) in enumerate(history)
        if checkpoint["input"]["decision_state"] == current
    ]
    # 一度の復帰は再修正を許す。同じ入力からの処理が再び同じ入力へ戻った場合、
    # 回数上限ではなく実際の循環を診断対象にする。
    cycle_states = set()
    if len(repeated) >= 2:
        for _, checkpoint in history[repeated[-2] :]:
            cycle_states.add(state_hash(checkpoint["input"]["decision_state"]))
            cycle_states.add(state_hash(checkpoint["audit"]["decision_basis"]["state"]))
        cycle_states.add(state_hash(current))
    return {
        "previous_checkpoint": reference,
        "previous_result": previous["structured_output"]["result"],
        "previous_basis": compact_basis(basis),
        "changes": {
            "paths": sorted(
                name
                for name in old["files"].keys() | current["files"].keys()
                if old["files"].get(name) != current["files"].get(name)
            ),
            "evidence_changed": old["evidence_sha256"] != current["evidence_sha256"],
        },
        "history": [reference for reference, _ in history],
        "cycle_states": sorted(cycle_states),
        "cycle_reason": (
            "A non-converging cycle has returned to the same decision inputs "
            "after repeated remediation."
        )
        if cycle_states
        else None,
    }


def decision_basis(
    state: dict[str, Any], result: dict[str, Any], recheck: dict[str, Any] | None
) -> dict[str, Any]:
    """検証直後の条件と結果を、後続の機械的同期より先に結び付ける。"""
    return {
        "scope": "repository-inputs-v1",
        "state": state,
        "verification": result["verification"],
        "current_evidence": result["current_evidence"],
        "cycle_states": recheck["cycle_states"]
        if recheck and result["status"] == "inconclusive"
        else [],
    }


def compact_basis(basis: dict[str, Any]) -> dict[str, Any]:
    """active state には file 一覧を複製せず、条件 hash と検査記録を保持する。"""
    return {key: value for key, value in basis.items() if key != "state"} | {
        "state_sha256": state_hash(basis["state"])
    }
