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
- active な session branch を home branch へ merge せず破棄する CLI サブコマンド実装を扱う。
- 実行時 wrapper 経由で本体処理を呼び、session branch・状態値・clean worktree・home branch 存在を確認したうえで、home branch へ切り替え、session state を abandoned に更新し、session branch を削除する。
- cleanup 失敗時は state と branch の rollback を試み、失敗内容・rollback 結果・branch/state file 情報を含む CmocError を返す。

## Read this when
- session abandon の事前条件、実行順序、成功時の branch 切り替え・state 更新・branch 削除の挙動を確認したいとき。
- active session を merge せず破棄する処理のエラー条件や、home branch が無い場合の扱いを変更・調査するとき。
- cleanup 失敗時の rollback 方針、CmocError の詳細情報、利用者向け再実行案内を確認したいとき。
- session abandon 成功時に表示される abandoned branch、切り替え先、session state の出力内容を確認したいとき。

## Do not read this when
- session abandon 以外の session サブコマンドの開始・一覧・適用・完了などを調べたいとき。
- session state の schema、永続化形式、branch から state を読み込む共通処理そのものを調べたいとき。
- git 操作 wrapper、worktree clean 判定、cmoc ignore 設定などの共通 runtime helper の実装詳細を調べたいとき。
- oracle 上の正本仕様や CLI 全体のコマンド登録構造を確認したいだけのとき。

## hash
- a116268c186c80736e9e3a46acdbb740ff0b890b55dcf846e15fa2d7245e4545

# `fork.py`

## Summary
- 通常の local branch から新しい cmoc session branch を作成する `session fork` サブコマンドの実行本体を扱う。
- managed branch 上での実行禁止、clean worktree 要求、同一 home branch の active session 重複禁止を確認したうえで、session state を初期化して作成結果を CLI に表示する処理への入口になる。

## Read this when
- `session fork` の実行条件、失敗条件、branch 作成、session state 初期値、CLI 表示内容を確認または変更したいとき。
- session 開始時に home branch、start commit、state file がどのように決まるかを追いたいとき。
- cmoc 管理 branch、dirty worktree、既存 active session に対する `session fork` のエラー挙動を調べたいとき。

## Do not read this when
- session branch への参加、破棄、終了など、fork 以外の session 操作を調べたいとき。
- session state のデータ構造、保存形式、path 解決、git 実行 helper そのものを調べたいとき。
- CLI アプリ全体のコマンド登録や Typer のルート構成だけを確認したいとき。

## hash
- ad0dedaa08ce69725b9f9cb7774c11d70a12ac2092d3348e9a0ff785ba36cbf6

# `join.py`

## Summary
- active な session branch を session home branch へ取り込む CLI 処理を実装する。事前条件確認、clean worktree 確認、home branch への切替、no-ff merge、状態更新、session branch 削除、利用者向け結果出力を扱う。
- merge conflict 発生時は Codex CLI に解決依頼し、conflict marker と unmerged path が残っていないことを確認して merge commit を完了する補助処理も含む。

## Read this when
- session join の実行条件、状態遷移、git merge・branch 削除・結果出力の挙動を確認または変更したいとき。
- session join 中の merge conflict 解決フロー、Codex CLI への依頼内容の呼び出し、conflict marker 検出、unmerged path 検査、merge commit 完了処理を確認したいとき。
- session branch 上でない場合、session/apply state が条件を満たさない場合、session home branch が無い場合などのエラー条件を調べたいとき。

## Do not read this when
- session join 以外の session サブコマンドの責務、CLI 登録、引数定義、ルーティングを調べたいとき。
- session state のデータ構造、永続化形式、branch から state を探す処理そのものを調べたいとき。
- Codex CLI に渡す conflict resolution parameter の具体的な構築内容を変更したいとき。
- indexing preflight、worktree clean 判定、cmoc ignore 設定、git 実行 wrapper などの共通 runtime 処理そのものを調べたいとき。

## hash
- db05d0d0b26eae836e9cebc0d748a9ba72a80face9758fbe68c181b25f41d029
