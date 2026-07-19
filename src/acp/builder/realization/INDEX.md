# `__init__.py`

## Summary
- realization workload を builder に適応するための adapter。realization workload の builder 連携を扱う実装への入口。

## Read this when
- realization workload の builder adapter や、その連携箇所を確認・変更するとき。

## Do not read this when
- builder の共通処理や realization workload 自体の内容を直接確認・変更するとき。

## hash
- cd24953f9993d22add52453bee8a2c6dd9c2fc85ecd238c962f1cc82066eec92

# `apply`

## Summary
- realization apply 用の builder adapter を提供するディレクトリ。apply 処理の builder 接続点と、fork 適用向け builder adapter への入口を扱う。
- 下位の `fork` は `cmoc realization apply fork` の launch_exec builder の import 入口を確認するための対象。

## Read this when
- realization apply の builder adapter の責務や配置を確認するとき
- `cmoc realization apply fork` の builder adapter や launch_exec builder の公開入口を辿るとき

## Do not read this when
- apply 処理の具体的な構築ロジックや仕様を調査するとき
- apply 処理以外の builder adapter を調査するとき

## hash
- 9808798aed8e873b2cda117405659a546e04c999c146b622c5ff4f665b875034

# `refactor`

## Summary
- realization refactor の builder adapter パッケージ。refactor 処理の builder 関連実装への入口で、fork 用 builder の公開入口を含む。

## Read this when
- realization refactor における builder adapter の責務や実装入口を確認するとき。
- fork 用の change summary parameter builder または file review parameter builder の公開入口・接続先を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- builder の具体的な生成ロジックを確認・変更するとき。

## hash
- c858be059c1590289ceaf3b0e4157f0af24da7eadb5bb53293bad55c49d1a4bd
