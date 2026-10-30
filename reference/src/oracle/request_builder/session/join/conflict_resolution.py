"""session join の競合解消用 prompt と起動パラメータの構築定義。"""

from pathlib import Path

from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import render_sd_node_as_markdown
from oracle.prompt_builder.merge_conflict_resolution import (
    build_merge_conflict_resolution_prompt,
)
from oracle.request_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)


def build_session_join_conflict_resolution_request(
    session_head_commit: str,
    home_head_commit: str,
    home_worktree: Path,
) -> AgentCallParameter:
    """home branch 上で session の変更を統合する call を構築する。

    Args:
        session_head_commit: merge 前に確定した session branch の HEAD。
        home_head_commit: merge 前に確定した home branch の HEAD。
        home_worktree: home branch への merge が進行中の worktree。

    NOTE
        `{{cmoc-root}}/spec/app_spec/sub_command/session_join.md` の
        「競合解消用の agent call」を参照。
        decision・reference は変更せず、spec・realization の統合に
        SPEC_AND_REALIZATION_WRITE を使う。
    """
    # merge target の cwd を明示し、共通の統合方針を組み込む。
    path_context = AgentCallPathContext(agent_call_cwd=home_worktree)
    prompt = build_merge_conflict_resolution_prompt(
        source_commit=session_head_commit,
        target_commit=home_head_commit,
        file_access_mode=FileAccessMode.SPEC_AND_REALIZATION_WRITE,
        path_context=path_context,
    )
    return AgentCallParameter(
        agent_call_kind=build_session_join_conflict_resolution_request.__name__,
        file_access_mode=FileAccessMode.SPEC_AND_REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
    )
