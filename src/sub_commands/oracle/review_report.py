# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
from pathlib import Path

from cmoc_runtime import SessionState, reports_dir, timestamp
from sub_commands.oracle.review_paths import finding_oracle_path, oracle_path_key


def write_oracle_review_report(
    root: Path,
    scope: str,
    session_branch: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    run_branch: str | None,
    run_fork_commit: str | None,
    run_join_commit: str | None,
    error_message: str | None = None,
    *,
    interrupted: bool = False,
) -> Path:
    """レビュー結果を timestamp 名の Markdown report として保存する。

    Args:
        root: レポート保存先を解決する repository root。
        scope: レビュー対象の scope。
        session_branch: レビューを実行した session branch。
        state: session の実行状態。
        oracle_count_total: 対象候補となった oracle file の総数。
        oracle_files: 実際に評価した oracle file。
        findings: レビューで得た所見。
        run_branch: run branch 名。不明なら None。
        run_fork_commit: run fork commit。不明なら None。
        run_join_commit: run join commit。不明なら None。
        error_message: レビュー失敗時のエラーメッセージ。
    Returns:
        作成した report file の path。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    report_dir = reports_dir(root, "oracle_review")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{timestamp()}.md"
    report_path.write_text(
        render_oracle_review_report(
            root,
            scope,
            session_branch,
            state,
            oracle_count_total,
            oracle_files,
            findings,
            run_branch,
            run_fork_commit,
            run_join_commit,
            error_message=error_message,
            interrupted=interrupted,
        )
    )
    return report_path


def render_oracle_review_report(
    root: Path,
    scope: str,
    session_branch: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    run_branch: str | None,
    run_fork_commit: str | None,
    run_join_commit: str | None,
    error_message: str | None = None,
    *,
    interrupted: bool = False,
) -> str:
    """oracle review report を Markdown と YAML frontmatter で描画する。

    レポートの frontmatter、必須セクション、所見の表示順をまとめて生成する。
    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    accepted = [finding for finding in findings if finding.get("verdict") == "accept"]
    rejected = [finding for finding in findings if finding.get("verdict") == "reject"]
    fatal_accepted = _findings_with(accepted, "fatal")
    minor_accepted = _findings_with(accepted, "minor")
    fatal_rejected = _findings_with(rejected, "fatal")
    minor_rejected = _findings_with(rejected, "minor")
    if error_message is not None:
        error_message = error_message.replace("`", "'")
    result, verdict = _review_report_verdict(
        error_message,
        interrupted,
        oracle_files,
        fatal_accepted,
        minor_accepted,
    )
    findings_by_path: dict[str, int] = {}
    for finding in [*accepted, *rejected]:
        oracle_path = finding_oracle_path(finding, root)
        path_key = None if oracle_path is None else oracle_path_key(root, oracle_path)
        if path_key is None:
            continue
        findings_by_path[path_key] = findings_by_path.get(path_key, 0) + 1
    row_lines: list[str] = []
    for idx, path in enumerate(oracle_files, 1):
        path_key = oracle_path_key(root, path)
        finding_count = findings_by_path.get(path_key, 0) if path_key is not None else 0
        row_lines.append(f"| {idx} | `{path_display(root, path)}` | {finding_count} |")
    rows = "\n".join(row_lines)
    frontmatter = [
        ("command", "oracle review"),
        ("generated_at", timestamp()),
        ("repo_root", root),
        ("scope", scope),
        ("session_branch", session_branch),
        ("session_fork_commit", state.session.session_fork_commit),
        ("run_branch", run_branch),
        ("run_fork_commit", run_fork_commit),
        ("run_join_commit", run_join_commit),
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
            "# cmoc oracle review report",
            "## Verdict",
            verdict,
            "## Evaluated oracle file",
            "| No. | Oracle file | Findings |",
            "|---:|---|---:|",
            rows,
            "## Fatal findings",
            _render_finding_group("Accepted fatal findings", fatal_accepted),
            "## Minor findings",
            _render_ordered_finding_tail(
                minor_accepted,
                fatal_rejected,
                minor_rejected,
            ),
            "",
        ]
    )


