"""quota availability probe の互換入口。"""

from collections.abc import Callable
from importlib import import_module
from typing import cast

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)

__all__ = ["build_quota_availability_probe_parameter"]


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    """正本 builder を使い、未配布時は空 stdin の最小 probe を返す。"""
    try:
        oracle_module = import_module("oracle.acp_builder.quota_probe")
        build_oracle_parameter = cast(
            Callable[[AgentCallParameter], AgentCallParameter],
            getattr(oracle_module, "build_quota_availability_probe_parameter"),
        )
    except ModuleNotFoundError as exc:
        if exc.name != "oracle.acp_builder.quota_probe":
            raise
        # optional oracle builder を含まない distribution のため、この compatibility
        # fallback を保持する。すべての supported distribution が
        # oracle.acp_builder.quota_probe を提供し、この path を import する caller が
        # なくなったら、この entry を削除して全 caller を canonical builder へ移行する。
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # 現在の oracle tree は最小 availability call だけを定義し、専用 builder を持たない。
        # 空 stdin により prompt を realization layer へコピーせず、optional oracle builder
        # を含まない package でも quota polling を実行可能にする。
        return AgentCallParameter(
            agent_call_kind=build_quota_availability_probe_parameter.__name__,
            model_class=ModelClass.MINIMUM,
            reasoning_effort=ReasoningEffort.LOW,
            file_access_mode=FileAccessMode.READONLY,
            prompt="",
            structured_output_schema_path=None,
            agent_call_cwd=base_parameter.agent_call_cwd,
            run_indexing_preflight=False,
        )
    return build_oracle_parameter(base_parameter)
