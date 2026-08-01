# `fork`

## Summary
- refactor fork における変更要約と単一ファイルレビュー・修正のための Structured Output schema、およびそれらを利用する AgentCallParameter 構築の正本実装を扱う。変更要約では差分のカテゴリ別要約と根拠ファイルを、ファイルレビューでは所見・修正・検証結果を構造化して返す。各ファイルの詳細な schema や prompt 構成、実行条件を確認するための入口となる。

## Read this when
- refactor fork の変更要約出力形式、要約結果の検証項目、根拠ファイル一覧を確認するとき
- 単一ファイルのレビュー・修正 agent に渡す prompt、対象 path の解決、権限、モデル設定、Structured Output schema、作業ディレクトリを確認・変更するとき
- レビュー結果に求める findings、resolution、修正・検証・git 操作の制約を確認するとき

## Do not read this when
- レビュー対象ファイル自体の実装内容や個別の oracle/realization file の仕様を調査するとき
- 変更要約またはファイルレビューの Structured Output schema の詳細だけを確認したいとき
- 一般的な prompt 構築、path 解決、構造化文書レンダリングの実装だけを調査したいとき

## hash
- 47e0b5a5cba29ece724b05362b1c0c64bf018691834d05036b9d1f918eddfa77
