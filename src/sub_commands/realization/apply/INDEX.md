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
- `cmoc realization apply fork` サブコマンドの実行処理を担当する。realization 差分の始点特定、oracle diff と Codex 実行パラメータの構築、追従 agent の実行、想定外変更の検査、INDEX を含む処理単位の commit、run の joinable 化、fork report の保存までを扱う。実行失敗時は子プロセス停止、変更 rollback、error state 更新、エラーレポート保存を行う。

## Read this when
- `cmoc realization apply fork` の挙動、run lifecycle、Codex agent の実行、差分検査・commit・rollback、fork report の生成を変更または調査するとき。

## Do not read this when
- realization apply の join や abandon の処理だけを扱うとき。共通 run lifecycle の詳細は `commons.runtime_run_lifecycle`、fork 起動パラメータの構築は `acp.builder.realization.apply.fork.launch_exec` を直接確認するとき。

## hash
- 51f53ffcd82a6f8ae67bd165d44aaf56b1f637bbf08ea1aca302e54931376e36
