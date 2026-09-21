# `doc`

## Summary
- cmoc の正本仕様ドキュメント群。アプリケーション仕様、サブコマンド仕様、開発規約、ブランチモデル、採用しなかった設計案を定義する。
- app_spec は cmoc の利用者向け機能・状態・入出力・エラー・agent call・feedback・indexing などの現在仕様を扱い、sub_command 配下は各サブコマンドの詳細仕様への入口となる。
- dev_rule は開発環境、設計・コーディング規則、テスト実装規約、テストと品質検査の実行手順を扱う。
- considered_alternative は現行仕様ではなく、採用・不採用判断の背景を確認するための記録である。
- branch_model はリポジトリのブランチ運用モデルを定義する。

## Read this when
- cmoc の正本仕様やサブコマンドの要求を確認するとき
- 実装・テスト・設定が仕様に適合しているか調査するとき
- 開発規約、検証手順、ブランチ運用、feedback や agent call の扱いを確認するとき
- 現行設計が採用された理由や代替案の判断背景を調べるとき

## Do not read this when
- 実装の具体的な現在挙動だけを確認したいときは src 配下を直接読む
- テストコードや fixture の具体的な構成だけを確認したいときは test 配下を直接読む
- 仕様解釈を必要としない補助ファイルや生成ログだけを扱うとき
- 採用判断の背景が不要で、現在の要求だけを確認したいときは considered_alternative 配下へ進まない

## hash
- c9f88bdb394f39adb35b8064ce6db68a03ebd6d0e763ab8b4ddafe6f10c8ec98

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
