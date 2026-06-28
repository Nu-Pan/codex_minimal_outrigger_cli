"""`cmoc apply fork` のファイル単位所見列挙 builder。"""

from pathlib import Path

from acp.builder.apply.fork._common import resolve_repo_root
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
    # is the canonical fragment. Runtime imports must stay inside `src`.
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        _prompt(target_path),
        Path(__file__).with_suffix(".json"),
    )


def _prompt(target_path: Path) -> str:
    repo_root = resolve_repo_root()
    target = target_path.resolve()
    return f"""# role

- あなたはソフトウェア実装の所見リストアップ担当です

# summary

- `{target}` を起点に `{repo_root}` ツリー内の所見 (realization file の要修正点) を調査すること

# goal

- `{target}` 以外の必要な oracle file, realization file も読んでいること
- 指定された Structured Output schema に従って所見リストを返すこと
- 列挙した所見リストが apply review standard を満たしている事

# file read write rule - readonly

- `{repo_root}` ツリー外は読み書き禁止
- `{repo_root}` ツリー内は書き込み禁止

# routing rule

- `INDEX.md` を手がかりに必要な本文を読むこと
- 関連しそうなファイルを総当たりで読む前に、まず `INDEX.md` で候補を絞ること

# oracle and realization basic

- oracle file は `{repo_root}/oracle` ツリー内の正本仕様断片である
- realization file は `{repo_root}` ツリー内かつ `{repo_root}/oracle` ツリー外の実現物である
- INDEX.md はルーティング情報であり、所見対象の本文としては扱わない

# apply review standard

- 明確に修正が必要な oracle file と realization file の不整合だけを所見にすること
- 仕様断片の隙間で実装者裁量として成立する差分を所見にしないこと
- クオリティアップだけを目的にした指摘ではなく、実行不能・仕様不一致・安全性問題など修正根拠が明確な問題だけを列挙すること
- 各所見には、根拠位置、oracle requirement、observed implementation、reason、suggested fix を含めること

# place holder definition

- <repo-root> = {repo_root}
- <target-path> = {target}
"""
