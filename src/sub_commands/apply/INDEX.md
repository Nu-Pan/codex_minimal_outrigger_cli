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
- 未 join の apply run を破棄し、apply state を ready に戻す CLI 処理を実装する。実行場所が session branch または対象 apply branch であることを検証し、必要なら実行中 apply process を停止したうえで、apply worktree・apply branch・process id file を片付け、状態ファイルを書き戻す。
- 破棄処理の結果として、対象 apply branch、apply worktree、破棄前後の状態、残存物や既欠落などの warning を利用者向けに出力する。

## Read this when
- 未 join の apply run を利用者操作で破棄して ready 状態へ戻す挙動を確認・変更したいとき。
- apply branch または session branch 上からの実行制約、active apply run が存在しない場合のエラー、対象 apply branch の整合性チェックを調べたいとき。
- running 状態の apply process 停止、apply worktree 削除、apply branch 強制削除、apply process id file 削除、apply state 初期化の一連の cleanup を追いたいとき。
- apply abandon の標準出力に含まれる before/after、warnings、削除対象情報を確認したいとき。

## Do not read this when
- apply run の開始、join、完了処理、または通常の ready 状態からの遷移を調べたいだけのとき。
- apply process の停止方法、process id file の保存場所、apply worktree path の算出規則そのものを調べたいときは、apply runtime helper 側を直接読む。
- branch 操作、worktree 削除、state file の読み書き、clean worktree 検証の低レベル実装を調べたいときは、CLI runtime 側の共通処理を直接読む。
- 破棄ではなく、apply run の成果を session branch へ取り込む処理を確認したいとき。

## hash
- 8cf68cbbea7c3a9377b922b36715768d1c71aea6dc037c1b20400f7f5834da66

# `fork.py`

## Summary
- apply fork サブコマンドの実行本体を担う実装。session branch 上で isolated apply worktree を作成し、scope に応じた対象列挙、Codex による finding 列挙と適用、禁止対象差分のロールバック、apply commit 作成、レポート作成、状態更新、終了コード決定までの apply loop を扱う。
- apply 対象の正規化、変更 path の収集、直近 join commit の推定、commit subject 生成など、apply fork の制御フローに密接な helper も同じ単位にまとまっている。

## Read this when
- apply fork の開始条件、session state の検証、apply 用 worktree・branch・process id・state のライフサイクルを確認したいとき。
- apply fork の scope が rolling、session、full の各場合にどのファイルを finding 列挙対象にするかを確認したいとき。
- Codex による finding 列挙、finding 適用、変更検出、commit message 生成、commit 作成、収束判定、unconverged 終了の流れを変更・調査したいとき。
- apply fork 中に oracle、.agents、memo などの編集禁止対象へ差分が出た場合の検出、ロールバック、再実行、エラー化の挙動を調べたいとき。
- apply fork の成功・失敗時に report、apply state、process id、CLI 出力、戻り値がどう扱われるかを確認したいとき。

## Do not read this when
- apply fork のレポート本文の生成内容や Markdown 出力の詳細だけを調べたいときは、レポート生成側を読む。
- Codex に渡す finding 列挙用または finding 適用用の prompt・AgentCallParameter の詳細だけを調べたいときは、builder 側を読む。
- apply join、apply abandon など apply fork 以外の apply サブコマンドの制御フローを調べたいときは、それぞれのサブコマンド実装を読む。
- worktree 作成、git 実行、状態ファイル読み書き、config 読み込みなど runtime 共通処理の低レベル挙動だけを調べたいときは、runtime 側を読む。
- INDEX.md 生成、oracle 文書の仕様、または一般的な realization 品質基準を調べたいだけなら、この実装ではなく正本仕様や対象の文書を読む。

## hash
- 9ad76bf357eac65e10409281458d6090bc174bb4651d5dfa1ceb674c4fdb66f1

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を、YAML frontmatter 付き Markdown report として保存する処理を扱う。
- fork 起点からの git diff を集め、Codex による変更要約を試み、失敗時や空差分時は変更 path ベースの fallback 要約を生成する。
- report には session/apply branch、fork commit、apply worktree、結果ラベル、所見数推移、変更要約を含める。

## Read this when
- apply fork の完了時・失敗時に生成される report の内容、保存先、生成タイミングを確認したいとき。
- apply fork の差分取得範囲、未コミット差分、staged 差分、fork commit が無い場合の扱いを確認したいとき。
- apply fork の変更要約生成で Codex 実行を呼ぶ箇所、構造化要約が空または例外になった場合の fallback 挙動を変更したいとき。
- report の result 表示文、finding count の列挙、change summary の Markdown 描画を変更したいとき。

## Do not read this when
- apply fork のループ制御、所見検出、収束判定そのものを確認したいだけのとき。
- apply fork 用の変更要約プロンプトや structured output parameter の詳細を確認したいとき。
- git 実行 helper、timestamp、reports directory の共通 runtime 実装を確認したいとき。
- apply 以外のサブコマンド report 生成や、一般的な report 保存規約を確認したいとき。

## hash
- 31f7ed1870c8087c24f1b489b1a8bbe1d4458668e1ba212d6a0441870c257427

# `join.py`

## Summary
- apply run の join 処理を実行し、apply branch を session branch へ merge して apply state を ready 相当に戻す CLI 実装。session/apply branch 上での実行位置調整、clean worktree 確認、想定外差分の検出と force resolve、merge conflict 処理、report 生成、apply worktree と branch の後始末を扱う。
- join 時に許可される apply/session 側の差分判定、想定外差分を基準 commit へ戻す処理、INDEX.md だけの merge conflict を機械解決する補助処理も含む。

## Read this when
- apply join の実行条件、状態遷移、merge、cleanup、report 出力、warning 出力を確認または変更したいとき。
- apply branch と session branch の想定外差分検出、--force-resolve の revert 挙動、許可される差分の境界を確認したいとき。
- apply join 中の merge conflict、特に INDEX.md conflict の自動解決条件や、未解決 conflict report の生成を調べたいとき。
- apply state の apply_branch や oracle snapshot commit を使った join 制御、last joined snapshot の更新、apply run 完了後の state 初期化に関わる変更を行うとき。

## Do not read this when
- apply join 以外の apply subcommand の開始・実行・完了処理を調べたいだけのとき。
- CLI runtime の共通ラップ、git 実行、state の読み書き、worktree 探索などの共通基盤そのものを変更したいときは、それぞれの定義元を読む。
- join report の保存先や timestamp など、reports や path の共通規約だけを確認したいときは、共通 runtime 側を読む。
- oracle file や INDEX.md の仕様そのものを確認したいときは、正本仕様側を読む。

## hash
- d48181bc0a5c37a70ada7b31a1a4b16b39177aaf23f8ad22b3d744af322b2255
