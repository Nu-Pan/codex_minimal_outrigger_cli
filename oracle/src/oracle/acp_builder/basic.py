"""
acp = Agent Call Parameter
"""

# std
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


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

    各 mode の意味と Codex CLI sandbox への対応は
    `oracle/doc/app_spec/codex_exec_rule.md` を正本とする。
    `build_file_access_rule` は agent に渡す正確な制限文面を構築する。
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

    # 対応する builder 関数名を使う、安定した低カーディナリティ識別子
    agent_call_kind: str

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

    # agent call に設定する cwd
    # builder は prompt 構築前に agent_call_cwd を決定し、同じ値から call-scoped path context を構築する
    agent_call_cwd: Path

    # True なら論理 agent call の初回 Codex call 前に indexing preflight を実行する
    # False なら indexing preflight を実行しない
    # Structured Output の補正用 Codex call では、この値によらず再実行しない
    # 本命 agent call 自身が indexing である場合は indexing preflight をスキップする、というのが主な使い方
    # 通常は True のままで良い
    # file access rule violation recovery のような indexing preflight から連鎖的に発生する処理の場合もスキップの対象。
    run_indexing_preflight: bool = True
