"""`cmoc eval-oracles` の本体処理。"""

from pathlib import Path

from commons.codex import parse_json_object, run_codex_exec
from commons.command_runner import run_command
from commons.indexing import maintain_indexes
from commons.repo import (
    changed_oracle_files,
    current_branch,
    ensure_cmoc_ignored,
    has_deleted_oracle_files,
    head_commit,
    is_cmoc_branch,
    is_session_branch,
    list_oracle_files,
    read_session_start_commit,
)
from commons.timing import StepTimer, start_step
from commons.timestamps import make_timestamp

_SEVERITY_ORDER = ["fatal", "inconclusive", "warning"]
_ISSUE_ID_PREFIXES = {
    "fatal": "FATAL",
    "inconclusive": "INCONCLUSIVE",
    "warning": "WARN",
}
_EVALUATION_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "target_oracle_path",
        "referenced_paths",
        "specification_only_basis",
        "issues",
    ],
    "properties": {
        "target_oracle_path": {
            "type": "string",
            "description": "評価対象 oracle ファイルの絶対パス。",
        },
        "referenced_paths": {
            "type": "array",
            "description": (
                "評価時に参照した oracle / INDEX ファイルの絶対パス。"
                "対象 oracle 自身も含める。"
            ),
            "items": {"type": "string"},
        },
        "specification_only_basis": {
            "type": "string",
            "description": (
                "この評価が oracles 配下の仕様断片と INDEX だけに基づくことの説明。"
            ),
        },
        "issues": {
            "type": "array",
            "description": "評価対象 oracle から検出した問題点。問題がない場合は空配列。",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "severity",
                    "title",
                    "oracle_path",
                    "oracle_line_start",
                    "oracle_line_end",
                    "affected_workflow",
                    "requirement",
                    "problem",
                    "reason",
                    "suggested_oracle_change",
                ],
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": ["fatal", "warning", "inconclusive"],
                        "description": "問題点の分類。",
                    },
                    "title": {
                        "type": "string",
                        "description": "問題点の短い見出し。",
                    },
                    "oracle_path": {
                        "type": "string",
                        "description": (
                            "問題点の根拠となる oracle ファイルの絶対パス。"
                            "通常は target_oracle_path と同じだが、関連 oracle 側に"
                            "問題がある場合はそのファイルを指してよい。"
                        ),
                    },
                    "oracle_line_start": {
                        "type": ["integer", "null"],
                        "description": (
                            "問題点の根拠となる oracle 記述の開始行。"
                            "特定できない場合は null。"
                        ),
                    },
                    "oracle_line_end": {
                        "type": ["integer", "null"],
                        "description": (
                            "問題点の根拠となる oracle 記述の終了行。"
                            "特定できない場合は null。"
                        ),
                    },
                    "affected_workflow": {
                        "type": "string",
                        "description": (
                            "影響を受ける workflow / subcommand / concept。"
                            "例: cmoc apply, cmoc eval-oracles, overall。"
                        ),
                    },
                    "requirement": {
                        "type": "string",
                        "description": "oracle が要求している、または要求すべき仕様。",
                    },
                    "problem": {
                        "type": "string",
                        "description": "仕様上の問題点。",
                    },
                    "reason": {
                        "type": "string",
                        "description": (
                            "なぜその severity と判断したのか。fatal の場合は"
                            "致命的問題の定義との対応を明示する。"
                        ),
                    },
                    "suggested_oracle_change": {
                        "type": "string",
                        "description": "oracle をどう修正すべきか。",
                    },
                },
            },
        },
    },
}


