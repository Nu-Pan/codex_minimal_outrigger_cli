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
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド固有モジュール。固定済み report cut を作成・再開し、raw observation と current state/reference を検証したうえで、deterministic processing、machine recurrence 集約、agent による issue identity normalization、全 candidate の verification を進める。
- checkpoint と manifest を用いて中断後の同一 cut を再利用し、検証済み candidate から generation artifacts と Markdown report を生成する。publication-ready 状態では current pointer の切替を再開できる。
- generation、report、observation、checkpoint の hash/reference を管理し、publication 後の cleanup と失敗・中断の記録まで含めて、feedback report の publication transaction 全体を扱う。

## Read this when
- `cmoc feedback report` サブコマンドの実行前提、writer lock、report cut の固定・再開、処理状態遷移を確認するとき。
- raw observation の canonical validation、repository reference の capture、machine rule の recurrence threshold、candidate の deterministic 集約を確認するとき。
- normalization・verification の Codex 実行、Structured Output の postcondition、checkpoint の hash/schema 検証、publication と current pointer 切替を追跡するとき。

## Do not read this when
- feedback observation の生成・保存、issue の normalization builder、verification builder/schema、active state や artifact 永続化の共通実装を直接確認したい場合。
- `cmoc feedback report` の利用方法や正本仕様だけを確認する場合は、対応する oracle file を直接読む。

## hash
- c8877748ce11fcd4ffb7b127f39c4d17dc9aa34d1e701f0253819772cded1e7c
