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
- 通常の local branch から cmoc session branch を作成し、session state を保存する `cmoc session fork` の実装。既存 active session の検査、clean worktree 要求、session-id 衝突回避、branch/state 作成失敗時の rollback、結果表示を扱う。

## Read this when
- `cmoc session fork` の branch 作成、session state 保存、session-id 生成、競合防止、失敗時 rollback の挙動を変更・調査するとき。

## Do not read this when
- session の join、abandon、state schema の詳細、または session branch の一般的な lifecycle だけを調べるとき。

## hash
- 55018934e7237d68f097a1a48c7c81a65ddd89c93202027155e4c43046f1337d

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
