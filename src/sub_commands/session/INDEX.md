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
- 現在の通常 local branch から cmoc session branch を作成する session fork サブコマンドの実装。managed branch 上での実行禁止、.cmoc の git ignore 化、clean worktree 確認、同一 home branch の active session 重複確認、session state 作成、実行結果表示を扱う。
- CLI ラッパーとして runtime のサブコマンド実行基盤へ session fork 本体を渡し、ログ作成前にも .cmoc ignore 確認を走らせる。

## Read this when
- session fork の開始条件、拒否条件、作成される session branch 名や session state の初期値を確認したいとき。
- session fork 実行時に .cmoc が git 管理対象外であることをどう保証しているか、またそれに失敗したときのエラーを調べたいとき。
- active session の重複判定、clean worktree 要求、managed branch 禁止といった session fork 固有の制御フローを変更・検証するとき。
- session fork コマンドを runtime の共通サブコマンド実行処理へどう接続しているかを確認したいとき。

## Do not read this when
- session fork 以外の session join、abandon、finish などの挙動を調べたいとき。
- SessionState の構造、state file の読み書き形式、active session 探索の詳細など runtime 側の共通データモデルや永続化処理を調べたいとき。
- git コマンド実行、branch 名取得、work root や repo root 解決などの低レベル runtime helper の実装を確認したいとき。
- CLI 全体の Typer コマンド登録や session サブコマンド群の一覧を確認したいとき。

## hash
- 615b534e93691ca235e253a0744731b65c7d957abc147448c7f4d126b88de7b7

# `join.py`

## Summary
- active な session branch を session home branch へ join するサブコマンド実装を扱う。現在 branch と保存状態の事前条件確認、clean worktree と ignore 設定確認、home branch への切り替え、no-ff merge、状態更新、session branch 削除、結果表示までの制御を担う。
- merge conflict 発生時は conflict 対象ファイルを検出し、Codex CLI に解消を依頼した後、残存 conflict marker と unmerged path を検査して add と merge commit を進める。
- CLI entrypoint では indexing preflight を有効化し、共通の subcommand runner 経由で join 処理を実行する。

## Read this when
- session join の事前条件、対象 branch、状態遷移、home branch への merge、session branch 削除の挙動を確認または変更したいとき。
- session join 中の merge conflict を Codex CLI へ渡す流れ、conflict marker 検査、unmerged path 検査、merge commit の完了処理を確認または変更したいとき。
- session join サブコマンドが indexing preflight や共通 CLI 実行 wrapper とどう接続されているかを確認したいとき。
- session join の利用者向け出力、warning 表示、CmocError の発生条件を確認したいとき。

## Do not read this when
- session join 以外の session サブコマンドの挙動を確認したいだけのとき。
- 保存状態の schema、branch からの状態読み込み、git 実行 wrapper、worktree 検査などの共通 runtime 処理そのものを変更したいとき。
- merge conflict 解消依頼に渡す Codex CLI parameter の内容を変更したいとき。
- indexing preflight の内部挙動を確認または変更したいとき。

## hash
- bd673ffaf918b1736dfabac70797b66f32cc052776ae1df514af40ec5ad733bf
