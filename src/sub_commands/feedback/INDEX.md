# `__init__.py`

## Summary
- feedback サブコマンドの実装を担う。feedback サブコマンドの処理を確認・変更するときの入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。

## hash
- 314f863a7cbf0d8eb6a2e9f72ee941edfcbbfcc5768f529aed40f09e96968cb9

# `report.py`

## Summary
- `cmoc feedback report` の active-state publication pipeline を実装するモジュール。固定済み report cut を入力に、raw observation の検証、agent/machine candidate の deterministic 集約、normalization と全 candidate の verification、checkpoint 再利用、report・generation artifact の作成、current pointer 切替、publication 後 cleanup までを単一 transaction として扱う。feedback report の状態機械、再開、中断、失敗処理の実装を確認したいときの入口。

## Read this when
- `cmoc feedback report` の cut 固定から publication までの処理順序や責務を調べるとき。
- feedback observation の validation、machine recurrence 集約、agent issue 同一性判定、verification checkpoint の再利用を変更・調査するとき。
- feedback report の current pointer 切替、generation artifact、cleanup、interruption/resume の挙動を確認するとき。

## Do not read this when
- feedback observation の envelope や永続 state の共通データ構造だけを調べる場合は、対応する runtime state/store の実装を直接読む。
- normalize/verify agent parameter や Structured Output schema の契約だけを調べる場合は、各 builder と schema を直接読む。
- 他の feedback サブコマンドの CLI 処理や、Markdown report の一般的な表示仕様だけを調べる場合は、対応する専用モジュール・oracle file を直接読む。

## hash
- a2cae4206f3c41c6c8d8bb58895bc3ffb14d827618e7a2384e6a0e836329af85
