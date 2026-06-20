"""`cmoc apply fork` の要修正点リスト改善 prompt 正本。"""

# std
import json
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.path_model import resolve_repo_root
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_refine_fixing_point_parameter(
    fixing_points: dict,
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンド、要修正点リスト改善用。
    AI エージェント呼び出しパラメータを構築する。

    fixing_points: dict
        ファイルごとの監査結果を連結した要修正点リスト
    """
    # パス
    repo_root = resolve_repo_root()
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装監査結果の整理担当です",
        summary=f"""
        - `{repo_root}` ツリー内の realization file に対する要修正点リストを改善すること
        """,
        goal="""
        - 改善後の要修正点リストを Structured Output schema に一致する JSON だけで返すこと
        - 要修正点の重複、相互矛盾、明らかな False-Positive が取り除かれていること
        - 改善の仮定で発見した新規の要修正点がリストに追加されていること
        - 改善後の要修正点リストを、先頭から順番に作業・消化可能であること
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[
            StructDoc(
                "要修正点リスト",
                StructCodeBlock(
                    "json",
                    json.dumps(fixing_points, ensure_ascii=False, indent=2),
                ),
            )
        ],
        oracle_standard=True,
        realization_standard=True,
        apply_review_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.FLAGSHIP,
        ReasoningEffort.HIGH,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).parent / "finding_list.json",
    )
