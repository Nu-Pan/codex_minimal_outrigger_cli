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
- `cmoc realization apply fork` サブコマンドの実行本体。realization 差分の始点特定、oracle diff 構築、追従 agent 実行、想定外変更の検査、INDEX 更新を含む処理単位の commit、run の joinable/error 更新、fork report 保存を統括する。
- realization apply fork の CLI 挙動、run ライフサイクル、差分検査、失敗時 rollback・error report の入口として読む。

## Read this when
- `cmoc realization apply fork` の実装や実行フローを変更・調査するとき
- realization apply agent の差分追従、commit、joinable 公開、fork report の生成を確認するとき
- apply fork 失敗時の run 回収、rollback、error state 遷移を調査するとき

## Do not read this when
- realization apply agent が生成する prompt の内容だけを確認したいときは、launch parameter builder を直接読む
- run の共通状態管理・commit・rollback・tracking の汎用仕様だけを調査するときは、`commons.runtime_run*` の実装や対応する oracle を直接読む
- fork report の共通フォーマットだけを確認するときは、`commons.runtime_run_report` を直接読む

## hash
- acf78bad8bee26a8229da1a2e2671ab0372d311e4f78f946acd1e54454dcadd3
