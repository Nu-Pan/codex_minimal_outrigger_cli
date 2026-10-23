"""editing run の人間向け Markdown report。

共通処理の canonical な配置は {{work-root}}/spec/dev_rule/design_rule.md
に従っている。
"""

import json
import re
from dataclasses import replace
from pathlib import Path

from .runtime_logging import current_execution_id, current_subcommand_logger
from .runtime_paths import (
    reports_dir,
    timestamp,
)
from .runtime_primary_report import (
    current_primary_report_fields,
    prepare_primary_report,
    rewrite_primary_report,
    write_reserved_primary_report,
)
from .runtime_primary_report_render import (
    execution_step_lines,
    observation_count_notice,
    related_log_lines,
)
from .runtime_primary_report_specs import TerminalClassification
from .runtime_report_markdown import (
    ReportSummary,
    inline_code,
    markdown_sections,
    terminal_outcome,
    yaml_scalar,
)
from .runtime_run_lifecycle import EditingRunContext


def write_workload_report(
    context: EditingRunContext,
    command_path: str,
    *,
    summary: ReportSummary,
    state_after: str,
    completion_reason: str,
    changed_paths: list[str] | None,
    codex_returncode: int | None = None,
    extra_fields: dict[str, object] | None = None,
    body_lines: list[str] | None = None,
    report_path: Path | None = None,
) -> Path:
    """workload の成果と終了処理を同じ invocation の report に保存する。"""
    directory = reports_dir(context.repo, command_path)
    directory.mkdir(parents=True, exist_ok=True)
    generated_at = timestamp()
    execution_id = current_execution_id(context.repo)
    path = report_path or directory / f"{execution_id}.md"
    if report_path is None:
        path.open("x").close()
    terminal_classification: TerminalClassification = (
        "error"
        if completion_reason == "error"
        else (
            "user_interruption"
            if completion_reason == "user_interruption"
            else "natural_completion"
        )
    )
    fields: list[tuple[str, object]] = [
        ("command", f"cmoc {command_path.replace('/', ' ')}"),
        ("execution_id", execution_id),
        ("repo_root", context.repo.resolve()),
        ("terminal_classification", terminal_classification),
        ("exit_code", 1 if completion_reason == "error" else 0),
        ("run_kind", context.kind),
        ("session_branch", context.session_branch),
        ("session_fork_commit", context.session_fork_commit),
        ("run_branch", context.run_branch),
        ("run_fork_commit", context.run_fork_commit),
        ("run_worktree", context.run_worktree),
        ("state_before", context.state_before),
        ("state_after", state_after),
        ("generated_at", generated_at),
        ("completion_reason", completion_reason),
        ("codex_returncode", codex_returncode),
    ]
    fields.extend((extra_fields or {}).items())
    fields = list(
        {
            **dict(fields),
            **current_primary_report_fields(),
            "state_after": state_after,
            "completion_reason": completion_reason,
        }.items()
    )
    if state_after != "ready" and completion_reason != "error":
        # 結果保存後に行う state 初期化・cleanup の成功を先取りしない。
        fields = [
            (name, None if name in {"terminal_classification", "exit_code"} else value)
            for name, value in fields
        ]
        summary = replace(
            summary,
            outcome="取り込み後の終了処理は未完了です。state 初期化と cleanup の結果を確認してください。",
        )
    observation_count = (extra_fields or {}).get("feedback_observation_count")
    if isinstance(observation_count, int) and observation_count > 0:
        summary = replace(
            summary,
            attention=(
                *summary.attention,
                observation_count_notice(observation_count),
            ),
        )
    changed = (
        [_render_changed_path(item) for item in changed_paths] or ["- none"]
        if changed_paths is not None
        else ["- unavailable"]
    )
    logger = current_subcommand_logger()
    if logger is not None:
        fields.append(("subcommand_log_path", str(logger.path.resolve())))
    execution = (
        execution_step_lines(logger, terminal_classification)
        if logger is not None
        else ["- unavailable"]
    )
    related_logs = (
        related_log_lines(logger) if logger is not None else ["- unavailable"]
    )
    content = [
        "## Completion",
        completion_reason,
        "## Changed paths",
        *changed,
        *(body_lines or []),
        "## Execution stages",
        *execution,
        "## Related logs",
        *related_logs,
        "",
    ]
    writer = (
        write_reserved_primary_report if report_path is None else rewrite_primary_report
    )
    writer(
        path,
        prepare_primary_report(
            path,
            f"cmoc {context.kind.replace('_', ' ')} report",
            dict(fields),
            summary,
            markdown_sections(content),
        ),
    )
    return path.resolve()


