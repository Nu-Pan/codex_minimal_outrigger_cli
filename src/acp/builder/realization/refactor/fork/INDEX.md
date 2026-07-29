# `__init__.py`

## Summary
- cmoc realization refactor fork 用の builder adapter パッケージ。fork 関連の realization builder 接続処理への入口。

## Read this when
- cmoc realization refactor fork の builder adapter を変更・調査するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。

## hash
- e2e95e4974cee8956ab6d1e32ba70f20ad2afb6bee161325bbeeb9561c4b4cf5

# `change_summary.py`

## Summary
- realization refactor の fork 差分に対する change summary builder を適合させる adapter。正本 builder で生成した agent call parameter の prompt に含まれる raw git diff の code fence を保護し、既存の prompt 生成処理を再利用する。

## Read this when
- realization refactor の fork 差分用 change summary builder の prompt 生成や、raw git diff の fence 保護処理を確認・変更するとき。

## Do not read this when
- refactor fork 以外の change summary builder を扱うとき。
- prompt fence 保護や正本 builder の実装自体を直接確認する必要があるとき。

## hash
- 1a0f88e4459525758ad70bb26e97affb36c4bea2fce730a51d9df010e783aae6

# `file_review_and_fix.py`

## Summary
- realization refactor の fork において、file review and fix の oracle builder を realization 側から再公開する薄い adapter。詳細な parameter 定義は対応する oracle file に委譲する。

## Read this when
- realization refactor fork の file review and fix parameter builder の参照先や公開 API を確認するとき。
- 対応する oracle builder の実装または JSON 定義との接続を確認するとき。

## Do not read this when
- file review and fix 以外の builder を扱うとき。
- parameter 定義そのものを確認・変更するとき。この場合は対応する oracle file を直接読む。

## hash
- a051f806eb19e9b73542f4bde735c17f507b6f008cf69e3c9c6a6b7e8c9d02b3
