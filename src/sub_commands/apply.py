"""`cmoc apply` の本体処理。"""

import json
from pathlib import Path

from commons.codex import parse_json_object, run_codex_exec
from commons.errors import CmocError
from commons.indexing import maintain_indexes
from commons.repo import (
    assert_only_oracles_uncommitted,
    changed_paths,
    commit_if_changed,
    current_branch,
    ensure_cmoc_ignored,
    is_cmoc_branch,
    list_oracle_files,
    run_git,
)
from commons.timestamps import make_timestamp

APPLY_INCOMPLETE_EXIT_CODE = 2


def cmoc_apply_impl(repo_root: Path) -> int:
    """oracle と実装のズレを Codex CLI へ追従させる。"""
    branch_name = current_branch(repo_root)
    if not is_cmoc_branch(branch_name):
        raise CmocError(
            "cmoc apply must be run on a cmoc branch.",
            ["Run `cmoc branch` first.", "Checkout an existing cmoc branch."],
            f"Current branch: {branch_name}",
        )

    print("apply (1/4) validate repository state")
    assert_only_oracles_uncommitted(repo_root)
    ensure_cmoc_ignored(repo_root)
    commit_if_changed(repo_root, ["oracles"], "Update oracle files")

    print("apply (2/4) maintain INDEX.md files")
    maintain_indexes(repo_root)

    print("apply (3/4) investigate and apply discrepancies")
    discrepancy_counts: list[int] = []
    completed = False
    for loop_index in range(1, 6):
        discrepancies = _investigate_discrepancies(repo_root)
        discrepancy_counts.append(len(discrepancies))
        print(f"implementation loop ({loop_index}/5) discrepancies: {len(discrepancies)}")
        if not discrepancies:
            completed = True
            break
        _apply_discrepancies(repo_root, discrepancies)
        _assert_forbidden_paths_clean(repo_root)
        _commit_all_changes(repo_root)

    print("apply (4/4) write report")
    report_path = _write_apply_report(repo_root, branch_name, completed, discrepancy_counts)
    print(str(report_path))
    return 0 if completed else APPLY_INCOMPLETE_EXIT_CODE


def _investigate_discrepancies(repo_root: Path) -> list[dict[str, object]]:
    """oracle ファイルごとにズレ調査を実行する。"""
    discrepancies: list[dict[str, object]] = []
    for oracle_file in list_oracle_files(repo_root):
        payload = parse_json_object(
            run_codex_exec(
                repo_root,
                _investigation_prompt(repo_root, oracle_file),
                read_only=True,
                expect_json=True,
            )
        )
        values = payload.get("discrepancies")
        if not isinstance(values, list):
            raise CmocError(
                "Discrepancy investigation response is missing discrepancies.",
                ["Fix the Codex CLI JSON output.", "Run `cmoc apply` again."],
                json.dumps(payload, ensure_ascii=False),
            )
        for value in values:
            if isinstance(value, dict):
                discrepancies.append(value)
    return discrepancies


def _apply_discrepancies(repo_root: Path, discrepancies: list[dict[str, object]]) -> None:
    """Codex CLI にズレ追従作業を依頼する。"""
    run_codex_exec(
        repo_root,
        _apply_prompt(repo_root, discrepancies),
        read_only=False,
        expect_json=False,
    )


def _assert_forbidden_paths_clean(repo_root: Path) -> None:
    """Codex CLI が編集禁止領域を変更していないことを確認する。"""
    forbidden = [
        path
        for path in changed_paths(repo_root)
        if path.startswith("oracles/") or path.startswith(".agents/")
    ]
    if forbidden:
        raise CmocError(
            "Forbidden paths were changed by implementation work.",
            [
                "Inspect and manually resolve the forbidden changes.",
                "Run `cmoc apply` again after the working tree is acceptable.",
            ],
            "\n".join(forbidden),
        )


def _commit_all_changes(repo_root: Path) -> None:
    """未コミット差分を Codex 生成メッセージで commit する。"""
    if not changed_paths(repo_root):
        return
    message = run_codex_exec(
        repo_root,
        _commit_message_prompt(repo_root),
        read_only=True,
        expect_json=False,
    ).strip()
    if not message:
        message = "Apply oracle implementation changes"
    run_git(repo_root, ["add", "--all"])
    run_git(repo_root, ["commit", "-m", message])


def _write_apply_report(
    repo_root: Path,
    branch_name: str,
    completed: bool,
    discrepancy_counts: list[int],
) -> Path:
    """作業レポートを Codex CLI に依頼し、ファイル保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / "apply"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{make_timestamp()}.md"
    prompt = "\n".join(
        [
            "You are a software work reporter.",
            f"Write a concise report for branch `{branch_name}` in repository `{repo_root}`.",
            "The task is complete when the report describes the work result, discrepancy count trend, and all branch changes.",
            f"Result: {'complete' if completed else 'incomplete'}",
            f"Discrepancy counts: {discrepancy_counts}",
            f"Do not edit `{repo_root / 'oracles'}` or `{repo_root / '.agents'}`.",
        ]
    )
    report = run_codex_exec(repo_root, prompt, read_only=True, expect_json=False)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def _investigation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """ズレ調査用 prompt を組み立てる。"""
    return "\n".join(
        [
            "You are a software implementation auditor.",
            f"Investigate discrepancies between `{oracle_file}` and implementation in `{repo_root}`.",
            "The task is complete when you return JSON with a discrepancies array.",
            "Return an empty array only when there are no clear discrepancies.",
            f"Do not read or edit `{repo_root / 'memo'}`.",
            "Do not edit any files.",
        ]
    )


def _apply_prompt(repo_root: Path, discrepancies: list[dict[str, object]]) -> str:
    """ズレ追従作業用 prompt を組み立てる。"""
    return "\n".join(
        [
            "You are a software implementation agent.",
            f"Update the implementation in `{repo_root}` to resolve the listed discrepancies.",
            "The task is complete when the implementation follows the oracle requirements and tests are updated as needed.",
            f"Discrepancies: {json.dumps(discrepancies, ensure_ascii=False)}",
            f"Do not edit `{repo_root / 'oracles'}`.",
            f"Do not edit `{repo_root / '.agents'}`.",
            f"Do not read or edit `{repo_root / 'memo'}`.",
        ]
    )


def _commit_message_prompt(repo_root: Path) -> str:
    """commit message 生成用 prompt を組み立てる。"""
    return "\n".join(
        [
            "You are a commit message writer.",
            f"Write one concise git commit message for the current changes in `{repo_root}`.",
            "The task is complete when you output only the commit message.",
            "Do not edit any files.",
        ]
    )
