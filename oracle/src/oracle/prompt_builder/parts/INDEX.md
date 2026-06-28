# `apply_review_standard.py`

## Summary
- oracle file の内容を realization file に適用してレビューする際、何を所見として扱うべきかを定める規範を構築する。
- oracle file と realization file の明確な不整合、oracle file の仕様断片の隙間、realization file 単体で明らかな致命的問題の扱いを切り分ける。
- 所見の根拠を正本仕様断片に置きつつ、未定義部分を過剰に問題化しないための境界を示す。

## Read this when
- oracle file と realization file を比較して、レビュー所見として列挙すべき不整合を判断したいとき。
- oracle file に明記されていない realization file の挙動を、所見にすべきか許容すべきか判断したいとき。
- oracle file との不整合ではないが、realization file 単体で明らかなバグや実行不能な問題を所見に含めてよいか確認したいとき。
- ベストプラクティス、実装上の違和感、過去仕様らしき残骸をレビュー所見として扱う境界を確認したいとき。

## Do not read this when
- oracle file や realization file の基本定義、所有責任、配置分類そのものを確認したいだけのとき。
- realization file をどのように設計・分割・削除・統合すべきかという実装品質全般の規範を確認したいとき。
- oracle file 自体の書き方、疎な正本仕様断片としての保守方針、用語統一や命名の一般規範を確認したいとき。
- レビュー所見の判断ではなく、特定コマンドや特定機能の仕様本文を探しているとき。

## hash
- 8084bdb3ce48e798cad1515dc50a8d5c7d66c417ec7d2d32494a4d68d6b43799

# `complete_prompt.py`

## Summary
- agent call に渡す完全なプロンプトを、基本プロンプト、ファイルアクセス規則、ルーティング規則、任意追加プロンプト、各種標準プロンプトから組み立てる関数を定義している。
- 指定された標準フラグ間の依存関係を解決し、必要な基本情報や標準断片が漏れなく追加されるようにする入口である。

## Read this when
- agent に渡すプロンプト全体の構成順序、必ず含まれる項目、任意に注入される標準断片を確認したいとき。
- oracle、realization、review、INDEX エントリーなどの標準プロンプト指定が、どの依存関係により追加されるかを確認したいとき。
- ファイルアクセス規則やルーティング規則が完全なプロンプトにどの位置で組み込まれるかを確認したいとき。
- agent call 用プロンプト構築処理へ新しい標準フラグや標準断片の注入条件を追加・変更したいとき。

## Do not read this when
- 個別のファイルアクセス規則、ルーティング規則、oracle 標準、realization 標準などの本文内容だけを確認したいときは、それぞれの標準断片を構築する対象へ進む。
- StructDoc 自体のデータ構造や振る舞いを確認したいときは、その定義元へ進む。
- 生成されたプロンプトを実際にどの agent 実行経路へ渡すかを確認したいときは、呼び出し側の処理へ進む。

## hash
- 18efdddfcbec9b291f2ca8aac02f42177f6c4fe051e13b6d1953fd1ea9afcc9f

# `file_access_rule.py`

## Summary
- AI エージェントに提示するファイル読み書き規則のプロンプト本文を、読み書きモードプリセットごとに構築する責務を持つ。
- 作業対象ルート、oracle、memo に対する読み書き可否の境界を、モードに応じた箇条書きの構造化文書として返す入口である。

## Read this when
- エージェントへ渡すファイルアクセス制約の文面を確認または変更したいとき。
- 読み取り専用、oracle のみ読み取り、realization 書き込み、oracle 書き込み、リポジトリ書き込みの各モードで、どの領域が読み書き禁止になるかを確認したいとき。
- ファイルアクセスモードとプロンプト本文の対応関係、または不正なモードを受けた場合の扱いを確認したいとき。

## Do not read this when
- oracle file と realization file の概念定義や所有責任そのものを確認したいだけのとき。
- パスキーワードや作業対象ルートの解決規則を確認したいとき。
- 構造化文書の表現方法や文字列整形処理そのものを確認したいとき。
- 実際のファイル操作を行う実装、権限チェック、サンドボックス制御の挙動を確認したいとき。

## hash
- a424cdb6c8c9580e780e0fb3d2680772604b665cdf85d6a21a8395fe23efb36c

# `index_entry_standard.py`

