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
- realization refactor の fork における change summary builder を、oracle 実装から再公開する互換入口。対応する builder を利用するための下位実装への入口として機能する。

## Read this when
- realization refactor の fork に関する change summary parameter builder を利用・変更・調査するとき。
- 互換入口から再公開される builder の参照元を確認するとき。

## Do not read this when
- change summary builder の実装詳細を確認する必要があるときは、直接 oracle 側の実装を読む。
- realization refactor の fork や change summary builder に関係しない作業。

## hash
- c0d7a42b998e37cd0eb58c2bed866165a5efdd716ffffa493db1a14b5780c2d8

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
