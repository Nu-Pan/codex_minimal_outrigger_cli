from utils.struct_docs import StructDocs
from .base import Requirement, Standard, standard_to_struct_docs


def build_realization_standards() -> StructDocs:
    """
    realization files の標準的な実装・保守観点を表す StructDocs を構築する。
    """
    standards = [
        Standard(
            title="realization files の総文字数の最小化を目標とする",
            targets=["realization files"],
            backgrounds=[
                "realization files の規模が大きいほど、実装担当者である AI に与える課題の難易度が上がる",
                "realization files の規模が大きいほど、トークン消費が増える",
            ],
            requirements=[
                Requirement(
                    "推奨",
                    "必ず守らなければならない要件を満たしている範囲内（解空間内）で、realization files 全体で見た時の総文字数が最小となること（文字数最小解）を目指す",
                ),
                Requirement(
                    "推奨",
                    "複数箇所で出現するよく似た処理は関数化し、それを各所で使い回す",
                ),
                Requirement(
                    "推奨",
                    "意味的に重複している実装は 1 つに集約する",
                ),
                Requirement(
                    "必須",
                    "現行の仕様と関係のない、過去の仕様に基づく実装は削除する",
                ),
            ],
            criteria=[
                "同じ意味・同じ責務の実装が複数箇所に重複していない",
                "現行仕様では使われない旧仕様向け実装・テスト・コメントが残っていない",
                "文字数削減のために可読性や意味の明確さが損なわれていない",
            ],
            examples=[
                "OK: 複数箇所で出現する同じ path 正規化処理を 1 つの helper に集約する",
                "OK: 仕様変更により使われなくなった旧分岐と対応テストを削除する",
                "NG: ほぼ同じ処理を別名の関数として複数箇所に残す",
                "NG: 文字数を減らすために、意味が読み取りにくい過度な短縮名を使う",
            ],
        ),
        Standard(
            title="realization files の高品質化は望ましいことである",
            targets=[
                "realization files",
                "realization code",
                "realization ancillary",
            ],
            backgrounds=[
                "realization files は cmoc により継続的にメンテナンスされる",
                "メンテナンスにかかるコストは、AI が読む文脈量や判断すべき分岐量の影響を受ける",
                "realization files の品質には、変更容易性・責務の明確さ・不要部分の少なさが含まれる",
            ],
            requirements=[
                Requirement(
                    "推奨",
                    "realization files は、現行仕様を満たすために必要な情報だけを持つ",
                ),
                Requirement(
                    "推奨",
                    "realization code は、責務・入力・出力・副作用が読み取りやすい単位に分割する",
                ),
                Requirement(
                    "禁止",
                    "読み取りやすさを損なう過度な圧縮をしてはいけない",
                ),
                Requirement(
                    "禁止",
                    "将来使うかもしれないだけの抽象化を追加してはいけない",
                ),
                Requirement(
                    "推奨",
                    "実装だけから読み取りにくい意図・制約・根拠は、コメントまたは docstring に書く",
                ),
                Requirement(
                    "禁止",
                    "シグネチャ・型名・実装から明らかな情報だけを、コメントや docstring で冗長に繰り返してはいけない",
                ),
                Requirement(
                    "必須",
                    "現行仕様・現行実装から不要になった realization files、関数、クラス、分岐、設定、テスト、コメントは削除する",
                ),
            ],
            criteria=[
                "各ファイル・関数・クラスの責務が読み取れる",
                "実装の意図や制約が、必要な範囲でコメントまたは docstring に残っている",
                "現行仕様に関係しない古い実装・コメント・補助ファイルが残っていない",
                "抽象化や分割により、読むべき文脈量が不要に増えていない",
            ],
            examples=[
                "OK: コードの意味的なブロックごとに、その実装でなければならない理由を短いコメントで補う",
                "OK: 仕様変更により使われなくなった互換分岐を削除する",
                "NG: 「将来別の形式にも対応するかもしれない」という理由だけで汎用 parser 層を追加する",
                "NG: シグネチャを見れば分かる引数名や戻り値型だけを docstring で長く説明する",
            ],
        ),
        Standard(
            title="realization code の追加は既存 realization code の整理と一体で行う",
            targets=[
                "realization code",
                "realization implementation",
                "realization test",
            ],
            backgrounds=[
                "コードベースの肥大化は、新しいファイル・関数・クラスを追加した時だけでなく、古い実装を残した時にも発生する",
                "既存実装の近くに同じ責務の実装が残ると、AI はどちらが正しいかを判断するために余計な文脈を読む必要がある",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "realization code を追加する前に、同じ責務または近い責務を持つ既存の realization code を確認する",
                ),
                Requirement(
                    "禁止",
                    "既存実装の修正・移動・置換で現行仕様を満たせる場合は、新しい実装を追加してはいけない",
                ),
                Requirement(
                    "必須",
                    "新しい実装を追加した場合は、置き換えられた古い実装、不要になった分岐、重複した定数、古いテストも同時に削除または統合する",
                ),
                Requirement(
                    "禁止",
                    "一時的な移行コード・互換コードは、現行仕様から明示的に必要な場合以外は残してはいけない",
                ),
                Requirement(
                    "必須",
                    "移行コード・互換コードを残す場合は、それを削除できる条件を近くのコメントに書く",
                ),
            ],
            criteria=[
                "新旧の実装経路が同じ責務を持ったまま並存していない",
                "新しい実装に置き換えられた古いテスト・fixture・定数が残っていない",
                "移行コードや互換コードには、残す理由と削除条件が書かれている",
            ],
            examples=[
                "OK: 新しい parser を追加する時に、旧 parser を呼ぶ経路・旧 parser 専用テスト・旧 parser 専用 fixture も整理する",
                "OK: 既存関数に引数を 1 つ追加して現行仕様を満たす",
                "NG: 既存関数を少し変えれば足りる処理のために、ほぼ同じ関数を別名で作る",
                "NG: `legacy_` や `old_` を名前に含む実装を、現行仕様上の必要性が不明なまま残す",
            ],
        ),
        Standard(
            title="新しい抽象化は実在する重複または明確な責務境界に基づく",
            targets=[
                "realization code",
                "realization implementation",
                "realization test",
            ],
            backgrounds=[
                "抽象化はコード量を減らすこともある",
                "抽象化は呼び出し関係・引数・概念を増やしてコードベースを肥大化させることもある",
                "「将来使うかもしれない」抽象化は、現時点の AI の読解対象を増やす",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "新しい関数・クラス・モジュールは、現行仕様上の責務境界を明確にする場合、または実在する重複を削減する場合に作る",
                ),
                Requirement(
                    "禁止",
                    "単に処理が短いという理由だけで、1 箇所からしか呼ばれない小関数を増やしてはいけない",
                ),
                Requirement(
                    "必須",
                    "共通化は、見た目が似ているだけではなく、入力・出力・失敗時挙動・不変条件が同じ場合に行う",
                ),
                Requirement(
                    "禁止",
                    "呼び出し元ごとの差分を大量のフラグや callback で吸収する汎用関数を作ってはいけない",
                ),
                Requirement(
                    "推奨",
                    "共有範囲が 1 モジュール内に閉じる場合は、そのモジュール内の private helper に留める",
                ),
                Requirement(
                    "必須",
                    "共有モジュールへ移動するのは、複数のサブコマンドまたは複数の上位モジュールから使うことが明確な場合に限る",
                ),
            ],
            criteria=[
                "新しい抽象化が、実在する重複または明確な責務境界に対応している",
                "抽象化により、呼び出し側の理解に必要な引数・フラグ・callback が過度に増えていない",
                "共通化された処理の入力・出力・失敗時挙動・不変条件が揃っている",
                "共有モジュールに置かれた処理が、実際に複数箇所から使われる見込みを持っている",
            ],
            examples=[
                "OK: 同じ入力・同じ失敗時挙動を持つ path 変換処理を 1 つの helper にまとめる",
                "OK: 1 モジュール内でだけ使う補助処理を private helper として置く",
                "NG: 2 つの処理がどちらも git command を呼んでいるという理由だけで、失敗時の扱いが違う処理を 1 関数にまとめる",
                "NG: `do_everything(options: dict)` のような万能関数で差分を吸収する",
                "NG: 1 箇所からしか呼ばれず、名前を付けても意図が増えない 3 行の処理を無理に関数化する",
            ],
        ),
        Standard(
            title="公開面・設定面・状態の増加を抑制する",
            targets=[
                "realization implementation",
                "realization ancillary",
                "CLI 引数",
                "サブコマンド",
                "設定項目",
                "環境変数",
                "出力 schema",
                "永続状態",
            ],
            backgrounds=[
                "CLI 引数、サブコマンド、設定項目、環境変数、出力 schema、保存ファイルは、一度追加すると互換性維持の対象になりやすい",
                "公開面が増えると、実装・テスト・ドキュメント・利用者理解のすべてが増える",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "新しい CLI 引数、サブコマンド、設定項目、環境変数、出力項目、状態ファイルは、現行仕様を満たすために必要な場合だけ追加する",
                ),
                Requirement(
                    "禁止",
                    "内部実装の都合だけで公開面を増やしてはいけない",
                ),
                Requirement(
                    "推奨",
                    "単一の妥当な挙動を選べる場合は、設定項目で利用者に選ばせない",
                ),
                Requirement(
                    "必須",
                    "新しい永続状態を追加する場合は、その生成条件・更新条件・削除条件を仕様または実装上で明確にする",
                ),
                Requirement(
                    "禁止",
                    "同じ情報をログ・状態ファイル・出力 schema に重複して保存してはいけない",
                ),
            ],
            criteria=[
                "追加された公開面が、現行仕様上の必要性に対応している",
                "内部実装の都合だけで利用者向けの選択肢が増えていない",
                "永続状態のライフサイクルが読み取れる",
                "同じ情報が複数の保存先・出力先に重複していない",
            ],
            examples=[
                "OK: 現行仕様で利用者が選ぶ必要のある挙動だけを CLI option として追加する",
                "OK: 新しい状態ファイルを追加する時に、作成・更新・削除の条件も実装上明確にする",
                "NG: デバッグ用に一時的に欲しい値を、恒久的な CLI option として追加する",
                "NG: 計算で再現できる値を、別ファイルに永続化する",
                "NG: 仕様上 1 つの動作で十分な処理に `--mode` や `--strategy` を追加する",
            ],
        ),
        Standard(
            title="realization test の肥大化も抑制する",
            targets=[
                "realization test",
                "realization code",
            ],
            backgrounds=[
                "realization test も realization code の一部であり、読み取り・保守・更新の対象である",
                "テストが重複すると、仕様変更時に実装よりテスト修正のほうが大きくなる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "テストは、実装詳細ではなく、現行仕様上意味のある外部挙動または制御ロジックを検証する",
                ),
                Requirement(
                    "推奨",
                    "同じ観点のテストケースは、可能な範囲で parametrized test や小さな fixture に集約する",
                ),
                Requirement(
                    "必須",
                    "似たテストを追加する前に、既存テストへケース追加できないか確認する",
                ),
                Requirement(
                    "必須",
                    "古い仕様に対応するテスト、削除済み実装に対応するテスト、同じ失敗を重複して検出するテストは削除または統合する",
                ),
                Requirement(
                    "推奨",
                    "大きな fixture ファイルは、現行仕様の検証に必要な最小内容にする",
                ),
                Requirement(
                    "禁止",
                    "Codex CLI や LLM の出力品質そのものを検証するためのテストを追加してはいけない",
                ),
            ],
            criteria=[
                "テストが現行仕様上意味のある挙動または制御ロジックを検証している",
                "同じ観点のテストが複数のテスト関数に不要に分散していない",
                "削除済み実装や旧仕様に対応するテストが残っていない",
                "fixture が検証対象に対して過大になっていない",
            ],
            examples=[
                "OK: 同じ関数の入力値違いの正常系を 1 本の parametrized test にまとめる",
                "OK: 内部 helper の呼び出し順ではなく、仕様上の出力や副作用を検証する",
                "NG: 同じ失敗条件を複数のテストで重複して検出する",
                "NG: Codex CLI に依頼した仕事の出力品質を自動テストで検証する",
                "NG: 小さな入力で足りるテストのために巨大な fixture ファイルを追加する",
            ],
        ),
        Standard(
            title="依存関係・補助ファイル・生成物の増加を抑制する",
            targets=[
                "realization files",
                "realization implementation",
                "realization ancillary",
                "外部依存",
                "補助スクリプト",
                "テンプレート",
                "生成済みファイル",
            ],
            backgrounds=[
                "外部依存、補助スクリプト、テンプレート、生成済みファイルは、実装本体以外にもメンテナンス対象を増やす",
                "realization ancillary の増加は、AI が読むべき文脈と更新すべき対象を増やす",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "新しい外部依存は、標準ライブラリまたは既存依存で現行仕様を十分に満たせない場合だけ追加する",
                ),
                Requirement(
                    "推奨",
                    "外部依存を追加する場合は、それにより自前実装・テスト・保守負担がどれだけ減るかを重視する",
                ),
                Requirement(
                    "禁止",
                    "小さな処理のためだけに大きな依存を追加してはいけない",
                ),
                Requirement(
                    "禁止",
                    "生成可能なキャッシュ、実行ログ、一時ファイル、ビルド成果物を realization files として持ってはいけない",
                ),
                Requirement(
                    "必須",
                    "補助スクリプトを追加する場合は、既存の CLI・テスト・開発手順で代替できないか確認する",
                ),
            ],
            criteria=[
                "追加された外部依存に、標準ライブラリまたは既存依存では代替しにくい理由がある",
                "外部依存の追加により、総合的な実装・テスト・保守負担が減っている",
                "再生成可能なファイルが正本のように管理されていない",
                "補助スクリプトが既存の CLI・テスト・開発手順と重複していない",
            ],
            examples=[
                "OK: 標準ライブラリでは安全に実装しにくい処理のために、十分に小さく一般的な依存を追加する",
                "OK: テストで必要な小さな入力を、巨大な fixture ファイルではなくテスト内で組み立てる",
                "NG: 数行の path 操作のために外部パッケージを追加する",
                "NG: 実行すれば再生成できるファイルを、正本のようにコミットする",
                "NG: 既存のテストコマンドで足りる処理のために、別の補助スクリプトを追加する",
            ],
        ),
        Standard(
            title="realization files の変更完了時には削除・統合余地を確認する",
            targets=[
                "realization files",
                "realization code",
                "realization ancillary",
            ],
            backgrounds=[
                "肥大化は、実装中よりも実装完了時に見落とされやすい",
                "「追加して動いた」状態は、「最小で保守しやすい」状態とは限らない",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "realization files の変更完了前に、追加したもののうち削除・統合・短縮できるものがないか確認する",
                ),
                Requirement(
                    "禁止",
                    "未使用の関数、クラス、import、定数、fixture、補助ファイルを残してはいけない",
                ),
                Requirement(
                    "禁止",
                    "同じ責務を持つ名前違いの実装を残してはいけない",
                ),
                Requirement(
                    "禁止",
                    "現行仕様の説明に不要な TODO、NOTE、コメントを残してはいけない",
                ),
                Requirement(
                    "推奨",
                    "変更後の realization files は、現行仕様を満たすための最小構成にする",
                ),
            ],
            criteria=[
                "追加した実装・テスト・補助ファイルに、削除・統合・短縮できるものが残っていない",
                "未使用の import、定数、fixture、helper が残っていない",
                "同じ責務を持つ実装が名前違いで並存していない",
                "TODO、NOTE、コメントが現行仕様の理解に寄与している",
            ],
            examples=[
                "OK: 実装の途中で作った確認用 helper を、最終的に使わないなら削除する",
                "OK: 新しい共通関数へ移行した後、旧 helper の import とテストも削除する",
                "NG: 新実装への移行後に、呼ばれなくなった旧 helper と旧 helper 専用テストを残す",
                "NG: 仕様説明に寄与しない「念のため」コメントを残す",
            ],
        ),
    ]
    return StructDocs(
        "realization standards",
        *[standard_to_struct_docs(rs) for rs in standards],
    )
