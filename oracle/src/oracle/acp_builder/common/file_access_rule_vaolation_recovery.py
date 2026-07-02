# std
from pathlib import Path

# cmoc
from oracle.other.struct_doc import StructDoc, render_as_markdown
from oracle.other.path_model import resolve_repo_root
from oracle.acp_builder.basic import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.parts.file_access_rule import build_file_access_rule


def build_file_access_rule_vaolation_recovery_parameter(
    violated_agent_call_log: Path,
    violated_file_list: list[Path],
    violated_file_access_mode: FileAccessMode,
) -> AgentCallParameter:
    """
    agent call でファイルアクセス規則違反が発生した時のリカバリ。
    AI エージェント呼び出しパラメータを構築する。

    violated_call_log: Path
        ファイルアクセス規則に違反した agetn call のログファイル
        `<repo-root>/.cmoc/log/codex/<time-stamp>_call.json` が渡される想定

    violated_file_list: list[Path]
        ファイルアクセス規則に違反したファイルのリスト

    violated_file_access_mode: FileAccessMode
        違反が発生した時のファイルアクセスモード
    """
    # 違反したファイルアクセス規則
    vfal_phm, vfal_doc = build_file_access_rule(violated_file_access_mode)
    if not isinstance(vfal_doc.children, str):
        raise TypeError("`build_file_access_rule` returns Unexpected StructDoc")
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはファイルアクセス規則違反のリカバリー担当です",
        summary="""
        - <violated-file-list> が <violated-file-access-rule> に違反しています
        - この違反は `<repo-root>/.cmoc/log/codex/<time-stamp>_call.json` で発生しました
        - このファイルアクセス規則違反をリカバリーして下さい
        """,
        goal="""
        - `<repo-root>` ツリー内の差分が、<violated-file-access-rule> に違反していないこと
        - `<repo-root>/.cmoc/log/codex/<time-stamp>_call.json` の作業目的を意味論的に損ねていないこと
        - `<violated-file-list>` の違反が解消されていること
        """,
        file_access_mode=FileAccessMode.NO_RULE,
        aux_dynamic_prompt=[
            StructDoc(
                "<violated-file-access-rule>",
                vfal_doc.children,
            ),
            StructDoc(
                "<violated-file-list>",
                "\n".join(f"- `{vfl}`" for vfl in violated_file_list),
            ),
        ],
        aux_placeholder_def={
            "repo-root": resolve_repo_root(),
            "time-stamp": violated_agent_call_log.stem,
            **vfal_phm,
        },
        oracle_and_realization_basic=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.FLAGSHIP,
        ReasoningEffort.MEDIUM,
        FileAccessMode.NO_RULE,
        render_as_markdown(prompt),
        None,
    )
