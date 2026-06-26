# `builder`

## Summary
- AI エージェント呼び出しパラメータを組み立てる実装群の入口。apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、各用途の prompt 内容、補助入力、ファイルアクセス条件、モデル設定、Structured Output 契約への接続を扱う。
- 実際の CLI 実行制御や git 操作、標準文書本文、汎用 prompt 部品そのものではなく、用途別にエージェントへ何を渡し、どの制約で何を返させるかを確認するための領域。

## Read this when
- cmoc の各サブ機能が AI エージェントを呼び出す際の role、goal、補助 prompt、対象パスや差分などの入力埋め込み、読み書き権限、モデルや reasoning effort の指定を確認・変更したいとき。
- apply fork 後の差分要約、realization file の所見列挙、検出済み所見への修正依頼など、apply 系の後段エージェント呼び出し条件と出力契約を追いたいとき。
- oracle review で、新規所見、理由追加、採否判定、所見整理を生成させる prompt と、正本仕様断片を根拠にした Structured Output schema を確認したいとき。
- session join の merge conflict marker 解消や、TUI 実行前のファイルアクセスモード・標準参照要否判定など、特定用途の事前解決エージェント呼び出しを調べたいとき。
- INDEX.md エントリー生成で、対象本文の渡し方、既存目次を根拠にしない方針、読み取り専用条件、出力 schema 指定を実装・検証したいとき。

## Do not read this when
- サブコマンド全体の実行順序、CLI 引数解析、git 操作、フォーク作成・統合、merge conflict marker 検出、生成結果の保存など、エージェント呼び出しパラメータ構築の外側を調べたいとき。
- oracle file、realization file、review standard、apply review standard、realization standard など、prompt に含められる標準文書や仕様本文そのものを読みたいとき。
- 汎用的な prompt 部品、Markdown rendering、構造化ドキュメント表現、パス解決 helper、AgentCallParameter の基本定義だけを確認したいとき。
- 個別の所見カテゴリやレビュー判断基準、実際の対象ファイル探索、git diff 生成、変更ファイル抽出アルゴリズムなど、呼び出しに渡す材料を作る側の詳細を調べたいとき。
- 生成済み INDEX.md の内容評価や、ルーティング文書一般の書き方だけを確認したいとき。

## hash
- 841d3789d8ef7a945918bcbf8698e7b6ef089bc26fc78778ab6c055169f75648

# `prompt_parts`

## Summary
- AI agent に渡す標準プロンプト断片を構築する実装群を収める領域。ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、各種 standard、レビュー規範、INDEX.md エントリー規範、完全プロンプトの組み立てを扱う。
- 個々の規範文章を StructDoc として生成する入口であり、agent 向けプロンプトに含める文面・構成順序・標準プロンプト間の依存関係を確認するための下位要素へ進む起点になる。

## Read this when
- ACP が agent に提示する標準プロンプト群の生成元を探しているとき。
- ファイルアクセス、ルーティング、oracle、realization、review、INDEX.md エントリーなどの規範文書が、どの実装から構築されるかを確認したいとき。
- agent に渡す完全プロンプトの構成や、任意の標準プロンプトを有効化した際に連動して含まれる前提プロンプトを追いたいとき。
- 標準プロンプトの自然言語本文を変更するために、対象となるプロンプト部品を選びたいとき。
- oracle file と realization file の責務境界、realization code の品質基準、oracle レビューや適用レビューの所見基準など、AI へ渡す判断基準の実装箇所を探しているとき。

## Do not read this when
- 生成済みプロンプトの利用先や agent 呼び出しの実行制御を調べたいときは、呼び出しフロー側を直接読む。
- StructDoc、StructCodeBlock、Standard、Requirement などの基盤データ構造や変換処理そのものを確認したいときは、それらの定義元を読む。
- 特定の CLI 挙動、サブコマンド、path model、状態ファイル、テスト対象の仕様を調べたいだけのときは、該当機能の実装や仕様へ直接進む。
- INDEX.md を使ったルーティング文書の個別エントリーを生成するだけで、標準プロンプト本文やその生成実装を確認する必要がないとき。
- oracle file 本文そのものの編集方針や個別仕様を確認したいときは、正本仕様断片側を読む。

## hash
- 8036699a9ce3c326a46f05bf099433bbccad55c1b62fdd3df2c3eff845a06f7e
