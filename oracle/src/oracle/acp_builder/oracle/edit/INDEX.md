# `fork`

## Summary
- oracle file 編集用の `codex exec` 起動パラメータを構築する実装への入口。ユーザー指示から完全 prompt を作り、実行モデル、権限、作業ディレクトリ、linked worktree などを設定する。

## Read this when
- `cmoc oracle edit fork` の agent call 起動設定を変更・確認するとき
- oracle file 編集用の完全 prompt、モデル、権限、作業ディレクトリ、linked worktree の指定を確認するとき

## Do not read this when
- oracle file 編集以外の agent call 起動パラメータを扱うとき
- 完全 prompt の共通生成規則だけを確認したいとき（prompt builder の実装を直接読む）

## hash
- ebe77e4f2c311f860d92caffa125e64024d60a44846d9254c94dcd5f10dbc201
