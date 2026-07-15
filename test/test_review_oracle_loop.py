"""review oracle の finding loop を検証する。

テストの根拠:

- {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/dev_rule/test_rule.md
- {{work-root}}/oracle/doc/dev_rule/coding_rule.md
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

from pathlib import Path
from typing import Any

import pytest
from _codex_support import codex_schema_name
from _git_support import make_repo

import sub_commands.review.oracle as review_module
import sub_commands.review_loop as review_loop_module
from basic.acp import AgentCallParameter
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig, CmocConfigReviewOracle


class _FakeCodexResult:
    """Codex の Structured Output を loop に渡す最小の fake 結果。

    根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    """

    def __init__(self, output_json: dict[str, object]) -> None:
        """Structured Output の payload を保持する。"""
        self.output_json = output_json


def _make_review_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    """ログ用 repo root と実行用 review worktree を分離して用意する。

    根拠:

    - {{work-root}}/oracle/doc/dev_rule/test_rule.md
    - {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    repo_root = make_repo(tmp_path)
    review_parent = tmp_path / "review"
    review_parent.mkdir()
    review_worktree = make_repo(review_parent)
    monkeypatch.chdir(review_worktree)
    return repo_root, review_worktree


def _assert_review_call_context(
    parameter: AgentCallParameter,
    kwargs: dict[str, object],
    repo_root: Path,
    review_worktree: Path,
) -> None:
    """review agent call が隔離 worktree を実行基準にすることを検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    assert Path.cwd() == review_worktree
    assert kwargs["root"] == repo_root
    assert kwargs["cwd"] == review_worktree
    assert parameter.cwd == review_worktree


def test_review_oracle_enumerate_receives_only_related_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """対象 oracle ごとに関連する finding だけを次の prompt へ渡す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    repo_root, review_worktree = _make_review_context(tmp_path, monkeypatch)
    (review_worktree / "oracle" / "a.md").write_text("# a\n")
    (review_worktree / "oracle" / "b.md").write_text("# b\n")
    prompts_by_target: dict[str, list[str]] = {}
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=2,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: Any
    ) -> _FakeCodexResult:
        """隔離 context を検証し、fake の固定応答を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """
        _assert_review_call_context(parameter, kwargs, repo_root, review_worktree)
        schema_name = codex_schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            target = Path(
                kwargs["purpose"].removeprefix("review oracle enumerate findings for ")
            ).name
            prompts_by_target.setdefault(target, []).append(parameter.prompt)
            if target == "a.md" and len(prompts_by_target[target]) == 1:
                return _FakeCodexResult(
                    {
                        "findings": [
                            {
                                "oracle_path": "{{oracle-root}}/a.md",
                                "severity": "fatal",
                                "title": "a finding",
                                "reason": "a reason",
                            }
                        ]
                    }
                )
            return _FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    review_module.run_review_oracle_loop(
        repo_root,
        review_worktree,
        [review_worktree / "oracle" / "a.md", review_worktree / "oracle" / "b.md"],
        config,
        fake_run_codex_exec,
    )

    assert "a finding" not in prompts_by_target["b.md"][0]
    assert "a finding" in prompts_by_target["a.md"][1]


