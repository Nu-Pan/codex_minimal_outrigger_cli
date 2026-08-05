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
- realization refactor における builder adapter パッケージ。refactor 処理の builder 関連実装へ進む入口。
- fork 用 builder adapter を提供し、change summary と file review and fix の builder 接続・再公開を扱う。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。
- fork の builder adapter、または change summary・file review and fix の agent call parameter builder の接続や公開 API を変更・調査するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- fork 以外の builder 実装を調査するとき。
- 正本 builder の parameter 定義・JSON 定義、prompt fence 共通処理を確認・変更するとき。

## hash
- 919e1c2f18330e415fd3ed57b7b0a2db49f15d291b83fdcafcf4e84b343aa516
