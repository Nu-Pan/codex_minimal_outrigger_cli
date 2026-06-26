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
- agent 呼び出しへ渡す完全な構造化プロンプトを組み立てる実装。基本情報、ファイルアクセス規則、ルーティング規則、追加プロンプトを並べ、指定された標準プロンプト群を依存関係込みで注入する。
- root token や内部呼び出し由来の表現を、agent に渡す前の文面として適切な実パス・表現へ置換するサニタイズ処理も担う。

## Read this when
- agent に渡す最終プロンプトの構成順序、必ず含まれる基本要素、任意標準プロンプトの追加条件を確認したいとき。
- oracle、realization、review、index entry などの標準プロンプトを有効化した際に、どの前提プロンプトが連動して含まれるかを確認・変更したいとき。
- 追加プロンプトが完全プロンプト内のどこに差し込まれるか、また最終的にどのような StructDoc のリストとして返されるかを確認したいとき。
- agent 向けプロンプトから内部の root token や呼び出し元表現を除去・置換する処理を確認・変更したいとき。

## Do not read this when
- 個々のファイルアクセス規則、ルーティング規則、oracle 標準、realization 標準、review 標準、index entry 標準の本文そのものを確認したいだけのときは、それぞれの標準プロンプトを構築する対象を直接読む。
- RootToken の定義、実パス解決、StructDoc や StructCodeBlock のデータ構造を確認したいだけのときは、それらを定義する基盤側の対象を直接読む。
- agent prompt 全体の組み立てではなく、特定のサブプロンプトの文言や仕様だけを変更したいとき。
- 生成済みプロンプトを実際にどのプロセスへ渡すか、agent 呼び出しの実行制御を追いたいとき。

## hash
- 0005725ac486fc1ef1117decc5620d424a99e32685c81fef05449d8cabf05e63

# `file_access_rule.py`

## Summary
- AI エージェントへ提示するファイル読み書き制約のプロンプト断片を、指定された読み書きモードに応じて構築する実装。作業ルート、oracle、.agents、memo に対する読み書き可否をモード別に本文化し、構造化ドキュメントとして返す。

## Read this when
- ACP へ渡すファイルアクセス制約文の内容、見出し、モード別の禁止範囲を確認または変更したいとき。
- 読み書きモードプリセットと、作業ルート・oracle・.agents・memo の扱いとの対応を確認したいとき。
- エージェント実行時に提示される read-only、oracle 読み取り、realization 書き込み、oracle 書き込み、repo 書き込みの制約文を調整したいとき。

## Do not read this when
- パスキーワードや作業ルート解決そのものの定義を確認したいだけのときは、パスモデル側を読む。
- 読み書きモードの列挙値や型定義を確認したいだけのときは、ACP の基本型定義側を読む。
- 構造化ドキュメントの表現形式や整形処理を確認したいだけのときは、構造化ドキュメント側を読む。

## hash
- 4920b058dea9bdcbcc9beecb4782ccd32763200f0860d6fdc47fff920dbe49ba

# `index_entry_standard.py`

## Summary
- 読む対象を選ぶための案内文が満たすべき規範を、構造化文書として生成する実装である。
- 案内文には、対象の責務、読むべき条件、読まなくてよい境界を本文根拠に基づいて書き、機械的識別情報や本文の詳細説明を混ぜないことを定める。
- 案内文生成や案内文品質の実装を確認するときに、求められる意味情報と禁止される過剰説明の境界を知る入口になる。

## Read this when
- 読む対象を選ぶための案内文に、どのような責務・読む条件・除外条件を書くべきか確認したいとき。
- 案内文生成ロジックで、本文根拠に基づく情報だけを出すべきか、推測や将来用途を含めてよいか判断したいとき。
- 案内文に機械的識別情報、出力形式の説明、本文を読まなければ分からない詳細を含めない制約を確認したいとき。
- 対象本文へ誘導する条件が広すぎないか、同階層の他対象ではなくその対象へ進む理由を書けているかを検討するとき。

## Do not read this when
- 案内文そのものではなく、正本仕様断片や実装ファイル全般の扱い、品質、分割、重複削減の規範を確認したいとき。
- 構造化文書のデータ構造、規範要素の型、文書変換処理の一般的な実装を確認したいとき。
- 個別の案内文エントリー内容を生成・修正したいだけで、案内文が従う一般規範の確認が不要なとき。
- 出力項目名や型など、呼び出し側の出力仕様で機械的に分かる情報だけを確認したいとき。

