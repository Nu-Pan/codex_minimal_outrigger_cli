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
- 現在の local branch を起点に cmoc session branch と session state を作成する session fork の実装。既存 session の確認、clean worktree の要求、session-id 衝突回避、branch/state 作成、失敗時の rollback と端末結果の確定を担う。

## Read this when
- `cmoc session fork` の実行フロー、session branch・state の生成、競合防止、rollback 動作を確認または変更するとき。

## Do not read this when
- session fork 以外のサブコマンドの処理を確認するとき。session state のデータ形式そのものや共通 CLI 実行基盤を調べる場合は、それぞれの定義元を直接読むとよい。

## hash
- fd571765175aef4185ab5ebfb1fb6cbe6524d189fefac15b005145b9e911406a

# `join.py`

## Summary
- `cmoc session join` の実行本体と、merge conflict の検出・Codex による解消・検証を担う実装。active な session branch を home branch に merge し、状態更新と session branch の削除まで行う。

## Read this when
- session branch を home branch へ参加させる処理の事前条件、merge、状態更新、後始末を確認したいとき。
- session join 中の conflict 対象列挙、marker 検査、stage、commit の流れを確認したいとき。

## Do not read this when
- session の fork や abandon の処理を確認したいとき。
- conflict resolution parameter の構築内容そのものを確認したいときは、対応する builder 実装を直接読むべき。

## hash
- f5e66b3bd1eddafe6db63d5dc50c2382e13e25be362483fda5d765d0148c3e3e
