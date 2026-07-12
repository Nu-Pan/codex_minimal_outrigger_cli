"""apply fork ACP builder の parameter と schema 参照を検証する。

対応する正本 schema: <work-root>/oracle/src/oracle/acp_builder/apply/fork/
"""

import json
from pathlib import Path

import pytest
from acp.builder.apply.fork.change_summary import (
    build_apply_fork_change_summary_parameter,
)
from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from basic.acp import ModelClass, ReasoningEffort
from jsonschema import validate

from _acp_builder_support import oracle_schema_path


def test_apply_fork_prompts_use_expected_roots(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    apply_worktree = repo_root / ".cmoc" / "local" / "worktree" / "session" / "run"
    apply_worktree.mkdir(parents=True)
    (repo_root / ".git").mkdir()
    (apply_worktree / ".git").write_text("gitdir: ignored\n")
    target = apply_worktree / "src" / "app.py"
    target.parent.mkdir()
    target.write_text("print('ok')\n")
    monkeypatch.chdir(apply_worktree)

    finding_application = build_apply_fork_finding_application_parameter([{"title": "t"}])
    finding_enumeration = build_apply_fork_file_finding_enumeration_parameter(target)
    change_summary = build_apply_fork_change_summary_parameter("diff")

    assert finding_application.model_class == ModelClass.EFFICIENCY
    assert finding_application.reasoning_effort == ReasoningEffort.MAX
    assert finding_enumeration.model_class == ModelClass.EFFICIENCY
    assert finding_enumeration.reasoning_effort == ReasoningEffort.MAX
    assert "`<repo-root>` ツリー内の realization file" in finding_application.prompt
    assert f"- <repo-root> = {repo_root}" in finding_application.prompt
    assert f"- <work-root> = {apply_worktree}" in finding_application.prompt
    assert "`<repo-root>` ツリー内の所見" in finding_enumeration.prompt
    assert f"- <repo-root> = {repo_root}" in finding_enumeration.prompt
    assert f"`{apply_worktree}` ツリー内の所見" not in finding_enumeration.prompt
    assert "`<repo-root>` ツリー内の差分" in change_summary.prompt
    assert f"- <repo-root> = {repo_root}" in change_summary.prompt
    assert "# oracle and realization basic" in change_summary.prompt


def test_apply_fork_change_summary_schema_matches_oracle_source() -> None:
    parameter = build_apply_fork_change_summary_parameter("diff")
    expected_path = oracle_schema_path("apply", "fork", "change_summary.json")

    assert parameter.structured_output_schema_path == expected_path

    schema = json.loads(parameter.structured_output_schema_path.read_text())
    validate(
        {
            "changes": [
                {
                    "category": "実装",
                    "summary": "変更要約 schema を正本仕様に合わせた。",
                    "changed_paths": [
                        "oracle/src/oracle/acp_builder/apply/fork/change_summary.json"
                    ],
                }
            ]
        },
        schema,
    )
