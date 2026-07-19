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
- `cmoc session abandon` サブコマンドの実装。active な session branch の事前条件を検証し、home branch へ切り替えたうえで session state を abandoned に更新し、session branch を削除する。cleanup 失敗時の state・branch ロールバックとエラー報告、および完了結果の CLI 表示を扱う。

## Read this when
- `cmoc session abandon` の挙動、事前条件、branch 切り替え・削除、session state 更新を変更または確認するとき。
- cleanup 失敗時のロールバック処理やエラー詳細の出力を調査するとき。

## Do not read this when
- session の作成・完了・通常の状態管理だけを扱い、abandon 操作に関係しないとき。
- 共通の Git 操作や state 読み書きの実装自体を調査する場合は、まずそれぞれの共通実装を直接読む。

## hash
- 9cf413933851d9243f3611b732bb8f8a5c1dd6611071c4b30f32b9d020982e65

# `fork.py`

## Summary
- 現在の local branch から cmoc 管理対象外の session branch と session state を作成する `session fork` の実装。既存 session の確認、clean worktree 検証、branch/state 作成、失敗時の rollback、session-id 衝突回避、結果表示までを扱う。session fork の branch 作成フローを確認する際の実装上の入口。

## Read this when
- `cmoc session fork` の作成手順、事前条件、競合防止、rollback 挙動を調査・変更するとき
- session-id の生成条件や session state 保存のタイミングを確認するとき
- session branch 作成後のエラー処理やユーザー向け出力を確認するとき

## Do not read this when
- session state の schema やライフサイクル仕様そのものを確認したいとき
- git 操作や CLI 共通実行基盤の詳細を直接確認したいとき
- session fork 以外の session サブコマンドを調査するとき

## hash
- 4cc3a37312cbc50d87b0fb69045b934f49dac12fd1365812cc4e3b3d0193f1ee

# `join.py`

## Summary
- session branch を home branch へ merge し、必要に応じて Codex CLI に merge conflict 解消を依頼する session join の CLI 実装。事前条件確認、conflict 対応、merge 後の状態更新、session branch 削除、安全性警告、結果表示を扱う。

## Read this when
- session join の事前条件、merge、conflict 解消、merge 完了処理、session branch 削除、結果表示を変更・調査するとき。
- Git の unmerged path や conflict marker の検出、NUL framing、Codex CLI の実行コンテキストを確認するとき。

## Do not read this when
- session join 以外の session サブコマンドの挙動だけを調査するとき。
- conflict resolution parameter の生成仕様だけを確認する場合は、専用の conflict resolution 実装を直接読む。

## hash
- 2ce0e70c7995d370def7ddf0c590650e3d76a7f63306d18629dcf3481c04f98d
