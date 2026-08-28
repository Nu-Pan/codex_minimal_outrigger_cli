import json
import math
from pathlib import Path
from typing import Any

from oracle.other.cmoc_config import (
    CodexCallConfig,
    CodexModelProviderConfig,
    JsonTomlValue,
)

from config.cmoc_config import (
    CmocConfig,
    CmocConfigCodex,
    CmocConfigOracleReview,
)

from .runtime_errors import CmocError
from .runtime_paths import config_path


def _model_name(value: Any) -> str:
    """Codex の専用 argv へ渡せる非空モデル名へ検証する。"""
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise TypeError
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # model は TOML string ではなく --model の argv へそのまま渡すため、NUL と
    # Unicode surrogate を設定読み込み時に拒否して subprocess 起動失敗を防ぐ。
    validate_json_toml_value(value)
    return value


def _reasoning_effort_name(value: Any) -> str:
    """Codex の TOML override へ渡せる非空 reasoning effort 名へ検証する。"""
    if not isinstance(value, str) or not value.strip():
        raise TypeError
    validate_json_toml_value(value)
    return value


def _model_provider_id(value: Any) -> str:
    """Codex CLI へ直接渡せる必須の model provider ID を検証する。"""
    if not isinstance(value, str) or not value.strip():
        raise TypeError
    validate_json_toml_value(value)
    return value


def _agent_call_kind(value: Any) -> str:
    """設定検索に使う安定した agent call 種別文字列を検証する。"""
    if not isinstance(value, str) or not value.strip():
        raise TypeError
    validate_json_toml_value(value)
    return value


def _config_int(value: Any) -> int:
    """永続化対象の int field が bool や別型に置き換わっていないか検証する。"""
    if type(value) is not int:
        raise TypeError
    return value


def config_to_dict(config: CmocConfig) -> dict[str, Any]:
    """正本 config 型を、永続化 JSON の object 境界へ変換する。"""
    model_providers: dict[str, dict[str, dict[str, JsonTomlValue]]] = {}
    for provider_id, provider_config in config.codex.model_providers.items():
        if not isinstance(provider_config, CodexModelProviderConfig):
            raise TypeError("invalid Codex model provider definition")
        normalized_provider_id = _model_provider_id(provider_id)
        settings: dict[str, JsonTomlValue] = {}
        for key, setting_value in provider_config.settings.items():
            if not isinstance(key, str):
                raise TypeError("invalid Codex model provider setting key")
            validate_json_toml_value(key)
            settings[key] = validate_json_toml_value(setting_value)
        model_providers[normalized_provider_id] = {"settings": settings}
    agent_calls: dict[str, dict[str, str]] = {}
    for agent_call_kind, call_config in config.codex.agent_calls.items():
        if not isinstance(call_config, CodexCallConfig):
            raise TypeError("invalid Codex agent call definition")
        normalized_kind = _agent_call_kind(agent_call_kind)
        agent_calls[normalized_kind] = {
            "model_provider": _model_provider_id(call_config.model_provider),
            "model": _model_name(call_config.model),
            "reasoning_effort": _reasoning_effort_name(call_config.reasoning_effort),
        }

    return {
        "num_parallel": _config_int(config.num_parallel),
        "codex": {
            "model_providers": model_providers,
            "agent_calls": agent_calls,
        },
        "oracle_review": {
            "num_enumerate_findings_loop": _config_int(
                config.oracle_review.num_enumerate_findings_loop
            ),
            "num_merge_findings_loop": _config_int(
                config.oracle_review.num_merge_findings_loop
            ),
            "num_validate_findings_loop": _config_int(
                config.oracle_review.num_validate_findings_loop
            ),
        },
    }


