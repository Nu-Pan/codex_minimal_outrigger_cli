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
- `cmoc session abandon` の CLI 実装。active な session branch の事前条件を検証し、home branch へ切り替えたうえで session state を abandoned に更新し、session branch を削除する。cleanup 失敗時の state・branch rollback と利用者向け結果表示も扱う。

## Read this when
- session abandon の実装、事前条件、branch cleanup、state rollback、または結果表示を変更・確認するとき。

## Do not read this when
- session の開始・参加・完了処理を扱うとき。共通の git 操作や state 操作の仕様を確認する場合は、まずそれぞれの共通実装・仕様を読むとき。

## hash
- 1a597407cf2b4b722889f500fc4b7aaf1781ac8dc2e100ef55319e593821197d

# `fork.py`

## Summary
- 通常の local branch から cmoc の session branch と session state を作成する CLI 実装。既存 active session の確認、clean worktree 検証、HEAD 保存、session-id 衝突回避、branch/state 作成、失敗時 rollback、結果表示までを扱う。session 作成処理の実装へ進む入口。

## Read this when
- `cmoc session fork` の動作、前提条件、session branch/state の生成、session-id の一意性、作成失敗時の rollback を変更・調査するとき。
- session fork と home branch の競合防止や lock 内での再確認を確認するとき。

## Do not read this when
- session の join、abandon、state schema 自体の仕様を確認したいとき。
- CLI 共通実行基盤や git/state 操作の共通 helper の詳細を直接調べるとき。

## hash
- f68e1c62fc0dffea0410050425b5572fb5ae503c3fc648a5d1178fe42d3c53d6

# `join.py`

## Summary
- session join サブコマンドの CLI 実装。active な session branch の事前条件を検証し、session home branch へ non-fast-forward merge する。
- merge conflict 発生時は対象を NUL 区切りで列挙し、Codex CLI に解消を依頼した後、conflict marker・stage 状態・merge 完了を検証して commit する。
- merge 成功後は状態を joined に更新し、session branch が HEAD から到達可能な場合だけ削除し、結果と警告を表示する。

## Read this when
- session join の実行条件、merge・conflict 解消・branch 削除の挙動を変更または確認するとき
- session join のエラー出力先、状態更新、結果表示を調査するとき
- conflict 対象の検出や conflict marker 検証の実装を変更するとき

## Do not read this when
- session join 以外の session サブコマンドの挙動だけを調べるとき
- 共通の Codex 実行規則だけを確認する場合は、共通規則の oracle file を直接読むとき
- session branch や session state のデータモデル自体を変更・確認するときは、その定義元を直接読むとき

## hash
- f80be9db336f02273fa6e326a3214b5abd642deb042a6ded78a3f3e31ebde9c0
