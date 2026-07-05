"""Codex quota availability probe parameter compatibility builder."""

from importlib import import_module

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort


_FALLBACK_PROBE_PROMPT = (
    "quota 利用可否を確認するための最小実行です。"
    "利用可能なら ok だけを返してください。"
)


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    try:
        builder = import_module("oracle.acp_builder.quota_probe")
    except ModuleNotFoundError as exc:
        if exc.name != "oracle.acp_builder.quota_probe":
            raise
    else:
        return builder.build_quota_availability_probe_parameter(base_parameter)

    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # oracle 側 builder 欠落中だけの fallback。正本 builder 追加後に削除する。
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        _FALLBACK_PROBE_PROMPT,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )


__all__ = ["build_quota_availability_probe_parameter"]
