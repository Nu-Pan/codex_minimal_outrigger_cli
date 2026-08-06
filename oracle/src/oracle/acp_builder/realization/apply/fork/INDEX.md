# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 用の codex exec 起動パラメータを構築する正本実装。oracle file の差分、対象コミット範囲、作業用 linked worktree を完全な realization 追従プロンプトへまとめ、実行モデルやアクセス権限などの AgentCallParameter を定義する。

## Read this when
- realization file へ oracle file の変更を追従させる AgentCallParameter の生成条件や、差分駆動の codex exec prompt 構築方法を確認したいとき。
- `realization_apply_change` ブロック、完全 prompt、実行時のモデル・推論・ファイルアクセス設定の対応関係を調べるとき。

## Do not read this when
- `cmoc realization apply fork` の起動以外の prompt 構築を調べるときは、各用途の prompt builder 実装を直接読む。
- realization file の具体的な変更処理やテスト内容を確認したいときは、対応する realization implementation または realization test を直接読む。

## hash
- 1e32c9dab816365b25751644b376838a59e1a19ab099271595baecb24980f936
