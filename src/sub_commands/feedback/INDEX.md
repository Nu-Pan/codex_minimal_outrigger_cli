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
- `cmoc feedback report` の CLI 実装本体。raw observation の snapshot 固定、未処理 observation の増分 normalization、machine/agent observation の issue 統合、checkpoint と unit commit/rollback、assessment 再評価、前回 report との差分判定、可視 issue の選別、Markdown report と tracked report record の保存までを一つの中断可能な transaction として扱う。
- feedback report の事前条件、snapshot と receipt の整合性検査、invalid observation の記録、normalization agent の Structured Output 検証、recurrence threshold、suppression、最終 report の集約を確認する入口。

## Read this when
- `cmoc feedback report` の実行フロー、状態機械、処理順序を変更または調査するとき
- observation の snapshot、normalization unit、checkpoint、unit commit/rollback の挙動を確認するとき
- issue の統合・assessment 再評価・前回 report との差分・既定表示や `--all` の選別規則を調査するとき
- feedback report の Markdown 出力や tracked report record の生成内容を変更するとき

## Do not read this when
- feedback observation の envelope、issue view、record schema、tracked state の基本構造だけを確認したいときは、共通 feedback state の実装・仕様を直接読む
- normalization agent に渡す parameter や Structured Output schema の定義だけを確認したいときは、feedback normalization builder と対応する schema を直接読む
- report command 以外の feedback subcommand の挙動を調査するときは、その subcommand の実装または正本仕様を直接読む

## hash
- 1f1b7c291cd7722d19ee3a9cf730ee219a90eec82032405699b27fbf30b79c1c
