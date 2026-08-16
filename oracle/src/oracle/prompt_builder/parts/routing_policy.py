# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_routing_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, StructDoc]:
    """
    INDEX.md を使って必要な文章へ進むための規定文面を構築する
    """
    # この part の文面が参照する root 定義を call-scoped context から取得する
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        StructDoc(
            "routing policy",
            """
            - `INDEX.md` は、同階層の対象へ進むための routing 情報であり、本文の代替ではない
            - 作業対象に近い階層の `INDEX.md` から読み始め、対象領域を推定できない場合は `{{work-root}}/INDEX.md` を起点にする
            - `Summary`、`Read this when`、および `Do not read this when` で候補を絞ってから、必要な本文を読む
            - 下位ディレクトリへ進む場合は、その階層の `INDEX.md` も必要に応じて使用する
            - `INDEX.md` と本文が異なる場合、意味の根拠には本文を使用する
            - 関連候補を総当たりで読む前に routing で対象を絞る
            """,
        ),
    )
