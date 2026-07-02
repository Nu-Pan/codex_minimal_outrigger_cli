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
        return restored
    for key, value in data.items():
        # `<work-root>/oracle/src/oracle/other/cmoc_config.py` stores enum values
        # in JSON, so non-strings must be rejected, not stringified.
        if not isinstance(value, str):
            raise TypeError
        restored[key_type(key)] = value
    return restored


def config_from_dict(data: dict[str, Any]) -> CmocConfig:
    """永続化 JSON object から、不足項目を既定値で補った config を復元する。"""
    default = CmocConfig()
    try:
        codex_data = data.get("codex", {})
        if not isinstance(codex_data, dict):
            codex_data = {}
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

        apply_fork_data = data.get("apply_fork", {})
        if not isinstance(apply_fork_data, dict):
            apply_fork_data = {}
        review_oracle_data = data.get("review_oracle", {})
        if not isinstance(review_oracle_data, dict):
            review_oracle_data = {}

        return CmocConfig(
            num_parallel=int(data.get("num_parallel", default.num_parallel)),
            codex=CmocConfigCodex(
                model=model,
                reasoning_effort=reasoning_effort,
                num_try_falv_recovery=int(
                    codex_data.get(
                        "num_try_falv_recovery",
                        default.codex.num_try_falv_recovery,
                    )
                ),
            ),
            apply_fork=CmocConfigApplyFork(
                num_apply_files=int(
                    apply_fork_data.get(
                        "num_apply_files",
                        default.apply_fork.num_apply_files,
                    )
                ),
            ),
            review_oracle=CmocConfigReviewOracle(
                num_enumerate_findings_loop=int(
                    review_oracle_data.get(
                        "num_enumerate_findings_loop",
                        default.review_oracle.num_enumerate_findings_loop,
                    )
                ),
                num_merge_findings_loop=int(
                    review_oracle_data.get(
                        "num_merge_findings_loop",
                        default.review_oracle.num_merge_findings_loop,
                    )
                ),
                num_validate_findings_loop=int(
                    review_oracle_data.get(
                        "num_validate_findings_loop",
                        default.review_oracle.num_validate_findings_loop,
                    )
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
            ["cmoc init を実行して <repo-root>/.cmoc/config.json を生成してください。"],
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
