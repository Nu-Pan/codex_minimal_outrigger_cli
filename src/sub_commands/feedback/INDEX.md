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
- `cmoc feedback report` の publication／diagnostic pipeline を担うサブコマンド実装。
- 固定済み report cut を起点に、raw observation の検証、machine／agent observation の deterministic な candidate 集約、normalization と verification checkpoint の再利用、全 candidate の verification、正常 publication または incomplete 診断までを一つの transaction として処理する。
- report cut、checkpoint、generation、current pointer、cleanup、再開・中断・失敗時の状態遷移を含むため、feedback report の実行経路や中断後の再開処理を確認する際の入口になる。

## Read this when
- `cmoc feedback report` の実行条件、report cut の固定と再開、candidate の集約、normalization／verification、正常 publication、incomplete 診断を調査・変更するとき。
- feedback observation、active issue、machine aggregate、checkpoint、current pointer、publication cleanup の処理順序や整合性を確認するとき。
- feedback report の KeyboardInterrupt、publication 前後の失敗、staged artifact、cleanup failure の挙動を確認するとき。

## Do not read this when
- feedback report の正本状態契約やサブコマンド仕様だけを確認する場合は、対応する oracle file を直接読む。
- feedback observation の書き込み・masking・path 解決など raw store の共通処理だけを確認する場合は、runtime feedback store の実装を直接読む。
- feedback state の schema、generation artifact、current pointer の共通操作だけを確認する場合は、runtime feedback state の実装を直接読む。

## hash
- 03b7b3947534a9379af27881cbc13d4678bc1ec5e9a4924e3c3937e661ea555a
