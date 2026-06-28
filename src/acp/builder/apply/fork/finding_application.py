"""`cmoc apply fork` の所見適用 builder。"""

import json
from typing import Any

from acp.builder.apply.fork._common import resolve_repo_root
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
    # is the canonical fragment. Runtime imports must stay inside `src`.
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REALIZATION_WRITE,
        _prompt(findings),
        None,
    )


def _prompt(findings: list[dict[str, Any]]) -> str:
    repo_root = resolve_repo_root()
    return f"""# role

- あなたはソフトウェア実装の修正担当です

# summary

- `{repo_root}` ツリー内の realization file を修正すること

# goal

- 所見として指摘されている問題の修正作業をベストエフォートで実施したこと
- 修正後の realization file が realization standard に従っている事

# file read write rule - realization_write

- `{repo_root}` ツリー外は読み書き禁止
- `{repo_root}/oracle` ツリー内は書き込み禁止
- `{repo_root}/.agents` ツリー内は書き込み禁止
- `{repo_root}/memo` は読み書き禁止

# routing rule

- `INDEX.md` を手がかりに必要な本文を読むこと
- 関連しそうなファイルを総当たりで読む前に、まず `INDEX.md` で候補を絞ること

# 作業上の注意点

- 所見本文は作業のためのヒントであり、絶対に従うべき指示書ではない
- git add と git commit は実行禁止

# 所見本文

```json
{json.dumps({"findings": findings}, ensure_ascii=False, indent=2)}
```

# place holder definition

- <repo-root> = {repo_root}
"""
