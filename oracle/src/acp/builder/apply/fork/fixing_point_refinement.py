"""`cmoc apply fork` の要修正点リスト改善 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import render_as_markdown
from basic.path_model import resolve_repo_root
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_fixing_point_refinement_parameter(
    fixing_points: str,
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンド、要修正点リスト改善用。
    AI エージェント呼び出しパラメータを構築する。

    fixing_points: str
        ファイルごとの監査結果を連結した要修正点リスト。
    """
    # パス
    repo_root = resolve_repo_root()
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装監査結果の整理担当です",
        summary=f"""
        - `{repo_root}` ツリー内の realization file に対する要修正点リストを改善すること
        - 現状の要修正点リストは以下である

        ```text
        {fixing_points}
        ```
        """,
        goal="""
        - 要修正点の重複、相互矛盾、明らかな False-Positive を取り除くこと
        - 漏れている明確な要修正点を発見した場合は追加すること
        - 先頭から順に対応する作業順序として自然なリストへ整えること
        - 改善後の要修正点リストを Structured Output schema に一致する JSON だけで返すこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
        oracle_standard=True,
        realization_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.FLAGSHIP,
        ReasoningEffort.HIGH,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
