# `apply_review_standard.py`

## Summary
- oracle file の内容を realization file に適用するレビューで、所見として扱うべき不整合・扱ってはいけない仕様断片の隙間・realization file 単体の致命的問題を定義する規範文書を構築する。
- 所見列挙時に oracle file を根拠にする境界、oracle file 未定義部分を理由に過剰な所見を作らない境界、実行不能な実装問題を所見に含める境界を確認する入口となる。

## Read this when
- oracle file と realization file の差分レビューで、何を所見として列挙すべきか判断したいとき。
- oracle file に明記されていない realization file の挙動を、所見に含めてよいか確認したいとき。
- oracle file との直接不整合ではないが、realization file 単体で明らかなバグや致命的問題を所見として扱う基準を確認したいとき。

## Do not read this when
- oracle file の内容を realization file へ実際に反映する実装修正手順やパッチ生成方法を確認したいとき。
- レビュー所見の出力 schema、CLI 入出力、またはプレースホルダ展開の仕組みを確認したいとき。
- oracle file や realization file の定義そのもの、または一般的な oracle 標準・realization 標準を確認したいとき。

## hash
- 65d7fa95504cb9bc06a0d024ca7d982b73ca5f845e6611f760e0fa13c4ed7433

# `file_access_rule.py`

## Summary
- AI エージェントに渡すファイル読み書き規則のプロンプト断片を、読み書きモードごとの deny list として組み立てる。
- 読み取り専用、oracle のみ参照・編集、リポジトリ編集、realization 編集などのモード差分を、プレースホルダ展開と構造化文書として返す責務を持つ。

## Read this when
- ファイルアクセス規則としてエージェントに提示される文面を変更したいとき。
- 読み書きモードごとに禁止される対象や、共通 deny ルールの扱いを確認したいとき。
- アクセス規則文書に埋め込む `<work-root>` プレースホルダや構造化文書の生成箇所を調べたいとき。

## Do not read this when
- 読み書きモードの列挙値そのものの定義を確認したいだけのとき。
- 実際のファイルシステム権限や sandbox 制御の実装を調べたいとき。
- 生成された完全なエージェントプロンプト全体の構成を確認したいとき。

## hash
- d97cb4699a40d624de847db6d3f2e7e59119b33e5da8b2c9d29cf67a2c802dd6

# `index_entry_standard.py`

## Summary
- INDEX.md エントリーを、対象本文へ進むべきか判断するためのルーティング情報として生成する規範文章を組み立てる。
- 対象内容に根拠を持つこと、読む条件と読まなくてよい境界を書くこと、機械的に補える識別情報や出力形式の説明を混ぜないことを標準化する。

## Read this when
- INDEX.md エントリーの作成・更新・評価に関する規範を確認したいとき。
- 対象本文を読む前に読むべき条件を判断できるルーティング文書の書き方を確認したいとき。
- エントリーに書いてよい意味情報と、書くべきでない機械的情報の境界を確認したいとき。

## Do not read this when
- oracle file や realization file 全般の責務境界を確認したいだけのとき。
- 特定ディレクトリ内の対象選択や既存エントリーの内容確認をしたいとき。
- StructDoc や Standard のデータ構造そのものの実装を調べたいとき。

## hash
- 5f8da15178f7c840797a82586fbfa750e0e43c1dfad56a32a5ec9355f591b037

# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の定義、役割、下位概念を構築するプロンプト部品。正本仕様断片と AI が編集する具体化ファイルの責務境界、配置場所、除外条件を説明する基本知識を扱う。

## Read this when
- oracle file と realization file の違い、所有者、編集責任、生成方向の境界を確認したいとき。
- oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary の位置づけを確認したいとき。
- プロンプト構築時に、正本仕様断片とその具体化ファイルに関する基本説明がどこで作られるかを確認したいとき。

## Do not read this when
- oracle file や realization file の品質基準、書き方、肥大化抑制などの詳細ルールを確認したいとき。
- 個別の CLI 挙動、テスト仕様、パスモデルの詳細、または StructDoc 自体の実装を確認したいとき。
- INDEX.md 用エントリーの生成規則やルーティング文書の書き方を確認したいとき。

