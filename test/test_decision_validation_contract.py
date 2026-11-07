"""decision 検証 MCP の入出力契約を検証する。検証器・stdio 通信は対象外。"""

import pytest
from jsonschema.validators import Draft202012Validator
from reference.mcp.decision_validation import (
    VALIDATION_TOOL_INPUT_SCHEMA,
    VALIDATION_TOOL_OUTPUT_SCHEMA,
)


def test_decision_validation_schemas_are_valid():
    """MCP に公開する schema 自体が宣言した JSON Schema dialect に従う。"""
    for schema in (VALIDATION_TOOL_INPUT_SCHEMA, VALIDATION_TOOL_OUTPUT_SCHEMA):
        Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize(
    ("arguments", "accepted"),
    [
        pytest.param({}, True, id="all-decisions"),
        pytest.param({"work_root": "/tmp/other"}, False, id="different-work-root"),
        pytest.param({"paths": ["decision/a.md"]}, False, id="partial-validation"),
        pytest.param({"fix": True}, False, id="automatic-edit"),
        pytest.param(None, False, id="not-an-object"),
    ],
)
def test_input_schema_accepts_only_an_empty_argument_object(arguments, accepted):
    """agent が対象を絞り込んだり、tool に編集を依頼したりできない。"""
    assert Draft202012Validator(VALIDATION_TOOL_INPUT_SCHEMA).is_valid(arguments) == (
        accepted
    )


@pytest.mark.parametrize(
    ("result", "accepted"),
    [
        pytest.param({"status": "ok", "problems": []}, True, id="no-problems"),
        pytest.param(
            {
                "status": "ok",
                "problems": [
                    {
                        "path": "decision/example.md",
                        "line": 3,
                        "message": "Unresolved reference [DEC-000123].",
                    }
                ],
            },
            True,
            id="completed-with-problems",
        ),
        pytest.param(
            {"status": "error", "message": "Cannot read decision/example.md."},
            True,
            id="validation-failed",
        ),
        pytest.param({"status": "ok"}, False, id="missing-problems"),
        pytest.param({"problems": []}, False, id="missing-status"),
        pytest.param({"status": "error"}, False, id="missing-failure-reason"),
        pytest.param(
            {"status": "error", "message": " \n"}, False, id="blank-failure-reason"
        ),
        pytest.param(
            {"status": "ok", "problems": [], "message": "Cannot read a file."},
            False,
            id="failure-with-success-status",
        ),
        pytest.param(
            {"status": "error", "message": "Cannot read a file.", "problems": []},
            False,
            id="failure-with-problems",
        ),
        pytest.param(
            {"status": "ok", "problems": None}, False, id="missing-problem-list"
        ),
    ],
)
def test_output_schema_distinguishes_completed_validation_from_failure(
    result, accepted
):
    """指摘ありは正常な検証結果とし、検証失敗を空の指摘一覧と混同させない。"""
    assert (
        Draft202012Validator(VALIDATION_TOOL_OUTPUT_SCHEMA).is_valid(result) == accepted
    )


@pytest.mark.parametrize(
    "problem",
    [
        {"path": "decision/a.md", "message": "Missing heading ID."},
        {"path": "", "line": 1, "message": "Missing heading ID."},
        {"path": "decision/a.md", "line": 0, "message": "Missing heading ID."},
        {"path": "decision/a.md", "line": True, "message": "Missing heading ID."},
        {"path": "decision/a.md", "line": 1, "message": " "},
        {
            "path": "decision/a.md",
            "line": 1,
            "message": "Missing heading ID.",
            "replacement": "# [DEC-000001] Added decision",
        },
    ],
)
def test_output_schema_requires_problem_locations_and_explanations(problem):
    """修正に必要な位置と説明を要求し、未定義の修正操作を結果へ混入させない。"""
    result = {"status": "ok", "problems": [problem]}
    assert not Draft202012Validator(VALIDATION_TOOL_OUTPUT_SCHEMA).is_valid(result)
