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
class TuiResumeTarget:
    """対象検査済みの対話再開入力。

    適格性と環境照合は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/resume.md`
    の「対象の適格性と会話選択」「workload と起動環境の保持」に従い、
    呼び出し管理側が構築前に確認する。
    """

    codex_session_id: str
    agent_call_cwd: Path

    def __post_init__(self) -> None:
        """外部識別子を加工せず、未指定の再開先と相対 cwd を拒否する。"""
        if not self.codex_session_id.strip():
            raise ValueError("codex_session_id must not be blank")
        if not self.agent_call_cwd.is_absolute():
            raise ValueError("agent_call_cwd must be absolute")


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

    # 初回入力となる完全 prompt。対話 resume だけは None とする。
    prompt: str | None

    # Structured Output schema ファイルパス
    # Structured Output を要求しない呼び出しでは None。
    # schema の機械的受理条件を prompt comment や realization 側へ複製しない。
    structured_output_schema_path: Path | None

    # agent call に設定する cwd
    agent_call_cwd: Path

    # cmoc_editor_input MCP server を呼び出し単位で有効化する
    enable_editor_input_handoff_mcp: bool = False

    # cmoc_document_search MCP server を呼び出し単位で有効化する。
    # `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」を参照。
    enable_document_search_mcp: bool = False

    # feedback reporter の提供判断。完全 prompt を構築する場合も同じ値を渡す。
    # `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の
    # 「feedback reporter と collector context」を参照。
    enable_feedback_reporting: bool = True

    # 対話 resume の外部 session ID。非対話 call の補正・回復には使用しない。
    # 意味は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の
    # 「TUI の新規起動と対話 resume」を正本とする。
    tui_resume_session_id: str | None = None

    def __post_init__(self) -> None:
        """初期 prompt と対話 resume の指定を排他的にする。"""
        if self.tui_resume_session_id is None:
            if self.prompt is None:
                raise ValueError("prompt is required unless resuming a TUI")
        else:
            if not self.tui_resume_session_id.strip():
                raise ValueError("tui_resume_session_id must not be blank")
            if self.prompt is not None:
                raise ValueError("TUI resume must not include an initial prompt")
            if self.structured_output_schema_path is not None:
                raise ValueError("TUI resume must not request Structured Output")
