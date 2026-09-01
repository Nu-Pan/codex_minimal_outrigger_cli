"""明示的に選択された editor input handoff 規定文面の構築定義。"""

# cmoc
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_editor_input_handoff_policy() -> tuple[PlaceholderMap, SDHeader]:
    """明示的に選択された editor input handoff 規定を構築する。

    NOTE
        意味仕様は `oracle/doc/app_spec/editor_input_handoff.md` を参照。
    """
    return (
        {},
        SDHeader(
            "editor input handoff",
            SDPolicy(
                what_is_this="active な prompt editor input へ完成済み内容を渡す方法を以下に示す",
                require=(
                    "人間が active target への handoff を明示的に要求し、target ID を提示した場合だけ `cmoc_editor_input.overwrite` を使用すること",
                    "提示された target ID と editor work file 全体の完成済み content を tool に渡すこと",
                    "tool の結果を正確に報告し、handoff の成否にかかわらず agent call に要求された回答または成果物を満たすこと",
                    "handoff に失敗した場合は、必要に応じて手動で利用できる完成済み content を回答へ残すこと",
                ),
                prohibit=(
                    "handoff の代替として editor work file へ直接書き込んだり、sandbox escalation を要求したりしてはならない",
                ),
            ),
        ),
    )
