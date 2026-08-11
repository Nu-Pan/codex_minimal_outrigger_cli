# `fork`

## Summary
- refactor fork の変更要約およびファイル単位レビュー・修正に関する AgentCallParameter と、各処理の構造化出力スキーマを扱う領域。変更要約・レビュー修正の agent call 構築から、対応する schema 定義へ進むための入口。

## Read this when
- refactor fork の変更要約 agent call の起動条件、prompt、実行設定、作業ディレクトリを確認するとき
- ファイル単位レビュー・修正 agent call の prompt、アクセス権、モデル設定、検証要求を確認するとき
- 変更要約またはレビュー結果の構造化出力項目・契約を確認するとき

## Do not read this when
- refactor fork の実際のコード変更や差分生成処理を調べるとき
- 一般的な prompt 構築規則や refactor と無関係な agent call を調べるとき
- レビュー対象ファイルの実装内容や個別の所見を確認するとき

## hash
- 6f0fdb27929de52aac51f9502f5a0cc9750325c4fba48a79027c7a4fad52d9d1
