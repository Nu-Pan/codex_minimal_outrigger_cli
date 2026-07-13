"""quota availability probe の互換 adapter。

正本 builder は `<work-root>/oracle/src/oracle/acp_builder/quota_probe.py` に
置く契約だが、現在の work-root にはまだ存在しない。正本が追加されるまでは
quota 復帰を止めない最小 fallback を使う。

この adapter と fallback は、正本 builder の追加後に `acp.builder.quota_probe`
参照が realization と利用者からなくなった時点で削除する。
"""

from importlib import import_module

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from basic.struct_doc import render_as_markdown
from oracle.prompt_builder.parts.file_access_rule import build_file_access_rule


__all__ = ["build_quota_availability_probe_parameter"]


def _fallback_prompt() -> str:
    # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # Keep the READONLY wording owned by the oracle prompt part while the
    # quota-specific fallback remains only an adapter concern.
    _, file_access_rule = build_file_access_rule(FileAccessMode.READONLY)
    return (
        render_as_markdown(file_access_rule)
        + "\n# quota availability probe\n\n"
        + "quota 回復確認です。実行可能なら OK とだけ返してください。\n"
    )


# The canonical part resolves roots from ambient cwd; render it once so
# concurrent probe calls cannot observe another call's temporary root lookup.
_FALLBACK_PROMPT = _fallback_prompt()


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    """正本 builder があれば委譲し、欠落時は quota 待機用の最小値を返す。"""
    try:
        oracle_module = import_module("oracle.acp_builder.quota_probe")
    except ModuleNotFoundError as exc:
        if exc.name != "oracle.acp_builder.quota_probe":
            raise
    else:
        return oracle_module.build_quota_availability_probe_parameter(base_parameter)

    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # 正本 builder が未配置でも、quota 復帰の probe だけは実行可能にする。
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        _FALLBACK_PROMPT,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )
