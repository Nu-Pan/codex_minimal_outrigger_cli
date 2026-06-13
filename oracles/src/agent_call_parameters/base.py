
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from enum import Enum


class BackendType:
    """
    バックエンドとして使用する AI エージェント CLI ツールの種類。
    """

    OPENAI_CODEX_CLI = "OpenAI Codex CLI"


class ModelClass(Enum):
    """
    AI (LLM) モデルのクラス。
    実際のモデル名への解決はバックエンドの責任。
    """

    # その時々の主力モデルが選ばれる想定
    # 判断材料が足りなくてなんとも言えない時に選ぶ
    # ある種のデフォルト選択肢
    MAINSTREAM = "mainstream"

    # フラッグシップモデルが選ばれる想定
    # 応答品質が何よりも重要な場合に選ぶ
    # 本当によほどの場合のみ使用する選択肢
    # 結果的に FLAGSHIP = MAINSTREAM となることも許容する
    FLAGSHIP = "flagship"

    # その時々の効率重視モデルが選ばれる想定
    # 品質に対してある程度妥協が可能で、かつトークン節約効果が高い時に選ぶ
    EFFICIENCY = "efficiency"

    # その時々の最安価モデルが選ばれる想定
    # 極端に簡単なことをやらせる時に選ぶ
    # 結果的に MINIMUM = EFFICIENCY となることも許容する
    MINIMUM = "medium"


class ReasoningEffort(Enum):
    """
    Reasoning effort の列挙値。
    実際の設定値への解決はバックエンドの責任。
    """
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"



@dataclass(frozen=True)
class AgentCallParameters:
    """
    AI コーディングエージェント (e.g. Codex CLI) の呼び出しパラメータをまとめたクラス。
    """

    # モデルクラス
    model_class: ModelClass

    # Reasoning Effort
    reasoning_effort: ReasoningEffort

    # プロンプト本文
    prompt: str

    # Structured output schema ファイルパス
    structured_output_schema_path: Path

