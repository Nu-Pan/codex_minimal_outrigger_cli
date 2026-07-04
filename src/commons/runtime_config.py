import json
from pathlib import Path
from typing import Any, TypeVar

from basic.acp import ModelClass, ReasoningEffort
from config.cmoc_config import (
    CmocConfig,
    CmocConfigApplyFork,
    CmocConfigCodex,
    CmocConfigReviewOracle,
)

from commons.runtime_errors import CmocError
from commons.runtime_paths import config_path

ConfigKey = TypeVar("ConfigKey", ModelClass, ReasoningEffort)


def config_to_dict(config: CmocConfig) -> dict[str, Any]:
    """正本 config 型を、永続化 JSON の object 境界へ変換する。"""
    return {
        "num_parallel": config.num_parallel,
        "codex": {
            "model": {
                key.value: value
                for key, value in sorted(
                    config.codex.model.items(), key=lambda item: item[0].value
                )
            },
            "reasoning_effort": {
                key.value: value
                for key, value in sorted(
                    config.codex.reasoning_effort.items(),
                    key=lambda item: item[0].value,
                )
            },
            "num_try_falv_recovery": config.codex.num_try_falv_recovery,
        },
        "apply_fork": {
            "num_apply_files": config.apply_fork.num_apply_files,
        },
        "review_oracle": {
            "num_enumerate_findings_loop": config.review_oracle.num_enumerate_findings_loop,
            "num_merge_findings_loop": config.review_oracle.num_merge_findings_loop,
            "num_validate_findings_loop": config.review_oracle.num_validate_findings_loop,
        },
    }


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
        # `<work-root>/oracle/src/oracle/other/cmoc_config.py` stores enum values
        # in JSON, so non-strings must be rejected, not stringified.
        if not isinstance(value, str):
            raise TypeError
        restored[key_type(key)] = value
    return restored


def _section(data: dict[str, Any], key: str) -> dict[str, Any]:
    if key not in data:
        return {}
    value = data[key]
    if not isinstance(value, dict):
        raise TypeError
    return value


def _int_value(data: dict[str, Any], key: str, default: int) -> int:
    value = data.get(key, default)
    # `<work-root>/oracle/src/oracle/other/cmoc_config.py` defines these as
    # int fields; JSON bool/string values are human edit errors, not numbers.
    if type(value) is not int:
        raise TypeError
    return value


def config_from_dict(data: dict[str, Any]) -> CmocConfig:
    """永続化 JSON object から、不足項目を既定値で補った config を復元する。"""
    default = CmocConfig()
    try:
        codex_data = _section(data, "codex")
        model = _enum_str_map_from_dict(
            default.codex.model,
            codex_data.get("model", {}),
            ModelClass,
        )
        reasoning_effort = _enum_str_map_from_dict(
            default.codex.reasoning_effort,
            codex_data.get("reasoning_effort", {}),
            ReasoningEffort,
        )

        apply_fork_data = _section(data, "apply_fork")
        review_oracle_data = _section(data, "review_oracle")

        return CmocConfig(
            num_parallel=_int_value(data, "num_parallel", default.num_parallel),
            codex=CmocConfigCodex(
                model=model,
                reasoning_effort=reasoning_effort,
                num_try_falv_recovery=_int_value(
                    codex_data,
                    "num_try_falv_recovery",
                    default.codex.num_try_falv_recovery,
                ),
            ),
            apply_fork=CmocConfigApplyFork(
                num_apply_files=_int_value(
                    apply_fork_data,
                    "num_apply_files",
                    default.apply_fork.num_apply_files,
                ),
            ),
            review_oracle=CmocConfigReviewOracle(
                num_enumerate_findings_loop=_int_value(
                    review_oracle_data,
                    "num_enumerate_findings_loop",
                    default.review_oracle.num_enumerate_findings_loop,
                ),
                num_merge_findings_loop=_int_value(
                    review_oracle_data,
                    "num_merge_findings_loop",
                    default.review_oracle.num_merge_findings_loop,
                ),
                num_validate_findings_loop=_int_value(
                    review_oracle_data,
                    "num_validate_findings_loop",
                    default.review_oracle.num_validate_findings_loop,
                ),
            ),
        )
    except (TypeError, ValueError) as exc:
        raise CmocError(
            "cmoc config が不正です。",
            ["<repo-root>/.cmoc/config.json を確認してから再実行してください。"],
            json.dumps(data, ensure_ascii=False, indent=2),
        ) from exc


def write_config(path: Path, config: CmocConfig) -> None:
    """config JSON を人間が確認しやすい安定した表現で保存する。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(config_to_dict(config), ensure_ascii=False, indent=2) + "\n"
    )


def load_config(root: Path) -> CmocConfig:
    """既存 config JSON を読み、利用者向け error 境界で config に復元する。"""
    path = config_path(root)
    if not path.exists():
        raise CmocError(
            "cmoc config が存在しません。",
            ["cmoc doctor を実行して <repo-root>/.cmoc/config.json を生成してください。"],
            str(path),
        )
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise CmocError(
            "cmoc config JSON を読み込めません。",
            ["<repo-root>/.cmoc/config.json の JSON 構文を確認してください。"],
            str(path),
        ) from exc
    if not isinstance(data, dict):
        raise CmocError(
            "cmoc config の top-level は object である必要があります。",
            ["<repo-root>/.cmoc/config.json を object に修正してください。"],
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
