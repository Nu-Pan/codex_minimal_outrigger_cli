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
- ACP の agent call 用プロンプトを構成する prompt part 群を扱うディレクトリ。ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、各種 standard、レビュー基準、INDEX エントリー規範、完全プロンプト組み立てをそれぞれ構造化文書として生成する実装への入口になる。
- 個別ファイルは自然言語の標準や規則そのものを定義するものと、それらを条件に応じて完全なプロンプトへ統合するものに分かれるため、ACP に渡すプロンプト本文の内容や注入順序を調べる際の起点となる。

## Read this when
- ACP が agent に渡すプロンプト本文をどの部品から作るか、または標準プロンプト群の責務分担を把握したいとき。
- oracle file、realization file、ファイルアクセス制約、INDEX.md ルーティング、レビュー所見基準、INDEX エントリー生成規範などをプロンプトとしてどう表現しているか確認したいとき。
- 新しい標準プロンプト種別を追加する、既存 standard の文面を変更する、または完全プロンプトへの組み込み条件や順序を調整したいとき。
- ACP のプロンプト生成で、作業目的・制約・規範・追加プロンプトがどのように構造化文書列へ分解されるかを追いたいとき。

## Do not read this when
- ACP の通信処理、外部 agent 呼び出し、CLI サブコマンド実行、状態管理など、生成済みプロンプトを使う側の実装を調べたいとき。
- oracle file や realization file の個別仕様本文そのものを読みたいだけで、プロンプト部品としての標準文面や組み立て処理を確認する必要がないとき。
- 構造化文書、Standard、Requirement などの共通データ型や整形処理そのものを調べたいとき。
- テストや個別機能の実装挙動を確認したいときで、ACP 向けプロンプト本文の生成に関係しないとき。

## hash
- 1eebf6d29025aed961d2c7757adc689643c660039b80c1ab7ff60cabf31b07d8
