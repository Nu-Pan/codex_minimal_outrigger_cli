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
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド本体。固定した report cut を起点に、raw observation の検証、agent/machine candidate の deterministic 集約、normalization と全 candidate verification、生成物の staging、current pointer 切替、publication 後 cleanup までを一つの再開可能な transaction として処理する。
- main worktree・active session branch・ready run state などの事前条件を確認し、writer lock、report cut manifest、hash 付き reference、normalization/verification checkpoint により中断後も同じ固定入力を再利用できるようにする。
- machine rule observation には 30 日 window、日次 bucket、bounded digest、allowlist threshold を適用し、agent observation には category・evidence fingerprint・deduplication hint に基づく比較と必要時の identity normalization を行う。
- verification 結果から unresolved issue、machine aggregate、Markdown report、generation artifact を構築し、成果物の hash を検証してから current pointer を公開する。公開済み cut の再開、ユーザー中断、失敗状態、cleanup warning、publication event の記録も扱う。

## Read this when
- `cmoc feedback report` の処理順序、再開可能な report cut、checkpoint、writer lock、current pointer publication の挙動を確認するとき。
- feedback observation から issue candidate・machine aggregate を作る deterministic processing、deduplication、30 日 recurrence threshold を調査するとき。
- normalization/verification agent call の入力、Structured Output schema の再検証、許可された reference と current evidence の制約を確認するとき。
- feedback report、active generation、cleanup manifest、publication event の生成または障害時の状態遷移を調査するとき。

## Do not read this when
- feedback observation の envelope や active state の永続化形式そのものを確認する場合は、参照される runtime feedback state/store の実装を直接読む。
- normalization・verification の agent prompt や Structured Output schema の正本を確認する場合は、対応する builder と oracle schema を直接読む。
- CLI の一般的な実行基盤、session/run state、ログ機構の共通仕様を確認する場合は、ここではなく `cmoc_runtime` など各共通モジュールを読む。
- publication 後の Markdown report 表示だけを確認する場合は、report の生成処理または実際の出力 artifact を直接読む。

## hash
- 856925b90c2182a09cbb7c288422f3c3f553adc00fa38e65f31f1126a2e0ee8c
