from pathlib import Path

from cmoc_runtime import SessionState, reports_dir, timestamp


def write_review_oracle_report(
    root: Path,
    scope: str,
    session_branch: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
    error_message: str | None = None,
) -> Path:
    report_dir = reports_dir(root, "review_oracle")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{timestamp()}.md"
    report_path.write_text(
        render_review_oracle_report(
            root,
            scope,
            session_branch,
            state,
            oracle_count_total,
            oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
            error_message=error_message,
        )
    )
    return report_path


def render_review_oracle_report(
    root: Path,
    scope: str,
    session_branch: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
    error_message: str | None = None,
) -> str:
    """eval-oracle report を Markdown + YAML frontmatter で描画する。"""
    accepted = [finding for finding in findings if finding.get("verdict") == "accept"]
    fatal_accepted = [
        finding for finding in accepted if finding.get("severity") == "fatal"
    ]
    minor_accepted = [
        finding for finding in accepted if finding.get("severity") == "minor"
    ]
    fatal_findings = [
        finding for finding in findings if finding.get("severity") == "fatal"
    ]
    minor_findings = [
        finding for finding in findings if finding.get("severity") == "minor"
    ]
    fatal_rejected = [
        finding
        for finding in findings
        if finding.get("severity") == "fatal" and finding.get("verdict") == "reject"
    ]
    minor_rejected = [
        finding
        for finding in findings
        if finding.get("severity") == "minor" and finding.get("verdict") == "reject"
    ]
    if error_message is not None:
        error_message = error_message.replace("`", "'")
    result, verdict = _review_report_verdict(
        error_message,
        oracle_files,
        fatal_findings,
        minor_findings,
    )
    findings_by_path: dict[str, int] = {}
    for finding in findings:
        oracle_path = finding.get("oracle_path", "")
        findings_by_path[oracle_path] = findings_by_path.get(oracle_path, 0) + 1
    rows = "\n".join(
        f"| {idx} | `{path_display(root, path)}` | "
        f"{findings_by_path.get(str(path), findings_by_path.get(path_display(root, path), 0))} |"
        for idx, path in enumerate(oracle_files, 1)
    )
    frontmatter = [
        ("command", "eval-oracle"),
        ("generated_at", timestamp()),
        ("repo_root", root),
        ("scope", scope),
        ("session_branch", session_branch),
        ("session_fork_commit", state.session.session_start_commit),
        ("review_branch", review_branch),
        ("review_fork_commit", review_fork_commit),
        ("review_join_commit", review_join_commit),
        ("oracle_count_total", oracle_count_total),
        ("oracle_count_evaluated", len(oracle_files)),
        ("fatal_findings_accepted_count", len(fatal_accepted)),
        ("minor_findings_accepted_count", len(minor_accepted)),
        ("fatal_findings_rejected_count", len(fatal_rejected)),
        ("minor_findings_rejected_count", len(minor_rejected)),
        ("result", result),
    ]
    return "\n".join(
        [
            "---",
            *(_render_frontmatter_field(name, value) for name, value in frontmatter),
            "---",
            "# cmoc eval-oracle report",
            "## Verdict",
            verdict,
            "## Evaluated oracle file",
            "| No. | Oracle file | Findings |",
            "|---:|---|---:|",
            rows,
            "## Fatal findings",
            render_finding_section(fatal_accepted),
            "## Minor findings",
            render_finding_section(minor_accepted),
            "## Rejected fatal findings",
            render_finding_section(fatal_rejected),
            "## Rejected minor findings",
            render_finding_section(minor_rejected),
            "",
        ]
    )


def _review_report_verdict(
    error_message: str | None,
    oracle_files: list[Path],
    fatal_accepted: list[dict],
    minor_accepted: list[dict],
) -> tuple[str, str]:
    if error_message is not None:
        return "error", f"レビュー処理が途中で失敗しました。\n\nError: `{error_message}`"
    if not oracle_files:
        return "no_targets", "レビュー対象 oracle が 0 件でした。"
    if fatal_accepted:
        return "fatal", "oracle ファイルに、直ちに修正するべき問題が存在します。"
    if minor_accepted:
        return "minor", "oracle file に、致命的ではない、細かい問題があります。"
    return (
        "ok",
        "レビュー対象の oracle file に、問題は何ら見つかりませんでした。"
        "ただし問題点の不存在を完全保証するものではありません。",
    )


def _render_frontmatter_field(name: str, value: object) -> str:
    return f"{name}: {'null' if value is None else value}"


def render_finding_section(findings: list[dict]) -> str:
    if not findings:
        return "なし"
    return "\n".join(
        f"- `{finding.get('finding_id')}` [{finding.get('verdict') or 'unjudged'}] "
        f"{finding.get('title')}: {finding.get('reason')}"
        for finding in findings
    )


def path_display(root: Path, path: Path) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = None
    if relative is not None and relative.parts[:1] == ("oracle",):
        return str(relative)
    parts = path.parts
    for index in range(len(parts) - 1, -1, -1):
        if parts[index] == "oracle":
            return str(Path(*parts[index:]))
    if relative is not None:
        return str(relative)
    return str(path)
