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
- active な session branch を session home branch へ merge し、成功時に session state を joined へ更新して branch 削除を試みる CLI 実装。
- merge conflict 発生時は conflict 対象だけを Codex CLI に解消させ、marker 外の内容や無関係な差分を検査したうえで stage・commit まで行う。
- session join の事前条件検証、Git の unmerged path・変更 fingerprint・conflict marker の安全な扱い、結果表示と警告報告を担う。

## Read this when
- session join コマンドの実行条件、merge 手順、state 更新、session branch 削除の挙動を確認するとき
- session join における conflict resolution の許可範囲や、Codex 実行前後の差分検査を変更・調査するとき
- session branch の merge 完了判定、NUL framing による path 処理、conflict marker 検出の実装を確認するとき

## Do not read this when
- session の作成・開始・終了など、join 以外のライフサイクル処理を確認するとき
- conflict resolution 用 prompt の仕様そのものや Codex 実行共通ルールを確認するときは、それぞれの専用仕様を直接読むとき
- session join の外部向け仕様ではなく、一般的な Git 操作や共通 CLI 実行基盤だけを調査するとき

## hash
- 7f428d41e416526549d0e37f36c5928a413f2cf428681cb4313da5d5777c53f3
