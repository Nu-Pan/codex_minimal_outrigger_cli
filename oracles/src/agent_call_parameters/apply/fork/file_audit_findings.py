"""`cmoc apply fork` のファイル単位監査 prompt 正本。"""

# std
from dataclasses import dataclass
from pathlib import Path

# cmoc
from agent_call_parameters.base import AgentCallParameters, ModelClass, ReasoningEffort
from utils.struct_docs import StructDocs, render_as_markdown
from utils.path_model import resolve_cmoc_root, resolve_repo_root, resolve_work_root
from prompt_parts.general import build_file_access_rule
from prompt_parts.oracles_standards import build_oracles_standards
from prompt_parts.realization_standards import build_realization_standards


def build_apply_fork_file_audit_parameter(
    target_path: Path,
) -> AgentCallParameters:
    """
    `cmoc apply fork` サブコマンド、ファイル単位監査用。
    AI エージェント呼び出しパラメータを構築する。

    taraget_path: Path
        監査の起点となるファイルのパス
        oracle file, realization file が渡される想定。
    """
    # エイリアス
    cmoc_root = resolve_cmoc_root()
    repo_root = resolve_repo_root()
    work_root = resolve_work_root()

    # プロンプトを構築
    # TODO 削除されたファイルもハンドル出来るようにする？
    # TODO 定義・標準をモジュール化・挿入出来るようにする
    prompt: list[StructDocs] = list()
    prompt = [
        StructDocs(
            "summary",
            f"""
            - あなたはソフトウェア実装の監査担当です
            - `{target_path}` を起点に `{repo_root.name}` の要修正点を調査してください
            - 完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです
            """,
        ),
        build_file_access_rule("readonly"),
        build_oracles_standards(),  # TODO 無くても良いような気もする
        build_realization_standards(),
        StructDocs(
            "要修正点の観点",
            StructDocs(
                "基本的な観点",
                f"""
                - 要修正点には、`{repo_root / 'oracles'}` 配下の仕様ファイルと実装との明確な不整合を含めて下さい
                - 要修正点には、実装だけから見た成果物品質上の致命的な問題も含めてください
                """,
            ),
            StructDocs(
                "調査対象",
                f"""
                - `{target_path}` は調査の起点であり、必要なら他の oracle file, realization file も読んでください
                """,
            ),
            # TODO `<work-root>` 配下で作業してる Codex CLI から realization stndards を読めるわけ無いだろう
            StructDocs(
                "規模の問題",
                """
                "realization standards に従い、realization files の肥大化抑制も確認してください。",
                "同じ責務の実装・テスト・fixture・定数・コメントが重複している場合は要修正点として扱ってください。",
                "現行仕様に不要な旧実装、互換分岐、未使用 import、未使用 helper、古いテストは削除対象として扱ってください。",
                "新しい抽象化、CLI 引数、設定項目、状態、外部依存、補助ファイルが現行仕様上必要か確認してください。",
                "テストは外部挙動または制御ロジックを検証し、同じ観点のテストは統合可能か確認してください。",
                """,
            ),
        ),
        # TODO schema で書いてるんだから、プロンプトに書かなくても良くない？　トークン節約した方が良くない？
        StructDocs(
            "出力のフォーマット",
            """
            - 指定された Structured Output schema に一致する JSON を返して下さい
            - 実装のみから発見した要修正点でも、関係する仕様要求を oracle_requirement に記載してください
            - 各要修正点には title、evidences、oracle_requirement、observed_implementation、reason、suggested_fix を含めてください
            """,
        ),
        StructDocs(
            "ファイル読み書き制限",
            f"""
            - 全てのファイルは編集禁止です
            - `{work_root / 'memo'}` は読み書き禁止です
            """,
        ),
    ]
    # Structured output schema
    structured_output_schema_path = (
        cmoc_root
        / "oracles"
        / "schemas"
        / "structured_output"
        / "apply"
        / "fork"
        / "file_audit_findings.json"
    )
    # 正常終了
    return AgentCallParameters(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        render_as_markdown(prompt),
        structured_output_schema_path,
    )
