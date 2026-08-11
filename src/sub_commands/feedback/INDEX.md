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
- `cmoc feedback report` の active-state publication pipeline を実装するモジュール。固定済み report cut を入力に、raw observation の検証、agent/machine candidate の deterministic 集約、必要な normalization と全 candidate の verification、report・generation artifact の staging、current pointer 切替、publication 後の cleanup までを一つの再開可能な transaction として処理する。
- report cut、normalization checkpoint、verification checkpoint の入力・実装・schema hash を検証し、中断や失敗時に同じ固定入力から安全に再開できるようにする。candidate の current evidence は report cut が許可した repository reference に限定し、active issue と Markdown report へ secret masking を適用する。

## Read this when
- `cmoc feedback report` の CLI 実行フロー、事前条件、report cut の固定・再開・失敗状態を確認するとき。
- feedback observation から issue candidate を作る deterministic normalization、machine recurrence 集約、agent observation の同一性判定を変更・調査するとき。
- feedback issue candidate の verification、checkpoint の再利用条件、current evidence の許可範囲を確認するとき。
- feedback report の generation artifact、Markdown 出力、current pointer 切替、publication 後 cleanup の transaction 境界を確認するとき。

## Do not read this when
- feedback observation の envelope、raw store、canonical JSON、secret masking の共通処理だけを確認したい場合は、feedback store の runtime モジュールを直接読む。
- normalization または verification の agent prompt・Structured Output schema の仕様だけを確認したい場合は、対応する builder と oracle schema を直接読む。
- active state、generation artifact、checkpoint path、current pointer の共通データ構造や永続化処理だけを確認したい場合は、feedback state runtime モジュールを直接読む。
- `cmoc feedback report` 以外のサブコマンドの処理や、report 表示以外の UI を調査するとき。

## hash
- 255fce57605e9450f52013207b3d35bd07b116c16bc434699fab2bcf56b3897e
