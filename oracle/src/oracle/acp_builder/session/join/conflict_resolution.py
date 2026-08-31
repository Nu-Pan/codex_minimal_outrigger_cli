"""session join の conflict 解消用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import (
    AgentCallPathContext,
    resolve_real_path,
    resolve_repo_root,
)

# cmoc
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_session_join_conflict_resolution_parameter(
    conflicted_paths: list[Path],
) -> AgentCallParameter:
    """
    `cmoc session join` サブコマンド、merge conflict marker 解消用。
    AI エージェント呼び出しパラメータを構築する。

    conflicted_paths: list[Path]
        conflict marker 解消対象ファイルのパス。

    NOTE
        marker 解消に必要な専用 policy だけを選び、edit や refactor の広い policy は使わない。
        余計な変更を避けるため preflight を行わない。
    """
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())
    resolved_paths = [
        resolve_real_path(path, path_context) for path in conflicted_paths
    ]
    path_list = "\n".join(str(path) for path in resolved_paths)
    prompt = build_complete_prompt(
        task="""
        - `{{work-root}}` ツリー内の merge conflict marker を解消すること
        """,
        completion_criteria="""
        - conflict marker が残っていないこと
        """,
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "additional file access policy",
                """
                - conflict 対象 oracle file は、この conflict marker 解消に必要な範囲だけ編集して良い
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDHeader(
                "conflict 対象ファイル",
                SDCodeBlock(
                    "text",
                    path_list,
                ),
            ),
        ],
        oracle_and_realization_basic=True,
        # NOTE
        #   解決後の状態も規定を遵守していなければならない
        #   その規定をエージェントに知らせる必要がある
        #   よって oracle_policy, realization_policy は True
        oracle_policy=True,
        realization_policy=True,
        conflict_resolution_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_session_join_conflict_resolution_parameter.__name__,
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
