"""Codex quota availability probe 用の最小 AgentCallParameter を作る。

Oracle: <work-root>/oracle/doc/app_spec/codex_exec_rule.md
"""

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # codex_exec_rule.md は「動作確認用のミニマルな Codex CLI 呼び出し」
    # だけを要求する。probe は runtime 側で同じ CODEX_HOME/profile/cwd を
    # 使って起動されるため、ここでは意味のある作業を依頼しない。
    return AgentCallParameter(
        base_parameter.model_class,
        base_parameter.reasoning_effort,
        base_parameter.file_access_mode,
        "Respond with exactly: ok",
        None,
    )


__all__ = ["build_quota_availability_probe_parameter"]
