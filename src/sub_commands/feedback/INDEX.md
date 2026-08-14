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
- `cmoc feedback report` の publication／diagnostic pipeline を実装する中核 module。固定済み report cut を作成し、raw observation と current state の参照を検証・固定する。
- deterministic な candidate 集約、machine recurrence 集約、必要時の issue identity normalization、全 candidate の verification、checkpoint の保存・再利用を一つの transaction として扱う。
- 全 verification が確定した場合は generation、Markdown report、current pointer を hash 付きで publication し、raw observation・checkpoint・旧 generation の cleanup まで進める。`inconclusive` がある場合は active generation を変更せず、incomplete 診断 report を保存する。
- 中断・失敗・publication 再開・cleanup 未完了を report-cut state と subcommand log に反映する。report の正本仕様、状態契約、normalization／verification の詳細契約を確認する場合は、本文冒頭に示された対応 oracle file や各 builder／schema が直接の入口になる。

## Read this when
- `cmoc feedback report` の処理順序、report cut、checkpoint 再開、publication、incomplete 診断の責務を確認するとき
- feedback observation から active issue candidate と machine aggregate を構築する処理を変更・調査するとき
- verification 結果から generation、current pointer、Markdown report、cleanup を確定する経路を確認するとき
- 中断時の状態更新、publication_ready の再開、cleanup failure の扱いを確認するとき

## Do not read this when
- feedback state の正本データ契約や状態遷移そのものを確認したいときは、対応する feedback_state oracle file を直接読む
- `cmoc feedback report` の利用条件や外部仕様を確認したいときは、sub_command/feedback_report oracle file を直接読む
- normalization または verification の agent prompt、Structured Output schema、builder の入出力契約だけを確認したいときは、各 builder／schema を直接読む
- 共通の runtime state、feedback store、logging、publication artifact の実装だけを確認したいときは、対応する `commons` module を直接読む

## hash
- 3824efa12e50fa9697e81745e05673d268f57239ac9eee9edd9343783ca6b382