def cmoc_eval_oracles_impl(
    repo_root: Path | None = None,
    *,
    full: bool,
) -> None:
    """oracle 断片を Codex CLI で評価し、レポートを作る。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_eval_oracles_impl(
                resolved_repo_root,
                full=full,
            )
        )
        return

    timer = StepTimer("eval-oracles")
    mode = None
    branch_name = None
    cmoc_branch = None
    base_commit = None
    commit_hash = None
    deleted_oracles = None
    all_oracle_files: list[Path] = []
    all_oracle_files_known = False
    oracle_files: list[Path] = []
    evaluations = []
    failed_stage = "initialize eval-oracles"
    try:
        # 評価前に `.cmoc` の ignore 保証を済ませる。
        failed_stage = "ensure .cmoc is ignored"
        start_step(timer, 1, 5, "ensure .cmoc is ignored")
        ensure_cmoc_ignored(repo_root)

        # 既存のユーザー向けステップとして INDEX.md メンテナンスを実行する。
        failed_stage = "maintain INDEX.md files"
        start_step(timer, 2, 5, "maintain INDEX.md files")
        maintain_indexes(repo_root)

        # branch 状態と `--full` だけから、部分評価か全体評価かを決める。
        failed_stage = "select oracle files"
        start_step(timer, 3, 5, "select oracle files")
        branch_name = current_branch(repo_root)
        cmoc_branch = is_cmoc_branch(branch_name)
        session_branch = is_session_branch(branch_name)
        partial = session_branch and not full
        mode = "partial" if partial else "full"
        if session_branch:
            base_commit = read_session_start_commit(repo_root, branch_name)
            deleted_oracles = has_deleted_oracle_files(repo_root, base_commit)
        else:
            deleted_oracles = False

        # 評価モードに応じて Codex CLI に渡す oracle ファイル一覧を作る。
        all_oracle_files = list_oracle_files(repo_root)
        all_oracle_files_known = True
        if partial:
            assert base_commit is not None
            changed_files = set(changed_oracle_files(repo_root, base_commit))
            oracle_files = [
                path for path in all_oracle_files if path in changed_files
            ]
        else:
            oracle_files = all_oracle_files
        commit_hash = head_commit(repo_root)

        # oracle ファイルごとに Codex CLI 評価を実行する。
        failed_stage = "oracle ファイル評価"
        start_step(timer, 4, 5, "oracle ファイル評価")
        for index, oracle_file in enumerate(oracle_files, start=1):
            print(
                f"oracle 評価 ({index}/{len(oracle_files)}) "
                f"{oracle_file}"
            )
            payload = parse_json_object(
                run_codex_exec(
                    repo_root,
                    _evaluation_prompt(repo_root, oracle_file),
                    purpose=(
                        f"oracle 評価 {oracle_file.relative_to(repo_root)}"
                    ),
                    read_only=True,
                    expect_json=True,
                    output_schema=_EVALUATION_OUTPUT_SCHEMA,
                    json_validator=lambda value, current_oracle=oracle_file: (
                        _validate_evaluation_payload(
                            value,
                            repo_root,
                            current_oracle,
                        )
                    ),
                )
            )
            evaluations.append(payload)

        # 評価結果を 1 つの Markdown レポートとして保存する。
        failed_stage = "write report"
        start_step(timer, 5, 5, "write report")
        report_path = _write_report(
            repo_root,
            mode,
            full,
            branch_name,
            cmoc_branch,
            base_commit,
            commit_hash,
            deleted_oracles,
            len(all_oracle_files),
            oracle_files,
            evaluations,
        )
    except Exception as error:
        report_path = _write_error_report(
            repo_root,
            mode,
            full,
            branch_name,
            cmoc_branch,
            base_commit,
            commit_hash,
            deleted_oracles,
            len(all_oracle_files) if all_oracle_files_known else None,
            oracle_files,
            evaluations,
            failed_stage,
            error,
        )
        print(str(report_path))
        raise
    print(str(report_path))
    timer.report()


def _evaluation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """oracle 評価用 prompt を組み立てる。"""
    # Codex CLI には prompt だけで解釈できる具体的な絶対パスを渡す。
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_file = oracle_file.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    concrete_oracle_index = (concrete_oracle_root / "INDEX.md").resolve()

    # 仕様の構成順序に従い、完了条件を詳細指示より前に置く。
    return "\n".join(
        [
            "あなたはソフトウェア仕様のレビュー担当です。",
            f"`{concrete_repo_root}` 内の oracle ファイル "
            f"`{concrete_oracle_file}` を評価してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "target_oracle_path には評価対象 oracle ファイルの絶対パスを返してください。",
            "referenced_paths には参照した oracle / INDEX ファイルの絶対パスをすべて返し、",
            "対象 oracle 自身も必ず含めてください。",
            "specification_only_basis には、評価が oracles 配下の仕様断片と INDEX だけに",
            "基づくことの説明を書いてください。",
            "issues には検出した問題点を入れ、問題がない場合は空配列を返してください。",
            "対象 oracle、関連する oracle ファイル、関連判断に必要な",
            f"`{concrete_oracle_root}` 配下の INDEX.md だけを読んでください。",
            f"`{concrete_oracle_index}` から始まる INDEX.md の Summary /",
            "Read this when / Do not read this when を根拠に、",
            "関連 oracle を選定してください。",
            f"`{concrete_oracle_root}` 外のファイルは一切参照禁止です。",
            "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。",
            "致命的な問題とは、実装を参照せずに仕様だけから判断・実装したとき、",
            "主要ワークフローを壊す、完了判定を妨げる、または中核目的を",
            "満たしたと判断できなくする問題です。",
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _validate_evaluation_payload(
    value: object,
    repo_root: Path,
    oracle_file: Path,
) -> None:
    """oracle 評価 Structured Output の schema と意味制約を検査する。"""
    # run_codex_exec の schema 検査に加え、Python 側でも後段で扱う型を保証する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    expected_keys = {
        "target_oracle_path",
        "referenced_paths",
        "specification_only_basis",
        "issues",
    }
    if set(value) != expected_keys:
        raise ValueError("Evaluation payload keys do not match schema.")

    target_path = _require_absolute_oracle_path(
        value["target_oracle_path"],
        repo_root,
        "target_oracle_path",
    )
    if target_path != oracle_file.resolve():
        raise ValueError("target_oracle_path does not match evaluated file.")

    referenced_paths = _validate_referenced_paths(
        value["referenced_paths"],
        repo_root,
    )
    if target_path not in referenced_paths:
        raise ValueError("referenced_paths must include target_oracle_path.")

    if not isinstance(value["specification_only_basis"], str):
        raise ValueError("specification_only_basis must be a string.")
    _validate_evaluation_issues(value["issues"], repo_root)


def _write_report(
    repo_root: Path,
    mode: str,
    full_requested: bool,
    branch_name: str,
    cmoc_branch: bool,
    base_commit: str | None,
    commit_hash: str,
    deleted_oracles: bool,
    oracle_count_total: int,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
) -> Path:
    """評価結果を `.cmoc/reports/eval-oracles` に保存する。"""
    # 保存先ディレクトリと timestamp 付きレポートパスを用意する。
    report_dir = repo_root / ".cmoc" / "reports" / "eval-oracles"
    report_dir.mkdir(parents=True, exist_ok=True)
    generated_at = make_timestamp()
    report_path = report_dir / f"{generated_at}.md"
    issue_counts = _issue_counts(evaluations)
    result = _evaluation_result(len(oracle_files), issue_counts)

    # frontmatter と問題点単位の本文を結合する。
    lines = [
        "---",
        "schema_version: 1",
        "command: cmoc eval-oracles",
        f"generated_at: {generated_at}",
        f"repo_root: {repo_root.resolve()}",
        f"oracle_root: {(repo_root / 'oracles').resolve()}",
        f"mode: {mode}",
        f"full_requested: {str(full_requested).lower()}",
        f"branch: {branch_name}",
        f"is_cmoc_branch: {str(cmoc_branch).lower()}",
        f"base_commit: {_yaml_nullable(base_commit)}",
        f"head_commit: {commit_hash}",
        f"commit: {commit_hash}",
        f"deleted_oracles_detected: {str(deleted_oracles).lower()}",
        f"oracle_count_total: {oracle_count_total}",
        f"oracle_count_evaluated: {len(oracle_files)}",
        f"oracle_count: {len(oracle_files)}",
        f"fatal_issue_count: {issue_counts['fatal']}",
        f"warning_issue_count: {issue_counts['warning']}",
        f"inconclusive_issue_count: {issue_counts['inconclusive']}",
        f"result: {result}",
        "---",
        "",
        "# cmoc eval-oracles report",
        "",
        "## Summary",
        "",
        f"- Result: `{result}`",
        f"- Mode: `{mode}`",
        f"- Evaluated oracle files: `{len(oracle_files)}`",
        f"- Fatal issues: `{issue_counts['fatal']}`",
        f"- Inconclusive issues: `{issue_counts['inconclusive']}`",
        f"- Warning issues: `{issue_counts['warning']}`",
        "",
        "## Verdict",
        "",
        _verdict_text(result),
        "",
        "## Specification-only basis",
        "",
        *_specification_only_basis_lines(repo_root, evaluations),
        "",
        "## Evaluated oracle files",
        "",
        "| No. | Oracle file | Issues |",
        "|---:|---|---:|",
    ]
    issue_count_by_target = _issue_count_by_target(evaluations)
    for index, oracle_file in enumerate(oracle_files, start=1):
        target = str(oracle_file.resolve())
        lines.append(
            f"| {index} | `{oracle_file.relative_to(repo_root)}` | "
            f"{issue_count_by_target.get(target, 0)} |"
        )
    lines.extend([""])
    for severity, heading in [
        ("fatal", "## Fatal issues"),
        ("inconclusive", "## Inconclusive issues"),
        ("warning", "## Warnings"),
    ]:
        lines.extend([heading, ""])
        issues = _issues_for_severity(evaluations, severity)
        if not issues:
            lines.extend(["No issues.", ""])
            continue
        for issue_id, issue in _numbered_issues(severity, issues):
            lines.extend(_issue_lines(repo_root, issue_id, issue))
    lines.extend(["## Referenced files", ""])
    referenced_path_rows = _referenced_path_rows(repo_root, evaluations)
    if referenced_path_rows:
        lines.extend(
            [
                "| No. | Referenced file |",
                "|---:|---|",
            ]
        )
        lines.extend(referenced_path_rows)
    else:
        lines.append("No referenced files.")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _write_error_report(
    repo_root: Path,
    mode: str | None,
    full_requested: bool,
    branch_name: str | None,
    cmoc_branch: bool | None,
    base_commit: str | None,
    commit_hash: str | None,
    deleted_oracles: bool | None,
    oracle_count_total: int | None,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
    failed_stage: str,
    error: Exception,
) -> Path:
    """評価処理失敗時の `result: error` レポートを best effort で保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / "eval-oracles"
    report_dir.mkdir(parents=True, exist_ok=True)
    generated_at = make_timestamp()
    report_path = report_dir / f"{generated_at}.md"
    issue_counts = _issue_counts(evaluations)
    result = "error"
    lines = [
        "---",
        "schema_version: 1",
        "command: cmoc eval-oracles",
        f"generated_at: {generated_at}",
        f"repo_root: {repo_root.resolve()}",
        f"oracle_root: {(repo_root / 'oracles').resolve()}",
        f"mode: {mode or 'unknown'}",
        f"full_requested: {str(full_requested).lower()}",
        f"branch: {_yaml_nullable(branch_name)}",
        f"is_cmoc_branch: {_yaml_bool_nullable(cmoc_branch)}",
        f"base_commit: {_yaml_nullable(base_commit)}",
        f"head_commit: {_yaml_nullable(commit_hash)}",
        f"commit: {_yaml_nullable(commit_hash)}",
        f"deleted_oracles_detected: {_yaml_bool_nullable(deleted_oracles)}",
        f"oracle_count_total: {_yaml_int_nullable(oracle_count_total)}",
        f"oracle_count_evaluated: {len(evaluations)}",
        f"oracle_count: {len(evaluations)}",
        f"fatal_issue_count: {issue_counts['fatal']}",
        f"warning_issue_count: {issue_counts['warning']}",
        f"inconclusive_issue_count: {issue_counts['inconclusive']}",
        f"result: {result}",
        "---",
        "",
        "# cmoc eval-oracles report",
        "",
        "## Summary",
        "",
        f"- Result: `{result}`",
        f"- Mode: `{mode or 'unknown'}`",
        f"- Evaluated oracle files: `{len(evaluations)}`",
        f"- Requested oracle files: `{len(oracle_files)}`",
        f"- Fatal issues: `{issue_counts['fatal']}`",
        f"- Inconclusive issues: `{issue_counts['inconclusive']}`",
        f"- Warning issues: `{issue_counts['warning']}`",
        f"- Failed stage: `{failed_stage}`",
        f"- Exception type: `{type(error).__name__}`",
        f"- Exception message: `{str(error)}`",
        "",
        "## Verdict",
        "",
        _verdict_text(result),
        "",
        f"Failed stage: `{failed_stage}`",
        "",
        f"Exception: `{type(error).__name__}: {str(error)}`",
        "",
        "## Specification-only basis",
        "",
        *_specification_only_basis_lines(repo_root, evaluations),
        "",
        "## Evaluated oracle files",
        "",
        "| No. | Oracle file | Issues |",
        "|---:|---|---:|",
    ]
    issue_count_by_target = _issue_count_by_target(evaluations)
    evaluated_files = _evaluated_oracle_files(evaluations)
    for index, oracle_file in enumerate(evaluated_files, start=1):
        target = str(oracle_file)
        lines.append(
            f"| {index} | `{_display_path(repo_root, str(oracle_file))}` | "
            f"{issue_count_by_target.get(target, 0)} |"
        )
    if not evaluated_files:
        lines.append("| - | No completed evaluations. | - |")
    not_evaluated_files = _not_evaluated_oracle_files(
        repo_root,
        oracle_files,
        evaluations,
    )
    lines.extend(["", "Not evaluated oracle files:", ""])
    if not_evaluated_files:
        for index, oracle_file in enumerate(not_evaluated_files, start=1):
            lines.append(
                f"{index}. `{_display_path(repo_root, str(oracle_file))}`"
            )
    else:
        lines.append("No requested oracle files remained unevaluated.")
    lines.extend([""])
    for severity, heading in [
        ("fatal", "## Fatal issues"),
        ("inconclusive", "## Inconclusive issues"),
        ("warning", "## Warnings"),
    ]:
        lines.extend([heading, ""])
        issues = _issues_for_severity(evaluations, severity)
        if not issues:
            lines.extend(["No issues.", ""])
            continue
        for issue_id, issue in _numbered_issues(severity, issues):
            lines.extend(_issue_lines(repo_root, issue_id, issue))
    lines.extend(["## Referenced files", ""])
    referenced_path_rows = _referenced_path_rows(repo_root, evaluations)
    if referenced_path_rows:
        lines.extend(
            [
                "| No. | Referenced file |",
                "|---:|---|",
            ]
        )
        lines.extend(referenced_path_rows)
    else:
        lines.append("No referenced files.")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _validate_referenced_paths(value: object, repo_root: Path) -> set[Path]:
    """referenced_paths を絶対 oracle / INDEX ファイル配列として検査する。"""
    if not isinstance(value, list):
        raise ValueError("referenced_paths must be a list.")
    paths = set()
    for index, item in enumerate(value):
        paths.add(
            _require_absolute_oracle_path(
                item,
                repo_root,
                f"referenced_paths[{index}]",
            )
        )
    return paths


