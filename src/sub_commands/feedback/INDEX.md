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
- `cmoc feedback report` サブコマンドの実行本体で、raw observation の snapshot 固定、未処理 observation の増分 normalization、invalid/integrated receipt の確定、checkpoint・unit manifest の復旧、issue assessment の再評価、state snapshot と Markdown report の publication を一連の中断可能 transaction として管理する。
- machine_rule observation の canonical key 統合と、agent observation の候補 issue 絞り込み・必要時の normalization agent 呼び出しを扱う。report では issue の変更、再発中 open issue、再検証要否、表示抑制、deferred/invalid 件数を集計し、`--all` を含む可視化内容を生成する。
- feedback report の CLI 前提条件、writer lock、状態整合性検証、再実行時の receipt/checkpoint 再利用、ユーザー中断・部分失敗の記録、最終 report record の公開までを確認したい場合の入口である。

## Read this when
- `cmoc feedback report` の実行フロー、transaction 順序、snapshot・normalization unit・state snapshot・report record の関係を調べるとき。
- machine rule と agent observation が issue に統合される条件、normalization agent の checkpoint 再利用、候補外 issue ID の拒否を確認するとき。
- report の表示対象、再発判定、fingerprint による needs_revalidation 判定、`--all` と既定表示の差を確認するとき。
- feedback report の中断・部分失敗・corruption 検出時の復旧と終了結果を調べるとき。

## Do not read this when
- feedback observation の入力 schema、state record のデータモデル、共通 persistence API の詳細だけを調べるときは、それぞれの oracle または `commons.runtime_feedback_state`・`commons.runtime_feedback_store` を直接読む。
- normalization agent に渡す parameter や Structured Output schema の定義だけを調べるときは、`acp.builder.feedback.normalize_issue` と対応する schema を直接読む。
- feedback report 以外のサブコマンドの実行制御、共通 CLI runtime、ログ、path、result validation の仕様だけを調べるときは、対応する共通 runtime モジュールを直接読む。

## hash
- a130a5b359986f38372723c535cf80ca1a72eea1549849eb806e32949ad30f98
