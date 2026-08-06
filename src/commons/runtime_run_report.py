"""editing run の Markdown + YAML Front Matter report。

共通処理の canonical な配置は {{work-root}}/oracle/doc/dev_rule/design_rule.md
に従っている。
"""

import html
import json
from pathlib import Path

from .runtime_paths import (
    _reserve_timestamped_path,
    reports_dir,
    timestamp,
)
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
    changed = [_render_changed_path(item) for item in changed_paths] or ["- none"]
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
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # report を書き始める前に path を予約し、同一 timestamp の run report を
        # 別 run が上書きしないようにする。
        generated_at, report_path = _reserve_timestamped_path(
            directory, ".md", timestamp
        )
    else:
        generated_at = timestamp()
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
        ("generated_at", generated_at),
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
    if isinstance(value, (list, dict)):
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
        # JSON flow style は YAML 1.2 と互換で、nested front matter を一行で保てる。
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return json.dumps(str(value), ensure_ascii=False)


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
