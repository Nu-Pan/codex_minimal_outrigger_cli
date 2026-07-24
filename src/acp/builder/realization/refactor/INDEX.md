# `__init__.py`

## Summary
- realization refactor 用の builder adapter パッケージ。refactor 処理の builder 関連実装へ進む入口。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。

## hash
- 4c331bccb54a9842893b30e509c994292dd25afbf1159ad4b7929ebffb3a311d

# `fork`

## Summary
- cmoc realization refactor fork 向けの builder adapter パッケージ。fork 関連の realization builder 接続処理への入口で、change summary と file review and fix の adapter を扱う。

## Read this when
- cmoc realization refactor fork の builder adapter を変更・調査するとき。
- fork 差分向け change summary builder のパラメータ生成、raw git diff の prompt fence 保護、または file review and fix builder の公開 API を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- 正本 builder の仕様・JSON 定義や parameter 定義そのものを確認・変更するときは、対応する oracle file を直接読む。
- realization refactor の fork 処理全般や、change summary・file review and fix 以外の prompt builder を調査するとき。

## hash
- 12223a874757db5d15a6a2b298794184dc7377e8236411d4d67c2f0752bef2b4
