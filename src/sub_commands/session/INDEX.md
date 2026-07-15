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
- `cmoc session abandon` の CLI 実装。session branch 上でのみ実行され、事前条件確認・home branch への切り替え・session 状態の更新・session branch の削除・失敗時の巻き戻しまでを扱う。

## Read this when
- session を破棄して home branch に戻す挙動を確認したいとき。
- cleanup 中の失敗時に state と branch が再実行可能な状態へ戻る条件を確認したいとき。
- session branch 前提、home branch 存在確認、worktree clean 要件、表示メッセージを変更したいとき。

## Do not read this when
- session を merge して終了する挙動を見たいときは、merge 系の subcommand を読む。
- session 作成・参加・通常の state 読み込みだけを扱う変更では、この file は直接読まない。
- CLI の共通 runtime や git 操作の実装確認が目的なら、subcommand 本体ではなく `cmoc_runtime` 側を読む。

## hash
- 28a1100aa48b87a06a5863f1612fff40a710c6e5b79967aec2391feb7ff1c25c

# `fork.py`

## Summary
- `cmoc session fork` の起点です。現在の local branch を session の home branch として扱い、その HEAD から session branch を作成し、session state を保存する処理を追うときに読む。失敗時の rollback と、active session の重複防止を確認したい場合もここが入口になる。

## Read this when
- `cmoc session fork` の実行条件、branch 作成、session state 保存、標準出力の内容を確認したいとき。
- fork 失敗時に home branch への戻し方、session branch の削除、state file の掃除まで含めて挙動を追いたいとき。
- 一意な session-id の生成条件や、既存の session branch / state file との衝突判定を確認したいとき。

## Do not read this when
- session の永続化スキーマだけを確認したいときは [session_state.md](/home/happy/codex_minimal_outrigger_cli_stage1/oracle/doc/app_spec/session_state.md) を先に読む。
- `cmoc session fork` 以外の `cmoc session` 系サブコマンドの仕様を確認したいときは別の sub_command 配下を読む。
- CLI の起動順序や共通 precheck の細部だけを確認したいときは、この file ではなく呼び出し元の runtime 側を読む。

## hash
- f2404006e55dac3cb99692735a54944ce191f2914e00cb57d0b561d46e4c7bad

# `join.py`

## Summary
- `cmoc session join` の CLI 実行本体を置く。事前条件確認、merge 実行、merge conflict の Codex CLI 依頼、状態更新、ブランチ削除と結果表示までをまとめて扱うので、このサブコマンドの振る舞いを追うときに読む。

## Read this when
- `session join` の実行条件、merge 失敗時の扱い、conflict 解消の流れ、完了後に session state と branch をどう扱うかを確認したいときに読む。
- CLI から起動される実処理の入口を探していて、`session join` がどの runtime と Git 操作を使うかを知りたいときに読む。

## Do not read this when
- `session join` 以外のサブコマンドの入口や共通 runtime の仕様を知りたいときは、より上位の共通処理や別サブコマンドの本文を読む。
- indexing preflight や Codex 実行基盤そのものの仕様を知りたいときは、このファイルではなく、その責務の本文を読む。

## hash
- f015b4b46576cd392c939102f90ace37a41e42eda536ee31762a5381cb267fc5
