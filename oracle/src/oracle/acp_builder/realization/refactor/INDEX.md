# `fork`

## Summary
- 変更要約とファイル単位レビュー・修正を行う agent call の oracle source および、それぞれの Structured Output schema を扱うディレクトリ。変更要約の出力形式を確認する場合は change_summary.json、prompt 構成や実行設定を確認する場合は change_summary.py を入口にする。ファイル単位レビューの出力形式は file_review_and_fix.json、レビュー・修正 prompt や検証要件は file_review_and_fix.py から確認する。

## Read this when
- refactor fork の変更要約出力形式や検証項目を確認するとき
- 変更要約 agent call の prompt、入力差分、モデル設定、schema 指定を確認するとき
- ファイル単位レビュー・修正の出力形式を確認するとき
- レビュー・修正 agent call の prompt、対象パス、アクセスモード、モデル設定、検証要件を確認するとき

## Do not read this when
- refactor 差分そのものの内容を確認したいとき
- レビュー対象の realization 実装を調査・修正したいとき
- 特定の Structured Output schema ではない実装挙動を調査したいとき

## hash
- 3eb45a1ba367a4b1519bf3484b3b7744bda84605f15f474f434b396e004913b9
