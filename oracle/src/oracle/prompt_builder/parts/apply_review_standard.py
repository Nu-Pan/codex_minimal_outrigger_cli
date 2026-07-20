# cmoc
from oracle.other.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_apply_review_standard() -> tuple[PlaceholderMap, StructDoc]:
    """
    oracle file の内容を realization file に適用する際に発生する「所見を列挙する作業」の規範文章を構築する
    """
    standards = [
        Standard(
            title="oracle file と realization file の明確な不整合を所見として扱う",
            backgrounds=[
                "realization file は oracle file で述べられた人間意図を具体化したものである",
                "oracle file 上で記述されている仕様と realization file が矛盾している場合、その realization file は正本仕様断片を満たしていない",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "oracle file 上で記述されている仕様と realization file が明確に不整合している点を所見として扱う",
                ),
                Requirement(
                    "必須",
                    "所見は、どの oracle file のどの仕様と、どの realization file のどの実装が不整合しているかを根拠にする",
                ),
                Requirement(
                    "禁止",
                    "oracle file を根拠にせずに realization file だけから正本仕様を推測してはいけない",
                ),
            ],
        ),
        Standard(
            title="oracle file の仕様断片の隙間だけを根拠に所見を作ってはいけない",
            backgrounds=[
                "oracle file は正本仕様断片であり、仕様全体を網羅するものではない",
                "oracle file に明記されていない仕様の隙間は、実装者である AI agent の裁量で補われる",
                "人間の認知コストの負担を小さくするために、oracle file は可能な限り疎に保たなければいけない",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "単に oracle file に明記されていないという理由だけで、realization file の挙動を所見として扱ってはいけない",
                ),
                Requirement(
                    "許容",
                    "仕様の隙間にある実装差は、oracle file, realization file から自然に導ける範囲内で許容される",
                ),
                Requirement(
                    "許容",
                    "oracle file で定義されていない部分は一般的なベストプラクティスに従って埋めてよい",
                ),
                Requirement(
                    "必須",
                    "一般的なベストプラクティスよりも oracle file の正本仕様断片を優先すること",
                ),
                Requirement(
                    "禁止",
                    "oracle file で定義されていないが realization file 上に存在する要素は正本仕様として扱ってはいけない",
                ),
                Requirement(
                    "許容",
                    "oracle file から推測可能な意図と realization file とが著しく乖離する場合は所見として扱ってよい",
                ),
                Requirement(
                    "許容",
                    "oracle file で定義されておらず、realization file 上に存在し、realization file に残す必要がないことが明確な要素は所見として扱ってよい",
                ),
            ],
            examples=[
                "一般的には設定項目化できる挙動でも、oracle file に選択可能にする要求がないなら CLI option の不足だけでは所見としない",
                "oracle file 上の `session home branch` が realization file 上で意味的に同じ `base branch` として実装されているなら、対応関係を示してリネーム候補の所見とする",
                "realization file 上に旧状態ファイルを読む処理が残っており、oracle file に対応仕様がなく現行実装からも必要性が読めないなら、過去仕様の残骸として所見とする",
            ],
        ),
        Standard(
            title="realization file だけから見た明確な致命的問題を所見として扱う",
            backgrounds=[
                "realization file には、oracle file との不整合ではなく、実装成果物の品質上の問題が発生している可能性がある",
                "realization file は oracle file との整合性を保ちつつ、正常動作可能な状態を保たなければいけない",
                "AI agent に解かせる問題の規模を小さく保つために realization file の肥大化を防がなければいけない",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "realization file だけから見て明らかにバグであるもの・致命的問題点は所見として扱う",
                ),
                Requirement(
                    "禁止",
                    "こうした方が良いというクオリティアップ的な話は所見としては扱わない",
                ),
                Requirement(
                    "必須",
                    "realization file の致命的問題を修正する場合も、修正後の実装は oracle file 上で記述されている仕様を満たしていなければならない",
                ),
            ],
            examples=[
                "現行仕様を満たして正常動作している処理は、helper 名を変えると読みやすいという程度では所見としない",
                "例外時に必ず未定義変数を参照する処理は、oracle file に直接書かれていなくても実行不能な致命的問題として所見にする",
            ],
        ),
    ]
    return (
        dict(),
        StructDoc(
            "apply review standard",
            *[standard_to_struct_doc(ars) for ars in standards],
        ),
    )
