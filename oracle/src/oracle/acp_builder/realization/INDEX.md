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
- refactor fork 配下で、変更差分の意味論的な要約処理と、指定ファイルを起点にしたファイル単位のレビュー・修正処理を定義するディレクトリ。各処理の prompt 構築、実行パラメータ、Structured Output 契約を確認する入口となる。

## Read this when
- refactor fork の変更差分要約やファイル単位レビュー・修正の起動条件、prompt、アクセス権限、モデル設定、検証方針を調査または変更するとき。
- これらの agent call が返す構造化結果の契約を確認するとき。

## Do not read this when
- 変更要約またはレビュー・修正結果の具体的な出力契約だけを確認したい場合は、対応する schema を直接読む。
- レビュー対象の実装、oracle の要求、個別仕様、実際の変更差分を調査する場合は、対象の oracle file、realization file、または raw git diff を直接読む。
- 共通の prompt 構築、パス解決、構造化文書レンダリング、agent call 基盤の仕様だけを調査する場合は、対応する共通実装を直接読む。

## hash
- 5bd08ca5521212f335a18cd5c0323b291cd51dbd8f89dea7fe63ff8428542d42
