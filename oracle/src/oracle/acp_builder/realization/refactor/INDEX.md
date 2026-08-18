# `fork`

## Summary
- refactor fork における変更差分の要約処理と、ファイル単位のレビュー・修正処理に関する schema および prompt builder の入口を案内するディレクトリ。変更要約、レビュー結果の出力契約、AgentCallParameter と実行設定の確認に利用する。

## Read this when
- refactor fork の変更差分を人間向けに要約する処理や、その Structured Output schema を確認するとき
- refactor fork のファイル単位レビュー・修正処理における prompt、対象 path、worktree、実行設定、結果 schema の関係を調査するとき
- レビュー結果の出力項目や、変更ファイル・対応状態の記録契約を確認するとき

## Do not read this when
- 変更要約やレビュー・修正の具体的な生成ロジックを調査する場合は、対応する Python ファイルを直接読むとき
- Structured Output の項目・型だけを確認する場合は、対応する JSON schema ファイルを直接読むとき
- レビュー対象の実装内容、個別仕様、または変更差分そのものを調査する場合は、対象の realization/oracle file や diff を直接読むとき

## hash
- a31f7c80e83ad9d46f509a037bfb70baa0a91b93fc0cbdb35353895ccb1d696c
