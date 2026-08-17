"""非対話末端サブコマンドの primary report 完了契約を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
- {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
- {{work-root}}/oracle/doc/app_spec/sub_command/
"""

import json
from pathlib import Path

import pytest
import typer
import yaml
from _git_support import make_repo

import commons.runtime_cli as runtime_cli
from cmoc_runtime import CmocError, TerminalResult

_EARLY_ERROR_REPORTS = [
    ("doctor", "doctor", ()),
    ("indexing", "indexing", ("commit_id",)),
    (
        "session fork",
        "session/fork",
        (
            "session_id",
            "home_branch",
            "session_branch",
            "session_fork_commit",
            "session_state_before",
            "session_state_after",
        ),
    ),
    (
        "session join",
        "session/join",
        (
            "session_branch",
            "home_branch",
            "session_branch_head_before_merge",
            "home_branch_head_before_merge",
            "merge_commit",
            "session_state_before",
            "session_state_after",
        ),
    ),
    (
        "session abandon",
        "session/abandon",
        (
            "session_branch",
            "home_branch",
            "abandoned_branch_start_commit",
            "session_state_before",
            "session_state_after",
        ),
    ),
    (
        "oracle edit",
        "oracle_edit",
        ("main_agent_call_status", "reduction_agent_call_status"),
    ),
    (
        "oracle review",
        "oracle_review",
        (
            "scope",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_join_commit",
            "oracle_count_total",
            "oracle_count_evaluated",
            "fatal_findings_accepted_count",
            "minor_findings_accepted_count",
            "fatal_findings_rejected_count",
            "minor_findings_rejected_count",
            "result",
        ),
    ),
    (
        "realization apply fork",
        "realization/apply/fork",
        (
            "run_kind",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "diff_base_commit",
            "codex_returncode",
            "changed_paths",
            "feedback_observation_count",
            "feedback_observations",
        ),
    ),
    (
        "realization refactor fork",
        "realization/refactor/fork",
        (
            "run_kind",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "refactor_state_path",
            "completion_reason",
        ),
    ),
    (
        "run join",
        "run/join",
        (
            "run_kind",
            "session_branch",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "run_join_commit",
        ),
    ),
    (
        "run abandon",
        "run/abandon",
        (
            "run_kind",
            "session_branch",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
        ),
    ),
    (
        "feedback report",
        "feedback/invocation",
        (
            "session_branch",
            "report_cut_id",
            "report_cut_at",
            "normal_publication_status",
            "incomplete_diagnostic_status",
            "current_pointer_update_status",
        ),
    ),
]


def _disable_external_completion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """test 対象を report と terminal result の確定処理へ限定する。"""
    monkeypatch.setattr(
        runtime_cli,
        "start_feedback_invocation",
        lambda *_args: (None, None),
    )
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda *_args: None,
    )


def _terminal_report_path(output: str) -> Path:
    """capsys で得た terminal result から primary report path を読む。"""
    prefix = "- primary report ("
    for line in output.splitlines():
        if line.startswith(prefix) and "): `" in line and line.endswith("`"):
            return Path(line.split("): `", 1)[1][:-1])
    raise AssertionError(f"primary report path not found:\n{output}")


