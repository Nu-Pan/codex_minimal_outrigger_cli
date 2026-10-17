"""共有・個別 call の設定選択と起動前拒否を Fake Codex CLI で検証する。

根拠: oracle/doc/dev_rule/test_rule.md の「agent call の設定選択と固定」。
"""

import json
from copy import deepcopy
from dataclasses import replace

import oracle.other.path_model as path_model
import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    script_codex_calls,
    setup_codex_home,
)
from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from oracle.acp_builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter,
)
from oracle.acp_builder.oracle.edit.launch_exec import (
    build_oracle_edit_main_launch_exec_parameter,
)
from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)
from oracle.acp_builder.primary_report_review import (
    build_primary_report_review_parameter,
)
from oracle.acp_builder.quota_probe import build_quota_availability_probe_parameter
from oracle.acp_builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter,
)
from oracle.acp_builder.realization.refactor.fork.file_review_and_fix import (
    build_realization_refactor_fork_file_review_and_fix_parameter,
)
from oracle.acp_builder.run.join.conflict_resolution import (
    build_run_join_conflict_resolution_parameter,
)
from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from oracle.acp_builder.tui.launch_tui import build_tui_launch_tui_parameter

from commons.runtime_codex_exec import run_codex_exec
from commons.runtime_config import config_from_dict, config_to_dict
from commons.runtime_errors import CmocError
from commons.runtime_feedback import FeedbackInvocation
from commons.runtime_feedback_store import iter_observation_paths
from commons.runtime_git import WorktreeSnapshot
from commons.runtime_logging import SubcommandLogger
from config.cmoc_config import CmocConfig, CodexCallConfig, CodexModelProviderConfig

SUCCESS = (
    '{"type":"thread.started","thread_id":"11111111-1111-4111-8111-111111111111"}\n'
    '{"type":"turn.completed"}\n'
)


@pytest.fixture
def settings_root(tmp_path, monkeypatch, nonpersistent_codex_ids):
    """設定選択には解決済み root を使い、CLI の入出力とログ処理を通す。"""
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.chdir(root)
    monkeypatch.setattr(
        path_model, "_resolve_git_worktree_roots", lambda _cwd: (root, root)
    )
    return root


@pytest.fixture
def unchanged_artifacts(monkeypatch):
    """成果物を変更しない設定・診断検査では、空の snapshot を使う。"""
    # 実差分の照合と補正中の変動検出・復元は test_codex_runtime_retry.py の
    # corrects_declared_postcondition と restores_artifacts_changed_by_correction に残す。
    monkeypatch.setattr(
        "commons.runtime_codex_exec.capture_worktree_snapshot",
        lambda root: WorktreeSnapshot(root, ()),
    )


def shared_parameters(root):
    return [
        build_realization_apply_fork_launch_exec_parameter("base", "head", root),
        build_realization_refactor_fork_file_review_and_fix_parameter(
            root / "src.py", root
        ),
        build_feedback_remediate_issue_parameter('{"issue_id":"issue"}', root),
        build_run_join_conflict_resolution_parameter("run", "session", root),
    ]


def configured_calls():
    """誤った entry の選択を区別できるよう、全項目に異なる値を与える。"""
    config = CmocConfig()
    for index, kind in enumerate(config.codex.agent_calls):
        provider = f"provider_{index}"
        config.codex.model_providers[provider] = CodexModelProviderConfig(
            {
                "base_url": f"https://provider-{index}.invalid/v1",
                "env_key": f"AUTH_{index}",
            }
        )
        config.codex.agent_calls[kind] = CodexCallConfig(
            provider, f"model-{index}", f"effort-{index}"
        )
    return config_from_dict(config_to_dict(config))


def assert_launch(call, config, parameter):
    selected = config.codex.agent_calls[parameter.agent_call_kind]
    assert codex_arg_value(call["argv"], "--model") == selected.model
    override = codex_override_config(call["argv"])
    assert override["model_provider"] == selected.model_provider
    assert override["model_reasoning_effort"] == selected.reasoning_effort
    assert override["model_providers"] == {
        selected.model_provider: config.codex.model_providers[
            selected.model_provider
        ].settings
    }
    assert override["mcp_servers"]["cmoc_feedback"]["enabled"] == (
        parameter.enable_feedback_reporting
    )


def test_shared_builders_use_one_entry_and_distinct_agent_call_ids(
    settings_root, monkeypatch
):
    root = settings_root
    parameters = shared_parameters(root)
    assert {parameter.agent_call_kind for parameter in parameters} == {
        "realization_edit"
    }
    config = configured_calls()
    calls = script_codex_calls(monkeypatch, [(0, SUCCESS, "done")] * 8)
    logs = []
    for version in range(2):
        for parameter in parameters:
            # schema 受理は各 workload のテストに残し、設定選択を全 builder で検査する。
            result = run_codex_exec(
                replace(parameter, structured_output_schema_path=None),
                root=root,
                config=config,
            )
            assert_launch(calls[-1], config, parameter)
            log = json.loads(result.call_log_path.read_text())
            assert log["agent_call_kind"] == "realization_edit"
            assert log["model"] == config.codex.agent_calls["realization_edit"].model
            logs.append(log)
        if version == 0:
            config.codex.model_providers["changed"] = CodexModelProviderConfig(
                {"base_url": "https://changed.invalid/v1", "env_key": "CHANGED_AUTH"}
            )
            config.codex.agent_calls["realization_edit"] = CodexCallConfig(
                "changed", "changed-model", "changed-effort"
            )
    assert len(calls) == len(logs) == 8
    assert len({log["agent_call_id"] for log in logs}) == 8


