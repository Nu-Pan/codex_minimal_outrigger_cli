# cmoc
from oracle.other.struct_doc import StructDoc
from oracle.other.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_standard() -> tuple[PlaceholderMap, StructDoc]:
    """
    oracle file が従うべき規範文章を構築する
    """
    standards = [
        Standard(
            title="人間の認知能力の消費は節約しなければならない",
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
                Requirement(
                    "禁止",
                    "人間が読み直すべき文脈量を不要に増やしてはいけない",
                ),
                Requirement(
                    "必須",
                    "人間が判断すべき事項と AI に任せてよい事項の境界が読み取れるようにする",
                ),
            ],
            examples=[
                "出力互換性の境界は人間判断が必要なので oracle file に書くが、内部 helper の分割は AI が既存実装に合わせて決めてよい",
                "例外処理の要否だけが人間意図なら、try 文の配置や関数呼び出し順まで oracle file に列挙しない",
            ],
        ),
        Standard(
            title="oracle file は正本仕様断片である",
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
                Requirement(
                    "必須",
                    "oracle file は、実装差を避けたい重要事項を中心に書く",
                ),
                Requirement(
                    "禁止",
                    "仕様全体を埋め尽くすためだけの分類・列挙・説明を増やしてはいけない",
                ),
            ],
            examples=[
                "CLI 出力の JSON key は実装差を避けたいので正本仕様断片として書き、内部 dict の組み立て順は書かない",
                "現在の機能に影響しない将来サブコマンドの分類表は、仕様全体を埋めるだけなら追加しない",
            ],
        ),
        Standard(
            title="仕様断片の隙間の未定義部分は許容する",
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
                Requirement(
                    "必須",
                    "実装差が許されない事項は oracle file に明示されていなければならない",
                ),
                Requirement(
                    "必須",
                    "AI 裁量で補われる部分は、現行の正本仕様断片と既存実装・既存テストから自然に導ける範囲に収める",
                ),
                Requirement(
                    "禁止",
                    "未定義部分を埋めるためだけの過剰な仕様記述を追加してはいけない",
                ),
            ],
            examples=[
                "エラー終了すべき条件は明示し、エラー判定を専用関数にするか呼び出し元に置くかは既存実装に合わせてよい",
                "利用者が読む出力形式を固定したい場合は oracle file に書き、既存実装の現在値だけを根拠にしない",
            ],
        ),
        Standard(
            title="oracle file は必要な判断情報を保ったまま読むべき文脈量を抑える",
            backgrounds=[
                "oracle file の規模が大きいほど、人間の認知負荷が増える",
                "oracle file の規模が大きいほど、AI が読む文脈量も増える",
            ],
            requirements=[
                Requirement(
                    "推奨",
                    "必ず守らなければならない要件を満たしている範囲内で、oracle file の読むべき文脈量を小さく保つ",
                ),
                Requirement(
                    "推奨",
                    "複数箇所で同じ内容を述べる必要がある場合は、1 箇所にまとめたうえで参照する",
                ),
                Requirement(
                    "禁止",
                    "文字数削減のために意味が曖昧になる省略をしてはいけない",
                ),
                Requirement(
                    "禁止",
                    "同じ意味の記述を複数箇所に重複させてはいけない",
                ),
                Requirement(
                    "禁止",
                    "冗長な言い回しを残してはいけない",
                ),
                Requirement(
                    "禁止",
                    "助詞や接続関係の省略により解釈が不安定になる書き方をしてはいけない",
                ),
                Requirement(
                    "禁止",
                    "oracle file の簡潔性要求を、調査根拠・検証結果・重大な留保を省く理由にしてはいけない",
                ),
            ],
            examples=[
                "`<work-root>` の定義を複数文書で使う場合は、定義を 1 箇所に置き、他の箇所ではその語だけを使う",
                "`A を B に渡す` と `A が B に渡る` で責務が変わる箇所では、短縮より係り受けの明確さを優先する",
            ],
        ),
        Standard(
            title="正本仕様断片の間で論理的な矛盾はあってはいけない",
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
                Requirement(
                    "禁止",
                    "ある正本仕様断片に従うと別の正本仕様断片に必ず違反する状態を作ってはいけない",
                ),
                Requirement(
                    "必須",
                    "一般的な方針と個別仕様の優先関係が読み取れるようにする",
                ),
            ],
            examples=[
                "一般方針で `INDEX.md` を自動生成対象とし、個別仕様で同じ `INDEX.md` を手編集必須として扱うなら矛盾として直す",
                "原則は read-only、例外条件では write 可のように優先関係が読める場合は、単なる文言差だけでは矛盾扱いしない",
            ],
        ),
        Standard(
            title="実装から仕様への逆流は原則として認めない",
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
                Requirement(
                    "禁止",
                    "oracle file の変更提案は、既存実装の都合だけを根拠にしてはいけない",
                ),
                Requirement(
                    "必須",
                    "実装から見える制約を扱う場合は、それを正本仕様の問題調査として位置づける",
                ),
            ],
            examples=[
                "oracle file が保存禁止としているファイルを既存実装が保存している場合、実装制約の調査材料として人間判断に回す",
                "既存実装がたまたま空文字を許容しているだけなら、その挙動を正本仕様として oracle file に追記しない",
            ],
        ),
        Standard(
            title="用語・表記は統一されていなければならない",
            backgrounds=[
                "読むべきファイルを特定する方法として、キーワード検索は重要な手がかりである",
                "同じ概念に複数の表記があると、人間と AI の検索・読解が不安定になる",
            ],
            requirements=[
                Requirement("必須", "同じ概念を指す表記揺れは統一する"),
                Requirement("推奨", "複数回登場する概念には専用の名前を割り当てる"),
                Requirement("必須", "typo は修正する"),
                Requirement(
                    "禁止",
                    "同じ概念を複数の名前で呼んではいけない",
                ),
                Requirement(
                    "必須",
                    "キーワード検索で関連する正本仕様断片を見つけられるようにする",
                ),
                Requirement(
                    "禁止",
                    "typo により別概念のように見える表記を残してはいけない",
                ),
            ],
            examples=[
                "`oracle file` を検索語にした時に関連箇所が見つかるよう、同じ概念を `oracle spec` や `仕様ファイル` に言い換えない",
                "`oracles file` のような typo が別概念に見える場合は、検索性を壊す表記として修正する",
            ],
        ),
        Standard(
            title="命名は適切でなければいけない",
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
                Requirement(
                    "必須",
                    "名前だけを見たときの自然な解釈が、oracle file 上の定義と矛盾しないようにする",
                ),
                Requirement(
                    "禁止",
                    "既存用語との関係が読み取りにくい名前にしてはいけない",
                ),
            ],
            examples=[
                "処理後に削除される branch には、永続的な保存場所と読める `home` や `permanent` を含めない",
                "設定値を検証するだけの関数を `load_config` と呼ぶと読み込みまで行うように見えるため、実態に合う名前にする",
            ],
        ),
        Standard(
            title="ベストプラクティスよりも oracle file で定義されている要求が優先される",
            backgrounds=[
                "一般的に良しとされていることが、このリポジトリ上での開発においても良しとされるとは限らない",
                "oracle file を正本仕様断片として扱う",
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
                Requirement(
                    "必須",
                    "判断の根拠は、一般論ではなく oracle file と正本仕様断片に置く",
                ),
                Requirement(
                    "必須",
                    "ベストプラクティスを採用する場合でも、oracle file と矛盾してはいけない",
                ),
            ],
            examples=[
                "一般論では詳細な API 仕様表が望ましくても、oracle file が実装差を避けたい点だけを求めているなら表を追加しない",
                "標準的な CLI 慣習と oracle file の出力形式が異なる場合は、慣習ではなく oracle file の出力形式を正とする",
            ],
        ),
        Standard(
            title="仕様断片として goal だけではなく non-goal も書くことが望ましい",
            backgrounds=[
                "実装者である AI が正本仕様断片を解釈するうえで、「そうである」と「そうではない」の境界は重要である",
                "non-goal がない場合、AI が人間意図を越えて仕様を広げることがある",
            ],
            requirements=[
                Requirement("推奨", "可能な限り、goal と対になる non-goal を記述する"),
                Requirement("許容", "goal だけの記述も許容する"),
                Requirement(
                    "必須",
                    "実装者である AI が、実装すべきことと実装しなくてよいことの境界を読み取れるようにする",
                ),
                Requirement(
                    "必須",
                    "non-goal を書かない場合でも、過剰な実装を誘発しにくい記述にする",
                ),
            ],
            examples=[
                "「typo は検出対象、設計改善提案は対象外」のように、境界が誤読されやすい場合は対で書く",
                "新しい補助ファイルを作る目的を書くなら、生成キャッシュを正本として管理しないことも併記する",
            ],
        ),
    ]
    return (
        {},
        StructDoc(
            "oracle standard",
            *[standard_to_struct_doc(os) for os in standards],
        ),
    )
