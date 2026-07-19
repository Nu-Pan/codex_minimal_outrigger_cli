# `launch_exec.py`

## Summary
- `cmoc oracle edit fork` 用の `codex exec` 起動パラメータを構築する。ユーザー指示を固定部分と組み合わせた完全 prompt に変換し、oracle file 編集用のモデル・権限・作業ディレクトリなどを設定する。

## Read this when
- oracle file 編集用の `codex exec` 起動設定を変更・確認するとき
- 完全 prompt の構成、oracle 編集権限、実行モデル、linked worktree の指定を確認するとき

## Do not read this when
- oracle file 編集以外の agent call パラメータを扱うとき
- 完全 prompt の共通生成規則だけを確認したいときは、prompt builder の実装を直接読む

## hash
- 96b949e6129b0a9a1848b99e720ca4f8cc2063e658dc5c6f48a2804a8c8cbdf0
