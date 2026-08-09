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
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンドモジュール。固定済み report cut を起点に、raw observation の検証、agent・machine observation の deterministic な集約と normalization、全 issue candidate の verification、generation/report の生成、current pointer の切替、publication 後の cleanup までを一つの再開可能な処理単位として扱う。

## Read this when
- `cmoc feedback report` の処理順序、report cut の固定・再開、checkpoint 検証、candidate 集約、verification、publication、cleanup の挙動を調べるとき。
- feedback report の active state や current pointer の切替が、どの固定入力・成果物参照・hash に基づくかを確認するとき。
- machine rule の recurrence 集約や agent observation の同一性判定、verification 出力の受理条件を変更・調査するとき。

## Do not read this when
- feedback observation の保存形式や共通 state・lock・artifact 操作そのものを調べる場合は、対応する `commons.runtime_feedback_*` の実装を直接読む。
- normalization または verification agent の入力 builder・Structured Output schema の契約だけを調べる場合は、対応する builder と schema を直接読む。
- `cmoc feedback report` 以外のサブコマンドの処理を調べる場合。

## hash
- 45c71abdba7b3f76e0abe83382327c23781810bfdad40c3c3610130693f32c84
