# `apply_review_standard.py`

## Summary
- oracle file の正本仕様断片を realization file に適用してレビューする際、どの差分や問題を所見として扱うべきかを定める規範文章を構築する。
- 明確な正本仕様との不整合、仕様断片の隙間だけを根拠にした過剰な指摘の禁止、realization file 単体で明らかな致命的問題の扱いを、背景・要求・例としてまとめる。
- oracle file と realization file の関係を前提に、レビュー所見の根拠を正本仕様断片へ置くための判断基準への入口となる。

## Read this when
- oracle file の内容を realization file に適用するレビューで、何を所見として列挙してよいか判断したいとき。
- oracle file に明記されていない実装差を、不整合として扱うべきか、AI の裁量範囲として許容すべきかを切り分けたいとき。
- realization file だけから見えるバグや実行不能な問題を、oracle file との不整合ではない所見として扱えるか確認したいとき。
- レビュー指摘が oracle file の正本仕様断片に根拠を持っているか、または単なる品質改善提案に留まっていないかを判断したいとき。

## Do not read this when
- oracle file と realization file の照合レビューではなく、通常の実装追加・リファクタリング・テスト追加の一般規範を確認したいとき。
- oracle file そのものの書き方、疎な正本仕様断片の維持、用語統一、仕様文書の編集方針を確認したいとき。
- INDEX.md エントリーの生成規則やルーティング文書の書き方だけを確認したいとき。
- 特定の CLI 挙動、path model、状態ファイル、サブコマンドなどの個別仕様を探しているとき。

## hash
- 8084bdb3ce48e798cad1515dc50a8d5c7d66c417ec7d2d32494a4d68d6b43799

# `complete_prompt.py`

## Summary
- agent call に渡す完全なプロンプト構成を組み立てる実装。role、summary、goal、ファイルアクセス規則、ルーティング規則、追加プロンプトを基本要素として並べ、指定された標準プロンプト群を依存関係に従って追加する入口になっている。
- 各標準プロンプトの有効化フラグを受け取り、上位の標準が必要とする基本情報や関連標準を自動的に有効化してから、最終的な構造化ドキュメント列を返す。

## Read this when
- agent に渡すプロンプト全体の組み立て順、必ず含まれる基本要素、任意標準プロンプトの追加条件を確認したいとき。
- oracle、realization、review、apply review、index entry などの標準プロンプトを有効化した場合に、どの依存プロンプトが同時に含まれるかを確認したいとき。
- プロンプト部品を追加・削除する変更で、完全なプロンプトに含める位置や依存フラグの扱いを調整する必要があるとき。

## Do not read this when
- 個別の標準プロンプト本文や文言を確認したいだけのとき。その場合は各標準プロンプトを構築する対象を直接読む。
- ファイルアクセス規則やルーティング規則そのものの内容を確認したいとき。この実装はそれらを呼び出すだけなので、規則を定義する対象を直接読む。
- agent call の実行処理、外部プロセス起動、または返されたプロンプトの利用側を調べたいとき。この対象はプロンプト列の構築だけを扱う。

## hash
- 18efdddfcbec9b291f2ca8aac02f42177f6c4fe051e13b6d1953fd1ea9afcc9f

# `file_access_rule.py`

## Summary
- AI エージェントへ渡すファイル読み書き規則のプロンプト断片を、読み書きモードプリセットごとに構築する実装。作業ルートを解決し、各モードに応じてツリー外アクセス、oracle 配下、memo 配下、書き込み可否の制約文を組み立て、構造化文書として返す。

## Read this when
- エージェントへ提示するファイルアクセス制約の文面を変更したいとき。
- 読み取り専用、oracle 専用読み取り、実装書き込み、oracle 書き込み、リポジトリ書き込みの各プリセットが、どの範囲の読み書きを許す文面になるか確認したいとき。
- 読み書きモードから構造化プロンプト文書を生成する処理の責務範囲や例外条件を確認したいとき。

## Do not read this when
- パスキーワードや作業ルート解決そのものの定義を確認したいだけのとき。
- 読み書きモードの列挙値や型定義を確認したいだけのとき。
- 構造化文書のデータ構造や整形処理を確認したいだけのとき。
- 実際のファイルシステムアクセス制御や権限 enforcement の実装を探しているとき。

## hash
- 7a8501f429c2afc741381c153cb19efe8e3bc46db311b639305ca339c46a8253

# `index_entry_standard.py`

