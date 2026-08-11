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
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド。固定した report cut に対する raw observation の検証、candidate 集約、normalization、全 candidate の verification、generation・Markdown report の生成、current pointer 切替、publication 後 cleanup を一貫して扱う。
- report cut、checkpoint、参照 artifact、publication 成果物の hash を検証し、中断・失敗時には同じ固定入力から再開できる。active issue と machine aggregate の更新も担当する。

## Read this when
- `cmoc feedback report` の実行条件、全体処理フロー、report cut の固定・再開・中断処理を確認するとき。
- feedback observation から issue candidate と machine aggregate を構築し、normalization・verification を経て active state を更新する挙動を調べるとき。
- generation artifact、Markdown report、current pointer の publication 順序、失敗時の状態遷移、cleanup failure の扱いを確認するとき。

## Do not read this when
- raw observation の保存形式や envelope validation だけを確認したい場合は、feedback store と observation validation の実装を直接読む。
- normalization または verification agent の Structured Output 契約だけを確認したい場合は、対応する builder と schema を直接読む。
- active state や artifact path の共通データモデル・操作だけを確認したい場合は、`commons.runtime_feedback_state` を直接読む。

## hash
- 7c3567f3506fbde495e8a8f66022d524d06fc9f912f2f72115c9f4abfe436ef4
