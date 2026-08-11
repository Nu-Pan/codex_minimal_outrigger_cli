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
- `cmoc feedback report` の active-state publication pipeline を実装するモジュール。固定済み report cut を起点に、raw observation の検証、agent/machine candidate の deterministic 集約、必要な normalization、全候補の verification、generation・Markdown report の作成、current pointer 切替、publication 後の cleanup までを一つの再開可能な transaction として扱う。
- report cut、checkpoint、generation、current pointer の hash/reference を検証し、処理中断・失敗・cleanup 未完了から安全に再開できる状態機械を提供する。feedback report サブコマンドの実行フローと publication 整合性を確認する際の入口であり、詳細な state schema やサブコマンド仕様は対応する oracle 文書を読む。

## Read this when
- `cmoc feedback report` の実行順序、report cut の固定、candidate 集約、normalization/verification、publication、再開・中断処理を変更または調査するとき。
- raw observation、active state、checkpoint、generation artifact、current pointer の整合性検証や cleanup の挙動を確認するとき。
- feedback report の Markdown 出力、machine rule の recurrence 集約、agent observation の issue identity 判定の実装を確認するとき。

## Do not read this when
- feedback の raw observation 保存形式や active state の共有ユーティリティだけを確認する場合は、対応する `commons` の実装を直接読む。
- normalization または verification agent の prompt・Structured Output schema 自体を確認する場合は、対応する builder と schema を直接読む。
- `cmoc feedback report` 以外のサブコマンドの処理や、report cut の正本仕様を確認する場合は、この実装ではなく該当するサブコマンド仕様・oracle 文書へ進む。

## hash
- c42649c0b7c336ba0ad569ea0c9fb6f1f62c0f14ec78ffa70babf82f62795269
