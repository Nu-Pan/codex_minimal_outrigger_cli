"""情報源への参照形式を定める agent 向け文面の構築定義。"""

from reference.other.struct_doc import SDHeader, SDPolicy
from reference.prompt_builder.basic import PlaceholderMap


def build_reference_policy() -> tuple[PlaceholderMap, SDHeader]:
    """decision、spec、その他の情報源への参照規定を構築する。"""
    # 参照先の種類に応じた表記と、詳細位置を示す情報をまとめる。
    return (
        {},
        SDHeader(
            "reference policy",
            SDPolicy(
                what_is_this="情報源への参照形式に関する規定を以下に示す",
                require=(
                    "decision への参照は「◯◯◯については [DECI-XXXXXX] を参照すること」の形式で記述すること",
                    "spec への参照は「◯◯◯については [SPEC-XXXXXX] を参照すること」の形式で記述すること",
                    "その他の情報源への参照は「◯◯◯については `<major-location>` の `<minor-location>` を参照すること」の形式で記述すること",
                    "`<major-location>` には、「ファイルパス」「URL」などの、読むべきファイルのパス情報を書くこと",
                    "`<minor-location>` には、「見出し名」「参照先の記述の一部」などの、`<major-location>` 内の詳細位置を特定出来る短いヒントを書くこと",
                ),
            ),
        ),
    )
