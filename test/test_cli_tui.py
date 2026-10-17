"""TUI 起動直前の CLI 前処理の外部挙動を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
"""

import json
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import oracle.other.path_model as path_model_module
import pytest
from _cli_support import runner, terminal_primary_report
from _git_support import make_repo, run_git
from _report_support import original_report_input, report_metadata

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_cli as runtime_cli_module
import sub_commands.oracle.edit as oracle_edit_module
import sub_commands.oracle.investigation as investigation_module
import sub_commands.tui as tui_module
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import write_config
from config.cmoc_config import CmocConfig
from main import app

# agent 起動は全ケースでダブルを使うため、利用しない feedback transport は準備しない。
# TCP の受付・保存・drain は test_feedback.py、doctor の検査順序は test_doctor_cli.py に残す。
# 採番の永続性は test_runtime_ids.py、logger との結合は test_runtime_cli.py に残す。
# 入力保存・root・起動順の検査では、採番 DB の作成・同期を省く。
pytestmark = pytest.mark.usefixtures(
    "feedback_without_transport", "nonpersistent_execution_ids"
)


@pytest.fixture
def editor_input(
    monkeypatch: pytest.MonkeyPatch,
    handoff_start: Mock,
) -> Callable[[str], list[Path]]:
    """CLI の editor 起動時に指定本文を書き、実際に渡された入力 path を記録する。"""

    # editor 選択と --wait は test_prompt_editor_input.py で検証する。
    # TCP・guide の結合は test_editor_input_handoff.py に残す。
    # CLI では target の終了順序を観測し、各ケースの確定保存は実経路を通す。
    # 本文を書くためだけの process 起動は省く。
    def supply_input(content: str) -> list[Path]:
        opened: list[Path] = []

        def edit_input(argv: list[str]) -> SimpleNamespace:
            path = Path(argv[-1])
            assert path.read_bytes() == b""
            handoff_start.return_value.close.assert_not_called()
            opened.append(path)
            path.write_text(content, encoding="utf-8")
            return SimpleNamespace(returncode=0)

        monkeypatch.setattr(
            prompt_editor_input_module, "_select_editor", lambda: ["fake-editor"]
        )
        # 他 module の subprocess.run は置換せず、実 Git・doctor の検証を保つ。
        monkeypatch.setattr(
            prompt_editor_input_module, "subprocess", SimpleNamespace(run=edit_input)
        )
        # 実行可能な外部 command は system tools に限定する。
        monkeypatch.setenv("PATH", "/usr/bin")
        return opened

    return supply_input


