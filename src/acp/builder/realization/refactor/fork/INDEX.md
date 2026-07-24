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
- realization refactor の fork 差分向け change summary builder を公開する adapter。oracle 側の builder で生成した agent call parameter を受け取り、raw git diff 部分のコードフェンスを保護した prompt に置き換える。

## Read this when
- realization refactor の fork 処理で change summary 用 agent call parameter の生成経路や prompt の diff フェンス保護を確認・変更するとき。
- oracle builder の結果を realization 側で再公開する adapter の挙動を確認するとき。

## Do not read this when
- oracle 側の change summary の正本仕様や prompt 内容そのものを確認したいときは、対応する oracle file を直接読む。
- realization refactor の fork 以外の builder や、一般的な prompt fence 処理を変更するとき。

## hash
- 9aeac639e31686800123265bc0655e8f6afa808e96a7232c11b5992a45c63fd1

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
