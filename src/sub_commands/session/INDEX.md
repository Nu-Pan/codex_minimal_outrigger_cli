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
- session abandon サブコマンドの実行処理を担い、active session を home branch に取り込まず abandoned 状態へ遷移させて session branch を削除する入口。
- 事前条件の検証、home branch への切替、state 更新、session branch cleanup、失敗時の state・branch rollback、terminal result の確定を一体として扱う。

## Read this when
- session abandon の CLI 挙動、実行前の session・worktree・branch 条件、cleanup の成否、または cleanup failure 時の rollback を確認・変更するとき。
- session lifecycle の join/fork と競合する abandon 処理の直列化や、abandon 完了時の報告項目を追跡するとき。

## Do not read this when
- session の作成・fork・join の処理だけを調べるとき。
- session abandon の内部処理ではなく、共通の CLI 実行基盤や state 永続化の一般仕様を直接確認したいとき。

## hash
- 3f24331daa9d8193978b19f952cd32e6c068197134c76293065feb0cb44ec987

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
- session branch を home branch に merge し、conflict 解消の検証と後処理まで行う session join の実装責務を扱う。
- session join の事前条件、Git merge、conflict 解消 agent の変更範囲検査、marker・unmerged path の確認、状態更新と session branch 削除を確認する入口。

## Read this when
- session join の実行フロー、merge 対象 branch、事前条件、merge 後の session 状態更新を調べるとき。
- merge conflict 発生時の解消依頼、許可される差分、conflict marker・unmerged path の検証、merge commit の確定条件を確認するとき。
- session branch の cleanup 論理や削除警告、primary report の進捗項目を追跡するとき。

## Do not read this when
- session を fork、abandon、または別の subcommand として操作する処理だけを調べるとき。
- conflict resolution parameter の具体的な agent 指示文だけを確認したい場合は、conflict resolution builder の定義を直接読むとき。
- session state のデータ構造や共通 Git・runtime helper の一般仕様だけを確認する場合。

## hash
- af434472386e37dbe94e11bd7377a2c67df8b69fa9f1d027fc5ed2ce9585aa41
