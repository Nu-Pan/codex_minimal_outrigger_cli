# cmoc
from basic.struct_doc import StructDoc
from basic.path_model import resolve_work_root


def build_routing_rule() -> StructDoc:
    """
    INDEX.md を使って必要な文章へ進むための規則文章を構築する
    """
    work_root = resolve_work_root()
    return StructDoc(
        "routing rule",
        StructDoc(
            "INDEX.md の扱い",
            """
            - `INDEX.md` は、同階層のファイル・ディレクトリへ進むためのルーティング情報である
            - `INDEX.md` は本文の代替ではなく、読むべき本文を選ぶための案内として扱う
            - `Summary`、`Read this when`、`Do not read this when` をヒントに、作業に必要な文章を読みに行く
            """,
        ),
        StructDoc(
            "読み進め方",
            f"""
            - 作業開始時に対象領域を推定し、それと近い階層の `INDEX.md` を読む
            - 対象領域を推定出来ない場合は `{work_root}/INDEX.md` を起点に読む
            - 下位ディレクトリへ進む場合は、その階層の `INDEX.md` も必要に応じて読む
            - `INDEX.md` を読んでも判断できない場合は、候補となる本文を読んで根拠を確認する
            - 関連しそうなファイルを総当たりで読む前に、まず `INDEX.md` で候補を絞る
            """,
        ),
        StructDoc(
            "判断基準",
            """
            - `Read this when` に現在の作業が当てはまる対象を優先して読む
            - `Do not read this when` に現在の作業が当てはまる対象は、より直接の読む先を探す
            - `INDEX.md` と本文が乖離している可能性がある場合は、本文を根拠として扱う
            """,
        ),
    )
