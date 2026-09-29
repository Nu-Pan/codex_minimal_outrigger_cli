"""session join の競合解消用 prompt と起動パラメータの構築定義。"""

from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    DocumentSearchScope,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import render_sd_node_as_markdown
from oracle.prompt_builder.merge_conflict_resolution import (
    build_merge_conflict_resolution_prompt,
)


def build_session_join_conflict_resolution_parameter(
    session_head_commit: str,
    home_head_commit: str,
    home_worktree: Path,
    *,
    document_search_scope: DocumentSearchScope,
) -> AgentCallParameter:
    """home branch 上で session の変更を統合する call を構築する。

    Args:
        document_search_scope: caller が確定した、その call の実効閲覧範囲。
        session_head_commit: merge 前に確定した session branch の HEAD。
        home_head_commit: merge 前に確定した home branch の HEAD。
        home_worktree: home branch への merge が進行中の worktree。

    NOTE
        `{{cmoc-root}}/oracle/doc/app_spec/sub_command/session_join.md` の
        「競合解消用の agent call」を参照。
        oracle と realization の統合を扱うため REPO_WRITE とし、
        進行中の tree の関連文書を検索するため、caller の scope を渡す。
    """
    # merge target の cwd を明示し、共通の統合方針を組み込む。
    path_context = AgentCallPathContext(agent_call_cwd=home_worktree)
    prompt = build_merge_conflict_resolution_prompt(
        source_commit=session_head_commit,
        target_commit=home_head_commit,
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=path_context,
        document_search_scope=document_search_scope,
    )
    return AgentCallParameter(
        agent_call_kind=build_session_join_conflict_resolution_parameter.__name__,
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        document_search_scope=document_search_scope,
    )
