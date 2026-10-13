"""`cmoc oracle edit` の main-worktree exec 制御を検証する。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
{{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py

変更あり・なしの成功時と各回の失敗時で、editor、Git 差分、session state、通知境界を比較する。
分割すると同じ invocation の前提と不変条件が重複するため、一つの制御テストに保つ。
"""

import json
from collections.abc import Iterator
from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from _cli_support import runner, terminal_primary_report
from _codex_support import FakeCodexResult, setup_codex_home
from _git_support import (
    RUN_BRANCH,
    SESSION_BRANCH,
    SESSION_ID,
    make_repo,
    run_git,
)

import commons.runtime_cli as runtime_cli_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError, write_config
from commons.runtime_config import config_path
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_state import (
    RunPart,
    SessionPart,
    SessionState,
    state_path,
    write_state,
)
from config.cmoc_config import CmocConfig, CodexCallConfig
from main import app


def _activate_session(
    root: Path,
    *,
    run: RunPart,
) -> Path:
    """隔離 repository に oracle edit 用の session state を作成する。"""
    run_git(root, "checkout", "-b", SESSION_BRANCH)
    path = state_path(root, SESSION_ID)
    # oracle edit は join 元情報を使わないため、state の必須文字列だけ用意する。
    write_state(
        path,
        SessionState(
            SessionPart("active", "unused-home", "abc", None),
            run,
        ),
    )
    return path


def _prepared_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """履歴・Codex HOME・既定設定を持つ隔離 repository を準備する。"""
    setup_codex_home(tmp_path, monkeypatch)
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    # doctor 成功後の設定を用意し、実際の保存・読込は検証対象に残す。
    write_config(config_path(root), CmocConfig())
    return root


def _assert_exec_parameter(
    parameter: AgentCallParameter,
    root: Path,
) -> None:
    """2 回の exec に共通する起動契約を検証する。"""
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.enable_document_search_mcp is True
    assert parameter.agent_call_cwd == root.resolve()


