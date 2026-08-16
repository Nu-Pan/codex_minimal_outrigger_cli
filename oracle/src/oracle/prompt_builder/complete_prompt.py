# cmoc
from typing import Callable

from oracle.acp_builder.basic import FileAccessMode
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructBlock, StructDoc

from .basic import PlaceholderMap

# local
from .parts.oracle_and_realization_basic import build_oracle_and_realization_basic
from .policy.apply_review import build_apply_review_policy
from .policy.conflict_resolution import build_conflict_resolution_policy
from .policy.editor_handoff import build_editor_handoff_policy
from .policy.feedback_reporting import build_feedback_reporting_policy
from .policy.file_access import build_file_access_policy
from .policy.index_entry import build_index_entry_policy
from .policy.oracle import (
    build_oracle_investigation_policy,
    build_oracle_policy,
)
from .policy.oracle_review import build_oracle_review_policy
from .policy.realization import build_realization_policy
from .policy.realization_oracle_reference import (
    build_realization_oracle_reference_policy,
)
from .policy.routing import build_routing_policy


def _merge_placeholder_definitions(
    destination: PlaceholderMap,
    source: PlaceholderMap,
) -> None:
    """同名 placeholder の異値上書きを拒否しながら定義を統合する。"""
    # 既存値と文字列表現が一致する定義だけを重複として許容する
    for name, value in source.items():
        if name in destination and str(destination[name]) != str(value):
            raise ValueError(
                "Conflicting placeholder definition "
                f"(name={name}, current={destination[name]}, new={value})"
            )
        destination.setdefault(name, value)


def build_complete_prompt(
    *,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    path_context: AgentCallPathContext,
    aux_static_prompt: list[StructDoc | StructBlock] = list(),
    aux_dynamic_prompt: list[StructDoc | StructBlock] = list(),
    aux_placeholder_def: PlaceholderMap = dict(),
    oracle_and_realization_basic: bool = False,
    oracle_policy: bool = False,
    oracle_investigation_policy: bool = False,
    realization_policy: bool = False,
    oracle_review_policy: bool = False,
    apply_review_policy: bool = False,
    conflict_resolution_policy: bool = False,
    editor_handoff_policy: bool = False,
    realization_oracle_reference_policy: bool = False,
    index_entry_policy: bool = False,
    routing_policy: bool = False,
) -> list[StructDoc | StructBlock]:
    """選択された agent 向け文面を完全 prompt として構築する。

    Args:
        summary: agent の担当、主作業、対象、および作業範囲。
        goal: agent call の終了時に満たされるべき状態。
        oracle_investigation_policy: oracle file の読み取り専用調査に必要な
            policy block を含めるか。
        editor_handoff_policy: editor work file への handoff に必要な
            policy block を含めるか。
        routing_policy: repository 内の参照先を選ぶ routing 文面を含めるか。

    Returns:
        agent call へ渡す構造化済み prompt。
    """
    # 完全 prompt 自身が参照できる root 定義を call-scoped context から初期化する
    ph_map: PlaceholderMap = path_context.root_placeholder_definitions()
    _merge_placeholder_definitions(ph_map, aux_placeholder_def)

    # 動的プロンプトの参照先
    summary_block = StructBlock("summary", StructDoc("summary", summary))
    goal_block = StructBlock("goal", StructDoc("goal", goal))

    # 構築先プロンプト。先頭要素の文言と順序は入力に依存させない。
    prompt: list[StructDoc | StructBlock] = [
        StructDoc(
            "プロンプト内地図",
            StructDoc("担当と依頼の概要", '<cmoc_ref target="summary"/>'),
            StructDoc("作業の完了条件", '<cmoc_ref target="goal"/>'),
        )
    ]

    # 構築ユーティリティ
    def _extend_static_prompt(build_fn: Callable, *args, **kwargs):
        temp_ph_map, temp_prompt = build_fn(*args, **kwargs)
        _merge_placeholder_definitions(ph_map, temp_ph_map)
        prompt.append(temp_prompt)

    # 静的プロンプトを構築
    # feedback reporting は個別 builder や Structured Output 契約へ重複させず、
    # 全 agent call に共通するこの経路で常に注入する。
    _extend_static_prompt(build_feedback_reporting_policy, path_context)
    if oracle_and_realization_basic:
        _extend_static_prompt(build_oracle_and_realization_basic, path_context)
    if oracle_policy:
        _extend_static_prompt(build_oracle_policy)
    if oracle_investigation_policy:
        _extend_static_prompt(build_oracle_investigation_policy)
    if realization_policy:
        _extend_static_prompt(build_realization_policy)
    if oracle_review_policy:
        _extend_static_prompt(build_oracle_review_policy)
    if apply_review_policy:
        _extend_static_prompt(build_apply_review_policy)
    if conflict_resolution_policy:
        _extend_static_prompt(build_conflict_resolution_policy)
    if editor_handoff_policy:
        _extend_static_prompt(build_editor_handoff_policy)
    if realization_oracle_reference_policy:
        _extend_static_prompt(build_realization_oracle_reference_policy, path_context)
    if index_entry_policy:
        _extend_static_prompt(build_index_entry_policy)
    if aux_static_prompt:
        prompt.extend(aux_static_prompt)
    if file_access_mode != FileAccessMode.NO_POLICY:
        _extend_static_prompt(build_file_access_policy, file_access_mode, path_context)
    if routing_policy:
        _extend_static_prompt(build_routing_policy, path_context)

    # 動的プロンプトを構築
    prompt.extend((summary_block, goal_block))
    prompt.extend(aux_dynamic_prompt)

    # プレースホルダマップを構築
    prompt.append(
        StructDoc(
            "place holder definition",
            "\n".join(f"- {{{{{k}}}}} = {v}" for k, v in ph_map.items()),
        )
    )

    # パターンプロンプトの注入
    return prompt
