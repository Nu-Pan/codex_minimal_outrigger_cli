"""oracle review の新規所見列挙用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import (
    AgentCallPathContext,
    resolve_real_path,
)

# cmoc
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_review_enumerate_finding_parameter(
    oracle_path: Path,
    related_findings: str,
    *,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """
    `cmoc oracle review` サブコマンド、新規所見列挙用。
    AI エージェント呼び出しパラメータを構築する。

    oracle_path: Path
        レビュー対象 oracle file のパス

    related_findings: str
        現状の所見リストのうち、レビュー対象ファイルと関連するもの

    agent_call_cwd: Path
        oracle review agent call を実行する worktree
    """
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        task="""
        - oracle file をレビューし、既知の関連所見と重複しない新規所見を列挙すること
        """,
        scope="""
        - `{{oracle-path}}` を起点に `{{oracle-root}}` ツリーを調査し、必要な場合は他の関連する oracle file も根拠とすること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
        aux_dynamic_prompt=[
            SDHeader(
                "既知の関連所見",
                SDCodeBlock(
                    "text",
                    related_findings,
                ),
            )
        ],
        aux_placeholder_def={
            "oracle-path": resolve_real_path(oracle_path, path_context),
            "oracle-root": resolve_real_path(
                Path("{{work-root}}/oracle"), path_context
            ),
        },
        oracle_and_realization_basic=True,
        oracle_policy=True,
        oracle_findings_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_oracle_review_enumerate_finding_parameter.__name__,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
