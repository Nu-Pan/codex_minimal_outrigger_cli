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
- `cmoc feedback report` サブコマンドの report cut を起点に、raw observation の固定・検証、active issue の正規化、machine observation の集約、全 candidate の verification、正常 publication または incomplete 診断を一つの transaction として実行する処理本体。
- writer lock、checkpoint、current pointer、generation artifact、cleanup、interruption／failure state を含む publication pipeline の実装を確認するときの主要な入口である。
- agent に渡す固定 reference、Structured Output checkpoint の再利用条件、verification 結果から active generation と Markdown report を生成する処理を追跡するときに読む。

## Read this when
- `cmoc feedback report` の処理順序、再開可能な report cut、publication、incomplete 診断、cleanup の責務を確認するとき
- feedback report の issue candidate 正規化、machine recurrence 集約、verification、active generation 更新の実装を変更または調査するとき
- report cut manifest、normalization／verification checkpoint、current pointer、generation artifact の整合性や中断時の状態遷移を確認するとき

## Do not read this when
- feedback state の永続形式や report cut／generation の共通 helper 契約だけを確認したいときは `commons.runtime_feedback_state` を直接読む
- raw observation の保存・canonical JSON・secret masking・path 制約だけを確認したいときは `commons.runtime_feedback_store` を直接読む
- normalization／verification agent の prompt builder や Structured Output schema の内容だけを確認したいときは対応する builder／schema を直接読む
- feedback report の正本仕様や interruption 契約を確認したいときは、本文冒頭に示された `oracle/doc/app_spec` の仕様書を直接読む

## hash
- cb802ce6f12944d4163205c9514be212b418b0b054e1d6e3d25ba0de278c689b
