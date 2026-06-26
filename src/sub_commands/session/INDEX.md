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
- active な session branch を home branch へ merge せずに破棄する CLI サブコマンド実装。session state と apply state の事前条件、clean worktree、home branch 存在確認を行ったうえで home branch へ switch し、state を abandoned に更新して session branch を削除する。
- cleanup 失敗時には state を active に戻し、可能なら session branch へ戻る rollback を試み、cleanup error・rollback errors・branch/state file 情報を含む CmocError として報告する。
- CLI ラッパーは実処理を run_cli_subcommand に渡し、command 名と argv を固定して実行する入口になっている。

## Read this when
- session abandon の実行条件、破棄時の state 遷移、session branch 削除、home branch への切り替えを確認または変更したいとき。
- session abandon の失敗時 rollback、cleanup error の詳細、再実行を促すエラー文言を確認または変更したいとき。
- session abandon サブコマンドを run_cli_subcommand 経由で呼び出す CLI 入口の扱いを確認したいとき。

## Do not read this when
- session を home branch に merge する apply/finish 系の処理を調べたいとき。
- session の作成、状態ファイルの schema、branch 名の生成規則、git helper の共通実装を調べたいとき。
- session abandon 以外の session サブコマンドの CLI 挙動や出力を調べたいとき。

## hash
- 1eaa53f5c7699bfde78f1b199f4af7e7ceb2206826ee8abb8082dbf2f1aacc0b

# `fork.py`

## Summary
- 現在の通常 local branch から cmoc session branch を作成する session fork サブコマンドの実処理を定義する。
- 作業ツリーと branch 状態を検証し、managed branch 上での実行、dirty worktree、同一 home branch の active session 重複を拒否したうえで、新しい session branch への切り替えと session state の初期保存を行う。
- CLI ラッパーは共通のサブコマンド実行ヘルパーに session fork の実処理とコマンド名・argv を渡す入口になっている。

## Read this when
- session fork の実行条件、拒否条件、作成される session branch 名、保存される session state の初期値を確認または変更したいとき。
- 通常 branch から session branch を作る処理で、worktree clean 判定、cmoc ignore 設定、active session 検出、git switch、state 書き込みの呼び出し順や責務を追いたいとき。
- session fork コマンドの利用者向け出力内容、または共通 CLI サブコマンド実行ラッパーへの接続を確認したいとき。

## Do not read this when
- 既存 session への参加、破棄、終了など、session fork 以外の session 操作を調べたいとき。
- branch 判定、worktree clean 判定、state path 算出、session state のデータ構造、git 実行、timestamp 生成そのものの実装を調べたいとき。
- Typer アプリへのサブコマンド登録構造や、session コマンド群全体のルーティングを確認したいとき。

## hash
- 119c105879fb2c3d9e2bb0eeea188d149e246debf489e16da7ec32b384a192fd

# `join.py`

## Summary
- active session branch を session home branch へ取り込み、session 状態を joined に更新するサブコマンド実装を扱う。
- join 実行時の事前条件確認、clean worktree 確認、home branch への切り替え、no-ff merge、session branch 削除、実行結果表示までの制御を担う。
- merge conflict 発生時は Codex CLI に conflict 解消を依頼し、残存 marker と unmerged path を検査して merge commit まで進める補助処理も含む。

## Read this when
- session join の実行条件、状態遷移、対象 branch の扱い、成功時の出力内容を確認または変更したいとき。
- active session branch を session home branch に merge する処理、merge 失敗時の conflict 解消フロー、branch 削除失敗時の warning 表示を調べたいとき。
- session join コマンド実行前に indexing preflight や CLI subcommand wrapper がどう呼ばれるかを確認したいとき。

## Do not read this when
- session join 以外の session 操作、apply 操作、review 操作など別サブコマンドの挙動を調べたいとき。
- session 状態ファイルの schema、branch からの state 解決、repo/work root の定義、git 実行 helper の詳細を知りたいだけのとき。
- Codex CLI に渡す conflict 解消依頼パラメータの具体的な構築内容を確認したいとき。

## hash
- 2b7cb0612808552e233d7d156407c1801f26d4f23995b66c87986ad9bc0a9456
