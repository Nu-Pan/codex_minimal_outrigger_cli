"""CmocConfig の既定値・永続化・入力検証を検証する。

この file は 16,000 文字を超えるが、既定値、JSON 変換、merge、および入力拒否は
同じ config schema と round-trip 契約を共有する。分割すると、設定 field ごとの
受理条件と永続化結果が複数 file に分散するため、一つの config 回帰として保つ。

根拠:
- {{work-root}}/oracle/src/oracle/other/cmoc_config.py
- {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
"""

import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import cast

import pytest
from _git_support import make_repo
from oracle.other.cmoc_config import (
    CodexCallConfig,
    CodexModelProviderConfig,
    JsonTomlValue,
)
from oracle.other.document_search import (
    SEARCH_CANDIDATE_COUNT_MAX,
    SEARCH_CANDIDATE_COUNT_MIN,
    DocumentSearchConfig,
)

from cmoc_runtime import (
    CmocError,
    config_from_dict,
    config_to_dict,
    load_config,
    render_error,
    sync_config,
    write_config,
)
from config.cmoc_config import CmocConfig


def test_config_defaults_define_direct_settings_for_every_agent_call() -> None:
    """全 agent call の正本既定値を設定補完と JSON 変換で保持する。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model_providers == {"openai": CodexModelProviderConfig()}
    assert config.codex.agent_calls
    for agent_call_kind, call_config in config.codex.agent_calls.items():
        assert agent_call_kind
        assert call_config.model_provider in config.codex.model_providers
        assert call_config.model
        assert call_config.reasoning_effort
    restored = config_from_dict({})
    assert restored.codex.agent_calls == config.codex.agent_calls
    assert config_to_dict(restored)["codex"]["agent_calls"] == {
        agent_call_kind: asdict(call_config)
        for agent_call_kind, call_config in config.codex.agent_calls.items()
    }


def test_config_json_preserves_oracle_member_order() -> None:
    """config の JSON 化で agent call 直接設定の定義順を保つ。"""
    config = CmocConfig()
    data = config_to_dict(config)

    assert list(data) == [
        "num_parallel",
        "codex",
        "document_search",
    ]
    assert list(data["codex"]) == [
        "model_providers",
        "agent_calls",
        "num_try_falv_recovery",
    ]
    assert list(data["codex"]["agent_calls"]) == list(config.codex.agent_calls)


@pytest.mark.parametrize("legacy_config", [False, True])
def test_load_config_missing_points_to_doctor(
    tmp_path: Path, legacy_config: bool
) -> None:
    """新配置に設定がなければ、旧配置に依存せず doctor の実行を案内する。"""
    root = tmp_path
    if legacy_config:
        write_config(root / ".cmoc/gt/ar/config.json", CmocConfig())

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "文書検索の設定が不足または不正です。"
    assert str(root / ".cmoc/gt/config.json") in exc_info.value.detail
    assert "document_search" in exc_info.value.detail
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert not (root / ".cmoc/gt/config.json").exists()


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
        }
    )

    config_path = root / ".cmoc" / "gt" / "config.json"
    write_config(config_path, config)

    assert config_to_dict(load_config(root)) == config_to_dict(config)


def test_saved_search_config_is_not_filled_by_deserialization_defaults(
    tmp_path: Path,
) -> None:
    """通常起動はメモリ内既定値で保存済み設定の不足を隠さない。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"num_parallel": 3}\n')

    assert (
        config_from_dict({"num_parallel": 3}).document_search == DocumentSearchConfig()
    )
    with pytest.raises(CmocError) as exc_info:
        sync_config(root)

    assert str(path) in exc_info.value.detail
    assert "document_search" in exc_info.value.detail
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert path.read_text() == '{"num_parallel": 3}\n'


def test_normal_startup_rejects_partial_saved_search_config(tmp_path: Path) -> None:
    """検索 object の一部だけがある場合も通常起動では補完しない。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = '{"document_search": {"chunk_tokens": 256}}\n'
    path.write_text(original)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert "document_search.batch_tokens" in exc_info.value.detail
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert path.read_text() == original


def test_explicit_doctor_fills_only_missing_search_fields(tmp_path: Path) -> None:
    """人間が指定した値を保ち、不足項目だけを補完して再実行で書き換えない。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    data = config_to_dict(CmocConfig())
    data["num_parallel"] = 3
    data["document_search"] = {"chunk_tokens": 256}
    path.write_text(json.dumps(data) + "\n")

    repaired = sync_config(root, repair_missing=True)

    assert repaired.generated is False
    assert repaired.saved is True
    assert repaired.additions == {
        name: value
        for name, value in asdict(DocumentSearchConfig()).items()
        if name != "chunk_tokens"
    }
    assert repaired.config.num_parallel == 3
    assert repaired.config.document_search.chunk_tokens == 256
    saved = path.read_bytes()
    mtime = path.stat().st_mtime_ns

    repeated = sync_config(root, repair_missing=True)
    assert repeated.saved is False
    assert repeated.additions == {}
    assert path.read_bytes() == saved
    assert path.stat().st_mtime_ns == mtime