def test_review_oracle_advocate_receives_same_round_challenger_reasons(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """同じ検証周回で得た challenger reason を advocate prompt に渡す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    repo_root, review_worktree = _make_review_context(tmp_path, monkeypatch)
    advocate_prompts: list[str] = []
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: Any
    ) -> _FakeCodexResult:
        """隔離 context を検証し、fake の固定応答を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """
        _assert_review_call_context(parameter, kwargs, repo_root, review_worktree)
        schema_name = codex_schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "finding",
                            "reason": "reason",
                        }
                    ]
                }
            )
        if schema_name == "validate_finding_challenger.json":
            return _FakeCodexResult({"reasons": ["same-round challenger reason"]})
        if schema_name == "validate_finding_advocate.json":
            advocate_prompts.append(parameter.prompt)
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    review_module.run_review_oracle_loop(
        repo_root,
        review_worktree,
        [review_worktree / "oracle" / "spec.md"],
        config,
        fake_run_codex_exec,
    )

    assert advocate_prompts
    assert "same-round challenger reason" in advocate_prompts[0]


def test_review_oracle_interrupt_keeps_only_completed_judgements(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """judge 中断時は完了済み verdict だけを部分結果として保持する。"""
    repo_root, review_worktree = _make_review_context(tmp_path, monkeypatch)
    oracle_path = review_worktree / "oracle" / "spec.md"
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )
    judge_calls = 0
    purposes: list[str] = []

    def interrupt_second_judge(
        parameter: AgentCallParameter, **kwargs: Any
    ) -> _FakeCodexResult:
        """列挙・検証を完了し、二つ目の judge call だけを中断する。"""
        nonlocal judge_calls
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        schema_name = codex_schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "first",
                            "reason": "first reason",
                        },
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "minor",
                            "title": "second",
                            "reason": "second reason",
                        },
                    ]
                }
            )
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            judge_calls += 1
            if judge_calls == 2:
                raise KeyboardInterrupt
            return _FakeCodexResult({"verdict": "accept", "reason": "accepted"})
        raise AssertionError(schema_name)

    with pytest.raises(review_loop_module.ReviewOracleInterrupted) as exc_info:
        review_module.run_review_oracle_loop(
            repo_root,
            review_worktree,
            [oracle_path],
            config,
            interrupt_second_judge,
        )

    interruption = exc_info.value
    assert interruption.evaluated_files == [oracle_path]
    assert [finding["verdict"] for finding in interruption.findings] == [
        "accept",
        None,
    ]
    assert judge_calls == 2
    assert purposes[-1].endswith("finding-0002")


def test_review_oracle_advocate_keeps_existing_challenger_reasons(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """既存と同じ周回の challenger reason をともに保持して渡す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
    """
    repo_root, review_worktree = _make_review_context(tmp_path, monkeypatch)
    advocate_prompts: list[str] = []
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )
    findings = [
        {
            "finding_id": "finding-0001",
            "oracle_path": "{{oracle-root}}/spec.md",
            "severity": "fatal",
            "title": "finding",
            "reason": "reason",
            "advocate_reasons": [],
            "challenger_reasons": ["old challenger reason"],
            "verdict": None,
            "judge_reason": None,
        }
    ]

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: Any
    ) -> _FakeCodexResult:
        """隔離 context を検証し、fake の固定応答を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """
        _assert_review_call_context(parameter, kwargs, repo_root, review_worktree)
        schema_name = codex_schema_name(parameter)
        if schema_name == "validate_finding_challenger.json":
            return _FakeCodexResult({"reasons": ["same-round challenger reason"]})
        if schema_name == "validate_finding_advocate.json":
            advocate_prompts.append(parameter.prompt)
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    review_loop_module._validate_and_judge_findings(
        repo_root,
        review_worktree,
        findings,
        config,
        fake_run_codex_exec,
    )

    assert advocate_prompts
    assert "old challenger reason" in advocate_prompts[0]
    assert "same-round challenger reason" in advocate_prompts[0]


def test_review_oracle_retries_semantic_merge_finding_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """意味的に不正な merge response の後に merge を再試行する。

    根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    """
    repo_root, review_worktree = _make_review_context(tmp_path, monkeypatch)
    merge_calls = 0
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=1,
            num_validate_findings_loop=1,
        ),
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: Any
    ) -> _FakeCodexResult:
        """隔離 context を検証し、fake の固定応答を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """
        _assert_review_call_context(parameter, kwargs, repo_root, review_worktree)
        nonlocal merge_calls
        schema_name = codex_schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "a",
                            "reason": "reason a",
                        },
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "b",
                            "reason": "reason b",
                        },
                    ]
                }
            )
        if schema_name == "merge_finding.json":
            merge_calls += 1
            if merge_calls == 1:
                return _FakeCodexResult(
                    {
                        "operations": [
                            {
                                "kind": "delete",
                                "target_ids": ["finding-9999"],
                                "finding": None,
                            }
                        ]
                    }
                )
            return _FakeCodexResult(
                {
                    "operations": [
                        {
                            "kind": "merge",
                            "target_ids": ["finding-0001", "finding-0002"],
                            "finding": {
                                "oracle_path": "{{oracle-root}}/spec.md",
                                "severity": "fatal",
                                "title": "merged",
                                "reason": "merged reason",
                            },
                        }
                    ]
                }
            )
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    findings = review_module.run_review_oracle_loop(
        repo_root,
        review_worktree,
        [review_worktree / "oracle" / "spec.md"],
        config,
        fake_run_codex_exec,
    )

    assert merge_calls == 2
    assert [finding["finding_id"] for finding in findings] == ["finding-0003"]
    assert findings[0]["title"] == "merged"


def test_review_oracle_fails_after_merge_finding_semantic_retries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """merge response が再試行上限まで不正なら loop を失敗させる。

    根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    """
    repo_root, review_worktree = _make_review_context(tmp_path, monkeypatch)
    merge_calls = 0
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=1,
            num_validate_findings_loop=1,
        ),
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: Any
    ) -> _FakeCodexResult:
        """隔離 context を検証し、fake の固定応答を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """
        _assert_review_call_context(parameter, kwargs, repo_root, review_worktree)
        nonlocal merge_calls
        schema_name = codex_schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "a",
                            "reason": "reason a",
                        }
                    ]
                }
            )
        if schema_name == "merge_finding.json":
            merge_calls += 1
            return _FakeCodexResult(
                {
                    "operations": [
                        {
                            "kind": "delete",
                            "target_ids": ["finding-9999"],
                            "finding": None,
                        }
                    ]
                }
            )
        raise AssertionError(schema_name)

    with pytest.raises(CmocError, match="merge finding"):
        review_module.run_review_oracle_loop(
            repo_root,
            review_worktree,
            [review_worktree / "oracle" / "spec.md"],
            config,
            fake_run_codex_exec,
        )

    assert merge_calls == 3
