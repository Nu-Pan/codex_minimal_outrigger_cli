"""oracle 変更後の公開 CLI leaf 集合を固定する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
- {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
- {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
- {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
- {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
- {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

import inspect

import click
import pytest
import typer
from _cli_support import _CliRunner
from click.testing import CliRunner
from typer.main import get_command

from main import app


@pytest.fixture(autouse=True)
def _clear_completion_probe_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通常の CLI tree test を外部の completion probe 環境から分離する。"""
    # {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
    monkeypatch.delenv("_CMOC_COMPLETE", raising=False)


@pytest.fixture(scope="module")
def cli_command() -> click.Command:
    """構造を変更しない検査間で、Typer から構築した command tree を共有する。"""
    # invocation ごとの Context は runner が作成し、tree の再構築だけを省く。
    return get_command(app)


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


def test_public_cli_leaf_commands_match_oracle(cli_command: click.Command) -> None:
    """公開 CLI の末端 command 集合が正本の列挙と一致することを確認する。"""
    assert _leaves(cli_command) == {
        ("doctor",),
        ("feedback", "report"),
        ("feedback", "close"),
        ("oracle", "edit"),
        ("oracle", "investigation"),
        ("realization", "apply"),
        ("realization", "refactor"),
        ("run", "abandon"),
        ("run", "join"),
        ("session", "abandon"),
        ("session", "fork"),
        ("session", "join"),
        ("tui",),
        ("resume",),
    }


def test_public_leaf_commands_have_production_scenarios(
    cli_command: click.Command,
) -> None:
    """実 CLI を実行しない通常検証でも、公開末端のケース追加漏れを検出する。"""
    from test_production_cli import PRODUCTION_SCENARIO_COMMANDS

    # 仕様との一致検査と同じ tree を使い、構築と末端列挙の実装を重ねない。
    assert _leaves(cli_command) == PRODUCTION_SCENARIO_COMMANDS


def test_help_renders_without_typer_click_compatibility_error(
    cli_command: click.Command,
) -> None:
    """Typer/Click の互換性エラーなく help が描画されることを確認する。"""
    context = click.Context(cli_command, info_name="cmoc")

    rendered = cli_command.get_help(context)

    assert "oracle" in rendered
    assert "realization" in rendered
    assert "run" in rendered

    runner = CliRunner()
    for command_path in (("oracle", "edit"), ("run", "join")):
        result = runner.invoke(cli_command, [*command_path, "--help"])
        assert result.exit_code == 0, result.output


@pytest.mark.parametrize("workload", ["apply", "refactor"])
def test_removed_realization_fork_entry_is_rejected_without_runtime(
    cli_command,
    tmp_path,
    monkeypatch,
    workload,
):
    """旧 fork を alias にせず、help と実行の双方を新しい末端に揃える。"""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    help_result = runner.invoke(cli_command, ["realization", workload, "--help"])
    assert help_result.exit_code == 0
    assert "fork" not in help_result.output
    removed = runner.invoke(cli_command, ["realization", workload, "fork"])
    assert removed.exit_code != 0
    assert "fork" in removed.output
    assert not (tmp_path / ".cmoc").exists()


def test_shared_cli_runner_reuses_tree_with_independent_invocations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """tree の再構築を省いても、引数・環境・Context を次の実行に持ち越さない。"""
    import _cli_support as cli_support

    probe = typer.Typer()
    contexts = []

    @probe.command()
    def echo(value: str = typer.Option(..., envvar="CMOC_TEST_VALUE")) -> None:
        contexts.append(click.get_current_context())
        typer.echo(value)

    builds = []

    def build(app):
        builds.append(app)
        return get_command(app)

    monkeypatch.setattr(cli_support, "get_command", build)
    runner = _CliRunner()
    explicit = runner.invoke(probe, ["--value", "argument"])
    environment = runner.invoke(probe, [], env={"CMOC_TEST_VALUE": "environment"})
    missing = runner.invoke(probe, [], env={"CMOC_TEST_VALUE": None})

    assert (explicit.exit_code, explicit.output) == (0, "argument\n")
    assert (environment.exit_code, environment.output) == (0, "environment\n")
    assert missing.exit_code == 2
    assert "Missing option" in missing.output
    assert contexts[0] is not contexts[1]
    assert builds == [probe]


def test_click_option_metavar_accepts_contextless_help_call() -> None:
    """Click 8.2 の標準 option も Typer の旧 rich help から呼び出せる。"""
    if "ctx" not in inspect.signature(click.Option.make_metavar).parameters:
        pytest.skip("Click 8.2 より前は metavar に context を要求しない")

    option = click.Option(["--value"])
    with click.Context(click.Command("cmoc")):
        assert option.make_metavar() == "TEXT"


def test_feedback_report_exposes_no_subcommand_specific_options(
    cli_command: click.Command,
) -> None:
    """feedback report が位置引数と固有 option を公開しないことを確認する。"""
    feedback = cli_command.commands["feedback"]
    feedback_commands = getattr(feedback, "commands", None)
    assert isinstance(feedback_commands, dict)
    report = feedback_commands["report"]
    options = {
        option
        for parameter in report.params
        if isinstance(parameter, click.Option)
        for option in parameter.opts
    }
    arguments = {
        parameter.name
        for parameter in report.params
        if isinstance(parameter, click.Argument)
    }

    assert arguments == set()
    assert options == set()
