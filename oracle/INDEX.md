# `doc`

## Summary
- cmoc の正本仕様ドキュメントを収録するディレクトリ。アプリケーション仕様、branch・commit・worktree モデル、不採用案、開発規約などを扱い、機能仕様や開発ルールを確認するための入口となる。
- app_spec は CLI 補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run/session、サブコマンドの仕様を扱う。branch_model.md は session・run の分岐、branch・commit・worktree の関係とライフサイクルを定義する。considered_alternative は不採用となった作業方式・検査方式・状態管理方式の検討記録を扱う。dev_rule は Python 実装、CLI 設計、開発環境、pytest 検証に関する開発規約を扱う。

## Read this when
- cmoc の正本仕様ドキュメントの所在を特定したいとき。
- CLI や session/run、branch・commit・worktree、開発環境・設計・テスト規則などの仕様を調査するとき。
- 不採用案の背景や現行設計との違いを確認するとき。

## Do not read this when
- 特定機能の詳細仕様が判明しており、対応する仕様本文を直接確認できるとき。
- 既存 realization 実装の詳細だけを調査したいとき。
- INDEX.md の読み方やルーティング方針自体を確認したいとき。

## hash
- 6d5ad19d05079b824223d1d2d9f5af47a36533f91b4bb8020c146994c733a09c

# `src`

## Summary
- `oracle/src` は、cmoc の正本ソースを集約する入口です。
- `oracle/acp_builder` は、各種 agent call・TUI・レビュー・fork 用パラメータと Structured Output schema を扱います。
- `oracle/other` は、設定、パス解決、規範データ構造、構造化 Markdown の基盤を扱います。
- `oracle/prompt_builder` は、完全なプロンプト構築と、アクセス規則・標準規則・ルーティング規則などの注入部品を扱います。

## Read this when
- cmoc の正本実装や Structured Output schema の定義箇所を特定するとき。
- agent call、TUI、oracle review、realization の fork 処理に対応する正本ソースを調査するとき。
- 設定値、パスモデル、構造化文書、完全なプロンプト生成や注入規則を調査するとき。

## Do not read this when
- CLI の具体的な実行経路や入出力処理だけを調査するとき。
- oracle/doc の自然言語仕様、oracle/test のテスト、または realization 側の実装を直接調査するとき。
- 個別のプロンプト本文や標準規則の内容だけを確認する場合は、該当する下位ディレクトリを直接読むとき。

## hash
- bb980daff461288cf45247499c8374d1f8e35bce6358b4d3364fef7c2ff48e52
