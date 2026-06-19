"""`cmoc session join` の merge conflict marker 解消 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_real_path, resolve_work_root
from agent_call_parameter.base import AgentCallParameters, ModelClass, ReasoningEffort
from agent_call_parameter.prompt_parts.complete_prompt import build_complete_prompt


def build_session_join_conflict_resolution_parameter(
    conflicted_paths: list[Path],
) -> AgentCallParameters:
    """
    `cmoc session join` サブコマンド、merge conflict marker 解消用。
    AI エージェント呼び出しパラメータを構築する。

    conflicted_paths: list[Path]
        conflict marker 解消対象ファイルのパス。
    """
    # パス
    work_root = resolve_work_root()
    resolved_paths = [resolve_real_path(path) for path in conflicted_paths]
    path_list = "\n".join(f"- `{path}`" for path in resolved_paths)
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたは git merge conflict の解消担当です",
        f"""
        - `{work_root}` ツリー内の merge conflict marker を解消すること
        - conflict 対象ファイルは以下である

        {path_list}
        """,
        """
        - 作業は conflict marker の解消に限定すること
        - 仕様の意味的な改訂や、conflict 対象外ファイルの編集は禁止
        - oracle file に conflict marker がある場合も、この conflict 解消作業に限って必要最小限の編集を許可する
        - git add と git commit は実行しないこと
        - 作業後に conflict marker が残らない状態にすること
        """,
        "realization_write",
        file_access_aux_rules="""
        - conflict 対象 oracle file は、この conflict marker 解消に必要な範囲だけ編集して良い
        """,
        structured_output=False,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        render_as_markdown(prompt),
        None,
    )
