"""`cmoc session join` の merge conflict marker 解消 prompt 正本。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import (
    AgentCallPathContext,
    resolve_real_path,
    resolve_repo_root,
)

# cmoc
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_session_join_conflict_resolution_parameter(
    conflicted_paths: list[Path],
) -> AgentCallParameter:
    """
    `cmoc session join` サブコマンド、merge conflict marker 解消用。
    AI エージェント呼び出しパラメータを構築する。

    conflicted_paths: list[Path]
        conflict marker 解消対象ファイルのパス。
    """
    # session join は main worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())

    # エイリアス
    resolved_paths = [
        resolve_real_path(path, path_context) for path in conflicted_paths
    ]
    path_list = "\n".join(str(path) for path in resolved_paths)
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたは git merge conflict の解消担当です",
        summary="""
        - `{{work-root}}` ツリー内の merge conflict marker を解消すること
        """,
        goal="""
        - conflict marker の解消以外の余計な差分が存在しないこと
        - 作業前後で仕様の意味が変化していないこと
        - conflict marker が残っていないこと
        """,
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructDoc(
                "conflict 対象ファイル",
                StructCodeBlock(
                    "text",
                    path_list,
                ),
            ),
            StructDoc(
                "additional file access rule",
                """
                - conflict 対象 oracle file は、この conflict marker 解消に必要な範囲だけ編集して良い
                """,
            ),
        ],
        oracle_and_realization_basic=True,
        conflict_resolution_standard=True,
    )
    # パラメータを生成して返す
    # NOTE
    #   conflict 解消時に余計な事をしてほしくないので run_indexing_preflight=False
    # NOTE
    #   ここでやらかすと、ここまでに投下したコストが全てパーになるので、最高品質設定で呼び出す
    return AgentCallParameter(
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
