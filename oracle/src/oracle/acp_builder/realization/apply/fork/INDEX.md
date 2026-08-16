# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 用の AgentCallParameter を構築する実装で、追従対象の commit 範囲と oracle file の raw git diff を prompt に埋め込み、run worktree を作業ディレクトリとして realization 追従 agent を起動する。
- realization file の差分追従 prompt、ファイルアクセス権、モデル・推論設定、検証および routing policy の適用範囲を確認したい場合の入口となる。

## Read this when
- `realization apply fork` の起動 prompt や AgentCallParameter の構築仕様を変更・確認するとき
- oracle file の変更を realization file 全体へ反映する agent call の作業範囲、完了条件、起動パラメータを調査するとき
- run worktree、commit 差分、oracle/realization policy の prompt 連携を確認するとき

## Do not read this when
- `realization apply fork` 以外の apply 処理や、一般的な AgentCallParameter の基礎定義だけを調査するとき
- prompt の共通生成処理そのものを変更・確認する場合は、まず `build_complete_prompt` の定義を読むとき
- oracle file の個別仕様や realization 実装の具体的な挙動を確認する場合は、対象の oracle file または realization file を直接読むとき

## hash
- 90a7e8737972af17ddbe94bf6da4108b1f45c08a3e4b9d2f352bca6477c438ba
