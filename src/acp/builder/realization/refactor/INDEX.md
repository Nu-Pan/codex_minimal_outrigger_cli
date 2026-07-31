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
- cmoc realization refactor fork 専用の builder adapter パッケージ。change summary と file review and fix の builder 接続・再公開を扱う。

## Read this when
- realization refactor fork の builder adapter を変更・調査するとき。
- fork 差分用 change summary の prompt 生成や raw git diff の code fence 保護を確認するとき。
- fork 側の file review and fix parameter builder の公開 API と oracle builder との接続を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- prompt fence 保護のない change summary builder 自体を直接確認するとき。
- file review and fix の parameter 定義そのものを確認・変更するとき。

## hash
- cb95e4128a0f959ebcf10939085d031218cf8a4e961ef76fa9eb712d879bd435
