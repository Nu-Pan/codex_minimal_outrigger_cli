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
- realization refactor の change summary builder を適合させる adapter。正本 builder が生成した agent call parameter の prompt に対し、raw Git diff をコードフェンス保護した内容へ差し替えて再公開する。

## Read this when
- realization refactor の fork における change summary 用 agent call parameter の生成や prompt 保護処理を変更・調査するとき。
- raw Git diff のコードフェンス保護と、正本 builder parameter の再利用方法を確認するとき。

## Do not read this when
- 正本の change summary builder や JSON 定義そのものを変更・調査するときは、対応する oracle file を直接読む。
- change summary 以外の realization refactor builder や prompt fence 共通処理を調査するとき。

## hash
- a83ec0611410a3ec583fa30996680b1cf7fcb8bc394ebe3f5ff81cfa4c83a1b7

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
