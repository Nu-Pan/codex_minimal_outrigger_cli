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
- `cmoc feedback report` の publication／diagnostic pipeline を一つの transaction として実装するモジュール。固定済み report cut を起点に、raw observation の検証、candidate の deterministic 集約、normalization と verification、正常 publication または incomplete 診断、checkpoint 再開、中断処理、cleanup までを統括する。
- feedback report 固有の状態機械と publication 境界を確認するための入口であり、normalization／verification の個別処理や feedback state の共通データモデルを読む前に、サブコマンド全体の処理経路を把握したい場合に適する。

## Read this when
- feedback report サブコマンドの report cut 固定、raw observation の検証・集約、candidate 処理、checkpoint、publication、incomplete 診断の挙動を変更または調査するとき
- feedback report の中断・再開、current pointer、active generation、cleanup、固定 repository reference、machine recurrence 集約の処理を確認するとき

## Do not read this when
- feedback state の正本データモデルや共通 state 操作を確認したいときは、対応する feedback state の oracle または共通 runtime モジュールを直接読む
- normalization builder、verification builder、Structured Output schema だけを確認したいときは、それぞれの builder または schema を直接読む
- report の仕様上の要件だけを確認したいときは、対応する feedback report の oracle file を直接読む

## hash
- 735f44f088bd947e22697336ae8810a21e760c8cc4fb7c70543f656efd25bb0a