def write_lifecycle_report(
    context: EditingRunContext,
    operation: str,
    *,
    state_after: str,
    warnings: list[str],
    details: dict[str, object],
    terminal_classification: TerminalClassification = "natural_completion",
    exit_code: int = 0,
    report_path: Path | None = None,
) -> Path:
    """run join/abandon の共通情報と cleanup 結果を保存する。"""
    if report_path is None:
        directory = reports_dir(context.repo, f"run/{operation}")
        directory.mkdir(parents=True, exist_ok=True)
        generated_at = timestamp()
        execution_id = current_execution_id(context.repo)
        target_path = directory / f"{execution_id}.md"
        target_path.open("x").close()
        new_report = True
    else:
        generated_at = timestamp()
        target_path = report_path
        execution_id = current_execution_id(context.repo)
        new_report = False
    fields: list[tuple[str, object]] = [
        ("command", f"cmoc run {operation}"),
        ("execution_id", execution_id),
        ("repo_root", context.repo.resolve()),
        ("terminal_classification", terminal_classification),
        ("exit_code", exit_code),
        ("operation", operation),
        ("run_kind", context.kind),
        ("session_branch", context.session_branch),
        ("session_fork_commit", context.session_fork_commit),
        ("run_branch", context.run_branch),
        ("run_fork_commit", context.run_fork_commit),
        ("run_worktree", context.run_worktree),
        ("state_before", context.state_before),
        ("state_after", state_after),
        ("generated_at", generated_at),
    ]
    # detail の YAML 表現は実行情報と本文で共有する。
    detail_fields = [f"{name}: {yaml_scalar(value)}" for name, value in details.items()]
    fields.extend(details.items())
    pending = (
        operation == "join"
        and state_after != "ready"
        and terminal_classification != "error"
    )
    if pending:
        fields = [
            (name, None if name in {"terminal_classification", "exit_code"} else value)
            for name, value in fields
        ]
    logger = current_subcommand_logger()
    if logger is not None:
        fields.append(("subcommand_log_path", str(logger.path.resolve())))
    execution = (
        execution_step_lines(logger, terminal_classification)
        if logger is not None
        else ["- unavailable"]
    )
    related_logs = (
        related_log_lines(logger) if logger is not None else ["- unavailable"]
    )
    resolution = details.get("conflict_resolution")
    if operation == "join":
        serialized = json.dumps(
            resolution or {"agent_status": "not_needed"}, ensure_ascii=False, indent=2
        )
        fence = "`" * max(
            3, 1 + max((len(run) for run in re.findall(r"`+", serialized)), default=0)
        )
        resolution_lines = ["## Conflict resolution", fence + "json", serialized, fence]
    else:
        resolution_lines = []
    attention = [*warnings, *([str(details["error"])] if details.get("error") else [])]
    if details.get("cleanup") != "completed":
        attention.append(f"cleanup: {details.get('cleanup', '未確認')}")
    if details.get("unexpected_paths"):
        attention.append(f"想定外差分: {details['unexpected_paths']}")
    summary = ReportSummary(
        (
            "取り込み後の終了処理は未完了です。"
            if pending
            else terminal_outcome(terminal_classification)
        ),
        (
            f"run state: {context.state_before} → {state_after}",
            *(
                f"{name}: {details[name]}"
                for name in (
                    "run_join_commit",
                    "post_join_hook",
                    "process_stop",
                    "cleanup",
                )
                if name in details
            ),
        ),
        tuple(attention),
        (
            (
                "エラーと残存資源を確認し、run の join または abandon を判断してください。",
            )
            if terminal_classification == "error" or state_after != "ready"
            else ()
        ),
    )
    content = prepare_primary_report(
        target_path,
        f"cmoc run {operation} report",
        dict(fields),
        summary,
        markdown_sections(
            [
                "## Outcome",
                "finalizing" if pending else terminal_classification,
                "## Details",
                *([f"- {field}" for field in detail_fields] or ["- none"]),
                "## Warnings",
                *([f"- {warning}" for warning in warnings] or ["- none"]),
                *resolution_lines,
                "## Execution stages",
                *execution,
                "## Related logs",
                *related_logs,
                "",
            ]
        ),
    )
    if new_report:
        write_reserved_primary_report(target_path, content)
    else:
        rewrite_primary_report(target_path, content)
    return target_path.resolve()


def _render_changed_path(path: str, indent: str = "", label: str = "") -> str:
    """Git path を report の Markdown 箇条書きとして安全に描画する。

    Git path には Markdown の code span 境界や行構造を壊す文字を含められる。
    根拠: {{work-root}}/spec/app_spec/sub_command/editing_run.md
    """
    # 改行を持つ path だけ JSON 文字列で区別し、他の記号はそのまま残す。
    value = (
        json.dumps(path, ensure_ascii=False) if "\r" in path or "\n" in path else path
    )
    return f"{indent}- {label}{inline_code(value)}"
