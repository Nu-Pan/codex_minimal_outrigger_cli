# `__init__.py`

## Summary
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `cmoc realization apply fork` サブコマンドの実行制御を担う実装。realization apply agent の起動、oracle 差分の構築、run worktree の変更検査・commit、joinable/error state 更新、fork report 保存、失敗時の rollback と run 回収を扱う。

## Read this when
- `cmoc realization apply fork` のライフサイクル、agent 実行、差分 commit、joinable/error 遷移を変更・調査するとき。
- apply fork の想定外差分、起動失敗、cleanup、fork report の挙動を確認するとき。

## Do not read this when
- realization apply agent の prompt 構築だけを変更・調査する場合は、launch parameter builder を直接読む。
- run の一般的な join・abandon 処理や共通 state 操作だけを確認する場合は、対応する runtime lifecycle 実装を直接読む。

## hash
- d8ab5c807e8b7b94113a2e08b503dae6dd225bf8dcd4b0f01f748f427a53b866
