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
- realization refactor における file review 用 fork parameter builder の公開 adapter。実体は oracle 側の builder を再公開するだけで、下位実装へ進む入口となる。

## Read this when
- realization refactor の file review・fix 処理で、fork parameter builder の公開入口を確認したいとき。

## Do not read this when
- file review・fix の builder と無関係な処理を調査するとき。
- builder の具体的な生成ロジックを確認したいときは、再公開元の oracle 実装を直接読む場合。

## hash
- 65717d928604ea224b2ea9290e707d41385c8235fd63b6fb4d96bbe744915382
