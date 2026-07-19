"""oracle 変更後の公開 CLI leaf 集合を固定する。"""

import click
from typer.main import get_command

from main import app


def _leaves(
    command: click.Command,
    prefix: tuple[str, ...] = (),
) -> set[tuple[str, ...]]:
    commands = getattr(command, "commands", None)
    if commands is None:
        return {prefix}
    return {
        leaf
        for name, child in commands.items()
        for leaf in _leaves(child, (*prefix, name))
    }


def test_public_cli_leaf_commands_match_oracle() -> None:
    assert _leaves(get_command(app)) == {
        ("doctor",),
        ("indexing",),
        ("oracle", "edit", "fork"),
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
    command = get_command(app)
    context = click.Context(command, info_name="cmoc")

    rendered = command.get_help(context)

    assert "oracle" in rendered
    assert "realization" in rendered
    assert "run" in rendered
