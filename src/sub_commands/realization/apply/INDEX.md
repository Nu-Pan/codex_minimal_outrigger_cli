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
- `cmoc realization apply fork` の実行本体を担い、realization apply agent を起動して差分を検査・commitし、runをjoinableまたはerror状態としてfork reportに記録する。
- editing runの作成、oracle差分の構築、agent実行、想定外変更やagent commitの検出、INDEX再生成、変更のrollback・state更新・report保存までを一連の処理として扱う。
- realization apply forkのCLI処理と、agent commit検査、preflight commit rollback、エラー時report生成などの補助処理を確認する入口である。

## Read this when
- `cmoc realization apply fork` の実行フロー、run状態遷移、fork reportの保存条件を調べるとき。
- realization apply agentが作成した差分の許可範囲、commit検査、想定外変更の扱いを変更または確認するとき。
- apply fork失敗時のCodex child停止、差分rollback、error state、cleanup warningの記録を調べるとき。

## Do not read this when
- realization apply agent自体のプロンプト生成や差分適用仕様を調べるときは、agent launch parameterの実装または対応する正本仕様を直接読む。
- editing run全般のjoin・abandonや共通ライフサイクルの仕様を調べるときは、共通runtime lifecycleまたはediting runの正本仕様を直接読む。
- INDEX生成機能そのものの仕様や実装を調べるときは、indexingの仕様または実装を直接読む。

## hash
- 710c25ffaf466fc4c12f3e50a2931903a5638de62df20e441080773388007503
