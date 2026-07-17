# cmoc
from oracle.other.struct_doc import StructDoc
from oracle.other.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)
from oracle.prompt_builder.basic import PlaceholderMap


def build_review_oracle_standard() -> tuple[PlaceholderMap, StructDoc]:
    """
    `cmoc oracle review` における「所見を列挙する作業」の規範文章を構築する
    """
    standards = [
        Standard(
            title="致命的な問題を fatal 所見として扱う",
            backgrounds=[
                "oracle file は正本仕様断片である",
                "正本仕様断片同士が明確に矛盾している場合、実装者である AI は一貫した実装を導けない",
                "仕様に従った実装時に実装者の裁量では解消不能な問題が発生する場合、人間判断が必要になる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "仕様断片同士に明確な矛盾がある場合は fatal 所見として扱う",
                ),
                Requirement(
                    "必須",
                    "仕様に従って実装した時に実装者の裁量では解消不能な問題が発生する場合は fatal 所見として扱う",
                ),
                Requirement(
                    "禁止",
                    "実装者の裁量で自然に補える仕様の隙間を fatal 所見として扱ってはいけない",
                ),
                Requirement(
                    "必須",
                    "fatal 所見は、一方の仕様断片に従うと別の仕様断片に必ず違反することを根拠にする",
                ),
                Requirement(
                    "必須",
                    "fatal 所見は、実装者が選択できる妥当な実装方針が残っていないことを根拠にする",
                ),
                Requirement(
                    "禁止",
                    "好みや一般的なベストプラクティスを fatal 所見の根拠にしてはいけない",
                ),
            ],
            examples=[
                "必須の出力 JSON schema と必須の保存 schema が同じ field に両立しない型を要求しているなら fatal 所見にする",
                "内部 helper の分割方法が未指定でも、既存仕様と実装から自然に選べるなら fatal 所見にしない",
            ],
        ),
        Standard(
            title="単純な問題を minor 所見として扱う",
            backgrounds=[
                "oracle file は人間が読む正本仕様断片である",
                "日本語的な誤りや typo は、仕様理解と検索の安定性を下げる",
                "用語の不統一や表記揺れは、同じ概念を別概念として誤読させる原因になる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "日本語的な誤りは minor 所見として扱う",
                ),
                Requirement(
                    "必須",
                    "誤字、脱字、助詞の抜けは minor 所見として扱う",
                ),
                Requirement(
                    "必須",
                    "用語の不統一、表記揺れ、typo は minor 所見として扱う",
                ),
                Requirement(
                    "許容",
                    "その他ケアレスミスの疑いが濃厚なものは minor 所見として扱ってよい",
                ),
                Requirement(
                    "必須",
                    "minor 所見は、文意や検索性を損なう単純な誤りであることを根拠にする",
                ),
                Requirement(
                    "必須",
                    "minor 所見は、正本仕様の内容を変える提案ではなく表記上の問題として説明できなければならない",
                ),
                Requirement(
                    "禁止",
                    "正しいが好みではない言い回しを minor 所見として扱ってはいけない",
                ),
            ],
            examples=[
                "`oracle file` と `oracles file` が同じ概念として混在している場合は、表記揺れとして minor 所見にする",
                "`A B に渡す` のように助詞抜けで渡す主体が読み取りにくい場合は、文意を変えない修正として minor 所見にする",
                "文法的に正しく検索性も損なわない言い回しは、より好みの表現があっても minor 所見にしない",
            ],
        ),
        Standard(
            title="oracle file だけから問題と言い切れないものは所見にしない",
            backgrounds=[
                "oracle file は正本仕様断片であり、仕様全体を網羅するものではない",
                "oracle file に書かれていない仕様の隙間は、実装者である AI の裁量で補われる",
                "`cmoc oracle review` は、リポジトリ固有の事情に依存しない汎用的なレビュー観点で oracle file を評価する",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "oracle file だけからは問題だとは言い切れないものを所見として扱ってはいけない",
                ),
                Requirement(
                    "禁止",
                    "仕様からは実装が一意に定まらないというだけで所見を作ってはいけない",
                ),
                Requirement(
                    "禁止",
                    "推測、好み、一般的なベストプラクティスだけを根拠に所見を作ってはいけない",
                ),
                Requirement(
                    "必須",
                    "所見は oracle file の具体的な記述に基づいて説明できなければならない",
                ),
                Requirement(
                    "必須",
                    "所見は oracle file の記述だけから問題であることを説明できなければならない",
                ),
                Requirement(
                    "禁止",
                    "仕様の隙間を実装者が自然に補える余地を問題扱いしてはいけない",
                ),
                Requirement(
                    "禁止",
                    "実装方針が複数あり得るだけの状態を所見として扱ってはいけない",
                ),
            ],
            examples=[
                "同じ用語が同一ファイル内で保存先と branch 名の両方を指しており文脈だけでは区別できない場合は、oracle file の記述に基づく問題として扱ってよい",
                "oracle file が実装手順を指定していなくても、実装者が既存実装に合わせて自然に選べるなら所見にしない",
                "一般論としてエラー例をもっと詳しく書けるだけで、現在の仕様理解に矛盾や単純誤りがないなら所見にしない",
            ],
        ),
    ]
    return (
        {},
        StructDoc(
            "review oracle standard",
            *[standard_to_struct_doc(ros) for ros in standards],
        ),
    )
