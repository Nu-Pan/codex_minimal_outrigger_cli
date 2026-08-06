# cmoc
from typing import Callable

from oracle.acp_builder.basic import FileAccessMode
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructBlock, StructDoc

from .basic import PlaceholderMap

# local
from .parts.apply_review_standard import build_apply_review_standard
from .parts.conflict_resolution_standard import build_conflict_resolution_standard
from .parts.feedback_reporting_standard import build_feedback_reporting_standard
from .parts.file_access_rule import build_file_access_rule
from .parts.index_entry_standard import build_index_entry_standard
from .parts.oracle_and_realization_basic import build_oracle_and_realization_basic
from .parts.oracle_review_standard import build_oracle_review_standard
from .parts.oracle_standard import build_oracle_standard
from .parts.realization_oracle_reference_rule import (
    build_realization_oracle_reference_rule,
)
from .parts.realization_standard import build_realization_standard
from .parts.routing_rule import build_routing_rule


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
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    path_context: AgentCallPathContext,
    aux_static_prompt: list[StructDoc | StructBlock] = list(),
    aux_dynamic_prompt: list[StructDoc | StructBlock] = list(),
    aux_placeholder_def: PlaceholderMap = dict(),
    oracle_and_realization_basic: bool = False,
    oracle_standard: bool = False,
    realization_standard: bool = False,
    oracle_review_standard: bool = False,
    apply_review_standard: bool = False,
    conflict_resolution_standard: bool = False,
    realization_oracle_reference_rule: bool = False,
    index_entry_standard: bool = False,
) -> list[StructDoc | StructBlock]:
    """agent call にそのまま渡すことができる完全なプロンプトを構築する

    入力プロンプトキャッシュヒット率の観点から、以下の工夫を取り入れている

    - 呼び出し内容によらず不変なプロンプトパーツを「静的プロンプト」として前半にまとめる
    - 呼び出し内容次第で変わりうるプロンプトパーツを「動的プロンプト」として後半にまとめる
    - 静的プロンプトのうち、出現頻度の高いものを前半側に持ってくる
    - プロンプトパーツの順序は一定にする
    - 完全固定文言の「プロンプト内地図」を先頭に置き、今回の用件などの重要情報を参照する
    - 変動要素を可能な限りプレースホルダ化し、実際の値との対応関係を動的プロンプト側で書くことで、変動要素だけを動的プロンプト側に押しやる

    role:
        agent が果たすべき役割の短い説明

    summary:
        agent への依頼する作業の概要・短い説明

    goal:
        agent が作業完了と判断する条件・基準

    file_access_mode:
        agent によるファイルアクセスに対する制限設定

    path_context:
        AgentCallParameter.agent_call_cwd から事前に構築した call-scoped path context

    aux_static_prompt:
        任意に追加可能な静的プロンプト
        毎回必ず同じ文面となるプロンプトはこちら

    aux_dynamic_prompt:
        任意に追加可能な動的プロンプト
        毎回変化する可能性があるプロンプトはこちら

    aux_placeholder_def:
        任意に追加可能なプレースホルダ定義

    oracle_and_realization_basic:
        True の時、oracle, realization についての基本情報をプロンプトに注入する

    oracle_standard:
        True の時、oracle standard をプロンプトに注入する

    realization_standard:
        True の時、realization standard をプロンプトに注入する

    oracle_review_standard:
        True の時、oracle review standard をプロンプトに注入する

    apply_review_standard:
        True の時、apply review standard をプロンプトに注入する

    conflict_resolution_standard:
        True の時、conflict resolution standard をプロンプトに注入する

    realization_oracle_reference_rule:
        True の時、realization code から oracle file path を参照する規則を
        プロンプトに注入する

    index_entry_standard:
        True の時、index entry standard をプロンプトに注入する

    return:
        agent call にそのまま渡すことができる完全なプロンプト
    """
    # 完全 prompt 自身が参照できる root 定義を call-scoped context から初期化する
    ph_map: PlaceholderMap = path_context.root_placeholder_definitions()
    _merge_placeholder_definitions(ph_map, aux_placeholder_def)

    # 動的プロンプトの参照先
    role_block = StructBlock("role", StructDoc("role", role))
    summary_block = StructBlock("summary", StructDoc("summary", summary))
    goal_block = StructBlock("goal", StructDoc("goal", goal))

    # 構築先プロンプト。先頭要素の文言と順序は入力に依存させない。
    prompt: list[StructDoc | StructBlock] = [
        StructDoc(
            "プロンプト内地図",
            StructDoc("あなたの役割", '<cmoc_ref target="role"/>'),
            StructDoc("依頼の概要", '<cmoc_ref target="summary"/>'),
            StructDoc("作業の完了条件", '<cmoc_ref target="goal"/>'),
        )
    ]

    # 構築ユーティリティ
    def _extend_static_prompt(build_fn: Callable, *args, **kwargs):
        temp_ph_map, temp_prompt = build_fn(*args, **kwargs)
        _merge_placeholder_definitions(ph_map, temp_ph_map)
        prompt.append(temp_prompt)

    # 適合性規範が依存する規範を決定論的に有効化する。
    if apply_review_standard:
        realization_standard = True
    if realization_standard or oracle_review_standard:
        oracle_standard = True

    # 下位規則が参照する cmoc 固有概念も同時に注入する。
    if (
        oracle_standard
        or realization_standard
        or oracle_review_standard
        or apply_review_standard
        or conflict_resolution_standard
        or realization_oracle_reference_rule
        or index_entry_standard
    ):
        oracle_and_realization_basic = True

    # 静的プロンプトを構築
    # feedback reporting は個別 builder や Structured Output 契約へ重複させず、
    # 全 agent call に共通するこの経路で常に注入する。
    _extend_static_prompt(build_feedback_reporting_standard, path_context)
    if oracle_and_realization_basic:
        _extend_static_prompt(build_oracle_and_realization_basic, path_context)
    if oracle_standard:
        _extend_static_prompt(build_oracle_standard, path_context)
    if realization_standard:
        _extend_static_prompt(build_realization_standard, path_context)
    if apply_review_standard:
        _extend_static_prompt(build_apply_review_standard)
    if oracle_review_standard:
        _extend_static_prompt(build_oracle_review_standard)
    if conflict_resolution_standard:
        _extend_static_prompt(build_conflict_resolution_standard)
    if realization_oracle_reference_rule:
        _extend_static_prompt(build_realization_oracle_reference_rule, path_context)
    if index_entry_standard:
        _extend_static_prompt(build_index_entry_standard)
    if aux_static_prompt:
        prompt.extend(aux_static_prompt)
    if file_access_mode != FileAccessMode.NO_RULE:
        _extend_static_prompt(build_file_access_rule, file_access_mode, path_context)
    _extend_static_prompt(build_routing_rule, path_context)

    # 動的プロンプトを構築
    prompt.extend((role_block, summary_block, goal_block))
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
