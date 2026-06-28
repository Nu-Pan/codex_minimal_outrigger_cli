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
- apply run を fork 側で開始し、isolated worktree 上で対象列挙、finding 列挙、finding 適用、禁止対象差分の rollback、commit subject 生成、commit、report 出力、state 更新までを進める orchestration を担う。
- apply scope ごとの対象決定、変更ファイルの再キュー、最後に join した apply merge commit の解決など、apply loop の進行条件と復旧条件を一箇所で扱う。

## Read this when
- apply fork の実行条件、session/apply state の遷移、apply branch/worktree 作成、process id 管理、report path の stdout 返却を確認・変更したいとき。
- apply scope に応じた finding 列挙対象の選び方、変更後ファイルの再キュー、INDEX や ignored file や oracle を対象から外す条件を確認したいとき。
- Codex による finding 適用、編集禁止対象へ差分が出た場合の rollback と retry、失敗時の error state/report 生成を確認・変更したいとき。
- apply finding 適用後の diff から commit subject を生成し、Codex 出力を commit message として安全な 1 行へ丸める処理を確認したいとき。
- rolling scope で基準にする直近 apply join merge commit を git 履歴から解決する制御を確認したいとき。

## Do not read this when
- apply fork で呼び出す Codex prompt の具体的な組み立てだけを確認したい場合は、file finding enumeration や finding application の parameter builder を直接読む方が適切。
- apply fork report の本文構成や error report の出力内容だけを確認したい場合は、report 生成側を直接読む方が適切。
- apply process id の保存形式や tracking context の詳細だけを確認したい場合は、apply runtime 側を直接読む方が適切。
- git worktree 作成、state 永続化、config 読み込み、CLI subcommand 共通実行など runtime 共通機能の詳細を確認したい場合は、共通 runtime 側を読む方が適切。

## hash
- acc9a53ca3208fbf786162f53aae04258562e248bc575de3389b9cb1de098f0d

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
- apply 実行結果を session 側へ取り込む join 処理の実装。実行ブランチと session/apply state を検証し、想定外差分の検出または force-resolve による復元、apply branch の merge、状態更新、report 作成、worktree と branch の後片付けまでを扱う。
- join 時の想定外差分を apply 側と session 側に分類する判定、削除や rename を含む git diff の扱い、INDEX.md conflict の機械解決、force-resolve 時の基準 commit への復元もこの対象に含まれる。

## Read this when
- apply run 完了後または error 後に、apply branch の成果を session branch へ取り込む制御を確認・変更したいとき。
- join 可能な state 条件、session branch/apply branch のどちらから実行できるか、current worktree の清潔性確認、apply worktree の特定に関する挙動を調べるとき。
- apply join が想定外差分をどのように検出し、--force-resolve で何を revert し、どの条件で中止 report を作るかを確認したいとき。
- apply branch merge の失敗時処理、INDEX.md だけの conflict の自動解決、未解決 conflict の report 出力を扱うとき。
- join 成功後に session state を ready 相当に戻す処理、last joined oracle snapshot commit の更新、apply branch/worktree の削除条件、warning 出力を確認・変更するとき。
- apply join report の front matter、Result、Unexpected Changes、Merge Conflicts に出す内容を確認・変更するとき。

## Do not read this when
- apply run の開始、apply branch/worktree の作成、または apply 対象タスクの実行本体を扱うだけなら、開始や実行を担当する対象へ進む。
- session state のデータ構造、永続化形式、branch 名から session id を得る共通処理そのものを変更したいだけなら、runtime や状態定義を担当する対象へ進む。
- git コマンド実行、worktree 削除、branch 削除、ignore 判定、report directory の共通 helper 自体を変更したいだけなら、共通 runtime 側を読む。
- join の外部仕様や人間が管理する正本仕様を確認したい場合は、この実装ではなく対応する oracle doc を読む。
- INDEX.md エントリー生成やルーティング文書の一般規則だけを扱う場合は、この apply join 実装を読む必要はない。

## hash
- 108dc017ed62efb4a5074732e441da9f4a5693fb4102764fff945a0a0b12be79
