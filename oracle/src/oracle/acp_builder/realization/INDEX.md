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
- 対象ディレクトリの責務を、refactor fork における変更要約・ファイル単位レビュー／修正の構造化出力と AgentCallParameter 構築の入口として説明する。変更差分の要約やレビュー・修正実行の条件を確認する際に参照する。

## Read this when
- refactor fork の変更要約・レビュー・修正 prompt の構成を確認するとき
- 構造化出力、AgentCallParameter、実行条件、変更後検証の実装を確認するとき

## Do not read this when
- 個別ファイルの実装内容やレビュー基準だけを調べるとき
- 構造化出力スキーマだけを確認するとき
- レビュー対象の変更内容や生成済み要約だけを確認するとき

## hash
- 8e0a8efc7a985a2ef3c63cd00841f6fa5014108ae7762cc328a87a497917d1a6
