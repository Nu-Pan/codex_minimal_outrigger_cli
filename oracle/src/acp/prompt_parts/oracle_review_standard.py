from basic.struct_doc import StructDoc
from basic.standard import Requirement, Standard, standard_to_struct_doc


def build_review_oracle_standard() -> StructDoc:
    """
    `cmoc review oracle` におけるレビュー作業が従うべき規範を構築する。
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
            ],
            criteria=[
                "一方の仕様断片に従うと、別の仕様断片に必ず違反することを説明できる",
                "実装者が選択できる妥当な実装方針が残っていないことを説明できる",
                "好みや一般的なベストプラクティスではなく、oracle file の具体的な記述を根拠にしている",
            ],
            examples=[
                "OK: 同じ条件について、ある oracle file は必ず実行すると書き、別の oracle file は実行してはいけないと書いている",
                "OK: 必須の出力形式と必須の保存形式が同時に満たせない形で定義されている",
                "NG: oracle file が内部 helper の分割方法を指定していないことを fatal 所見にする",
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
            ],
            criteria=[
                "文意や検索性を損なう単純な誤りとして説明できる",
                "同じ概念が複数の表記で現れていることを説明できる",
                "正本仕様の内容を変える提案ではなく、表記上の問題として説明できる",
            ],
            examples=[
                "OK: 同じ概念が `oracle file` と `oracles file` の両方で書かれている",
                "OK: 助詞の抜けにより係り受けが読み取りにくい",
                "NG: 正しいが好みではない言い回しを minor 所見にする",
            ],
        ),
        Standard(
            title="oracle file だけから問題と言い切れないものは所見にしない",
            backgrounds=[
                "oracle file は正本仕様断片であり、仕様全体を網羅するものではない",
                "oracle file に書かれていない仕様の隙間は、実装者である AI の裁量で補われる",
                "`cmoc review oracle` は、リポジトリ固有の事情に依存しない汎用的なレビュー観点で oracle file を評価する",
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
            ],
            criteria=[
                "oracle file の記述だけから問題であることを説明できる",
                "仕様の隙間を実装者が自然に補える余地を問題扱いしていない",
                "実装方針が複数あり得るだけの状態を所見にしていない",
            ],
            examples=[
                "OK: 同じ用語が同一ファイル内で異なる意味に使われている",
                "NG: oracle file が実装手順を指定していないという理由だけで所見にする",
                "NG: 一般論としてより詳しく書けるという理由だけで所見にする",
            ],
        ),
    ]
    return StructDoc(
        "review oracle standard",
        *[standard_to_struct_doc(standard) for standard in standards],
    )
