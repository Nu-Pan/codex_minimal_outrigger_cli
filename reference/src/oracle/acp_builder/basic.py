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
    `{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の
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
    """内部の自動移行と公開 resume に共用する検査済みの対話再開入力。

    呼び出し管理側が、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md`
    の「検査済みの再開入力」に従って、経路ごとの適格性と環境を構築前に照合する。
    この型は検査結果を保持する入力であり、ログや process の検査は行わない。
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
    AI コーディングエージェント (e.g. Codex CLI) の呼び出し要求 1 件を表現するクラス
    """

    # 呼び出し種別の正確な値は各 builder が指定する。
    # 意味と用途は `{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「呼び出し単位と ID」に従う。
    agent_call_kind: str

    # ファイルアクセスモード
    file_access_mode: FileAccessMode

    # TUI 起動用の初回 exec を含む、初回入力となる完全 prompt。
    # 内部の自動移行と公開 resume の対話起動では None とする。
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
    # `{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「文書検索 MCP」を参照。
    enable_document_search_mcp: bool = False

    # feedback reporter の提供判断。完全 prompt を構築する場合も同じ値を渡す。
    # `{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の
    # 「feedback reporter と collector context」を参照。
    enable_feedback_reporting: bool = True

    # 内部の自動移行と公開 resume の対話起動で使う外部 session ID。
    # 非対話 call の補正・回復には使用しない。
    # 意味は `{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の
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
