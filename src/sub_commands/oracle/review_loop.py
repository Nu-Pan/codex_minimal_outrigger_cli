"""oracle review の finding 列挙・判定・merge loop を扱う。

この file は 16,000 文字を超えるが、review progress、同一 round の finding、merge、
interrupt 時の部分保存は同じ review loop 状態を共有する一つの責務である。
分割すると、judgement と merge operation の再開・失敗条件を複数 file で追う必要が
生じるため、現状は oracle review loop として一箇所に保つ。

根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable

from acp.builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter,
)
from acp.builder.oracle.review.judge_finding import (
    build_oracle_review_judge_finding_parameter,
)
from acp.builder.oracle.review.merge_finding import (
    build_oracle_review_merge_finding_parameter,
)
from acp.builder.oracle.review.validate_finding_advocate import (
    build_oracle_review_validate_finding_advocate_parameter,
)
from acp.builder.oracle.review.validate_finding_challenger import (
    build_oracle_review_validate_finding_challenger_parameter,
)
from basic.acp import AgentCallParameter
from basic.path_model import AgentCallPathContext
from commons.runtime_results import (
    CodexExecCallable,
    StructuredOutputValidationIssue,
)
from config.cmoc_config import CmocConfig

from .review_paths import finding_oracle_path, oracle_path_key

StepCallback = Callable[[int | str, str, str | None], None]


class OracleReviewInterrupted(KeyboardInterrupt):
    """中断までに確定した oracle review の部分結果を運ぶ。"""

    def __init__(
        self,
        findings: list[dict],
        evaluated_files: list[Path],
    ) -> None:
        """中断時に確定済みfindingと評価済みfileを例外へ保持する。"""
        super().__init__("oracle review was interrupted by the user")
        self.findings = findings
        self.evaluated_files = evaluated_files


@dataclass
class _ReviewProgress:
    """KeyboardInterrupt 発生時にも参照できる確定済み進捗。"""

    findings: list[dict]
    evaluated_files: list[Path]


def _report_step(
    step_callback: StepCallback | None,
    index: int | str,
    description: str,
    log_description: str,
) -> None:
    """step callback が指定された場合だけ手順開始を通知する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    if step_callback is not None:
        step_callback(index, description, log_description)


def _bind_review_parameter_to_worktree(
    parameter: AgentCallParameter, worktree: Path
) -> AgentCallParameter:
    """canonical review parameter を isolated review worktree の context へ束縛する。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md
    および {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md

    oracle review の canonical builder は main worktree を既定の context として
    構築する。review run が linked worktree を fork した後は、そのまま実行すると
    parameter の cwd、prompt の root 定義、indexing preflight の対象が分裂するため、
    canonical builder が生成した prompt の placeholder 定義だけを call-scoped context
    に合わせ、その他の prompt と parameter は変更しない。
    """
    source_context = AgentCallPathContext(parameter.agent_call_cwd)
    target_context = AgentCallPathContext(worktree)
    marker = "\n# place holder definition\n"
    before, separator, definitions = parameter.prompt.rpartition(marker)
    if not separator:
        raise ValueError("oracle review prompt has no placeholder definition section")

    for name, source_value, target_value in (
        ("work-root", source_context.work_root, target_context.work_root),
        (
            "oracle-root",
            source_context.work_root / "oracle",
            target_context.work_root / "oracle",
        ),
    ):
        definitions = definitions.replace(
            f"- {{{{{name}}}}} = {source_value}",
            f"- {{{{{name}}}}} = {target_value}",
        )
    return replace(
        parameter,
        prompt=before + separator + definitions,
        agent_call_cwd=target_context.agent_call_cwd,
    )


