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
- 対象は `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド固有モジュールです。固定済み report cut を入力に、raw observation の検証、候補の deterministic 集約と agent normalization、全候補の verification、generation/report の staging、current pointer 切替、publication 後 cleanup までを一つの再開可能な transaction として扱います。
- `feedback report` の処理順序、report cut、candidate 集約、checkpoint、publication、cleanup を調べる際の入口です。

## Read this when
- `cmoc feedback report` の全体フローや transaction 境界を確認するとき
- report cut の固定・再開、observation 検証、checkpoint の再利用を確認するとき
- observation から issue candidate と machine aggregate を作る規則を確認するとき
- verification 結果から generation、Markdown report、current pointer を publication する処理を確認するとき
- publication 後の cleanup や中断・失敗時の状態遷移を確認するとき

## Do not read this when
- observation 保存形式や canonical JSON の詳細だけを調べるときは feedback store の実装を直接読む
- active state、generation artifact、current pointer のデータ契約だけを調べるときは feedback state の実装を直接読む
- normalization／verification の agent parameter や schema だけを調べるときは対応する builder と schema を直接読む
- CLI 共通実行制御や subcommand state だけを調べるときは runtime の実装を直接読む
- feedback report の正本仕様を確認するときは対応する oracle 文書を読む

## hash
- 35f7be7463a1087ff746eb0ec6c82b1cdc45508b10fe74e4269fd1d96dc61543
