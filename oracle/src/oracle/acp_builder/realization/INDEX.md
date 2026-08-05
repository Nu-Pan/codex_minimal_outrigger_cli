# `apply`

## Summary
- `cmoc realization apply fork` 用の codex exec 起動パラメータを構築する実装。oracle file の差分、commit 範囲、linked worktree を prompt に組み込み、FLAGSHIP モデルへ realization file の差分追従を委譲する入口。

## Read this when
- oracle file の変更を realization file へ追従させる AgentCallParameter を構築・変更するとき
- realization apply fork の prompt、作業範囲、差分参照、モデル設定、worktree 設定を確認するとき
- 差分追従の完了条件や realization write の委譲方法を調査するとき

## Do not read this when
- realization apply fork の差分適用ロジックやテストだけを調べるとき
- 一般的な prompt 構築処理を調べるとき
- AgentCallParameter や path context の共通定義を調べるとき

## hash
- 132f46ba2d4207e8b13105a02aa0265cc1bd78a348aa3c925878926a52fbe27c

# `refactor`

## Summary
- refactor fork における変更要約と、ファイル単位のレビュー・修正結果を扱う正本実装および Structured Output スキーマの領域。変更要約、レビュー結果、各処理の prompt と実行条件を確認する入口。

## Read this when
- refactor fork の変更差分を要約する処理や出力契約を確認・変更するとき
- ファイル単位レビュー・修正の所見、修正結果、検証結果の出力形式を確認・変更するとき
- 変更要約またはレビュー・修正 agent call の prompt 構成・実行条件を確認・変更するとき

## Do not read this when
- 個別の realization 実装やテストの挙動を直接調査・変更するとき
- prompt や実行パラメータを確認せず、出力形式だけを確認したいとき
- 変更内容そのものだけを確認したいとき

## hash
- 4d3ab490fae709e20c5eab2e9492858dd77db7e7520ba0532a5eecc989e7e0d3
