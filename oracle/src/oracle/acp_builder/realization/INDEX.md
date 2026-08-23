# `apply`

## Summary
- `cmoc realization apply fork` が使用する realization 追従 AgentCallParameter の定義。追従対象の commit 範囲や oracle file の raw git diff、prompt、worktree・権限・モデル・preflight などの起動条件を扱う、apply fork 関連設定の入口。

## Read this when
- `cmoc realization apply fork` の agent call における prompt 構成や起動パラメータを変更・確認するとき
- oracle file の差分を realization file に追従させる agent call の作業範囲、権限、worktree、モデル、preflight 設定を調査するとき

## Do not read this when
- realization file 個別の実装やテストの挙動を変更するとき
- apply fork の実行処理そのもの、または別種の agent call の prompt・起動条件を調査するとき

## hash
- ea4327451fe0dd6ad5fe3e8e4e14cc07faee090c9fdce21ff8ed3399c5432fd9

# `refactor`

## Summary
- refactor fork 向けの変更要約と、ファイル単位のレビュー・修正を行う agent call の構築定義をまとめたディレクトリ。
- 各処理の prompt、対象ファイルへのアクセス方針、実行設定、結果契約を確認する入口となる。

## Read this when
- refactor fork の変更差分を要約する agent call の責務や実行条件を確認・変更するとき
- refactor fork の oracle／realization file をレビュー・修正する agent call の調査範囲、修正条件、検証条件を確認・変更するとき
- 変更要約またはレビュー結果の Structured Output schema と、それに対応する prompt 構築定義を確認・変更するとき

## Do not read this when
- 実際の refactor 差分、oracle file、realization file の実装内容を調査するとき
- 変更要約やファイルレビュー・修正の処理本体ではなく、別の realization 領域の agent call 構築定義を直接調査するとき
- refactor fork の agent call を使った後の個別の変更内容やレビュー所見だけを確認したいとき

## hash
- e1d4c2f211e10bd95e41ebfb6671714f58b6091f112001362f9d907b12983c30
