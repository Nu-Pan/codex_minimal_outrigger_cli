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
- agent call に渡す完全なプロンプトを、基本プロンプト、ファイルアクセス規則、ルーティング規則、任意追加プロンプト、各種標準プロンプトから組み立てる実装。
- oracle と realization の基本情報を前提として必要に応じて有効化し、oracle standard、realization standard、review/apply review standard、INDEX エントリー標準などの依存関係を解決したうえで、構造化文書のリストを返す。
- 個別の標準プロンプト本文そのものではなく、どの標準プロンプトを含めるかを制御する入口として位置づけられる。

## Read this when
- agent に渡すプロンプト全体の構成順、必ず含まれる基本要素、任意追加要素の挿入位置を確認したいとき。
- 標準プロンプトの有効化フラグ同士の依存関係、たとえば特定の標準を要求した時に前提となる基本情報や別標準も自動的に含まれるかを確認したいとき。
- 新しい標準プロンプト種別を追加し、完全なプロンプトへ注入する条件や順序を既存の制御に合わせたいとき。
- agent call 用のプロンプト生成で、role、summary、goal、ファイルアクセス制限、ルーティング規則、補助プロンプトがどのように一つの構造化文書列へ統合されるかを追いたいとき。

## Do not read this when
- 個別の標準プロンプトに書かれる自然言語の本文内容を確認したいだけの場合は、その標準を構築する対象を直接読む。
- ファイルアクセス規則やルーティング規則の具体的な文面・モード別の詳細を確認したい場合は、それぞれの規則を構築する対象を直接読む。
- 構造化文書クラス自体の表現、保持データ、出力形式を調べたい場合は、構造化文書の定義を読む。
- 生成済みプロンプトを受け取った後の agent 呼び出し処理や CLI 実行フローを調べたい場合は、呼び出し側の実装を読む。

## hash
- 4ef4cf1eb1c3e35bc79da3ea62130616f441048603de51c70addf5a6c9271d4e

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
- oracle file が従うべき規範文章を `StructDoc` として構築する prompt part。人間の認知負荷削減、正本仕様断片としての扱い、未定義部分の許容、文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語・命名統一、oracle file 優先、goal/non-goal の境界といった oracle standard 全体を一つのまとまりとして定義する。
- 各規範は背景・要求・判断例を持つ Standard 群として並び、oracle file の記述規範を prompt 本文に変換する入口になっている。

## Read this when
- oracle file の書き方、分量、責務境界、未定義部分の扱いに関する prompt 本文を確認したいとき。
- oracle standard の各規範がどの背景・要求・判断例として構成され、AI に提示されるかを確認したいとき。
- 正本仕様断片と既存実装の関係、実装から仕様へ逆流させない原則、一般的なベストプラクティスより oracle file を優先する判断基準を扱うとき。
- oracle file における用語統一、命名、論理矛盾、goal/non-goal の境界を prompt 化する実装を変更・検証するとき。

## Do not read this when
- oracle file と realization file の概念定義そのものを確認したいだけのときは、概念定義を述べる正本仕様側を読む。
- realization file の品質、分割、依存、テスト肥大化など realization standard の内容を確認したいときは、realization standard を構築する対象を読む。
- `StructDoc`、`Standard`、`Requirement`、変換関数のデータ構造や整形仕様を調べたいときは、それらの基本型・変換処理を定義する対象を読む。
- 個別の oracle file 本文を編集・確認したいときは、この prompt part ではなく該当する oracle file 本文を読む。

## hash
- e0143e637b7720812bdfedc7f74ded40ec4928c0733e1ac0f4aa2f1ad0d25112

# `realization_standard.py`

## Summary
- realization file の品質基準を StructDoc として組み立てる prompt part。実装・テスト・依存・公開面・コメント・責務分割・完了時点検を、realization file の肥大化抑制と保守性向上という観点から一つの規範集合にまとめている。
- 各基準は相互参照される前提で同時に読む構成になっており、単独の細目ではなく realization file 全体を最小で明確に保つための判断材料を提供する。

## Read this when
- realization file や realization code の品質基準を prompt として生成・変更・確認したいとき。
- 実装追加時の重複削減、旧仕様削除、抽象化の可否、公開面や永続状態の増加抑制、テスト肥大化抑制に関する基準を確認したいとき。
- コメントや docstring に何を書くべきか、または冗長なコメントを避ける基準を確認したいとき。
- 大きな realization file を分割すべきか、凝集性を理由に一体で保つべきかを判断する prompt 側の規範を確認したいとき。

## Do not read this when
- oracle file の正本仕様としての扱い、人間責任、仕様断片の書き方を確認したいだけのとき。
- 実際の CLI コマンド挙動、入出力 schema、状態ファイル形式など、個別機能の実装詳細を調べたいとき。
- StructDoc や Standard のデータ構造そのもの、または standard 変換処理の実装を調べたいとき。
- INDEX.md エントリー生成規則やルーティング文書の記述基準を確認したいだけのとき。

## hash
- 33750997924b6fd92999352125680450d9eeb680d6ddd2bb9ccb3874935ed98a

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
