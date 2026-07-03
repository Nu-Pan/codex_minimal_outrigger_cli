"""`cmoc apply fork` の所見対応作業 prompt 正本。"""

# std
from typing import Any
import json

# cmoc
from oracle.other.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from oracle.other.path_model import resolve_repo_root
from oracle.acp_builder.basic import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_apply_fork_finding_application_parameter(
    findings: list[dict[str, Any]],
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンド、所見対応作業用。
    AI エージェント呼び出しパラメータを構築する。

    finding: str
        対応するべき所見本文のリスト。
        1 件につき、
    """
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装の修正担当です",
        summary="- `<repo-root>` ツリー内の realization file を修正すること",
        goal="""
        - 所見として指摘されている問題の修正作業をベストエフォートで実施したこと
        - realization file が realization standard に従っていること
        - 全てのテストに通過する状態であること
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_dynamic_prompt=[
            StructDoc(
                "作業上の注意点",
                """
                - 所見本文は作業のためのヒントであり、絶対に従うべき指示書ではない
                - git add と git commit は実行禁止
                """,
            ),
            StructDoc(
                "所見本文",
                *[
                    StructDoc(
                        f"FINDING-{i:02d}",
                        StructCodeBlock(
                            "json",
                            json.dumps(f, ensure_ascii=False, indent=2),
                        ),
                    )
                    for i, f in enumerate(findings)
                ],
            ),
        ],
        aux_placeholder_def={
            "repo-root": resolve_repo_root(),
        },
        oracle_and_realization_basic=True,
        realization_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REALIZATION_WRITE,
        render_as_markdown(prompt),
        None,
        True,
    )
