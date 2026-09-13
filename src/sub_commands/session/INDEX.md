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
- アクティブな session branch を対応する home branch にマージし、必要に応じて Codex CLI に conflict 解消を依頼したうえで、解消結果・merge 完了・session state 更新・session branch の削除を検証する session join の実行入口。
- session join の事前条件、merge conflict の安全な列挙と解消確認、変更 path の stage、merge 後の branch cleanup を調べるときの入口。

## Read this when
- session branch の成果を home branch に統合する処理を変更・レビューするとき
- merge conflict の解消依頼、conflict marker 検査、unmerged path 検証の挙動を確認するとき
- session state の joined 更新や、merge 到達性に基づく session branch 削除の条件を確認するとき

## Do not read this when
- session fork、session abandon、または session の状態モデル自体を調べるとき
- conflict 解消 agent に渡す指示内容だけを確認したいとき
- 共通の Git path status、runtime、primary report 更新処理の実装を直接調べるとき

## hash
- 864dbbdf240351ad902b4975e52df63434654a3c4a2fff6ec4ee6bebf9ffbc5b
