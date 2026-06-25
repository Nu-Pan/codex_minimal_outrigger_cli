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
- active session を home branch へ merge せず破棄する session abandon の実装。現在の branch と session state を検証し、clean worktree と ignore 設定を確認したうえで home branch へ切り替え、session state を abandoned に更新し、session branch を削除する。
- cleanup 失敗時は session state を active に戻し、可能なら session branch へ戻る rollback を試み、失敗内容と rollback 結果をまとめて CmocError として報告する。

## Read this when
- session abandon の実行条件、状態遷移、副作用、エラー時 rollback を確認・変更したいとき。
- active session を破棄する際の branch 切り替え、session branch 削除、state file 更新、利用者向け出力の実装を調べたいとき。
- session branch 上でのみ許可する制約、apply state が ready である制約、home branch 存在確認などの事前条件を扱うとき。

## Do not read this when
- session の開始、apply、merge、一覧表示など、abandon 以外の session subcommand の挙動を調べたいとき。
- git 操作、worktree clean 判定、state file の読み書き、branch 判定などの共通 helper の詳細実装を調べたいとき。
- CLI command の Typer 登録や subcommand routing 全体を確認したいとき。

## hash
- 449eeb6b32282f86b6af5bb5c9f5d84452402b09fbaf1d644031924a2477d230

# `fork.py`

## Summary
- 現在の通常 local branch から cmoc managed session branch を新規作成し、その session state を初期化する session fork 処理を定義する実装。
- 作業ツリーの清潔性、cmoc 管理 branch 上でないこと、同じ home branch に active session がないことを確認してから、Git branch 作成、session metadata 保存、利用者向け結果表示を行う。

## Read this when
- session fork の実行条件、拒否条件、作成される session branch 名や session state の初期値を確認したいとき。
- active session の重複検出、managed branch からの fork 禁止、clean worktree 要求、cmoc ignore 確保が session fork でどう組み合わされているかを調べるとき。
- session fork 成功時に利用者へ表示される情報、または session state file に保存される home branch と開始 commit の由来を確認したいとき。

## Do not read this when
- session fork 以外の session 操作、たとえば既存 session への参加、放棄、統合などの具体挙動を調べたいとき。
- Git コマンド実行、branch 判定、worktree 検査、state file の読み書き形式そのものの共通実装を調べたいとき。
- Typer のサブコマンド登録や CLI ルーティング全体を確認したいだけのとき。

## hash
- 20a60dc2af872ac95e7885c085938ee36695778f1001625fd002721d34b16217

# `join.py`

## Summary
- active な session branch を session home branch へ join する実装を扱う。現在 branch と状態ファイルの事前条件確認、clean worktree と cmoc ignore の確認、home branch への切り替え、no-ff merge、状態更新、session branch 削除、Typer への結果出力までを担う。
- join 中の merge conflict を Codex CLI に解決依頼する補助処理も含む。unmerged path の収集、conflict 解決パラメータ生成、marker 残存確認、対象 file の add、unmerged path 再確認、merge commit 完了を扱う。

## Read this when
- session branch を session home branch に取り込む処理、事前条件、状態遷移、branch 削除、join 結果出力を確認または変更したいとき。
- session join の merge conflict 発生時に Codex CLI へ何を渡し、解決後にどの検証と git 操作を行うかを確認または変更したいとき。
- session.state、apply.state、session_home_branch、現在 branch、worktree cleanliness、cmoc ignore が join 可否にどう関わるかを追いたいとき。
- join 失敗時の CmocError メッセージ、利用者向け action、git status や残存 conflict marker の表示内容を確認したいとき。

## Do not read this when
- session の作成、開始、一覧、apply など join 以外の sub command の振る舞いを調べたいとき。
- 状態ファイルの schema、path model、repo root や work root の定義、git wrapper の一般仕様を調べたいとき。
- Codex CLI へ渡す conflict resolution prompt や parameter の具体的な組み立てだけを変更したいとき。
- merge conflict 解決の品質そのものや LLM 出力内容を評価したいとき。

## hash
- 5453a2dfb5696635b39e26de825a48a0f16d52ea55dcdb9601437a2eae835520
