import json
from pathlib import Path
from typing import Callable

import typer

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
from cmoc_runtime import (
    CmocError,
    SessionState,
    create_run_worktree,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored,
    head_commit,
    is_binary,
    is_git_ignored,
    load_config,
    load_state_for_branch,
    pushd,
    remove_worktree,
    reports_dir,
    repo_root,
    require_clean_worktree,
    run_git,
    timestamp,
    worktrees_dir,
)
from config.cmoc_config import CmocConfig


CodexExec = Callable[..., object]


def cmoc_review_oracle_impl(
    scope: str,
    codex_exec: CodexExec,
    enumerate_all_oracle_files_func: Callable[[Path], list[Path]],
    enumerate_targets_func: Callable[[Path, str, SessionState], list[Path]],
    run_loop_func: Callable[..., list[dict]],
    commit_index_changes_func: Callable[[Path], bool],
    merge_review_branch_func: Callable[[Path, str], str],
    render_report_func: Callable[..., str],
) -> None:
    """現在の session branch の oracle を isolated review worktree 上でレビューする。"""
    if scope not in {"session", "full"}:
        raise CmocError("scope が不正です。", ["session または full を指定してください。"], scope)
    root = repo_root()
    branch = current_branch(root)
    session_id, _state_path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/") or state.session.state != "active":
        raise CmocError("review oracle は active session branch 上で実行してください。", [], branch)
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    config = load_config(root)
    run_id = timestamp()
    review_branch = f"cmoc/run/{session_id}/{run_id}"
    review_worktree = worktrees_dir(root) / session_id / run_id
    review_fork_commit = head_commit(root)
    create_run_worktree(root, review_branch, review_worktree, "HEAD")
    review_join_commit = None
    try:
        with pushd(review_worktree):
            all_oracle_files = enumerate_all_oracle_files_func(review_worktree)
            oracle_files = enumerate_targets_func(review_worktree, scope, state)
            findings = run_loop_func(root, review_worktree, oracle_files, config, codex_exec=codex_exec)
            review_has_index_commit = commit_index_changes_func(review_worktree)
        if review_has_index_commit:
            review_join_commit = merge_review_branch_func(root, review_branch)
    finally:
        remove_worktree(root, review_worktree)
        delete_branch(root, review_branch, force=True)
    report_dir = reports_dir(root, "review_oracle")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{timestamp()}.md"
    report_path.write_text(
        render_report_func(
            root,
            scope,
            branch,
            session_id,
            state,
            len(all_oracle_files),
            oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
        )
    )
    typer.echo(str(report_path.resolve()))


def commit_review_index_changes(review_worktree: Path) -> bool:
    """review worktree 上の INDEX.md 変更だけを commit する。"""
    changed_paths = review_worktree_status_paths(review_worktree)
    non_index = [path for path in changed_paths if Path(path).name != "INDEX.md"]
    if non_index:
        raise CmocError(
            "review oracle が INDEX.md 以外の差分を作成しました。",
            ["review worktree の差分を確認してください。"],
            "\n".join(non_index),
        )
    changed_index_paths = [
        path for path in changed_paths if Path(path).name == "INDEX.md"
    ]
    if not changed_index_paths:
        return False
    run_git(["add", "-A", "--", *changed_index_paths], review_worktree)
    staged = run_git(
        ["diff", "--cached", "--name-only"], review_worktree
    ).stdout.splitlines()
    if staged:
        run_git(["commit", "-m", "cmoc review oracle indexing"], review_worktree)
        return True
    return False


def review_worktree_status_paths(review_worktree: Path) -> list[str]:
    fields = run_git(
        ["status", "--porcelain=v1", "-z"], review_worktree
    ).stdout.split("\0")
    paths: list[str] = []
    index = 0
    while index < len(fields) and fields[index]:
        field = fields[index]
        status = field[:2]
        paths.append(field[3:])
        index += 1
        if status[0] in {"R", "C"}:
            paths.append(fields[index])
            index += 1
    return paths


def merge_review_branch(root: Path, review_branch: str) -> str:
    """review branch を session branch へ merge し、merge 後 HEAD を返す。"""
    merge = run_git(["merge", "--no-ff", review_branch], root, check=False)
    if merge.returncode != 0:
        if not resolve_review_index_conflicts(root):
            raise CmocError(
                "review branch の merge に失敗しました。",
                ["git status を確認し、手動で解決してください。"],
                merge.stderr,
            )
    return head_commit(root)


def resolve_review_index_conflicts(root: Path) -> bool:
    conflicted = run_git(["diff", "--name-only", "--diff-filter=U"], root).stdout.splitlines()
    if not conflicted:
        return False
    if any(Path(path).name != "INDEX.md" for path in conflicted):
        return False
    for path in conflicted:
        run_git(["checkout", "--ours", "--", path], root)
        run_git(["add", path], root)
    run_git(["commit", "--no-edit"], root)
    return True


def enumerate_review_oracle_targets(root: Path, scope: str, state: SessionState) -> list[Path]:
    """review oracle の scope に応じた oracle file 対象を列挙する。"""
    all_oracle_files = enumerate_review_all_oracle_files(root)
    if scope == "full":
        return all_oracle_files
    start = state.session.session_start_commit
    if not start:
        return []
    changed = set(run_git(["diff", "--name-only", start, "HEAD", "--", "oracle"], root).stdout.splitlines())
    return [path for path in all_oracle_files if str(path.relative_to(root)) in changed]