@pytest.mark.parametrize(
    "command", [["tui"], ["oracle", "investigation"], ["oracle", "edit"]]
)
# 空 file と空白の分類は test_prompt_editor_input.py に残す。
# 各 CLI は空白から EmptyPromptInput を受ける経路で、中断後の終了処理を検証する。
@pytest.mark.parametrize(
    ("raw_input", "save_fails"),
    [
        pytest.param(b"recoverable input\r\n", True, id="save-failure"),
        pytest.param(" \t\r\n\u3000\u00a0\n".encode("utf-8"), False, id="whitespace"),
    ],
)
def test_editor_input_abort_preserves_input_and_finalizes_without_workload(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    handoff_start: Mock,
    command: list[str],
    raw_input: bytes,
    save_fails: bool,
) -> None:
    """保存失敗・空入力では原文を残し、後続の構築・起動をせず終了処理を行う。"""
    root = cli_terminal_directory
    # root 解決は test_basic_runtime.py と下の main/linked 成功ケースに残す。
    # 入力中断の CLI 制御では root を解決済みとし、Git の準備・探索を省く。
    monkeypatch.setattr(
        path_model_module,
        "_resolve_git_worktree_roots",
        lambda _start_path=None: (root, root),
    )
    # doctor の実処理との結合は、下の TUI 成功ケースと test_doctor_cli.py に残す。
    # 入力中断の検査では呼び出しを記録し、修復 commit・索引同期を繰り返さない。
    doctor_roots: list[Path] = []
    monkeypatch.setattr(
        runtime_cli_module, "run_doctor_preprocess", doctor_roots.append
    )
    # 実 ignore の修復・main/linked 境界は下の成功ケースと test_runtime_git_ignore.py に残す。
    # 各 command から doctor 後、editor 前に渡す root は引き続き観測する。
    ignored_roots: list[Path] = []

    def record_editor_roots_ignored(target_root: Path) -> None:
        assert doctor_roots == [root]
        ignored_roots.append(target_root)

    for module in (tui_module, investigation_module, oracle_edit_module):
        monkeypatch.setattr(
            module, "ensure_prompt_editor_roots_ignored", record_editor_roots_ignored
        )
    # doctor は上で置換済みで、入力中断は load_config より前に起きる。
    # 消費しない設定の検証・JSON 保存と directory 作成は準備しない。

    # TCP・guide の cleanup は専用 test と editor 失敗 test が実経路で検証する。
    # ここでは target を閉じてから確定保存へ進む CLI の制御だけを観測する。
    def edit_input(argv: list[str]) -> SimpleNamespace:
        assert doctor_roots == [root]
        assert ignored_roots == [root]
        handoff_start.return_value.close.assert_not_called()
        Path(argv[-1]).write_bytes(raw_input)
        return SimpleNamespace(returncode=0)

    # editor の起動・引数は専用 test が検証する。ここでは入力中断後の CLI 制御を扱う。
    # module 内の境界だけを置換し、他の subprocess.run は実行する。
    monkeypatch.setattr(
        prompt_editor_input_module, "subprocess", SimpleNamespace(run=edit_input)
    )
    monkeypatch.setattr(
        prompt_editor_input_module, "_select_editor", lambda: ["fake-editor"]
    )
    monkeypatch.setenv("PATH", "/usr/bin")
    real_replace = prompt_editor_input_module.os.replace
    save_destinations: list[Path] = []

    def save_input(source, destination):
        if Path(destination).parent == root / ".cmoc/gu/log/editor_input":
            handoff_start.return_value.close.assert_called_once_with()
            save_destinations.append(Path(destination))
            assert Path(source).read_bytes() == raw_input
            if save_fails:
                raise OSError("input save failed")
        return real_replace(source, destination)

    builders = []
    for module, name in (
        (tui_module, "build_tui_launch_tui_parameter"),
        (investigation_module, "build_oracle_investigation_launch_tui_parameter"),
        (oracle_edit_module, "build_oracle_edit_main_launch_exec_parameter"),
    ):
        builder = Mock(wraps=getattr(module, name))
        builders.append(builder)
        monkeypatch.setattr(module, name, builder)

    agent_call = Mock()
    monkeypatch.setattr(prompt_editor_input_module.os, "replace", save_input)
    monkeypatch.setattr(tui_module, "run_codex_tui", agent_call)
    monkeypatch.setattr(investigation_module, "run_codex_tui", agent_call)
    monkeypatch.setattr(oracle_edit_module, "run_codex_exec", agent_call)
    notify = Mock()
    open_report = Mock()
    monkeypatch.setattr(runtime_cli_module, "notify_terminal_result", notify)
    monkeypatch.setattr(
        runtime_cli_module, "open_primary_report_in_editor", open_report
    )

    result = runner.invoke(app, command, catch_exceptions=False)

    # CLI は BaseException も終了 code へ変換するため、call の有無を外から検査する。
    agent_call.assert_not_called()
    assert [call.args for builder in builders for call in builder.call_args_list] == [
        (prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER,)
    ]
    assert result.exit_code == 1
    assert ignored_roots == [root]
    files = list((root / ".cmoc/gu/log/editor_input").iterdir())
    assert len(files) == 1
    handoff_start.assert_called_once()
    assert handoff_start.call_args.args[:2] == (root, files[0])
    assert save_destinations == files
    assert files[0].name.endswith("_orig.md")
    assert files[0].read_bytes() == raw_input

    # 入力の中断でも、共通の終端ログ・通知と oracle edit 固有の report を保つ。
    notify.assert_called_once_with(" ".join(command), root, "failed")
    [log_path] = (root / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    finished = json.loads(log_path.read_text(encoding="utf-8").splitlines()[-1])
    assert finished["event"] == "command_finished"
    assert finished["classification"] == "error"
    assert finished["returncode"] == 1
    if not save_fails:
        assert "プロンプトが空" in result.output
        assert "Traceback" not in result.output
        assert finished["failure"]["classification"] == "handled_failure"
    if command == ["oracle", "edit"]:
        report_path = terminal_primary_report(result)
        open_report.assert_called_once_with(report_path)
        assert report_path.parent == root / ".cmoc/gu/report/oracle_edit"
        report = report_path.read_text(encoding="utf-8")
        metadata = report_metadata(report)
        assert metadata["terminal_classification"] == "error"
        assert metadata["exit_code"] == 1
        assert metadata["first_agent_call_status"] == "not_started"
        assert metadata["second_agent_call_status"] == "not_started"
        if not save_fails:
            assert original_report_input(report) == ""
    else:
        open_report.assert_not_called()


def test_tui_runs_editor_and_launches_codex_directly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    editor_input: Callable[[str], list[Path]],
    handoff_start: Mock,
) -> None:
    """既存差分を保ち、編集済み prompt から Codex TUI を直接起動する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    # 設定だけ用意し、doctor の実処理は検証対象の TUI invocation で一度だけ通す。
    # 無変更時の索引再利用は test_doctor_cli.py で検証する。
    write_config(root / ".cmoc/gt/config.json", CmocConfig())
    readme_path = root / "README.md"
    readme_path.write_text("# staged change\n")
    run_git(root, "add", "README.md")
    readme_path.write_text("# unstaged change\n")
    # v2 status の HEAD・index blob ID、三段階の mode、dirty 状態と本文を比較する。
    # staged・unstaged diff を別々に取得するための Git 起動は重ねない。
    git_state_before = run_git(
        root, "status", "--porcelain=v2", "--", "README.md"
    ).stdout
    events: list[str] = []

    real_run_doctor_preprocess = runtime_cli_module.run_doctor_preprocess

    def record_run_doctor_preprocess(
        target_root: Path,
        *,
        sync_refactor_entries: bool = True,
    ) -> None:
        """TUI invocation 内の doctor preprocess を記録して本来の処理へ委譲する。"""
        events.append("doctor")
        real_run_doctor_preprocess(
            target_root,
            sync_refactor_entries=sync_refactor_entries,
        )

    opened_inputs = editor_input(
        "\n<!-- remove me -->\n# 依頼\n\nsrc を確認して必要なら直す\n"
    )
    builder_calls: list[tuple[str, AgentCallParameter]] = []
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    real_build_parameter = tui_module.build_tui_launch_tui_parameter

    def record_build_parameter(
        original_prompt: str,
    ) -> AgentCallParameter:
        """skeleton 用と実行用の builder 呼び出しを記録する。"""
        kind = (
            "build-skeleton"
            if original_prompt == prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
            else "build-parameter"
        )
        if kind == "build-parameter":
            handoff_start.return_value.close.assert_called_once_with()
        events.append(kind)
        parameter = real_build_parameter(original_prompt)
        builder_calls.append((original_prompt, parameter))
        return parameter

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """TUI 起動 call を記録して生成パラメータを検証する。"""
        events.append("tui")
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert kwargs["purpose"] == "tui codex"
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is None
        assert parameter is builder_calls[1][1]

    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_run_doctor_preprocess,
    )
    monkeypatch.setattr(
        tui_module,
        "build_tui_launch_tui_parameter",
        record_build_parameter,
    )
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    log_dir = root / ".cmoc/gu/log/sub_command"
    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    [tui_log] = log_dir.glob("*.jsonl")
    log_events = [json.loads(line) for line in tui_log.read_text().splitlines()]
    sync_events = [
        event
        for event in log_events
        if event["event"].startswith("document_search_sync_")
    ]
    assert [event["event"] for event in sync_events] == [
        "document_search_sync_started",
        "document_search_sync_finished",
    ]
    assert sync_events[0]["sync_id"] == sync_events[1]["sync_id"]
    assert sync_events[1]["command"] == "tui"
    assert sync_events[1]["work_root"] == str(root)
    assert sync_events[1]["status"] == "updated"
    assert events == [
        "doctor",
        "build-skeleton",
        "build-parameter",
        "tui",
    ]
    assert len(builder_calls) == 2
    assert builder_calls[0][0] == prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
    assert len(tui_calls) == 1
    orig_files = list(
        (root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md")
    )
    assert len(orig_files) == 1
    assert opened_inputs == orig_files
    handoff_start.assert_called_once_with(
        root, orig_files[0], builder_calls[0][1].prompt
    )
    handoff_start.return_value.close.assert_called_once_with()
    editor_contents = orig_files[0].read_text()
    assert (
        editor_contents
        == "\n<!-- remove me -->\n# 依頼\n\nsrc を確認して必要なら直す\n"
    )
    assert not list((root / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md"))
    complete_prompt = tui_calls[0][0].prompt
    assert "# file access policy (repo_write)" in complete_prompt
    for heading in (
        "# oracle and realization basic",
        "# oracle policy",
        "# realization policy",
        "# realization findings policy",
        "# routing policy",
    ):
        assert heading in complete_prompt
    for heading in (
        "# oracle findings policy",
        "# realization oracle reference policy",
        "# index entry policy",
    ):
        assert heading not in complete_prompt
    assert '<cmoc_ref target="original_prompt"/>' in complete_prompt
    assert "# オリジナルプロンプト" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "<!-- remove me -->" in complete_prompt
    assert (
        builder_calls[1][0]
        == "<!-- remove me -->\n# 依頼\n\nsrc を確認して必要なら直す"
    )
    assert readme_path.read_bytes() == b"# unstaged change\n"
    assert (
        run_git(root, "status", "--porcelain=v2", "--", "README.md").stdout
        == git_state_before
    )
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "gu" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_tui_saves_input_and_ignores_both_roots_from_linked_worktree(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    editor_input: Callable[[str], list[Path]],
    handoff_start: Mock,
) -> None:
    """linked 起動で両 root を ignore し、入力記録と agent context を main に置く。"""
    # HEAD と linked metadata だけが必要なので、追跡 file・index の準備は省く。
    root = committed_repository
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")
    # doctor との実結合は main 起動ケース、linked 修復は test_doctor_cli.py に残す。
    # ここでは呼び出し先・順序を検査し、両 root の ignore は実 pre-log check に任せる。
    doctor_roots: list[Path] = []
    monkeypatch.setattr(
        runtime_cli_module, "run_doctor_preprocess", doctor_roots.append
    )
    # handoff の TCP・guide の結合は test_editor_input_handoff.py に残し、
    # linked 起動では main root への引き渡しと終了順序を観測する。
    write_config(linked / ".cmoc/gt/config.json", CmocConfig())
    monkeypatch.chdir(linked)
    opened_inputs = editor_input("\nlinked worktree task\n")
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """linked worktree の TUI 起動 call を記録する。"""
        assert doctor_roots == [linked.resolve()]
        handoff_start.return_value.close.assert_called_once_with()
        tui_calls.append((parameter, kwargs))

    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert doctor_roots == [linked.resolve()]
    assert len(tui_calls) == 1
    parameter, tui_kwargs = tui_calls[0]
    assert tui_kwargs["root"] == root.resolve()
    assert tui_kwargs["purpose"] == "tui codex"
    assert parameter.agent_call_cwd == root.resolve()
    [saved_input] = (root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md")
    assert opened_inputs == [saved_input]
    handoff_start.assert_called_once()
    assert handoff_start.call_args.args[:2] == (root.resolve(), saved_input)
    assert (
        prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
        in handoff_start.call_args.args[2]
    )
    assert saved_input.read_text() == "\nlinked worktree task\n"
    assert not list(
        (linked / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md"))
    complete_prompt = parameter.prompt
    assert "linked worktree task" in complete_prompt
    assert not list((root / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))
    assert not list((linked / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert "/.cmoc/gu/" in (linked / ".gitignore").read_text()
    assert (
        len(list((root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl"))) == 1
    )
    assert run_git(root, "status", "--short", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(linked, "status", "--short", "--", ".cmoc/gu").stdout.strip() == ""
