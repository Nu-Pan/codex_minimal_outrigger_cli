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
- apply fork サブコマンドの実行本体を担う実装。session branch 上の事前条件確認、isolated apply worktree の作成、対象ファイル列挙、Codex による finding 列挙と適用、禁止対象差分のロールバック、変更コミット、レポート出力、apply 状態更新までの制御フローをまとめて扱う。
- apply scope から調査対象を決める処理、変更済み path の正規化、重複排除、直近 join 済み apply merge commit の解決など、apply fork loop の対象選定に必要な補助処理も含む。
- Codex が生成した commit subject を 1 行に整形し、生成失敗時には適用済み finding から代替 subject を作る処理を持つ。

## Read this when
- apply fork の実行条件、状態遷移、worktree 作成、apply branch 名、process id 管理、成功・失敗時のレポート出力や終了コードを確認したいとき。
- apply fork がどのファイルを finding 列挙対象にするかを、scope、session state、git diff、ignore、oracle 除外条件、INDEX 除外条件との関係で確認したいとき。
- finding 適用中に oracle、.agents、memo へ差分が出た場合の検出、ロールバック、再実行、エラー化の挙動を確認したいとき。
- apply fork loop が findings の有無、変更の有無、pending target、設定された処理回数に応じて converged、unconverged、error を決める流れを追いたいとき。
- apply fork が Codex CLI に渡す役割を、finding 列挙、finding 適用、commit message 生成の各用途に分けて確認したいとき。

## Do not read this when
- apply fork の最終レポート本文やエラーレポートの markdown 構成だけを変更・確認したいときは、レポート生成側を直接読む。
- Codex に渡す finding 列挙用または finding 適用用プロンプトの詳細を変更・確認したいときは、パラメータ生成側を直接読む。
- apply process id の保存形式や追跡用 context manager の低レベル実装だけを確認したいときは、apply runtime 側を直接読む。
- CLI 全体の dispatch、引数定義、または run_cli_subcommand の共通実行仕様を確認したいだけなら、CLI 共通実行基盤やサブコマンド登録側を読む。
- repo root、work root、worktree 作成、git 実行、状態ファイル読み書きなどの共通 runtime primitive の実装詳細だけを確認したいときは、runtime 側を直接読む。

## hash
- 8f1537401b0f931ed228c6a4402202bf3ba18f9a1129982ca4d5b5cac72cf8d2

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
