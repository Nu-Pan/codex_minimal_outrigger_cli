import json
from dataclasses import replace
from pathlib import Path
from typing import Callable

from cmoc_runtime import CmocError
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
from config.cmoc_config import CmocConfig
from sub_commands.review_paths import finding_oracle_path, oracle_path_key

CodexExec = Callable[..., object]
_MAX_MERGE_FINDING_SEMANTIC_RETRIES = 2

StepCallback = Callable[[int | str, str, str | None], None]


def _report_step(
    step_callback: StepCallback | None,
    index: int | str,
    description: str,
    log_description: str,
) -> None:
    """step callback が指定された場合だけ手順開始を通知する。

    根拠: <work-root>/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    if step_callback is not None:
        step_callback(index, description, log_description)


def run_review_oracle_loop(
    log_root: Path,
    worktree: Path,
    oracle_files: list[Path],
    config: CmocConfig,
    codex_exec: CodexExec,
    step_callback: StepCallback | None = None,
) -> list[dict]:
    """review oracle の finding enumerate/merge/validate/judge loop を実行する。"""
    _report_step(step_callback, 4, "所見リスト列挙ループ", "enumerate findings loop")
    findings: list[dict] = []
    dirty_files = set(oracle_files)
    next_id = 1
    for _ in range(config.review_oracle.num_enumerate_findings_loop):
        if not dirty_files:
            break
        _report_step(
            step_callback,
            "4/8, 1/2",
            "レビュー対象ファイルを列挙",
            "enumerate oracle files",
        )
        for oracle_path in sorted(dirty_files):
            result = codex_exec(
                replace(
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
                    cwd=worktree,
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
        _report_step(step_callback, "4/8, 2/2", "所見リストをマージ", "merge findings")
        for _ in range(config.review_oracle.num_merge_findings_loop):
            findings, added_count, changed = _merge_findings_with_semantic_retry(
                log_root, worktree, findings, next_id, config, codex_exec
            )
            if not changed:
                break
            next_id += added_count
    return _validate_and_judge_findings(
        log_root, worktree, findings, config, codex_exec, step_callback
    )


def _findings_related_to_oracle_path(
    findings: list[dict], oracle_path: Path, worktree: Path
) -> list[dict]:
    """対象 oracle file と同じ repository path の finding だけを返す。

    根拠: <work-root>/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    target_key = oracle_path_key(worktree, oracle_path)
    if target_key is None:
        return []
    related: list[dict] = []
    for finding in findings:
        finding_path = finding_oracle_path(finding, worktree)
        if (
            finding_path is not None
            and oracle_path_key(worktree, finding_path) == target_key
        ):
            related.append(finding)
    return related


def _validate_and_judge_findings(
    log_root: Path,
    worktree: Path,
    findings: list[dict],
    config: CmocConfig,
    codex_exec: CodexExec,
    step_callback: StepCallback | None = None,
) -> list[dict]:
    _report_step(step_callback, 5, "所見リスト検証ループ", "validate findings loop")
    dirty_findings = {finding["finding_id"] for finding in findings}
    for _ in range(config.review_oracle.num_validate_findings_loop):
        if not dirty_findings:
            break
        next_dirty: set[str] = set()
        for finding in findings:
            if finding["finding_id"] not in dirty_findings:
                continue
            _report_step(
                step_callback,
                "5/8, 1/2",
                "所見の妥当性を反証",
                "challenge finding",
            )
            finding_text = json.dumps(finding, ensure_ascii=False, indent=2)
            challenger = codex_exec(
                replace(
                    build_review_oracle_validate_finding_challenger_parameter(
                        finding_text,
                        "\n".join(finding["advocate_reasons"]),
                        "\n".join(finding["challenger_reasons"]),
                    ),
                    cwd=worktree,
                ),
                root=log_root,
                cwd=worktree,
                config=config,
                purpose=f"review oracle validate challenger {finding['finding_id']}",
            ).output_json
            challenger_reasons = list((challenger or {}).get("reasons", []))
            _report_step(
                step_callback,
                "5/8, 2/2",
                "所見の妥当性を擁護",
                "advocate finding",
            )
            advocate = codex_exec(
                replace(
                    build_review_oracle_validate_finding_advocate_parameter(
                        finding_text,
                        "\n".join(finding["advocate_reasons"]),
                        "\n".join(finding["challenger_reasons"] + challenger_reasons),
                    ),
                    cwd=worktree,
                ),
                root=log_root,
                cwd=worktree,
                config=config,
                purpose=f"review oracle validate advocate {finding['finding_id']}",
            ).output_json
            advocate_reasons = list((advocate or {}).get("reasons", []))
            finding["challenger_reasons"].extend(challenger_reasons)
            finding["advocate_reasons"].extend(advocate_reasons)
            if challenger_reasons or advocate_reasons:
                next_dirty.add(finding["finding_id"])
        dirty_findings = next_dirty
    _report_step(step_callback, 6, "所見を採用・不採用判定", "judge findings")
    for finding in findings:
        judge = codex_exec(
            replace(
                build_review_oracle_judge_finding_parameter(
                    json.dumps(finding, ensure_ascii=False, indent=2),
                    "\n".join(finding["advocate_reasons"]),
                    "\n".join(finding["challenger_reasons"]),
                ),
                cwd=worktree,
            ),
            root=log_root,
            cwd=worktree,
            config=config,
            purpose=f"review oracle judge finding {finding['finding_id']}",
        ).output_json
        finding["verdict"] = (judge or {}).get("verdict", "reject")
        finding["judge_reason"] = (judge or {}).get("reason", "")
    return findings


def _merge_findings_with_semantic_retry(
    log_root: Path,
    worktree: Path,
    findings: list[dict],
    next_id: int,
    config: CmocConfig,
    codex_exec: CodexExec,
) -> tuple[list[dict], int, bool]:
    last_error: ValueError | None = None
    for _ in range(_MAX_MERGE_FINDING_SEMANTIC_RETRIES + 1):
        operations = codex_exec(
            replace(
                build_review_oracle_merge_finding_parameter(
                    json.dumps(findings, ensure_ascii=False, indent=2)
                ),
                cwd=worktree,
            ),
            root=log_root,
            cwd=worktree,
            config=config,
            purpose="review oracle merge findings",
        ).output_json
        edits = list((operations or {}).get("operations", []))
        if not edits:
            return findings, 0, False
        try:
            merged, added_count = apply_finding_merge_operations(
                findings, edits, next_id
            )
        except ValueError as exc:
            last_error = exc
            continue
        return merged, added_count, True
    # `<work-root>/oracle/doc/app_spec/codex_exec_rule.md` treats merge
    # operation contract violations as semantic response failures.
    raise CmocError(
        "review oracle merge finding の Structured Output 検証に失敗しました。",
        ["merge finding の Codex 出力と対象 finding_id を確認してください。"],
        str(last_error),
    ) from last_error


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