def _validate_evaluation_issues(value: object, repo_root: Path) -> None:
    """issues 配列の item schema を検査する。"""
    if not isinstance(value, list):
        raise ValueError("issues must be a list.")
    required_keys = {
        "severity",
        "title",
        "oracle_path",
        "oracle_line_start",
        "oracle_line_end",
        "affected_workflow",
        "requirement",
        "problem",
        "reason",
        "suggested_oracle_change",
    }
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"issues[{index}] must be an object.")
        if set(item) != required_keys:
            raise ValueError(f"issues[{index}] keys do not match schema.")
        if item["severity"] not in _SEVERITY_ORDER:
            raise ValueError(f"issues[{index}].severity is invalid.")
        _require_issue_string(item, "title", index)
        _require_absolute_oracle_path(
            item["oracle_path"],
            repo_root,
            f"issues[{index}].oracle_path",
        )
        _validate_issue_lines(item, index)
        for key in [
            "affected_workflow",
            "requirement",
            "problem",
            "reason",
            "suggested_oracle_change",
        ]:
            _require_issue_string(item, key, index)


def _require_absolute_oracle_path(
    value: object,
    repo_root: Path,
    label: str,
) -> Path:
    """JSON 値を参照可能な oracle / INDEX ファイル path として検査する。"""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string.")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"{label} must be an absolute path.")
    resolved_path = path.resolve()
    oracle_root = (repo_root / "oracles").resolve()
    try:
        resolved_path.relative_to(oracle_root)
    except ValueError as error:
        raise ValueError(f"{label} must be under oracles.") from error
    if not resolved_path.exists():
        raise ValueError(f"{label} must exist.")
    if not resolved_path.is_file():
        raise ValueError(f"{label} must be a file.")
    if resolved_path.name == "INDEX.md":
        return resolved_path

    oracle_files = {path.resolve() for path in list_oracle_files(repo_root)}
    if resolved_path not in oracle_files:
        raise ValueError(f"{label} must be an oracle file or INDEX.md.")
    return resolved_path


