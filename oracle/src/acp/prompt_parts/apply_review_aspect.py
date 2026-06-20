# cmoc
from basic.struct_doc import StructDoc
from basic.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)


def build_apply_review_aspect() -> StructDoc:
    """
    oracle file の内容を realization file に適用する際に発生する「所見（要修正点）を列挙する作業」のレビュー観点を構築する
    """
    standards = [
        Standard(
            title="oracle file と realization file の明確な不整合を要修正点として扱う",
            targets=[
                "oracle file",
                "realization file",
                "要修正点",
            ],
            backgrounds=[
                "realization file は oracle file で述べられた人間意図を具体化したものである",
                "oracle file 上で記述されている仕様と realization file が矛盾している場合、その realization file は正本仕様断片を満たしていない",
                "cmoc apply fork の監査・整理・修正では、実装を oracle file に合わせる必要がある",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "oracle file 上で記述されている仕様と realization file が明確に不整合している点を要修正点として扱う",
                ),
                Requirement(
                    "必須",
                    "要修正点は、どの oracle file のどの仕様と、どの realization file のどの実装が不整合しているかを根拠にする",
                ),
                Requirement(
                    "禁止",
                    "oracle file を根拠にせず、実装だけから正本仕様を推測して不整合を作ってはいけない",
                ),
                Requirement(
                    "許容",
                    "仕様文言から推測可能な意図と realization file が著しく乖離する場合は、要修正点として扱ってよい",
                ),
            ],
            criteria=[
                "oracle file の具体的な記述を根拠にしている",
                "realization file がその記述に反していることを説明できる",
                "実装上の選好ではなく、正本仕様断片との不整合として説明できる",
            ],
            examples=[
                "OK: oracle file が read-only を要求している処理で、realization file が対象ファイルを書き換えている",
                "OK: oracle file が `<work-root>/oracle` を編集禁止としているのに、realization file がその配下を更新する",
                "NG: oracle file に規定がない内部関数名が好みと違うという理由だけで要修正点にする",
            ],
        ),
        Standard(
            title="oracle file の仕様断片の隙間だけを根拠に要修正点を作ってはいけない",
            targets=[
                "oracle file",
                "realization file",
                "要修正点",
            ],
            backgrounds=[
                "oracle file は正本仕様断片であり、仕様全体を網羅するものではない",
                "oracle file に明記されていない仕様の隙間は、実装者である AI の裁量で補われる",
                "仕様の隙間を過剰に問題扱いすると、人間があえて疎に保っている oracle file の意図と衝突する",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "oracle file に明記されていないという理由だけで、realization file の挙動を要修正点として扱ってはいけない",
                ),
                Requirement(
                    "必須",
                    "仕様の隙間にある実装差は、oracle file・既存 realization file・既存 test から自然に導ける範囲なら許容する",
                ),
                Requirement(
                    "禁止",
                    "一般的なベストプラクティスや好みを、oracle file の未定義部分を埋める正本仕様として扱ってはいけない",
                ),
                Requirement(
                    "許容",
                    "仕様の隙間にある実装でも、仕様文言から推測可能な意図と著しく乖離する場合は要修正点として扱ってよい",
                ),
            ],
            criteria=[
                "要修正点が、単なる未定義部分の存在だけを根拠にしていない",
                "AI 裁量で補える範囲の実装差を不整合扱いしていない",
                "ベストプラクティスや好みよりも oracle file の記述を優先している",
            ],
            examples=[
                "OK: oracle file が出力形式を明示しているのに、realization file が別形式を出力している",
                "NG: oracle file が内部 helper の分割を指定していないのに、分割方法が好みと違うだけで要修正点にする",
                "NG: 一般的には設定項目化できる挙動だという理由だけで、oracle file にない CLI option の不足を要修正点にする",
            ],
        ),
        Standard(
            title="realization file だけから見た明確な致命的問題を要修正点として扱う",
            targets=[
                "realization file",
                "realization code",
                "要修正点",
            ],
            backgrounds=[
                "realization file には、oracle file との不整合ではなく、実装成果物の品質として発生する問題がある",
                "cmoc apply fork は oracle file の適用だけでなく、適用後の realization file を動作可能な成果物に近づける役割を持つ",
                "単なるクオリティアップ提案まで要修正点に含めると、修正対象が肥大化する",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "realization file だけから見てもバグ級である明確な致命的問題を要修正点として扱う",
                ),
                Requirement(
                    "禁止",
                    "こうした方が良いというクオリティアップ的な話を要修正点として扱ってはいけない",
                ),
                Requirement(
                    "禁止",
                    "可読性・命名・分割・抽象化への好みだけを根拠に要修正点を作ってはいけない",
                ),
                Requirement(
                    "必須",
                    "realization file の致命的問題を修正する場合も、修正後の実装は oracle file 上で記述されている仕様を満たしていなければならない",
                ),
            ],
            criteria=[
                "実行不能、明確な例外、明確なデータ破壊、明確な契約違反など、バグ級の問題として説明できる",
                "単なる改善提案や設計上の好みではない",
                "修正方針が oracle file と矛盾していない",
            ],
            examples=[
                "OK: import 漏れにより対象サブコマンドが起動直後に失敗する",
                "OK: パス解決の誤りにより、許可されていないツリーを書き換える可能性がある",
                "NG: もっと短く書ける、または別名の helper にした方が読みやすいという理由だけで要修正点にする",
                "NG: 現行仕様を満たしている処理を、一般論としてより美しい設計に置き換えるためだけに要修正点にする",
            ],
        ),
    ]
    return StructDoc(
        "apply review aspect",
        *[standard_to_struct_doc(ars) for ars in standards],
    )