def enumerate_review_all_oracle_files(root: Path) -> list[Path]:
    """review 対象候補となる oracle file 全件を列挙する。"""
    return [
        path
        for path in sorted((root / "oracle").rglob("*"))
        if path.is_file()
        and path.name != "INDEX.md"
        and not is_git_ignored(root, path)
        and not is_binary(path)
    ]


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
                    json.dumps(findings, ensure_ascii=False, indent=2),
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
            findings = apply_finding_merge_operations(findings, edits, next_id)
            next_id += len([edit for edit in edits if edit.get("kind") in {"replace", "merge"}])
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


def apply_finding_merge_operations(findings: list[dict], operations: list[dict], next_id: int) -> list[dict]:
    """merge finding Structured Output の edit operation を finding list に適用する。"""
    by_id = {finding["finding_id"]: finding for finding in findings}
    deleted: set[str] = set()
    additions: list[dict] = []
    for operation in operations:
        target_ids = set(operation.get("target_ids", []))
        kind = operation.get("kind")
        if kind == "delete":
            deleted.update(target_ids)
        elif kind in {"replace", "merge"} and operation.get("finding"):
            deleted.update(target_ids)
            finding = dict(operation["finding"])
            finding["finding_id"] = f"finding-{next_id:04d}"
            finding.setdefault("advocate_reasons", [])
            finding.setdefault("challenger_reasons", [])
            finding.setdefault("verdict", None)
            finding.setdefault("judge_reason", None)
            next_id += 1
            additions.append(finding)
    return [finding for finding in findings if finding["finding_id"] not in deleted and finding["finding_id"] in by_id] + additions


def render_review_oracle_report(
    root: Path,
    scope: str,
    session_branch: str,
    session_id: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
) -> str:
    """review oracle report を Markdown + YAML frontmatter で描画する。"""
    accepted = [finding for finding in findings if finding.get("verdict") == "accept"]
    fatal_accepted = [finding for finding in accepted if finding.get("severity") == "fatal"]
    minor_accepted = [finding for finding in accepted if finding.get("severity") == "minor"]
    fatal_rejected = [finding for finding in findings if finding.get("severity") == "fatal" and finding.get("verdict") != "accept"]
    minor_rejected = [finding for finding in findings if finding.get("severity") == "minor" and finding.get("verdict") != "accept"]
    if not oracle_files:
        result = "no_targets"
        verdict = "レビュー対象 oracle が 0 件でした。"
    elif fatal_accepted:
        result = "fatal"
        verdict = "oracle ファイルに、直ちに修正するべき問題が存在します。"
    elif minor_accepted:
        result = "minor"
        verdict = "oracle file に、致命的ではない、細かい問題があります。"
    else:
        result = "ok"
        verdict = "レビュー対象の oracle file に、問題は何ら見つかりませんでした。ただし問題点の不存在を完全保証するものではありません。"
    findings_by_path: dict[str, int] = {}
    for finding in findings:
        findings_by_path[finding.get("oracle_path", "")] = findings_by_path.get(finding.get("oracle_path", ""), 0) + 1
    rows = "\n".join(
        f"| {idx} | `{path_display(root, path)}` | {findings_by_path.get(str(path), findings_by_path.get(path_display(root, path), 0))} |"
        for idx, path in enumerate(oracle_files, 1)
    )
    return "\n".join(
        [
            "---",
            "command: review oracle",
            f"generated_at: {timestamp()}",
            f"repo_root: {root}",
            f"scope: {scope}",
            f"session_branch: {session_branch}",
            f"session_fork_commit: {state.session.session_start_commit}",
            f"review_branch: {review_branch}",
            f"review_fork_commit: {review_fork_commit}",
            f"review_join_commit: {review_join_commit}",
            f"oracle_count_total: {oracle_count_total}",
            f"oracle_count_evaluated: {len(oracle_files)}",
            f"fatal_findings_accepted_count: {len(fatal_accepted)}",
            f"minor_findings_accepted_count: {len(minor_accepted)}",
            f"fatal_findings_rejected_count: {len(fatal_rejected)}",
            f"minor_findings_rejected_count: {len(minor_rejected)}",
            f"result: {result}",
            f"session_id: {session_id}",
            "---",
            "# cmoc review oracle report",
            "## Verdict",
            verdict,
            "## Evaluated oracle file",
            "| No. | Oracle file | Findings |",
            "|---:|---|---:|",
            rows,
            "## Fatal findings",
            render_finding_section(fatal_accepted + fatal_rejected),
            "## Minor findings",
            render_finding_section(minor_accepted + minor_rejected),
            "",
        ]
    )


def render_finding_section(findings: list[dict]) -> str:
    if not findings:
        return "なし"
    return "\n".join(
        f"- `{finding.get('finding_id')}` [{finding.get('verdict') or 'unjudged'}] {finding.get('title')}: {finding.get('reason')}"
        for finding in findings
    )


def path_display(root: Path, path: Path) -> str:
    parts = path.parts
    if "oracle" in parts:
        index = parts.index("oracle")
        return str(Path(*parts[index:]))
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
