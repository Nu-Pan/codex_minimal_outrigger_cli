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
- AI agent に渡す ACP プロンプトを構成する部品群を扱う実装領域。ファイルアクセス規則、INDEX.md を使ったルーティング規則、oracle file と realization file の基本概念、oracle/realization/review/INDEX エントリー向け標準、完全なプロンプト列への組み立てをそれぞれ構造化文書として生成する。
- 個別の標準本文を生成する部品と、それらを agent call 用の完全なプロンプトへ含める制御の入口が集まっており、AI に提示する作業規範や読み書き制約の文面を確認・変更する際の起点になる。

## Read this when
- AI agent に渡すプロンプト全体の構成、含める部品の順序、標準プロンプト間の依存関係を確認・変更したいとき。
- ファイルアクセス制約、INDEX.md ルーティング規則、oracle/realization の概念説明を ACP 向けプロンプトとしてどう生成しているか確認したいとき。
- oracle file、realization file、oracle review、oracle 適用レビュー、INDEX.md エントリー生成に関する標準文書の本文を生成・調整したいとき。
- 新しい標準プロンプト種別を追加し、既存の構造化文書生成や完全プロンプトへの注入条件に合わせたいとき。

## Do not read this when
- 生成されたプロンプトを受け取った後の agent 実行、CLI サブコマンド処理、外部プロセス呼び出しの流れを調べたいとき。
- StructDoc、Standard、Requirement などの共通データ構造や整形処理そのものを確認したいとき。
- path alias や root path の解決仕様を確認したいだけで、プロンプト文面への埋め込み処理を扱わないとき。
- 個別の CLI 挙動、状態ファイル形式、入出力 schema、テスト実装など、プロンプト標準ではない機能仕様や実装詳細を探しているとき。

## hash
- a6d6b2764f86d003379a36bf932bbcc2c041f3be28eb8a6f97411682df74886a
