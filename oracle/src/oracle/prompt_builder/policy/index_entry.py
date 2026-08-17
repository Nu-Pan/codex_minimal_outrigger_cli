"""INDEX.md 用エントリーを生成する agent 向け文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_index_entry_policy() -> tuple[PlaceholderMap, StructDoc]:
    """INDEX.md エントリーが従う規定を構築する。"""
    return (
        {},
        StructDoc(
            "index entry policy（`INDEX.md` 用エントリー生成時）",
            """
            **必須**

            - INDEX.md エントリーのルーティング情報には、対象を読むべき作業・質問・変更の条件を判断できる意味情報を書く
            - 対象が担う責務と、同階層の他対象ではなくその対象へ進む理由を書く
            - 対象内容から根拠を持って言える責務・入口・読む条件だけを書く
            - 対象を読まなくてよい境界や、より直接読むべき別対象がある場合の境界を書く
            - INDEX.md エントリーには、機械的な識別情報ではなく、対象を読むべきか判断するための意味情報だけを書く

            **禁止**

            - ルーティング情報である INDEX.md エントリーに、対象本文を読まなければ理解できない詳細説明を展開してはいけない
            - 関連しそうという理由だけで対象へ進ませるような広すぎる条件を書いてはいけない
            - 推測で対象外の責務や将来の用途を広げてはいけない
            - ファイル名・ディレクトリ名・ハッシュ値のような機械的に補える情報を書いてはいけない
            - Structured Output schema を読めば分かる出力項目名・型・形式を説明してはいけない
            """,
        ),
    )
