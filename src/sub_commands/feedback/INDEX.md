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
- `cmoc feedback report` の active-state publication pipeline を担う実装。固定した report cut を入力として、raw observation の検証、agent observation の candidate 集約・同一性判断、machine recurrence の集約、全 candidate の verification、generation/report の作成、current pointer 切替、publication 後の cleanup と中断・再開処理までを一つの transaction として実行する。feedback report の処理順序、checkpoint 再利用、固定参照、publication 状態遷移を変更・調査するときの主な入口である。

## Read this when
- `cmoc feedback report` の実行フロー、report cut、normalization、verification、publication、current pointer 切替、cleanup、または中断後の再開挙動を確認・変更するとき。
- feedback observation から active issue candidate や machine aggregate が生成される条件、同一性判断、verification 結果の反映を確認するとき。
- feedback report の durable checkpoint、固定入力・repository reference の検証、publication の atomicity や再実行安全性を調査するとき。

## Do not read this when
- feedback observation の保存・canonical validation・参照取得だけを変更または調査する場合は、feedback store／state の実装を直接読む。
- issue normalization や verification agent の入力契約・Structured Output schema 自体を確認する場合は、対応する builder と schema を直接読む。
- feedback report の正本仕様や interruption policy の意図を確認する場合は、対応する oracle specification を直接読む。
- Markdown report の表示形式だけを確認する場合は、描画関数または report 仕様を直接読む。

## hash
- 746a6f79ef543e5b8fa4eb690def1ffd72879643ed0472fd24343cf2211089a9
