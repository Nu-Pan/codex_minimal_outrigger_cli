import json
from pathlib import Path
from typing import Callable

from acp.builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter,
)
from acp.builder.review.oracle.judge_finding import (
    build_review_oracle_judge_finding_parameter,
)
from acp.builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter,
)
from acp.builder.review.oracle.validate_finding_advocate import (
    build_review_oracle_validate_finding_advocate_parameter,
)
from acp.builder.review.oracle.validate_finding_challenger import (
    build_review_oracle_validate_finding_challenger_parameter,
)
from basic.path_model import resolve_real_path
from config.cmoc_config import CmocConfig

CodexExec = Callable[..., object]


def run_review_oracle_loop(
    log_root: Path,
    worktree: Path,
    oracle_files: list[Path],
    config: CmocConfig,
    codex_exec: CodexExec,
) -> list[dict]:
    """review oracle の finding enumerate/merge/validate/judge loop を実行する。"""
    findings: list[dict] = []
    dirty_files = set(oracle_files)
    next_id = 1
    for _ in range(config.review_oracle.num_enumerate_findings_loop):
        if not dirty_files:
            break
        for oracle_path in sorted(dirty_files):
            result = codex_exec(
                build_review_oracle_enumerate_finding_parameter(
                    oracle_path,
                    json.dumps(
                        _findings_related_to_oracle_path(
                            findings, oracle_path, worktree
                        ),
                        ensure_ascii=False,
                        indent=2,
                    ),
                ),
                root=log_root,
                cwd=worktree,
                config=config,
                purpose=f"review oracle enumerate findings for {oracle_path}",
            )
            new_findings = list((result.output_json or {}).get("findings", []))
            if not new_findings:
                dirty_files.discard(oracle_path)
            for finding in new_findings:
                finding.setdefault("finding_id", f"finding-{next_id:04d}")
                finding.setdefault("advocate_reasons", [])
                finding.setdefault("challenger_reasons", [])
                finding.setdefault("verdict", None)
                finding.setdefault("judge_reason", None)
                next_id += 1
                findings.append(finding)
        if not dirty_files:
            break
        for _ in range(config.review_oracle.num_merge_findings_loop):
            operations = codex_exec(
                build_review_oracle_merge_finding_parameter(
                    json.dumps(findings, ensure_ascii=False, indent=2)
                ),
                root=log_root,
                cwd=worktree,
                config=config,
                purpose="review oracle merge findings",
            ).output_json
            edits = list((operations or {}).get("operations", []))
            if not edits:
                break
            findings, added_count = apply_finding_merge_operations(
                findings, edits, next_id
            )
            next_id += added_count
    return _validate_and_judge_findings(log_root, worktree, findings, config, codex_exec)


def _findings_related_to_oracle_path(
    findings: list[dict], oracle_path: Path, worktree: Path
) -> list[dict]:
    return [
        finding
        for finding in findings
        if _finding_oracle_path(finding, worktree) == oracle_path.resolve()
    ]


def _finding_oracle_path(finding: dict, worktree: Path) -> Path | None:
    raw_path = finding.get("oracle_path")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    if path.parts and path.parts[0].startswith("<"):
        try:
            return resolve_real_path(path)
        except (TypeError, ValueError):
            return None
    return (worktree / path).resolve()


