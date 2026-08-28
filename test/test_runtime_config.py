"""CmocConfig の既定値・永続化・入力検証を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/cmoc_config.py
- {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
"""

import os
import sys
from pathlib import Path
from typing import cast

import pytest
from _git_support import make_repo
from oracle.other.cmoc_config import (
    CodexCallConfig,
    CodexModelProviderConfig,
    JsonTomlValue,
)

from cmoc_runtime import (
    CmocError,
    config_from_dict,
    config_to_dict,
    load_config,
    render_error,
    write_config,
)
from config.cmoc_config import CmocConfig


def test_config_defaults_define_direct_settings_for_every_agent_call() -> None:
    """既定の全 agent call 設定が定義済み provider を直接選ぶ。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model_providers == {"openai": CodexModelProviderConfig()}
    assert config.codex.agent_calls
    for agent_call_kind, call_config in config.codex.agent_calls.items():
        assert agent_call_kind
        assert call_config.model_provider in config.codex.model_providers
        assert call_config.model
        assert call_config.reasoning_effort
    assert config.oracle_review.num_enumerate_findings_loop == 2
    assert config.oracle_review.num_merge_findings_loop == 2
    assert config.oracle_review.num_validate_findings_loop == 2


def test_config_json_preserves_oracle_member_order() -> None:
    """config の JSON 化で agent call 直接設定の定義順を保つ。"""
    config = CmocConfig()
    data = config_to_dict(config)

    assert list(data) == [
        "num_parallel",
        "codex",
        "oracle_review",
    ]
    assert list(data["codex"]) == [
        "model_providers",
        "agent_calls",
    ]
    assert list(data["codex"]["agent_calls"]) == list(config.codex.agent_calls)


def test_load_config_missing_points_to_doctor(tmp_path: Path) -> None:
    """設定ファイルがない場合に doctor の実行を案内する。"""
    root = make_repo(tmp_path)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config が存在しません。"
    assert exc_info.value.next_actions == [
        "cmoc doctor を実行して {{work-root}}/.cmoc/gt/ar/config.json を生成してください。"
    ]


def test_config_round_trips_through_json_file(tmp_path: Path) -> None:
    """設定を config.json へ保存しても全 section の値を復元できる。"""
    root = make_repo(tmp_path)
    config = config_from_dict(
        {
            "num_parallel": 3,
            "codex": {
                "model_providers": {
                    "provider": {"settings": {"endpoint": "http://127.0.0.1"}}
                },
                "agent_calls": {
                    "custom_call": {
                        "model_provider": "provider",
                        "model": "local-model",
                        "reasoning_effort": "deliberate",
                    }
                },
            },
            "oracle_review": {
                "num_enumerate_findings_loop": 3,
                "num_merge_findings_loop": 4,
                "num_validate_findings_loop": 5,
            },
        }
    )

    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    write_config(config_path, config)

    assert config_to_dict(load_config(root)) == config_to_dict(config)


@pytest.mark.parametrize("payload", [b"{", b"\xff"])
def test_load_config_rejects_unreadable_json(tmp_path: Path, payload: bytes) -> None:
    """JSON 構文または UTF-8 が壊れた config を利用者向けエラーへ変換する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_bytes(payload)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


