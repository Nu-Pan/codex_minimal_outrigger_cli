# `__init__.py`

## Summary
- realization apply 用の builder adapter を提供するモジュール。apply 処理の builder 実装へ進む入口となる。

## Read this when
- realization apply の builder adapter の責務や実装を確認するとき
- apply 処理の builder 実装を辿るとき

## Do not read this when
- apply 処理以外の builder 実装を確認するとき
- builder adapter の詳細実装を直接確認する場合

## hash
- f826a5bac8bd998fa3b25c1e1a4faaebe0a1a1fe62de19e3062e0f78c2b14d60

# `fork`

## Summary
- `cmoc realization apply fork` 用の builder adapter 群。初期化モジュールと、oracle builder の呼び出しおよび生成 prompt 内の raw oracle git diff のコードフェンス保護を担う launch_exec adapter を含む。fork 適用処理における builder 接続点の入口。

## Read this when
- `cmoc realization apply fork` の builder adapter の配置・責務を確認するとき。
- apply fork の launch_exec builder の引数、oracle builder との adapter 境界、prompt 内の diff フェンス保護を確認・変更するとき。

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき。
- apply fork 以外の builder adapter を調査するとき。
- prompt fence 保護の共通処理や正本 builder の仕様を確認するとき。

## hash
- c1980cf470953f39a0f3c00338b0b2754e1ba593c163cd793f8c5627b323c844
