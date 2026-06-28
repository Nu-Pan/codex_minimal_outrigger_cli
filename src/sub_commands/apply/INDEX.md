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
- apply fork サブコマンドの実行本体を扱う実装。session branch 上で isolated apply worktree を作成し、scope に応じた対象列挙、Codex による finding 列挙と適用、変更の再キュー、commit 生成、完了・失敗時の state 更新と report 出力を統括する。
- apply fork 中に編集禁止対象へ差分が出た場合の検出、ロールバック、再実行、エラー化の制御も含む。
- finding 列挙対象の正規化、変更 path の取得、重複排除、前回 join 済み apply merge commit の推定など、apply fork loop を支える局所 helper 群への入口になる。

## Read this when
- apply fork の CLI 実行条件、scope 別の対象ファイル選定、apply worktree・apply branch・session state の更新順を確認または変更したいとき。
- Codex による finding 列挙、finding 適用、適用後 diff からの commit subject 生成、report 出力までの apply fork loop 全体を追いたいとき。
- apply fork 中に oracle、.agents、memo など編集禁止対象へ差分が発生した場合の検出・復元・再試行・エラー処理を確認したいとき。
- 変更済みファイルを再度 finding 列挙対象へ戻す処理、INDEX.md や git ignored path の除外、oracle を含めるかどうかの対象正規化条件を確認したいとき。

## Do not read this when
- apply fork report の具体的な markdown 内容や error report の生成内容だけを確認したい場合は、report 書き出し側の実装を直接読む。
- Codex に渡す finding 列挙用または finding 適用用 prompt parameter の内容だけを確認したい場合は、acp builder 側の apply fork 用実装を読む。
- apply process id の保存・削除・tracking context の細部だけを確認したい場合は、apply runtime 側の実装を読む。
- apply fork 以外の apply サブコマンド、join・abandon などの挙動を調べたい場合は、それぞれのサブコマンド実装へ進む。

## hash
- 97643a5463e0147f03c62061105d5315d729f1546b84624e00edfab14b458df8

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
- apply run の完了またはエラー状態を session branch へ join する処理を実装する。apply branch/session branch の状態検証、想定外差分の検出と force-resolve による復元、merge conflict の扱い、report 生成、成功後の apply state リセットと apply worktree/branch cleanup を担う。
- apply join 中に許可される apply 側・session 側の差分範囲、削除・rename を含む managed branch 差分分類、INDEX.md だけの merge conflict 自動解決の判断もここにまとまっている。

## Read this when
- apply join の実行条件、成功時の state 更新、apply branch の merge と削除、apply worktree の除去について確認・変更したいとき。
- apply join が想定外差分をどう検出し、--force-resolve でどの branch/worktree の path をどの commit へ戻すかを確認・変更したいとき。
- apply join report の内容、出力される warnings、merge conflict 発生時のエラーと report 保存挙動を確認・変更したいとき。
- apply branch/session branch 上で許可される変更範囲、root memo や oracle/.agents/INDEX.md/git ignored path の扱いを確認・変更したいとき。

## Do not read this when
- apply run の開始、apply branch/worktree の作成、apply state を completed/error にする処理だけを調べたいとき。
- apply join 以外の subcommand の CLI 定義や option 宣言だけを調べたいとき。
- git 実行、session state の読み書き、branch/worktree 検索、report directory の基本 helper の実装そのものを調べたいとき。
- oracle や INDEX.md の正本仕様を調べたいとき。

## hash
- b7e76b43057c1047a7d3097dc49065074b11e01dc5b5086217077087fd1f0a2d