## Summary
- INDEX.md の個々のエントリーが、本文の代替ではなく読む先を選ぶためのルーティング情報として成立するための規範を定義する。
- 対象の責務、読むべき条件、読まなくてよい境界を、対象内容に根拠を持つ意味情報として書くことを求める。
- 機械的に補える識別情報や出力形式の説明を混ぜず、読む判断に必要な情報だけに絞るための基準を示す。

## Read this when
- INDEX.md エントリーを生成・レビューし、対象へ進むべき条件や進まなくてよい境界の書き方を確認したいとき。
- エントリーが本文の要約に寄りすぎていないか、または広すぎる誘導になっていないかを判断したいとき。
- 対象内容に根拠のない責務、将来用途、機械的な識別情報をエントリーへ混ぜてよいか迷うとき。

## Do not read this when
- 特定の対象本文そのものの仕様や実装内容を知りたいとき。
- INDEX.md 全体の生成手順、配置規則、更新フローを確認したいとき。
- 出力データの項目や型など、機械的に決まる形式だけを確認したいとき。

## hash
- 9948bdff6712106ea91119db4a9fbd06529bf36046318db4e3adb5863e9c5fb0

# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の基本概念を説明するプロンプト部品。oracle file を人間が責任を持つ正本仕様断片、realization file を AI が編集する具体化物として定義し、それぞれの配置領域・対象外条件・下位概念を整理している。
- oracle doc、oracle src、oracle test、および realization implementation、realization test、realization ancillary など、正本仕様断片と実装成果物を区別するための基礎用語への入口になる。

## Read this when
- oracle file と realization file の違い、所有者、編集責任、正本仕様としての優先関係を確認したいとき。
- oracle 配下の文書・実装・テストと、通常の実装・テスト・補助ファイルをどの概念として扱うべきか判断したいとき。
- 正本仕様断片から realization file が生成される関係や、realization file から oracle file へ逆向きに仕様化してはいけない境界を確認したいとき。
- INDEX.md や gitignore 対象ファイルが oracle file / realization file の概念から除外されるかを確認したいとき。

## Do not read this when
- 個別コマンド、出力形式、状態ファイル、実装手順など、cmoc の具体的な機能仕様を調べたいとき。
- oracle file や realization file の品質基準、最小化方針、抽象化方針などの標準を確認したいとき。
- パスキーワード自体の意味や解決規則を調べたいときは、パスモデルの説明を直接読む方が適切。
- 特定の realization implementation や realization test の現在の挙動を調べたいだけで、oracle / realization の概念区分を確認する必要がないとき。

