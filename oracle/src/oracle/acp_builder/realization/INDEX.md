# `apply`

## Summary
- oracle の変更を realization へ反映する差分追従 Agent の起動定義を扱うディレクトリ。始点・終点 commit 間の oracle file の raw git diff を Agent prompt に渡し、対象 worktree、realization 書き込み権限、モデル・推論設定、起動時 indexing を指定する。配下の `fork` から起動定義の実装へ進む。

## Read this when
- oracle file の変更を realization file へ反映する Agent の prompt や起動パラメータを調査・変更するとき
- realization_apply_change の commit 範囲や oracle file の差分を Agent prompt に渡す処理を確認するとき

## Do not read this when
- 個別の oracle file または realization file の実装内容を直接調査するとき
- AgentCallParameter の共通仕様や prompt の共通生成処理だけを確認するときは、それぞれの定義元を直接読む

## hash
- a7d463e4657e3337b806e8957bd55a3ea4f637796a33243bdac78310fe1a96fc

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
