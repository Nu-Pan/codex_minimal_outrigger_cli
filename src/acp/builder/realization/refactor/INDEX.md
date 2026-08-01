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
- cmoc realization refactor fork 用の builder adapter パッケージ。change summary と file review and fix の builder 接続・再公開を扱う。

## Read this when
- cmoc realization refactor fork の builder adapter を変更・調査するとき。
- change summary または file review and fix の agent call parameter builder の接続や公開 API を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- 正本 builder の詳細な parameter 定義や JSON 定義を確認・変更するとき。
- prompt fence 共通処理など、fork adapter 以外の実装を調査するとき。

## hash
- d1db174d960fc94e8437a4f466b4d7cae422d72de994ac291f52a6a5b3ec172e
