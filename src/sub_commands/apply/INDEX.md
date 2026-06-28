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
- apply 実行時に使う worktree 解決、apply process の pid file ライフサイクル、Codex subprocess 追跡、停止処理をまとめた runtime 補助実装。
- session branch や apply branch から対象 worktree を特定し、apply abandon が pid 再利用や child process group を考慮して停止対象を安全に扱うための入口になる。

## Read this when
- apply 実行中 process の記録、読み取り、削除、環境変数経由の Codex subprocess 追跡を確認・変更したいとき。
- apply abandon が実行中 apply process や Codex subprocess group をどの順序・条件で停止するかを確認・変更したいとき。
- branch 名から linked worktree や managed worktree path を復元する処理、または pid file の壊れた内容を停止対象から除外する処理を調べたいとき。
- process start time、pidfd、process group、SIGTERM/SIGKILL、待機 timeout に関わる失敗時の CmocError 化を確認したいとき。

## Do not read this when
- apply サブコマンドの CLI 引数、ユーザー向け入出力、全体の実行フローを知りたいだけのときは、command 層や orchestration 側を先に読む。
- session state の schema、保存形式、読み書き責務を調べたいときは、状態管理を担当する対象を先に読む。
- git 操作の共通実行規約、root/worktree パスモデル、process start time の取得実装そのものを調べたいときは、共通 runtime 側を読む。
- Codex CLI の呼び出し内容や生成物適用の中身を調べたいだけで、実行中 process の追跡・停止に触れないときは読まなくてよい。

## hash
- a9b8c0bd8a2c1ba292459129a90f1257066df010dd73aeb86e74ce2d3bac0345

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
- apply run を isolated worktree 上で開始し、scope に応じた対象列挙、Codex による finding 列挙・適用、禁止対象差分の rollback、commit、report 出力、apply state 更新までを一つの制御 loop として扱う。
- apply fork の事前条件確認、run 用 branch/worktree 作成、process id 管理、converged/unconverged/error の結果処理、finding 適用後の変更 file 再キュー、commit subject 生成をまとめて読む入口になる。
- 16,000 文字を超えるが、apply state、worktree、禁止差分 rollback、再キュー、commit subject が同じ失敗時復旧条件を共有するため、apply fork orchestration として一箇所に保持されている。

## Read this when
- apply fork の実行条件、scope ごとの対象 file 選定、apply worktree/branch の作成、apply state の running/completed/error 遷移を確認したいとき。
- Codex による finding 列挙・適用 loop、finding がない場合や変更がない場合の扱い、変更 file の再キュー、converged/unconverged の判定を追いたいとき。
- apply fork 中に oracle、.agents、memo へ発生した禁止差分を検出・rollback し、再実行または CmocError にする挙動を確認・変更したいとき。
- apply fork の report path を stdout に返す挙動、error report 生成、process id の削除、commit message の生成規則、最後に join した apply merge commit の解決を扱うとき。

## Do not read this when
- apply fork report の本文生成や error report の書式だけを確認したい場合は、report 作成側を直接読む。
- Codex に渡す finding 列挙・finding 適用用 parameter の詳細だけを確認したい場合は、builder 側を直接読む。
- apply process id の保存形式や tracking context manager の内部だけを確認したい場合は、apply runtime 側を直接読む。
- apply 以外の subcommand、共通 CLI runtime、git wrapper、config/state model の一般仕様だけを調べたい場合は、それぞれの共通実装や仕様へ進む。

## hash
- 4d678c7a36b51a5d92f17e6cc1328c1648e901296bd2733201588e8c8b5f9713

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を担う。
- fork 元からの変更差分を git diff と未追跡ファイル差分から集め、Codex による構造化変更要約を試み、失敗時は変更 path の機械的な要約へフォールバックする。
- report には session/apply の branch・commit・worktree、収束結果、所見数の推移、変更要約を frontmatter と本文として描画する。

## Read this when
- apply fork の report 生成先、保存タイミング、保存内容を確認・変更したいとき。
- apply fork の変更差分として、commit 差分、worktree 差分、staged 差分、未追跡ファイルをどう集めるか確認したいとき。
- apply fork の変更要約生成で Codex 実行結果を使う箇所、または要約生成失敗時・空差分時のフォールバック挙動を確認したいとき。
- apply fork report の result 表示、finding count 表示、change summary 表示、YAML frontmatter の構成に関わる変更を行うとき。

## Do not read this when
- apply fork のループ制御、所見検出、apply branch の作成・削除など、report 作成以外の実行フローを調べたいとき。
- Codex に渡す変更要約プロンプトや構造化出力の設計そのものを調べたいとき。
- reports directory や timestamp、git command 実行 helper の共通仕様を調べたいとき。
- apply fork 以外のサブコマンド report や、汎用的な report 表示仕様を調べたいとき。

## hash
- 910bff7f1c498e1843455a81c937f9793cf522a8cf47a71b6255132e74867ac3

# `join.py`

## Summary
- apply run の完了またはエラー状態から、apply branch を session branch へ join して apply state を初期化するサブコマンド実装を扱う。
- join 前の worktree 清潔性確認、想定外差分の検出と force-resolve による復元、merge conflict レポート作成、join 後の apply worktree・branch cleanup までを一連の責務として持つ。
- apply 側・session 側で許可される差分の分類、削除や rename の扱い、INDEX.md だけの conflict 自動解決など、join 固有の差分判定と復旧補助の入口になる。

## Read this when
- apply join の実行条件、session/apply branch 上での動作、apply state を ready 相当に戻す流れを確認・変更したいとき。
- apply branch の merge、merge conflict 検出、INDEX.md conflict の機械解決、join report の内容や生成条件を確認・変更したいとき。
- 想定外差分の分類、--force-resolve 時の session/apply 側差分の戻し方、apply worktree や apply branch の cleanup 条件を確認・変更したいとき。

## Do not read this when
- apply run の開始、作業ブランチ作成、または apply state を completed/error にする処理だけを調べたいとき。
- apply join に限らない CLI 共通実行ラッパー、git 実行、session state の低レベル読み書き、path model の定義を調べたいとき。
- INDEX.md エントリー生成やルーティング文書そのものの規約だけを確認したいとき。

## hash
- bdf6e03d8f2bf5d377ec2e86a06e0a7c979dc184aebe57e820d11a9beef541aa