def validate_json_toml_value(value: Any) -> JsonTomlValue:
    """JSON と TOML の双方へ意味を変えず保存できる値を検証する。"""

    def _validate(item: Any, active_containers: set[int]) -> JsonTomlValue:
        """循環 container も拒否しながら再帰的な値を検証する。"""
        if isinstance(item, str):
            # TOML string は Unicode scalar value だけを受理する。
            if any(0xD800 <= ord(character) <= 0xDFFF for character in item):
                raise TypeError
            return item
        if isinstance(item, bool):
            return item
        if type(item) is int:
            # TOML 1.0 の integer は signed 64 bit に限定される。
            if not -(2**63) <= item < 2**63:
                raise TypeError
            return item
        if isinstance(item, float):
            # NaN と infinity は JSON value ではない。
            if not math.isfinite(item):
                raise TypeError
            return item
        if isinstance(item, (list, dict)):
            identity = id(item)
            if identity in active_containers:
                raise TypeError
            active_containers.add(identity)
            try:
                if isinstance(item, list):
                    return [_validate(element, active_containers) for element in item]
                restored: dict[str, JsonTomlValue] = {}
                for key, element in item.items():
                    if not isinstance(key, str):
                        raise TypeError
                    _validate(key, active_containers)
                    restored[key] = _validate(element, active_containers)
                return restored
            finally:
                active_containers.remove(identity)
        raise TypeError

    try:
        return _validate(value, set())
    except RecursionError as exc:
        # {{work-root}}/oracle/doc/app_spec/error_handling.md
        # 深すぎる provider-local container も設定エラーとして上位へ返す。
        raise TypeError("JSON/TOML value is too deeply nested") from exc


def _model_provider_map_from_dict(
    default: dict[str, CodexModelProviderConfig],
    data: Any,
) -> dict[str, CodexModelProviderConfig]:
    """provider-local 設定を型検証済みの正本設定型へ戻す。"""
    if not isinstance(data, dict):
        raise TypeError
    restored = dict(default)
    for provider_id, value in data.items():
        if not isinstance(value, dict):
            raise TypeError
        normalized_provider_id = _model_provider_id(provider_id)
        settings = value.get("settings", {})
        if not isinstance(settings, dict):
            raise TypeError
        restored_settings: dict[str, JsonTomlValue] = {}
        for key, setting in settings.items():
            if not isinstance(key, str):
                raise TypeError
            validate_json_toml_value(key)
            restored_settings[key] = validate_json_toml_value(setting)
        restored[normalized_provider_id] = CodexModelProviderConfig(restored_settings)
    return restored


def _agent_call_map_from_dict(
    default: dict[str, CodexCallConfig],
    data: Any,
) -> dict[str, CodexCallConfig]:
    """agent call ごとの直接設定を既定値補完済みの map へ戻す。"""
    restored = dict(default)
    if not isinstance(data, dict):
        raise TypeError
    for agent_call_kind, value in data.items():
        if not isinstance(value, dict):
            raise TypeError
        normalized_kind = _agent_call_kind(agent_call_kind)
        restored[normalized_kind] = CodexCallConfig(
            model_provider=_model_provider_id(value.get("model_provider")),
            model=_model_name(value.get("model")),
            reasoning_effort=_reasoning_effort_name(value.get("reasoning_effort")),
        )
    return restored


def _section(data: dict[str, Any], key: str) -> dict[str, Any]:
    """省略可能な config section を、型検証済み dict として取り出す。"""
    if key not in data:
        return {}
    value = data[key]
    if not isinstance(value, dict):
        raise TypeError
    return value


def _int_value(data: dict[str, Any], key: str, default: int) -> int:
    """JSON の bool 混入を拒否しつつ int config 値を復元する。"""
    value = data.get(key, default)
    # `{{work-root}}/oracle/src/oracle/other/cmoc_config.py` では int field なので、
    # JSON の bool/string 値は数値ではなく人手編集エラーとして扱う。
    return _config_int(value)


