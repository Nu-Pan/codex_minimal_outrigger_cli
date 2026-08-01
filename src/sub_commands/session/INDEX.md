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
- `session join` サブコマンドの実装。active な session branch の事前条件を確認し、session home branch へ merge した後、状態更新・branch 削除・結果表示までを担当する。merge conflict 発生時の Codex CLI による解消、NUL 区切りの conflict 対象取得、conflict marker 検査も含む。

## Read this when
- `cmoc session join` の挙動、事前条件、merge・conflict 解消・後始末を変更または調査するとき
- session branch の削除条件、state 更新、エラー出力先、結果表示を確認するとき
- session join に関する Git 操作や conflict marker のテストを追加・修正するとき

## Do not read this when
- session の作成・実行・終了など、`session join` 以外のサブコマンドだけを扱うとき
- session join の conflict 解消パラメータ生成自体を変更するときは、conflict resolution builder の実装を直接読む
- 共通の Git 実行、state 管理、CLI ランタイムの仕様だけを確認するときは、対応する共通モジュールや oracle 文書を直接読む

## hash
- e976577e9c3747cad1e6bcc24ebed882043e694a422fde579860926a11e76528
