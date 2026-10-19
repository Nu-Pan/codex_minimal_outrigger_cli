"""非対話末端サブコマンドの primary report 完了契約を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
- {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
- {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
- {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
- {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
- {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
"""

import json
import threading
import time
from pathlib import Path
from unittest.mock import Mock

import pytest
import typer
from _cli_support import terminal_primary_report
from _report_support import (
    assert_report_layout,
    original_report_input,
    report_metadata,
    report_section,
    report_text,
)

import commons.runtime_cli as runtime_cli
import commons.runtime_primary_report as primary_report_module
import commons.runtime_primary_report_render as report_render_module
from cmoc_runtime import CmocError, TerminalResult
from commons.runtime_logging import SubcommandLogger
from commons.runtime_primary_report import PrimaryReportSaveError
from commons.runtime_primary_report_render import execution_record_markdown
from commons.runtime_report_markdown import (
    ReportSummary,
    markdown_sections,
    render_report_document,
)


@pytest.mark.parametrize("fence", ["```", "~~~~"])
def test_report_sections_preserve_quoted_content_and_separate_generated_headings(fence):
    """生成見出しだけを空行で区切り、複数行の原文と code block は変えない。"""
    quoted = "# 原文の見出し\n## 原文の内部"
    quoted_code = "```text\n## 原文のコード\n```"
    fenced = [fence + "text", "# コード内の見出し", fence[:-1], fence]
    lines = [
        "# report",
        "本文",
        "## 詳細",
        quoted,
        quoted_code,
        *fenced,
        "####### 見出しではない本文",
        "#空白のない本文",
        "## 終了",
        "- none",
    ]

    assert markdown_sections(lines) == (
        "# report\n\n本文\n\n## 詳細\n\n"
        + quoted
        + "\n"
        + quoted_code
        + "\n"
        + "\n".join(fenced)
        + "\n####### 見出しではない本文\n#空白のない本文\n\n## 終了\n\n- none\n"
    )


@pytest.mark.parametrize(
    "source",
    [
        '`cmoc` <target> & "value" | [label](file.md) *literal* \\path',
        "``quoted`` と `trailing`",
        "literal &#96; &lt;tag&gt; &amp; &#10;",
        "# 入力の見出し\n- 項目\n```text\n本文\n```",
    ],
)
def test_report_summary_preserves_symbols_in_source_and_markdown(source):
    """抜粋・要約は元の記号を保ち、Markdown として読んでも本文を欠落させない。"""
    rendered = render_report_document(
        "cmoc oracle edit report",
        {
            "command": "cmoc oracle edit",
            "execution_id": "test-execution",
            "repo_root": "/repo/<target>&value",
            "session_branch": "session",
        },
        ReportSummary("完了", (source,), (source,), (source,)),
        "詳細結果なし",
        original_input=source,
        execution_record="## 実行記録\n\n実行なし",
    )
    assert_report_layout(rendered)
    assert original_report_input(rendered) == source
    excerpt = " ".join(source.split())
    intro = rendered.split("## 実行結果", 1)[0]
    for section in (
        intro,
        *(
            report_section(rendered, name)
            for name in ("実行結果", "要注意事項", "次の操作")
        ),
    ):
        assert excerpt in section
        assert excerpt in report_text(section)
    assert "/repo/<target>&value" in intro
    assert "/repo/<target>&value" in report_text(intro)


def test_report_metadata_preserves_types_and_escaped_values():
    """実行情報は値の型と境界を保ち、連続した report 間で本文を混ぜない。"""
    values = ["", None, True, False, 0, 1.25, [], {}, "null", "日本語\n次の行", r"\n"]
    for execution_id in ("first", "second", "first"):
        fields = {
            "command": "cmoc doctor",
            "execution_id": execution_id,
            "work_root": Path('/repo/"quoted"\\path'),
            "values": values,
            "nested": {"key\n\ud800": ["\udfff", {"value": "日本語"}]},
        }
        rendered = render_report_document("report", fields, ReportSummary("完了"), "")
        rendered.encode("utf-8")
        metadata = report_metadata(rendered)
        assert metadata == {
            **fields,
            "work_root": str(fields["work_root"]),
            "nested": {"key\n\\ud800": [r"\udfff", {"value": "日本語"}]},
        }
        assert [type(value) for value in metadata["values"]] == [
            type(value) for value in values
        ]


