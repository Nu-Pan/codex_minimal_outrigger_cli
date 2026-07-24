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
- `cmoc realization apply fork` 用の builder adapter を含むディレクトリ。fork 適用処理の builder 接続点を確認する入口。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や、launch_exec 用 agent call parameter の生成経路を確認・変更するとき。
- raw oracle git diff を含む prompt のコードフェンス保護処理を調査するとき。

## Do not read this when
- 正本 builder の仕様や prompt 本文そのものを確認するとき。
- fork 適用処理そのものの実装詳細、または apply fork 以外の builder を調査するとき。

## hash
- 3fd45141dec0067cc29da7c47da04675b1529ac709fbef15afb4bc0e2713e85f
