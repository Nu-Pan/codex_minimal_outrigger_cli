# `__init__.py`

## Summary
- session サブコマンドの実装パッケージ。session サブコマンドに関する実装を確認する際の入口となる。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。

## hash
- bfd8539ef9776e0e27e2e2e0d6365626dc832eb3abf90403affec4b29f1f8364

# `abandon.py`

## Summary
- active な session branch の事前条件を検証し、未 join の run や dirty worktree を拒否する session abandon サブコマンドの実装。
- home branch へ切り替え、session state を abandoned に更新したうえで session branch を削除する cleanup 処理。
- cleanup 中の失敗・中断時に state と session branch を active 状態へロールバックし、再実行可能性と失敗詳細を報告する処理。

## Read this when
- `cmoc session abandon` の事前条件、home branch への切り替え、session branch 削除の挙動を変更・確認するとき。
- session abandon の cleanup 失敗時のロールバック、エラー報告、再実行可能性を調査するとき。

## Do not read this when
- session の join や fork のライフサイクル全体を確認したいときは、対応するサブコマンド実装や session 仕様を直接読む。
- run abandon 単体の挙動や一般的な CLI 実行基盤を確認したいときは、それぞれの実装対象を直接読む。

## hash
- 1f77a2d356b51d2ef653868dbaf4661146a20bf1ab74457ee31e8c353871cde9

# `fork.py`

## Summary
- 現在の通常の local branch を起点に、session branch と session state を排他的に作成する `cmoc session fork` の実行処理。前提検証、fork 元 commit の固定、session-id 衝突回避、作成失敗時の rollback、CLI 結果の確定までを担う。

## Read this when
- `cmoc session fork` の branch・state 作成フロー、同一 home branch での競合防止、作成失敗時の復旧動作を確認・変更するとき
- session-id の生成条件や既存 branch/state との衝突処理を確認するとき

## Do not read this when
- session の join・abandon など、fork 後の状態遷移そのものを確認したいときは、それぞれの session 操作用実装を直接読む
- session state のデータ形式や永続化仕様だけを確認したいときは、state 定義・永続化処理を直接読む
- CLI 全体の共通実行ラッパーや Git 操作の一般的な挙動だけを確認したいときは、共通 runtime 実装を直接読む

## hash
- fa5f8734a893ac8545c67fa88c0fb50107b2e37a49b4b542812966d365dfad2e

# `join.py`

## Summary
- `cmoc session join` の実行本体と、merge conflict の検出・Codex による解消・検証を担う実装。active な session branch を home branch に merge し、状態更新と session branch の削除まで行う。

## Read this when
- session branch を home branch へ参加させる処理の事前条件、merge、状態更新、後始末を確認したいとき。
- session join 中の conflict 対象列挙、marker 検査、stage、commit の流れを確認したいとき。

## Do not read this when
- session の fork や abandon の処理を確認したいとき。
- conflict resolution parameter の構築内容そのものを確認したいときは、対応する builder 実装を直接読むべき。

## hash
- f5e66b3bd1eddafe6db63d5dc50c2382e13e25be362483fda5d765d0148c3e3e
