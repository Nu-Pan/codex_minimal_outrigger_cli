# `fork`

## Summary
- realization refactor の変更要約 schema と、その prompt・起動条件を定義する Python builder、ならびにファイル単位レビュー・修正の出力 schema と起動条件を定義する Python builder を扱うディレクトリです。変更要約やレビュー結果の出力形式を確認する入口であり、レビュー対象の realization file や prompt・oracle・path・構造化文書関連実装への導線も提供します。

## Read this when
- realization refactor の変更差分を要約する agent call の出力形式や、カテゴリ別の要約と変更ファイル対応を確認するとき
- refactor fork の変更差分要約 agent call の prompt、入力差分の埋め込み、実行条件を確認・変更するとき
- realization refactor のファイル単位レビュー・修正 agent call の結果、prompt、実行パラメータ、Structured Output schema との整合性を確認するとき

## Do not read this when
- 変更差分の実装内容や分類結果そのものを確認したいとき
- レビュー対象の realization 実装、oracle 要求、共通 prompt 生成処理、パス解決、markdown rendering の仕様を直接確認したいとき
- refactor fork 以外の agent call 種別や別の出力形式を調査するとき

## hash
- 75b5f6dc05d68183731123e7599c50a2f7632b9651a5cd9d854edd9bab01d56c
