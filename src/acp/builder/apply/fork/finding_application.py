"""`cmoc apply fork` の所見対応作業 prompt 正本。"""

# std
from typing import Any
import json
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_finding_application_parameter(
    findings: list[dict[str, Any]],
    work_root: Path,
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
        summary=f"- `{work_root}` ツリー内の realization file を修正すること",
        goal="""
        - 所見として指摘されている問題の修正作業をベストエフォートで実施したこと
        - 修正後の realization file が realization standard に従っている事
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_prompt=[
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
    )
