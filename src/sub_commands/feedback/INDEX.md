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
- `cmoc feedback report` の publication／diagnostic pipeline を実装するサブコマンド本体。固定済み report cut を起点に、raw observation の検証、candidate の deterministic 集約、normalization と全候補の verification、正常な active generation／Markdown report の publication、または incomplete 診断 report の保存までを一つの transaction として扱う。
- 中断・失敗時の report cut、checkpoint、publication 状態を durable に管理し、同一入力での再開、current pointer の整合性確認、artifact の hash 検証、publication 後の cleanup とログ記録も担う。feedback report の状態機械や subcommand 固有の中断・publication 仕様を確認・変更するときの実装入口である。

## Read this when
- `cmoc feedback report` の処理順序、再開可能な report cut、normalization／verification、publication または incomplete 診断の挙動を確認・変更するとき。
- feedback observation の candidate 化、machine recurrence 集約、active issue の再検証、current reference の固定と検証に関する実装を調べるとき。
- report artifact、generation、current pointer、checkpoint、cleanup、subcommand log の連携や中断時の状態遷移を調べるとき。

## Do not read this when
- feedback observation の入力形式や保存処理だけを確認する場合は、観測 envelope／store を直接扱う実装へ進む。
- normalization または verification agent の prompt・builder・Structured Output schema だけを確認する場合は、それぞれの feedback builder と正本 schema を直接読む。
- feedback state の正本仕様や `feedback report` の利用者向け挙動を確認する場合は、対応する oracle の app specification を先に読む。
- 共通の lock、active state、artifact、checkpoint、pointer 操作だけを確認する場合は、`commons` 配下の runtime state／store 実装へ直接進む。

## hash
- 400266f16f8c80c4c350aeda74deac91ccc4ec2ff9891062d8b5ca0328e6fd8d