@pytest.fixture
def primary_report_directory(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """Git 探索と外部通知を省き、report の保存・描画・終了処理を検証する。"""
    # 実 Git の cwd・linked worktree 境界は test_runtime_cli.py に残す。
    monkeypatch.setattr(runtime_cli, "notify_terminal_result", lambda *_args: None)
    return cli_terminal_directory


@pytest.mark.parametrize(
    ("editor", "expected_argv"),
    [
        ("code", ["/fake/code"]),
        ("nano", ["/fake/xterm", "-e", "/fake/nano"]),
    ],
)
def test_primary_report_editor_launch_is_detached_without_console_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    editor: str,
    expected_argv: list[str],
) -> None:
    """report 表示は保存済み file を開き、editor の終了を待たずに戻る。"""
    report = tmp_path / "report.md"
    report.write_text("# report\n", encoding="utf-8")
    monkeypatch.setattr(
        primary_report_module,
        "select_editor",
        lambda: (editor, f"/fake/{editor}"),
    )
    monkeypatch.setattr(
        primary_report_module.shutil,
        "which",
        lambda name: "/fake/xterm" if name == "xterm" else None,
    )
    calls: list[tuple[list[str], dict[str, object]]] = []
    release_editor = threading.Event()

    class FakeProcess:
        def wait(self) -> int:
            release_editor.wait(timeout=5)
            return 0

    def fake_popen(argv: list[str], **kwargs: object) -> FakeProcess:
        calls.append((argv, kwargs))
        return FakeProcess()

    monkeypatch.setattr(primary_report_module.subprocess, "Popen", fake_popen)
    started = time.monotonic()
    try:
        primary_report_module.open_primary_report_in_editor(report)
        assert time.monotonic() - started < 1
    finally:
        release_editor.set()

    assert len(calls) == 1
    argv, kwargs = calls[0]
    assert argv == [*expected_argv, str(report.resolve())]
    assert "--wait" not in argv
    assert kwargs == {
        "stdin": primary_report_module.subprocess.DEVNULL,
        "stdout": primary_report_module.subprocess.DEVNULL,
        "stderr": primary_report_module.subprocess.DEVNULL,
        "start_new_session": True,
        "close_fds": True,
    }


@pytest.mark.parametrize("ending", ["success", "interruption", "error"])
def test_formatted_primary_report_is_opened_once_before_terminal_event(
    primary_report_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    ending: str,
) -> None:
    """全終了分類で最終出力を整形保存し、終了 event より先に一度だけ開く。"""
    root = primary_report_directory
    opened: list[Path] = []

    def observe_open(path: Path) -> None:
        logger = runtime_cli.current_subcommand_logger()
        assert logger is not None
        assert path.is_file()
        rendered = path.read_text(encoding="utf-8")
        assert_report_layout(rendered)
        assert "# cmoc doctor report" in rendered
        assert '"message": "first\nsecond"' in rendered
        assert "### Codex 最終出力" in rendered
        assert not any(
            event["event"] == "command_finished" for event in logger.event_records()
        )
        opened.append(path)

    monkeypatch.setattr(runtime_cli, "open_primary_report_in_editor", observe_open)

    def finish() -> None:
        logger = runtime_cli.current_subcommand_logger()
        assert logger is not None
        output = logger.path.with_name("structured-output.json")
        output.write_text('{"message":"first\\nsecond"}', encoding="utf-8")
        logger.event(
            "codex_call",
            output_path=str(output),
            schema_path=str(root / "schema.json"),
            status="succeeded",
        )
        if ending == "error":
            raise CmocError("failed", [], "injected failure")
        if ending == "interruption":
            runtime_cli.mark_current_subcommand_interrupted()

    if ending == "error":
        with pytest.raises(typer.Exit) as exit_info:
            runtime_cli.run_cli_subcommand(
                finish, command_name="doctor", doctor_preprocess=False
            )
        assert exit_info.value.exit_code == 1
    else:
        runtime_cli.run_cli_subcommand(
            finish, command_name="doctor", doctor_preprocess=False, interruptible=True
        )

    output = capsys.readouterr()
    report = terminal_primary_report(output.err if ending == "error" else output.out)
    assert opened == [report]
    [log_path] = (root / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert (
        events[-1]["classification"]
        == {
            "success": "natural_completion",
            "interruption": "user_interruption",
            "error": "error",
        }[ending]
    )


def test_primary_report_editor_failure_is_warning_without_result_change(
    primary_report_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """editor 起動失敗は report・終了 code を保ち、診断記録へ残す。"""
    root = primary_report_directory

    def fail_open(_path: Path) -> None:
        raise OSError("editor unavailable")

    monkeypatch.setattr(runtime_cli, "open_primary_report_in_editor", fail_open)
    runtime_cli.run_cli_subcommand(
        lambda: None, command_name="doctor", doctor_preprocess=False
    )

    output = capsys.readouterr()
    report = terminal_primary_report(output.out)
    assert report.is_file()
    assert "# 完了: cmoc doctor" in output.out
    assert "primary report editor launch failed" in output.out
    [log_path] = (root / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-2]["event"] == "warning"
    assert "editor unavailable" in events[-2]["message"]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 0


_EARLY_ERROR_REPORTS = [
    ("doctor", "doctor", ()),
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
        ("first_agent_call_status", "second_agent_call_status"),
    ),
    (
        "realization apply",
        "realization/apply",
        (
            "run_kind",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "completion_reason",
            "diff_base_commit",
            "codex_returncode",
            "changed_paths",
            "feedback_observation_count",
            "feedback_observations",
        ),
    ),
    (
        "realization refactor",
        "realization/refactor",
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
            "run_kind",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "wave_count",
            "final_high_watermark",
            "processed_issues",
            "confirmed_issue_commits",
            "rollback",
            "report_cut_id",
            "report_cut_at",
            "normal_publication_status",
            "incomplete_diagnostic_status",
            "current_pointer_update_status",
        ),
    ),
]

