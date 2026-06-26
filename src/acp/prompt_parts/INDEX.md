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
- agent call に渡す完全なプロンプトを、基本プロンプト、ファイルアクセス規則、ルーティング規則、任意追加文書、必要に応じた標準プロンプト群から組み立てる処理を定義している。
- oracle・realization・review・index entry などの標準プロンプト指定に応じて依存する基本情報を自動的に含め、最終的に agent 向け表現へ置換・無害化した構造化文書列を返す。
- root token の実パス展開や呼び出し元表現の言い換えなど、生成済みプロンプト本文を agent に直接渡せる形へ整える補助処理も含む。

## Read this when
- agent に渡す最終プロンプト全体がどの順序・構成で作られるかを確認したいとき。
- role、summary、goal、file access rule、routing rule、aux prompt、各種 standard prompt がどのように結合されるかを調べるとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard を有効化した際に、どの依存プロンプトが追加されるかを確認したいとき。
- prompt 内の root token や `cmoc から呼び出された` という表現が agent 向けにどう変換されるかを確認・変更したいとき。

## Do not read this when
- 個別の file access rule、routing rule、oracle standard、realization standard などの本文内容そのものを確認したいだけのときは、それぞれの構築元を直接読む。
- StructDoc や StructCodeBlock のデータ構造そのものを調べたいときは、構造化文書を定義する基盤側を読む。
- path token の定義や実パス解決の仕様を確認したいときは、path model 側を読む。
- agent 実行、サブプロセス起動、LLM 呼び出しの制御を調べたいときは、この構築済みプロンプトを利用する呼び出し側を読む。

## hash
- 58c697960b06d3b3a80c6d0ec4c03fa40667dd5b5d8d6760048999d141d25f47

# `file_access_rule.py`

## Summary
- AI エージェントに提示するファイル読み書き規則のプロンプト断片を、指定された読み書きモードプリセットから構築する実装。作業ルート、oracle、memo に対する読み書き禁止条件をモードごとに本文化し、見出し付きの構造化文書として返す。

## Read this when
- ACP 向けプロンプトに含めるファイルアクセス制約の文面を確認・変更したいとき。
- 読み取り専用、oracle 参照専用、realization 編集、oracle 編集、repo 編集といったモードごとの読み書き許可範囲を確認したいとき。
- FileAccessMode の値に応じて生成される StructDoc のタイトルや本文を調整したいとき。

## Do not read this when
- ファイルアクセス規則ではなく、作業ルートやパスエイリアスそのものの解決仕様を確認したいとき。
- FileAccessMode の列挙値や型定義を変更したいとき。
- 生成されたファイルアクセス規則をどのプロンプト全体へ組み込むかを追いたいとき。

## hash
- a424cdb6c8c9580e780e0fb3d2680772604b665cdf85d6a21a8395fe23efb36c

# `index_entry_standard.py`

## Summary
- AI agent が作業前に読む案内エントリーについて、対象本文へ進むべきかを判断できる意味情報だけを書くための規範を組み立てる実装。
- エントリーには、対象の責務、読むべき条件、読まなくてよい境界を対象内容に根拠づけて書き、本文の詳細説明や機械的に補える識別情報を混ぜないことを定める。

## Read this when
- 案内エントリーの生成方針として、本文の代替ではなく読む先を選ぶための情報に限定する基準を確認したいとき。
- 対象内容から根拠を持って言える責務や読む条件だけを抽出し、推測で用途を広げないための規範を確認したいとき。
- エントリーに書くべき情報と、本文詳細・識別子・出力形式のように書かない情報の境界を確認したいとき。

## Do not read this when
- 個別ファイルやディレクトリの実際の案内文を作るために、その対象本文の責務や内容を確認したいだけのとき。
- 構造化文書のデータ構造、要求項目の表現、または規範文書への変換処理そのものを調べたいとき。
- 既存の案内エントリー一覧から読む先を選びたいだけで、エントリー生成時の規範を確認する必要がないとき。

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
- `cmoc review oracle` で oracle file をレビューする際に、列挙すべき所見の種類と根拠条件を構築する prompt part。fatal 所見、minor 所見、所見にしてはいけない判断を `Standard` と `Requirement` からなる構造化文書として定義する。
- oracle file 同士の明確な矛盾や実装者裁量では解消不能な問題を fatal とし、日本語上の誤り・typo・表記揺れなど表記上の単純問題を minor とし、oracle file の具体的記述だけから問題と言えない推測・好み・一般論を所見から除外する基準を扱う。

