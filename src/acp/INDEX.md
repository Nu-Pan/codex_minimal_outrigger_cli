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
- AI agent に渡すプロンプトを構成する標準文書・基本説明・作業規則を、構造化文書として組み立てる prompt part 群を扱う。
- oracle file と realization file の基本概念、oracle/realization の品質基準、レビュー所見の判定基準、INDEX.md ルーティング規則、ファイルアクセス制約、完全な agent prompt の組み立てを確認する入口となる。
- 個別機能の CLI 挙動ではなく、agent へ提示する共通規範や標準プロンプト断片の生成責務を探すときのまとまりである。

## Read this when
- agent call に渡すプロンプト全体の構成や、標準プロンプト群がどの条件で追加されるかを確認したいとき。
- oracle file と realization file の責務境界、またはそれぞれに適用する共通規範の文面生成を確認・変更したいとき。
- oracle review や oracle-to-realization review で、どの問題を所見として扱うか、fatal/minor や仕様不整合の境界を確認したいとき。
- INDEX.md を使った読み進め方、INDEX.md エントリーの品質基準、またはルーティング文書生成に関する標準プロンプトを確認したいとき。
- 作業ルート、oracle、memo、リポジトリ全体などに対するファイルアクセス禁止条件が、各アクセスモードでどのようなプロンプト文面になるかを追いたいとき。

## Do not read this when
- 特定サブコマンド、path model、状態ファイル、出力 schema など、個別機能の仕様や実装詳細を探しているとき。
- 標準プロンプトの本文ではなく、agent 呼び出し基盤、構造化文書型、永続状態、CLI 引数処理そのものを調べたいとき。
- 実装やテストの一般的な変更対象がすでに個別ファイルに絞れており、共通規範プロンプトの生成内容を確認する必要がないとき。
- oracle file の正本仕様断片そのものや、個別の製品仕様を確認したいときは、このまとまりではなく該当する oracle 本文を読む方が直接的である。

## hash
- 187ae8dcbe1c97fb1fec2c03e08caf6932ce841df19a1b5fd75d39e1af0ec0e2