## hash
- 386a32b55a8f1730b5760b5e634fab4699f3cecc067fa69c8e208df58b94f82d

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
- oracle file のレビューで所見を列挙する際の判定規範を構築する実装。fatal 所見、minor 所見、所見にしない対象の境界を StructDoc としてまとめ、正本仕様断片の矛盾、実装者裁量で補える隙間、表記上の単純誤りをどう扱うかを定義する。
- oracle file レビュー用プロンプト部品のうち、所見の重大度分類と、oracle file の記述だけを根拠に問題と言えるかどうかの基準を確認する入口になる。

## Read this when
- oracle file レビューで、仕様断片同士の明確な矛盾や実装不能な要求を fatal 所見にすべきか判断したいとき。
- 日本語の誤り、typo、用語不統一、表記揺れを minor 所見として扱う基準を確認したいとき。
- oracle file に未定義部分や複数の実装方針が残っているだけの状態を、所見にしてよいか切り分けたいとき。
- oracle file レビュー用の規範文章を生成する処理や、その StructDoc 構造を変更・確認したいとき。

## Do not read this when
- oracle file そのものの定義、realization file との関係、正本仕様断片の一般原則を確認したいだけのとき。
- oracle file レビュー結果の出力形式、CLI コマンド、保存先、実行フローを確認したいとき。
- 通常の realization code レビューやテスト品質の基準を確認したいとき。
- fatal/minor/対象外という所見判定ではなく、個別の oracle file 本文の内容そのものを調べたいとき。

## hash
- 7fddf3e4f4aee293b48f8539fc6273c5ecfd02007a44c78ba1450ac5557712fe

# `oracle_standard.py`

## Summary
- oracle file が従うべき規範文章を StructDoc として構築する実装。人間の認知負荷削減、正本仕様断片としての扱い、未定義部分の許容、文字数最小化、論理的整合性、実装から仕様への逆流禁止、用語統一、命名、ベストプラクティスより oracle file を優先する判断、goal と non-goal の境界を扱う。
- prompt parts 側で oracle standard を生成する入口であり、Standard と Requirement の列挙から構造化文書へ変換する責務を持つ。

## Read this when
- oracle file 向け規範文章として出力される項目や文言を確認したいとき。
- oracle standard の StructDoc 生成処理、Standard/Requirement の並び、または standard_to_struct_doc への渡し方を変更するとき。
- oracle file の書き方に関する規範が、プロンプト部品としてどの内容で実装されているか確認するとき。

## Do not read this when
- oracle file と realization file の基本定義や所有関係だけを確認したいとき。
- realization file や realization test の品質・肥大化抑制・依存追加の規範を確認したいとき。
- StructDoc、Standard、Requirement、standard_to_struct_doc 自体のデータ構造や変換ロジックを確認したいとき。
- 生成済みの自然言語文書としての oracle standard の表示結果だけを確認したいとき。

## hash
- a877eaac93f163ce3855b5c7cb620d1997fcdb55a07d3dc156a7604bff89b99d

# `realization_standard.py`

## Summary
- realization file を小さく、読みやすく、現行仕様に必要な範囲へ保つための standard を StructDoc として組み立てる実装。
- 重複削減、旧仕様実装の削除、責務境界に沿った分割・統合、公開面や依存関係の増加抑制、テスト肥大化の抑制、変更完了時の削除・統合確認といった realization code 全般の品質基準を扱う。
- ACP の prompt parts として、実装担当 AI に realization file の保守性・最小性・抽象化・状態管理・テスト整理に関する判断基準を渡す入口になる。

## Read this when
- realization file や realization code の品質基準、肥大化抑制、重複削減、旧実装削除に関するプロンプト内容を確認・変更したいとき。
- 実装追加時に既存実装の整理、抽象化の作成条件、公開面・設定面・永続状態の追加条件を AI にどう指示しているか確認したいとき。
- realization test、外部依存、補助ファイル、生成物を増やす際の制約や、変更完了前の削除・統合確認に関する標準文書の生成元を確認したいとき。

## Do not read this when
- oracle file の正本仕様としての扱い、人間の認知負荷、仕様断片の未定義部分など oracle 側の標準を確認したいだけのとき。
- INDEX.md エントリーそのものの書き方やルーティング文書生成ルールを確認したいだけのとき。
- 個別の CLI 挙動、サブコマンド仕様、パスモデル、実行状態など、realization file 全般の品質基準ではなく具体機能の仕様や実装を調べたいとき。

## hash
- 1657f67dc21bf798d9725ccacebc23b7b0e8db34d95a3552218e285b30b065ef

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
