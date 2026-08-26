# `apply`

## Summary
- `cmoc realization apply fork` の AgentCallParameter 構築を担うディレクトリ。追従対象の commit 範囲と oracle file の raw git diff を prompt に組み込み、リポジトリ全体の realization file への反映・整合性検証を行う agent call の起動条件を定義する。配下の `fork` 用起動定義へ進む入口となる。

## Read this when
- `cmoc realization apply fork` の prompt、作業範囲、realization write 権限、モデル、推論 effort、linked worktree、ルーティング事前処理を確認・変更するとき。
- oracle file の変更を realization file 全体へ反映する agent call の起動契約を確認するとき。

## Do not read this when
- 通常の realization implementation、realization test、realization ancillary の具体的な実装を変更するとき。
- `fork` 用起動定義の本文を直接確認すれば足りるとき。
- `cmoc realization apply fork` 以外の起動パラメータを確認するとき。

## hash
- dae9a7c63930db5904f198f431a91643a217b52a8ae19aad77af139d8d946d6b

# `refactor`

## Summary
- `fork` は、realization refactor 用の変更要約とファイル単位レビュー・修正に関する agent call builder および Structured Output schema を定義するディレクトリです。変更差分を意味論的カテゴリ別に要約する処理と、指定した oracle file または realization file を起点に所見調査、realization file の修正、検証まで行う処理を扱います。各 agent call の prompt、ファイルアクセス権、実行パラメータ、作業ディレクトリ、indexing preflight、出力契約を確認する入口です。

## Read this when
- realization refactor の変更差分をカテゴリ別に要約する agent call の出力契約や prompt、入力差分、実行条件を確認・変更するとき
- realization refactor のファイル単位レビュー・修正 agent call の findings、根拠、変更 path、oracle 要求、修正結果、検証の出力契約を確認・変更するとき
- これら二つの agent call の Structured Output schema と builder の設定の整合性を確認するとき

## Do not read this when
- 変更差分の実装内容や要約結果そのものを確認したいとき
- レビュー対象の oracle file や realization file の要求・実装を直接確認したいとき
- 共通 prompt 生成、構造化文書の Markdown rendering、path 解決の一般仕様を確認したいとき
- realization refactor の fork 以外の agent call、別の出力 schema、または git 差分生成そのものを調査するとき

## hash
- 2276d634baf5643d5c9ca83b08bf5512cdad9435104f536a1d4666e2639b9dfc
