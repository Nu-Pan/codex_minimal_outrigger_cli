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
- AI agent に渡す構造化プロンプトの部品群を実装する領域。基本情報、ファイルアクセス規則、ルーティング規則、oracle・realization・review・INDEX.md エントリーに関する標準文書を StructDoc として組み立てる。
- 個別の標準プロンプトを生成する関数と、それらを依存関係込みで完全な agent prompt にまとめ、root token などの内部表現を agent 向け文面へ置換する処理への入口になる。

## Read this when
- agent 呼び出しに渡されるプロンプト全体の構成、標準プロンプトの注入条件、追加プロンプトの差し込み位置を確認したいとき。
- ファイルアクセス制約、INDEX.md を使った読み進め方、oracle file と realization file の基本説明を、agent prompt としてどの文面で生成しているか確認・変更したいとき。
- oracle file の書き方、realization file の保守性、oracle review、oracle と realization の照合 review、INDEX.md エントリー生成に関する規範文書の生成元を探しているとき。
- 複数の標準プロンプトを有効化した際に、どの前提説明や関連標準が連動して含まれるかを確認したいとき。
- agent へ渡す前のプロンプトから内部の root token や呼び出し元表現を除去・置換する処理を確認したいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、path model、実行フローなど、プロンプト文書の生成ではない個別機能の仕様や実装を調べたいとき。
- StructDoc、StructCodeBlock、Standard、Requirement、読み書きモード列挙値、root token 解決など、プロンプト部品が利用する基盤データ構造や型定義そのものを確認したいとき。
- 生成されたプロンプトを実際にどのプロセスへ渡すか、agent 実行をどう制御するかを追いたいとき。
- 個別の標準文書や規則文書だけを確認・変更したいことが明確で、すでに該当する下位対象へ直接進めるとき。

## hash
- c90f4f904614e9317d410db061555183549d136164794f8acd1cd582e317bb77
