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
- isolated apply worktree 上で Codex CLI による apply loop を実行するサブコマンド実装。session branch と apply state の事前条件確認、apply 用 branch/worktree 作成、対象ファイル列挙、finding 列挙、finding 適用、変更 commit、結果 report 作成、apply 状態更新までの制御フローを扱う。
- apply 対象の正規化、scope ごとの対象選択、重複除去、変更 path 抽出、編集禁止対象差分の検出・ロールバック、Codex 生成 commit subject の整形など、apply fork 実行中に必要な補助処理も同じまとまりで持つ。

## Read this when
- apply fork の実行条件、終了コード、状態遷移、作成される apply branch/worktree、report 出力、apply process id の扱いを確認または変更したいとき。
- scope に応じてどのファイルを finding 列挙対象にするか、oracle・memo・INDEX・binary・git ignored file をどう除外するかを確認または変更したいとき。
- Codex CLI を使った finding 列挙、finding 適用、commit message 生成の呼び出し方や、config.apply_fork.num_apply_files による apply loop の上限処理を確認したいとき。
- apply fork 中に編集禁止対象へ差分が出た場合の検出、ロールバック、再試行、エラー化の挙動を確認または変更したいとき。
- apply fork が作る commit の単位、commit message の生成・sanitize、dirty target の再投入や変更ファイルの再調査ロジックを追いたいとき。

## Do not read this when
- apply fork の最終 report の本文フォーマットやエラー report の具体的な書き出し内容だけを変更したいときは、report 作成を担当する実装を直接読む。
- Codex に渡す finding 列挙用または finding 適用用の AgentCallParameter の詳細プロンプトだけを変更したいときは、builder 側の該当実装を読む。
- apply process id の保存形式や削除対象 path の詳細だけを確認したいときは、apply runtime 側の補助実装を読む。
- git worktree 作成、state 読み書き、config 読み込み、path model、git command wrapper など共通 runtime の基盤挙動だけを調べたいときは、runtime 側を読む。
- CLI コマンド定義や Typer への登録位置だけを確認したいときは、サブコマンド登録側の実装を読む。

## hash
- 02f60e1a87e5a0df9b0de15ce69f3db6b3b065336a9ab1944925cbe55bfea9c0

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
- apply run 完了後またはエラー後に、apply branch の成果を session branch へ merge して apply state を初期状態へ戻す処理を担う。
- session/apply branch の状態検証、想定外差分の検出と force-resolve 時の復元、merge conflict の扱い、join report 作成、apply worktree と branch の後片付けまでを扱う。
- apply join の CLI ラッパーと実処理、join report の描画、想定差分判定、復元、INDEX.md だけの conflict 自動解決 helper への入口になる。

## Read this when
- apply run の結果を session branch に取り込む join 処理の条件、状態遷移、副作用を確認したいとき。
- apply join がどの branch 上で実行可能か、clean worktree や apply state をどう検証するかを調べるとき。
- apply/session branch の想定外差分判定、--force-resolve による復元 commit、merge conflict 時の report 出力を変更したいとき。
- apply join 後に apply worktree を削除し apply branch を消す条件や、削除できない場合の warning 出力を確認したいとき。
- INDEX.md だけの merge conflict を機械的に解決する特例を確認したいとき。

## Do not read this when
- apply run の開始、apply branch の作成、または作業用 worktree の初期化だけを調べたいとき。
- session state のデータ構造そのもの、永続化形式、branch からの state 読み込み規則を確認したいだけのとき。
- git wrapper、worktree 探索、report 保存先、cmoc ignore 判定などの共通 runtime helper の詳細を調べたいとき。
- apply join 以外の subcommand の CLI 定義や dispatch だけを確認したいとき。
- oracle file や realization file の仕様上の扱い、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- db531dc6c7d8aed77c5678dc687dbaa7f52d1681cacaf8da526854a53562291f