_EARLY_ERROR_SECTIONS = {
    "doctor": ("## doctor preprocess",),
    "session fork": (
        "## branch の作成と checkout",
        "## session state file と状態遷移",
        "## rollback と残存資源",
    ),
    "session join": ("## branch 切替と merge", "## state 遷移"),
    "session abandon": (
        "## 破棄対象",
        "## branch 切替と state 遷移",
        "## branch 削除と cleanup",
        "## rollback と残存資源",
    ),
    "oracle edit": ("## agent call", "first agent call", "second agent call"),
    "realization apply": (
        "## run",
        "## 追従差分と Codex result",
        "## feedback observation",
    ),
    "realization refactor": ("## Current fork", "## Processing units"),
    "run join": (
        "## run join",
        "## 差分検査と merge / no-op join",
        "## post-join と cleanup",
    ),
    "run abandon": ("## process と cleanup", "## state 遷移"),
    "feedback report": ("## 確定済みの部分結果", "## 維持した state と未実行処理"),
}


@pytest.mark.parametrize(
    ("command_name", "report_directory", "required_fields"),
    _EARLY_ERROR_REPORTS,
)
def test_early_error_saves_command_specific_primary_report(
    primary_report_directory: Path,
    capsys: pytest.CaptureFixture[str],
    command_name: str,
    report_directory: str,
    required_fields: tuple[str, ...],
) -> None:
    """処理開始前の error でも固有の保存先と必須実行情報を保つ。"""
    # doctor preprocess から共通 report 保存へ到達する経路は、
    # test_runtime_cli.py の前処理失敗ケースで検証し、個別 report を重複生成しない。
    root = primary_report_directory

    def fail_precondition(_runtime_root: Path) -> None:
        """report 保存前の処理開始エラーを再現する。"""
        raise CmocError("early failure", ["retry command"], "early detail")

    def command_body_must_not_start() -> None:
        """事前条件の失敗後にサブコマンド本体を開始しないことを検証する。"""
        pytest.fail("command body started after precondition failure")

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            command_body_must_not_start,
            command_name=command_name,
            command_argv=("cmoc", *command_name.split(), "--scope", "all"),
            pre_log_check=fail_precondition,
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert exc_info.value.exit_code == 1
    assert captured.out == ""
    assert "実行 ID: exec_" in captured.err.splitlines()[0]
    report_path = terminal_primary_report(captured.err)
    assert report_path.parent == (root / ".cmoc" / "gu" / "report" / report_directory)
    assert report_path.is_file()
    assert captured.err.count(str(report_path)) == 1
    rendered = report_path.read_text(encoding="utf-8")
    assert_report_layout(rendered)
    information = report_section(rendered, "実行情報")
    metadata = report_metadata(rendered)
    assert isinstance(metadata, dict)
    assert metadata["execution_id"] == report_path.stem
    assert metadata["subcommand_log_path"] == str(
        root / ".cmoc/gu/log/sub_command" / f"{report_path.stem}.jsonl"
    )
    assert metadata["terminal_classification"] == "error"
    assert metadata["exit_code"] == 1
    assert 'terminal_classification: "error"' in information
    assert "exit_code: 1" in information
    assert f'repo_root: "{root.resolve()}"' in information
    assert "理由:" not in information
    assert "詳細:" not in information
    for field in required_fields:
        assert field in metadata
    assert "early failure" in rendered
    assert "early detail" in rendered
    assert "診断用サブコマンドログ" in rendered
    for section in _EARLY_ERROR_SECTIONS[command_name]:
        assert section in rendered
    if command_name == "oracle edit":
        assert 'first_agent_call_status: "not_started"' in information
        assert 'second_agent_call_status: "not_started"' in information
        assert "入力未確定" in report_section(rendered, "元の指示")
        assert "入力未確定" in rendered.split("## 元の指示", 1)[0]
    if command_name == "realization refactor":
        assert 'completion_reason: "error"' in information
        assert "## Current fork" in rendered
        assert "- processed targets: not_fixed" in rendered
        assert "## Unresolved targets" in rendered
        assert "- count: not_fixed" in rendered
        assert "## Unresolved findings" in rendered
        assert "## Processing units" in rendered
        assert "## Refactor state" not in rendered
        assert "investigation_required" not in rendered
        assert "## Change summary" in rendered
    if command_name == "realization apply":
        assert 'completion_reason: "error"' in information
        assert "feedback_observation_count: 0" in information
        assert "feedback_observations: []" in information
        assert "commit 範囲: 未確定 → 未確定" in report_section(rendered, "元の指示")
    if command_name == "feedback report":
        assert "feedback publication または active state ではありません" in rendered


