"""完全 prompt の構築定義。"""

from oracle.acp_builder.basic import FileAccessMode
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDTagBlock

from .basic import PlaceholderMap

# local
from .parts.oracle_and_realization_basic import build_oracle_and_realization_basic
from .policy.conflict_resolution import build_conflict_resolution_policy
from .policy.feedback_reporting import build_feedback_reporting_policy
from .policy.file_access import build_file_access_policy
from .policy.index_entry import build_index_entry_policy
from .policy.oracle import build_oracle_policy
from .policy.oracle_findings import build_oracle_findings_policy
from .policy.realization import build_realization_policy
from .policy.realization_findings import build_realization_findings_policy
from .policy.routing import build_routing_policy


def _merge_placeholder_definitions(
    destination: PlaceholderMap,
    source: PlaceholderMap,
) -> None:
    """同名 placeholder の異値上書きを拒否しながら定義を統合する。

    NOTE
        各 part は参照する placeholder だけを申告し、同じ文字列表現の重複は統合する。
        同名異値を後勝ちにすると call 内で path context が分裂するため拒否する。
    """
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
    aux_static_prompt: list[SDHeader | SDTagBlock] = list(),
    aux_dynamic_prompt: list[SDHeader | SDTagBlock] = list(),
    aux_placeholder_def: PlaceholderMap = dict(),
    oracle_and_realization_basic: bool = False,
    oracle_policy: bool = False,
    realization_policy: bool = False,
    oracle_findings_policy: bool = False,
    realization_findings_policy: bool = False,
    conflict_resolution_policy: bool = False,
    index_entry_policy: bool = False,
    routing_policy: bool = False,
) -> list[SDHeader | SDTagBlock]:
    """選択された agent 向け文面を完全 prompt として構築する。

    Args:
        summary: agent の担当、主作業、対象、および作業範囲。
        goal: agent call の終了時に満たされるべき状態。
        routing_policy: repository 内の参照先を選ぶ routing 文面を含めるか。

    Returns:
        agent call へ渡す構造化済み prompt。

    NOTE
        プロンプトは変動が少ないものを前に、変動が多いものを後に配置する。
        これはキャッシュヒット率を上げるための措置。
    NOTE
        policy 系の有効・無効化フラグの効果は相互に独立。
        勝手に前提規定を有効化したりはしない。
    """
    # place holder map 構築先
    ph_map: PlaceholderMap = path_context.root_placeholder_definitions()
    _merge_placeholder_definitions(ph_map, aux_placeholder_def)

    # プロンプト構築ユーティリティ
    def _append(
        target_prompt: list[SDHeader | SDTagBlock],
        builder_result: tuple[PlaceholderMap, SDHeader],
    ) -> None:
        temp_ph_map, temp_prompt = builder_result
        _merge_placeholder_definitions(ph_map, temp_ph_map)
        target_prompt.append(temp_prompt)

    # 最終的なフルプロンプト構築先
    # NOTE
    #   読み飛ばされると困る内容は prompt 先頭で参照を明示する。
    full_prompt: list[SDHeader | SDTagBlock] = list()
    full_prompt.append(
        SDHeader(
            "プロンプト内の重要な情報",
            """
            - このセッションにおける基礎的な作業規定: <cmoc_ref target="fundamental_policy"/>
            - このセッションの目的: <cmoc_ref target="objective"/>
            """,
        )
    )

    # 基礎規定プロンプト
    # NOTE
    #   無視されると困るような、全ての作業の基礎となるような作業規定
    #   重要な指示なので StructBlock で囲って「プロンプト内地図」から参照する
    fundamental_policy_prompt: list[SDHeader | SDTagBlock] = list()
    _append(
        fundamental_policy_prompt,
        build_feedback_reporting_policy(path_context),
    )
    if file_access_mode != FileAccessMode.NO_POLICY:
        _append(
            fundamental_policy_prompt,
            build_file_access_policy(file_access_mode, path_context),
        )
    if routing_policy:
        _append(
            fundamental_policy_prompt,
            build_routing_policy(path_context),
        )
    if oracle_and_realization_basic:
        _append(
            fundamental_policy_prompt,
            build_oracle_and_realization_basic(path_context),
        )
    full_prompt.append(SDTagBlock("fundamental_policy", *fundamental_policy_prompt))

    # 基礎的ではない規定プロンプト
    # NOTE
    #   基礎とか根幹ってほどじゃないけど、でも大事な規定。
    # NOTE
    #   指定された通りに規定の有効・無効を反映する。
    #   依存先規定の自動注入みたいな余計なことはしない
    if oracle_policy:
        _append(
            full_prompt,
            build_oracle_policy(),
        )
    if realization_policy:
        _append(
            full_prompt,
            build_realization_policy(path_context),
        )
    if oracle_findings_policy:
        _append(
            full_prompt,
            build_oracle_findings_policy(),
        )
    if realization_findings_policy:
        _append(
            full_prompt,
            build_realization_findings_policy(),
        )
    if conflict_resolution_policy:
        _append(
            full_prompt,
            build_conflict_resolution_policy(),
        )
    if index_entry_policy:
        _append(
            full_prompt,
            build_index_entry_policy(),
        )

    # caller 指定の追加プロンプト (static)
    if aux_static_prompt:
        full_prompt.extend(aux_static_prompt)

    # caller 指定の目的
    full_prompt.append(
        SDTagBlock(
            "objective",
            SDHeader("summary", summary),
            SDHeader("goal", goal),
        )
    )

    # caller 指定の追加プロンプト (dynamic)
    if aux_dynamic_prompt:
        full_prompt.extend(aux_dynamic_prompt)

    # placeholder 定義
    # NOTE
    #   特にパスはものすごく変動するので、絶対にプロンプト末尾に置く。
    full_prompt.append(
        SDHeader(
            "place holder definition",
            "\n".join(f"- {{{{{k}}}}} = {v}" for k, v in ph_map.items()),
        )
    )

    return full_prompt