def config_from_dict(data: dict[str, Any]) -> CmocConfig:
    """永続化 JSON object から、不足項目を既定値で補った config を復元する。"""
    default = CmocConfig()
    try:
        if not isinstance(data, dict):
            raise TypeError("config top-level must be an object")
        codex_data = _section(data, "codex")
        model_providers = _model_provider_map_from_dict(
            default.codex.model_providers,
            codex_data.get("model_providers", {}),
        )
        agent_calls = _agent_call_map_from_dict(
            default.codex.agent_calls,
            codex_data.get("agent_calls", {}),
        )

        oracle_review_data = _section(data, "oracle_review")
        return CmocConfig(
            num_parallel=_int_value(data, "num_parallel", default.num_parallel),
            codex=CmocConfigCodex(
                model_providers=model_providers,
                agent_calls=agent_calls,
            ),
            oracle_review=CmocConfigOracleReview(
                num_enumerate_findings_loop=_int_value(
                    oracle_review_data,
                    "num_enumerate_findings_loop",
                    default.oracle_review.num_enumerate_findings_loop,
                ),
                num_merge_findings_loop=_int_value(
                    oracle_review_data,
                    "num_merge_findings_loop",
                    default.oracle_review.num_merge_findings_loop,
                ),
                num_validate_findings_loop=_int_value(
                    oracle_review_data,
                    "num_validate_findings_loop",
                    default.oracle_review.num_validate_findings_loop,
                ),
            ),
        )
    except (RecursionError, TypeError, ValueError) as exc:
        try:
            # {{work-root}}/oracle/doc/app_spec/error_handling.md
            # 不正 JSON には surrogate も含まれうるため、error report を UTF-8 で出力
            # できる ASCII escape へ変換する。
            detail = json.dumps(data, ensure_ascii=True, indent=2, default=repr)
        except (RecursionError, TypeError, ValueError):
            detail = repr(data).encode("utf-8", "backslashreplace").decode("utf-8")
        raise CmocError(
            "cmoc config が不正です。",
            [
                "{{work-root}}/.cmoc/gt/ar/config.json を確認してから再実行してください。"
            ],
            detail,
        ) from exc


def _reject_symlinked_config_path(path: Path) -> None:
    """config path の symlink 経由アクセスを拒否する。"""
    # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    # config は work-root 内の tracked file なので、link 先の設定を読み書きしない。
    current = path.absolute()
    while current != current.parent:
        if current.is_symlink():
            raise CmocError(
                "cmoc config path は symlink 経由で扱えません。",
                [
                    "config.json と親 directory を通常の file/directory に戻してから再実行してください。"
                ],
                str(current),
            )
        current = current.parent


def write_config(path: Path, config: CmocConfig) -> None:
    """config JSON を人間が確認しやすい安定した表現で保存する。"""
    _reject_symlinked_config_path(path)
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    # FIFO などを open して command が停止しないよう、既存 path は regular file に限る。
    if path.exists() and not path.is_file():
        raise CmocError(
            "cmoc config path は通常ファイルではありません。",
            [
                "config.json を通常の file に戻してから再実行してください。",
            ],
            str(path),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            config_to_dict(config),
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def load_config(root: Path) -> CmocConfig:
    """既存 config JSON を読み、利用者向け error 境界で config に復元する。"""
    path = config_path(root)
    _reject_symlinked_config_path(path)
    if not path.exists():
        raise CmocError(
            "cmoc config が存在しません。",
            [
                "cmoc doctor を実行して {{work-root}}/.cmoc/gt/ar/config.json を生成してください。"
            ],
            str(path),
        )
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    # 特殊 file を read_text する前に拒否し、設定読み込みを即時に失敗させる。
    if not path.is_file():
        raise CmocError(
            "cmoc config JSON を読み込めません。",
            [
                "{{work-root}}/.cmoc/gt/ar/config.json を通常の file に修正してください。"
            ],
            str(path),
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise CmocError(
            "cmoc config JSON を読み込めません。",
            ["{{work-root}}/.cmoc/gt/ar/config.json の JSON 構文を確認してください。"],
            str(path),
        ) from exc
    if not isinstance(data, dict):
        raise CmocError(
            "cmoc config の top-level は object である必要があります。",
            ["{{work-root}}/.cmoc/gt/ar/config.json を object に修正してください。"],
            str(path),
        )
    return config_from_dict(data)


def sync_config(root: Path) -> CmocConfig:
    """未作成なら既定 config を生成し、既存 config も現在の形へ書き戻す。"""
    path = config_path(root)
    if path.exists():
        config = load_config(root)
    else:
        config = CmocConfig()
    write_config(path, config)
    return config
