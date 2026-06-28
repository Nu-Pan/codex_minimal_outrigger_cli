"""`cmoc apply fork` の所見適用 builder。"""

import json
from typing import Any

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


def build_apply_fork_finding_application_parameter(
    findings: list[dict[str, Any]],
) -> AgentCallParameter:
    """所見適用用 agent call parameter を構築する。"""
    # `<work-root>/oracle/src/oracle/acp_builder/apply/fork/finding_application.py`
    # is the canonical fragment. Prompt standards are owned by oracle/src, so
    # this builder loads that source of truth only at construction time.
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REALIZATION_WRITE,
        _prompt(findings),
        None,
    )


def _prompt(findings: list[dict[str, Any]]) -> str:
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.basic import FileAccessMode as OracleFileAccessMode
    from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
    from oracle.prompt_builder.complete_prompt import build_complete_prompt

    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装の修正担当です",
        summary="- `<repo-root>` ツリー内の realization file を修正すること",
        goal="""
        - 所見として指摘されている問題の修正作業をベストエフォートで実施したこと
        - 修正後の realization file が realization standard に従っている事
        """,
        file_access_mode=OracleFileAccessMode.REALIZATION_WRITE,
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
                            json.dumps(finding, ensure_ascii=False, indent=2),
                        ),
                    )
                    for i, finding in enumerate(findings)
                ],
            ),
        ],
        aux_placeholder_def={"repo-root": repo_root},
        oracle_and_realization_basic=True,
        realization_standard=True,
    )
    return render_as_markdown(prompt)
