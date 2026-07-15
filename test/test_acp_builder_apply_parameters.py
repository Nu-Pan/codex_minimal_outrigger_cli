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
from acp.builder.apply.fork.file_review_and_fix import (
    build_apply_fork_file_review_and_fix_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort
from jsonschema import ValidationError, validate

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
    {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_review_and_fix.json
    """
    result = run_apply_fork_builder_import(
        tmp_path,
        (
            "from pathlib import Path; "
            "from acp.builder.apply.fork.change_summary import "
            "build_apply_fork_change_summary_parameter as change_summary; "
            "from acp.builder.apply.fork.file_review_and_fix import "
            "build_apply_fork_file_review_and_fix_parameter as review_and_fix; "
            "cs = change_summary('diff'); "
            "rf = review_and_fix(Path('{{repo-root}}') / 'src' / 'main.py'); "
            "assert cs.structured_output_schema_path.name == 'change_summary.json'; "
            "assert rf.structured_output_schema_path.name == "
            "'file_review_and_fix.json'; "
            "assert '# oracle and realization basic' in cs.prompt; "
            "assert '# apply review standard' in rf.prompt; "
            "assert rf.file_access_mode.value == 'realization_write'"
        ),
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("status", ["fixed", "unresolved"])
def test_file_review_and_fix_schema_matches_oracle_source(status: str) -> None:
    """file review and fix が正本 schema を参照することを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_review_and_fix.json
    """
    parameter = build_apply_fork_file_review_and_fix_parameter(Path(__file__))
    expected_path = oracle_schema_path("apply", "fork", "file_review_and_fix.json")

    assert parameter.structured_output_schema_path == expected_path
    schema = json.loads(expected_path.read_text())
    finding = {
        "title": "review finding",
        "evidences": [
            {
                "path": str(Path(__file__)),
                "line_start": 1,
                "line_end": 2,
                "summary": "test evidence",
            }
        ],
        "oracle_requirement": "required behavior",
        "observed_implementation": "observed behavior",
        "reason": "the implementation differs",
        "resolution": {
            "status": status,
            "summary": "fixed or left unresolved",
            "verification": "pytest result",
        },
    }
    validate({"findings": [finding]}, schema)

    with pytest.raises(ValidationError):
        validate(
            {"findings": [{**finding, "suggested_fix": "legacy field"}]},
            schema,
        )


def test_file_review_and_fix_prompt_uses_complete_standard_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """file review and fix が標準 prompt と root を組み立てることを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_review_and_fix.py
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    target = repo_root / "src" / "app.py"
    target.parent.mkdir()
    target.write_text("print('ok')\n")
    monkeypatch.chdir(repo_root)

    parameter = build_apply_fork_file_review_and_fix_parameter(
        Path("{{repo-root}}") / "src" / "app.py"
    )

    assert "# oracle standard" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# apply review standard" in parameter.prompt
    assert "# file read write rule - realization_write" in parameter.prompt
    assert "- oracle file は書き込み禁止" in parameter.prompt
    assert "- `{{work-root}}/memo` は読み書き禁止" in parameter.prompt
    assert (
        "所見の調査、修正、修正後の検証を同一の agent call 内で行う" in parameter.prompt
    )
    assert f"- {{{{target-path}}}} = {target}" in parameter.prompt
    assert f"- {{{{work-root}}}} = {repo_root}" in parameter.prompt
    assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE


def test_file_review_and_fix_rejects_relative_target_without_root_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """root token のない相対 target path を拒否することを検証する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_review_and_fix.py
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    with pytest.raises(
        ValueError, match="relative path without root path place holder"
    ):
        build_apply_fork_file_review_and_fix_parameter(Path("src/app.py"))


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

    file_review_and_fix = build_apply_fork_file_review_and_fix_parameter(target)
    change_summary = build_apply_fork_change_summary_parameter("diff")

    assert file_review_and_fix.model_class == ModelClass.EFFICIENCY
    assert file_review_and_fix.reasoning_effort == ReasoningEffort.MAX
    assert "`{{repo-root}}` ツリー内の所見" in file_review_and_fix.prompt
    assert "realization file を修正" in file_review_and_fix.prompt
    assert f"- {{{{repo-root}}}} = {repo_root}" in file_review_and_fix.prompt
    assert f"- {{{{work-root}}}} = {apply_worktree}" in file_review_and_fix.prompt
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
