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
- ACP 経由で agent に渡す標準プロンプト部品を構築する実装群をまとめる領域。ファイルアクセス制約、INDEX.md を使ったルーティング規則、oracle file と realization file の基本概念、oracle・realization・review・INDEX.md エントリーの各標準文書を扱う。
- 個別の標準文書の本文生成だけでなく、複数の標準プロンプトを依存関係込みで最終的な agent 向け構造化プロンプトへ組み立てる入口にもなる。
- agent に提示される作業前提、読み書き制約、レビュー判断基準、実装品質基準、ルーティング文書品質基準の文言や注入条件を確認・変更するための起点である。

## Read this when
- agent に渡される標準プロンプトの構成、順序、依存関係、追加条件、または内部表現の置換処理を確認・変更したいとき。
- ファイル読み書き制約、INDEX.md を使った読み進め方、oracle file と realization file の責務境界を、ACP プロンプトとしてどう文面化しているか確認したいとき。
- oracle file、realization file、oracle レビュー、oracle と realization の照合レビュー、INDEX.md エントリー生成に関する標準文書の生成元を探しているとき。
- 標準プロンプトの文言追加・削除・修正や、標準項目が StructDoc として組み立てられる流れを変更したいとき。
- レビュー所見の根拠、fatal/minor の分類、仕様断片の隙間の扱い、実装品質やテスト肥大化抑制の規範を agent prompt 側から確認したいとき。

## Do not read this when
- 特定サブコマンド、path model、永続状態、CLI 引数、出力 schema などの個別機能仕様や実装詳細を探しているとき。
- 構造化ドキュメント、標準項目、要求項目、root token、基本型などのデータ構造そのものを確認したいだけのとき。
- 生成されたプロンプトをどのプロセスへ渡すか、agent 呼び出しや実行制御の流れを追いたいとき。
- 個別の oracle file や realization file の本文内容を確認したいだけで、標準プロンプトの文言や組み立てを変更しないとき。
- INDEX.md エントリーの実際の文面だけを対象本文から作りたい段階で、標準文書の生成実装を確認する必要がないとき。

## hash
- 604e922425d90f30bec364558475caaae6e7dc605530b56710dfc9471c27d264