## hash
- 58452b0f1e52b84af71900f085977504ccad9f29c858d2fd7a8a64d5ed7c58f9

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` で oracle file をレビューする際の所見列挙ルールを、構造化文書として組み立てる実装。fatal 所見、minor 所見、所見にしない条件を定義し、レビュー用プロンプト部品として利用される。

## Read this when
- oracle review の所見分類基準を確認したいとき。
- 明確な仕様矛盾や実装者裁量では解消できない問題を fatal と扱う条件を確認したいとき。
- 日本語上の誤り、typo、用語揺れなどを minor と扱う境界を確認したいとき。
- oracle file だけでは問題と言い切れない内容を所見から除外する基準を確認したいとき。

## Do not read this when
- oracle review の出力形式、CLI 引数、実行経路を確認したいとき。
- oracle file の一般的な品質基準や正本仕様断片としての扱いを確認したいとき。
- レビュー対象ファイルの探索、読み込み、git 管理対象判定の実装を確認したいとき。

## hash
- a83d32e646c0e234ec9b344c7fa0e9f23db19d26f6f6cd2967c613962abf93c3

# `oracle_standard.py`

## Summary
- oracle file が従うべき規範を Standard/Requirement の列として定義し、StructDoc の `oracle standard` として組み立てる prompt builder 部品。人間の認知負荷削減、正本仕様断片、未定義部分、文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語統一、命名、oracle 優先、goal/non-goal の境界を扱う。

## Read this when
- oracle standard の prompt 断片として、oracle file の記述方針や禁止事項がどの構造化文書に変換されるかを確認したいとき。
- oracle file の規範に関する Standard/Requirement/例示の追加・削除・文言変更が、StructDoc 生成にどう反映されるかを追うとき。
- prompt builder が返す PlaceholderMap と StructDoc のうち、oracle standard 部分の責務を確認したいとき。

## Do not read this when
- realization file、INDEX.md、ファイルアクセス規則など oracle standard 以外の規範を確認したいとき。
- StructDoc、Standard、Requirement、PlaceholderMap そのもののデータ構造や変換処理の実装を確認したいとき。
- CLI コマンド、永続状態、テスト実行など prompt 文書生成以外の挙動を調べたいとき。

## hash
- 79ba7326ddbddb60db66b8f2f933f29644dbd962fdc5dad23a17e7c3890e1ba2

# `realization_standard.py`

## Summary
- realization file、realization code、realization test、realization ancillary が従うべき規範文章を組み立てる。文字数最小化、不要実装削除、oracle src コピー禁止、コメント方針、ファイルサイズ、既存実装整理、抽象化、公開面、テスト肥大化、依存・補助ファイル・生成物、変更完了時の削除統合確認を扱う。
- 各規範は背景・要求・判断例からなる構造化文書へ変換され、prompt builder が利用する realization standard セクションの入力になる。

## Read this when
- realization file 全般の品質・最小化・不要部分削除に関する規範文を確認または変更したいとき。
- realization implementation、realization test、realization ancillary の追加・整理・削除に関する AI 向け標準を調整したいとき。
- oracle src の内容を realization src にコピーしない方針や、oracle file path をコメント根拠として残す方針を確認したいとき。
- CLI 引数、設定、環境変数、出力項目、状態ファイル、外部依存、補助スクリプト、生成物を増やす条件を定める prompt 断片を扱うとき。

## Do not read this when
- oracle file 自体の責務、疎な正本仕様断片、用語統一、命名、ベストプラクティスとの優先関係など、oracle standard 側の規範を確認したいとき。
- INDEX.md エントリーの書き方やルーティング文書の標準だけを確認したいとき。
- cmoc の具体的な CLI 挙動、path model、永続状態操作、個別サブコマンド実装を調べたいだけのとき。
- 構造化文書型、標準データ型、placeholder の汎用的な実装を確認したいだけのとき。

## hash
- 70a575ce2ed7c73343dade21db24a5f3956c5da825f8ee42f4cfa22d2ff5a5ec

# `routing_rule.py`

## Summary
- INDEX.md をルーティング情報として扱い、作業内容に応じて読むべき本文へ進むための規則文章を構築する。
- 作業開始時の対象領域推定、階層ごとの INDEX.md 確認、候補本文での根拠確認、Summary・Read this when・Do not read this when を使った判断基準を扱う。

## Read this when
- INDEX.md を本文の代替ではなく、読むべき本文を選ぶ案内として扱う規則を確認したいとき。
- 作業開始時にどの階層の INDEX.md から読み始めるべきか、また下位階層へ進む際の読み進め方を確認したいとき。
- Read this when と Do not read this when を使って、読む対象を優先または除外する判断基準を確認したいとき。
- INDEX.md と本文が乖離している可能性がある場合に、どちらを根拠として扱うか確認したいとき。

## Do not read this when
- 個別ファイルやディレクトリの具体的な INDEX.md エントリー内容を確認したいだけのとき。
- oracle file、realization file、index entry standard など、ルーティング規則以外の仕様断片を確認したいとき。
- StructDoc や PlaceholderMap の実装詳細、または path 解決処理そのものを調べたいとき。

## hash
- 8f80f160290402887206332cf110cee5e25abf56ea8f64c2e77b4a7ecb246732
