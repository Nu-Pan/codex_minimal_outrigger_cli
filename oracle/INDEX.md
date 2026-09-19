# `doc`

## Summary
- cmoc の正本仕様を、製品挙動、サブコマンド、開発規約、採用しなかった設計案に分けて収録する文書群。
- app_spec はセッション、run、agent 呼び出し、feedback、oracle/realization、ログなどの現行仕様を扱い、配下の sub_command は各 CLI サブコマンドと編集 run の仕様への入口となる。
- dev_rule は開発環境、設計、コーディング、テスト実装、検査実行の規約を扱う。
- considered_alternative は現行仕様ではなく、採用しなかった方式の判断理由や代替方針を確認するための記録である。

## Read this when
- cmoc の現行の製品仕様や CLI の挙動を確認・改訂するとき
- 特定のサブコマンド、セッション、編集 run、feedback、oracle/realization の仕様を調べるとき
- 実装・テストの設計方針、コーディング規約、検査手順を確認するとき
- 採用されなかった設計案の背景や、現行方式を選んだ理由を確認するとき

## Do not read this when
- 仕様ではなく、現在の実装コードやテストコードの具体的な挙動だけを確認したいとき
- 既に対象の仕様領域やサブコマンドが特定できており、その配下の文書を直接読めるとき
- 一般的な開発手順だけを確認したい場合に、製品仕様全体を読む必要がないとき
- 採用されなかった設計案の経緯を必要とせず、現行仕様だけを実装・検証するとき

## hash
- 4f750ff34be04dbceb7a8d1cc5b5cdc50abcfd4b68c4124bd06fdc78a082e975

# `src`

## Summary
- cmoc の agent 呼び出しパラメータを定義する層で、アクセスモード、作業 prompt、Structured Output schema、実行コンテキストをまとめる。
- feedback、INDEX エントリー生成、oracle 編集・調査・レビュー、realization の適用・リファクタリング、TUI、セッション結合など、用途別の agent call builder と schema を収録する。
- prompt_builder 配下では完全 prompt の合成と、ファイルアクセス、oracle/realization、routing、feedback 報告、競合解消などの共通規定を構築する。
- other 配下ではパス・設定・構造化 Markdown のモデルと変換処理を提供し、editor_input_handoff と feedback では外部 handoff 用の入力 schema を定義する。

## Read this when
- agent call の起動条件、prompt の構成、アクセス境界、Structured Output、または実行対象の path context を確認・変更するとき。
- cmoc のサブコマンド別に agent 呼び出しの入力文面や結果 schema の正本実装を調べるとき。
- 共通 prompt policy、placeholder の解決、Markdown 構造化、設定・パスモデルの挙動を確認するとき。

## Do not read this when
- 意味仕様や人間意図の正本を確認したいときは oracle/doc を先に読む。
- realization の実装やテストの挙動だけを確認したいときは src または test の該当対象へ直接進む。
- 特定の一つの agent call の詳細だけが必要な場合は、このディレクトリ全体ではなく対応する acp_builder 配下のファイルと schema を直接読む。

## hash
- d44cc3463836d0c07a528fb994e662bf4aa103fdb8767b2bc90feac49e6d2767
