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
- `cmoc session abandon` サブコマンドの実装。active session を検証し、home branch へ切り替えた後に session branch と state を abandoned としてクリーンアップする。失敗時は state・branch を可能な限りロールバックし、結果または cleanup error を表示する。

## Read this when
- `cmoc session abandon` の事前条件、branch 切り替え・削除、state 更新、cleanup 失敗時の復旧処理を変更・調査するとき。

## Do not read this when
- session の開始・継続・完了など、abandon 処理以外の session サブコマンドを変更・調査するときは、各サブコマンドの実装を直接読む。

## hash
- 4409f62cddd5b057e30bd1769b75c2bbddcfdcb40636b89b68e7075effa1c815

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
