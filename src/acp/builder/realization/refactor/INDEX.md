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
- cmoc realization refactor fork 用の builder adapter パッケージ。fork 関連の realization builder 公開入口を提供する。
- change summary parameter builder と file review 用 fork parameter builder を oracle 側実装から再公開する薄い adapter を含む。

## Read this when
- cmoc realization refactor fork の builder adapter の公開入口や import 経路を変更・調査するとき。
- fork 用 change summary parameter builder または file review parameter builder の接続先を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- builder の具体的な生成ロジックを確認・変更するとき。再公開元の oracle 実装を直接読む。

## hash
- 5c9c2c8473640ff0a4340416a4811bfb20b6d734428aac28efff347b4f40196c
