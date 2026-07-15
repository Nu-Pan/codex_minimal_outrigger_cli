"""quota availability probe の互換入口。"""

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
        from oracle.acp_builder.quota_probe import (
            build_quota_availability_probe_parameter as build_oracle_parameter,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "oracle.acp_builder.quota_probe":
            raise
        # Keep this compatibility fallback for distributions that omit the
        # optional oracle builder. Remove this entry and migrate all callers
        # to the canonical builder once every supported distribution ships
        # oracle.acp_builder.quota_probe and no caller imports this path.
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # The current oracle tree specifies only a minimal availability call and
        # has no dedicated builder. Empty stdin avoids copying a prompt into the
        # realization layer while keeping quota polling executable in packages
        # that do not ship an optional oracle builder.
        return AgentCallParameter(
            ModelClass.MINIMUM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "",
            None,
            run_indexing_preflight=False,
            cwd=base_parameter.cwd,
        )
    return build_oracle_parameter(base_parameter)
