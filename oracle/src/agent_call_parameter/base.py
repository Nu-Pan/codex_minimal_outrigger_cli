# std
from dataclasses import dataclass
from pathlib import Path
from enum import StrEnum, auto


class BackendType:
    """
    バックエンドとして使用する AI エージェント CLI ツールの種類。
    """

    OPENAI_CODEX_CLI = auto()


class ModelClass(StrEnum):
    """
    AI (LLM) モデルのクラス。
    バックエンドが受理可能なモデル名への解決はバックエンドの責任。
    """

    # その時々の主力モデルが選ばれる想定
    # 判断材料が足りなくてなんとも言えない時に選ぶ
    # ある種のデフォルト選択肢
    MAINSTREAM = auto()

    # フラッグシップモデルが選ばれる想定
    # 応答品質が何よりも重要な場合に選ぶ
    # 本当によほどの場合のみ使用する選択肢
    # 結果的に FLAGSHIP = MAINSTREAM となることも許容する
    FLAGSHIP = auto()

    # その時々の効率重視モデルが選ばれる想定
    # 品質に対してある程度妥協が可能で、かつトークン節約効果が高い時に選ぶ
    EFFICIENCY = auto()

    # その時々の最安価モデルが選ばれる想定
    # 極端に簡単なことをやらせる時に選ぶ
    # 結果的に MINIMUM = EFFICIENCY となることも許容する
    MINIMUM = auto()


class ReasoningEffort(StrEnum):
    """
    Reasoning effort の列挙値。
    バックエンドが受理可能な設定値への解決はバックエンドの責任。
    """

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class FileAccessMode(StrEnum):
    """
    ファイルアクセスモードの列挙値。
    バックエンドが受理可能なモードへの解決はバックエンドの責任。
    """

    READONLY = auto()
    PURE_ORACLE_READ = auto()
    REALIZATION_WRITE = auto()
    ORACLE_WRITE = auto()


@dataclass(frozen=True)
class AgentCallParameters:
    """
    AI コーディングエージェント (e.g. Codex CLI) の呼び出しパラメータをまとめたクラス。
    """

    # モデルクラス
    model_class: ModelClass

    # Reasoning Effort
    reasoning_effort: ReasoningEffort

    # ファイルアクセスモード
    file_access_mode: FileAccessMode

    # プロンプト本文
    prompt: str

    # Structured Output schema ファイルパス
    # Structured Output を要求しない呼び出しでは None。
    structured_output_schema_path: Path | None
