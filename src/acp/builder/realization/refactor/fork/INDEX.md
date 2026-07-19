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
- realization refactor の fork 用 change summary parameter builder を oracle 側の実装から再公開する薄い adapter。呼び出し側がこの realization builder を入口として利用するためのファイル。

## Read this when
- realization refactor の fork における change summary parameter builder の公開入口や import 経路を確認するとき。

## Do not read this when
- change summary parameter の具体的な生成ロジックを確認・変更するときは、再公開元の oracle 実装を直接読む。

## hash
- 2d0aa02653f4f579de9055d709c3b1b21366834fc9fcc0681c8a4bd8036fa7a6

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
