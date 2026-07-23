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
- 変更要約とファイル単位レビュー・修正を行う agent call の oracle source および Structured Output schema を扱うディレクトリ。変更要約は change_summary、ファイル単位レビュー・修正は file_review_and_fix を入口に確認する。

## Read this when
- refactor fork の変更要約の出力形式・検証項目、prompt、入力差分、実行設定、schema 指定を確認するとき
- ファイル単位レビュー・修正の出力形式、prompt、対象パス、アクセスモード、モデル設定、検証要件を確認するとき

## Do not read this when
- refactor 差分そのものやレビュー対象の realization 実装を調査・修正するとき
- 特定の Structured Output schema に関係しない実装挙動を調査するとき

## hash
- 0d86a9a99db3a4145a82b427cf6aaf60523fec85bb902f9ad010208776f2b2ad
