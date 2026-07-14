"""apply fork ACP builder の parameter と schema 参照を検証する。

対応する正本 schema: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/
"""

import json
import os
import shutil
import subprocess
import sys
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


def run_apply_fork_builder_import(
    tmp_path: Path, code: str
) -> subprocess.CompletedProcess[str]:
    """subprocess の被テスト環境を tmp_path 配下だけに置く。

    根拠: {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    target = tmp_path / "site"
    shutil.copytree(root / "src" / "acp", target / "acp")
    shutil.copytree(root / "src" / "basic", target / "basic")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    work = tmp_path / "work"
    (work / ".git").mkdir(parents=True)
    return subprocess.run(
        [sys.executable, "-S", "-c", code],
        cwd=work,
        env={**os.environ, "PYTHONPATH": str(target), "PYTHONNOUSERSITE": "1"},
        text=True,
        capture_output=True,
    )


def test_apply_fork_builders_import_from_packaged_layout(tmp_path: Path) -> None:
    """packaged layout で apply fork builder の import 契約を検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/change_summary.json
    {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_finding_enumeration.json
    """
    result = run_apply_fork_builder_import(
        tmp_path,
        (
            "from pathlib import Path; "
            "from acp.builder.apply.fork.change_summary import "
            "build_apply_fork_change_summary_parameter as change_summary; "
            "from acp.builder.apply.fork.file_finding_enumeration import "
            "build_apply_fork_file_finding_enumeration_parameter as enumerate_file; "
            "from acp.builder.apply.fork.finding_application import "
            "build_apply_fork_finding_application_parameter as apply_finding; "
            "cs = change_summary('diff'); "
            "fe = enumerate_file(Path('{{repo-root}}') / 'src' / 'main.py'); "
            "fa = apply_finding([{'title': 't'}]); "
            "assert cs.structured_output_schema_path.name == 'change_summary.json'; "
            "assert fe.structured_output_schema_path.name == "
            "'file_finding_enumeration.json'; "
            "assert fa.structured_output_schema_path is None; "
            "assert '# oracle and realization basic' in cs.prompt; "
            "assert 'realization file' in fa.prompt"
        ),
    )

    assert result.returncode == 0, result.stderr


def test_finding_application_prompt_uses_complete_standard_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """finding application が標準 prompt と所見を保持することを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/finding_application.py
    """
    repo_root = tmp_path / "repo"
    apply_worktree = repo_root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    apply_worktree.mkdir(parents=True)
    (repo_root / ".git").mkdir()
    (apply_worktree / ".git").write_text("gitdir: ignored\n")
    monkeypatch.chdir(apply_worktree)

    parameter = build_apply_fork_finding_application_parameter(
        [
            {
                "title": "first",
                "evidences": [
                    {
                        "path": str(repo_root / "review" / "_comment.md"),
                        "line_start": 1,
                        "line_end": 2,
                        "summary": "comment evidence",
                    }
                ],
            },
            {"title": "second"},
        ]
    )

    assert "# oracle and realization basic" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# file read write rule - realization_write" in parameter.prompt
    assert "- oracle file は書き込み禁止" in parameter.prompt
    assert "- `{{work-root}}/memo` は読み書き禁止" in parameter.prompt
    assert "/.agents` ツリー内は書き込み禁止" in parameter.prompt
    assert "## FINDING-00" in parameter.prompt
    assert '"title": "first"' in parameter.prompt
    assert "_comment.md" in parameter.prompt
    assert "## FINDING-01" in parameter.prompt
    assert '"title": "second"' in parameter.prompt
    assert '"findings"' not in parameter.prompt
    assert f"- {{{{work-root}}}} = {apply_worktree}" in parameter.prompt
    assert f"- {{{{repo-root}}}} = {repo_root}" in parameter.prompt


def test_file_finding_enumeration_schema_matches_oracle_source() -> None:
    """file finding enumeration が正本 schema を参照することを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_finding_enumeration.json
    """
    parameter = build_apply_fork_file_finding_enumeration_parameter(Path(__file__))

    assert parameter.structured_output_schema_path == oracle_schema_path(
        "apply", "fork", "file_finding_enumeration.json"
    )
    assert (
        json.loads(parameter.structured_output_schema_path.read_text())["type"]
        == "object"
    )


def test_file_finding_enumeration_prompt_uses_complete_standard_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """file finding enumeration が標準 prompt と root を組み立てることを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_finding_enumeration.py
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    target = repo_root / "src" / "app.py"
    target.parent.mkdir()
    target.write_text("print('ok')\n")
    monkeypatch.chdir(repo_root)

    parameter = build_apply_fork_file_finding_enumeration_parameter(
        Path("{{repo-root}}") / "src" / "app.py"
    )

    assert "# oracle standard" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# apply review standard" in parameter.prompt
    assert "- `{{work-root}}/memo` は読み書き禁止" in parameter.prompt
    assert f"- {{{{target-path}}}} = {target}" in parameter.prompt
    assert f"- {{{{work-root}}}} = {repo_root}" in parameter.prompt


def test_file_finding_enumeration_rejects_relative_target_without_root_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """root token のない相対 target path を拒否することを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_finding_enumeration.py
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    with pytest.raises(
        ValueError, match="relative path without root path place holder"
    ):
        build_apply_fork_file_finding_enumeration_parameter(Path("src/app.py"))


def test_apply_fork_prompts_use_expected_roots(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """apply fork の各 prompt が repo root と work root を使い分けることを検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
    """
    repo_root = tmp_path / "repo"
    apply_worktree = repo_root / ".cmoc" / "gu" / "worktree" / "session" / "run"
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
    assert "`{{repo-root}}` ツリー内の realization file" in finding_application.prompt
    assert f"- {{{{repo-root}}}} = {repo_root}" in finding_application.prompt
    assert f"- {{{{work-root}}}} = {apply_worktree}" in finding_application.prompt
    assert "`{{repo-root}}` ツリー内の所見" in finding_enumeration.prompt
    assert f"- {{{{repo-root}}}} = {repo_root}" in finding_enumeration.prompt
    assert f"`{apply_worktree}` ツリー内の所見" not in finding_enumeration.prompt
    assert "`{{repo-root}}` ツリー内の差分" in change_summary.prompt
    assert f"- {{{{repo-root}}}} = {repo_root}" in change_summary.prompt
    assert "# oracle and realization basic" in change_summary.prompt


def test_apply_fork_change_summary_schema_matches_oracle_source() -> None:
    """change summary が正本 schema に適合することを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/change_summary.json
    """
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
