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
- apply 実行時に使う worktree 特定、apply process の pid file 管理、process tracking 用環境変数の一時設定、実行中 apply process と Codex subprocess group の停止処理をまとめる実行時補助モジュール。
- session branch や apply branch から対象 worktree を解決し、apply 中断・放棄時に stale pid や process identity を確認しながら安全に停止する責務を持つ。

## Read this when
- apply の実行・中断・abandon 周辺で、session branch または apply branch から linked worktree を特定する処理を確認・変更したいとき。
- apply process の pid file の保存場所、書き込み、読み取り、削除、child process 記録形式の扱いを確認・変更したいとき。
- APPLY_PROCESS_TRACKING_ENV を使った process tracking の環境変数設定範囲や復元処理を確認・変更したいとき。
- apply abandon などで実行中の apply process や Codex subprocess group に SIGTERM/SIGKILL を送り、停止確認や stale pid 判定を行う制御を確認・変更したいとき。
- pidfd、process start time、process group id、権限不足、process 消滅時の扱いなど、process identity を保った停止安全性に関わる不具合を調査するとき。

## Do not read this when
- apply の CLI 引数定義、サブコマンドの dispatch、ユーザー向け出力全体の流れだけを確認したいとき。
- session state file の schema や apply branch 値そのものの生成・保存ルールを調べたいとき。
- Codex CLI を起動するための command 組み立てやプロンプト生成を調べたいとき。
- git worktree の一般的な作成・削除処理を調べたいだけで、branch から既存 linked worktree を解決する処理に関心がないとき。
- process 停止に関係しない apply の差分適用、検証、結果保存、テスト観点を調べたいとき。

## hash
- dc0dbe336dc11df7f60f91e714c78c01e3de2d2acf5ffc0e005d42dbdb9a718b

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
- apply fork サブコマンドの実行本体を担い、session branch 上で isolated apply worktree を作成して Codex による finding 列挙、適用、commit、report 作成、state 更新を制御する。
- apply scope から調査対象 file を列挙・正規化し、変更された realization file を再キューしながら収束判定または未収束終了を行う apply loop の入口になる。
- apply 中に編集禁止対象へ差分が出た場合の rollback と再実行、commit subject 生成、直前 join commit の git 履歴解決など、apply fork 固有の制御 helper を含む。

## Read this when
- apply fork の事前条件、branch・worktree・state・process id・report のライフサイクルを確認または変更したいとき。
- apply scope ごとの対象 file 列挙、INDEX.md や ignored file や oracle file の除外条件、変更後 target の再キュー挙動を確認または変更したいとき。
- finding 列挙と finding 適用の Codex 呼び出し、適用後 commit、未収束時 return code、stdout に report path だけを返す挙動を確認または変更したいとき。
- apply fork 中の編集禁止対象差分を検出・rollback・再試行する挙動や、その失敗時エラーを確認または変更したいとき。

## Do not read this when
- apply fork report の markdown 内容や error report の構成だけを確認したいときは、report 生成側を直接読む。
- finding 列挙や finding 適用の prompt 内容そのものを確認したいときは、ACP parameter builder 側を直接読む。
- CLI 引数の parser 登録やサブコマンド一覧だけを確認したいときは、CLI command 定義側を直接読む。
- apply fork 以外の apply join、abandon、status などの利用者操作を確認したいときは、それぞれのサブコマンド実装を直接読む。

## hash
- 409c5c180654eafb666b90cee4f627c6a7b1cedc68c7890596c7f56c81246bd9

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を担う。report の frontmatter、結果表示、finding count、変更要約の描画と、report 保存先作成までを扱う。
- apply worktree の fork commit 以降の差分、作業ツリー差分、cached 差分、untracked file 差分を集め、Codex による変更要約生成を試みる。要約生成に失敗した場合や要約が空の場合の fallback もここで扱う。

## Read this when
- apply fork の report 生成内容、保存タイミング、保存先、Markdown/YAML frontmatter の項目、result label の表示文言を確認・変更したいとき。
- apply fork report に含める変更要約の入力差分、untracked file の扱い、fork commit がある場合とない場合の git diff 範囲を確認・変更したいとき。
- Codex による apply fork change summary 呼び出し、失敗時の path だけの機械的要約、変更なし判定の挙動を確認・変更したいとき。

## Do not read this when
- apply fork の loop 制御、branch/worktree の作成や削除、状態遷移そのものを調べたいだけのとき。
- apply fork change summary を生成する Codex prompt/parameter の内容を調べたいとき。
- report directory の共通的な path 解決、timestamp 生成、git command 実行 wrapper の詳細を調べたいとき。

## hash
- 9bce7083c1ad5885d4d64fc7f7fb5ce0bdbb759c8b21ba9789657c3670456aec

# `join.py`

## Summary
- apply 実行結果を session 側へ取り込む処理を担う。session branch または apply branch 上で実行され、状態確認、想定外差分の検出または force-resolve、apply branch の merge、状態更新、report 生成、apply worktree と branch の後片付けまでを扱う。
- 想定外差分の判定では、apply 側と session 側の変更範囲を oracle snapshot などの基準 commit から比較し、許可される変更種別を分けて分類する。merge conflict では INDEX.md だけの conflict を機械解決し、それ以外は report とともに手動解決へ委ねる。

## Read this when
- apply run の完了後または error 後に、変更を session branch へ join する制御を確認・変更したいとき。
- join 可能条件、session/apply branch 上での実行条件、clean worktree 要求、apply state を ready 相当に戻す流れを調べたいとき。
- 想定外差分の検出条件、--force-resolve による session/apply 側変更の復元と commit、許可される変更 path の境界を確認したいとき。
- apply branch merge の失敗時処理、INDEX.md conflict の自動削除 commit、未解決 merge conflict report の生成を扱うとき。
- join report の内容、保存先種別、cleanup_reachable や warnings の出力内容を変更・検証したいとき。
- join 成功後の apply worktree 削除、apply branch 削除、削除できない場合の警告処理を確認したいとき。

## Do not read this when
- apply run の開始、apply branch や worktree の作成、apply state を実行中にする処理だけを調べたいとき。
- session の作成・終了、通常の session state モデル、branch 名規則や runtime 共通処理そのものを調べたいとき。
- git command 実行、状態ファイルの読み書き、report root、worktree root などの共通 helper の実装詳細だけが必要なとき。
- INDEX.md エントリー生成や oracle/realization の一般ルールを確認したいだけで、apply join の実行時挙動に関心がないとき。

## hash
- 6e36810b25961e75aa685a289870b06e37aaec6b5a107337b70c63690b863d83
