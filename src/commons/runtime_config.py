import json
import math
from pathlib import Path
from typing import Any, TypeVar

from oracle.other.cmoc_config import (
    CodexModelProviderConfig,
    CodexModelSpec,
    JsonTomlValue,
)

from basic.acp import ModelClass, ReasoningEffort
from commons.runtime_errors import CmocError
from commons.runtime_paths import config_path
from config.cmoc_config import (
    CmocConfig,
    CmocConfigCodex,
    CmocConfigOracleReview,
)

ConfigKey = TypeVar("ConfigKey", ModelClass, ReasoningEffort)


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


def _config_int(value: Any) -> int:
    """永続化対象の int field が bool や別型に置き換わっていないか検証する。"""
    if type(value) is not int:
        raise TypeError
    return value


def config_to_dict(config: CmocConfig) -> dict[str, Any]:
    """正本 config 型を、永続化 JSON の object 境界へ変換する。"""
    model_providers: dict[str, dict[str, dict[str, JsonTomlValue]]] = {}
    for provider_id, provider_config in config.codex.model_providers.items():
        if not isinstance(provider_id, str) or not isinstance(
            provider_config, CodexModelProviderConfig
        ):
            raise TypeError("invalid Codex model provider definition")
        validate_json_toml_value(provider_id)
        settings: dict[str, JsonTomlValue] = {}
        for key, setting_value in provider_config.settings.items():
            if not isinstance(key, str):
                raise TypeError("invalid Codex model provider setting key")
            validate_json_toml_value(key)
            settings[key] = validate_json_toml_value(setting_value)
        model_providers[provider_id] = {"settings": settings}
    model: dict[str, dict[str, str | None]] = {}
    for key, model_spec in config.codex.model.items():
        if not isinstance(key, ModelClass) or not isinstance(
            model_spec, CodexModelSpec
        ):
            raise TypeError("invalid Codex model definition")
        model_provider = model_spec.model_provider
        if model_provider is not None:
            if not isinstance(model_provider, str):
                raise TypeError("invalid Codex model provider ID")
            validate_json_toml_value(model_provider)
        model[key.value] = {
            "model_provider": model_provider,
            "model": _model_name(model_spec.model),
        }

    reasoning_effort: dict[str, str] = {}
    for key, value in config.codex.reasoning_effort.items():
        if not isinstance(key, ReasoningEffort):
            raise TypeError("invalid Codex reasoning effort key")
        reasoning_effort[key.value] = _reasoning_effort_name(value)

    return {
        "num_parallel": _config_int(config.num_parallel),
        "codex": {
            "model_providers": model_providers,
            "model": model,
            "reasoning_effort": reasoning_effort,
            # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
            "num_try_falv_recovery": _config_int(config.codex.num_try_falv_recovery),
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

    return _validate(value, set())


def _model_provider_map_from_dict(data: Any) -> dict[str, CodexModelProviderConfig]:
    """provider-local 設定を型検証済みの正本設定型へ戻す。"""
    if not isinstance(data, dict):
        raise TypeError
    restored: dict[str, CodexModelProviderConfig] = {}
    for provider_id, value in data.items():
        if not isinstance(provider_id, str) or not isinstance(value, dict):
            raise TypeError
        validate_json_toml_value(provider_id)
        settings = value.get("settings", {})
        if not isinstance(settings, dict):
            raise TypeError
        restored_settings: dict[str, JsonTomlValue] = {}
        for key, setting in settings.items():
            if not isinstance(key, str):
                raise TypeError
            validate_json_toml_value(key)
            restored_settings[key] = validate_json_toml_value(setting)
        restored[provider_id] = CodexModelProviderConfig(restored_settings)
    return restored


def _enum_str_map_from_dict(
    default: dict[ConfigKey, str],
    data: Any,
    key_type: type[ConfigKey],
) -> dict[ConfigKey, str]:
    """enum key の JSON 表現を、既定値補完済みの runtime map へ戻す。"""
    restored = dict(default)
    if not isinstance(data, dict):
        raise TypeError
    for key, value in data.items():
        # `{{work-root}}/oracle/src/oracle/other/cmoc_config.py` は ReasoningEffort を
        # Codex CLI 名へ変換するため、空名は不正な JSON 編集として扱う。
        restored[key_type(key)] = _reasoning_effort_name(value)
    return restored


def _model_spec_map_from_dict(
    default: dict[ModelClass, CodexModelSpec],
    data: Any,
) -> dict[ModelClass, CodexModelSpec]:
    """JSON 由来の model spec map を正本 enum key と設定型へ戻す。"""
    restored = dict(default)
    if not isinstance(data, dict):
        raise TypeError
    for key, value in data.items():
        if not isinstance(value, dict):
            raise TypeError
        provider = value.get("model_provider")
        model = value.get("model")
        # `{{work-root}}/oracle/src/oracle/other/cmoc_config.py` は未定義の Codex
        # model 名を許可しないため、人手編集による空値はこの境界で失敗させる。
        if provider is not None and not isinstance(provider, str):
            raise TypeError
        model = _model_name(model)
        if isinstance(provider, str):
            validate_json_toml_value(provider)
        restored[ModelClass(key)] = CodexModelSpec(provider, model)
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
        codex_data = _section(data, "codex")
        model_providers = _model_provider_map_from_dict(
            codex_data.get("model_providers", {})
        )
        model = _model_spec_map_from_dict(
            default.codex.model,
            codex_data.get("model", {}),
        )
        reasoning_effort = _enum_str_map_from_dict(
            default.codex.reasoning_effort,
            codex_data.get("reasoning_effort", {}),
            ReasoningEffort,
        )

        oracle_review_data = _section(data, "oracle_review")
        return CmocConfig(
            num_parallel=_int_value(data, "num_parallel", default.num_parallel),
            codex=CmocConfigCodex(
                model_providers=model_providers,
                model=model,
                reasoning_effort=reasoning_effort,
                num_try_falv_recovery=_int_value(
                    codex_data,
                    "num_try_falv_recovery",
                    default.codex.num_try_falv_recovery,
                ),
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
    except (TypeError, ValueError) as exc:
        try:
            detail = json.dumps(data, ensure_ascii=False, indent=2, default=repr)
        except (TypeError, ValueError):
            detail = repr(data)
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
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
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
