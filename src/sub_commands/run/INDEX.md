# `__init__.py`

## Summary
- editing run の共通 lifecycle サブコマンドをまとめるパッケージの入口。関連する run サブコマンドの共通処理を確認する際に読む。

## Read this when
- editing run サブコマンドの共通 lifecycle や、その配下の実装を調査・変更するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。具体的な処理の実装を確認する場合は、この入口ではなく配下の該当ファイルを直接読む。

## hash
- ee750515c16235f73dd57b6cd7864576f1957fe840d0ceb82b9658c56c959115

# `abandon.py`

## Summary
- `cmoc run abandon` の CLI 実装。active editing run を特定し、実行中プロセスを停止したうえで run worktree・branch・state・process tracking を cleanup し、ライフサイクルレポートと結果を表示する。
- run の解決、プロセス停止、worktree と branch の削除、および cleanup 警告・失敗時の扱いを確認するための実装入口。

## Read this when
- `cmoc run abandon` の動作、cleanup lifecycle、active run の破棄処理を変更または調査するとき
- run process の停止、worktree・branch の削除、state 更新、abandon レポート出力の連携を確認するとき

## Do not read this when
- run の作成・参加・通常完了や merge 処理を調査するときは、それぞれの lifecycle 実装を直接読む
- workload 固有の処理や一般的な run lifecycle 解決処理だけを調査するとき

## hash
- 8bbf6071bfc54d4b7bf780941e71a3e8a5b38d90f86fab071598cfef69bdd6de

# `join.py`

## Summary
- `cmoc run join` の workload 非依存な merge lifecycle を実装する。active run の事前検査、session branch への merge、INDEX.md conflict の限定的解決、post-join hook、state 同期、report 保存、worktree・branch cleanup を一連で扱う。
- 想定外差分、merge・post-join 失敗、error state、cleanup 失敗を検出し、必要に応じて report と error state を残す。`--force-resolve` 指定時は run branch の想定外差分を fork commit へ戻してから処理する。

## Read this when
- `cmoc run join` の merge、force-resolve、post-join 処理、state 更新、report、cleanup の挙動を変更・調査するとき。
- run lifecycle の失敗時 rollback、error state、process tracking の停止、INDEX.md conflict 処理を確認するとき。
- join 処理に関係する `doctor preprocess` や refactor state 同期の連携を確認するとき。

## Do not read this when
- run の開始・編集・abandon など、join 以外の lifecycle だけを変更・調査するときは、対応する lifecycle 実装を直接読む。
- run 共通の context 解決、差分判定、commit、report 生成の詳細だけを確認する場合は、それぞれの専用 module を直接読む。

## hash
- 59e88f7888ff73835e32fa98e1400f38f87d6ef1419af429bac00d3714f02215

# `lifecycle.py`

## Summary
- editing run の開始・active run 解決・state 更新を共通化するライフサイクル処理を担う。session/run の worktree・branch・commit・state を検証し、work unit の rollback/commit、INDEX 更新、Git 差分の列挙と許可外 path 検出を提供する。run 関連サブコマンドから共通処理を確認する入口。

## Read this when
- editing run の開始、active run の解決、joinable/error state への遷移を変更・調査するとき
- run worktree の作成・削除、session state、branch/commit の整合性検証を変更・調査するとき
- work unit の commit/rollback、INDEX 再生成、Git の rename/copy を含む差分解析を変更・調査するとき
- agent または run/session branch の変更 path 許可検査を変更・調査するとき

## Do not read this when
- 個別サブコマンドのユーザー向け引数や固有処理だけを変更・調査するとき
- state データ構造や永続化形式そのものを変更・調査するときは、まず runtime_state の実装と対応する oracle を読むとき
- Git、path、index 更新の低レベル utility 自体を変更・調査するときは、まず各 commons モジュールを読むとき

## hash
- 21a82ef038f182bbcbf49b131f21f3a4cf1cf4b692f8ad72e4984ae3d7cadacf

# `report.py`

## Summary
- editing run の fork report と lifecycle report を Markdown + YAML Front Matter として保存する共通ライター。実行コンテキスト、状態遷移、完了理由、変更パス、警告、詳細情報をレポートへ整形し、生成先の絶対パスを返す。

## Read this when
- run の fork、join、abandon に関するレポート生成や保存先を変更するとき
- レポートの Front Matter 項目、本文構成、YAML scalar の表現を確認するとき
- run lifecycle の状態・警告・cleanup 結果をレポートへ反映する処理を調査するとき

## Do not read this when
- run のライフサイクル状態遷移そのものを変更・調査するとき
- レポート保存先のパス規則を変更・調査するとき
- レポート生成を呼び出す fork、join、abandon コマンドの処理を直接変更・調査するとき

## hash
- 6e5d43347dec29d80de40b87d7e8a6d828da95fdb54001207f6e307b2c53fd62
