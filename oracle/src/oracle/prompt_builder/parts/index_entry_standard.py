# cmoc
from oracle.other.struct_doc import StructDoc
from oracle.other.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)
from oracle.prompt_builder.basic import PlaceholderMap


def build_index_entry_standard() -> tuple[PlaceholderMap, StructDoc]:
    """
    `INDEX.md` のエントリーが従うべき規範文章を生成する
    """
    standards = [
        Standard(
            title="INDEX.md エントリーは読むべき対象へのルーティング情報である",
            backgrounds=[
                "AI agent は作業前に INDEX.md を読み、どのファイル・ディレクトリへ進むべきかを判断する",
                "INDEX.md エントリーの価値は、対象本文を読む前に、読むべきかどうかを判断できることにある",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "対象を読むべき作業・質問・変更の条件を判断できる意味情報を書く",
                ),
                Requirement(
                    "必須",
                    "対象が担う責務と、同階層の他対象ではなくその対象へ進む理由を書く",
                ),
                Requirement(
                    "禁止",
                    "対象本文を読まなければ理解できない詳細説明を INDEX.md エントリーに展開してはいけない",
                ),
                Requirement(
                    "禁止",
                    "関連しそうという理由だけで対象へ進ませるような広すぎる条件を書いてはいけない",
                ),
            ],
        ),
        Standard(
            title="INDEX.md エントリーは対象内容に根拠を持つ",
            backgrounds=[
                "INDEX.md は対象ファイル・ディレクトリの現在内容から生成される",
                "対象外の責務まで書くと、AI agent が不要なファイルを読む原因になる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "対象内容から根拠を持って言える責務・入口・読む条件だけを書く",
                ),
                Requirement(
                    "禁止",
                    "推測で対象外の責務や将来の用途を広げてはいけない",
                ),
                Requirement(
                    "必須",
                    "対象を読まなくてよい境界や、より直接読むべき別対象がある場合の境界を書く",
                ),
            ],
        ),
        Standard(
            title="機械的に補える情報を INDEX.md エントリーの意味情報に混ぜない",
            backgrounds=[
                "ファイル・ディレクトリの識別子、ハッシュ、出力形式は、この agent call の外側の仕組みで補われる",
                "機械的に分かる情報を自然言語へ混ぜるほど、ルーティング判断に必要な意味情報が薄まる",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "ファイル名・ディレクトリ名・ハッシュ値のような機械的に補える情報を書いてはいけない",
                ),
                Requirement(
                    "禁止",
                    "Structured Output schema を読めば分かる出力項目名・型・形式を説明してはいけない",
                ),
                Requirement(
                    "必須",
                    "機械的な識別情報ではなく、対象を読むべきか判断するための意味情報だけを書く",
                ),
            ],
        ),
    ]
    return (
        {},
        StructDoc(
            "index entry standard",
            *[standard_to_struct_doc(ies) for ies in standards],
        ),
    )
