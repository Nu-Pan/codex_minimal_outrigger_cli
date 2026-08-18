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
- `cmoc feedback report` サブコマンドの実装本体。固定した report cut を起点に、raw observation の検証、agent／machine candidate の正規化・集約、checkpoint 再利用、全 candidate の verification、正常 publication または incomplete 診断までを一つの transaction として処理する。
- writer lock、active state と current reference の検証、publication 後の cleanup、中断・失敗時の状態記録、Markdown report と generation artifact の生成を担う。feedback report の処理順序、再開条件、checkpoint、publication 境界を確認する実装上の入口である。
- 正本仕様の詳細や state schema の意味を確認する場合は、対応する feedback state／feedback report の oracle file を先に読む。builder の prompt／Structured Output 契約や共通 feedback state・store の実装詳細は、それぞれの下位 module を直接読む。

## Read this when
- `cmoc feedback report` の処理フロー、report cut の固定と再開、normalization／verification checkpoint、publication／incomplete 診断の挙動を調査・変更するとき。
- feedback writer lock、current pointer、active generation、raw observation cleanup、割り込み・失敗処理の責務を確認するとき。
- feedback report の candidate 集約、machine recurrence threshold、current reference の固定、検証結果の report 反映を追跡するとき。

## Do not read this when
- feedback observation の envelope や保存形式だけを確認する場合は、共通 feedback state／store の実装または対応する oracle file を直接読む。
- normalization／verification agent の prompt と Structured Output schema だけを確認する場合は、`acp.builder.feedback` の各 builder と schema を直接読む。
- 一般的な CLI runner、logging、report rendering の共通仕様だけを確認する場合は、このサブコマンド実装ではなく対応する共通 runtime module を直接読む。

## hash
- ebb7617bb85609b56938fa542e20ebc5425fcd5641950749db1fa9fdb1bc1015
