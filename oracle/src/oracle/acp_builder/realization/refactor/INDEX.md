# `fork`

## Summary
- refactor fork における変更要約とファイル単位レビュー・修正の agent call 定義、および各処理の Structured Output schema をまとめたディレクトリ。変更差分の要約形式を確認する場合は change_summary.json、要約 call の起動条件や prompt を確認する場合は change_summary.py、レビュー・修正結果の契約は file_review_and_fix.json、レビュー・修正 call の構築は file_review_and_fix.py が入口となる。

## Read this when
- refactor fork の変更差分要約、ファイル単位レビュー、修正処理の prompt・実行パラメータ・構造化出力契約を調査または変更するとき。

## Do not read this when
- 変更要約やレビュー結果の項目定義だけを確認したい場合は、各処理に対応する JSON schema を直接読む。
- レビュー対象の実装内容や個別仕様、実際の変更差分を調査する場合は、このディレクトリではなく対象 realization file や raw git diff を直接読む。
- 一般的な prompt 構築、パス解決、構造化文書レンダリングの共通実装だけを調査する場合は、対応する共通実装を直接読む。

## hash
- ed61a389e93fa55b396185b8d4dae063e733f651e78d1fdc9867f92889dfe2ee
