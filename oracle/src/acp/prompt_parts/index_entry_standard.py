# cmoc
from basic.struct_doc import StructDoc, ntqs


def build_index_entry_standard() -> StructDoc:
    """
    `INDEX.md` のエントリーが従うべき規範文章を生成する
    """
    return StructDoc(
        "index entry standard",
        """
        - `INDEX.md` のエントリーは、読むべきファイル・ディレクトリへ AI を案内するためのルーティング情報である
        - `summary` には、対象に何が書いてあるか、または対象に何が入っているかを、人間向けの簡潔な箇条書き項目として返す
        - `summary` には、対象の役割、扱う内容、下位要素への入口としての位置づけを含める
        - `read_this_when` には、AI が対象を読む判断を下す具体的な条件を箇条書き項目として返す
        - `read_this_when` には、どんな作業・質問・変更のときに対象から確認を始めるべきかを書く
        - `do_not_read_this_when` には、AI が関連しそうという理由だけで過剰に読みに行かないための条件を箇条書き項目として返す
        - `do_not_read_this_when` には、対象を読まなくてよい場合、または別のファイル・下位項目へ直接進む方が適切な場合を書く
        - ファイル名、ディレクトリ名、hash は返さない
        - 機械的に補える情報ではなく、対象を読むべきか判断するための意味情報だけを返す
        - 対象内容から根拠を持って言えることだけを書き、推測で対象外の責務を広げない
        """,
    )
