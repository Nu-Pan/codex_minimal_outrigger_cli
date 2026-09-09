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
- `cmoc realization apply fork` 用の builder adapter の入口。fork 適用処理の builder 接続点を確認するときに読む。
- 既存の builder 参照を維持する互換入口であり、正本 builder の実装や realization 側の処理を調査するときは、再公開元の正本実装へ進む。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や入口を確認するとき
- 既存の `acp.builder.realization.apply.fork.launch_exec` 参照がどの正本 builder へ接続されるかを確認するとき

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき
- 互換入口の存在確認だけで、再公開元の正本 builder を調べる必要がないとき
- `cmoc realization apply fork` 以外の builder adapter を調査するとき

## hash
- 50ede43ea9ebe4ad326e44a9439129cf912b4334bdaf9fd13113119c6b1840eb
