"""
acp = Agent Call Parameter
"""

# std
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


class FileAccessMode(StrEnum):
    """cmoc 上の論理的なファイルアクセスモード

    各 mode の意味と Codex CLI sandbox への対応は
    `oracle/doc/app_spec/codex_exec_rule.md` を正本とする。
    `build_file_access_policy` は agent に渡す正確な制限文面を構築する。
    """

    READONLY = auto()
    PURE_ORACLE_READ = auto()
    REPO_WRITE = auto()
    PURE_ORACLE_WRITE = auto()
    REALIZATION_WRITE = auto()
    NO_POLICY = auto()


@dataclass(frozen=True)
class AgentCallParameter:
    """
    AI コーディングエージェント (e.g. Codex CLI) の呼び出しパラメータをまとめたクラス
    """

    # エージェント呼び出しの種類を表す安定した低カーディナリティ識別子
    # 典型的には対応する builder 関数名を使う
    # Codex call 設定の検索と cmoc feedback 用の問題分類に使う
    agent_call_kind: str

    # ファイルアクセスモード
    file_access_mode: FileAccessMode

    # Codex CLI の初回入力となる完全な prompt 本文
    prompt: str

    # Structured Output schema ファイルパス
    # Structured Output を要求しない呼び出しでは None。
    # schema の機械的受理条件を prompt comment や realization 側へ複製しない。
    structured_output_schema_path: Path | None

    # agent call に設定する cwd
    agent_call_cwd: Path

    # True なら論理 agent call の初回 Codex call 前に indexing preflight を実行する
    # False なら indexing preflight を実行しない
    # 通常は True のままで良い
    # 本命 agent call 自身が indexing である場合は indexing preflight をスキップする、というのが主な使い方
    run_indexing_preflight: bool = True
