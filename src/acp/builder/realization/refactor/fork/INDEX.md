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
- realization refactor の change summary 用 prompt builder を、oracle の builder を再利用する adapter として提供する。raw Git diff 内の backtick に応じて Markdown の差分 fence を動的に拡張し、prompt の構造を壊さずに返す。

## Read this when
- realization refactor の fork における change summary prompt の生成や、raw Git diff の Markdown fence 保護を変更・調査するとき。
- oracle builder の呼び出し結果を AgentCallParameter として再公開する adapter の挙動を確認するとき。

## Do not read this when
- change summary の正本仕様や prompt 定義そのものを確認したいときは、対応する oracle file を直接読む。
- realization refactor の change summary 以外の builder や、一般的な fork 処理を調査するとき。

## hash
- 6154e6c9ce39e051f4b4998b9c3381d68a9f417d0c60cb526ed97fdf26a8cff0

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
