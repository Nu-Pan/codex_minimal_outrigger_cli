# `doc`

## Summary
- cmoc の正本仕様ドキュメント群。開発規則、アプリケーション仕様、サブコマンド仕様、branch model、採用しなかった代替案を分けて扱う。
- dev_rule は開発環境、設計、コーディング規則、テスト実装・実行手順を定めるため、実装方法や検証方法を確認する入口となる。
- app_spec はファイル分類、セッション、run isolation、Codex 呼び出し、ログ、feedback、indexing など cmoc のプロダクト挙動を定める中核仕様で、サブコマンドごとの詳細仕様も配下に整理されている。
- branch_model は session と run の branch、commit、worktree の関係を定義し、Git 上のライフサイクルや差分の扱いを確認する入口となる。
- considered_alternative は不採用とした設計案とその判断理由を記録する補足資料で、現行仕様そのものではなく、設計判断の背景を調べる場合に参照する。

## Read this when
- cmoc の正本仕様全体の構成や、どの仕様領域から確認を始めるべきか判断したいとき。
- 開発規則、プロダクト挙動、Git の branch model、または不採用案の判断理由を調べるとき。
- 特定のサブコマンド仕様へ進む前に、共通する app_spec の前提を確認したいとき。

## Do not read this when
- 特定のサブコマンド、開発規則、またはアプリケーション機能の詳細だけを確認したいときは、対応する下位文書を直接読む。
- 実装やテストの具体的なコードを調べるときは、oracle/src または test 配下を読む。
- INDEX の更新手順や対象ファイルの一覧だけが必要なときは、このディレクトリ全体を読む必要はない。

## hash
- 9be9100eab53e8abc03af4162427fa7472335dd9a5c985bee7c12eff4c622322

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