def test_user_interruption_saves_feedback_invocation_summary(
    primary_report_directory: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """feedback 中断は publication ではない invocation summary を保存する。"""

    def interrupt() -> TerminalResult:
        runtime_cli.mark_current_subcommand_interrupted()
        return TerminalResult(
            details=(("中断理由", "report cut を固定する前に停止しました。"),),
            next_actions=("同じ command を再実行してください。",),
        )

    runtime_cli.run_cli_subcommand(
        interrupt,
        command_name="feedback report",
        command_argv=("cmoc", "feedback", "report"),
        doctor_preprocess=False,
        interruptible=True,
    )

    captured = capsys.readouterr()
    report_path = terminal_primary_report(captured.out)
    rendered = report_path.read_text(encoding="utf-8")
    assert "# 中断完了: cmoc feedback report" in captured.out
    assert 'terminal_classification: "user_interruption"' in rendered
    assert "feedback publication または active state ではありません" in rendered
    for field, label in (
        ("normal_publication_status", "正常 publication"),
        ("incomplete_diagnostic_status", "incomplete 診断"),
        ("current_pointer_update_status", "current pointer 更新"),
    ):
        assert f'{field}: "not_completed"' in rendered
        assert f"- {label}: `not_completed`" in rendered

    assert "中断理由: `report cut を固定する前に停止しました。`" in rendered
    assert "## checkpoint と部分結果" in rendered
    assert "report cut: `not_fixed`" in rendered
    assert "確定済み部分結果: `not_fixed`" in rendered
    assert not list(report_path.parent.parent.glob("*.md"))
    assert not list(report_path.parent.parent.joinpath("incomplete").glob("*.md"))


@pytest.mark.parametrize("supplied_report", [False, True])
def test_primary_report_keeps_outputs_observations_and_artifact_paths(
    primary_report_directory: Path,
    capsys: pytest.CaptureFixture[str],
    supplied_report: bool,
) -> None:
    """初回・resume の本文、区切り付き path、observation を両 report 経路へ残す。"""
    from commons.runtime_logging import current_subcommand_logger

    root = primary_report_directory
    # path の境界条件も同じ保存経路で検証し、別の CLI invocation を準備しない。
    artifacts = (
        (
            root / "output`first.txt",
            root / "call`first.json",
            "first final output\n```embedded fence```\n",
        ),
        (
            root / "output`resume.txt",
            root / "call`resume.json",
            "resume final output\n",
        ),
    )
    observation = {
        "summary": "accepted issue",
        "workload_limitation": "different workload",
    }

    def body() -> TerminalResult:
        logger = current_subcommand_logger()
        assert logger is not None
        for output, call_log, content in artifacts:
            output.write_text(content)
            logger.event(
                "codex_call",
                output_path=str(output),
                call_log_path=str(call_log),
                purpose="unsafe path",
                status="succeeded",
            )
        logger.event(
            "feedback_observation_accepted",
            observation_id="fbo_000000_2026-09-29_15-04",
            payload=observation,
        )
        if supplied_report:
            saved = logger.path.with_suffix(".md")
            saved.write_text(
                render_report_document(
                    "Workload report",
                    {"command": "cmoc doctor", "execution_id": logger.execution_id},
                    ReportSummary("完了"),
                    "## 実行記録\n\n本文にも同じ見出しがある。\n",
                )
            )
            return TerminalResult(
                primary_report=saved, primary_report_role="test report"
            )
        return TerminalResult()

    runtime_cli.run_cli_subcommand(body, command_name="doctor", doctor_preprocess=False)
    captured = capsys.readouterr()
    report = terminal_primary_report(captured.out).read_text()
    for output, call_log, content in artifacts:
        assert content in report
        assert f"出力: ``{output.resolve()}``" in report
        if not supplied_report:
            expected_call_log = str(call_log.resolve()).replace("`", "'")
            assert (
                f"Codex call (unsafe path, succeeded): `{expected_call_log}`" in report
            )
    assert "accepted issue" in report
    assert "different workload" in report


def test_saved_individual_report_uses_final_result_and_late_notices(
    primary_report_directory,
    capsys,
):
    root = primary_report_directory
    warning = "late warning " + "details " * 80

    def body():
        logger = runtime_cli.current_subcommand_logger()
        path = root / "individual.md"
        content = primary_report_module.prepare_primary_report(
            path,
            "cmoc run join report",
            {
                "command": "cmoc run join",
                "execution_id": logger.execution_id,
                "subcommand_log_path": str(logger.path),
                "terminal_classification": "natural_completion",
                "exit_code": 0,
                "state_after": "ready",
            },
            ReportSummary("完了", ("merge は確定済みです。",)),
            "確定済みの merge を維持します。",
        )
        primary_report_module.write_reserved_primary_report(path, content)
        logger.record_warning(warning, emit=False)
        logger.event(
            "feedback_observation_accepted",
            observation_id="new-observation",
            payload={"summary": "new issue", "workload_limitation": "external"},
        )
        raise CmocError(
            "late failure",
            ["inspect latest result"],
            "late failure detail",
            terminal_result=TerminalResult(
                primary_report=path, primary_report_role="run join report"
            ),
        )

    with pytest.raises(typer.Exit):
        runtime_cli.run_cli_subcommand(
            body, command_name="run join", doctor_preprocess=False
        )
    report = terminal_primary_report(capsys.readouterr().err).read_text()
    assert_report_layout(report)
    assert "失敗" in report_section(report, "実行結果")
    assert "merge は確定済み" in report_section(report, "実行結果")
    assert "late warning" in report_section(report, "要注意事項")
    assert "新規 feedback observation: 1 件" in report_section(report, "要注意事項")
    assert "late failure" in report_section(report, "要注意事項")
    assert "inspect latest result" in report_section(report, "次の操作")
    assert warning in report
    assert "new issue" in report
    assert report_metadata(report)["terminal_classification"] == "error"
    assert report_metadata(report)["exit_code"] == 1


def test_inherited_report_notices_belong_to_original_execution(
    tmp_path, monkeypatch, nonpersistent_execution_ids
):
    # 警告の実行帰属は実ログで検査し、永続採番は logger・ID の専用 test に残す。
    original = SubcommandLogger(tmp_path, "feedback report")
    original.record_warning("original warning", emit=False)
    resumed = SubcommandLogger(tmp_path, "feedback report")
    resumed.record_warning("resumed warning", emit=False)
    monkeypatch.setattr(
        report_render_module, "current_subcommand_logger", lambda: resumed
    )
    notices = report_render_module.saved_execution_notices(
        original.path, original.execution_id
    )
    assert notices == ("original warning",)


def test_structured_output_display_preserves_json_values_and_hierarchy(
    tmp_path: Path,
) -> None:
    """report 表示だけを整え、JSON 文字列を二重に解釈しない。"""
    output = tmp_path / "structured-output.json"
    source = {
        "nested": {
            "text": "日本語\n次の行",
            "literal": r"\n",
            "json_text": '{"x":1}',
            "quoted": 'say "hi" \\ slash',
            "line\nkey": "first\n\nlast\n",
            "surrogate": "\ud800",
            "empty": "",
            "nothing": None,
            "items": [True, False, 0, 1.25, [], {}],
            "groups": [[1], {"key": [2, 3]}, 4],
        }
    }
    output.write_text(json.dumps(source, ensure_ascii=True), encoding="utf-8")
    duplicate_output = tmp_path / "duplicate-keys.json"
    duplicate_output.write_text(
        '{"duplicate":"first","duplicate":"second"}', encoding="utf-8"
    )
    report = execution_record_markdown(
        None,
        saved_events=(
            {
                "event": "codex_call",
                "output_path": str(output),
                "schema_path": str(tmp_path / "schema.json"),
                "status": "succeeded",
            },
            {
                "event": "codex_call",
                "output_path": str(duplicate_output),
                "schema_path": str(tmp_path / "schema.json"),
                "status": "succeeded",
            },
        ),
    )

    assert f"出力: `{output.resolve()}`" in report
    assert '"nested": {\n    "text": "日本語\n次の行"' in report
    assert r'"literal": "\\n"' in report
    assert r'"json_text": "{\"x\":1}"' in report
    assert r'"quoted": "say \"hi\" \\ slash"' in report
    assert '"line\nkey": "first\n\nlast\n"' in report
    assert r'"surrogate": "\ud800"' in report
    assert '"empty": ""' in report
    assert '"nothing": null' in report
    assert (
        '"items": [\n      true,\n      false,\n      0,\n      1.25,\n      [],\n      {}\n    ]'
        in report
    )
    assert (
        '"groups": [\n      [\n        1\n      ],\n'
        '      {\n        "key": [\n          2,\n          3\n        ]\n      },\n'
        "      4\n    ]" in report
    )
    assert '"literal": "\n"' not in report
    assert '"duplicate": "first",\n  "duplicate": "second"' in report
    assert "正式な結果ではありません" not in report


def test_structured_output_display_marks_unaccepted_and_unparseable_outputs(
    tmp_path: Path,
) -> None:
    """補正前の出力と JSON parse 不能な原文を正式結果と区別する。"""
    outputs = (
        b'{"result":"wrong"}',
        b"{broken JSON\n\n",
        b"NaN",
        b'{"text":"\xff"}',
    )
    events = []
    for index, content in enumerate(outputs):
        output = tmp_path / f"output-{index}.json"
        output.write_bytes(content)
        events.append(
            {
                "event": "codex_call",
                "output_path": str(output),
                "schema_path": str(tmp_path / "schema.json"),
                "status": (
                    "output_correction_requested"
                    if index == 0
                    else "structured_output_validation_failed"
                ),
            }
        )

    report = execution_record_markdown(None, saved_events=tuple(events))

    assert report.count("検証不合格（正式な結果ではありません）。") == 4
    assert '"result": "wrong"' in report
    assert report.count("JSON として解析できません。取得できた原文を示します。") == 3
    assert "{broken JSON" in report
    assert "```text\n{broken JSON\n\n\n```" in report
    assert "\nNaN\n" in report
    assert r'"text":"\xff"' in report


def test_primary_report_explains_when_codex_output_is_unavailable(
    tmp_path: Path,
) -> None:
    """最終出力 artifact が無い失敗でも、未取得状態を report に残す。"""
    report = execution_record_markdown(
        None,
        saved_events=(
            {
                "event": "codex_call",
                "output_path": str(tmp_path / "missing-output.txt"),
                "status": "failed",
            },
        ),
    )

    assert "### Codex 最終出力" in report
    assert "取得済みの最終出力はありません。" in report


def test_refactor_fallback_records_user_interruption_reason(
    primary_report_directory: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """fallback report でも refactor の中断理由を確定する。"""

    def interrupt_without_report() -> TerminalResult:
        """処理本体が中断だけを確定し、report 保存を共通 fallback に委ねる。"""
        runtime_cli.mark_current_subcommand_interrupted()
        return TerminalResult()

    runtime_cli.run_cli_subcommand(
        interrupt_without_report,
        command_name="realization refactor",
        command_argv=("cmoc", "realization", "refactor"),
        doctor_preprocess=False,
        interruptible=True,
    )

    captured = capsys.readouterr()
    report_path = terminal_primary_report(captured.out)
    information = report_metadata(report_path.read_text(encoding="utf-8"))
    assert information["terminal_classification"] == "user_interruption"
    assert information["completion_reason"] == "user_interruption"


def test_existing_primary_report_survives_update_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """execution record の更新失敗で、cleanup 前に保存した report を失わない。"""
    path = tmp_path / "report.md"
    path.write_text("pending report\n")

    def fail_replace(_temporary: Path, _target: Path) -> None:
        """既存 report の atomic replacement failure を再現する。"""
        raise OSError("injected report update failure")

    monkeypatch.setattr(primary_report_module.os, "replace", fail_replace)

    with pytest.raises(PrimaryReportSaveError):
        primary_report_module.rewrite_primary_report(path, "final report\n")

    assert path.read_text() == "pending report\n"
    assert not list(tmp_path.glob(".report.md.*"))


@pytest.mark.parametrize(
    "invalid_kind", ["empty", "directory", "symlink", "dangling_symlink", "unreadable"]
)
def test_existing_invalid_report_is_rejected_without_rewrite(
    tmp_path: Path,
    invalid_kind: str,
) -> None:
    """各 file 境界と読取失敗を拒否し、既存 report と link 先を保持する。"""
    # missing path と共通の終了処理は次の結合 test に残し、ここでは保存 API を検証する。
    # report 検査で終了するため、CLI context・実ログ・採番を準備しない。
    root = tmp_path
    report_path = root / "invalid-report.md"
    linked_target = root / "linked-report.md"
    if invalid_kind == "empty":
        report_path.touch()
    elif invalid_kind == "directory":
        report_path.mkdir()
    elif invalid_kind in {"symlink", "dangling_symlink"}:
        if invalid_kind == "symlink":
            linked_target.write_text("protected report\n", encoding="utf-8")
        report_path.symlink_to(linked_target)
    else:
        report_path.write_bytes(b"\xff")

    logger = Mock(spec=SubcommandLogger)
    with pytest.raises(PrimaryReportSaveError) as exc_info:
        primary_report_module.ensure_primary_report(
            root,
            "doctor",
            ("cmoc", "doctor"),
            "natural_completion",
            0,
            TerminalResult(
                primary_report=report_path,
                primary_report_role="doctor execution report",
            ),
            logger,
        )

    assert exc_info.value.target_path == report_path
    assert logger.mock_calls == []
    if invalid_kind in {"symlink", "dangling_symlink"}:
        assert report_path.is_symlink()
        assert report_path.readlink() == linked_target
        if invalid_kind == "symlink":
            assert linked_target.read_text(encoding="utf-8") == "protected report\n"
        else:
            assert not linked_target.exists()
    elif invalid_kind == "directory":
        assert report_path.is_dir()
    else:
        assert report_path.read_bytes() == (b"" if invalid_kind == "empty" else b"\xff")


def test_invalid_report_save_becomes_internal_failure_without_path_display(
    primary_report_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """保存 API の失敗を internal failure にし、未保存 path の表示・起動を防ぐ。"""
    root = primary_report_directory
    unsaved_path = root / "must-not-be-displayed.md"
    opened: list[Path] = []
    monkeypatch.setattr(runtime_cli, "open_primary_report_in_editor", opened.append)

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
    assert opened == []
    log_directory = root / ".cmoc" / "gu" / "log" / "sub_command"
    [log_path] = log_directory.glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    finished = events[-1]
    assert finished["event"] == "command_finished"
    assert finished["failure"]["classification"] == "internal_failure"
    assert finished["failure"]["target_path"] == str(unsaved_path.absolute())
    assert finished["terminal_result"]["primary_report_path"] is None
