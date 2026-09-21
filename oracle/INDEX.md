# `doc`

## Summary
- cmoc の正本仕様を構成する自然言語文書のルート。アプリケーション仕様、開発規約、ブランチモデル、および採用しなかった代替案への入口を提供する。
- app_spec は CLI の利用者向け挙動、状態管理、ファイルアクセス、agent call、サブコマンドなどの現行仕様を扱う。
- dev_rule は開発環境、設計、コーディング、テスト実装、検査実行に関する開発時の規約を扱う。
- branch_model は cmoc が管理する Git branch と commit の役割・関係を定義する。
- considered_alternative は現行仕様そのものではなく、設計判断で検討した代替案と採用しなかった理由を記録する。

## Read this when
- cmoc の人間管理の正本仕様を探しているとき。
- 実装やテストの変更が、アプリケーション挙動・開発規約・ブランチ運用のどれに関係するか判断するとき。
- 現行設計の背景や、代替案を採用しなかった理由を確認するとき。

## Do not read this when
- 実装の具体的な処理や設定値を直接確認したいときは src 配下を読む場合。
- テストケースや検証コードを直接確認したいときは test 配下を読む場合。
- INDEX.md、作業メモ、Codex の補助設定などの分類対象外ファイルを探しているとき。
- 現行仕様の適用根拠を求めているのに、considered_alternative 配下だけを参照しようとしているとき。

## hash
- 4a32614adf9a29c2d847f0fe5494f991c7ff0ff241898ef3e64a13d4a0b89600

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
