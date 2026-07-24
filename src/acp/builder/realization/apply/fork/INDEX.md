# `__init__.py`

## Summary
- `cmoc realization apply fork` 用の builder adapter を示す初期化モジュール。fork 適用処理の builder 接続点を確認する際の入口となる。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき。

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき。
- `cmoc realization apply fork` 以外の builder adapter を調査するとき。

## hash
- 8ac1b4ff7590d29ce880b9d540f7fcace726de341416b79123260b174c415a65

# `launch_exec.py`

## Summary
- realization apply fork の launch_exec builder を再公開する adapter。正本 builder が生成した agent call parameter の prompt に対し、oracle git diff 内のコードフェンスを保護して返す。

## Read this when
- realization apply fork の launch_exec 用 agent call parameter の生成経路や、raw oracle git diff を含む prompt のコードフェンス保護を確認・変更するとき。

## Do not read this when
- 正本 builder の仕様や prompt 本文そのものを確認したいときは、対応する oracle file を直接読む。
- apply fork 以外の builder、または raw diff を扱わない prompt 処理だけを調べるとき。

## hash
- 7d7823b8056b116a50fbe9fca1d4d9c5a087c0f55920e7bccca577634ee5d683
