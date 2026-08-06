"""`cmoc feedback report` の曖昧な issue 正規化 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import (
    AgentCallPathContext,
    RootPathPlaceHolder,
    resolve_ph_path,
)
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_feedback_normalize_issue_parameter(
    observation_json: str,
    candidate_issues_json: str,
    current_reference_paths: list[Path],
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """構造化 observation と絞り込み済み候補だけから issue を正規化する。"""
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    reference_paths = [
        str(resolve_ph_path(path, RootPathPlaceHolder.WORK, path_context))
        for path in current_reference_paths
    ]
    references_text = (
        "\n".join(f"- `{path}`" for path in reference_paths)
        if reference_paths
        else "- なし"
    )
    reference_scope = "\n".join(
        (
            "- 現在状態の確認が必要な場合に限り、次の参照対象を読んでよい",
            references_text,
            "- 指定されていない raw log、過去の Codex session、"
            "feedback observation 保存 file を追加調査してはいけない",
        )
    )

    prompt = build_complete_prompt(
        role="- あなたは人間向け feedback issue の正規化担当です",
        summary="""
        - 構造化済み observation を、絞り込み済みの既存 issue 候補と比較し、既存 issue への統合または新規 issue の作成を判断すること
        - raw Codex call log は読み直さず、入力された observation、既存 issue 候補、および指定された現在の参照対象だけを根拠にすること
        """,
        goal="""
        - 指定された Structured Output schema に従って正規化結果を返すこと
        - agent が申告した原因、重要度、および重複判定用 hint を確定事実として扱っていないこと
        - 現在の存在可能性を、入力と指定された現在参照だけから machine assessment として評価すること
        - human disposition を決定または変更していないこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[
            StructDoc(
                "Structured Output の決定論的事後条件",
                """
                - `existing_issue_id` と `related_issue_ids` に含めてよいのは、入力された既存 issue 候補の issue ID だけとする
                - `decision=existing` の場合、`existing_issue_id` を `related_issue_ids` に重複させてはいけない
                """,
            ),
            StructDoc(
                "参照範囲",
                reference_scope,
            ),
        ],
        aux_dynamic_prompt=[
            StructDoc(
                "構造化済み observation",
                StructCodeBlock("json", observation_json),
            ),
            StructDoc(
                "既存 issue 候補",
                StructCodeBlock("json", candidate_issues_json),
            ),
        ],
    )

    return AgentCallParameter(
        agent_call_kind=build_feedback_normalize_issue_parameter.__name__,
        model_class=ModelClass.MAINSTREAM,
        reasoning_effort=ReasoningEffort.HIGH,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
