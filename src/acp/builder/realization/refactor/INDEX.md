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
- cmoc realization refactor fork 向けの builder adapter パッケージ。change summary や file review・fix など、fork 側から oracle builder を利用する公開入口を提供する。

## Read this when
- realization refactor fork の builder adapter を変更・調査するとき。
- change summary prompt の生成や raw Git diff の Markdown fence 保護を確認するとき。
- file review・fix 用の fork parameter builder の公開入口を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- change summary の正本仕様や prompt 定義そのものを確認したいとき。
- builder の具体的な生成ロジックを確認したいとき。

## hash
- 6e63e98aa5984e311ba7a75ea96d5a21bbc0b96654b7db478f3f3f2c35bbda8c
