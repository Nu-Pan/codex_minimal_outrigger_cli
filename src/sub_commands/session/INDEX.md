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
- 現在の local branch から cmoc 管理対象の session branch と state file を作成する CLI 実装。active session の重複確認、clean worktree 検証、session-id 衝突回避、branch/state 作成、結果表示を担う。作成途中の失敗時には branch と state file をロールバックし、復旧情報を含むエラーを報告する。

## Read this when
- `cmoc session fork` の branch 作成、session state 保存、session-id 生成、競合制御、失敗時ロールバックの挙動を変更・調査するとき。

## Do not read this when
- session の join・abandon など、fork 実行以外のライフサイクル処理を確認するとき。
- session state のデータ構造や共通 runtime 関数の仕様を直接確認する必要があるとき。

## hash
- 9f402913f831a35fc4e90001691620f8eed657cda8878eeb7ae91320860736e7

# `join.py`

## Summary
- active な session branch を session home branch へ merge し、事前条件確認、conflict 解消、状態更新、branch 削除、結果表示までを担う session join の実装。
- merge conflict 発生時の対象列挙、feedback state の安全な処理、Codex による marker 解消、許可外変更の検査、stage・commit を含む conflict resolution の入口でもある。

## Read this when
- `cmoc session join` の実行条件、merge 先、session state の更新、session branch 削除条件を変更・調査するとき。
- session join の merge conflict 処理、conflict marker 検査、Codex 呼び出し、変更範囲制限、feedback state conflict の扱いを変更・調査するとき。
- session join の git 操作、worktree の clean 判定、エラー出力先、結果表示を変更・調査するとき。

## Do not read this when
- session の作成・実行・離脱など、session join の merge と後始末に直接関係しない subcommand を扱うとき。
- conflict resolution parameter のプロンプト仕様そのものを変更するときは、まずその parameter builder の実装を読む。
- CLI 共通の状態管理、git 実行、結果処理の一般仕様だけを確認する場合は、対応する共通 runtime の実装を直接読む。

## hash
- c68a36e4aa56bc3be3a0c498e5494da7619c107f9746554896e8ae5aa3658f4e