def _findings_with(findings: list[dict], severity: str) -> list[dict]:
    """指定した severity の所見だけを report 用に抽出する。

    Args:
        findings: 抽出元の所見。
        severity: 残す所見の severity。
    Returns:
        指定 severity に一致する所見のリスト。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    return [finding for finding in findings if finding.get("severity") == severity]


def _render_finding_group(title: str, findings: list[dict]) -> str:
    """見出し付きの finding group を Markdown 節として描画する。

    Args:
        title: group の Markdown 見出し。
        findings: 節に表示する所見。
    Returns:
        見出しと所見一覧を結合した Markdown。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    return "\n".join([f"### {title}", render_finding_section(findings)])


def _render_ordered_finding_tail(
    minor_accepted: list[dict],
    fatal_rejected: list[dict],
    minor_rejected: list[dict],
) -> str:
    """Minor findings 節内の所見を仕様で定めた順序に並べて描画する。

    Args:
        minor_accepted: 採用された minor 所見。
        fatal_rejected: 不採用となった fatal 所見。
        minor_rejected: 不採用となった minor 所見。
    Returns:
        3 つの finding group を順序どおりに結合した Markdown。

    Fatal/Minor の H2 節順を保ったまま、所見の採否・severity 順を維持する。
    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md は finding detail
    # stream を verdict 順にし、同時に Fatal と Minor の H2 anchor もその順にすることを求める。
    return "\n".join(
        [
            _render_finding_group("Accepted minor findings", minor_accepted),
            _render_finding_group("Rejected fatal findings", fatal_rejected),
            _render_finding_group("Rejected minor findings", minor_rejected),
        ]
    )


def _review_report_verdict(
    error_message: str | None,
    interrupted: bool,
    oracle_files: list[Path],
    fatal_accepted: list[dict],
    minor_accepted: list[dict],
) -> tuple[str, str]:
    """レビュー結果の frontmatter 値と人間向け verdict 文面を決める。

    Args:
        error_message: レビュー中のエラーメッセージ。
        interrupted: ユーザー中断要求で部分結果を確定したか。
        oracle_files: 実際に評価した oracle file。
        fatal_accepted: 採用された fatal 所見。
        minor_accepted: 採用された minor 所見。
    Returns:
        result と本文の verdict を組み合わせた tuple。

    エラー、対象なし、fatal、minor、問題なしの優先順位で判定する。
    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    if error_message is not None:
        return (
            "error",
            f"レビュー処理が途中で失敗しました。\n\nError: `{error_message}`",
        )
    if interrupted:
        return (
            "interrupted",
            "ユーザー中断要求によってレビューを完了しました。"
            "レポートに含まれるのは中断までに確定した部分結果だけであり、"
            "対象範囲のレビュー完了を保証しません。",
        )
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
    """frontmatter の値を report に書ける一行へ整形する。

    Args:
        name: frontmatter 項目名。
        value: 項目値。未知の値は None で表す。
    Returns:
        name: value 形式の frontmatter 行。

    None を YAML の null として出力し、不明な実行情報も項目として保持する。
    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    return f"{name}: {'null' if value is None else value}"


def render_finding_section(findings: list[dict]) -> str:
    """所見リストを report 本文の Markdown 箇条書きへ描画する。

    Args:
        findings: 表示する所見。
    Returns:
        所見が無ければ なし、それ以外は finding ごとの Markdown 行。

    各行に finding ID、判定、タイトル、理由を含める。
    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    if not findings:
        return "なし"
    lines = []
    for finding in findings:
        line = (
            f"- `{finding.get('finding_id')}` [{finding.get('verdict') or 'unjudged'}] "
            f"{finding.get('title')}: {finding.get('reason')}"
        )
        if finding.get("judge_reason"):
            line += f" (judge reason: {finding.get('judge_reason')})"
        lines.append(line)
    return "\n".join(lines)


def path_display(root: Path, path: Path) -> str:
    """report 内の oracle file 表示名を repository-relative key に揃える。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    key = oracle_path_key(root, path)
    if key is not None:
        return key
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = None
    if relative is not None:
        return str(relative)
    return str(path)