def _validate_and_judge_findings(
    log_root: Path,
    worktree: Path,
    findings: list[dict],
    config: CmocConfig,
    codex_exec: CodexExec,
) -> list[dict]:
    dirty_findings = {finding["finding_id"] for finding in findings}
    for _ in range(config.review_oracle.num_validate_findings_loop):
        if not dirty_findings:
            break
        next_dirty: set[str] = set()
        for finding in findings:
            if finding["finding_id"] not in dirty_findings:
                continue
            finding_text = json.dumps(finding, ensure_ascii=False, indent=2)
            challenger = codex_exec(
                build_review_oracle_validate_finding_challenger_parameter(
                    finding_text,
                    "\n".join(finding["advocate_reasons"]),
                    "\n".join(finding["challenger_reasons"]),
                ),
                root=log_root,
                cwd=worktree,
                config=config,
                purpose=f"review oracle validate challenger {finding['finding_id']}",
            ).output_json
            advocate = codex_exec(
                build_review_oracle_validate_finding_advocate_parameter(
                    finding_text,
                    "\n".join(finding["advocate_reasons"]),
                    "\n".join(finding["challenger_reasons"]),
                ),
                root=log_root,
                cwd=worktree,
                config=config,
                purpose=f"review oracle validate advocate {finding['finding_id']}",
            ).output_json
            challenger_reasons = list((challenger or {}).get("reasons", []))
            advocate_reasons = list((advocate or {}).get("reasons", []))
            finding["challenger_reasons"].extend(challenger_reasons)
            finding["advocate_reasons"].extend(advocate_reasons)
            if challenger_reasons or advocate_reasons:
                next_dirty.add(finding["finding_id"])
        dirty_findings = next_dirty
    for finding in findings:
        judge = codex_exec(
            build_review_oracle_judge_finding_parameter(
                json.dumps(finding, ensure_ascii=False, indent=2),
                "\n".join(finding["advocate_reasons"]),
                "\n".join(finding["challenger_reasons"]),
            ),
            root=log_root,
            cwd=worktree,
            config=config,
            purpose=f"review oracle judge finding {finding['finding_id']}",
        ).output_json
        finding["verdict"] = (judge or {}).get("verdict", "reject")
        finding["judge_reason"] = (judge or {}).get("reason", "")
    return findings


def apply_finding_merge_operations(
    findings: list[dict], operations: list[dict], next_id: int
) -> tuple[list[dict], int]:
    """merge finding Structured Output の edit operation を finding list に適用する。"""
    by_id = {finding["finding_id"]: finding for finding in findings}
    existing_ids = set(by_id)
    used_ids: set[str] = set()
    validated_operations: list[tuple[dict, set[str]]] = []
    for operation in operations:
        target_ids = _validate_finding_merge_operation(operation, existing_ids)
        reused_ids = target_ids & used_ids
        if reused_ids:
            raise ValueError(
                "merge finding operation target_ids reuse finding_id: "
                + ", ".join(sorted(reused_ids))
            )
        used_ids.update(target_ids)
        validated_operations.append((operation, target_ids))
    deleted: set[str] = set()
    additions: list[dict] = []
    for operation, target_ids in validated_operations:
        kind = operation.get("kind")
        if kind == "delete":
            deleted.update(target_ids)
        else:
            deleted.update(target_ids)
            finding = dict(operation["finding"])
            finding["finding_id"] = f"finding-{next_id:04d}"
            finding.setdefault("advocate_reasons", [])
            finding.setdefault("challenger_reasons", [])
            finding.setdefault("verdict", None)
            finding.setdefault("judge_reason", None)
            next_id += 1
            additions.append(finding)
    return [
        finding
        for finding in findings
        if finding["finding_id"] not in deleted and finding["finding_id"] in by_id
    ] + additions, len(additions)


def _validate_finding_merge_operation(
    operation: dict, existing_ids: set[str]
) -> set[str]:
    kind = operation.get("kind")
    target_ids = operation.get("target_ids")
    if not isinstance(target_ids, list) or not all(
        isinstance(target_id, str) for target_id in target_ids
    ):
        raise ValueError("merge finding operation target_ids must be a string list")
    if len(set(target_ids)) != len(target_ids):
        raise ValueError(
            "merge finding operation target_ids must not contain duplicates"
        )
    target_id_set = set(target_ids)
    unknown_ids = target_id_set - existing_ids
    if unknown_ids:
        raise ValueError(
            "merge finding operation target_ids include unknown finding_id: "
            + ", ".join(sorted(unknown_ids))
        )
    finding = operation.get("finding")
    if kind == "delete":
        if not target_ids or finding is not None:
            raise ValueError("delete operation requires targets and finding null")
    elif kind == "replace":
        if len(target_ids) != 1 or not isinstance(finding, dict):
            raise ValueError(
                "replace operation requires exactly one target and a finding object"
            )
    elif kind == "merge":
        if len(target_ids) < 2 or not isinstance(finding, dict):
            raise ValueError(
                "merge operation requires at least two targets and a finding object"
            )
    else:
        raise ValueError(f"unknown merge finding operation kind: {kind!r}")
    return target_id_set
