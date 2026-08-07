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
- feedback report サブコマンドの中核実装。raw observation の snapshot 固定、未処理 observation の validation・増分 normalization、machine/agent issue 統合、checkpoint と unit commit/rollback、assessment 再評価、前回 report との差分計算、表示対象の選別、Markdown report と tracked record の保存までを一つの中断可能な transaction として扱う。feedback report の CLI 入口および処理順序・状態遷移を確認するための入口。

## Read this when
- `cmoc feedback report` の実行フロー、snapshot、deferred/invalid 処理、normalization unit、checkpoint、commit/rollback を調査または変更するとき
- machine observation と agent observation の issue 統合、candidate 選定、assessment、再発判定、表示境界を確認するとき
- feedback report の生成形式、report record、state commit IDs、前回 report との差分を確認するとき

## Do not read this when
- feedback observation の schema や tracked state の record 定義だけを確認したい場合は、対応する runtime feedback state/store または oracle 仕様を直接読む
- feedback report の CLI 呼び出しだけを確認したい場合は、サブコマンドの公開入口を直接読む
- report 生成とは無関係な feedback の記録・収集処理を調査する場合は、この実装全体を読まず該当する収集側モジュールへ進む

## hash
- 3f11befab4dd8b0a012c08cddabbf2144aca11a544eef038df1d322bf5a2d7e5
