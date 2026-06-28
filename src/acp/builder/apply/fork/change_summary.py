"""`cmoc apply fork` の変更要約生成 builder。"""

from pathlib import Path

from acp.builder.apply.fork._common import resolve_repo_root
from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


def build_apply_fork_change_summary_parameter(raw_git_diff: str) -> AgentCallParameter:
    """作業レポート用の変更要約 agent call parameter を構築する。"""
    # `<work-root>/oracle/src/oracle/acp_builder/apply/fork/change_summary.py`
    # is the canonical fragment. This realization must not import oracle/src at
    # runtime because normal `cmoc` startup exposes only `src`.
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        _prompt(raw_git_diff),
        Path(__file__).with_suffix(".json"),
    )


def _prompt(raw_git_diff: str) -> str:
    repo_root = resolve_repo_root()
    return f"""# role

- あなたはソフトウェア変更内容の要約担当です

# summary

- `{repo_root}` ツリー内の差分を、人間が読む用に要約すること

# goal

- `{repo_root}` ツリー内の差分を、指定の Structured Output schema に従って返却すること

# file read write rule - readonly

- `{repo_root}` ツリー外は読み書き禁止
- `{repo_root}` ツリー内は書き込み禁止

# routing rule

- `INDEX.md` を手がかりに必要な本文を読むこと

# ツリー内の差分

```diff
{raw_git_diff}
```

# place holder definition

- <repo-root> = {repo_root}
"""
