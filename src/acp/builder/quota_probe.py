"""Codex quota availability probe parameter builder."""

from importlib import import_module

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    try:
        module = import_module("oracle.acp_builder.quota_probe")
    except ModuleNotFoundError as error:
        if error.name != "oracle.acp_builder.quota_probe":
            raise
        # <work-root>/oracle/doc/app_spec/prompt_standard.md
        # Missing oracle builder is a spec gap, not a place for realization-side
        # prompt fallback.
        raise RuntimeError(
            "oracle.acp_builder.quota_probe."
            "build_quota_availability_probe_parameter is required"
        ) from error
    return module.build_quota_availability_probe_parameter(base_parameter)


__all__ = ["build_quota_availability_probe_parameter"]
