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
- `cmoc feedback report` の publication／diagnostic pipeline を実装するサブコマンド本体。固定済み report cut を起点に、raw observation の検証、issue candidate の deterministic 集約、必要な normalization、全 candidate の verification、正常 publication、または incomplete 診断までを一つの transaction として処理する。
- report cut、checkpoint、generation artifact、current pointer、cleanup、割り込み・失敗状態を連携させ、中断後の再開や publication 前後の整合性検証を担う。feedback report の処理順序、candidate 同一性判定、machine rule の集約、verification 結果の永続化、Markdown report 描画を確認するための入口である。
- feedback report サブコマンドの実装挙動、feedback state の遷移、割り込み時の扱い、または report publication／diagnostic pipeline の変更・調査を行うときに読む。個別の normalization／verification prompt や共有 feedback state／store の責務だけを確認する場合は、対応する builder または commons の実装を直接読む。

## Read this when
- `cmoc feedback report` の実行経路、事前条件、writer lock、report cut 固定、再開処理を確認するとき
- raw observation から candidate・machine aggregate を生成する deterministic processing や agent による normalization を調査するとき
- 全 candidate の verification、checkpoint の検証・再利用、inconclusive による incomplete 診断を確認するとき
- generation artifact、Markdown report、current pointer の publication と publication 後 cleanup の関係を確認するとき
- feedback report の中断・失敗・再開時の状態記録やログイベントを変更・検証するとき

## Do not read this when
- feedback observation の envelope や保存形式そのものだけを確認する場合
- normalization／verification agent の prompt builder や Structured Output schema の内容だけを確認する場合
- feedback state、generation artifact、checkpoint、raw store の共有 primitive だけを確認する場合
- feedback report 以外のサブコマンドの状態機械や publication 処理を調査する場合

## hash
- 23a01fb04ea0f12e0927e82cdd01244ecfac9d4ebf22523efb7d015652ff6ba7
