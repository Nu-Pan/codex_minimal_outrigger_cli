"""`cmoc oracle edit` の main-worktree exec 制御を検証する。

根拠: {{work-root}}/spec/app_spec/sub_command/oracle_edit.md
{{work-root}}/reference/src/oracle/request_builder/oracle/edit/launch_exec.py

変更あり・なしの成功時と各回の失敗時で、editor、Git 差分、session state、通知境界を比較する。
分割すると同じ invocation の前提と不変条件が重複するため、一つの制御テストに保つ。
"""

import json
import shutil
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace

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
from _report_support import assert_report_layout, original_report_input, report_section

import commons.runtime_cli as runtime_cli_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_config import config_path, config_to_dict
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


def _write_session_state(
    root: Path,
    *,
    run: RunPart,
) -> Path:
    """session branch 上の隔離 repository に oracle edit 用の state を作成する。"""
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


def _preserved_git_status(root: Path) -> tuple[str, ...]:
    """HEAD・branch・index の blob/mode と working tree の mode を取得する。"""
    return tuple(
        run_git(
            root,
            "status",
            "--porcelain=v2",
            "--branch",
            "--",
            "README.md",
            "oracle/spec.md",
        ).stdout.splitlines()
    )


@pytest.fixture(scope="module")
def oracle_edit_repository_seed(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[Path, tuple[str, ...]]:
    """各ケースへコピーする初期履歴・既存差分と、その比較基準を一度だけ作る。"""
    seed = tmp_path_factory.mktemp("oracle-edit-seed")
    with pytest.MonkeyPatch.context() as patch:
        setup_codex_home(seed, patch)
        root = make_repo(seed, initial_branch=SESSION_BRANCH)
        # 全ケースで同じ staged/unstaged 差分を使い、準備用の Git 起動を共有する。
        # index と working tree は下の fixture でそれぞれ独立して複製する。
        readme_path = root / "README.md"
        readme_path.write_text("# staged change\n")
        run_git(root, "add", "README.md")
        readme_path.write_text("# unstaged change\n")
        status = _preserved_git_status(root)
        assert any(
            line.startswith("1 MM ") and line.endswith(" README.md") for line in status
        )
        return root, status


@pytest.fixture
def oracle_edit_repository(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    oracle_edit_repository_seed: tuple[Path, tuple[str, ...]],
) -> tuple[Path, tuple[str, ...]]:
    """session branch・履歴・Codex HOME を持つ repository を準備する。"""
    setup_codex_home(tmp_path, monkeypatch)
    # cmoc は各ケースの tmp_path 内でだけ起動し、index・履歴もケース間で共有しない。
    seed, status = oracle_edit_repository_seed
    root = shutil.copytree(seed, tmp_path / "repo")
    monkeypatch.chdir(root)
    return root, status


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
    oracle_edit_repository: tuple[Path, tuple[str, ...]],
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_execution_ids: None,
    failure_stage: str | None,
    first_changes: bool,
) -> None:
    """既存差分を保ち、初回成功時は変更の有無によらず同じ入力で再実行する。"""
    # 変更なしでも二回目へ進む条件は成功ケースで検証する。
    # 失敗処理は差分に分岐しないため、各回の編集後の失敗で差分保持も検証する。
    # collector の受理・drain は test_feedback.py に残し、exec 制御と差分保持を検証する。
    # 永続採番と logger の結合は test_runtime_ids.py と test_runtime_cli.py に残す。
    # ここでは実行 ID の受け渡しと editor input・report・log の保存を実検査する。
    root, status_before = oracle_edit_repository
    instruction = (
        "oracle spec を更新する\n# 指示中の見出し\n空行を挿入しない\n"
        "過去の agent の会話と最終回答、実行ログ /example/sender.jsonl を参考にする\n"
        "````text\n```\n## 実行情報\n````\n"
        + "長い指示の続きです。\n" * 180
        + "指示全文の末尾"
    )
    integrated_case = failure_stage is None and first_changes
    if not integrated_case:
        # root 探索・branch 取得との結合は edit-success に残す。
        # ここでも実 Git の staged/unstaged 差分、branch、session state は検証する。
        monkeypatch.setattr(
            path_model_module,
            "_resolve_git_worktree_roots",
            lambda _start_path=None: (root, root),
        )

        def session_branch(target_root: Path) -> str:
            # 前提違反は下の launch_preconditions test に残し、同じ Git 取得を重ねない。
            assert target_root == root
            return SESSION_BRANCH

        monkeypatch.setattr(oracle_edit_module, "current_branch", session_branch)
    active_run = RunPart(
        "running",
        "decision_apply",
        RUN_BRANCH,
        "abc",
    )
    session_state_path = _write_session_state(root, run=active_run)
    state_before = json.loads(session_state_path.read_text())
    readme_path = root / "README.md"
    # 全ケースで同じ seed の状態を比較基準にし、開始前の Git 起動を重ねない。
    # 終了後は各 repository の実 Git 状態と本文を検査し、各回の失敗時も差分保持を確かめる。
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

    real_build_main_parameter = oracle_edit_module.build_oracle_edit_request

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
        work_path.write_text(" \n" + instruction + "\n ", encoding="utf-8")

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
        "build_oracle_edit_request",
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
    # doctor 成功後の設定を直接用意し、直後に上書きする既定設定の保存・再読込を省く。
    configured = config_to_dict(CmocConfig())
    call_kind = "build_oracle_edit_request"
    configured["codex"]["agent_calls"][call_kind] = {
        "model_provider": "custom",
        "model": "custom-model",
        "reasoning_effort": "high",
    }
    configured["codex"]["model_providers"]["custom"] = {
        "settings": {"name": "custom", "http_headers": {"X-Test": "original"}}
    }
    config_file.parent.mkdir(parents=True, exist_ok=True)
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
            assert input_path.read_text(encoding="utf-8") == " \n" + instruction + "\n "
            input_path.write_text("later human edit", encoding="utf-8")
            if first_changes:
                (root / "oracle" / "spec.md").write_text("# first edit\n")

            # 自己編集に相当する定義・設定の変更後も再構築・再読込を許さない。
            def reject_rebuild(_instruction, **_kwargs):
                pytest.fail("editor input was rebuilt after the first call")

            monkeypatch.setattr(
                oracle_edit_module,
                "build_oracle_edit_request",
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

    assert result.exit_code == (0 if failure_stage is None else 1), result.output
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
    assert instruction in complete_prompt
    # ユーザーのログ参照は保持し、自動生成文面には過去会話への参照を加えない。
    # 同じ完成 prompt で検査し、文面検査だけの fixture と builder 実行を重ねない。
    generated = complete_prompt.replace(instruction, "", 1)
    for prior_context in ("過去の agent の会話", "最終回答", "実行ログ"):
        assert prior_context not in generated
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
    status_after = _preserved_git_status(root)
    oracle_status = [line for line in status_after if line.endswith(" oracle/spec.md")]
    assert len(oracle_status) == 1
    assert oracle_status[0].startswith("1 .M ")
    assert (
        tuple(line for line in status_after if line not in oracle_status)
        == status_before
    )
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
    assert_report_layout(report)
    assert original_report_input(report) == instruction
    assert instruction in report
    assert "later human edit" not in report_section(report, "元の指示")
    overview = report.split("## 元の指示", 1)[0]
    assert "oracle spec を更新する" in overview
    assert "指示全文の末尾" not in overview
    assert len(overview) < 2000
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
    """準備失敗の検証に必要な root と前処理の呼び出し記録を用意する。"""
    # 準備失敗には Git state は不要。共通 fixture で CLI root と collector を隔離する。
    root = cli_terminal_directory
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
        "build_oracle_edit_request",
        fail_build_main_parameter,
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 1
    assert "builder failed" in result.output
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md"))
    report = terminal_primary_report(result).read_text()
    assert "入力未確定" in report.split("## 元の指示", 1)[0]
    assert "入力未確定" in report_section(report, "元の指示")


@pytest.mark.parametrize("failure_stage", ["config", "preconditions"])
def test_oracle_edit_preparation_failure_leaves_both_calls_not_started(
    oracle_edit_failure_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
) -> None:
    """共用入力確定後の準備失敗では、どちらの編集も開始済みにしない。"""
    root = oracle_edit_failure_repository
    # 完全 prompt と起動 parameter の結合は上の CLI test に残す。
    # 準備失敗では消費されない本文を構築せず、builder への入力を観測する。
    builder_inputs: list[str] = []

    def build_parameter(user_instruction: str) -> SimpleNamespace:
        builder_inputs.append(user_instruction)
        return SimpleNamespace(prompt="test skeleton")

    monkeypatch.setattr(
        oracle_edit_module,
        "build_oracle_edit_request",
        build_parameter,
    )
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

    def load_config(repository):
        # 設定の保存・読込と両回での共用は上の CLI test に残し、失敗段階だけを制御する。
        assert repository == root
        record_stage("config")
        return CmocConfig()

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
    assert builder_inputs == [
        oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER,
        "edit oracle",
    ]
    stages = ["config", "preconditions"]
    assert events == stages[: stages.index(failure_stage) + 1]
    report = terminal_primary_report(result).read_text()
    assert_report_layout(report)
    assert original_report_input(report) == "edit oracle"
    assert "edit oracle" in report.split("## 元の指示", 1)[0]
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
