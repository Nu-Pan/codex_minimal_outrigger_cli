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
- `cmoc realization apply fork` における builder adapter の入口。fork 適用の launch_exec パラメータ生成へ到達するための互換接続点を扱い、配下の対象へ進むためのルーティング起点となる。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき。
- apply fork の launch_exec パラメータ生成、または互換入口から正本 builder への委譲関係を確認するとき。

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき。
- 正本 builder の実装内容や挙動を確認したいとき。
- apply fork 以外の realization apply や、launch_exec パラメータ生成と無関係な処理を扱うとき。

## hash
- 969bb10283d32eac44ac3c9c0235f822b323bae8734c4143f05df0deaf4c707b
