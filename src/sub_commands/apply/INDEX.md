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
- apply fork の実行結果レポートを生成する実装。通常終了・エラー終了のレポート作成、実装差分の要約生成、要約生成失敗時の changed path fallback、Markdown と YAML frontmatter の描画を担当する。

## Read this when
- apply fork 後に保存されるレポートの内容、保存先、frontmatter、Result・Finding Count・Change Summary の出力を確認または変更したいとき。
- apply fork の差分要約を Codex 実行結果から組み立てる処理、差分がない場合の文言、要約生成に失敗した場合の fallback 挙動を確認したいとき。
- fork commit からの変更 path 収集や、staged/unstaged diff をレポート用に扱う制御を確認したいとき。

## Do not read this when
- apply fork のループ実行、worktree 作成、branch 操作、状態更新そのものを確認したいだけのとき。
- 差分要約プロンプトや構造化出力パラメータの定義を確認したいとき。
- 生成済みレポートを読むだけで、レポート生成ロジックや fallback 挙動を変更しないとき。

## hash
- fac29034274e0665667ef6dcc6dd9f738abcdb3e77d2b6f5a34924f00b7fd3aa

# `join.py`

## Summary
- 完了済みまたはエラー状態の apply run を session branch に取り込む処理を担う。実行位置の補正、状態検証、想定外差分の検出と force-resolve 時の復元、merge と INDEX.md だけの conflict 自動解決、join report 作成、apply worktree と apply branch の後片付けまでを扱う。

## Read this when
- apply run の成果を session branch へ取り込むサブコマンドの挙動を確認・変更したいとき。
- join 可能条件、session/apply branch 上での実行位置、clean worktree 要件、apply state の ready への復帰を調べたいとき。
- apply/session branch の想定外差分判定、--force-resolve による差分復元、merge conflict 時の停止条件や report 内容を確認したいとき。
- apply join 後の apply worktree 削除、apply branch 削除、警告出力、last_joined_apply_oracle_snapshot_commit 更新を追うとき。

## Do not read this when
- apply run の開始、apply branch や worktree の作成、session state を completed/error にする処理を調べたいだけのとき。
- 汎用の git 実行、branch 削除、worktree 削除、状態ファイル読み書き、report directory 解決の共通実装を確認したいとき。
- INDEX.md エントリーの一般的な生成規則や routing 文書全体の仕様を調べたいとき。
- merge conflict のうち INDEX.md 以外を自動解決する実装を探しているとき。この対象はそれらを自動解決せず手動解決へ誘導する。

## hash
- be6749da572fb3434fe94e29aade1751789a07d52cf995f78d3c8e638dbb846a
