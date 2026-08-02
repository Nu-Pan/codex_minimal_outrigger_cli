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
- refactor fork における変更要約とファイル単位レビュー・修正の AgentCallParameter、および Structured Output schema を定義するファイル群。変更要約・レビュー結果の形式確認と、各 prompt 構築処理の変更時に参照する入口。

## Read this when
- refactor fork の変更要約出力形式、根拠ファイル一覧、要約結果の検証項目を確認するとき
- ファイル単位レビュー・修正の所見フォーマットや、根拠・oracle 要求・対応・検証結果の構造を確認するとき
- 変更要約またはファイル単位レビュー・修正の prompt 構成、対象 path、実行条件、モデル設定、Structured Output schema の参照先を確認・変更するとき
- レビュー時の oracle・realization 参照規則や修正・検証条件を確認するとき

## Do not read this when
- レビュー対象ファイルの具体的な実装内容や個別の所見を調査するとき
- 変更差分そのものや要約結果の具体的内容を確認するとき
- 共通 prompt builder や path model の内部仕様を直接確認するとき
- 通常の実装・テスト仕様や、このディレクトリ以外の出力スキーマを扱うとき

## hash
- 56003164afc00ea727f3c2ed9ebf137e5e673f67fd213b15d94cfa9265589100
