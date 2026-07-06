"""quota availability probe 用の AgentCallParameter を構築する。"""

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort


_PROMPT = "quota 回復確認です。実行可能なら OK とだけ返してください。"


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # quota wait must keep polling with a minimal Codex exec call. This builder
    # stays deliberately small because no separate oracle src fragment exists
    # for the probe-specific parameter.
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        _PROMPT,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )


__all__ = ["build_quota_availability_probe_parameter"]