@pytest.mark.parametrize(
    ("command_name", "report_directory", "required_fields"),
    _EARLY_ERROR_REPORTS,
)
def test_early_error_saves_command_specific_primary_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    command_name: str,
    report_directory: str,
    required_fields: tuple[str, ...],
) -> None:
    """処理開始前の error でも固有の保存先と必須 front matter を保つ。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _disable_external_completion(monkeypatch)

    def fail_before_command_body() -> None:
        """doctor preprocess または共通事前条件での終了を再現する。"""
        raise CmocError("early failure", ["retry command"], "early detail")

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            fail_before_command_body,
            command_name=command_name,
            command_argv=("cmoc", *command_name.split(), "--scope", "all"),
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert exc_info.value.exit_code == 1
    assert captured.out == ""
    report_path = _terminal_report_path(captured.err)
    assert report_path.parent == (
        root / ".cmoc" / "gu" / "ar" / "report" / report_directory
    )
    assert report_path.is_file()
    assert captured.err.count(str(report_path)) == 1
    rendered = report_path.read_text(encoding="utf-8")
    front_matter = rendered.split("---", 2)[1]
    metadata = yaml.safe_load(front_matter)
    assert isinstance(metadata, dict)
    assert metadata["terminal_classification"] == "error"
    assert metadata["exit_code"] == 1
    assert 'terminal_classification: "error"' in front_matter
    assert "exit_code: 1" in front_matter
    assert f'repo_root: "{root.resolve()}"' in front_matter
    assert "理由:" not in front_matter
    assert "詳細:" not in front_matter
    for field in required_fields:
        assert f"{field}:" in front_matter
    assert "early failure" in rendered
    assert "early detail" in rendered
    assert "診断用サブコマンドログ" in rendered
    if command_name == "oracle edit":
        assert 'main_agent_call_status: "not_started"' in front_matter
        assert 'reduction_agent_call_status: "not_started"' in front_matter
    if command_name == "oracle review":
        assert 'result: "error"' in front_matter
        assert "## Verdict" in rendered
    if command_name == "realization refactor fork":
        assert 'completion_reason: "error"' in front_matter
    if command_name == "realization apply fork":
        assert "feedback_observation_count: 0" in front_matter
        assert "feedback_observations: []" in front_matter
    if command_name == "feedback report":
        assert "feedback publication または active state ではありません" in rendered


def test_user_interruption_saves_feedback_invocation_summary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """feedback 中断は publication ではない invocation summary を保存する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _disable_external_completion(monkeypatch)

    def interrupt() -> TerminalResult:
        runtime_cli.mark_current_subcommand_interrupted()
        return TerminalResult(next_actions=("同じ command を再実行してください。",))

    runtime_cli.run_cli_subcommand(
        interrupt,
        command_name="feedback report",
        command_argv=("cmoc", "feedback", "report"),
        doctor_preprocess=False,
        interruptible=True,
    )

    captured = capsys.readouterr()
    report_path = _terminal_report_path(captured.out)
    rendered = report_path.read_text(encoding="utf-8")
    assert "# 中断完了: cmoc feedback report" in captured.out
    assert 'terminal_classification: "user_interruption"' in rendered
    assert "feedback publication または active state ではありません" in rendered
    assert "## checkpoint と部分結果" in rendered
    assert "report cut: `not_fixed`" in rendered
    assert "確定済み部分結果: `not_fixed`" in rendered
    assert not list(report_path.parent.parent.glob("*.md"))
    assert not list(report_path.parent.parent.joinpath("incomplete").glob("*.md"))


def test_refactor_fallback_records_user_interruption_reason(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """fallback report でも refactor の中断理由を確定する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _disable_external_completion(monkeypatch)

    def interrupt_without_report() -> TerminalResult:
        """処理本体が中断だけを確定し、report 保存を共通 fallback に委ねる。"""
        runtime_cli.mark_current_subcommand_interrupted()
        return TerminalResult()

    runtime_cli.run_cli_subcommand(
        interrupt_without_report,
        command_name="realization refactor fork",
        command_argv=("cmoc", "realization", "refactor", "fork"),
        doctor_preprocess=False,
        interruptible=True,
    )

    captured = capsys.readouterr()
    report_path = _terminal_report_path(captured.out)
    front_matter = report_path.read_text(encoding="utf-8").split("---", 2)[1]
    assert 'terminal_classification: "user_interruption"' in front_matter
    assert 'completion_reason: "user_interruption"' in front_matter


def test_unsaved_report_path_becomes_internal_failure_without_path_display(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """保存を確認できない path を隠し、report 基盤の internal failure にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _disable_external_completion(monkeypatch)
    unsaved_path = root / "must-not-be-displayed.md"

    def return_unsaved_report() -> TerminalResult:
        return TerminalResult(
            primary_report=unsaved_path,
            primary_report_role="doctor execution report",
        )

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            return_unsaved_report,
            command_name="doctor",
            command_argv=("cmoc", "doctor"),
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert exc_info.value.exit_code == 1
    assert "# 失敗: cmoc doctor" in captured.err
    assert "primary report の保存を確認できませんでした。" in captured.err
    assert str(unsaved_path) not in captured.err
    assert "- primary report (" not in captured.err
    assert not unsaved_path.exists()
    log_directory = root / ".cmoc" / "gu" / "ar" / "log" / "sub_command"
    [log_path] = log_directory.glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    finished = events[-1]
    assert finished["event"] == "command_finished"
    assert finished["failure"]["classification"] == "internal_failure"
    assert finished["terminal_result"]["primary_report_path"] is None
