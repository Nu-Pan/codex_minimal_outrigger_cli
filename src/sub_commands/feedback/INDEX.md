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
- `cmoc feedback report` の固定済み report cut を処理するサブコマンド実装。
- pending observation、active state、repository reference を検証・固定し、deterministic normalization、machine 集約、全 candidate の verification、checkpoint 再利用を管理する。
- 全 candidate が確定した場合は active generation と Markdown report を publication し、判定不能 candidate がある場合は current pointer を変更せず incomplete 診断 report を保存する。
- writer lock、割り込み復旧、publication 前後の状態遷移、artifact hash、secret masking、cleanup、subcommand log 記録までを一つの transaction として扱う。

## Read this when
- `cmoc feedback report` の処理順序、publication、incomplete 診断、再開・割り込み時の挙動を確認するとき。
- feedback observation の candidate 化、machine recurrence 集約、agent normalization、verification checkpoint の仕様または実装を調べるとき。
- report cut、current pointer、generation artifact、raw observation の整合性検証や cleanup の責務を追跡するとき。
- feedback report の状態遷移、永続化、artifact hash、current evidence の制約を実装から確認するとき。

## Do not read this when
- feedback observation の受理・保存形式や共通 state の定義だけを確認する場合は、対応する runtime store または feedback state の定義を直接読む。
- normalization agent や verification agent の prompt・Structured Output schema の内容だけを確認する場合は、各 builder と schema を直接読む。
- 一般的な CLI runner、logging、report 表示規則だけを確認する場合は、対応する共通 runtime・logging・仕様文書を直接読む。
- feedback report 以外のサブコマンドの処理や、Markdown report の利用方法だけを調べる場合は、この実装を入口にしない。

## hash
- 7edae973eab26cd5bd841202d4b1a5d179a8a8d1b279feb110828faff49f2eca
