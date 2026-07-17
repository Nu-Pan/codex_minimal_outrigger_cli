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
- `cmoc session abandon` サブコマンドの実装。active な session branch の事前条件と clean worktree を確認し、home branch へ切り替えたうえで session state を abandoned に更新し、session branch を削除する。cleanup 失敗時は state と branch を可能な範囲で rollback し、詳細なエラーを返す。正常時は破棄した branch、切替先、session state を CLI に表示する。

## Read this when
- `cmoc session abandon` の動作、事前条件、home branch への切替、session state 更新、session branch 削除を変更・確認するとき
- cleanup 失敗時の rollback、エラー詳細、再実行可能な状態への復帰を調査するとき
- session abandon の CLI 出力や runtime 呼び出し手順を確認するとき

## Do not read this when
- session の作成・join・merge など、abandon 処理以外のライフサイクルを調査するときは、対応するサブコマンド実装や oracle を直接読む
- 共通の git 操作、state 永続化、CLI runtime の一般仕様だけを調査するときは、`cmoc_runtime` の実装や対応する oracle を直接読む

## hash
- e4d92bf3ecad58d40d9a03288f2d22cc2a45c147fff58bc4efa0047a0f9f1b4a

# `fork.py`

## Summary
- `cmoc session fork` サブコマンドの実装。現在の通常 local branch と clean worktree を検証し、競合を防ぎながら session branch と session state を作成する。作成失敗時は branch・state のロールバックを試み、結果を CLI に表示する。

## Read this when
- `cmoc session fork` の作成処理、session branch/state の初期化、重複 session 防止、失敗時ロールバックを確認・変更するとき。
- session-id の生成条件や branch/state の衝突回避を確認するとき。

## Do not read this when
- session の join、abandon、state schema 自体の仕様を確認するとき。
- CLI 共通実行基盤や git 操作 helper の実装を直接調査するとき。

## hash
- 7d283a1d85a7a5a3a83ec3a2c348e9a7a636591d5e430db7284da1f71535d8e9

# `join.py`

## Summary
- `session join` サブコマンドの実行処理と、merge conflict の自動解消を担当する。active な session branch を session home branch へ merge し、成功後に状態更新・branch 削除・結果表示を行う。
- 事前条件検証、clean worktree 要求、merge 到達可能性に基づく branch 削除、stderr へのエラー通知、NUL framing による conflict 対象取得、conflict marker 検査・stage・commit を扱う。

## Read this when
- `cmoc session join` の挙動、事前条件、merge 後の状態更新や session branch 削除を変更・調査するとき
- session join 時の merge conflict 解消、conflict marker 検査、Git の unmerged path 処理を変更・調査するとき
- session join の Codex 実行時の worktree と repo-root の扱いを確認するとき

## Do not read this when
- session の作成・apply・離脱など、join 処理や merge conflict 解消に直接関係しない機能を調査するとき
- 共通 runtime や conflict resolution parameter の定義そのものを変更・調査するときは、それぞれの定義元を直接読む

## hash
- 7a56baec6b15301b4c3ff0a0abf49b3c1d2a79c195328726286f47b936ca106c
