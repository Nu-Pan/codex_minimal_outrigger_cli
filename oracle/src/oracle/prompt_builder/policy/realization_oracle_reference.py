# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader
from oracle.prompt_builder.basic import PlaceholderMap


def build_realization_oracle_reference_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """realization code から oracle file path を参照する規定を構築する。"""
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        SDHeader(
            "realization oracle reference policy（realization code の作成・変更時）",
            """
            **必須**

            - 対応する oracle file が存在する場合、realization code のコメントに `{{work-root}}` 起点の oracle file path を書く
            """,
        ),
    )
