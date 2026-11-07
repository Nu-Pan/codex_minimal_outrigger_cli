"""参照規定の独立した選択と、各 call への注入を検証する。

対応する正本:
- {{work-root}}/reference/src/reference/prompt_builder/complete_prompt.py
- {{work-root}}/reference/src/reference/prompt_builder/policy/reference.py
"""

import pytest
import reference.other.path_model as path_model_module
from reference.other.path_model import AgentCallPathContext
from reference.other.struct_doc import render_sd_node_as_markdown
from reference.prompt_builder.complete_prompt import build_complete_prompt
from reference.request_builder.basic import FileAccessMode
from reference.request_builder.common.conflict_resolution import (
    build_merge_conflict_resolution_request,
)
from reference.request_builder.common.primary_report_review import (
    build_primary_report_review_request,
)
from reference.request_builder.common.quota_probe import (
    build_quota_availability_probe_request,
)
from reference.request_builder.decision.apply.launch_exec import (
    build_decision_apply_decision_request,
    build_decision_apply_realization_request,
    build_decision_apply_spec_request,
)
from reference.request_builder.decision.plan.launch_tui import (
    build_decision_plan_request,
)
from reference.request_builder.feedback.report.normalize_issue import (
    build_feedback_issue_normalization_request,
)
from reference.request_builder.feedback.report.remediate_issue import (
    build_feedback_issue_remediation_request,
)
from reference.request_builder.realization.refactor.file_review_and_fix import (
    build_realization_refactor_request,
)
from reference.request_builder.tui.launch_tui import build_tui_request


@pytest.fixture
def prompt_repository(tmp_path, monkeypatch):
    # Git root の探索だけを代替し、prompt の構築・描画は実物を使う。
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        path_model_module,
        "_resolve_git_worktree_roots",
        lambda _start_path=None: (tmp_path, tmp_path),
    )
    return tmp_path


@pytest.mark.parametrize("cmoc_basic_instruction", [False, True])
@pytest.mark.parametrize("reference_policy", [None, False, True])
def test_reference_policy_is_selected_independently(
    prompt_repository, cmoc_basic_instruction, reference_policy
):
    """参照形式の注入は基本説明の有無に依存せず、未指定時には無効となる。"""
    flags = {} if reference_policy is None else {"reference_policy": reference_policy}
    prompt = build_complete_prompt(
        task="参照先を示すこと",
        file_access_mode=FileAccessMode.READONLY,
        path_context=AgentCallPathContext(agent_call_cwd=prompt_repository),
        cmoc_basic_instruction=cmoc_basic_instruction,
        **flags,
    )
    rendered = render_sd_node_as_markdown(*prompt)
    headings = [line for line in rendered.splitlines() if line.startswith("# ")]
    assert headings.count("# reference policy") == bool(reference_policy)
    assert headings.count("# cmoc basic instruction") == cmoc_basic_instruction
    assert not set(headings) & {
        "# spec policy",
        "# realization policy",
        "# routing policy",
        "# editor input handoff",
        "# feedback observation reporting",
    }
    assert "referenece format" not in rendered
    for requirement in (
        "decision への参照は「◯◯◯については [DEC-XXXXXX] を参照すること」",
        "spec への参照は「◯◯◯については [SPC-XXXXXX] を参照すること」",
        "その他の情報源への参照は「◯◯◯については `<major-location>` の `<minor-location>` を参照すること」",
        "「ファイルパス」「URL」などの、読むべきファイルのパス情報",
        "「見出し名」「参照先の記述の一部」",
        "詳細位置を特定出来る短いヒント",
    ):
        assert (requirement in rendered) == bool(reference_policy)


@pytest.mark.parametrize(
    ("build_request", "reference_enabled"),
    [
        pytest.param(lambda root: build_tui_request("task"), True, id="tui"),
        pytest.param(
            lambda root: build_decision_plan_request("task"), True, id="decision-plan"
        ),
        pytest.param(
            build_decision_apply_decision_request,
            False,
            id="decision-apply-decision",
        ),
        pytest.param(
            lambda root: build_decision_apply_spec_request("before", "after", root),
            True,
            id="decision-apply-spec",
        ),
        pytest.param(
            lambda root: build_decision_apply_realization_request(
                "before", "after", root
            ),
            True,
            id="decision-apply-realization",
        ),
        pytest.param(
            lambda root: build_realization_refactor_request(
                root / "src/example.py", root
            ),
            True,
            id="realization-refactor",
        ),
        pytest.param(
            lambda root: build_merge_conflict_resolution_request(
                source_commit="source", target_commit="target", merge_worktree=root
            ),
            True,
            id="merge-conflict",
        ),
        pytest.param(
            lambda root: build_primary_report_review_request(root / "report.md", root),
            True,
            id="primary-report-review",
        ),
        pytest.param(
            lambda root: build_feedback_issue_normalization_request("{}", "[]", root),
            True,
            id="feedback-normalize",
        ),
        pytest.param(
            lambda root: build_feedback_issue_remediation_request("{}", root),
            True,
            id="feedback-remediate",
        ),
        pytest.param(build_quota_availability_probe_request, False, id="quota-probe"),
    ],
)
def test_request_builders_select_reference_policy(
    prompt_repository, build_request, reference_enabled
):
    """参照規定を使う各 call は一度だけ注入し、利用可否 probe は省略する。"""
    request = build_request(prompt_repository)
    assert request.prompt.count("# reference policy\n") == reference_enabled
    assert "referenece format" not in request.prompt
