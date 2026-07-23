"""editing run の Markdown + YAML Front Matter report。"""

import json
from pathlib import Path

from commons.runtime_paths import reports_dir, timestamp
from sub_commands.run.lifecycle import EditingRunContext


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
    generated_at = timestamp()
    path = directory / f"{generated_at}.md"
    fields: list[tuple[str, object]] = [
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
    changed = [f"- `{item}`" for item in changed_paths] or ["- none"]
    content = [
        "---",
        *[f"{name}: {_yaml_scalar(value)}" for name, value in fields],
        "---",
        f"# cmoc {context.kind.replace('_', ' ')} fork report",
        "## Completion",
        completion_reason,
        "## Changed paths",
        *changed,
        *(body_lines or []),
        "",
    ]
    path.write_text("\n".join(content), encoding="utf-8")
    return path.resolve()


def write_lifecycle_report(
    context: EditingRunContext,
    operation: str,
    *,
    state_after: str,
    warnings: list[str],
    details: dict[str, object],
    report_path: Path | None = None,
) -> Path:
    """run join/abandon の共通情報と cleanup 結果を保存する。"""
    if report_path is None:
        directory = reports_dir(context.repo, f"run/{operation}")
        directory.mkdir(parents=True, exist_ok=True)
        report_path = directory / f"{timestamp()}.md"
    fields: list[tuple[str, object]] = [
        ("operation", operation),
        ("run_kind", context.kind),
        ("session_branch", context.session_branch),
        ("session_fork_commit", context.session_fork_commit),
        ("run_branch", context.run_branch),
        ("run_fork_commit", context.run_fork_commit),
        ("run_worktree", context.run_worktree),
        ("state_before", context.state_before),
        ("state_after", state_after),
        ("generated_at", timestamp()),
        *details.items(),
    ]
    report_path.write_text(
        "\n".join(
            [
                "---",
                *[f"{name}: {_yaml_scalar(value)}" for name, value in fields],
                "---",
                f"# cmoc run {operation} report",
                "## Warnings",
                *([f"- {warning}" for warning in warnings] or ["- none"]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return report_path.resolve()


def _yaml_scalar(value: object) -> str:
    """report の YAML scalar として安全に表現する。"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)
