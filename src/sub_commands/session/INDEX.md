# `__init__.py`

## Summary
- session 系サブコマンド実装を収めるパッケージであることを示す、最小限のパッケージ初期化モジュール。
- 具体的な処理や公開 API は定義せず、下位モジュールへ進むための入口として位置づく。

## Read this when
- session 系サブコマンド実装のパッケージ境界や、パッケージ自体に初期化処理があるかを確認したいとき。
- session 配下の実装を調べる前に、この階層がサブコマンド実装用のまとまりかだけを確認したいとき。

## Do not read this when
- 個別の session サブコマンドの処理、引数、入出力、状態操作を調べたいとき。その場合は具体的な実装モジュールを読む。
- 共通 CLI ルーティング、サブコマンド登録、または session 以外のサブコマンド実装を調べたいとき。

## hash
- a2616b13a1c260f66ad6dfda2f7821fc573b581179e92bbad014a023d5958042

# `abandon.py`

## Summary
- active な session branch を home branch に merge せず破棄する CLI サブコマンド実装。事前条件の検証、home branch への切替、session state の abandoned 更新、session branch の削除、失敗時のロールバック、結果表示を扱う。

## Read this when
- `cmoc session abandon` の挙動、事前条件、state 更新、branch cleanup、失敗時ロールバックを変更または確認するとき。

## Do not read this when
- session の開始・参加・完了など、abandon 以外のサブコマンドを扱うとき。共通 CLI runtime や state 操作の仕様を確認する場合は、それらの実装または正本仕様を直接読むとき。

## hash
- 28a1100aa48b87a06a5863f1612fff40a710c6e5b79967aec2391feb7ff1c25c

# `fork.py`

## Summary
- 現在の local branch から cmoc session branch と session state を作成する CLI 実装。既存 active session の確認、clean worktree 要求、session-id 衝突回避、branch/state 作成時の rollback、作成結果表示を扱う。

## Read this when
- `cmoc session fork` の作成処理、session branch または session state の初期化、作成失敗時の rollback を変更・調査するとき。
- session-id の一意性確認や home branch 上の active session 競合を調査するとき。

## Do not read this when
- session の join、abandon、state schema 自体の仕様や処理を確認したいときは、それぞれの専用実装・仕様を直接読む。
- 共通の git 操作、CLI 実行基盤、session state 操作の一般実装だけを確認したいとき。

## hash
- f2404006e55dac3cb99692735a54944ce191f2914e00cb57d0b561d46e4c7bad

# `join.py`

## Summary
- `cmoc session join` の CLI 実行処理を担う。active な session branch の事前条件を確認し、session home branch へ merge し、必要時は Codex CLI に conflict 解消を依頼する。merge 後の状態保存、session branch 削除判定、警告表示までを扱う。

## Read this when
- `cmoc session join` の挙動、事前条件、merge・conflict 解消、branch 削除、結果表示を変更または調査するとき。
- session join に関係する Git path の扱い、conflict marker 検査、Codex 実行の作業ディレクトリを確認するとき。

## Do not read this when
- session join 以外の session サブコマンドを変更・調査するときは、対象サブコマンドの実装へ直接進む。
- conflict 解消パラメータの生成仕様だけを確認する場合は、conflict resolution builder の実装を直接読む。

## hash
- 53cf65b89a6cb47a2c6063a7cf5570a1e39a8b9cf3ed06bc6f0aca651b6aaaaa
