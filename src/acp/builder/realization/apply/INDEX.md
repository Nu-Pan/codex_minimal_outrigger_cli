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
- `cmoc realization apply fork` 用の builder adapter を提供するディレクトリ。fork 適用処理の builder 接続点と、launch_exec builder の import 入口を確認する際の入口となる。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき。
- realization apply fork の launch_exec builder の import 入口や公開 API を確認するとき。

## Do not read this when
- fork 適用処理や builder の具体的な構築ロジック・仕様を調査するとき。再公開元の oracle 実装を直接読む。
- `cmoc realization apply fork` 以外の builder adapter を調査するとき。

## hash
- fdd93fd1ce8600a5f91a3e3ec3d8028ed92f26521a4d3b02cb086de5a36a8923
