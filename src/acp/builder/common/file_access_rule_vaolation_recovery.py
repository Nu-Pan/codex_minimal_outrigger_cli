"""ファイルアクセス規則違反リカバリー用 AgentCallParameter wrapper。"""

from dataclasses import replace
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
    """
    oracle 側正本 builder へ委譲して recovery parameter を構築する。

    対応 oracle file: `<work-root>/oracle/src/oracle/acp_builder/common/file_access_rule_vaolation_recovery.py`
    """
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
    if (
        violated_agent_call_log.suffix != ".json"
        or not violated_agent_call_log.stem.endswith("_call")
    ):
        raise ValueError("violated agent call log must be `*_call.json`")
    time_stamp = violated_agent_call_log.stem.removesuffix("_call")
    # `<work-root>/oracle/src/oracle/acp_builder/common/file_access_rule_vaolation_recovery.py`
    # currently emits the call-log stem, but its prompt refers to
    # `<time-stamp>_call.json`; keep the placeholder on the timestamp part.
    return replace(
        parameter,
        prompt=parameter.prompt.replace(
            f"- <time-stamp> = {violated_agent_call_log.stem}",
            f"- <time-stamp> = {time_stamp}",
            1,
        ),
    )
