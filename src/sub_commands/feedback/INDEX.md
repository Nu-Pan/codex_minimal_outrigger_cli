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
- `cmoc feedback report` の固定済み report cut を処理するサブコマンド実装。raw observation と active state・repository reference を検証して cut を固定し、machine recurrence 集約、agent issue identity normalization、全 candidate の verification、正常な generation/report publication、または incomplete 診断 report の保存までを checkpoint・writer lock・current pointer と一体で管理する。
- feedback report の中断・失敗・publication 再開・cleanup 再試行を含む transaction 状態機械を担い、canonical JSON、hash、Structured Output schema、reference 制約、secret masking、bounded evidence を検証・永続化する。

## Read this when
- `cmoc feedback report` の実行経路、report cut の作成・再開・破棄、normalization／verification checkpoint、candidate 集約、または publication の挙動を調査・変更するとき。
- feedback report の正常 publication と incomplete 診断、current pointer の切替、active issue／machine aggregate の生成、raw observation cleanup の責務を確認するとき。
- feedback state や feedback report の app specification と実装の対応を確認するとき。

## Do not read this when
- feedback observation の入力形式や保存処理だけを調べる場合は、観測 envelope・raw store を直接定義する対象を先に読む。
- feedback issue の normalization／verification agent prompt や Structured Output schema の内容だけを調べる場合は、それぞれの builder・schema を直接読む。
- report の Markdown 表示形式だけを確認する場合は、report rendering を仕様化する対象を先に読む。

## hash
- 26a3b66fb10275c28f3b157fad0f98fb21102eda9ec05d53482e14d78badb3d4
