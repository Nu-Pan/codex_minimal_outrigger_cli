# `doc`

## Summary
- cmoc の人間向け正本仕様ドキュメント群への入口。アプリケーション仕様、サブコマンド、oracle/realization の境界、実行・ログ・状態管理、開発規約とテスト規約を扱う。
- `app_spec` は cmoc の機能仕様とサブコマンド仕様、`dev_rule` は実装・開発環境・テストの規約、`branch_model.md` はブランチモデルを確認するための下位入口。
- 代替案や設計判断の履歴を調べる場合は `considered_alternative` 配下へ進む。

## Read this when
- cmoc の仕様全体から、確認すべき仕様領域や下位ドキュメントを判断するとき。
- アプリケーション挙動、サブコマンド、開発規約、テスト規約、ブランチ運用の正本を探すとき。
- 実装やテストの確認に先立ち、人間意図として定義された仕様の入口を確認するとき。

## Do not read this when
- 対象となる具体的な仕様領域やサブコマンドが既に分かっており、`app_spec` または `dev_rule` 配下の個別文書を直接読むべきとき。
- 実装コードや realization test の具体的な挙動だけを確認したいとき。
- 過去の代替案・設計判断だけを調べる場合は、`considered_alternative` 配下を直接読むべき。

## hash
- 5dd3760340ffae73c86fddc654377428ca1e732cd75dead921af460607942676

# `src`

## Summary
- cmoc の正本ソース実装を構成する Python モジュール群と Structured Output スキーマを収めるディレクトリ。
- エージェント呼び出しのパラメータ、フィードバック処理、インデックス生成、セッション・TUI 起動などの呼び出し定義を扱う。
- プロンプト構築、ファイルアクセス、oracle／realization、routing、feedback などの規定文面と、パス・構造化文書・設定モデルを提供する。

## Read this when
- cmoc の正本実装として、エージェント呼び出しやプロンプト生成の具体的な構成を確認するとき
- oracle／realization の扱い、ファイルアクセス境界、routing や feedback 処理の実装上の詳細を調べるとき
- Structured Output のスキーマと、それを利用する呼び出しパラメータ構築の対応を確認するとき

## Do not read this when
- 意味仕様や人間意図の正本を確認する場合は oracle/doc を直接読むとき
- テストケースや検証用 fixture を確認する場合は oracle/test を直接読むとき
- 生成済み realization 実装の挙動だけを調べる場合は src を直接読むとき
- 対象が単一の下位機能に限定され、その下位ディレクトリの実装へ直接進めるとき

## hash
- 38575df0f4d9ca2e8ea90d8cec0577603214ac1af26d9b3679376d45c6c77ce8
