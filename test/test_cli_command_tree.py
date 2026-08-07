"""oracle 変更後の公開 CLI leaf 集合を固定する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
- {{work-root}}/oracle/doc/app_spec/sub_command/indexing.md
- {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
- {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
- {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
- {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
"""

import click
from typer.main import get_command

from main import app


def _leaves(
    command: click.Command,
    prefix: tuple[str, ...] = (),
) -> set[tuple[str, ...]]:
    """Click command tree から末端 command の path 集合を抽出する。"""
    commands = getattr(command, "commands", None)
    if commands is None:
        return {prefix}
    return {
        leaf
        for name, child in commands.items()
        for leaf in _leaves(child, (*prefix, name))
    }


def test_public_cli_leaf_commands_match_oracle() -> None:
    """公開 CLI の末端 command 集合が正本の列挙と一致することを確認する。"""
    assert _leaves(get_command(app)) == {
        ("doctor",),
        ("feedback", "report"),
        ("indexing",),
        ("oracle", "edit"),
        ("oracle", "investigation"),
        ("oracle", "review"),
        ("realization", "apply", "fork"),
        ("realization", "refactor", "fork"),
        ("run", "abandon"),
        ("run", "join"),
        ("session", "abandon"),
        ("session", "fork"),
        ("session", "join"),
        ("tui",),
    }


def test_help_renders_without_typer_click_compatibility_error() -> None:
    """Typer/Click の互換性エラーなく help が描画されることを確認する。"""
    command = get_command(app)
    context = click.Context(command, info_name="cmoc")

    rendered = command.get_help(context)

    assert "oracle" in rendered
    assert "realization" in rendered
    assert "run" in rendered


def test_feedback_report_exposes_only_all_option() -> None:
    """feedback report は表示範囲を広げる option だけを公開する。"""
    command = get_command(app)
    feedback = command.commands["feedback"]
    assert isinstance(feedback, click.Group)
    report = feedback.commands["report"]
    options = {
        option
        for parameter in report.params
        if isinstance(parameter, click.Option)
        for option in parameter.opts
    }

    assert options == {"--all"}
