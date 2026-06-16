"""`cmoc review oracle` の新規所見列挙 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_real_path
from agent_call_parameter.base import AgentCallParameters, ModelClass, ReasoningEffort
from prompt_parts.complete_prompt import build_complete_prompt


def build_review_oracle_enumerate_finding_parameter(
    oracle_path: Path,
    related_findings: str,
) -> AgentCallParameters:
    """
    `cmoc review oracle` サブコマンド、新規所見列挙用。
    AI エージェント呼び出しパラメータを構築する。

    oracle_path: Path
        レビュー対象 oracle file のパス。
    related_findings: str
        現状の所見リストのうち、レビュー対象ファイルと関連するもの。
    """
    # パス
    oracle_path = resolve_real_path(oracle_path)
    oracle_root = resolve_real_path(Path("<work-root>/oracle"))
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェア仕様断片のレビュー担当です",
        f"""
        - `{oracle_path}` を起点に `{oracle_root}` ツリー内の oracle file をレビューすること
        - 必要なら `{oracle_path}` 以外の関連する oracle file も読むこと
        - 既知の関連所見は以下である

        ```text
        {related_findings}
        ```
        """,
        """
        - 既知の関連所見と重複しない新規所見だけを列挙すること
        - 新規所見が無い場合は空配列を返すこと
        """,
        "pure_oracle_read",
        oracle_standard=True,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
