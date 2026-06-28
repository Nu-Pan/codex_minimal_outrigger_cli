"""`cmoc apply fork` のファイル単位所見列挙 builder。"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


def build_apply_fork_file_finding_enumeration_parameter(
    target_path: Path,
) -> AgentCallParameter:
    """所見列挙用 agent call parameter を構築する。"""
    # `<work-root>/oracle/src/oracle/acp_builder/apply/fork/file_finding_enumeration.py`
    # is the canonical fragment. Prompt standards are owned by oracle/src, so
    # this builder loads that source of truth only at construction time.
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        _prompt(target_path),
        Path(__file__).with_suffix(".json"),
    )


def _prompt(target_path: Path) -> str:
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.basic import FileAccessMode as OracleFileAccessMode
    from oracle.other.path_model import resolve_real_path
    from oracle.other.struct_doc import render_as_markdown
    from oracle.prompt_builder.complete_prompt import build_complete_prompt

    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装の所見リストアップ担当です",
        summary="""
        - `<target-path>` を起点に `<repo-root>` ツリー内の所見 (realization file の要修正点) を調査すること
        """,
        goal="""
        - `<target-path>` 以外の必要な oracle file, realization file も読んでいること
        - 指定された Structured Output schema に従って所見リストを返すこと
        - 列挙した所見リストが apply review standard を満たしている事
        """,
        file_access_mode=OracleFileAccessMode.READONLY,
        aux_placeholder_def={
            "repo-root": repo_root,
            "target-path": resolve_real_path(target_path),
        },
        oracle_standard=True,
        realization_standard=True,
        apply_review_standard=True,
    )
    return render_as_markdown(prompt)