## Read this when
- `cmoc review oracle` の所見列挙プロンプトで、どの問題を fatal または minor として扱うかを確認したいとき。
- oracle file の矛盾、実装者裁量で補えない仕様問題、typo・表記揺れ・日本語上の誤りをレビュー結果に含める条件を変更または検証するとき。
- oracle file だけでは問題と言い切れない仕様の隙間、一般的なベストプラクティス、実装方針の複数性を所見にしない境界を確認したいとき。

## Do not read this when
- oracle review 以外のサブコマンドや一般的な CLI 動作の仕様・実装を確認したいとき。
- 所見の分類基準ではなく、レビュー対象となる oracle file の定義、配置、正本仕様としての扱いそのものを確認したいとき。
- 構造化文書を組み立てる共通データ型や `Standard` から `StructDoc` への変換処理の実装詳細を確認したいとき。

## hash
- 1404f2566c5a97fa55822658a9003371e37b786d40ea67b3c81e64c0d013c436

# `oracle_standard.py`

## Summary
- oracle file が従うべき規範文章を StructDoc として構築する実装。人間の認知負荷節約、正本仕様断片としての扱い、未定義部分の許容、総文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語・命名統一、oracle file 優先、goal と non-goal の境界記述といった標準項目をまとめている。
- oracle file の品質基準をプロンプト部品として参照したい場合の入口になる。各標準は背景、要求、判断例を持ち、oracle file をどう書くべきか、どこまで AI 裁量を許すべきかを判断するためのまとまりを提供する。

## Read this when
- oracle file の記述方針、粒度、量、重複、用語、命名、矛盾、未定義部分の扱いに関する標準プロンプトを確認したいとき。
- oracle file を正本仕様断片として扱うためのルールを、StructDoc 化される元データとして追いたいとき。
- 実装者である AI に任せてよい範囲と、人間が oracle file に明示すべき範囲の境界を扱うプロンプト部品を調べるとき。
- oracle file に関する標準文書の生成内容が、どの Standard と Requirement から組み立てられているか確認したいとき。

## Do not read this when
- realization file の品質、分割、抽象化、テスト、依存関係、公開面の増加抑制に関する標準だけを確認したいとき。
- oracle file と realization file の定義や配置条件そのものを確認したいとき。
- StructDoc、Standard、Requirement のデータ構造やレンダリング処理の実装を調べたいとき。
- 特定の oracle file 本文の仕様内容や、個別機能の正本仕様断片を確認したいとき。

## hash
- 0a349edcd2226daeb977cfec784977f7ba675274ecc1267c01a68e304d36871a

# `realization_standard.py`

## Summary
- realization file を小さく保ち、現行仕様に必要な実装・テスト・補助要素だけへ整理するための基準を StructDoc として組み立てる。
- 重複実装の集約、旧仕様向け実装の削除、責務境界に沿った分割・統合、公開面・状態・依存関係・補助ファイル・テストの増加抑制など、realization 全体の肥大化を防ぐ判断基準を扱う。
- prompt parts の一部として、実装担当 AI に渡す realization 品質・最小化方針の本文を生成する入口である。

## Read this when
- realization file の追加・変更・削除時に、どこまで既存実装を整理し、重複や旧仕様向け要素を取り除くべきか確認したいとき。
- 新しい関数・クラス・モジュール・共有 helper・公開設定・永続状態・外部依存・補助スクリプトを追加してよい条件を確認したいとき。
- realization code や realization test のサイズ、責務境界、分割・統合、コメントや docstring の残し方に関する基準を生成・変更したいとき。
- 実装完了前に、未使用要素、重複した責務、不要な TODO や旧テストなどの削除・統合余地を確認するための標準文書を扱うとき。

## Do not read this when
- oracle file の責務、人間が持つ正本仕様断片の書き方、または oracle から realization への関係そのものを確認したいだけのとき。
- INDEX.md エントリーの生成規則やルーティング文書の書き方を確認したいとき。
- 特定の CLI サブコマンド、状態ファイル、path model、実装処理の具体的な挙動を調べたいとき。
- StructDoc や Standard、Requirement のデータ構造や変換処理そのものを変更・確認したいとき。

## hash
- 8863a0f211c617e6e94e9ec938e0d908aa82d4193ae83c3629d3d2e5d5028d50

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
