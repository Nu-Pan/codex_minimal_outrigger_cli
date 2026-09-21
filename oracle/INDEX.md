# `doc`

## Summary
- cmoc の正本仕様を Markdown で定義する文書群。アプリケーション仕様、開発規則、ブランチ運用、および不採用案の記録を、実装・テストの根拠として参照する入口。
- app_spec は CLI サブコマンド、実行状態、ファイル分類、ログ、フィードバック、インデクシングなど、cmoc の利用時の要求と外部挙動を定義する。
- dev_rule は開発環境、設計、コーディング規則、テスト実装、テスト実行手順を定義する。
- branch_model は session・run と Git branch、commit、worktree の対応関係を定義する。
- considered_alternative は採用しなかった設計案とその判断理由を記録し、現行仕様そのものではなく設計判断の背景を確認するための資料である。

## Read this when
- cmoc の要求、外部から観測可能な挙動、状態遷移、CLI の仕様を確認するときは app_spec 配下から読む。
- 実装方針、Python 環境、コーディング規則、テスト要件や検査手順を確認するときは dev_rule 配下から読む。
- session・run の分岐、commit、worktree の関係を確認するときは branch_model.md を読む。
- 現在の仕様ではなく、なぜ別案を採用しなかったのかという設計判断の背景を調べるときは considered_alternative 配下から読む。
- src や test の変更がどの正本仕様に適合すべきかを判断するとき。

## Do not read this when
- 実装の具体的な処理や設定値だけを確認したい場合は、対応する src 配下を直接読む。
- テストケース、fixture、ベンチマーク、または検証コードだけを確認したい場合は、対応する test 配下を直接読む。
- 特定の仕様文書が既に分かっており、その文書だけで目的を満たせる場合は oracle/doc 全体を読む必要はない。
- 不採用案の理由を調べる必要がなく、現行の要求や挙動だけを知りたい場合は considered_alternative を読む必要はない。
- INDEX.md の生成・更新自体を行う場合は、このディレクトリの既存 INDEX.md を参照せず、対象となる実ファイルを直接読む。

## hash
- 6f7943971f23fad0856563e21189f70017a8dce02c888c75c6f8014fe3308793

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
