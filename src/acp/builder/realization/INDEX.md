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
- realization apply 用の builder adapter を提供するモジュール。apply 系 builder 実装を確認する際の入口となる。
- fork 適用向け builder adapter を配下に持つサブディレクトリ。`cmoc realization apply fork` の launch_exec パラメータ生成へ進むための入口となる。

## Read this when
- realization apply の builder adapter の責務や、apply 系 builder 実装の配置を確認するとき
- `cmoc realization apply fork` の builder adapter や launch_exec パラメータ生成を確認するとき

## Do not read this when
- apply 以外の realization builder を確認するとき
- fork の launch_exec パラメータ生成そのものの実装詳細を直接確認するとき

## hash
- 1aff7bd61edfd5529e41a280a5cd7b7d325315f8879f7b155e750a471a4618fe

# `refactor`

## Summary
- realization refactor の builder adapter を収めるパッケージ。refactor 処理における builder 関連実装へ進む入口であり、fork 用の互換的な builder adapter も含む。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。
- fork の change summary または file review and fix parameter builder の公開 API、参照元、接続を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- fork 以外の builder 実装を調査するとき。
- builder の parameter 定義や実装詳細を、対応する oracle 側の実装から直接確認できるとき。

## hash
- 9967ee89fdb7e90dfd3488fbe7ed2698f1535924ffd79a69418eda3f742a629e
