# `builder`

## Summary
- AI エージェント呼び出しパラメータを組み立てる builder 群をまとめた領域。apply、indexing、review、session、tui などの用途ごとに、role・summary・goal・補助 prompt・ファイルアクセス制約・モデル設定・reasoning effort・Structured Output schema を結び付ける実装への入口になる。
- 正本仕様レビュー、実装差分レビュー、ルーティング文書エントリー生成、merge conflict marker 解消、TUI 実行前のパラメータ解決など、各サブタスクを AI に依頼するための prompt 内容と構造化出力契約を確認する起点となる。

## Read this when
- cmoc の各機能が、どのような条件・権限・モデル・出力 schema で補助 AI エージェントを呼び出すかを確認または変更したいとき。
- apply 後の差分要約、realization file 所見列挙、検出済み所見への修正依頼など、apply 系の後段エージェント呼び出しを追いたいとき。
- ルーティング文書用エントリー生成で、対象本文を根拠にした prompt、読み取り専用条件、効率モデル、structured output の指定を確認したいとき。
- oracle レビューで、新規所見列挙、理由調査、採否判定、所見整理を AI に依頼する各段階の呼び出し内容を確認したいとき。
- session join の merge conflict marker 解消や、TUI 実行前のファイルアクセスモード・標準参照要否判定に関するエージェント呼び出しを確認したいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、結果の保存・表示、git 操作、フォーク作成・統合など、AI 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、apply review standard、realization standard、INDEX.md エントリー標準など、prompt に組み込まれる標準本文そのものを読みたいとき。
- AgentCallParameter、prompt 部品、Markdown レンダリング、構造化ドキュメント、パス解決 helper、JSON Schema 読み込みなど、複数用途で共有される基盤実装を調べたいとき。
- 実際のレビュー判断基準、カテゴリ分け、git diff 生成、merge conflict marker 検出、TUI 表示や対話処理など、個別サブタスクのドメインロジック本体を調べたいとき。
- 生成済みの INDEX.md 内容の評価や、特定ファイルを実際に読むべきかどうかのルーティング判断だけをしたいとき。

## hash
- b352eddb93cfdc1a6bfd2e2cc39dc542e1fcabee8ef7964642e7214992b0641f

# `prompt_parts`

## Summary
- AI agent に渡すプロンプトを構成する部品群を扱うディレクトリ。ファイルアクセス規則、ルーティング規則、oracle/realization の基本説明、oracle・realization・レビュー・INDEX.md エントリーの標準文書を構造化文書として組み立てる実装がまとまっている。
- 個別の標準文書本文を生成する部品と、それらを依頼内容・アクセスモード・追加プロンプト・有効化フラグに応じて完全な agent 用プロンプトへ集約する入口がある。

## Read this when
- AI agent に渡す最終プロンプトの構成、標準文書の注入順序、または有効化フラグ間の依存関係を確認・変更したいとき。
- ファイル読み書き制約、INDEX.md を使った読み進め方、oracle file と realization file の責務境界を、agent 向けプロンプトとしてどの文面で提示しているか確認したいとき。
- oracle file、realization file、oracle review、oracle-to-realization review、INDEX.md エントリー生成に関する標準文書の生成内容を確認・変更したいとき。
- 標準文書を構成する要求・背景・判断例が、どの構造化文書として agent prompt に組み込まれるかを追いたいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、path model、入出力 schema などの個別機能仕様や実装詳細を探しているとき。
- 標準文書を利用する側ではなく、構造化文書型、標準項目型、またはそれらの変換基盤そのものを確認したいとき。
- テスト実装や fixture の内容を確認したいとき。
- INDEX.md エントリーの完成文面だけが必要で、対象本文をすでに直接読める状態にあるとき。

## hash
- ac07129c880ae3dc8b3364000026c106640eb98405ec3b2a163479f01af1c160
