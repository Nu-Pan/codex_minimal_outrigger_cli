"""CmocConfig の既定値・永続化・入力検証を検証する。

設定 I/O は通常の directory で検証し、Git 追跡は test_doctor_cli.py で扱う。

この file は 16,000 文字を超えるが、既定値、JSON 変換、保存、および入力拒否は
同じ config schema と round-trip 契約を共有する。分割すると、設定 field ごとの
受理条件と永続化結果が複数 file に分散するため、一つの config 回帰として保つ。

根拠:
- {{work-root}}/reference/src/oracle/other/cmoc_config.py
- {{work-root}}/spec/app_spec/codex_model_provider.md
- {{work-root}}/spec/app_spec/error_handling.md
"""

import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import cast

import pytest
from oracle.other.cmoc_config import (
    CodexCallConfig,
    CodexModelProviderConfig,
    DocumentSearchConfig,
    JsonTomlValue,
)
from oracle.other.document_search import (
    SEARCH_CANDIDATE_COUNT_MAX,
    SEARCH_CANDIDATE_COUNT_MIN,
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
from commons.runtime_config import SearchConfigIssue
from config.cmoc_config import CmocConfig


@pytest.fixture
def config_data():
    """検証対象の項目以外は正本の既定状態で満たす。"""
    return config_to_dict(CmocConfig())


def test_config_defaults_define_direct_settings_for_every_agent_call() -> None:
    """共有設定と7種の個別設定の正本既定値を JSON 変換で保持する。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model_providers == {"openai": CodexModelProviderConfig()}
    assert set(config.codex.agent_calls) == {
        "realization_edit",
        "build_session_join_conflict_resolution_request",
        "build_tui_request",
        "build_decision_plan_request",
        "build_oracle_edit_request",
        "build_feedback_issue_normalization_request",
        "build_primary_report_review_request",
        "build_quota_availability_probe_request",
    }
    for agent_call_kind, call_config in config.codex.agent_calls.items():
        assert agent_call_kind
        assert call_config.model_provider in config.codex.model_providers
        assert call_config.model
        assert call_config.reasoning_effort
    restored = config_from_dict(config_to_dict(config))
    assert restored.codex.agent_calls == config.codex.agent_calls
    assert config_to_dict(restored)["codex"]["agent_calls"] == {
        agent_call_kind: asdict(call_config)
        for agent_call_kind, call_config in config.codex.agent_calls.items()
    }


def test_config_json_preserves_oracle_member_order() -> None:
    """config の JSON 化で agent call 直接設定の定義順を保つ。"""
    config = CmocConfig(document_search=DocumentSearchConfig(chunk_tokens=256))
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
    assert list(data["document_search"]) == list(asdict(config.document_search))

    # 保存済み object の順序が異なっても、値を保持して正本の定義順へ戻す。
    data["document_search"] = dict(reversed(data["document_search"].items()))
    restored = config_from_dict(data)
    assert restored.document_search == config.document_search
    assert list(config_to_dict(restored)["document_search"]) == list(
        asdict(config.document_search)
    )


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


def test_config_round_trips_through_json_file(tmp_path: Path, config_data) -> None:
    """設定を config.json へ保存しても全 section の値を復元できる。"""
    root = tmp_path / "repo"
    config_data["num_parallel"] = 3
    config_data["codex"]["model_providers"]["provider"] = {
        "settings": {"endpoint": "http://127.0.0.1"}
    }
    config_data["codex"]["agent_calls"]["realization_edit"] = {
        "model_provider": "provider",
        "model": "local-model",
        "reasoning_effort": "deliberate",
    }
    config = config_from_dict(config_data)

    config_path = root / ".cmoc" / "gt" / "config.json"
    write_config(config_path, config)

    assert config_to_dict(load_config(root)) == config_to_dict(config)


def test_saved_search_config_is_not_filled_by_deserialization_defaults(
    tmp_path: Path,
) -> None:
    """通常起動はメモリ内既定値で保存済み設定の不足を隠さない。"""
    root = tmp_path / "repo"
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"num_parallel": 3}\n')

    with pytest.raises(CmocError):
        config_from_dict({"num_parallel": 3})
    with pytest.raises(CmocError) as exc_info:
        sync_config(root)

    assert str(path) in exc_info.value.detail
    assert "document_search" in exc_info.value.detail
    assert "cmoc doctor" in exc_info.value.next_actions[0]
    assert path.read_text() == '{"num_parallel": 3}\n'


def test_normal_startup_rejects_partial_saved_search_config(tmp_path: Path) -> None:
    """検索 object の一部だけがある場合も通常起動では補完しない。"""
    root = tmp_path / "repo"
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
    root = tmp_path / "repo"
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
    root = tmp_path / "repo"
    path = root / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    data = config_to_dict(CmocConfig())
    data["codex"]["agent_calls"].pop("build_tui_request")
    path.write_text(json.dumps(data) + "\n")

    for repair_missing in (False, True):
        with pytest.raises(CmocError) as exc_info:
            sync_config(root, repair_missing=repair_missing)
        assert "codex.agent_calls.build_tui_request" in exc_info.value.detail

    data = config_to_dict(CmocConfig())
    data["codex"]["agent_calls"]["build_tui_request"]["model_provider"] = "missing"
    path.write_text(json.dumps(data) + "\n")
    with pytest.raises(CmocError) as exc_info:
        load_config(root)
    assert "codex.agent_calls.build_tui_request.model_provider" in exc_info.value.detail


@pytest.mark.parametrize("kind", list(CmocConfig().codex.agent_calls))
def test_saved_config_rejects_missing_call_without_doctor_completion(
    tmp_path, config_data, kind
):
    """共有設定も個別設定も必須とし、検索の補完候補があっても保存しない。"""
    path = tmp_path / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    del config_data["codex"]["agent_calls"][kind]
    del config_data["document_search"]["chunk_tokens"]
    original = json.dumps(config_data) + "\n"
    path.write_text(original)

    with pytest.raises(CmocError) as error:
        config_from_dict(config_data)
    assert f"codex.agent_calls.{kind}" in error.value.detail
    with pytest.raises(CmocError) as error:
        sync_config(tmp_path, repair_missing=True)
    assert f"codex.agent_calls.{kind}" in error.value.detail
    assert str(path) in error.value.detail
    assert "手動" in error.value.next_actions[0]
    assert path.read_text() == original


@pytest.mark.parametrize(
    "kind",
    [
        "build_decision_apply_request",
        "build_realization_refactor_request",
        "build_feedback_issue_remediation_request",
        "build_run_join_conflict_resolution_request",
        "custom_call",
    ],
)
@pytest.mark.parametrize("replace_shared", [False, True], ids=["extra", "replacement"])
def test_saved_config_rejects_unrecognized_call_keys(
    tmp_path, config_data, kind, replace_shared
):
    """builder 別 entry と未知の種別を、追加・共有設定の代用のどちらでも拒否する。"""
    calls = config_data["codex"]["agent_calls"]
    calls[kind] = dict(calls["realization_edit"])
    if replace_shared:
        del calls["realization_edit"]
    path = tmp_path / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = json.dumps(config_data) + "\n"
    path.write_text(original)

    for repair_missing in (False, True):
        with pytest.raises(CmocError) as error:
            sync_config(tmp_path, repair_missing=repair_missing)
        field = "realization_edit" if replace_shared else kind
        assert f"codex.agent_calls.{field}" in error.value.detail
        assert path.read_text() == original


@pytest.mark.parametrize(
    "location",
    [
        (),
        ("codex",),
        ("codex", "agent_calls", "realization_edit"),
        ("codex", "model_providers", "openai"),
    ],
)
@pytest.mark.parametrize("operation", ["missing", "unknown", "replacement"])
def test_config_validates_record_fields_without_defaults(
    tmp_path, config_data, location, operation
):
    """項目数が同じ置換も拒否し、欠落の診断と保存内容を保つ。"""
    record = config_data
    for field in location:
        record = record[field]
    if operation in ("missing", "replacement"):
        field = next(iter(record))
        del record[field]
    if operation == "unknown":
        field = "overrides"
    if operation in ("unknown", "replacement"):
        record["overrides"] = {"model": "per-call-model"}
    path = tmp_path / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = json.dumps(config_data) + "\n"
    path.write_text(original)

    for repair_missing in (False, True):
        with pytest.raises(CmocError) as error:
            sync_config(tmp_path, repair_missing=repair_missing)
        record_name = ".".join(location) or "config"
        assert f"reason: {record_name}.{field}:" in error.value.detail
        assert path.read_text() == original


def test_config_rejects_missing_provider_without_inserting_builtin(
    tmp_path, config_data
):
    """組み込み provider も定義が必須で、doctor は暗黙に追加しない。"""
    config_data["codex"]["model_providers"].clear()
    path = tmp_path / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = json.dumps(config_data) + "\n"
    path.write_text(original)

    for repair_missing in (False, True):
        with pytest.raises(CmocError) as error:
            sync_config(tmp_path, repair_missing=repair_missing)
        assert "model_provider" in error.value.detail
        assert path.read_text() == original


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
    root = tmp_path / "repo"
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


def test_saved_search_config_rejects_same_size_field_replacement(tmp_path, config_data):
    """欠落と未知項目が同時にあっても未知項目の除去を案内し、保存しない。"""
    search = config_data["document_search"]
    del search["chunk_tokens"]
    search["reranker_context_tokens"] = 512
    path = tmp_path / ".cmoc/gt/config.json"
    path.parent.mkdir(parents=True)
    original = json.dumps(config_data) + "\n"
    path.write_text(original)

    for repair_missing in (False, True):
        with pytest.raises(CmocError) as error:
            sync_config(tmp_path, repair_missing=repair_missing)
        assert "item: document_search.reranker_context_tokens\n" in error.value.detail
        assert "手動で修正" in error.value.next_actions[0]
        assert path.read_text() == original


def test_explicit_doctor_adds_request_deadlines_without_replacing_validation_timeout(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
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
    root = tmp_path / "repo"
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
    root = tmp_path / "repo"
    config_path = root / ".cmoc" / "gt" / "config.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_bytes(payload)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


def test_load_config_rejects_excessively_nested_json(tmp_path: Path) -> None:
    """JSON parser の recursion error を利用者向け設定エラーへ変換する。"""
    root = tmp_path / "repo"
    config_path = root / ".cmoc" / "gt" / "config.json"
    config_path.parent.mkdir(parents=True)
    depth = sys.getrecursionlimit() * 20
    config_path.write_text("[" * depth + "0" + "]" * depth)

    with pytest.raises(CmocError) as exc_info:
        load_config(root)

    assert exc_info.value.summary == "cmoc config JSON を読み込めません。"


def test_load_config_rejects_non_file_config_path(tmp_path: Path) -> None:
    """config path が通常ファイルでない場合も読み込みエラーへ変換する。"""
    root = tmp_path / "repo"
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
    root = tmp_path / "repo"
    config_path = root / ".cmoc" / "gt" / "config.json"
    config_path.parent.mkdir(parents=True)
    os.mkfifo(config_path)

    with pytest.raises(CmocError, match="cmoc config JSON"):
        load_config(root)
    with pytest.raises(CmocError, match="cmoc config path"):
        write_config(config_path, CmocConfig())


@pytest.mark.parametrize("link_kind", ["file", "parent"])
@pytest.mark.parametrize("target_exists", [False, True])
def test_config_rejects_symlinked_path_without_touching_link_target(
    tmp_path: Path,
    link_kind: str,
    target_exists: bool,
) -> None:
    """file・親 directory の symlink は link 先がなくても読み書きしない。"""
    root = tmp_path / "repo"
    config_path = root / ".cmoc" / "gt" / "config.json"
    link = config_path if link_kind == "file" else config_path.parent
    target = tmp_path / "outside"
    outside_config = target if link_kind == "file" else target / "config.json"
    if target_exists:
        outside_config.parent.mkdir(parents=True, exist_ok=True)
        outside_config.write_text("original\n")
    link.parent.mkdir(parents=True)
    link.symlink_to(target, target_is_directory=link_kind == "parent")

    with pytest.raises(CmocError, match="cmoc config path"):
        load_config(root)
    with pytest.raises(CmocError, match="cmoc config path"):
        write_config(config_path, CmocConfig())

    if target_exists:
        assert outside_config.read_text() == "original\n"
    else:
        assert not target.exists()


@pytest.mark.parametrize("value", [False, None, [], "gpt"])
def test_config_rejects_non_object_codex_agent_call_settings(
    config_data, value: object
) -> None:
    """agent call 設定に object 以外を指定した config を拒否する。"""
    config_data["codex"]["agent_calls"]["realization_edit"] = value
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

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
    config_data,
    field: str,
    value: object,
) -> None:
    """不正な必須文字列を拒否し、surrogate の診断も UTF-8 出力できる。"""
    call_config: dict[str, object] = {
        "model_provider": "openai",
        "model": "gpt-model",
        "reasoning_effort": "high",
    }
    call_config[field] = value
    config_data["codex"]["agent_calls"]["realization_edit"] = call_config
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"
    if value == "\ud800":
        report = render_error(exc_info.value)
        report.encode("utf-8")
        assert "\\ud800" in report


@pytest.mark.parametrize("field", ["model_providers", "agent_calls"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_codex_name_maps(
    config_data, field: str, value: object
) -> None:
    """codex の map field にオブジェクト以外を指定した config を拒否する。"""
    config_data["codex"][field] = value
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

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
    config_data,
    providers: object,
) -> None:
    """provider 定義と settings に object 以外を指定した config を拒否する。"""
    config_data["codex"]["model_providers"] = providers
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_codex_section(config_data, value: object) -> None:
    """codex section にオブジェクト以外を指定した config を拒否する。"""
    config_data["codex"] = value
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "data",
    [
        {"num_parallel": True},
        {"num_parallel": "3"},
    ],
)
def test_config_rejects_non_integer_int_values(
    config_data, data: dict[str, object]
) -> None:
    """整数を要求する設定項目が bool や文字列を受け入れない。"""
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({**config_data, **data})

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_config_preserves_generic_model_provider_settings(config_data) -> None:
    """任意 ID と再帰的な JSON/TOML 共通値を読み込みと JSON 化で保持する。"""
    # 同じ container の再出現を循環と誤判定せず、値として保存できる。
    shared = {"answer": 42}
    settings: dict[str, JsonTomlValue] = {
        "name.with.dot": "local provider",
        "enabled": True,
        "retries": 2,
        "ratio": 0.5,
        "nested": ["value", shared, shared],
        "unicode": "\ud7ff\ue000\U0010ffff",
    }
    config_data["codex"]["model_providers"].update(
        {
            "provider.with.dot": {"settings": settings},
            "builtin": {"settings": {}},
        }
    )
    config_data["codex"]["agent_calls"]["realization_edit"] = {
        "model_provider": "provider.with.dot",
        "model": "local-model",
        "reasoning_effort": "deliberate",
    }
    config = config_from_dict(config_data)

    assert config.codex.model_providers == {
        "openai": CodexModelProviderConfig(),
        "provider.with.dot": CodexModelProviderConfig(settings),
        "builtin": CodexModelProviderConfig(),
    }
    assert config.codex.agent_calls["realization_edit"] == CodexCallConfig(
        "provider.with.dot", "local-model", "deliberate"
    )
    assert config_to_dict(config)["codex"]["model_providers"] == {
        "openai": {"settings": {}},
        "provider.with.dot": {"settings": settings},
        "builtin": {"settings": {}},
    }


@pytest.mark.parametrize(
    "setting",
    [None, float("nan"), float("inf"), 2**63, object(), "\udfff", {"\ud800": "value"}],
)
def test_config_rejects_values_without_unique_json_toml_encoding(
    config_data,
    setting: object,
) -> None:
    """null、非有限数、範囲外整数などを provider-local 値として拒否する。"""
    config_data["codex"]["model_providers"]["provider"] = {
        "settings": {"setting": setting}
    }
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_config_rejects_excessively_nested_provider_setting(config_data) -> None:
    """深すぎる provider-local 値を利用者向け設定エラーへ変換する。"""
    nested: object = 0
    for _ in range(sys.getrecursionlimit()):
        nested = [nested]

    config_data["codex"]["model_providers"]["provider"] = {
        "settings": {"nested": nested}
    }
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"
    assert "provider" in exc_info.value.detail
    assert "nested" in exc_info.value.detail
    render_error(exc_info.value).encode("utf-8")


@pytest.mark.parametrize("container_kind", ["list", "dict"])
def test_config_rejects_cyclic_provider_setting(
    config_data, container_kind: str
) -> None:
    """循環値も設定エラーへ変換し、診断を UTF-8 出力できる。"""
    if container_kind == "list":
        setting = []
        setting.append(setting)
    else:
        setting = {}
        setting["self"] = setting

    config_data["codex"]["model_providers"]["provider"] = {
        "settings": {"cycle": setting}
    }
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"
    assert "cycle" in exc_info.value.detail
    render_error(exc_info.value).encode("utf-8")


def test_config_to_dict_rejects_invalid_in_memory_provider_setting() -> None:
    """型注釈を迂回した null も永続化境界では拒否する。"""
    config = CmocConfig()
    config.codex.model_providers["provider"] = CodexModelProviderConfig(
        {"setting": cast(JsonTomlValue, None)}
    )

    with pytest.raises(TypeError):
        config_to_dict(config)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("chunk_tokens", True),
        ("startup_timeout_seconds", float("nan")),
        ("chunk_overlap_tokens", 512),
    ],
)
def test_config_to_dict_rejects_invalid_in_memory_search_config(field, value) -> None:
    """検索 dataclass も JSON 化の前に型・有限性・項目間制約を検証する。"""
    config = CmocConfig(document_search=DocumentSearchConfig(**{field: value}))

    with pytest.raises(SearchConfigIssue) as exc_info:
        config_to_dict(config)

    assert f"document_search.{field}" in exc_info.value.field


@pytest.mark.parametrize("model", ["\x00", "\ud800"])
def test_config_to_dict_rejects_unusable_in_memory_model_name(model: str) -> None:
    """型注釈を迂回した model 名も永続化境界で拒否する。"""
    config = CmocConfig()
    config.codex.agent_calls["realization_edit"] = CodexCallConfig(
        "openai", model, "high"
    )

    with pytest.raises(TypeError):
        config_to_dict(config)


def test_config_preserves_codex_falv_recovery_try_count(config_data) -> None:
    """codex の recovery 試行回数を読み込みと JSON 化の両方で保持する。"""
    config_data["codex"]["num_try_falv_recovery"] = 4
    config = config_from_dict(config_data)

    assert config.codex.num_try_falv_recovery == 4
    assert config_to_dict(config)["codex"]["num_try_falv_recovery"] == 4


@pytest.mark.parametrize("value", [True, "1", None])
def test_config_rejects_invalid_codex_falv_recovery_try_count(
    config_data, value: object
) -> None:
    """recovery 試行回数へ int 以外を指定した config を拒否する。"""
    config_data["codex"]["num_try_falv_recovery"] = value
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(config_data)

    assert exc_info.value.summary == "cmoc config が不正です。"
