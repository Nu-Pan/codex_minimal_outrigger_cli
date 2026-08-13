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
- 対象は `cmoc feedback report` の publication／diagnostic pipeline を実装するサブコマンド固有モジュールです。固定した report cut を起点に、raw observation の検証、candidate の deterministic 集約、normalization／verification checkpoint の再利用、正常な active generation publication、または incomplete 診断 report 保存までを一つの transaction として進めます。
- feedback state、report cut、current pointer、generation artifact、checkpoint、および cleanup の整合性を検証・更新し、処理の中断や失敗後に安全に再開できる実行経路を提供します。
- `feedback report` の状態機械、publication 契約、または report cut／checkpoint／incomplete 診断の実装責務を確認・変更するときの入口です。共通の feedback state／store API の詳細や CLI 全体の割り込み規則を直接調べる場合は、それぞれの定義元へ進んでください。

## Read this when
- `cmoc feedback report` の処理順序、固定済み入力、candidate 集約、全 candidate verification、publication、incomplete 診断を確認するとき。
- report cut、normalization／verification checkpoint、current pointer、generation artifact、cleanup の再開・失敗時挙動を調査するとき。
- raw observation の canonical validation、repository reference の capture、machine recurrence aggregation、agent observation の identity normalization の実装を確認するとき。
- feedback report の中断、publication 後 cleanup、subcommand log event、生成 Markdown report の構築経路を確認するとき。

## Do not read this when
- feedback の永続 state や raw store の共通データ構造・ファイル操作だけを確認する場合は、対応する `commons` の定義元を直接読んでください。
- normalization／verification の prompt、builder、Structured Output schema だけを確認する場合は、各 builder と schema を直接読んでください。
- `feedback report` 以外のサブコマンドの処理や、一般的な CLI runner の挙動だけを確認する場合は、この対象を入口にしないでください。

## hash
- 575d8652f0350ec0e2363e3719c22071ddd3bd013350441aae189fc6d04ba2b8
