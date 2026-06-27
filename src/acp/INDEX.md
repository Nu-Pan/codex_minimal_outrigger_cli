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
- AI agent に渡すプロンプト断片を構築する実装群をまとめる領域。oracle・realization の基本概念、ファイルアクセス制限、INDEX.md ルーティング規則、各種レビュー規範、oracle/realization/INDEX エントリー作成規範、完全プロンプトの組み立てを扱う。
- 個々の標準や規則は StructDoc 化され、agent call 用の完全なプロンプトへ注入される前提で分かれているため、prompt 全体の構成確認と、特定の標準プロンプト本文の確認・変更への入口になる。

## Read this when
- agent call 用プロンプトに含める基本情報、アクセス制限、ルーティング規則、標準規範、追加プロンプトの構成や結合順序を確認・変更したいとき。
- oracle file、realization file、review、INDEX.md エントリーなどに関する標準プロンプト本文をどのように生成しているか調べたいとき。
- 標準プロンプト片の注入条件や依存関係を変更し、必要な前提情報が完全プロンプトへ含まれるようにしたいとき。
- AI に提示する規範文書として、所見列挙基準、oracle 記述基準、realization 品質基準、INDEX.md ルーティング基準、ファイルアクセス制約のいずれかを確認したいとき。

## Do not read this when
- 個別 CLI 機能、状態ファイル、パス解決、コマンド実行、入出力 schema など、プロンプト断片以外のプロダクト挙動を調べたいとき。
- StructDoc、Standard、Requirement などのデータ構造や、構造化文書変換の共通実装そのものを確認・変更したいとき。
- 特定の oracle file や realization file の本文内容をレビューしたいだけで、レビューや標準プロンプトの判断基準はすでに分かっているとき。
- 実装テストや補助ファイルの保守、外部依存、公開 CLI 面の変更など、realization code 全般の作業方針だけを調べたいとき。

## hash
- 81d010c7aba08e3a0a04d0d38602eb90b2e781db9d7454a215d81f7d8ef49bae
