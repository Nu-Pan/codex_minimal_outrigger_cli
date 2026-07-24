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
- cmoc realization refactor fork 向けの builder adapter パッケージ。fork 関連の change summary および file review and fix の builder 接続・公開 API を扱う。

## Read this when
- realization refactor fork の builder adapter を変更・調査するとき。
- fork 処理における change summary の prompt 生成や file review and fix の oracle builder 接続を確認するとき。

## Do not read this when
- oracle 側の正本仕様や parameter 定義そのものを確認・変更するとき。
- fork 以外の builder 実装や、一般的な prompt fence 処理を調査するとき。

## hash
- 5f3ac5cbae80cd2ef3625f04c4b7853d5b1ff62d49e6efaf5ddbf9b3ae0bdb17
