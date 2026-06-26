# `__init__.py`

## Summary
- サブコマンド実装パッケージの入口として、パッケージの役割を短い docstring で示すだけの対象。
- 具体的な処理、公開 API、import 副作用、設定値は持たないため、実装詳細への入口ではなく、パッケージ単位の責務確認に限って使う。

## Read this when
- サブコマンド実装パッケージそのものに、パッケージ説明や初期化時の処理があるかを確認したいとき。
- パッケージ import 時に実行される処理や再 export が存在しないことを本文で確認したいとき。

## Do not read this when
- 具体的なサブコマンドの引数定義、実行処理、入出力、エラー処理を調べたいとき。
- 実装変更やテスト追加のために、実際の制御ロジックを読む必要があるとき。
- パッケージ説明の文言確認以外が目的で、同階層または下位の具体的な実装対象へ直接進めるとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `_runtime.py`

## Summary
- apply 系処理で使う runtime helper をまとめる実装。session branch や apply branch から linked worktree を特定し、apply process の pid file を読み書きし、pidfd と process start time で同一性を確認しながら実行中 apply process を停止する責務を持つ。
- git worktree の porcelain 出力、`.cmoc/state/apply_processes` 配下の永続 pid、Linux の `/proc` と pidfd をまたぐ、apply 実行時状態の低レベル操作の入口になる。

## Read this when
- apply branch 名から期待される worktree path を導く処理、または branch が checkout されている linked worktree の探索処理を確認・変更したいとき。
- apply 実行中 process の pid file の生成、読み取り、削除、破損値や stale pid の扱いを確認・変更したいとき。
- apply abandon などで既存 apply process を安全に停止する制御、SIGTERM/SIGKILL の順序、pidfd、process start time、権限不足時のエラーを確認・変更したいとき。
- apply process の同一性確認に関係する Linux 依存の `/proc/<pid>/stat` 読み取り、pidfd open、pidfd signal、終了待機の挙動を調べたいとき。

## Do not read this when
- apply サブコマンドの CLI 引数、利用者向け出力、上位の実行フローだけを確認したいとき。
- session state file 全体の schema や apply 状態遷移の高レベル仕様を確認したいとき。
- git worktree 作成・削除そのものの処理や、apply 用 branch の作成手順を確認したいとき。
- process 停止や pid file に関係しない apply の差分適用、commit、merge、検証処理を調べたいとき。

## hash
- a921a309f8c677277658a3382f49adbccec6bb581f6e74b9946773ccd4bebe85

# `abandon.py`

## Summary
- 未 join の apply run を破棄し、apply state を ready に戻すための apply abandon サブコマンド実装を扱う。
- 実行場所が session branch または apply branch であること、active apply run が存在すること、対象 worktree が clean であることを検証し、必要に応じて実行中 apply process の停止、apply worktree と apply branch の削除、process id の削除、state の初期化を行う。
- 処理結果として対象 apply branch、apply worktree、破棄前後の状態、警告一覧を CLI 出力する。

## Read this when
- apply abandon の実行条件、失敗条件、破棄対象 apply run の特定方法を確認したいとき。
- running 状態の apply run を abandon する際の process id 読み取り、process 停止、停止警告の扱いを確認したいとき。
- apply worktree、apply branch、apply process id、session state の削除または初期化順序と、欠落・残存時の warning 出力を確認したいとき。
- session branch 上と apply branch 上で abandon を実行した場合の current working directory 移動や対象 worktree 解決を確認したいとき。

## Do not read this when
- apply run の開始、join、status など、破棄以外の apply サブコマンドの挙動を確認したいとき。
- apply process id file の読み書きや process 停止 helper の低レベル実装だけを確認したいときは、apply runtime 側を直接読む。
- branch 操作、worktree 削除、state 読み書き、clean worktree 検証などの共通 runtime 処理そのものを確認したいときは、共通 runtime 側を読む。
- INDEX.md の生成規則やルーティング文書の方針を確認したいとき。

## hash
- 6cce3ca85362df7858aed3d594cf712cb341066c5d0e52b8d31220f5d4316adf

# `fork.py`

## Summary
- isolated apply worktree 上で apply loop を実行するサブコマンド実装を扱う。session branch と apply ready 状態の検証、apply worktree と apply branch の作成、所見列挙、所見適用、コミット生成、report 作成、状態更新までの制御フローを持つ。
- apply scope から調査対象ファイルを決める処理、対象正規化、変更 path 検出、重複排除、編集禁止対象差分の検出とロールバック、Codex CLI による commit subject 生成を含む。

