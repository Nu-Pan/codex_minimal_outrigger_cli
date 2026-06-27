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
- apply fork サブコマンドの実行本体を担う実装。session branch 上で事前条件を検証し、isolated apply worktree と apply branch を作成して、対象ファイル列挙、所見列挙、所見適用、差分コミット、report 生成、state 更新までの apply loop を制御する。
- apply fork 中に編集禁止対象へ差分が出た場合の検出、ロールバック、再実行、エラー化を扱う。
- scope と session state から調査対象ファイルを決める処理、変更 path の正規化、重複除去、前回 join 済み apply merge commit の解決、Codex CLI による commit subject 生成を含む。

## Read this when
- apply fork の CLI 実行フロー、事前条件、終了コード、stdout report path、state 遷移、apply worktree/branch 作成を確認または変更したいとき。
- apply scope ごとの調査対象ファイル列挙、INDEX.md・memo・.git・.agents・oracle 除外、git ignored path の扱いを確認または変更したいとき。
- apply fork が Codex CLI に依頼する所見列挙、所見適用、commit message 生成の呼び出し条件や入力を追いたいとき。
- apply fork 中の編集禁止対象差分をロールバックする挙動、再試行回数、失敗時エラー、未追跡ファイル削除の扱いを確認または変更したいとき。
- apply fork report 生成前後の例外処理、process id の作成・削除、完了/エラー時の state 更新を追いたいとき。

## Do not read this when
- apply fork の report markdown 内容や error report の具体的な構成だけを変更したいときは、report 生成側を読む。
- Codex CLI に渡す所見列挙・所見適用プロンプトの詳細だけを確認したいときは、apply fork 用 builder 側を読む。
- apply fork 以外の apply サブコマンドや join/abandon 系の挙動を確認したいときは、それぞれのサブコマンド実装を読む。
- CLI 共通ランタイム、git wrapper、worktree 作成、state 読み書き、config 読み込みの汎用挙動だけを確認したいときは、共通ランタイム側を読む。
- indexing preflight の詳細や有効化条件だけを確認したいときは、indexing サブコマンド側を読む。

## hash
- 4aae96c520e42607b909a73b4e545215df41add0c9c4ddb482b231b2991919d2

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
