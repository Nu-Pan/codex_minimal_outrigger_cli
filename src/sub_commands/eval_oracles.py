"""`cmoc eval-oracles` の本体処理。"""

from pathlib import Path

from commons.codex import run_codex_exec
from commons.indexing import maintain_indexes
from commons.repo import (
    current_branch,
    ensure_cmoc_ignored,
    is_cmoc_branch,
    list_oracle_files,
    read_branch_base_commit,
    changed_oracle_files,
)
from commons.timestamps import make_timestamp


def cmoc_eval_oracles_impl(repo_root: Path, *, full: bool) -> None:
    """oracle 断片を Codex CLI で評価し、レポートを作る。"""
    print("eval-oracles (1/5) ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)

    print("eval-oracles (2/5) maintain INDEX.md files")
    maintain_indexes(repo_root)

    print("eval-oracles (3/5) select oracle files")
    branch_name = current_branch(repo_root)
    partial = is_cmoc_branch(branch_name) and not full
    if partial:
        oracle_files = changed_oracle_files(repo_root, read_branch_base_commit(repo_root, branch_name))
        mode = "partial"
    else:
        oracle_files = list_oracle_files(repo_root)
        mode = "full"

    print("eval-oracles (4/5) evaluate oracle files")
    evaluations = []
    for oracle_file in oracle_files:
        output = run_codex_exec(
            repo_root,
            _evaluation_prompt(repo_root, oracle_file),
            read_only=True,
            expect_json=False,
        )
        evaluations.append((oracle_file, output))

    print("eval-oracles (5/5) write report")
    report_path = _write_report(repo_root, mode, branch_name, evaluations)
    print(str(report_path))


def _evaluation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """oracle 評価用 prompt を組み立てる。"""
    return "\n".join(
        [
            "You are a software specification reviewer.",
            f"Review the oracle file `{oracle_file}` in repository `{repo_root}`.",
            "The task is complete when you report whether fatal specification problems exist.",
            "A fatal problem is one that can break the main workflow, prevent completion judgment, or make the core purpose unverifiable.",
            f"Do not read or edit `{repo_root / 'memo'}`.",
            "Do not edit any files.",
        ]
    )


def _write_report(
    repo_root: Path,
    mode: str,
    branch_name: str,
    evaluations: list[tuple[Path, str]],
) -> Path:
    """評価結果を `.cmoc/reports/eval-oracles` に保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / "eval-oracles"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{make_timestamp()}.md"
    lines = [
        "---",
        f"mode: {mode}",
        f"branch: {branch_name}",
        f"oracle_count: {len(evaluations)}",
        "---",
        "",
    ]
    for oracle_file, output in evaluations:
        lines.extend([f"## {oracle_file}", "", output.strip(), ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
