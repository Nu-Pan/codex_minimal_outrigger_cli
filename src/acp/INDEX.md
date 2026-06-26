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
- AI agent に渡すプロンプトを構成する標準部品群を扱う領域。ファイルアクセス制約、INDEX.md ルーティング規則、oracle/realization の基本概念、各種標準文書、レビュー基準、最終プロンプト組み立てを、それぞれ構造化文書として生成する実装がまとまっている。
- agent call 用プロンプトにどの規範・制約・補助説明を含めるかを調べる際、個別の標準文書本文と、それらを組み合わせる入口へ進むための起点となる。

## Read this when
- ACP へ渡すプロンプト本文の構成要素、標準文書、ファイルアクセス規則、ルーティング規則の生成処理を探しているとき。
- oracle file、realization file、INDEX.md、レビュー基準などに関する共通規範を、agent prompt としてどのように文章化しているか確認したいとき。
- 標準プロンプトの有効化フラグや依存関係により、どの補助プロンプトが最終プロンプトへ追加されるかを確認・変更したいとき。
- agent に提示されるレビュー判断基準、実装品質基準、oracle/realization の責務境界、読み書き制約の文面を調整したいとき。

## Do not read this when
- ACP の通信処理、agent 呼び出し処理、StructDoc の基盤データ構造や整形処理そのものを調べたいとき。
- 個別サブコマンド、path model、永続状態、CLI 引数、出力 schema などの具体的なプロダクト挙動を探しているとき。
- 実装やテストの一般的な追加・修正を行うだけで、agent prompt に含まれる標準文書や制約文を確認する必要がないとき。
- 既に読むべき個別の標準プロンプト部品が特定できており、この階層全体の入口情報が不要なとき。

## hash
- a53ecc9b8bf05b006cb6929255ed035bf3ceefd0f7947f682c040fc92288d2a0
