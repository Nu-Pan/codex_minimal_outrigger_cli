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
- cmoc realization refactor fork の builder adapter パッケージ。fork における change summary および file review and fix の parameter builder を、oracle 実装から利用するための互換的な公開入口を提供する。

## Read this when
- cmoc realization refactor fork の builder adapter の変更・調査を行うとき。
- fork の change summary または file review and fix parameter builder の公開 API、参照元、接続を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- builder の parameter 定義や実装詳細を確認することが目的で、対応する oracle 側の実装を直接読めるとき。

## hash
- a7abf8a243b9633a083c8790886337faeceed4b98c00a1439f7f1a0213de4855
