# `join`

## Summary
- 対象ディレクトリは、`session join` 中に検出された競合ファイルを解消するためのエージェント呼び出し設定を扱う。競合パスの解決、専用プロンプト、最高品質のモデル・推論設定、リポジトリへの書き込み権限、作業ディレクトリ、および indexing preflight 制御をまとめる実装への入口である。

## Read this when
- `session join` の merge conflict 解消エージェントの呼び出し条件、プロンプト、モデル・推論設定、権限、作業ディレクトリ、または indexing preflight 制御を変更・確認するとき。

## Do not read this when
- 通常の `session join` 処理や競合検出ロジックだけを確認するときは、まずそれらの処理実装を読む。
- 共通のプロンプト構築仕様や agent call パラメータ型を確認するときは、対応する共通実装を直接読む。

## hash
- b88b350444d676036d8aa38021e693c37e14848ca63f8534499168c62fbbd4a6
