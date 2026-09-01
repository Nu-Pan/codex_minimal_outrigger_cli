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
- active session を home branch に取り込まず abandoned 状態へ変更し、session branch を削除する CLI 処理の実装。
- 事前条件の検証、home branch への切替、state 更新、session branch の cleanup、および失敗時の state・branch rollback を扱う。

## Read this when
- `cmoc session abandon` の実行経路や、active session を破棄する処理を確認・変更するとき
- cleanup 失敗時に session を再実行可能な状態へ戻す rollback 挙動を確認するとき

## Do not read this when
- session の開始・再開・完了など、abandon 以外のライフサイクル処理を確認するとき
- session 共通の状態形式や git 操作の一般仕様を確認することが目的で、共通実装または正本仕様を直接読む方が適切なとき

## hash
- 10bde8b05c4789feab0fc3d5e4f27fdae231b518bd24a47acbf3521617863a6d

# `fork.py`

## Summary
- 現在の通常の local branch から cmoc session branch と session state を作成する session fork の実装。
- 既存 active session と session-id の衝突を確認し、worktree の clean 状態を要求したうえで fork を実行する。
- branch 作成や state 保存に失敗した場合は、作成済み branch と state file を可能な範囲で rollback し、失敗状況を報告する。

## Read this when
- `cmoc session fork` の実行前提、session branch の分岐元、session state の保存処理を確認したいとき。
- session-id が既存 branch や state file と衝突しない仕組みを確認したいとき。
- session fork の失敗時に branch 切り替え、branch 削除、state file cleanup がどう処理されるかを追うとき。

## Do not read this when
- session の join や abandon の処理を確認したいとき。
- SessionState のデータ形式や state file の一般的な仕様を確認したいとき。
- session fork 以外の CLI サブコマンドの挙動を調べたいとき。

## hash
- faf5a81034d58cc1120d2c5049ba3c74fde713f2fb5c92d6fe2dc22ef507be21

# `join.py`

## Summary
- session branch を home branch へ安全に merge し、merge conflict の解消と完了状態を検証する実行入口。
- conflict 対象の列挙、Codex による marker 解消、許可範囲外の差分・marker・unmerged path の検査、merge 完了を扱う。
- merge 後に session state を joined へ更新し、ancestor 判定に基づいて local session branch の削除を行う。

## Read this when
- `cmoc session join` の実行経路、session branch と home branch の merge 前提条件、または merge 後の state 更新を確認するとき。
- session join の conflict 解消方針、Codex 呼び出し後の差分制限、conflict marker や unmerged path の検証を調べるとき。
- session branch の削除条件や、merge 結果・警告を含む terminal result の扱いを確認するとき。

## Do not read this when
- session の状態形式や branch のライフサイクル全般を確認したい場合は、session state の仕様を直接読むとき。
- conflict 解消パラメータの生成内容だけを確認したい場合は、conflict resolution builder を直接読むとき。
- 共通の CLI 実行ラッパー、Git 操作、report 更新の一般仕様だけを確認したい場合は、それぞれの共通実装・仕様を直接読むとき。

## hash
- 81bce26eb277ba3590b158ca91358efba4c73001d8e31f1c7441c179bc6f3a1e
