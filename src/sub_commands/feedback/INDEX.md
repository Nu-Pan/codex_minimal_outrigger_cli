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
- `cmoc feedback report` の CLI 実装本体。raw observation の snapshot 固定、未処理 observation の増分 normalization、checkpoint・unit manifest・state snapshot の保存、最終 Markdown report と publication record の生成を、一つの中断可能な transaction として管理する。
- machine_rule と agent_report の observation を issue に統合し、invalid observation、重複候補、assessment の再評価、deferred observation、表示対象・抑制対象を算出する。feedback report サブコマンドの状態機械を確認・変更する際の入口。

## Read this when
- `cmoc feedback report` の snapshot、normalization、checkpoint、unit publication、report publication の処理を調査・変更するとき。
- machine observation と agent observation の issue 統合、candidate 選定、assessment freshness、再発判定、既定表示の規則を確認するとき。
- feedback report の中断・部分完了・corruption recovery や session/run の事前条件を確認するとき。

## Do not read this when
- feedback observation の受付や保存だけを調べるときは、observation 書き込み側の実装を直接確認する。
- feedback state の record schema、lock、recovery primitive、issue view の構築を調べるときは、runtime feedback state/store の実装を直接確認する。
- normalization agent に渡す parameter や Structured Output schema の定義だけを調べるときは、feedback normalization builder と対応する oracle schema を直接確認する。
- report Markdown の一般的な出力先や timestamp path の共通処理だけを調べるときは、runtime paths の実装を直接確認する。

## hash
- a2aea90660cf3644c9d6c264ce5315c532a9433c620046d12178db3613aeb62a