## hash
- fe33761da72ba70e8745a65b7ba3562e83c07ac65605f824a71f3fadb8996a03

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` が oracle file をレビューするときの所見分類基準を構築する prompt part。fatal、minor、所見にしない対象の境界を定義し、レビュー結果が正本仕様断片の明確な矛盾・解消不能性・単純な表記問題にだけ基づくようにする。

## Read this when
- oracle file レビューで、ある問題を fatal 所見として扱うべきか判断したいとき。
- oracle file の誤字、表記揺れ、日本語上の単純な問題を minor 所見として扱う基準を確認したいとき。
- oracle file だけから問題と言い切れない推測、好み、一般的なベストプラクティスを所見から除外する境界を確認したいとき。
- `cmoc review oracle` の所見列挙プロンプトが、どのようなレビュー規範を AI に渡しているか確認したいとき。

## Do not read this when
- oracle file そのものの定義、realization file との関係、正本仕様断片としての基本原則を確認したいだけのとき。
- oracle レビュー結果の JSON schema、入出力形式、CLI サブコマンドの実行仕様を確認したいとき。
- oracle file の内容を実際に修正するため、対象仕様本文の意味や意図を確認したいとき。
- 一般的な realization code の実装品質、テスト整理、依存追加の基準を確認したいとき。

## hash
- 1404f2566c5a97fa55822658a9003371e37b786d40ea67b3c81e64c0d013c436

# `oracle_standard.py`

## Summary
- oracle file の書き方に関する共通規範を StructDoc として構築する。人間の認知負荷を節約し、正本仕様断片を小さく疎に保ち、未定義部分・論理整合性・実装から仕様への逆流禁止・用語統一・命名・ベストプラクティスとの優先関係・goal/non-goal の境界を扱う。

## Read this when
- oracle file に何を書くべきか、何を書かないべきかの基本方針を確認したいとき。
- 正本仕様断片の粒度、文字量、重複、未定義部分の扱いを判断したいとき。
- oracle file 同士の矛盾、用語揺れ、命名の妥当性、実装由来の仕様追加可否を評価したいとき。
- 一般的なベストプラクティスと oracle file の要求が競合した場合の優先関係を確認したいとき。

## Do not read this when
- 特定の CLI 挙動、出力 schema、状態ファイル、パスモデルなど個別機能の仕様を確認したいだけのとき。
- realization file の実装品質、テスト整理、依存追加、補助ファイル管理の規範だけを確認したいとき。
- oracle file の形式や構造ではなく、生成された realization code の具体的な実装箇所を探しているとき。

## hash
- 0a349edcd2226daeb977cfec784977f7ba675274ecc1267c01a68e304d36871a

# `realization_standard.py`

## Summary
- realization file が従うべき規範文章を構築する oracle src。実装・テスト・補助ファイルを最小で保守しやすく保つための基準を、文字数最小化、品質、コメントと docstring、ファイル分割、既存実装整理、抽象化、公開面・状態、テスト、依存関係、変更完了時の削除確認という観点で定義する。
- 実装担当 AI に渡す realization standard の本文を生成する入口であり、realization file を追加・変更・整理する際に参照される規範群の内容を確認するための対象。

## Read this when
- realization file、realization code、realization test、realization ancillary に対する一般的な実装規範を確認したいとき。
- 実装やテストを追加する前に、既存実装の修正・移動・置換・削除・統合を優先すべきか判断したいとき。
- 新しい関数・クラス・モジュール・共有 helper・外部依存・補助スクリプト・状態ファイル・CLI 引数などを追加してよい条件を確認したいとき。
- コメントや docstring に、実装意図・根拠・oracle file path・取らなかった方針を書くべきか、または冗長なので書くべきでないかを判断したいとき。
- realization file の分割・統合、巨大化、小さすぎるファイル群、重複実装、旧仕様由来の実装やテストをどう扱うべきか確認したいとき。
- 実装完了前に、未使用要素、旧実装、重複テスト、過大 fixture、不要 TODO や NOTE、再生成可能な成果物を残していないか確認する基準が必要なとき。

## Do not read this when
- oracle file 自体の書き方、正本仕様断片の疎さ、人間の認知負荷、実装から仕様への逆流禁止など、oracle 側の規範を確認したいだけのとき。
- パス語彙、oracle file と realization file の基本定義、配置先、下位概念だけを確認したいとき。
- 特定の CLI 挙動、出力 schema、コマンド仕様、個別機能の正本仕様を探しているとき。
- INDEX.md エントリーの生成規則やルーティング文書としての書き方だけを確認したいとき。
- 生成された StructDoc を実際にどう連結・出力・表示するかという基盤処理を調べたいとき。

## hash
- cd7279ccbd21f535147ac6a242f486faa8681f5ca797a952bc5a647efae5e8fb

# `routing_rule.py`

## Summary
- INDEX.md を本文の代替ではなく同階層の対象へ進むための案内として扱い、Summary、Read this when、Do not read this when を手がかりに読むべき本文を選ぶための規則文章を構築する。
- 作業開始時に近い階層の INDEX.md から読むこと、対象領域が推定できない場合は work root の INDEX.md を起点にすること、下位へ進む際は必要に応じて各階層の INDEX.md を読むことを定める。
- INDEX.md だけで判断できない場合は候補本文で根拠を確認し、総当たりより先に INDEX.md で候補を絞り、本文と INDEX.md が乖離する可能性がある場合は本文を根拠にする判断基準をまとめる。

## Read this when
- INDEX.md を使って読むべきファイルやディレクトリを選ぶ手順を確認したいとき。
- 作業開始時にどの階層の INDEX.md から読み始めるべきか、また対象領域を推定できない場合の起点を確認したいとき。
- Read this when や Do not read this when をどう優先し、INDEX.md と本文の関係をどう扱うかを確認したいとき。
- 関連候補を総当たりで読む前に、INDEX.md によって読む対象を絞る方針を確認したいとき。

## Do not read this when
- INDEX.md の個別エントリー生成基準やエントリー品質の要求を確認したいだけのとき。
- oracle file、realization file、oracle src などのファイル種別や責務境界を確認したいとき。
- 特定のディレクトリ配下でどの本文へ進むべきかを知りたいだけで、その階層の INDEX.md を直接読めば足りるとき。
- path keyword の定義や work root の解決方法そのものを確認したいとき。

## hash
- d8e006c47095d5110437cb8a851dee23ad97b314657531a3d570f52d146f8443
