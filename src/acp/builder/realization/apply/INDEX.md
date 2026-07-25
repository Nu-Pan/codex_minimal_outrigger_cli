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
- `cmoc realization apply fork` 用の builder adapter を収める初期化モジュール群。fork 適用処理の builder 接続点と、launch_exec builder の prompt 生成・raw oracle git diff 埋め込みを確認する入口。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき。
- realization apply fork の launch_exec builder の挙動、prompt 生成、または raw oracle git diff の埋め込みを変更・調査するとき。

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき。
- `cmoc realization apply fork` 以外の builder adapter を調査するとき。
- 正本 builder 自体の仕様や実装を確認するとき。対応する oracle file を直接読む。

## hash
- 1bb3a9b7c555d706b37165e3009620a3b3c866dc1d6b0a822117135a18780d61