def run_oracle_review_loop(
    log_root: Path,
    worktree: Path,
    oracle_files: list[Path],
    config: CmocConfig,
    codex_exec: CodexExecCallable,
    step_callback: StepCallback | None = None,
    evaluated_files: list[Path] | None = None,
) -> list[dict]:
    """oracle review の finding enumerate/merge/validate/judge loop を実行する。

    ``evaluated_files`` が指定された場合は、列挙 agent call の完了実績を
    呼び出し元へ反映する。
    """
    progress = _ReviewProgress(
        [], evaluated_files if evaluated_files is not None else []
    )
    try:
        return _run_oracle_review_loop(
            log_root,
            worktree,
            oracle_files,
            config,
            codex_exec,
            step_callback,
            progress,
        )
    except KeyboardInterrupt as exc:
        # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
        # 未完了 agent call の出力を捨て、既に反映済みの結果だけを呼び出し元へ渡す。
        raise OracleReviewInterrupted(
            list(progress.findings),
            list(progress.evaluated_files),
        ) from exc


def _run_oracle_review_loop(
    log_root: Path,
    worktree: Path,
    oracle_files: list[Path],
    config: CmocConfig,
    codex_exec: CodexExecCallable,
    step_callback: StepCallback | None,
    progress: _ReviewProgress,
) -> list[dict]:
    """進捗を外部保持しながら oracle review loop 本体を実行する。"""
    _report_step(step_callback, 4, "所見リスト列挙ループ", "enumerate findings loop")
    findings = progress.findings
    dirty_files = set(oracle_files)
    next_id = 1
    for _ in range(config.oracle_review.num_enumerate_findings_loop):
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
                _bind_review_parameter_to_worktree(
                    build_oracle_review_enumerate_finding_parameter(
                        oracle_path,
                        json.dumps(
                            _findings_related_to_oracle_path(
                                findings, oracle_path, worktree, log_root
                            ),
                            ensure_ascii=False,
                            indent=2,
                        ),
                    ),
                    worktree,
                ),
                root=log_root,
                config=config,
                purpose=f"oracle review enumerate findings for {oracle_path}",
            )
            if oracle_path not in progress.evaluated_files:
                progress.evaluated_files.append(oracle_path)
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
        for _ in range(config.oracle_review.num_merge_findings_loop):
            findings, added_count, changed = _merge_findings(
                log_root, worktree, findings, next_id, config, codex_exec
            )
            progress.findings = findings
            if not changed:
                break
            next_id += added_count
    progress.findings = findings
    return _validate_and_judge_findings(
        log_root, worktree, findings, config, codex_exec, step_callback
    )


def _findings_related_to_oracle_path(
    findings: list[dict],
    oracle_path: Path,
    worktree: Path,
    repo_root: Path,
) -> list[dict]:
    """対象 oracle file と同じ repository path の finding だけを返す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    target_key = _review_oracle_path_key(repo_root, worktree, oracle_path)
    if target_key is None:
        return []
    related: list[dict] = []
    for finding in findings:
        finding_path = finding_oracle_path(finding, worktree)
        if (
            finding_path is not None
            and _review_oracle_path_key(repo_root, worktree, finding_path) == target_key
        ):
            related.append(finding)
    return related


def _review_oracle_path_key(repo_root: Path, worktree: Path, path: Path) -> str | None:
    """review worktree と main repository のどちらの path でも正規化する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    return oracle_path_key(worktree, path) or oracle_path_key(repo_root, path)