def _require_issue_string(
    item: dict[object, object],
    key: str,
    index: int,
) -> None:
    """issue item の string 項目を検査する。"""
    if not isinstance(item[key], str):
        raise ValueError(f"issues[{index}].{key} must be a string.")


def _validate_issue_lines(item: dict[object, object], index: int) -> None:
    """issue item の行番号項目を検査する。"""
    start = item["oracle_line_start"]
    end = item["oracle_line_end"]
    if start is not None and not isinstance(start, int):
        raise ValueError(f"issues[{index}].oracle_line_start is invalid.")
    if end is not None and not isinstance(end, int):
        raise ValueError(f"issues[{index}].oracle_line_end is invalid.")
    if isinstance(start, int) and isinstance(end, int) and start > end:
        raise ValueError(f"issues[{index}] line range is invalid.")


def _issue_counts(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """severity ごとの issue 件数を数える。"""
    counts = {severity: 0 for severity in _SEVERITY_ORDER}
    for issue in _all_issues(evaluations):
        severity = str(issue["severity"])
        counts[severity] += 1
    return counts


def _evaluation_result(
    oracle_count: int,
    issue_counts: dict[str, int],
) -> str:
    """issue 件数からレポート result を決める。"""
    if oracle_count == 0:
        return "no_targets"
    for severity in _SEVERITY_ORDER:
        if issue_counts[severity] > 0:
            return severity
    return "ok"


def _verdict_text(result: str) -> str:
    """result ごとの Verdict 本文を返す。"""
    if result == "ok":
        return (
            "今回評価した範囲では問題点が検出されませんでした。"
            "ただし、問題点の不存在を完全保証するものではありません。"
        )
    if result == "fatal":
        return (
            "oracle スナップショットには、仕様だけから判断して主要ワークフロー、"
            "完了判定、または中核目的を壊しうる問題があります。"
        )
    if result == "inconclusive":
        return "致命的問題ありとは断定できませんが、仕様評価として判断不能な点があります。"
    if result == "warning":
        return "致命的ではありませんが、仕様品質・可読性・将来の実装安定性に問題があります。"
    if result == "no_targets":
        return "評価対象 oracle が 0 件だったため、問題点の評価は行われませんでした。"
    if result == "error":
        return (
            "評価処理またはレポート生成に失敗したため、成功評価ではありません。"
            "ログと例外情報を確認し、必要な修正または再実行を判断してください。"
        )
    return (
        "未知の result のため、評価状態を成功として扱えません。"
        "ログとレポート生成処理を確認してください。"
    )


def _issue_count_by_target(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """評価対象ファイルごとの issue 件数を返す。"""
    result = {}
    for evaluation in evaluations:
        issues = _evaluation_issues(evaluation)
        target = Path(str(evaluation["target_oracle_path"])).resolve()
        result[str(target)] = len(issues)
    return result


def _evaluated_oracle_files(evaluations: list[dict[str, object]]) -> list[Path]:
    """完了した評価結果に含まれる対象 oracle ファイルを返す。"""
    return [
        Path(str(evaluation["target_oracle_path"])).resolve()
        for evaluation in evaluations
    ]


def _not_evaluated_oracle_files(
    repo_root: Path,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
) -> list[Path]:
    """依頼対象のうち評価完了していない oracle ファイルを返す。"""
    evaluated = set(_evaluated_oracle_files(evaluations))
    return [
        oracle_file.resolve()
        for oracle_file in oracle_files
        if oracle_file.resolve() not in evaluated
    ]


def _issues_for_severity(
    evaluations: list[dict[str, object]],
    severity: str,
) -> list[dict[str, object]]:
    """指定 severity の issue を評価順・issue 順で返す。"""
    return [
        issue
        for issue in _all_issues(evaluations)
        if issue["severity"] == severity
    ]


def _numbered_issues(
    severity: str,
    issues: list[dict[str, object]],
) -> list[tuple[str, dict[str, object]]]:
    """severity ごとに report-local id を付ける。"""
    prefix = _ISSUE_ID_PREFIXES[severity]
    return [
        (f"{prefix}-{index:03d}", issue)
        for index, issue in enumerate(issues, start=1)
    ]


def _specification_only_basis_lines(
    repo_root: Path,
    evaluations: list[dict[str, object]],
) -> list[str]:
    """評価ごとの specification_only_basis を Markdown 行へ変換する。"""
    if not evaluations:
        return ["No completed evaluations."]
    lines = [
        "| No. | Oracle file | Basis |",
        "|---:|---|---|",
    ]
    for index, evaluation in enumerate(evaluations, start=1):
        target = str(evaluation["target_oracle_path"])
        basis = _markdown_table_cell(
            str(evaluation["specification_only_basis"])
        )
        lines.append(
            f"| {index} | `{_display_path(repo_root, target)}` | {basis} |"
        )
    return lines


def _markdown_table_cell(value: str) -> str:
    """Markdown table cell に入れる自由文を 1 行へ整形する。"""
    return " ".join(value.splitlines()).replace("|", "\\|")


def _issue_lines(
    repo_root: Path,
    issue_id: str,
    issue: dict[str, object],
) -> list[str]:
    """issue 1 件を Markdown 行へ変換する。"""
    return [
        f"### {issue_id}: {issue['title']}",
        "",
        f"- Oracle file: `{_display_path(repo_root, str(issue['oracle_path']))}`",
        f"- Lines: `{_line_range(issue)}`",
        f"- Affected workflow: `{issue['affected_workflow']}`",
        "- Requirement:",
        f"  - {issue['requirement']}",
        "- Problem:",
        f"  - {issue['problem']}",
        "- Reason:",
        f"  - {issue['reason']}",
        "- Suggested oracle change:",
        f"  - {issue['suggested_oracle_change']}",
        "",
    ]


def _line_range(issue: dict[str, object]) -> str:
    """issue の行範囲を Markdown 表示用文字列にする。"""
    start = issue["oracle_line_start"]
    end = issue["oracle_line_end"]
    if start is None or end is None:
        return "unknown"
    if start == end:
        return str(start)
    return f"{start}-{end}"


def _referenced_path_rows(
    repo_root: Path,
    evaluations: list[dict[str, object]],
) -> list[str]:
    """全評価結果の referenced_paths を重複排除した表示行を返す。"""
    referenced_paths = _unique_strings(
        [
            path
            for evaluation in evaluations
            for path in _string_list(evaluation["referenced_paths"])
        ]
    )
    result = []
    for index, path in enumerate(referenced_paths, start=1):
        result.append(
            f"| {index} | `{_display_path(repo_root, path)}` |"
        )
    return result


def _all_issues(
    evaluations: list[dict[str, object]],
) -> list[dict[str, object]]:
    """全評価結果の issues を評価順に連結する。"""
    result = []
    for evaluation in evaluations:
        result.extend(_evaluation_issues(evaluation))
    return result


def _evaluation_issues(
    evaluation: dict[str, object],
) -> list[dict[str, object]]:
    """検証済み evaluation から issues を取り出す。"""
    issues = evaluation["issues"]
    if not isinstance(issues, list):
        raise ValueError("issues must be a list.")
    return [issue for issue in issues if isinstance(issue, dict)]


def _string_list(value: object) -> list[str]:
    """JSON 値を文字列配列として検査する。"""
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("Expected list[str].")
    return value


def _yaml_nullable(value: str | None) -> str:
    """YAML frontmatter 用に nullable scalar を返す。"""
    if value is None:
        return "null"
    return value


def _yaml_bool_nullable(value: bool | None) -> str:
    """YAML frontmatter 用に nullable bool を返す。"""
    if value is None:
        return "null"
    return str(value).lower()


def _yaml_int_nullable(value: int | None) -> str:
    """YAML frontmatter 用に nullable int を返す。"""
    if value is None:
        return "null"
    return str(value)


def _unique_strings(values: list[str]) -> list[str]:
    """文字列配列を順序維持で重複排除する。"""
    result = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _display_path(repo_root: Path, path_text: str) -> str:
    """repo 配下の絶対パスをレポート向けの相対パスにする。"""
    path = Path(path_text)
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path_text
