# `doc`

## Summary
- cmoc の人間所有の正本仕様ドキュメント群。app_spec は CLI の利用方法、実行ライフサイクル、agent 呼び出し、feedback、INDEX、oracle/realization、各サブコマンドの振る舞いを定義する。
- branch_model.md は cmoc が管理する branch・commit・worktree の概念と関係を定義する。
- considered_alternative は採用しなかった設計案と、その判断理由を記録する。
- dev_rule は実装設計、開発環境、コーディング、テスト実装、テスト実行に関する開発規約を定義する。

## Read this when
- cmoc の正本仕様、CLI の挙動、状態遷移、agent 連携、feedback 処理を確認するときは app_spec から読む。
- branch や worktree の意味、命名、commit の関係を確認するときは branch_model.md を読む。
- 実装・テストの開発規約や検証手順を確認するときは dev_rule から読む。
- 過去に検討されたが採用されなかった設計判断の理由を確認するときは considered_alternative から読む。

## Do not read this when
- 現在の実装や設定の挙動を確認したいときは src を読む。
- テストコードやテスト fixture の具体的な検証内容を確認したいときは test を読む。
- 特定の仕様文書が既に分かっている場合は、このディレクトリ全体ではなく該当する文書を直接読む。

## hash
- 1e7c6caf1e3db663ed74333b357c9d1f0ebbc50d60fad9d6244bcf82784a1fc3

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
