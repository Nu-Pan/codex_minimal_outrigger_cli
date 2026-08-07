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
- `cmoc feedback report` の実行本体を担い、raw observation の snapshot 作成、未処理 observation の増分 normalization、checkpoint/unit の復旧・確定、issue state assessment、state snapshot、最終 Markdown report と report record の公開を一つの中断可能な transaction として管理する。machine rule と agent observation の統合、invalid/deferred/interrupted/partial 状態、表示対象 issue の選別まで扱う feedback report command の中心実装である。

## Read this when
- feedback report の状態機械、snapshot と normalization unit の処理順序、agent normalization の checkpoint 復旧、issue の可視性判定、report/state snapshot の公開処理を変更または調査するとき
- feedback observation の machine_rule・agent_report 統合、再発判定、fingerprint に基づく再検証、invalid または中断時の report 挙動を確認するとき

## Do not read this when
- feedback observation の受け付け・保存形式だけを確認したいときは、観測受付や store の実装を直接読む
- feedback state の record schema、issue view のロード、unit/report publication の低レベル処理だけを確認したいときは、`commons.runtime_feedback_state` または `commons.runtime_feedback_store` を直接読む
- normalization agent に渡す parameter や Structured Output schema の定義だけを確認したいときは、normalization parameter builder と対応する oracle/spec を直接読む

## hash
- ff72718fb3fb2c56aeb3b2fec534070fe4d72dc4eb4606d7a44484b03de97baf