def _validate_and_judge_findings(
    log_root: Path,
    worktree: Path,
    findings: list[dict],
    config: CmocConfig,
    codex_exec: CodexExecCallable,
    step_callback: StepCallback | None = None,
) -> list[dict]:
    """所見の妥当性を反復検証し、各所見の採否を判定する。

    反証・擁護の新規理由がある所見だけを次の周回へ送り、検証が収束した
    所見に judge の verdict と理由を付与する。

    根拠:
        {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    _report_step(step_callback, 5, "所見リスト検証ループ", "validate findings loop")
    dirty_findings = {finding["finding_id"] for finding in findings}
    for _ in range(config.oracle_review.num_validate_findings_loop):
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
                _bind_review_parameter_to_worktree(
                    build_oracle_review_validate_finding_challenger_parameter(
                        finding_text,
                        "\n".join(finding["advocate_reasons"]),
                        "\n".join(finding["challenger_reasons"]),
                    ),
                    worktree,
                ),
                root=log_root,
                config=config,
                purpose=f"oracle review validate challenger {finding['finding_id']}",
            ).output_json
            challenger_reasons = list((challenger or {}).get("reasons", []))
            # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
            # challenger call は完了済みなので、続く advocate call の中断時にも
            # その結果だけを確定済み部分結果として残す。
            finding["challenger_reasons"].extend(challenger_reasons)
            _report_step(
                step_callback,
                "5/8, 2/2",
                "所見の妥当性を擁護",
                "advocate finding",
            )
            advocate = codex_exec(
                _bind_review_parameter_to_worktree(
                    build_oracle_review_validate_finding_advocate_parameter(
                        finding_text,
                        "\n".join(finding["advocate_reasons"]),
                        "\n".join(finding["challenger_reasons"]),
                    ),
                    worktree,
                ),
                root=log_root,
                config=config,
                purpose=f"oracle review validate advocate {finding['finding_id']}",
            ).output_json
            advocate_reasons = list((advocate or {}).get("reasons", []))
            finding["advocate_reasons"].extend(advocate_reasons)
            if challenger_reasons or advocate_reasons:
                next_dirty.add(finding["finding_id"])
        dirty_findings = next_dirty
    _report_step(step_callback, 6, "所見を採用・不採用判定", "judge findings")
    for finding in findings:
        judge = codex_exec(
            _bind_review_parameter_to_worktree(
                build_oracle_review_judge_finding_parameter(
                    json.dumps(finding, ensure_ascii=False, indent=2),
                    "\n".join(finding["advocate_reasons"]),
                    "\n".join(finding["challenger_reasons"]),
                ),
                worktree,
            ),
            root=log_root,
            config=config,
            purpose=f"oracle review judge finding {finding['finding_id']}",
        ).output_json
        finding["verdict"] = (judge or {}).get("verdict", "reject")
        finding["judge_reason"] = (judge or {}).get("reason", "")
    return findings


def _merge_findings(
    log_root: Path,
    worktree: Path,
    findings: list[dict],
    next_id: int,
    config: CmocConfig,
    codex_exec: CodexExecCallable,
) -> tuple[list[dict], int, bool]:
    """所見リストの編集操作を、検証済み Structured Output から適用する。"""
    # {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/merge_finding.py
    operations = codex_exec(
        _bind_review_parameter_to_worktree(
            build_oracle_review_merge_finding_parameter(
                json.dumps(findings, ensure_ascii=False, indent=2)
            ),
            worktree,
        ),
        root=log_root,
        config=config,
        purpose="oracle review merge findings",
        structured_output_postcondition=lambda output, changed_paths: (
            _merge_target_id_postcondition(findings, output, changed_paths)
        ),
    ).output_json
    edits: list[dict] = operations["operations"]
    if not edits:
        return findings, 0, False
    merged, added_count = apply_finding_merge_operations(findings, edits, next_id)
    return merged, added_count, True


def _merge_target_id_postcondition(
    findings: list[dict],
    output: object,
    _artifact_changed_paths: frozenset[str],
) -> tuple[StructuredOutputValidationIssue, ...]:
    """merge prompt が宣言する入力 finding_id 参照を検証する。"""
    # {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/merge_finding.py
    assert isinstance(output, dict)
    existing_ids = {finding["finding_id"] for finding in findings}
    issues: list[StructuredOutputValidationIssue] = []
    for operation_index, operation in enumerate(output["operations"]):
        for target_index, target_id in enumerate(operation["target_ids"]):
            if target_id in existing_ids:
                continue
            issues.append(
                StructuredOutputValidationIssue(
                    condition=(
                        "operations[].target_ids の各値が、入力された finding_id "
                        "集合の要素である"
                    ),
                    location=(
                        f"operations[{operation_index}].target_ids[{target_index}]"
                    ),
                    expected=repr(sorted(existing_ids)),
                    observed=repr(target_id),
                )
            )
    return tuple(issues)


def apply_finding_merge_operations(
    findings: list[dict], operations: list[dict], next_id: int
) -> tuple[list[dict], int]:
    """merge finding Structured Output の edit operation を finding list に適用する。"""
    by_id = {finding["finding_id"]: finding for finding in findings}
    deleted: set[str] = set()
    additions: list[dict] = []
    for operation in operations:
        target_ids = set(operation["target_ids"])
        kind = operation["kind"]
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
