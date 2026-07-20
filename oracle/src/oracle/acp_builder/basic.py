"""
acp = Agent Call Parameter
"""

# std
from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path

# cmoc
from oracle.other.path_model import resolve_work_root


class ModelClass(StrEnum):
    """
    cmoc 上の論理的なモデルクラス
    バックエンドが受理可能なモデル名への解決は realization src の責任
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
    cmoc 上の論理的な Reasoning effort
    バックエンドに対応する Reasoning Effort 名が存在しない場合、realization src の責任で近い名前に丸めても良い
    """

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    XHIGH = auto()
    MAX = auto()


class FileAccessMode(StrEnum):
    """cmoc 上の論理的なファイルアクセスモード

    各モードの詳細は `build_file_access_rule` を参照
    Codex CLI sandbox への対応と permission profile の禁止規則は
    `oracle/doc/app_spec/codex_exec_rule.md` を正本とする
    """

    READONLY = auto()
    PURE_ORACLE_READ = auto()
    REPO_WRITE = auto()
    PURE_ORACLE_WRITE = auto()
    REALIZATION_WRITE = auto()
    NO_RULE = auto()


@dataclass(frozen=True)
class AgentCallParameter:
    """
    AI コーディングエージェント (e.g. Codex CLI) の呼び出しパラメータをまとめたクラス
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

    # True なら本命 agent call の前に indexing preflight を実行する
    # False なら indexing preflight を実行しない
    # 本命 agent call 自身が indexing である場合は indexling preflight をスキップする、というのが主な使い方
    # 通常は True のままで良い
    # file access rule violation recovery のような indexing preflight から連鎖的に発生する処理の場合もスキップの対象。
    run_indexing_preflight: bool = field(default=True)

    # agent call 時のカレントパス
    # 通常は `{{work-root}}` のままで良い
    cwd: Path = field(default_factory=lambda: resolve_work_root())
