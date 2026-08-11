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
- 対象ファイルは `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド固有モジュールです。
- 固定済み report cut を起点に、raw observation の検証、agent observation の normalization、machine observation の recurrence 集約、全 issue candidate の verification、generation/report artifact の生成、current pointer の publication、publication 後の cleanup までを一つの再開可能な transaction として扱います。
- report cut manifest と normalization/verification checkpoint を用いて、中断・失敗後も固定入力と処理結果を再検証しながら再開します。active issue や repository reference の capture、hash による不変性検証、secret-safe な永続化、Markdown report の描画もこの処理経路に含まれます。
- `feedback report` サブコマンドの実装挙動、report cut、checkpoint 再利用、verification、publication、interruption、cleanup の変更や調査を行うときの入口です。

## Read this when
- `cmoc feedback report` の処理順序、状態遷移、再開動作を確認するとき
- feedback observation から issue candidate を作る規則、machine recurrence 集約、agent normalization を調べるとき
- issue candidate の verification 入力・checkpoint・current evidence 制約を調べるとき
- feedback generation、Markdown report、current pointer の publication、cleanup の整合性を調べるとき
- report cut の固定入力、repository reference、hash 検証、ユーザー中断時の扱いを変更するとき

## Do not read this when
- feedback observation の書き込みや共通 state/store のデータ形式だけを調べる場合は、対応する `commons` 実装を直接読む
- normalize/verify 用 agent prompt や Structured Output schema の契約だけを確認する場合は、対応する builder または schema を直接読む
- feedback report 以外のサブコマンドの処理を調べる場合は、このファイルではなく該当サブコマンドの実装へ進む

## hash
- 370ad5e6117ec40d7b6dfff6e2f5ebfdd06c29a7b159678e85124461798ef5d8
