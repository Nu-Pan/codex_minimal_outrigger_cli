"""ファイルアクセス規則違反リカバリー用 AgentCallParameter wrapper。"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter, FileAccessMode


def build_file_access_rule_vaolation_recovery_parameter(
    violated_agent_call_log: Path,
    violated_file_list: list[Path],
    violated_file_access_mode: FileAccessMode,
) -> AgentCallParameter:
    """oracle 側正本 builder へ委譲して recovery parameter を構築する。"""
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.common.file_access_rule_vaolation_recovery import (
        build_file_access_rule_vaolation_recovery_parameter as build_oracle_parameter,
    )

    parameter = adapt_oracle_parameter(
        build_oracle_parameter(
            violated_agent_call_log,
            violated_file_list,
            violated_file_access_mode,
        )
    )
    schema_path = parameter.structured_output_schema_path
    if schema_path is not None and not schema_path.exists():
        return AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            parameter.file_access_mode,
            parameter.prompt,
            Path(__file__).with_suffix(".json"),
        )
    return parameter
