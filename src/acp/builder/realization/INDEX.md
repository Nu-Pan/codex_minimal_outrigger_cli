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
- realization apply 用の builder adapter を提供するモジュール群。apply の共通入口と、fork 適用時の builder 接続・launch_exec の prompt 生成および raw oracle git diff 埋め込みを扱う。

## Read this when
- realization apply の builder adapter の責務や配置を確認するとき
- `cmoc realization apply fork` の builder adapter、launch_exec builder の挙動、prompt 生成、または raw oracle git diff 埋め込みを調査・変更するとき

## Do not read this when
- apply 処理そのものの実装詳細を調査するとき
- realization apply fork 以外の builder adapter を調査するとき
- 正本 builder の仕様や実装を確認するとき（対応する oracle file を直接読む）

## hash
- 18b45cb27d4e2b32d14c8e0ed99ac43b897c37b88ad434dd7216e412e09a341e

# `refactor`

## Summary
- realization refactor の builder adapter パッケージ。refactor 処理における builder 関連実装への入口で、fork 用 adapter を下位要素として含む。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。
- realization refactor fork の builder adapter、change summary 用 parameter 生成、または file review and fix parameter builder の接続を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- 正本 builder 仕様、change summary JSON 定義、file review and fix の parameter 定義、または prompt fence 保護の共通実装を確認するとき。

## hash
- db19447baaeb6057a30ad381abb56478455cefdf2accdd949ba3c6b0bd47cf2c
