"""CmocConfig の既定値・永続化・入力検証を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/cmoc_config.py
- {{work-root}}/oracle/doc/app_spec/error_handling.md
"""

from pathlib import Path
from typing import cast

import pytest
from _git_support import make_repo
from oracle.other.cmoc_config import (
    CodexModelProviderConfig,
    CodexModelSpec,
    JsonTomlValue,
)

from basic.acp import ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, config_from_dict, config_to_dict, load_config
from config.cmoc_config import CmocConfig


def test_config_defaults_match_logical_model_classes() -> None:
    """既定 config が論理 model class と reasoning effort を埋める。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model_providers == {}
    assert config.codex.model[ModelClass.MAINSTREAM] == CodexModelSpec(
        None, "gpt-5.6-terra"
    )
    assert config.codex.reasoning_effort[ReasoningEffort.HIGH] == "high"
    assert config.codex.reasoning_effort[ReasoningEffort.XHIGH] == "xhigh"
    assert config.codex.reasoning_effort[ReasoningEffort.MAX] == "max"
    assert config.codex.num_try_falv_recovery == 1


def test_config_json_preserves_oracle_member_order() -> None:
    """config の JSON 化で model と reasoning effort の定義順を保つ。"""
    data = config_to_dict(CmocConfig())

    assert list(data) == [
        "num_parallel",
        "codex",
        "oracle_review",
    ]
    assert list(data["codex"]) == [
        "model_providers",
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
    """設定ファイルがない場合に doctor の実行を案内する。"""
    root = make_repo(tmp_path)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config が存在しません。"
    assert exc_info.value.next_actions == [
        "cmoc doctor を実行して {{work-root}}/.cmoc/gt/ar/config.json を生成してください。"
    ]


@pytest.mark.parametrize("value", [False, None, [], "gpt"])
def test_config_rejects_non_object_codex_model_specs(value: object) -> None:
    """model の値にオブジェクト以外を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"model": {"mainstream": value}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "spec",
    [
        {"model_provider": False, "model": "gpt-5.5"},
        {"model_provider": [], "model": "gpt-5.5"},
        {"model_provider": "provider", "model": ""},
        {"model_provider": "provider", "model": "  "},
        {"model_provider": "provider", "model": None},
    ],
)
def test_config_rejects_invalid_codex_model_specs(
    spec: dict[str, object],
) -> None:
    """model provider 型や model 名が不正な config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"model": {"mainstream": spec}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("value", [False, None, [], {}, "", "  "])
def test_config_rejects_non_string_reasoning_effort_names(value: object) -> None:
    """reasoning effort 名に文字列以外や空文字列を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"reasoning_effort": {"low": value}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("field", ["model_providers", "model", "reasoning_effort"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_codex_name_maps(field: str, value: object) -> None:
    """codex の map field にオブジェクト以外を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {field: value}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "providers",
    [
        {"provider": None},
        {"provider": {"settings": None}},
        {"provider": {"settings": []}},
    ],
)
def test_config_rejects_invalid_model_provider_definitions(
    providers: object,
) -> None:
    """provider 定義と settings に object 以外を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"model_providers": providers}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("section", ["codex", "oracle_review"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_sections(section: str, value: object) -> None:
    """各設定 section にオブジェクト以外を指定した config を拒否する。"""
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
        {"oracle_review": {"num_enumerate_findings_loop": False}},
        {"oracle_review": {"num_enumerate_findings_loop": "2"}},
        {"oracle_review": {"num_merge_findings_loop": True}},
        {"oracle_review": {"num_merge_findings_loop": "2"}},
        {"oracle_review": {"num_validate_findings_loop": False}},
        {"oracle_review": {"num_validate_findings_loop": "2"}},
    ],
)
def test_config_rejects_non_integer_int_values(data: dict[str, object]) -> None:
    """整数を要求する設定項目が bool や文字列を受け入れない。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(data)

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_config_preserves_generic_model_provider_settings() -> None:
    """任意 ID と再帰的な JSON/TOML 共通値を読み込みと JSON 化で保持する。"""
    settings: dict[str, JsonTomlValue] = {
        "name.with.dot": "local provider",
        "enabled": True,
        "retries": 2,
        "ratio": 0.5,
        "nested": ["value", {"answer": 42}],
    }
    config = config_from_dict(
        {
            "codex": {
                "model_providers": {
                    "provider.with.dot": {"settings": settings},
                    "builtin": {},
                },
                "model": {
                    "minimum": {
                        "model_provider": "provider.with.dot",
                        "model": "local-model",
                    }
                },
            }
        }
    )

    assert config.codex.model_providers == {
        "provider.with.dot": CodexModelProviderConfig(settings),
        "builtin": CodexModelProviderConfig(),
    }
    assert config.codex.model[ModelClass.MINIMUM] == CodexModelSpec(
        "provider.with.dot", "local-model"
    )
    assert config_to_dict(config)["codex"]["model_providers"] == {
        "provider.with.dot": {"settings": settings},
        "builtin": {"settings": {}},
    }


@pytest.mark.parametrize(
    "setting",
    [None, float("nan"), float("inf"), 2**63, object()],
)
def test_config_rejects_values_without_unique_json_toml_encoding(
    setting: object,
) -> None:
    """null、非有限数、範囲外整数などを provider-local 値として拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(
            {
                "codex": {
                    "model_providers": {"provider": {"settings": {"setting": setting}}}
                }
            }
        )

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_config_to_dict_rejects_invalid_in_memory_provider_setting() -> None:
    """型注釈を迂回した null も永続化境界では拒否する。"""
    config = CmocConfig()
    config.codex.model_providers["provider"] = CodexModelProviderConfig(
        {"setting": cast(JsonTomlValue, None)}
    )

    with pytest.raises(TypeError):
        config_to_dict(config)


def test_config_preserves_codex_falv_recovery_try_count() -> None:
    """codex の recovery 試行回数を読み込みと JSON 化の両方で保持する。"""
    config = config_from_dict({"codex": {"num_try_falv_recovery": 4}})

    assert config.codex.num_try_falv_recovery == 4
    assert config_to_dict(config)["codex"]["num_try_falv_recovery"] == 4
