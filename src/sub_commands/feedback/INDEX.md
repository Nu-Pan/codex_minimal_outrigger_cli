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
- feedback report コマンドの中心実装。raw observation の snapshot 固定、未処理 observation の normalization、invalid receipt、machine/agent issue 統合、checkpoint、unit 単位の commit/rollback、assessment 再評価、前回 report との差分計算、Markdown report と tracked report record の生成までを一連の中断可能 transaction として扱う。
- feedback report の状態機械や normalization の順序・境界を確認する必要がある場合の主要な入口であり、個別の正規化ルール、永続 state の record schema、CLI 実行基盤そのものを調べる場合は対応する import 先を直接読む。

## Read this when
- cmoc feedback report の実行順序、snapshot、deferred/invalid 処理、machine または agent observation の issue 統合を変更・調査するとき
- normalization checkpoint の再利用、unit commit/rollback、assessment の再評価、report の表示・抑制条件を確認するとき
- report の front matter、issue 差分、tracked report record、部分失敗・中断時の挙動を確認するとき

## Do not read this when
- 個別の observation schema や feedback record のデータ構造だけを確認する場合は、runtime feedback state/store の定義を直接読む
- normalization agent に渡す parameter や Structured Output schema だけを確認する場合は、feedback normalize builder と schema を直接読む
- CLI 共通実行、ログ、session state、git 操作の共通仕様だけを確認する場合は、対応する runtime module や oracle specification を直接読む

## hash
- 76513f6cf3c1cf4485174493038e2851d909868302d875b7cc4a5b632581c0c3
