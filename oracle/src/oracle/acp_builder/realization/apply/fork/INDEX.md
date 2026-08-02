# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 用の codex exec 起動パラメータを構築する。oracle file の差分、commit 範囲、linked worktree を完全 prompt に組み込み、realization file の差分追従を FLAGSHIP モデルへ委譲する処理の入口。

## Read this when
- oracle file の変更を realization file へ追従させる AgentCallParameter の構築・変更を行うとき
- realization apply fork の prompt 内容、作業範囲、差分参照、モデル設定、worktree 設定を確認するとき
- 差分追従処理の完了条件や realization write の委譲方法を調査するとき

## Do not read this when
- realization apply fork の実際の差分適用ロジックやテストだけを調べるとき
- 一般的な prompt 構築処理を調べるときは、prompt_builder の対象実装を直接読む方が適切
- AgentCallParameter や path context の共通定義を調べるときは、それぞれの定義元を直接読む方が適切

## hash
- 68cf3897fb535f36e027ccadd2b32f81fb566e2f4e0d7d9671d808b76b4a995b
