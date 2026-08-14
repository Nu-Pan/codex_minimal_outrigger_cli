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
- realization apply 用の builder adapter をまとめたディレクトリ。apply 処理の builder 実装や、配下の fork adapter へ進む入口となる。

## Read this when
- realization apply に関する builder adapter の構成や入口を確認するとき
- apply 処理の builder 実装を辿るとき

## Do not read this when
- apply 処理以外の builder adapter を確認するとき
- 個別 adapter の詳細実装を直接確認したいときは、配下の対象へ直接進める

## hash
- 489bb960e219cb5547d82a3939183a15250f7f3053cb5244010addb81b6870c4

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
