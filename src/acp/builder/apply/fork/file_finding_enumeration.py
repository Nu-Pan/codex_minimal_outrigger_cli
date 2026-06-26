"""`cmoc apply fork` のファイル単位の所見リストアップ prompt 構築実装。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import render_as_markdown
from basic.path_model import resolve_real_path, resolve_work_root
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_file_finding_enumeration_parameter(
    target_path: Path,
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンド、ファイル単位の所見リストアップ用。
    AI エージェント呼び出しパラメータを構築する。

    target_path: Path
        所見リストアップの起点となるファイルのパス
        oracle file, realization file が渡される想定
    """
    # パス
    work_root = resolve_work_root()
    target_path = resolve_real_path(target_path)
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装の所見リストアップ担当です",
        summary=f"""
        - `{target_path}` を起点に `{work_root}` ツリー内の所見 (realization file の要修正点) を調査すること
        """,
        goal=f"""
        - `{target_path}` 以外の必要な oracle file, realization file も読んでいること
        - 指定された Structured Output schema に従って所見リストを返すこと
        - 列挙した所見リストが apply review standard を満たしている事
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
        oracle_standard=True,
        realization_standard=True,
        apply_review_standard=True,
    )
    # パラメータを生成して返す
    # NOTE
    #   ファイル数だけ呼び出されるということは、トークン消費 N 倍なので重い。
    #   しかし、ここの失敗が下流全てに影響することを鑑みて MAINSTREAM にしている。
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