def test_individual_builders_select_their_own_entries(settings_root, monkeypatch):
    root = settings_root
    parameters = [
        build_session_join_conflict_resolution_parameter("session", "home", root),
        build_tui_launch_tui_parameter("task"),
        build_oracle_investigation_launch_tui_parameter("question"),
        build_oracle_edit_main_launch_exec_parameter("edit"),
        build_feedback_normalize_issue_parameter("{}", "[]", root),
        build_primary_report_review_parameter(root / "report.md", root),
        build_quota_availability_probe_parameter(root),
    ]
    config = configured_calls()
    kinds = {parameter.agent_call_kind for parameter in parameters}
    assert kinds == config.codex.agent_calls.keys() - {"realization_edit"}
    calls = script_codex_calls(monkeypatch, [(0, SUCCESS, "done")] * len(parameters))
    for parameter in parameters:
        run_codex_exec(
            replace(parameter, structured_output_schema_path=None),
            root=root,
            config=config,
        )
        assert_launch(calls[-1], config, parameter)
    assert len({codex_arg_value(call["argv"], "--model") for call in calls}) == 7


def test_shared_settings_remain_fixed_across_output_corrections(
    settings_root, monkeypatch, unchanged_artifacts
):
    root = settings_root
    parameter = build_realization_refactor_fork_file_review_and_fix_parameter(
        root / "src.py", root
    )
    config = configured_calls()
    original = deepcopy(config)

    def change_source(index, _call):
        if index == 1:
            config.codex.agent_calls["realization_edit"] = CodexCallConfig(
                "openai", "changed", "low"
            )
            config.codex.model_providers["provider_0"].settings["base_url"] = (
                "https://changed.invalid"
            )

    accepted = {
        "findings": [],
        "verification": {"status": "not_required", "summary": "no changes"},
    }
    calls = script_codex_calls(
        monkeypatch,
        [(0, SUCCESS, "{"), (0, SUCCESS, "{}"), (0, SUCCESS, json.dumps(accepted))],
        on_call=change_source,
    )
    result = run_codex_exec(parameter, root=root, config=config)
    assert result.output_json == accepted
    assert len(calls) == 3
    logs = [
        json.loads(path.read_text())
        for path in (root / ".cmoc/gu/log/codex").glob("*/*_call.json")
    ]
    assert len({log["agent_call_id"] for log in logs}) == 1
    assert len({log["codex_call_id"] for log in logs}) == 3
    for call in calls:
        assert_launch(call, original, parameter)


@pytest.mark.parametrize("invalid", ["missing_shared", "override", "missing_provider"])
def test_invalid_saved_settings_fail_before_codex_launch(
    settings_root, monkeypatch, invalid
):
    root = settings_root
    parameter = shared_parameters(root)[0]
    data = config_to_dict(CmocConfig())
    if invalid == "missing_shared":
        del data["codex"]["agent_calls"]["realization_edit"]
    elif invalid == "override":
        data["codex"]["agent_calls"]["realization_edit"]["overrides"] = {
            "model": "other"
        }
    else:
        data["codex"]["model_providers"].clear()
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(data))
    calls = script_codex_calls(monkeypatch, [])

    with pytest.raises(CmocError):
        run_codex_exec(parameter, root=root)
    assert calls == []
    assert not (root / ".cmoc/gu/log/codex").exists()


def test_shared_structured_output_failures_keep_feedback_kind_and_call_ids(
    committed_repository,
    tmp_path,
    monkeypatch,
    nonpersistent_codex_ids,
    unchanged_artifacts,
):
    """異なる builder の受理失敗を共通種別で分類し、各実行の ID は分ける。"""
    # feedback の保存 context に必要な HEAD は、実 Git で用意する。
    root = committed_repository
    setup_codex_home(tmp_path, monkeypatch)
    logger = SubcommandLogger(root, "settings test")
    invocation = FeedbackInvocation(root, root, "settings test", logger)
    calls = script_codex_calls(monkeypatch, [(0, SUCCESS, "{}")] * 6)
    for parameter in shared_parameters(root)[1:3]:
        with pytest.raises(CmocError, match="Structured Output"):
            run_codex_exec(
                parameter, root=root, config=CmocConfig(), subcommand_logger=logger
            )
    diagnostics = [
        event
        for event in logger.event_records()
        if event.get("event_type") == "codex.structured_output_validation_exhausted"
    ]
    assert len(diagnostics) == 2
    assert {event["agent_call_kind"] for event in diagnostics} == {"realization_edit"}
    assert len({event["agent_call_id"] for event in diagnostics}) == 2
    for event in diagnostics:
        invocation.detect_event(event, logger.path)
    observations = [
        json.loads(path.read_text()) for path in iter_observation_paths(root)
    ]
    assert len(observations) == 2
    assert {item["payload"]["normalized_subject_id"] for item in observations} == {
        "realization_edit"
    }
    assert len(calls) == 6
