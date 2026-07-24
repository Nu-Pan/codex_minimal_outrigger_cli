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
- `cmoc realization apply fork` 向けの builder adapter を収めるディレクトリ。fork 適用時の launch_exec 用 builder の公開接続点を提供する。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や、launch_exec parameter builder の prompt 生成・公開 API を確認または変更するとき。

## Do not read this when
- oracle 側の正本 builder の仕様や prompt 構成を確認するとき。
- fork 適用処理そのもの、または fork 以外の apply 処理を調査するとき。

## hash
- ba21f080ee2dd6d1eda4888435f503adee257f4aff6d97e30080a2befd36e3d4