def test_load_config_rejects_excessively_nested_json(tmp_path: Path) -> None:
    """JSON parser の recursion error を利用者向け設定エラーへ変換する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.parent.mkdir(parents=True)
    depth = sys.getrecursionlimit() * 20
    config_path.write_text("[" * depth + "0" + "]" * depth)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


def test_load_config_rejects_non_file_config_path(tmp_path: Path) -> None:
    """config path が通常ファイルでない場合も読み込みエラーへ変換する。"""
    root = make_repo(tmp_path)
    (root / ".cmoc" / "gt" / "ar" / "config.json").mkdir(parents=True)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


@pytest.mark.parametrize("data", [[], "invalid", set()])
def test_config_rejects_non_object_top_level(data: object) -> None:
    """直接呼び出しでも top-level の非 object を設定エラーへ変換する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(cast(dict[str, object], data))

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_config_rejects_named_pipe_config_path(tmp_path: Path) -> None:
    """config path が named pipe の場合に read/write で block しない。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.parent.mkdir(parents=True)
    os.mkfifo(config_path)

    with pytest.raises(CmocError, match="cmoc config JSON"):
        load_config(root)
    with pytest.raises(CmocError, match="cmoc config path"):
        write_config(config_path, CmocConfig())


def test_config_rejects_symlinked_path_without_touching_link_target(
    tmp_path: Path,
) -> None:
    """tracked config の symlink 経由 read/write で link 先を扱わない。"""
    root = make_repo(tmp_path)
    outside = tmp_path / "outside-config.json"
    outside.write_text("original\n")
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.parent.mkdir(parents=True)
    config_path.symlink_to(outside)

    with pytest.raises(CmocError, match="cmoc config path"):
        load_config(root)
    with pytest.raises(CmocError, match="cmoc config path"):
        write_config(config_path, CmocConfig())

    assert outside.read_text() == "original\n"


@pytest.mark.parametrize("value", [False, None, [], "gpt"])
def test_config_rejects_non_object_codex_agent_call_settings(value: object) -> None:
    """agent call 設定に object 以外を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"agent_calls": {"custom_call": value}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model_provider", False),
        ("model_provider", None),
        ("model_provider", []),
        ("model_provider", ""),
        ("model_provider", "  "),
        ("model_provider", "\ud800"),
        ("model", ""),
        ("model", "  "),
        ("model", None),
        ("model", "\x00"),
        ("model", "\ud800"),
        ("reasoning_effort", False),
        ("reasoning_effort", None),
        ("reasoning_effort", []),
        ("reasoning_effort", {}),
        ("reasoning_effort", ""),
        ("reasoning_effort", "  "),
        ("reasoning_effort", "\ud800"),
    ],
)
def test_config_rejects_invalid_codex_agent_call_settings(
    field: str,
    value: object,
) -> None:
    """直接設定の必須文字列が不正な config を拒否する。"""
    call_config: dict[str, object] = {
        "model_provider": "openai",
        "model": "gpt-model",
        "reasoning_effort": "high",
    }
    call_config[field] = value
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"agent_calls": {"custom_call": call_config}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_invalid_config_error_report_escapes_surrogate() -> None:
    """不正な surrogate を含む設定でも error report を UTF-8 出力できる。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(
            {
                "codex": {
                    "agent_calls": {
                        "custom_call": {
                            "model_provider": "openai",
                            "model": "\ud800",
                            "reasoning_effort": "high",
                        }
                    }
                }
            }
        )

    report = render_error(exc_info.value)
    report.encode("utf-8")
    assert "\\ud800" in report


@pytest.mark.parametrize("field", ["model_providers", "agent_calls"])
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
                "agent_calls": {
                    "custom_call": {
                        "model_provider": "provider.with.dot",
                        "model": "local-model",
                        "reasoning_effort": "deliberate",
                    }
                },
            }
        }
    )

    assert config.codex.model_providers == {
        "openai": CodexModelProviderConfig(),
        "provider.with.dot": CodexModelProviderConfig(settings),
        "builtin": CodexModelProviderConfig(),
    }
    assert config.codex.agent_calls["custom_call"] == CodexCallConfig(
        "provider.with.dot", "local-model", "deliberate"
    )
    assert config_to_dict(config)["codex"]["model_providers"] == {
        "openai": {"settings": {}},
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


def test_config_rejects_excessively_nested_provider_setting() -> None:
    """深すぎる provider-local 値を利用者向け設定エラーへ変換する。"""
    nested: object = 0
    for _ in range(sys.getrecursionlimit()):
        nested = [nested]

    with pytest.raises(CmocError) as exc_info:
        config_from_dict(
            {
                "codex": {
                    "model_providers": {"provider": {"settings": {"nested": nested}}}
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


@pytest.mark.parametrize("model", ["\x00", "\ud800"])
def test_config_to_dict_rejects_unusable_in_memory_model_name(model: str) -> None:
    """型注釈を迂回した model 名も永続化境界で拒否する。"""
    config = CmocConfig()
    config.codex.agent_calls["custom_call"] = CodexCallConfig("openai", model, "high")

    with pytest.raises(TypeError):
        config_to_dict(config)


def test_config_drops_legacy_codex_model_class_maps() -> None:
    """旧 model class と reasoning effort map を永続設定から除外する。"""
    config = config_from_dict(
        {
            "codex": {
                "model": {"minimum": {"model": "legacy"}},
                "reasoning_effort": {"low": "legacy"},
            }
        }
    )

    codex_data = config_to_dict(config)["codex"]
    assert "model" not in codex_data
    assert "reasoning_effort" not in codex_data


@pytest.mark.parametrize("value", [4, True, "1", None])
def test_config_drops_legacy_codex_falv_recovery_try_count(value: object) -> None:
    """廃止済みの recovery 試行回数を config JSON の公開面から除外する。"""
    config = config_from_dict({"codex": {"num_try_falv_recovery": value}})

    assert "num_try_falv_recovery" not in config_to_dict(config)["codex"]
