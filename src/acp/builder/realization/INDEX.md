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
- `__init__.py` は realization apply 用の builder adapter を提供し、apply 処理の builder 実装へ進む入口となる。
- `fork` は `cmoc realization apply fork` 用の builder adapter 群を収め、初期化と launch_exec adapter による oracle builder 呼び出しおよび prompt 内 raw oracle git diff のコードフェンス保護を担う。fork 適用処理における builder 接続点の入口である。

## Read this when
- realization apply の builder adapter の責務や実装を確認するとき
- apply 処理の builder 実装を辿るとき
- `cmoc realization apply fork` の builder adapter の配置・責務を確認するとき
- apply fork の launch_exec builder の引数、oracle builder との adapter 境界、prompt 内 diff フェンス保護を確認・変更するとき

## Do not read this when
- apply 処理以外の builder 実装を確認するとき
- builder adapter の詳細実装を直接確認する場合
- fork 適用処理そのものの実装詳細を調査するとき
- apply fork 以外の builder adapter を調査するとき
- prompt fence 保護の共通処理や正本 builder の仕様を確認するとき

## hash
- 57a0537b9501de7783fe84e97545b76d19c05684a168f04670a729aee468461c

# `refactor`

## Summary
- realization refactor の builder adapter パッケージ。refactor 処理に関する builder 実装へ進む入口で、fork 配下に専用の接続・再公開実装がある。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。
- fork 側の change summary や file review and fix に関する builder 接続を調査するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- fork 以外の builder 実装を調査するとき。

## hash
- 418124a68c32e7db4e47360041c5ab69b5e533b7e174b395951a6ff3f999cdbe
