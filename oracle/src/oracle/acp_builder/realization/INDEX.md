# `apply`

## Summary
- `realization apply fork` 用の agent call 起動処理を担う oracle src。codex exec の起動パラメータと完全 prompt を構築し、oracle 差分・commit 範囲・linked worktree、AgentCallParameter の設定を realization 追従 agent に渡す。

## Read this when
- `realization apply fork` の agent call 起動処理を変更・調査するとき
- oracle diff、commit 範囲、linked worktree の realization 追従 prompt への組み込みを確認するとき
- AgentCallParameter の model、reasoning、file access、indexing 設定を変更するとき

## Do not read this when
- `realization apply fork` 以外の agent call prompt を変更するとき
- prompt の共通生成仕様だけを確認するとき
- 実際の realization implementation や test の追従内容を調査するとき

## hash
- 7ac025b33ddf3ea7a9cb73ddb36ebc52bbe2216b9a3dd9f5d4f6c4d0f581223c

# `refactor`

## Summary
- refactor fork の変更要約とファイル単位レビュー・修正に関する AgentCallParameter の正本 schema および builder 実装をまとめるディレクトリ。差分要約、レビュー結果、各処理の prompt、実行条件、構造化出力契約を確認する入口。

## Read this when
- refactor fork の変更要約、単一ファイルのレビュー・修正、AgentCallParameter、prompt 構築、実行条件、Structured Output schema を確認または変更するとき。

## Do not read this when
- 実際のレビュー対象ファイルの実装内容を調査するとき。
- 変更差分そのものや、要約・レビュー結果の詳細な出力形式だけを確認するとき。

## hash
- 7c65884066bf26a7c0c2ed02199dc76ca8f9b6ac29bf27afd1f5ec52dfc4131d
