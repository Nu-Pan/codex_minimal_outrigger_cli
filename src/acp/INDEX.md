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
- ACP 向けに agent prompt の部品を構築する実装群を収める領域。ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、各種 standard、レビュー規範、INDEX.md エントリー生成規範などを StructDoc として組み立てる。
- 完全プロンプトの組み立てでは、基本情報・アクセス制約・ルーティング規則・追加プロンプト・標準プロンプト群を依存関係込みで注入し、agent に渡す前の表現サニタイズも扱う。
- 個々のプロンプト部品の文言や、標準プロンプトを有効化したときに agent へ渡される前提規則を確認・変更するための入口となる。

## Read this when
- ACP が agent に渡す prompt の構成要素として、どの規則文・標準文・レビュー規範が生成されるかを確認したいとき。
- ファイルアクセス規則、INDEX.md を使った読み進め方、oracle file と realization file の責務境界、oracle/realization の品質基準を prompt 部品として変更したいとき。
- oracle review、oracle と realization の照合レビュー、INDEX.md エントリー生成など、agent に渡す判断基準の文面や StructDoc 生成処理を確認・変更したいとき。
- 標準プロンプト群を完全プロンプトへ組み込む際の依存関係、追加位置、root token や内部表現の置換処理を追いたいとき。

## Do not read this when
- 個別の CLI サブコマンド、path model、状態ファイル、実行フローなど、prompt 文面ではなく cmoc の具体機能仕様や実装を調べたいとき。
- StructDoc、StructCodeBlock、Standard、Requirement、FileAccessMode、RootToken などの基盤データ構造や列挙値そのものを確認したいとき。
- oracle file や realization file の本文そのものを編集・レビューしたいだけで、agent prompt に載せる標準文の生成元を確認する必要がないとき。
- 生成済み prompt をどの agent プロセスへ渡すか、実際の ACP 呼び出し制御や外部プロセス管理を追いたいとき。

## hash
- d77f48d02eff94645635cd416a450121013ca3798b191787a253b0f8efab7fcf
