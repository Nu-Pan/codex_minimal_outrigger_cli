# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_routing_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """
    INDEX.md を使って必要な文章へ進むための規定文面を構築する

    NOTE
        意味仕様は `oracle/doc/app_spec/indexing.md:79` の
        「`INDEX.md` による routing」を参照。
    """
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        SDHeader(
            "routing policy",
            SDPolicy(
                what_is_this="`{{work-root}}` ツリー内のどのファイルを読むべきか特定する時に従うべき規定を以下に示す",
                require=(
                    "`INDEX.md` はどのファイル・ディレクトリを読むべきか判断・特定するための routing 情報として用いること",
                    "原則としては作業対象に近い階層の `INDEX.md` を起点とするが、対象領域を推定できない場合は `{{work-root}}/INDEX.md` を起点にする",
                    "`INDEX.md` と本文とで内容が食い違う場合は本文を優先すること",
                    "`INDEX.md` を本文の代替にせず、必ず本文を判断の根拠とすること",
                ),
                supplemental=(
                    "`INDEX.md` は各階層に存在し、同階層のファイル・ディレクトリの説明が書かれている",
                ),
            ),
        ),
    )
