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
- Codex による apply loop を隔離 worktree 上で実行し、対象ファイルごとの finding 列挙、finding 適用、変更コミット、レポート出力、状態更新までを制御する実装。
- apply 対象の scope 解釈、変更対象ファイルの正規化、編集禁止対象差分の検出とロールバック、commit subject 生成、前回 join 済み apply の基準 commit 解決を扱う。

## Read this when
- apply fork サブコマンドの実行条件、状態遷移、作業用 branch/worktree 作成、成功・失敗時のレポート出力や終了コードを確認したいとき。
- rolling、session、full の scope がどのファイル群を finding 列挙対象にするかを確認・変更したいとき。
- apply 中に oracle、.agents、memo など編集禁止対象へ差分が出た場合の検出、ロールバック、再実行、エラー化の挙動を確認したいとき。
- Codex 呼び出しによる finding 列挙、finding 適用、commit message 生成の呼び出しパラメータや実行順を追いたいとき。
- apply fork が変更済み worktree path を次の調査対象へ戻す制御、重複排除、binary・git ignored・INDEX.md 除外などの対象正規化を調べたいとき。
- 最後に join した apply の merge commit を git 履歴から解決する rolling scope の基準判定を確認したいとき。

## Do not read this when
- apply fork のレポート本文フォーマットやエラーレポート生成の詳細だけを確認したい場合は、レポート生成側を読む。
- Codex に渡す finding 列挙用プロンプトや finding 適用用プロンプトの本文を確認したい場合は、パラメータ builder 側を読む。
- apply process id の保存場所や永続化形式だけを確認したい場合は、apply runtime 側を読む。
- session state、worktree 作成、git 実行、設定読み込みなど共通 runtime helper の詳細を確認したい場合は、runtime 側を読む。
- apply fork 以外の apply 系サブコマンドや join/abandon の挙動を調べる場合は、それぞれのサブコマンド実装へ進む。

## hash
- 984b9db0d296aaad2375830c8727ee2e4d51218badea3461c83276a0cf681905

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
- apply run 完了後または error 後に、apply branch を session branch へ取り込み、apply state を初期化して join report と後片付けを行う実装。
- join 前の状態検証、想定外差分の検出と force resolve、merge conflict の扱い、apply worktree と apply branch の cleanup をまとめて扱う。
- INDEX.md だけの merge conflict を削除 commit で機械解決する例外処理や、想定外差分・conflict を利用者向け report に残す処理も含む。

## Read this when
- apply join の実行条件、対象 branch の判定、session branch と apply branch の切り替え挙動を確認したいとき。
- completed または error 状態の apply run を session branch に merge する処理、join 後に apply state を戻す処理、last joined oracle snapshot commit の更新を調べるとき。
- apply join 時の想定外差分の分類、force resolve による差分復元、許可される apply/session 側差分の境界を変更・確認するとき。
- apply branch merge の失敗、merge conflict report、INDEX.md conflict の自動解決、apply worktree と apply branch の削除条件を調べるとき。
- apply join report の生成内容、保存先カテゴリ、標準出力に出す summary と warnings を変更・確認するとき。

## Do not read this when
- apply run の開始、apply branch の作成、作業用 worktree の生成そのものを調べたいだけのとき。
- session state のデータ構造、branch 名規則、git wrapper、report directory、path model などの共通 runtime API の定義を調べたいとき。
- apply join 以外の apply サブコマンド、または session lifecycle 全体の仕様を確認したいとき。
- oracle file や memo の内容そのもの、INDEX.md エントリー生成規則そのものを確認したいとき。
- join report を読むだけで、実装上の検証順序や cleanup 条件を追う必要がないとき。

## hash
- db531dc6c7d8aed77c5678dc687dbaa7f52d1681cacaf8da526854a53562291f
