"""明示的に選択された editor input handoff 規定文面の構築定義。"""

# cmoc
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_editor_input_handoff_policy() -> tuple[PlaceholderMap, SDHeader]:
    """明示的に選択された editor input handoff 規定を構築する。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の
        「agent の責務と権限」を参照。
    """
    # tool の各項目への記述と、handoff の成否に依存しない成果責務を伝える。
    return (
        {},
        SDHeader(
            "editor input handoff",
            SDPolicy(
                what_is_this="別セッションへの handoff 操作が満たすべき規定以下に示す",
                require=(
                    "人間が active target への handoff を明示的に要求し、target ID を提示した場合だけ MCP tool `cmoc_editor_input.overwrite` を使用すること",
                    "handoff する各項目は、送り元の会話を読まなくても依頼を理解できる内容にすること",
                    "handoff の成否にかかわらず agent call に要求された回答または成果物を満たすこと",
                    "handoff に失敗した場合は、必要に応じて自分が作成した依頼・コンテキスト部分を手動利用できる形で回答へ残すこと",
                ),
                prohibit=(
                    "経緯や決定が存在しない箇所を勝手に補ってはならない",
                    "handoff を根拠とした作業スコープの拡大はしてはならない",
                    "handoff に失敗した場合の代替手段として sandbox escalation を要求してはならない",
                ),
            ),
        ),
    )
