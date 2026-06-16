"""`cmoc apply fork` のファイル単位監査 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_repo_root, resolve_real_path
from agent_call_parameter.base import AgentCallParameters, ModelClass, ReasoningEffort
from agent_call_parameter.prompt_builder.complete_prompt import build_complete_prompt


def build_apply_fork_file_audit_parameter(
    target_path: Path,
) -> AgentCallParameters:
    """
    `cmoc apply fork` サブコマンド、ファイル単位監査用。
    AI エージェント呼び出しパラメータを構築する。

    target_path: Path
        監査の起点となるファイルのパス
        oracle file, realization file が渡される想定。
    """
    # パス
    repo_root = resolve_repo_root()
    target_path = resolve_real_path(target_path)
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェア実装の監査担当です",
        f"""
        - `{target_path}` を起点に `{repo_root.name}` の要修正点を調査すること
        - 必要なら `{target_path}` 以外の oracle file, realization file も読むこと
        - 要修正点とは
            - oracle file と realization file との明確な不整合
            - realization file だけから見た品質上の致命的な問題
        """,
        "- 指定された Structured Output schema に一致する JSON だけを返すこと",
        "readonly",
        oracle_standard=True,
        realization_standard=True,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