def test_saved_agent_call_settings_require_all_call_kinds_and_provider_definitions(
    tmp_path: Path,
) -> None:
    """通常起動と明示 doctor は既存の agent call 設定を暗黙補完しない。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    data = config_to_dict(CmocConfig())
    data["codex"]["agent_calls"].pop("build_tui_launch_tui_parameter")
    path.write_text(json.dumps(data) + "\n")

    for repair_missing in (False, True):
        with pytest.raises(CmocError) as exc_info:
            sync_config(root, repair_missing=repair_missing)
        assert (
            "codex.agent_calls.build_tui_launch_tui_parameter" in exc_info.value.detail
        )

    data = config_to_dict(CmocConfig())
    data["codex"]["agent_calls"]["build_tui_launch_tui_parameter"]["model_provider"] = (
        "missing"
    )
    path.write_text(json.dumps(data) + "\n")
    with pytest.raises(CmocError) as exc_info:
        load_config(root)
    assert (
        "codex.agent_calls.build_tui_launch_tui_parameter.model_provider"
        in exc_info.value.detail
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("chunk_tokens", None),
        ("chunk_tokens", True),
        ("startup_timeout_seconds", 0),
        ("resource_wait_timeout_seconds", True),
        ("sync_no_progress_timeout_seconds", 0),
        ("post_sync_search_timeout_seconds", -1),
        ("search_request_timeout_seconds", "3600"),
        ("chunk_overlap_tokens", 512),
        ("embedding_context_tokens", 512),
        ("reranker_context_tokens", 512),
        ("candidate_count", 0),
        ("candidate_count", -1),
        ("candidate_count", 8),
        ("candidate_count", 19),
        ("candidate_count", 51),
        ("candidate_count", 20.5),
        ("candidate_count", True),
    ],
)
def test_saved_search_config_rejects_invalid_explicit_values(
    tmp_path: Path, field: str, value: object
) -> None:
    """null・bool・値域外・項目間不整合を黙って既定値に置換しない。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    search = asdict(DocumentSearchConfig())
    search[field] = value
    path.write_text(json.dumps({"document_search": search}) + "\n")

    original = path.read_text()
    for repair_missing in (False, True):
        with pytest.raises(CmocError) as exc_info:
            sync_config(root, repair_missing=repair_missing)

        assert str(path) in exc_info.value.detail
        assert f"document_search.{field}" in exc_info.value.detail
        assert "手動で修正" in exc_info.value.next_actions[0]
        if field == "candidate_count":
            reason = exc_info.value.detail.split("\nreason:", 1)[1]
            assert str(SEARCH_CANDIDATE_COUNT_MIN) in reason
            assert str(SEARCH_CANDIDATE_COUNT_MAX) in reason
        assert path.read_text() == original


def test_explicit_doctor_adds_request_deadlines_without_replacing_validation_timeout(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    data = config_to_dict(CmocConfig())
    names = (
        "resource_wait_timeout_seconds",
        "sync_no_progress_timeout_seconds",
        "post_sync_search_timeout_seconds",
        "search_request_timeout_seconds",
    )
    for name in names:
        data["document_search"].pop(name)
    data["document_search"]["request_timeout_seconds"] = 37
    original = json.dumps(data) + "\n"
    path.write_text(original)
    with pytest.raises(CmocError):
        load_config(root)
    with pytest.raises(CmocError):
        sync_config(root, repair_missing=False)
    assert path.read_text() == original
    repaired = sync_config(root, repair_missing=True)
    saved = json.loads(path.read_text())
    assert repaired.config.document_search.request_timeout_seconds == 37
    defaults = asdict(DocumentSearchConfig())
    assert all(saved["document_search"][name] == defaults[name] for name in names)
    assert repaired.additions == {name: defaults[name] for name in names}


def test_explicit_doctor_does_not_save_inconsistent_candidate(tmp_path: Path) -> None:
    """既存 context と暫定 chunk が衝突しても候補を保存しない。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = '{"document_search": {"embedding_context_tokens": 256}}\n'
    path.write_text(original)

    with pytest.raises(CmocError) as exc_info:
        sync_config(root, repair_missing=True)

    assert "chunk_tokens=512" in exc_info.value.detail
    assert "embedding_context_tokens=256" in exc_info.value.detail
    assert "手動で修正" in exc_info.value.next_actions[0]
    assert path.read_text() == original


@pytest.mark.parametrize(
    "payload",
    [
        b"{",
        b"\xff",
        b'{"unused": NaN}',
        b'{"unused": Infinity}',
        b'{"unused": -Infinity}',
    ],
)
def test_load_config_rejects_unreadable_json(tmp_path: Path, payload: bytes) -> None:
    """壊れた JSON または UTF-8 の config を利用者向けエラーへ変換する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "config.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_bytes(payload)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


def test_load_config_rejects_excessively_nested_json(tmp_path: Path) -> None:
    """JSON parser の recursion error を利用者向け設定エラーへ変換する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "config.json"
    config_path.parent.mkdir(parents=True)
    depth = sys.getrecursionlimit() * 20
    config_path.write_text("[" * depth + "0" + "]" * depth)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


def test_load_config_rejects_non_file_config_path(tmp_path: Path) -> None:
    """config path が通常ファイルでない場合も読み込みエラーへ変換する。"""
    root = make_repo(tmp_path)
    (root / ".cmoc" / "gt" / "config.json").mkdir(parents=True)

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
    config_path = root / ".cmoc" / "gt" / "config.json"
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
    config_path = root / ".cmoc" / "gt" / "config.json"
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


@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_codex_section(value: object) -> None:
    """codex section にオブジェクト以外を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": value})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "data",
    [
        {"num_parallel": True},
        {"num_parallel": "3"},
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


def test_config_preserves_codex_falv_recovery_try_count() -> None:
    """codex の recovery 試行回数を読み込みと JSON 化の両方で保持する。"""
    config = config_from_dict({"codex": {"num_try_falv_recovery": 4}})

    assert config.codex.num_try_falv_recovery == 4
    assert config_to_dict(config)["codex"]["num_try_falv_recovery"] == 4


@pytest.mark.parametrize("value", [True, "1", None])
def test_config_rejects_invalid_codex_falv_recovery_try_count(value: object) -> None:
    """recovery 試行回数へ int 以外を指定した config を拒否する。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {"num_try_falv_recovery": value}})

    assert exc_info.value.summary == "cmoc config が不正です。"
