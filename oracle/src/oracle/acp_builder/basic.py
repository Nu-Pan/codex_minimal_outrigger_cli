"""
acp = Agent Call Parameter
"""

# std
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


class FileAccessMode(StrEnum):
    """cmoc 上の論理的なファイルアクセスモード

    各 mode の意味と sandbox 設定との責務分担は
    `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の
    「ファイルアクセス制限」を正本とする。
    `build_file_access_policy` は一時作業領域の利用規定を含む正確な文面を構築する。
    """

    READONLY = auto()
    PURE_ORACLE_READ = auto()
    REPO_WRITE = auto()
    PURE_ORACLE_WRITE = auto()
    REALIZATION_WRITE = auto()
    NO_POLICY = auto()


@dataclass(frozen=True)
class DocumentSearchScope:
    """caller が確定した文書検索の閲覧範囲。

    NOTE
        `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
        「対象と信頼境界」が path の受理条件と集合の意味を所有する。
        各 tuple は work-root 相対の POSIX path。空の許可集合は全拒否を表す。
    """

    allowed_files: tuple[str, ...] = ()
    allowed_subtrees: tuple[str, ...] = ()
    excluded_files: tuple[str, ...] = ()
    excluded_subtrees: tuple[str, ...] = ()


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

    # cmoc_editor_input MCP server を呼び出し単位で有効化する
    enable_editor_input_handoff_mcp: bool = False

    # None は検索 MCP 無効。明示された scope は空集合でも検索 MCP 有効。
    # `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」を参照。
    document_search_scope: DocumentSearchScope | None = None