## Summary
- INDEX.md エントリーを、本文を読む前に読むべき対象を判断するためのルーティング情報として扱う規範文章を生成する。
- エントリーに書くべき意味情報、対象内容への根拠、対象外責務を書かない境界、機械的識別情報を混ぜない方針を定義する。
- INDEX.md 生成や評価で、エントリーの内容品質を揃えるための規範文書への入口となる。

## Read this when
- INDEX.md エントリーにどの程度の要約・読む条件・読まない条件を書くべきかを確認したいとき。
- ルーティング文書のエントリーが、本文説明に寄りすぎていないか、または読む条件が広すぎないかを判断したいとき。
- 対象内容に根拠のない責務や将来用途をエントリーへ含めてよいか迷うとき。
- ファイル名、識別子、出力形式など機械的に補える情報を、自然言語の意味情報へ含めるべきか判断したいとき。

## Do not read this when
- 個別の対象について実際の INDEX.md エントリー文面だけを作りたいときは、対象本文そのものを読む方が直接的である。
- oracle file や realization file の一般的な品質基準、編集方針、責務境界を確認したいときは、それぞれの規範文章を読む方が適切である。
- Structured Output の項目構造や型そのものを確認したいだけのときは、この規範文章の対象外である。
- INDEX.md を使った探索手順やリポジトリ内の具体的なルーティング先を調べたいときは、該当階層のルーティング情報を読む方が適切である。

## hash
- 9948bdff6712106ea91119db4a9fbd06529bf36046318db4e3adb5863e9c5fb0

# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の基本概念を説明するプロンプト部品を構築する。
- oracle file を人間が責任を持つ正本仕様断片、realization file を AI が編集する具体化物として区別し、それぞれの定義・役割・下位概念を扱う。
- oracle doc/src/test と realization implementation/test/ancillary の配置上の分類を確認する入口になる。

## Read this when
- oracle file と realization file の責務境界をプロンプトに含める処理を確認・変更したいとき。
- 正本仕様断片と実装・テスト・補助ファイルの違いを説明する文面を調整したいとき。
- oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary の分類や配置説明が必要なとき。
- AI が編集してよい対象と、人間が所有して編集する対象の境界を確認したいとき。

## Do not read this when
- 個別の oracle 標準や realization 標準の詳細な要求事項を確認したいだけのとき。
- パスキーワードそのものの定義や解決規則を確認したいとき。
- 特定の CLI 挙動、サブコマンド、テスト実装の詳細を調べたいとき。
- INDEX.md エントリーの生成規則やルーティング文書の品質基準だけを確認したいとき。

