# `fork`

## Summary
- refactor fork 配下の変更要約・ファイルレビュー修正に関する Structured Output schema と、そのための agent call 構築定義をまとめたディレクトリ。変更要約の出力契約、レビュー結果の出力契約、各処理の prompt・実行条件を確認する入口となる。

## Read this when
- 変更差分を意味論的カテゴリ別に要約する出力形式や必須項目を確認するとき
- ファイル単位のレビュー・修正 agent call の prompt、アクセス範囲、実行設定、検証条件を確認・変更するとき
- レビュー結果に必要な根拠、変更パス、仕様との関係、対応状態を確認するとき

## Do not read this when
- 実際の変更差分やレビュー対象ファイルの実装内容を調査するとき
- レビュー・修正処理そのものの実装ではなく、変更要約の生成ロジックだけを確認したいとき
- refactor fork 以外の agent call 構築定義を直接調査するとき

## hash
- 155fa733168e7aba9205c22d1ba5508d5e5c025b33dd9eeb9301cd799d42b2d5
