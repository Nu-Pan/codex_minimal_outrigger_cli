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
- `cmoc feedback report` の report cut 固定から、normalization・全 candidate verification・正常 publication または incomplete 診断までを一つの transaction として実行する CLI runtime。
- raw observation、active state、repository reference、処理バージョンを固定し、checkpoint による中断後の再開と deterministic な issue 集約を管理する。
- verification 結果に基づき active generation・Markdown report・current pointer を publication し、判定不能 candidate がある場合は通常 publication せず診断 report を保存する。
- feedback report サブコマンドの状態遷移、cleanup、interruption、publication ログを実装する下位実装への入口。

## Read this when
- `cmoc feedback report` の report cut、checkpoint 再開、candidate 集約、verification、publication、incomplete 診断の挙動を変更または調査するとき。
- feedback raw observation と active state から current report が生成される処理経路を確認するとき。
- publication 前後の中断処理、artifact cleanup、current pointer 更新、subcommand log 記録を確認するとき。

## Do not read this when
- feedback observation の保存・envelope 検証だけを扱うときは、raw observation の store 実装を直接読む。
- issue normalization または verification 用 prompt・Structured Output schema の契約だけを扱うときは、対応する builder と schema を直接読む。
- feedback state のデータ契約や report サブコマンドの正本仕様を確認するときは、対応する oracle file を読む。

## hash
- af5d2483affbd930c32cf16dfab300ca699ce37f184263262438017c55a22ed3