## hash
- fe33761da72ba70e8745a65b7ba3562e83c07ac65605f824a71f3fadb8996a03

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` で oracle file をレビューするときに、検出した問題を所見として扱うかどうか、また fatal/minor のどちらに分類するかを決めるための規範文章を構築する。
- 正本仕様断片同士の明確な矛盾や実装者裁量では解消できない問題を fatal とし、日本語の誤り・typo・用語揺れなど表記上の単純な問題を minor とし、oracle file だけから問題と言い切れないものは所見にしない、という判定境界を担う。
- レビュー所見の列挙ロジックやプロンプト部品から参照される、所見作成の判断基準を構造化文書として提供する入口である。

## Read this when
- `cmoc review oracle` が列挙する所見の分類基準、特に fatal と minor の境界を確認したいとき。
- oracle file の矛盾、未定義部分、表記揺れ、typo、好みや一般論に基づく指摘を、所見として扱うべきか判断する実装やテストを変更するとき。
- レビュー結果が oracle file の具体的記述だけを根拠にしているか、実装者の裁量で自然に補える仕様の隙間を誤って問題扱いしていないかを確認したいとき。

## Do not read this when
- oracle file や realization file の基本的な定義、正本仕様断片と実装成果物の関係を確認したいだけのとき。
- `cmoc review oracle` 以外のサブコマンド、入出力 schema、永続状態、CLI 引数などの具体仕様を探しているとき。
- 所見分類の規範ではなく、構造化文書を組み立てる共通型、標準文書変換、プロンプト部品の集約方法そのものを確認したいとき。

## hash
- 1404f2566c5a97fa55822658a9003371e37b786d40ea67b3c81e64c0d013c436

# `oracle_standard.py`

## Summary
- oracle file が従うべき規範を StructDoc として構築する実装。人間の認知負荷節約、正本仕様断片としての扱い、未定義部分の許容、文字数最小化、論理的整合性、実装から仕様への逆流禁止、用語統一、命名、oracle file 優先、goal と non-goal の境界記述に関する標準を定義する。
- oracle file の標準文書を生成するための prompt parts 実装であり、各規範を Standard と Requirement の列として記述し、構造化文書へ変換して返す入口になっている。

## Read this when
- oracle file に適用される共通規範の生成内容や、どの標準項目が prompt parts として組み込まれるかを確認したいとき。
- oracle file の記述方針について、認知負荷削減、仕様断片の疎さ、未定義部分の扱い、矛盾禁止、用語・命名、ベストプラクティスとの優先関係を実装上どのように表現しているかを確認したいとき。
- oracle standard の StructDoc を組み立てる処理、または Standard・Requirement から構造化文書へ変換する呼び出し側を変更するとき。

## Do not read this when
- oracle file と realization file の概念定義そのものを確認したいだけのとき。
- realization file、realization code、realization test に適用される実装・テスト側の規範を確認したいとき。
- INDEX.md エントリーの書き方やルーティング文書の規範だけを確認したいとき。
- 個別の oracle file が定めるプロダクト仕様や、特定サブコマンドの挙動仕様を確認したいとき。

## hash
- 0a349edcd2226daeb977cfec784977f7ba675274ecc1267c01a68e304d36871a

# `realization_standard.py`

## Summary
- realization file に求める規範文章を構築するための実装。文字数最小化、品質、責務境界とファイルサイズ、既存実装との整理、抽象化、公開面・状態、テスト、依存関係・補助ファイル、変更完了時の削除・統合確認に関する standard 群をまとめて返す。
- realization standard の文書本文を生成する入口であり、各 standard は背景・要求・判断例を持つ構造化文書として組み立てられる。

## Read this when
- realization file や realization code が従うべき規範文書の生成内容を確認・変更したいとき。
- 実装・テスト・補助ファイルの肥大化、重複、旧仕様残存、不要な抽象化、公開面や永続状態の増加を抑制する基準を確認したいとき。
- realization standard に新しい要求・背景・判断例を追加する、または既存の standard 群の責務範囲を調整したいとき。
- cmoc が生成する realization standard の StructDoc 構成や、standard から構造化文書へ変換する流れを確認したいとき。

## Do not read this when
- oracle file の規範、正本仕様断片の書き方、人間責任の仕様管理について確認したいだけのとき。
- 特定の CLI 挙動、path model、実行状態、入出力 schema など、個別機能の実装詳細を探しているとき。
- realization standard の本文ではなく、構造化文書型や standard 変換処理そのものの実装を確認したいとき。
- INDEX.md エントリーの書き方やルーティング文書の一般規範だけを確認したいとき。

## hash
- fd6040e79dad679cd79b34e76dbc76ec53f367723699c3d20836a28d42a5b54d

# `routing_rule.py`

## Summary
- INDEX.md を本文の代替ではなく同階層の対象へ進むための案内として扱い、Summary / Read this when / Do not read this when を手がかりに読むべき本文を選ぶための規則文章を構築する。
- 作業開始時の起点選択、下位階層へ進む際の追加確認、INDEX.md だけで判断できない場合の本文確認、総当たり前の候補絞り込みという読み進め方を定義する。
- Read this when と Do not read this when による優先・回避判断、および INDEX.md と本文が乖離し得る場合は本文を根拠にする判断基準をまとめる。

## Read this when
- AI agent が作業前に INDEX.md をどう使って読む対象を選ぶべきかを確認したいとき。
- 対象領域が推定できる場合とできない場合で、どの階層の INDEX.md から読み始めるかを確認したいとき。
- 下位ディレクトリへ進む際に追加で INDEX.md を読む条件や、INDEX.md で判断できない場合に本文へ進む条件を確認したいとき。
- Read this when / Do not read this when / Summary を使ったルーティング判断の優先基準を確認したいとき。
- INDEX.md と本文の内容が食い違う可能性がある場面で、どちらを根拠に扱うかを確認したいとき。

## Do not read this when
- 個別ファイルの正本仕様、実装内容、テスト内容そのものを確認したいだけで、INDEX.md を使った読み進め方を確認する必要がないとき。
- INDEX.md エントリーを生成するための対象本文を探している段階で、既に読むべき本文が特定できているとき。
- パス概念そのものの定義や root path の意味を確認したいときは、path model の定義を直接読む。
- oracle file と realization file の責務境界や編集権限を確認したいときは、それらを定義する正本仕様を直接読む。

## hash
- d8e006c47095d5110437cb8a851dee23ad97b314657531a3d570f52d146f8443
