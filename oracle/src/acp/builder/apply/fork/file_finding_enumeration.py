"""`cmoc apply fork` のファイル単位の所見リストアップ prompt 正本。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import render_as_markdown
from basic.path_model import resolve_repo_root, resolve_real_path
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
    repo_root = resolve_repo_root()
    target_path = resolve_real_path(target_path)
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装の所見リストアップ担当です",
        summary=f"""
        - `{target_path}` を起点に `{repo_root}` ツリー内の realization file の所見を調査すること
        - 必要なら `{target_path}` 以外の oracle file, realization file も読むこと
        """,
        goal="""
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
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).parent / "finding_list.json",
    )
