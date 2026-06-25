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
- active session を home branch へ merge せず破棄する `session abandon` サブコマンドの実装。現在 branch と session state の事前条件を確認し、clean worktree と cmoc ignore を保証したうえで home branch へ切り替え、session state を `abandoned` に更新して session branch を削除する。cleanup 失敗時は state と branch の rollback を試み、詳細付きの `CmocError` を返す。

## Read this when
- `cmoc session abandon` の実行条件、成功時の branch 切り替え・state 更新・session branch 削除の流れを確認したいとき。
- active session を merge せず破棄する処理のエラー条件、rollback、利用者向け出力を変更するとき。
- session 系サブコマンドから共通 CLI 実行 wrapper へ渡す command 名や argv を確認するとき。

## Do not read this when
- session の作成、再開、適用、完了など、abandon 以外の session 操作を調べたいとき。
- state file の schema、branch 検出、git 実行、clean worktree 判定などの共通 runtime helper の詳細を調べたいとき。
- CLI 全体のコマンド登録や Typer app 構成を調べたいとき。

## hash
- 9ce6fce98b69d891fa7eb88e2335219c900da7f78a7ae09ca77d69b29c3dd600

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
