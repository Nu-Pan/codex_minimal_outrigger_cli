# `apply`

## Summary
- Oracle 側の差分を realization file 全体へ反映する `codex exec` 用 AgentCallParameter を構築する処理を扱う。raw git diff と commit 範囲を prompt に埋め込み、実行設定と linked worktree を組み立てる。

## Read this when
- `cmoc realization apply fork` の実行 prompt や realization 追従処理を変更・調査するとき。
- 対象 agent call のモデル、推論強度、ファイルアクセス、作業ディレクトリ、indexing preflight を確認するとき。

## Do not read this when
- 通常の realization 実装・テストを変更または調査するとき。
- prompt の一般的な組み立て規則だけを確認したいとき。

## hash
- 6831092f313aa0e997cc403d2a897d51b344a43ca142092721e9db68a91ab45b

# `refactor`

## Summary
- realization refactor fork の変更要約と、ファイル単位レビュー・修正に関する prompt 構築処理および Structured Output schema をまとめる領域。差分要約とレビュー対象の調査・修正・検証に進む入口。

## Read this when
- realization refactor fork の変更要約 agent call の入力、モデル設定、アクセス権、出力形式を確認するとき
- ファイル単位レビュー・修正 agent call の対象パス、prompt、修正方針、検証要件、所見 schema を確認するとき

## Do not read this when
- refactor fork の差分内容や候補ファイルの処理順を確認したいとき
- レビュー対象ファイルの実装詳細を調査したいとき
- 変更要約またはレビュー・修正の Structured Output schema の詳細だけを確認したいときは、対応する JSON schema を直接読む

## hash
- 334d143dc97e803e7a15bc5ba906e800523440036ef01d806d0fd9d5c99176fc
