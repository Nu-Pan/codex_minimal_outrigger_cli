# `fork`

## Summary
- refactor fork の変更要約およびファイル単位レビュー・修正に関する構造化出力スキーマと AgentCallParameter 定義を扱うディレクトリ。変更差分の要約形式、レビュー結果の記録形式、各処理を起動する prompt・権限・検証条件の定義への入口となる。

## Read this when
- refactor fork の変更差分を要約する出力契約を確認・変更するとき
- ファイル単位のレビュー・修正結果の出力契約を確認・変更するとき
- 変更要約またはレビュー・修正 agent call の prompt、実行条件、Structured Output 設定を確認・変更するとき

## Do not read this when
- 実際の変更差分やレビュー対象ファイルの実装内容を調査するとき
- レビュー結果のフィールド定義だけを確認する場合は、対応する JSON スキーマを直接読む
- refactor fork 以外の agent call 構築や realization 実装を調査するとき

## hash
- cd5a3a5bc5b574a073b75e0069d3e2b8e62f6a6e5697adaf761fac8ce0159a28
