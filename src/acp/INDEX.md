# `builder`

## Summary
- AI エージェント呼び出しに渡す AgentCallParameter を、用途別の complete prompt、補助入力、file access mode、model/reasoning、Structured Output schema 参照として組み立てる builder 群をまとめる領域。
- 対象は、apply fork の変更要約・所見列挙・所見対応、indexing の目次エントリー生成、review oracle の所見列挙・検証・採否・整理、session join の conflict marker 解消、TUI の実行パラメータ解決など、AI に何を依頼し、どの制約と出力契約で呼び出すかを定義する処理である。
- 実際の CLI 制御、git 操作、ファイル更新、レビュー結果の保存、目次ファイルの描画や永続化ではなく、各機能が AI 呼び出しへ渡すプロンプトと呼び出し条件を確認するための入口になる。

## Read this when
- cmoc の各機能が AI エージェントを呼び出す際の prompt、補助文脈、アクセス権限、モデル区分、推論量、Structured Output schema の対応関係を調べたいとき。
- apply fork、indexing、review oracle、session join、TUI parameter resolve のいずれかで、AI に渡す作業目的・禁止事項・標準文脈・入力データがどう complete prompt に組み込まれるか確認したいとき。
- 特定フェーズの出力 schema と、その schema を参照する AgentCallParameter 構築処理を対応づけて確認したいとき。
- AI 呼び出しの file access mode が readonly、pure oracle read、realization write などのどれに設定されるか、またその権限が prompt 上の作業範囲とどう対応するかを追いたいとき。
- 新しい AI 呼び出し builder を追加または既存 builder を変更する前に、同種の呼び出し定義の責務分割や schema 参照の置き方を確認したいとき。

## Do not read this when
- CLI サブコマンドの引数解析、実行順序、状態管理、git branch 操作、merge 実行、ファイル列挙、保存、表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- AI が返した構造化結果を実際に適用する処理、レビュー結果や目次情報を永続化する処理、または markdown として描画する処理を調べたいとき。
- complete prompt の共通構築規則、StructDoc や render 処理、path model、AgentCallParameter、FileAccessMode などの基礎型そのものを調べたいとき。
- oracle file、realization file、review standard、apply review standard、index entry standard など、builder が参照する標準文脈の本文や一般規約を読みたいだけのとき。
- 個別の AI 呼び出しではなく、対象コマンドの利用者向け仕様、実際の実装修正箇所、またはテストだけを直接確認したいとき。

## hash
- 2fa7d3217c15a26c90e074c17bfdf5257f83b909cb8438de8523b0f8a4d778ee

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
