# std
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc
from basic.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)


def build_oracle_standard() -> StructDoc:
    """
    oracle file のレビュー観点を表す StructDocs を構築する。
    """
    standards = [
        Standard(
            title="人間の認知能力の消費は節約しなければならない",
            targets=["oracle file"],
            backgrounds=[
                "人間の認知能力は人間だけが提供できる希少なリソースである",
                "希少性ゆえに、あらゆるケースで人間の認知能力の供給不足がボトルネックになる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "oracle file の記述・構成・量は、人間の認知能力の消費を節約する方向で決める",
                ),
                Requirement(
                    "推奨",
                    "人間の認知能力の投入量あたりの成果量を最大化する",
                ),
                Requirement(
                    "推奨",
                    "人間が少ない判断で大きな実装成果を得られるように、oracle file のレバレッジを高める",
                ),
            ],
            criteria=[
                "人間が読み直すべき文脈量が不要に増えていない",
                "人間が判断すべき事項と AI に任せてよい事項の境界が読み取れる",
            ],
            examples=[
                "OK: 人間判断が必要な境界条件だけを oracle file に書き、細部の実装選択は AI に任せる",
                "NG: 人間判断が不要な実装手順を網羅的に列挙する",
            ],
        ),
        Standard(
            title="oracle file は正本仕様断片である",
            targets=["oracle file"],
            backgrounds=[
                "oracle file は人間が 100% 責任を持つ",
                "oracle file の規模は人間のメンテナンスコストに影響する",
                "人間の認知負荷を下げるためには、oracle file の規模を小さく保つ必要がある",
            ],
            requirements=[
                Requirement("必須", "oracle file を正本仕様の断片として扱う"),
                Requirement("推奨", "正本仕様断片が疎な状態を目指す"),
                Requirement(
                    "禁止",
                    "正本仕様を網羅的に記述すること自体を目的として oracle file を書いてはいけない",
                ),
            ],
            criteria=[
                "oracle file が、実装差を避けたい重要事項を中心に書かれている",
                "仕様全体を埋め尽くすためだけの分類・列挙・説明が増えていない",
            ],
            examples=[
                "OK: 実装差が出ると困る入出力契約だけを正本仕様断片として書く",
                "NG: 必要性の薄い文言を過剰にカテゴリ分けして網羅的に記述する",
            ],
        ),
        Standard(
            title="仕様断片の隙間の未定義部分は許容する",
            targets=["oracle file"],
            backgrounds=[
                "oracle file は正本仕様断片である",
                "仕様断片の隙間には未定義部分が生まれる",
                "未定義部分は、実装者である AI による実装差が生まれる原因となる",
            ],
            requirements=[
                Requirement(
                    "許容",
                    "oracle file 上に未定義部分が存在することを許容する",
                ),
                Requirement(
                    "必須",
                    "oracle file 上に未定義部分が存在する場合、それは人間があえて是認しているものとみなす",
                ),
                Requirement(
                    "必須",
                    "実装差が許されない事項は、人間の責任で oracle file に明示する",
                ),
                Requirement(
                    "許容",
                    "実装者である AI は、「正本仕様断片」「現在の既存実装・既存テスト」から妥当な新実装・テストを導き出してよい",
                ),
                Requirement(
                    "推奨",
                    "実装者である AI の裁量で補う仕様の規模は小さく保つ",
                ),
            ],
            criteria=[
                "実装差が許されない事項が oracle file に明示されている",
                "AI 裁量で補われる部分が、現行の正本仕様断片と既存実装・既存テストから自然に導ける範囲に収まっている",
                "未定義部分を埋めるためだけの過剰な仕様記述が追加されていない",
            ],
            examples=[
                "OK: エラー終了すべき条件だけを明示し、内部実装の関数分割は AI の裁量に任せる",
                "NG: 実装差が許されない出力形式を oracle file に書かず、既存実装から推測させる",
            ],
        ),
        Standard(
            title="oracle file の総文字数の最小化を目標とする",
            targets=["oracle file"],
            backgrounds=[
                "oracle file の規模が大きいほど、人間の認知負荷が増える",
                "oracle file の規模が大きいほど、AI が読む文脈量も増える",
            ],
            requirements=[
                Requirement(
                    "推奨",
                    "必ず守らなければならない要件を満たしている範囲内で、oracle file 全体の総文字数が最小となることを目指す",
                ),
                Requirement(
                    "推奨",
                    "複数箇所で同じ内容を述べる必要がある場合は、1 箇所にまとめたうえで参照する",
                ),
                Requirement(
                    "禁止",
                    "文字数削減のために意味が曖昧になる省略をしてはいけない",
                ),
            ],
            criteria=[
                "同じ意味の記述が複数箇所に重複していない",
                "冗長な言い回しが残っていない",
                "助詞や接続関係の省略により解釈が不安定になっていない",
            ],
            examples=[
                "OK: 複数箇所で同じ説明を書く代わりに、1 箇所にまとめて参照する",
                "NG: 文字数を減らすために助詞を削り、文の係り受けを曖昧にする",
            ],
        ),
        Standard(
            title="正本仕様断片の間で論理的な矛盾はあってはいけない",
            targets=[
                "oracle file",
                "正本仕様断片",
            ],
            backgrounds=[
                "実装は正本仕様断片と矛盾してはいけない",
                "正本仕様断片が矛盾している場合、実装も矛盾する",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "正本仕様断片の間に、解釈の余地のない明確な論理的矛盾があってはいけない",
                ),
                Requirement(
                    "必須",
                    "基本原則と具体的な詳細仕様は論理的に整合していなければならない",
                ),
            ],
            criteria=[
                "ある正本仕様断片に従うと、別の正本仕様断片に必ず違反する状態になっていない",
                "一般的な方針と個別仕様の優先関係が読み取れる",
            ],
            examples=[
                "OK: 基本原則と具体的な詳細仕様が同じ結論を導く",
                "NG: ある仕様では「必ず実行する」と書き、別の仕様では同じ条件で「実行してはいけない」と書く",
            ],
        ),
        Standard(
            title="実装から仕様への逆流は原則として認めない",
            targets=[
                "oracle file",
                "oracle file の作成・修正提案",
            ],
            backgrounds=[
                "oracle file に記述された正本仕様断片を元に実装が生成される",
                "人間の意図が正確に直接反映されているのは oracle file である",
                "実装には、AI の裁量・過去の都合・偶然の挙動が含まれ得る",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "oracle file を調査せずに、実装だけから正本仕様を導き出してはいけない",
                ),
                Requirement(
                    "禁止",
                    "実装から導き出された仕様を、正本仕様としてそのまま oracle file に反映してはいけない",
                ),
                Requirement(
                    "許容",
                    "実装不可能な正本仕様の調査を目的とする場合のみ、実装から見える制約や矛盾を oracle file の修正提案材料として扱ってよい",
                ),
            ],
            criteria=[
                "oracle file の変更提案が、既存実装の都合だけを根拠にしていない",
                "実装から見える制約を扱う場合、それが正本仕様の問題調査として位置づけられている",
            ],
            examples=[
                "OK: oracle file と既存実装が矛盾している箇所を見つけ、人間判断が必要な修正候補として提示する",
                "NG: 既存実装がそうなっているという理由だけで、oracle file に同じ挙動を正本仕様として追記する",
            ],
        ),
        Standard(
            title="用語・表記は統一されていなければならない",
            targets=[
                "oracle file",
                "oracle file 内の用語・表記",
            ],
            backgrounds=[
                "読むべきファイルを特定する方法として、キーワード検索は重要な手がかりである",
                "同じ概念に複数の表記があると、人間と AI の検索・読解が不安定になる",
            ],
            requirements=[
                Requirement("必須", "同じ概念を指す表記揺れは統一する"),
                Requirement("推奨", "複数回登場する概念には専用の名前を割り当てる"),
                Requirement("必須", "typo は修正する"),
            ],
            criteria=[
                "同じ概念が複数の名前で呼ばれていない",
                "キーワード検索で関連する正本仕様断片を見つけられる",
                "typo により別概念のように見える表記が残っていない",
            ],
            examples=[
                "OK: 同じ概念を常に `oracle file` と表記する",
                "NG: 同じ概念を `oracle file`, `oracles file`, `oracle files`, `oracles files` と揺らして書く",
                "NG: 同じ概念を `oracle file`, `oracle spec`, `仕様ファイル` と揺らして書く",
            ],
        ),
        Standard(
            title="命名は適切でなければいけない",
            targets=[
                "oracle file",
                "oracle file 内で定義・使用される名前",
            ],
            backgrounds=[
                "AI は命名から実態を推測しやすい",
                "名前と実態が乖離していると、人間意図と実装が乖離しやすい",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "名前から推測される説明と、oracle file から読み取れる実際上の説明は整合していなければならない",
                ),
                Requirement(
                    "禁止",
                    "実態と異なる推測を強く誘発する名前を使ってはいけない",
                ),
            ],
            criteria=[
                "名前だけを見たときの自然な解釈が、oracle file 上の定義と矛盾していない",
                "既存用語との関係が読み取りにくい名前になっていない",
            ],
            examples=[
                "OK: 一時実行用の branch に、永続 branch と誤解されない名前を付ける",
                "NG: 削除される一時ファイルに `permanent` を含む名前を付ける",
            ],
        ),
        Standard(
            title="ベストプラクティスよりも oracle file で定義されている要求が優先される",
            targets=[
                "oracle file",
                "oracle file の解釈",
                "cmoc による oracle file 支援機能",
            ],
            backgrounds=[
                "一般的に良しとされていることが cmoc でも良しとされるとは限らない",
                "cmoc は oracle file を正本仕様断片として扱う",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "一般的に知られているベストプラクティスと oracle file の要求が競合した場合は、oracle file を優先する",
                ),
                Requirement(
                    "必須",
                    "一般的に知られているベストプラクティスを理由に、oracle file の要求を無視してはいけない",
                ),
            ],
            criteria=[
                "判断の根拠が、一般論ではなく oracle file と正本仕様断片に置かれている",
                "ベストプラクティスを採用する場合でも、oracle file と矛盾していない",
            ],
            examples=[
                "OK: 一般には網羅的な仕様書が望ましい場面でも、oracle file が疎な正本仕様断片を求めるなら疎に保つ",
                "NG: 一般的なドキュメントベストプラクティスを理由に、oracle file を網羅的に書き直す",
            ],
        ),
        Standard(
            title="仕様断片として goal だけではなく non-goal も書くことが望ましい",
            targets=[
                "oracle file",
                "正本仕様断片",
            ],
            backgrounds=[
                "実装者である AI が正本仕様断片を解釈するうえで、「そうである」と「そうではない」の境界は重要である",
                "non-goal がない場合、AI が人間意図を越えて仕様を広げることがある",
            ],
            requirements=[
                Requirement("推奨", "可能な限り、goal と対になる non-goal を記述する"),
                Requirement("許容", "goal だけの記述も許容する"),
            ],
            criteria=[
                "実装者である AI が、実装すべきことと実装しなくてよいことの境界を読み取れる",
                "non-goal を書かない場合でも、過剰な実装を誘発しにくい記述になっている",
            ],
            examples=[
                "OK: `cmoc review oracle` が検出する対象と、検出しない対象を対で書く",
                "NG: 目的だけを書き、明らかに対象外にしたい処理まで AI が追加し得る状態にする",
            ],
        ),
    ]
    return StructDoc(
        "oracle standard",
        *[standard_to_struct_doc(os) for os in standards],
    )
