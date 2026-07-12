"""CmocConfig の既定値・永続化・入力検証を検証する。

根拠:
- <work-root>/oracle/src/oracle/other/cmoc_config.py
- <work-root>/oracle/doc/app_spec/error_handling.md
"""

from pathlib import Path

import pytest

from basic.acp import ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, config_from_dict, config_to_dict, load_config
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from _git_support import make_repo


def test_config_defaults_match_logical_model_classes() -> None:
    """既定 config が論理 model class と reasoning effort を埋める。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model[ModelClass.MAINSTREAM] == CodexModelSpec(
        "codex", "gpt-5.6-terra"
    )
    assert config.codex.reasoning_effort[ReasoningEffort.HIGH] == "high"
    assert config.codex.reasoning_effort[ReasoningEffort.XHIGH] == "xhigh"
    assert config.codex.reasoning_effort[ReasoningEffort.MAX] == "max"
    assert config.codex.num_try_falv_recovery == 1


def test_config_json_preserves_oracle_member_order() -> None:
    data = config_to_dict(CmocConfig())

    assert list(data["codex"]) == [
        "model",
        "reasoning_effort",
        "num_try_falv_recovery",
    ]
    assert list(data["codex"]["model"]) == [
        "mainstream",
        "flagship",
        "efficiency",
        "minimum",
    ]
    assert list(data["codex"]["reasoning_effort"]) == [
        "low",
        "medium",
        "high",
        "xhigh",
        "max",
    ]


def test_load_config_missing_points_to_doctor(tmp_path: Path) -> None:
    root = make_repo(tmp_path)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config が存在しません。"
    assert exc_info.value.next_actions == [
        "cmoc doctor を実行して <repo-root>/.cmoc/config.json を生成してください。"
    ]


@pytest.mark.parametrize("value", [False, None, [], "gpt"])
def test_config_rejects_non_object_codex_model_specs(value: object) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"model": {"mainstream": value}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "spec",
    [
        {"model_provider": "bad", "model": "gpt-5.5"},
        {"model_provider": "codex", "model": ""},
        {"model_provider": "codex", "model": "  "},
        {"model_provider": "codex", "model": None},
    ],
)
def test_config_rejects_invalid_codex_model_specs(
    spec: dict[str, object],
) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"model": {"mainstream": spec}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("value", [False, None, [], {}, "", "  "])
def test_config_rejects_non_string_reasoning_effort_names(value: object) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"reasoning_effort": {"low": value}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("field", ["model", "reasoning_effort"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_codex_name_maps(
    field: str, value: object
) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {field: value}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("section", ["codex", "apply_fork", "review_oracle"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_sections(section: str, value: object) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({section: value})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "data",
    [
        {"num_parallel": True},
        {"num_parallel": "3"},
        {"codex": {"num_try_falv_recovery": True}},
        {"codex": {"num_try_falv_recovery": "1"}},
        {"apply_fork": {"num_apply_files": True}},
        {"apply_fork": {"num_apply_files": "200"}},
        {"review_oracle": {"num_enumerate_findings_loop": False}},
        {"review_oracle": {"num_enumerate_findings_loop": "2"}},
        {"review_oracle": {"num_merge_findings_loop": True}},
        {"review_oracle": {"num_merge_findings_loop": "2"}},
        {"review_oracle": {"num_validate_findings_loop": False}},
        {"review_oracle": {"num_validate_findings_loop": "2"}},
    ],
)
def test_config_rejects_non_integer_int_values(data: dict[str, object]) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(data)

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_config_preserves_codex_falv_recovery_try_count() -> None:
    config = config_from_dict({"codex": {"num_try_falv_recovery": 4}})

    assert config.codex.num_try_falv_recovery == 4
    assert config_to_dict(config)["codex"]["num_try_falv_recovery"] == 4
