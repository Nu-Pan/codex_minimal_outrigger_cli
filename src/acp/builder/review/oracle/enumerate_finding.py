"""`cmoc review oracle` の新規所見列挙 prompt 構築実装。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.path_model import resolve_real_path
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_review_oracle_enumerate_finding_parameter(
    oracle_path: Path,
    related_findings: str,
) -> AgentCallParameter:
    """
    `cmoc review oracle` サブコマンド、新規所見列挙用。
    AI エージェント呼び出しパラメータを構築する。

    oracle_path: Path
        レビュー対象 oracle file のパス

    related_findings: str
        現状の所見リストのうち、レビュー対象ファイルと関連するもの
    """
    # パス
    oracle_path = resolve_real_path(oracle_path)
    oracle_root = resolve_real_path(Path("<work-root>/oracle"))
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片のレビュー担当です",
        summary=f"""
        - `{oracle_path}` を起点に `{oracle_root}` ツリー内の oracle file をレビューすること
        - 必要なら `{oracle_path}` 以外の関連する oracle file も読むこと
        """,
        goal="""
        - 指定の Structured Output schema に従って所見が列挙されていること
        - 既知の関連所見と重複しない新規所見だけが列挙されていること
        - 新規所見が無い場合は空配列を返していること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        aux_prompt=[
            StructDoc(
                "既知の関連所見",
                StructCodeBlock(
                    "text",
                    related_findings,
                ),
            )
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
        review_oracle_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.PURE_ORACLE_READ,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
