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
- AI agent に渡すプロンプトを構成する標準文書・規則文書の断片を生成する実装群をまとめるディレクトリ。
- oracle / realization の基本概念、file access rule、routing rule、各種 standard、review standard、index entry standard などを StructDoc として組み立て、完全な agent prompt の部品または統合処理への入口になる。
- 個別のプロンプト断片の本文内容を確認する場合は各生成元へ進み、最終プロンプト全体の組み立て順序や標準プロンプト間の依存関係を確認する場合は完全プロンプト構築処理へ進むためのまとまりである。

## Read this when
- ACP 経由で agent に渡すプロンプトの文面や標準規範がどこで生成されるかを調べたいとき。
- oracle file、realization file、review、apply review、routing、file access、index entry などの標準プロンプト部品を確認・変更したいとき。
- 複数の標準プロンプト断片がどのように最終的な agent prompt に含まれるか、または root token 置換などの仕上げ処理を追いたいとき。
- AI agent の作業前ルール、読む対象の選び方、レビュー所見の基準、実装・仕様文書の品質基準をプロンプトとして生成する箇所を探しているとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、path model、agent 実行制御など、プロンプト部品ではない具体的な機能実装を調べたいとき。
- StructDoc、Standard、Requirement などの構造化文書データ型やレンダリング基盤そのものを確認したいとき。
- oracle file や realization file の個別本文の仕様内容を読みたいだけで、agent に提示する標準文書の生成処理を確認する必要がないとき。
- テストコード、外部コマンド実行、LLM 呼び出し、サブプロセス管理など、生成済みプロンプトを利用する側の処理を追いたいとき。

## hash
- b0162cb9ec1dff590eb958f7a80c22594f30bf752d42738576f81a2f0920a780
