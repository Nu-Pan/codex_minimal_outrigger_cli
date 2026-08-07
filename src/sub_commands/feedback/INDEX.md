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
- `cmoc feedback report` の実行本体として、raw observation の snapshot 固定、増分 normalization、checkpoint 復旧、state snapshot、最終 report record の公開を一つの中断可能な transaction として管理する。
- machine_rule と agent_report の observation を issue へ統合し、invalid・deferred・再発・再検証要否・human disposition の変更を集計して Markdown report を生成する。

## Read this when
- `cmoc feedback report` の事前条件、実行順序、lock、migration、state 整合性検証を確認するとき。
- observation の pending 判定、machine/agent 別の normalization、候補 issue の絞り込み、agent checkpoint の再利用または呼び出し条件を確認するとき。
- normalization unit、ingestion receipt、assessment、state snapshot、report record の公開順序や中断・部分失敗時の復旧処理を確認するとき。
- report の表示対象、machine issue の抑制、再発判定、fingerprint に基づく再検証、Markdown 出力項目を確認するとき。

## Do not read this when
- feedback observation の保存・列挙・immutable file 操作そのものを確認するときは、feedback store の実装を直接読む。
- issue state の record schema、effective state の構築、unit/report publication の共通処理を確認するときは、runtime feedback state の実装を直接読む。
- normalization agent の prompt や Structured Output schema の定義を確認するときは、normalize issue parameter の実装と対応する schema を直接読む。
- `cmoc feedback report` 以外の CLI subcommand の処理や、正本仕様の意図を確認するときは、この report runtime 実装を入口にしない。

## hash
- e970b35f2509afc52be8e0812dc384c723d888aba0d162aabc89671b51da1f4e
