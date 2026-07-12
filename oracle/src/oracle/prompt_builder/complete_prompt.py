# cmoc
from oracle.other.struct_doc import StructDoc
from copy import deepcopy
from typing import Callable

# local
from .parts.file_access_rule import build_file_access_rule
from .parts.oracle_standard import build_oracle_standard
from .parts.realization_standard import build_realization_standard
from .parts.oracle_and_realization_basic import build_oracle_and_realization_basic
from .parts.apply_review_standard import build_apply_review_standard
from .parts.oracle_review_standard import build_review_oracle_standard
from .parts.index_entry_standard import build_index_entry_standard
from .parts.routing_rule import build_routing_rule
from .basic import PlaceholderMap
from oracle.acp_builder.basic import FileAccessMode


def build_complete_prompt(
    *,
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    aux_static_prompt: list[StructDoc] = list(),
    aux_dynamic_prompt: list[StructDoc] = list(),
    aux_placeholder_def: PlaceholderMap = dict(),
    oracle_and_realization_basic: bool = False,
    oracle_standard: bool = False,
    realization_standard: bool = False,
    review_oracle_standard: bool = False,
    apply_review_standard: bool = False,
    index_entry_standard: bool = False,
) -> list[StructDoc]:
    """agent call にそのまま渡すことができる完全なプロンプトを構築する

    入力プロンプトキャッシュヒット率の観点から、以下の工夫を取り入れている

    - 呼び出し内容によらず不変なプロンプトパーツを「静的プロンプト」として前半にまとめる
    - 呼び出し内容次第で変わりうるプロンプトパーツを「動的プロンプト」として後半にまとめる
    - 静的プロンプトのうち、出現頻度の高いものを前半側に持ってくる
    - プロンプトパーツの順序は一定にする
    - 先頭の固定プロンプトパーツで、今回の用件などの重要情報への参照を明言する
    - 変動要素を可能な限りプレースホルダ化し、実際の値との対応関係を動的プロンプト側で書くことで、変動要素だけを動的プロンプト側に押しやる

    role:
        agent が果たすべき役割の短い説明

    summaey:
        agent への依頼する作業の概要・短い説明

    goal:
        agent が作業完了と判断する条件・基準

    file_access_mode:
        agent によるファイルアクセスに対する制限設定

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

    review_oracle_standard:
        True の時、review oracle standard をプロンプトに注入する

    apply_review_standard:
        True の時、apply review standard をプロンプトに注入する

    index_entry_standard:
        True の時、index entry standard をプロンプトに注入する

    return:
        agent call にそのまま渡すことができる完全なプロンプト
    """
    # プレースホルダマップ
    if aux_placeholder_def:
        ph_map = deepcopy(aux_placeholder_def)
    else:
        ph_map = dict()

    # 構築先プロンプト
    prompt = []

    # 構築ユーティリティ
    def _extend_static_prompt(build_fn: Callable, *args, **kwargs):
        temp_ph_map, temp_prompt = build_fn(*args, **kwargs)
        ph_map.update(**temp_ph_map)
        prompt.append(temp_prompt)

    # 注入プロンプトを調整
    # NOTE
    #   例えば、`oracle_standard` の内容を理解するには `oracle_and_realization_basic` の内容を一緒に伝える必要がある。
    #   そういった、依存関係の有る情報がけっそんしないようにフラグを調整する。
    if oracle_and_realization_basic:
        pass
    if oracle_standard:
        oracle_and_realization_basic = True
    if realization_standard:
        oracle_and_realization_basic = True
    if review_oracle_standard:
        oracle_and_realization_basic = True
        oracle_standard = True
    if apply_review_standard:
        oracle_and_realization_basic = True
        realization_standard = True
    if index_entry_standard:
        oracle_and_realization_basic = True
        oracle_standard = True
        realization_standard = True

    # 静的プロンプトを構築
    if oracle_and_realization_basic:
        _extend_static_prompt(build_oracle_and_realization_basic)
    if oracle_standard:
        _extend_static_prompt(build_oracle_standard)
    if realization_standard:
        _extend_static_prompt(build_realization_standard)
    if apply_review_standard:
        _extend_static_prompt(build_apply_review_standard)
    if review_oracle_standard:
        _extend_static_prompt(build_review_oracle_standard)
    if index_entry_standard:
        _extend_static_prompt(build_index_entry_standard)
    if aux_static_prompt:
        prompt.extend(aux_static_prompt)
    if file_access_mode != FileAccessMode.NO_RULE:
        _extend_static_prompt(build_file_access_rule, file_access_mode)
    _extend_static_prompt(build_routing_rule)

    # 動的プロンプトを構築
    prompt.append(
        StructDoc(
            "role",
            role,
        )
    )
    prompt.append(
        StructDoc(
            "summary",
            summary,
        )
    )
    prompt.append(
        StructDoc(
            "goal",
            goal,
        )
    )
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