## Read this when
- apply fork の実行条件、状態遷移、終了コード、report 出力、apply worktree 作成や apply branch 命名の挙動を確認・変更したいとき。
- apply scope によって finding 列挙対象がどう選ばれるか、oracle・memo・.agents・INDEX.md・binary・git ignored file がどう除外されるかを確認したいとき。
- apply fork 中に編集禁止対象へ差分が出た場合の rollback と再実行、または rollback 後のエラー化を確認・変更したいとき。
- 所見列挙、所見適用、変更検出、commit message 生成、git add/commit の apply loop 制御を追いたいとき。

## Do not read this when
- apply fork の report markdown の具体的な生成内容だけを確認したいときは、report 書き出し側を読む。
- Codex 呼び出し用 parameter の prompt や JSON schema の詳細だけを確認したいときは、apply fork 用 builder 側を読む。
- apply process id の保存・削除形式だけを確認したいときは、apply runtime 側を読む。
- apply 以外のサブコマンド、一般的な git wrapper、worktree 作成 helper、設定読み込み、状態ファイルの構造そのものを確認したいときは、それぞれの runtime や config 定義を読む。

## hash
- fd38b3e78f105f88ffdf2d93977f7c53b69ada9adb4bb9eed2704ce1be830e7b

# `fork_report.py`

## Summary
- apply fork の通常終了・エラー終了時に、人間向けの実行結果 report を生成して保存する実装。session/apply branch、fork commit、worktree、result、finding count、変更要約をまとめた Markdown report を組み立てる。
- apply worktree の git diff から変更要約を作る入口を持ち、Codex による構造化要約生成が失敗した場合は変更 path 一覧だけの fallback 要約へ切り替える。

## Read this when
- apply fork の実行結果 report がどのタイミングで作られ、どの情報を含めて保存されるかを確認したいとき。
- apply fork の変更要約が git diff、Codex 実行、fallback のどの経路で作られるかを調べたいとき。
- apply fork report の Markdown 本文、YAML frontmatter、result 表示文、finding count 表示、変更要約行の描画を変更したいとき。
- apply fork の失敗時 report と通常 report の差分、特に result を error として扱う経路を確認したいとき。

## Do not read this when
- apply fork の loop 制御、所見検出、作業ツリー作成、branch 操作そのものを調べたいだけのとき。
- 変更要約プロンプトや構造化出力 schema の内容を変更したいときは、変更要約 parameter を組み立てる側を直接読む。
- report 保存先を決める共通ロジック、timestamp 生成、git コマンド実行の低レベル挙動を調べたいだけのときは、それらの共通 runtime 実装を読む。
- apply 以外のサブコマンドの report 形式や、全体の report 一覧・閲覧機能を調べたいだけのとき。

## hash
- 3b7d16ab4b308ade457264de3668f44fc74fee6b20accc3934bb81ca9404cfd1

# `join.py`

## Summary
- apply run の完了またはエラー状態を session branch へ join する処理を実装する。apply branch 上で実行された場合は対応する session branch の worktree へ移動し、状態検証、想定外差分の検出または force-resolve、merge、state 更新、report 出力、apply worktree と branch の cleanup までを扱う。
- join 前後の想定外差分判定、force-resolve 時の restore、INDEX.md だけの merge conflict 自動解決、join report の生成も同じ責務として含む。

## Read this when
- apply join の CLI 実行時挙動、実行可能な branch と state 条件、clean worktree 要件を確認したいとき。
- apply branch を session branch へ merge した後に state がどのように更新され、apply branch や apply worktree がどの条件で削除されるかを追うとき。
- apply join が想定外差分をどう分類し、force-resolve でどの差分をどの commit 基準へ戻すかを変更・調査するとき。
- apply join report の内容、保存先、merge conflict や想定外差分検出時のエラー出力を確認するとき。
- INDEX.md のみの merge conflict を機械解決する特例を調査・変更するとき。

## Do not read this when
- apply run の開始、worktree 作成、apply branch 生成、作業依頼の投入を調べたいだけのとき。
- session state のデータ構造、読み書き形式、branch 名や path model の共通定義そのものを確認したいとき。
- git 操作や worktree 操作の共通 helper の詳細実装を調べたいとき。
- oracle file や INDEX.md の一般的なルーティング仕様を調べたいとき。

## hash
- 6be30b4c1eddf18348a832c95c16fd5b5695bf6d3979f3473c083417efe9d021
