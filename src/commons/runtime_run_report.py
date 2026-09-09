"""editing run の Markdown + YAML Front Matter report。

共通処理の canonical な配置は {{work-root}}/oracle/doc/dev_rule/design_rule.md
に従っている。
"""

import html
from pathlib import Path

from .runtime_logging import current_subcommand_logger
from .runtime_paths import (
    _reserve_timestamped_path,
    reports_dir,
    timestamp,
)
from .runtime_primary_report import write_reserved_primary_report
from .runtime_primary_report_render import (
    execution_step_lines,
    related_log_lines,
    yaml_scalar,
)
from .runtime_primary_report_specs import TerminalClassification
from .runtime_run_lifecycle import EditingRunContext


def write_fork_report(
    context: EditingRunContext,
    command_path: str,
    *,
    state_after: str,
    completion_reason: str,
    changed_paths: list[str],
    codex_returncode: int | None = None,
    extra_fields: dict[str, object] | None = None,
    body_lines: list[str] | None = None,
) -> Path:
    """workload 共通項目を持つ fork report を保存する。"""
    directory = reports_dir(context.repo, command_path)
    directory.mkdir(parents=True, exist_ok=True)
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # report を書き始める前に path を予約し、同一 timestamp の run report を
    # 別 run が上書きしないようにする。
    generated_at, path = _reserve_timestamped_path(directory, ".md", timestamp)
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
    changed = [_render_changed_path(item) for item in changed_paths] or ["- none"]
    logger = current_subcommand_logger()
    execution = (
        execution_step_lines(logger, terminal_classification)
        if logger is not None
        else ["- unavailable"]
    )
    related_logs = (
        related_log_lines(logger) if logger is not None else ["- unavailable"]
    )
    content = [
        "---",
        *[f"{name}: {yaml_scalar(value)}" for name, value in fields],
        "---",
        f"# cmoc {context.kind.replace('_', ' ')} fork report",
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
    write_reserved_primary_report(path, "\n".join(content))
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
) -> Path:
    """run join/abandon の共通情報と cleanup 結果を保存する。"""
    directory = reports_dir(context.repo, f"run/{operation}")
    directory.mkdir(parents=True, exist_ok=True)
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # report を書き始める前に path を予約し、同一 timestamp の run report を
    # 別 run が上書きしないようにする。
    generated_at, report_path = _reserve_timestamped_path(directory, ".md", timestamp)
    fields: list[tuple[str, object]] = [
        ("command", f"cmoc run {operation}"),
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
        *details.items(),
    ]
    logger = current_subcommand_logger()
    execution = (
        execution_step_lines(logger, terminal_classification)
        if logger is not None
        else ["- unavailable"]
    )
    related_logs = (
        related_log_lines(logger) if logger is not None else ["- unavailable"]
    )
    content = "\n".join(
        [
            "---",
            *[f"{name}: {yaml_scalar(value)}" for name, value in fields],
            "---",
            f"# cmoc run {operation} report",
            "## Outcome",
            terminal_classification,
            "## Details",
            *(
                [f"- {name}: {yaml_scalar(value)}" for name, value in details.items()]
                or ["- none"]
            ),
            "## Warnings",
            *([f"- {warning}" for warning in warnings] or ["- none"]),
            "## Execution stages",
            *execution,
            "## Related logs",
            *related_logs,
            "",
        ]
    )
    write_reserved_primary_report(report_path, content)
    return report_path.resolve()


def _render_changed_path(path: str, indent: str = "", label: str = "") -> str:
    """Git path を report の Markdown 箇条書きとして安全に描画する。

    Git path には Markdown の code span 境界や行構造を壊す文字を含められる。
    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    if not any(character in path for character in ("`", "|", "\r", "\n")):
        return f"{indent}- {label}`{path}`"
    escaped = html.escape(path, quote=False)
    escaped = (
        escaped.replace("`", "&#96;")
        .replace("|", "&#124;")
        .replace("\r\n", "&#13;&#10;")
        .replace("\r", "&#13;")
        .replace("\n", "&#10;")
    )
    return f"{indent}- {label}<code>{escaped}</code>"
