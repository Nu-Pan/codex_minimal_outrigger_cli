# `__init__.py`

## Summary
- session 系サブコマンド実装を収めるパッケージの入口であり、この階層が session サブコマンド実装群であることだけを示す。具体的な処理や公開 API は定義していない。

## Read this when
- session サブコマンド実装群のパッケージ境界を確認したいとき。
- この階層がどのサブコマンド領域に対応するかだけを最小限に確認したいとき。

## Do not read this when
- session サブコマンドの具体的な処理、引数、入出力、状態操作を調べたいとき。
- 実装関数やクラス、テスト対象となる挙動を探しているとき。

## hash
- a2616b13a1c260f66ad6dfda2f7821fc573b581179e92bbad014a023d5958042

# `abandon.py`

## Summary
- active な session branch を home branch へ merge せず破棄する `session abandon` サブコマンドの実行処理を定義する。
- 現在 branch と session state を検証し、worktree の clean 確認、cmoc ignore 確保、home branch の存在確認を行ったうえで、home branch へ switch し、session state を `abandoned` に更新し、session branch を削除する。
- cleanup 失敗時には session state と branch の rollback を試み、失敗内容、rollback 結果、現在 branch、session branch、home branch、state file path を含む `CmocError` を返す。
- CLI ラッパーとして、実処理を `run_cli_subcommand` 経由で `session abandon` コマンド名と argv に結び付ける。

## Read this when
- `cmoc session abandon` の事前条件、成功時の git branch 操作、session state 更新、標準出力の内容を確認または変更したいとき。
- active session を merge せず破棄する処理で、session branch 判定、`active`/`ready` state 判定、home branch の扱い、branch 削除の順序を調べるとき。
- session abandon の cleanup 失敗時に、どの rollback を試み、どの情報をエラー詳細へ含めるかを確認したいとき。
- `cmoc session abandon` を共通 CLI 実行ラッパーへ渡す command name や argv の定義を確認したいとき。

## Do not read this when
- session を home branch へ merge して完了する apply/finish 系の挙動を調べたいとき。
- session の作成、開始、一覧表示、状態ファイル schema、または branch/state の低レベル helper 自体を調べたいとき。
- abandon 済み session の後続処理や履歴表示など、このコマンドの破棄実行以外の workflow を調べたいとき。
- Typer アプリへのサブコマンド登録全体や CLI ルート構造を調べたいとき。

## hash
- 9ce6fce98b69d891fa7eb88e2335219c900da7f78a7ae09ca77d69b29c3dd600

# `fork.py`

## Summary
- 現在の通常 local branch から新しい cmoc session branch を作成する session fork サブコマンドの実処理を定義する実装。管理対象 branch 上での実行、dirty worktree、既存 active session などを拒否し、開始 commit と home branch を session state として保存して、作成結果を利用者向けに出力する。
- CLI サブコマンド実行ラッパーに処理本体を渡し、command name と argv を固定して session fork を起動する入口も持つ。

## Read this when
- session fork の実行条件、拒否条件、作成する branch 名、session state に保存する値、成功時出力を確認または変更したいとき。
- active session の重複判定、cmoc ignore の確保、clean worktree 要求、managed branch 禁止など、session fork 開始前の安全確認を追いたいとき。
- session fork サブコマンドが共通 CLI 実行ラッパーへ渡す command name や argv を確認したいとき。

## Do not read this when
- session への join、abandon、その他の session 操作の挙動を調べたいだけのとき。
- session state のデータ構造、保存形式、状態ファイル path の組み立て規則そのものを調べたいとき。
- git 操作、branch 判定、worktree 清潔性判定、cmoc ignore 管理、timestamp 生成などの共通 helper の内部実装を調べたいとき。

## hash
- 119c105879fb2c3d9e2bb0eeea188d149e246debf489e16da7ec32b384a192fd

# `join.py`

## Summary
- active な session branch を session home branch に join する CLI 処理を担う。事前条件確認、worktree の清潔性確認、home branch への切り替え、session branch の no-ff merge、状態更新、session branch 削除、結果出力までを扱う。
- merge conflict が発生した場合に、unmerged path を特定して Codex CLI に解消依頼し、conflict marker と未解決 path が残っていないことを確認して merge commit を完了する処理も含む。
- コマンド実行入口では indexing preflight を有効化し、共通の CLI subcommand runner 経由で join 実装を実行する。

## Read this when
- session join の実行条件、状態遷移、home branch への merge、join 成功時の出力内容を確認または変更したいとき。
- session join 中の merge conflict を Codex CLI に解決させる流れ、conflicted path の検出、marker 残存確認、git add と commit の扱いを確認したいとき。
- session branch の削除失敗をエラーではなく warning として出力する扱い、または join 後の state 書き込みタイミングを確認したいとき。
- session join コマンドに indexing preflight や共通 subcommand runner 経由の実行制御がどう接続されているかを確認したいとき。

## Do not read this when
- session start、session apply、session abort など join 以外の session サブコマンドの仕様や制御を調べたいとき。
- session state や apply state のデータ構造、永続化形式、branch から state を探す仕組みそのものを調べたいとき。
- Codex CLI に渡す conflict resolution prompt や parameter の具体的な生成内容を調べたいとき。
- git 実行 wrapper、worktree 検証、cmoc ignore 設定、共通エラー型など runtime helper の実装詳細を調べたいとき。

## hash
- 2b7cb0612808552e233d7d156407c1801f26d4f23995b66c87986ad9bc0a9456
