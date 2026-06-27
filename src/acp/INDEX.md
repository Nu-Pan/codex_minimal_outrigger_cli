# `builder`

## Summary
- 対象ディレクトリ直下の本文から責務境界を確認し、既存の `INDEX.md` には触れずにルーティング用の意味情報だけを抽出します。

## Read this when
- `src/acp` 配下で、各機能が AI エージェントへ渡す呼び出しパラメータ、complete prompt、モデル・reasoning、file access mode、Structured Output schema の組み立てを確認したいとき。
- apply fork、indexing、oracle review、session conflict 解消、TUI parameter resolve などの処理で、呼び出し側がどのような役割・制約・補助入力・出力契約を AI に渡しているかを追いたいとき。
- 個別ワークフローの実行処理ではなく、そのワークフロー内の AI 呼び出し条件やプロンプト設計を変更・検証したいとき。

## Do not read this when
- AI 呼び出し後の実処理、CLI サブコマンドの配線、git 操作、ファイルシステム更新、状態管理、結果の保存・表示・適用制御を調べたいとき。
- complete prompt 構築、Markdown rendering、StructDoc、path model、file access mode、AgentCallParameter などの共通基盤そのものを調べたいとき。
- 個別の正本仕様断片や realization file の本文をレビュー・修正したいだけのとき。
- INDEX.md 全体の走査・更新・保存、生成済みエントリーの markdown 描画、またはルーティング文書一般の規約を確認したいとき。

## hash
- 4b572409891af96399d79264a0bc36bf3b794fc7e2b9f4ff24fa6957373fc218

# `prompt_parts`

## Summary
- AI agent に渡す prompt part 群を置くディレクトリであり、oracle/realization の基本概念、ファイルアクセス規則、ルーティング規則、各種 standard、review 判定基準、完全プロンプト組み立てを扱う。
- 各対象は StructDoc として渡すための標準文書または基本文書を構築し、agent call 用プロンプトへ注入される規範・制約・前提知識の入口になる。
- 個別の標準文言を確認する場合は該当する構築対象へ、複数の prompt part をどう組み合わせるか確認する場合は完全プロンプト構築側へ進むための階層である。

## Read this when
- AI agent に渡す基本情報、制約、ルーティング規則、standard、review 判定基準などの prompt part がどこで構築されているか探したいとき。
- oracle file、realization file、INDEX エントリー、レビュー所見、ファイルアクセス規則など、複数種類の標準プロンプトの責務分担を比較して読む先を選びたいとき。
- agent call 用の完全なプロンプトへ、どの標準プロンプト片が含まれ、どの条件で注入されるかを調べたいとき。
- 標準文書の本文を変更する前に、対象が oracle standard、realization standard、review standard、routing rule、file access rule のどれに属するか切り分けたいとき。

## Do not read this when
- 個別 CLI コマンド、状態ファイル、パス解決、入出力 schema など、プロンプト本文ではなくプロダクト挙動の実装詳細を調べたいとき。
- StructDoc、Standard、Requirement などの基礎データ構造や、文書変換の汎用処理そのものを確認・変更したいとき。
- 特定の oracle file や realization file の内容、または実際のレビュー対象ファイルの差分を確認したいだけのとき。
- ファイルアクセスモードやパスキーワードの定義など、prompt part が参照する基礎概念の型・モデルを確認したいとき。

## hash
- 603edd63c65145eec68ee83c1d99ae5ad3eb13be6df4a826f8921e393973768f
