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
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド固有モジュール。固定した report cut を入力に、raw observation の検証、candidate の deterministic processing、normalization と全 candidate の verification、generation/report の作成、current pointer の切替、publication 後の cleanup までを一つの再開可能な transaction として扱う。feedback report の処理順序、checkpoint 再利用、中断・失敗時の状態遷移、publication 契約を確認する入口。

## Read this when
- `cmoc feedback report` の実行経路、report cut の固定・再開、observation の集約、issue candidate の normalization、verification、generation publication、current pointer 切替を変更・調査するとき。
- feedback report の active state、checkpoint、固定参照、machine recurrence aggregate、publication cleanup の整合性や中断時の挙動を確認するとき。

## Do not read this when
- feedback observation の envelope や raw store の書き込み・読み出し仕様だけを確認する場合は、feedback store または observation validation の実装を直接読む。
- normalize/verify agent の入力 builder や Structured Output schema の契約だけを確認する場合は、対応する builder・schema を直接読む。
- active state、generation artifact、current pointer の共通永続化処理だけを確認する場合は、`runtime_feedback_state` を直接読む。
- Markdown report の表示形式だけを確認する場合は、`_render_feedback_report` とその仕様を直接読む。

## hash
- 35c95df4daa334562483b5bbc5bb70df323548cace16a7829c15d9eca22fcdd6