@pytest.mark.usefixtures("feedback_without_transport")
@pytest.mark.parametrize(
    ("first_changes", "failure_stage"),
    [
        pytest.param(True, None, id="edit-success"),
        pytest.param(False, None, id="no-change-success"),
        pytest.param(True, "first", id="edit-first-failure"),
        pytest.param(True, "second", id="edit-second-failure"),
    ],
)
def test_oracle_edit_runs_two_exec_calls_and_preserves_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str | None,
    first_changes: bool,
) -> None:
    """既存差分を保ち、初回成功時は変更の有無によらず同じ入力で再実行する。"""
    # 変更なしでも二回目へ進む条件は成功ケースで検証する。
    # 失敗処理は差分に分岐しないため、各回の編集後の失敗で差分保持も検証する。
    # collector の受理・drain は test_feedback.py に残し、exec 制御と差分保持を検証する。
    root = _prepared_repo(tmp_path, monkeypatch)
    integrated_case = failure_stage is None and first_changes
    if not integrated_case:
        # root 探索の結合は edit-success と専用テストに残す。
        # ここでも実 Git の staged/unstaged 差分、branch、session state は検証する。
        monkeypatch.setattr(
            path_model_module,
            "_resolve_git_worktree_roots",
            lambda _start_path=None: (root, root),
        )
    active_run = RunPart(
        "running",
        "realization_apply",
        RUN_BRANCH,
        "abc",
    )
    session_state_path = _activate_session(root, run=active_run)
    state_before = json.loads(session_state_path.read_text())
    readme_path = root / "README.md"
    readme_path.write_text("# staged change\n")
    run_git(root, "add", "README.md")
    readme_path.write_text("# unstaged change\n")
    # HEAD・branch・index の blob/mode と working tree の mode を一度に取得する。
    # working tree の本文は下で直接比較し、patch 生成と個別の Git 起動を省く。
    status_args = (
        "status",
        "--porcelain=v2",
        "--branch",
        "--",
        "README.md",
        "oracle/spec.md",
    )
    status_before = run_git(root, *status_args).stdout.splitlines()
    input_path: Path
    editor_calls: list[tuple[Path, str]] = []
    built_main_parameters: list[AgentCallParameter] = []
    events: list[str] = []
    notifications: list[tuple[str, Path, str]] = []

    def record_run_doctor_preprocess(target_root: Path) -> None:
        """doctor の呼び出し先と、編集開始前の実行順序を検証する。"""
        # 修復・索引同期は test_doctor_cli.py、共通 CLI との実結合と既存差分保持は
        # test_cli_tui.py の test_tui_runs_editor_and_launches_codex_directly に残す。
        assert target_root == root
        events.append("doctor")

    real_ensure_prompt_editor_roots_ignored = (
        oracle_edit_module.ensure_prompt_editor_roots_ignored
    )

    def record_ensure_prompt_editor_roots_ignored(target_root: Path) -> None:
        """ignore 修復との結合は代表ケースに残し、全ケースで呼び出しを検証する。"""
        assert target_root == root
        events.append("ignore")
        # 成功・失敗によらず編集開始前の同じ処理なので、Git 修復を繰り返さない。
        # 境界・失敗・変更後の再検査は test_runtime_git_ignore.py と test_git_query_reuse.py に残す。
        if integrated_case:
            real_ensure_prompt_editor_roots_ignored(target_root)

    real_build_main_parameter = (
        oracle_edit_module.build_oracle_edit_main_launch_exec_parameter
    )

    def record_build_main_parameter(
        user_instruction: str,
    ) -> AgentCallParameter:
        """skeleton 用と実行用の本命 builder 呼び出しを記録する。"""
        events.append(
            "build-main-skeleton"
            if user_instruction == oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER
            else "build-main"
        )
        parameter = real_build_main_parameter(user_instruction)
        built_main_parameters.append(parameter)
        return parameter

    def fake_edit_prompt_editor_input(
        target_root: Path,
        work_path: Path,
        complete_prompt_skeleton: str,
    ) -> None:
        """エディタへ渡す path と完全 prompt skeleton を記録する。"""
        nonlocal input_path
        input_path = work_path
        logger = current_subcommand_logger()
        assert logger is not None
        assert work_path.name == f"{logger.execution_id}_orig.md"
        events.append("editor")
        assert target_root == root
        editor_calls.append((work_path, complete_prompt_skeleton))
        work_path.write_text("oracle spec を更新する", encoding="utf-8")

    real_collect_prompt_editor_input = oracle_edit_module.collect_prompt_editor_input

    def fake_collect_prompt_editor_input(
        target_root: Path,
        work_path: Path,
    ) -> str:
        """一回の最終読み取りから抽出した入力を返す。"""
        events.append("collect")
        assert target_root == root
        assert work_path == input_path
        return real_collect_prompt_editor_input(target_root, work_path)

    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_run_doctor_preprocess,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "ensure_prompt_editor_roots_ignored",
        record_ensure_prompt_editor_roots_ignored,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "build_oracle_edit_main_launch_exec_parameter",
        record_build_main_parameter,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "edit_prompt_editor_input",
        fake_edit_prompt_editor_input,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    real_load_config = oracle_edit_module.load_config
    config_file = config_path(root)
    configured = json.loads(config_file.read_text())
    call_kind = "build_oracle_edit_main_launch_exec_parameter"
    configured["codex"]["agent_calls"][call_kind] = {
        "model_provider": "custom",
        "model": "custom-model",
        "reasoning_effort": "high",
    }
    configured["codex"]["model_providers"]["custom"] = {
        "settings": {"name": "custom", "http_headers": {"X-Test": "original"}}
    }
    config_file.write_text(json.dumps(configured))

    def record_load_config(target_root: Path):
        events.append("config")
        return real_load_config(target_root)

    monkeypatch.setattr(oracle_edit_module, "load_config", record_load_config)
    real_require_launch_preconditions = (
        oracle_edit_module._require_oracle_edit_launch_preconditions
    )

    def record_launch_preconditions(repository: Path, current_root: Path) -> None:
        """oracle edit の起動前提検査を記録して本来の検査へ委譲する。"""
        events.append("check")
        real_require_launch_preconditions(repository, current_root)

    def fake_runtime_exec(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> FakeCodexResult:
        """各 exec の差分と、失敗後も差分を残す挙動を再現する。"""
        calls.append((parameter, kwargs))
        assert parameter is built_main_parameters[1]
        config = kwargs["config"]
        assert isinstance(config, CmocConfig)
        # 呼び出し時点の値を検査し、共用 object の途中変更も検出する。
        # argv・MCP 設定の変換は test_runtime_codex_profile.py と
        # test_codex_runtime_exec.py に残し、この制御 test で Git 探索を重ねない。
        call_config = config.codex.agent_calls[parameter.agent_call_kind]
        assert call_config == CodexCallConfig("custom", "custom-model", "high")
        assert config.codex.model_providers[call_config.model_provider].settings == {
            "name": "custom",
            "http_headers": {"X-Test": "original"},
        }
        if len(calls) == 1:
            events.append("first")
            assert input_path.read_text(encoding="utf-8") == "oracle spec を更新する"
            input_path.write_text("later human edit", encoding="utf-8")
            if first_changes:
                (root / "oracle" / "spec.md").write_text("# first edit\n")

            # 自己編集に相当する定義・設定の変更後も再構築・再読込を許さない。
            def reject_rebuild(_instruction, **_kwargs):
                pytest.fail("editor input was rebuilt after the first call")

            monkeypatch.setattr(
                oracle_edit_module,
                "build_oracle_edit_main_launch_exec_parameter",
                reject_rebuild,
            )
            configured["codex"]["agent_calls"][call_kind]["model"] = "changed-model"
            configured["codex"]["model_providers"]["custom"]["settings"][
                "http_headers"
            ]["X-Test"] = "changed"
            config_file.write_text(json.dumps(configured))
            if failure_stage == "first":
                raise CmocError("first failed", [], "returncode: 7")
        else:
            events.append("second")
            expected_before_second = "# first edit\n" if first_changes else spec_before
            assert (root / "oracle" / "spec.md").read_text() == expected_before_second
            (root / "oracle" / "spec.md").write_text("# second edit\n")
            if failure_stage == "second":
                raise CmocError("second failed", [], "returncode: 8")
        return FakeCodexResult()

    monkeypatch.setattr(
        oracle_edit_module,
        "_require_oracle_edit_launch_preconditions",
        record_launch_preconditions,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "run_codex_exec",
        fake_runtime_exec,
    )
    monkeypatch.setattr(
        runtime_cli_module,
        "notify_terminal_result",
        lambda command, repository, state: notifications.append(
            (command, repository, state)
        ),
    )

    spec_before = (root / "oracle" / "spec.md").read_text()
    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == (0 if failure_stage is None else 1)
    assert len(built_main_parameters) == 2
    assert editor_calls[0][0] == input_path
    complete_prompt_skeleton = editor_calls[0][1]
    assert (
        complete_prompt_skeleton.count(oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER)
        == 1
    )
    assert "# file access policy (pure_oracle_write)" in complete_prompt_skeleton
    skeleton_objective = complete_prompt_skeleton.split(
        '<cmoc_block id="objective">', 1
    )[1].split("</cmoc_block>", 1)[0]
    assert "# task" in skeleton_objective
    assert "目標状態" in skeleton_objective
    assert "# completion criteria" in skeleton_objective
    assert "# scope" in skeleton_objective
    assert "# 変更操作の制約" in complete_prompt_skeleton
    assert "`git add`、`git commit`、`git stash`、branch 切替" in (
        complete_prompt_skeleton
    )
    assert "変更を未コミットのまま残す" in complete_prompt_skeleton
    expected_events = [
        "doctor",
        "ignore",
        "build-main-skeleton",
        "editor",
        "collect",
        "build-main",
        "config",
        "check",
        "first",
    ]
    if failure_stage != "first":
        expected_events.append("second")
    assert events == expected_events
    assert len(calls) == (1 if failure_stage == "first" else 2)

    main_parameter, main_kwargs = calls[0]
    assert main_parameter is built_main_parameters[1]
    _assert_exec_parameter(main_parameter, root)
    assert "cwd" not in main_kwargs
    assert "before_agent_call" not in main_kwargs
    assert main_kwargs["root"] == root
    assert main_kwargs["purpose"] == "oracle edit first"
    complete_prompt = main_parameter.prompt
    assert "oracle spec を更新する" in complete_prompt
    assert oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER not in complete_prompt
    assert "# oracle policy" in complete_prompt
    assert "# routing policy" in complete_prompt
    main_objective = complete_prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in main_objective
    assert "# completion criteria" in main_objective
    assert "# 変更操作の制約" in complete_prompt

    if failure_stage != "first":
        second_parameter, second_kwargs = calls[1]
        assert second_parameter is main_parameter
        assert second_kwargs["root"] == root
        assert second_kwargs["config"] is main_kwargs["config"]
        assert second_kwargs["purpose"] == "oracle edit second"

    assert input_path.read_text(encoding="utf-8") == "later human edit"
    assert not list(input_path.parent.glob("*_cmpl.md"))
    expected_spec = "# first edit\n" if failure_stage == "first" else "# second edit\n"
    assert (root / "oracle" / "spec.md").read_text() == expected_spec
    assert json.loads(session_state_path.read_text()) == state_before
    assert readme_path.read_text() == "# unstaged change\n"
    status_after = run_git(root, *status_args).stdout.splitlines()
    oracle_status = [line for line in status_after if line.endswith(" oracle/spec.md")]
    assert len(oracle_status) == 1
    assert oracle_status[0].startswith("1 .M ")
    assert [line for line in status_after if line not in oracle_status] == status_before
    assert not (root / ".cmoc" / "gu" / "report" / "oracle" / "edit" / "fork").exists()
    terminal_output = result.stdout + result.stderr
    if failure_stage is None:
        assert "# 完了: cmoc oracle edit" in result.stdout
        assert notifications == [("oracle edit", root, "completed")]
    else:
        assert "# 失敗: cmoc oracle edit" in result.stderr
        assert notifications == [("oracle edit", root, "failed")]
    assert (
        terminal_output.count("# 完了: cmoc oracle edit")
        + terminal_output.count("# 失敗: cmoc oracle edit")
        == 1
    )
    assert "- result:" not in terminal_output
    assert "- completion_reason:" not in terminal_output
    report_path = terminal_primary_report(result)
    assert terminal_output.count(str(report_path)) == 1
    report = report_path.read_text(encoding="utf-8")
    expected_classification = "natural_completion" if failure_stage is None else "error"
    expected_first_status = "failed" if failure_stage == "first" else "succeeded"
    expected_second_status = {
        None: "succeeded",
        "first": "not_started",
        "second": "failed",
    }[failure_stage]
    assert f'terminal_classification: "{expected_classification}"' in report
    assert f"exit_code: {result.exit_code}" in report
    assert f'first_agent_call_status: "{expected_first_status}"' in report
    assert f'second_agent_call_status: "{expected_second_status}"' in report
    assert "# cmoc oracle edit report" in report
    assert "診断用サブコマンドログ" in report


@pytest.fixture
def oracle_edit_failure_repository(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[Path]:
    """準備失敗の検証に必要な root・設定・前処理の呼び出し記録を用意する。"""
    # 準備失敗には Git state は不要。共通 fixture で CLI root と collector を隔離する。
    root = cli_terminal_directory
    write_config(config_path(root), CmocConfig())
    # builder も同じ root を使う。実 Git の探索は edit-success と test_basic_runtime.py に残す。
    monkeypatch.setattr(
        path_model_module,
        "_resolve_git_worktree_roots",
        lambda _start_path=None: (root, root),
    )
    # doctor との実結合は test_cli_tui.py、修復は test_doctor_cli.py に残す。
    # ignore の実処理は edit-success、境界・失敗は test_runtime_git_ignore.py に残す。
    preparation_calls: list[tuple[str, Path]] = []
    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        lambda target_root: preparation_calls.append(("doctor", target_root)),
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "ensure_prompt_editor_roots_ignored",
        lambda target_root: preparation_calls.append(("ignore", target_root)),
    )
    yield root
    assert preparation_calls == [("doctor", root), ("ignore", root)]


def test_oracle_edit_builder_failure_does_not_reserve_editor_input_file(
    oracle_edit_failure_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """skeleton 構築に失敗した場合は editor input file を残さない。"""
    root = oracle_edit_failure_repository

    def fail_build_main_parameter(
        _user_instruction: str, **_kwargs: object
    ) -> AgentCallParameter:
        """skeleton の構築失敗を再現する。"""
        raise CmocError("builder failed", [], "test failure")

    monkeypatch.setattr(
        oracle_edit_module,
        "build_oracle_edit_main_launch_exec_parameter",
        fail_build_main_parameter,
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 1
    assert "builder failed" in result.output
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md"))


@pytest.mark.parametrize("failure_stage", ["config", "preconditions"])
def test_oracle_edit_preparation_failure_leaves_both_calls_not_started(
    oracle_edit_failure_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
) -> None:
    """共用入力確定後の準備失敗では、どちらの編集も開始済みにしない。"""
    # 起動前提は失敗境界の double へ置き換えるため、session は不要。
    monkeypatch.setattr(
        oracle_edit_module, "edit_prompt_editor_input", lambda *_args: None
    )
    monkeypatch.setattr(
        oracle_edit_module, "collect_prompt_editor_input", lambda *_args: "edit oracle"
    )
    events = []

    def record_stage(stage):
        events.append(stage)
        if stage == failure_stage:
            raise CmocError(f"{stage} failed", [], "test failure")

    real_load_config = oracle_edit_module.load_config

    def load_config(repository):
        record_stage("config")
        return real_load_config(repository)

    monkeypatch.setattr(oracle_edit_module, "load_config", load_config)
    monkeypatch.setattr(
        oracle_edit_module,
        "_require_oracle_edit_launch_preconditions",
        lambda *_args: record_stage("preconditions"),
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("edit started after preparation failure"),
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 1
    stages = ["config", "preconditions"]
    assert events == stages[: stages.index(failure_stage) + 1]
    report = terminal_primary_report(result).read_text()
    for pass_name in ("first", "second"):
        assert f'{pass_name}_agent_call_status: "not_started"' in report


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("linked", "main worktree"),
        ("non_session", "session branch"),
        ("inactive", "active な session"),
    ],
)
def test_oracle_edit_launch_preconditions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
    message: str,
) -> None:
    """oracle edit の各起動前提違反を利用者向け例外として検証する。"""
    # branch 取得との結合は上の CLI test に残し、各判定には返り値と実 state を使う。
    root = tmp_path / "repo"
    root.mkdir()

    def branch_for_precondition(repository: Path) -> str:
        assert repository == root
        assert case != "linked"
        return SESSION_BRANCH if case == "inactive" else "main"

    monkeypatch.setattr(oracle_edit_module, "current_branch", branch_for_precondition)
    current_root = root
    if case == "linked":
        current_root = tmp_path / "linked"
        current_root.mkdir()
    elif case == "inactive":
        write_state(
            state_path(root, SESSION_ID),
            SessionState(SessionPart("joined", "main", "abc", None)),
        )
    with pytest.raises(CmocError, match=message):
        oracle_edit_module._require_oracle_edit_launch_preconditions(
            root,
            current_root,
        )


def test_oracle_edit_prompt_preserves_user_log_reference(tmp_path, monkeypatch):
    """ユーザーのログ参照は保持し、自動生成の過去会話参照は含めない。"""
    # 実 Git の root 解決は test_basic_runtime.py と上の CLI 結合 test に残す。
    # 文面の検査では探索結果だけを置換し、builder と renderer は実物を使う。
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        path_model_module,
        "_resolve_git_worktree_roots",
        lambda _start_path=None: (tmp_path, tmp_path),
    )
    instruction = (
        "診断用サブコマンドログ /example/sender.jsonl を参考に oracle を編集する"
    )
    empty = oracle_edit_module.build_oracle_edit_main_launch_exec_parameter("").prompt
    prompt = oracle_edit_module.build_oracle_edit_main_launch_exec_parameter(
        instruction
    ).prompt
    assert instruction in prompt
    for prior_context in ("過去の agent の会話", "最終回答", "実行ログ"):
        assert prior_context not in empty
