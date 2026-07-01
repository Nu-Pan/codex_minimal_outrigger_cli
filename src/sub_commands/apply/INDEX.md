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
- apply 実行時の作業ツリー特定、apply process の pid file ライフサイクル、Codex subprocess 追跡、abandon 時の安全な停止処理を担う実装。
- pid 再利用を避けるため process start time と pidfd を使い、apply 本体 process と Codex child process group の同一性確認、SIGTERM/SIGKILL 送信、停止待ち、stale 判定、権限エラーの cmoc エラー化を扱う。
- apply branch 名から managed worktree を復元する処理と、git worktree list から branch checkout 済み worktree を探す処理も含む。

## Read this when
- apply や apply abandon の実行中 process 管理、pid file の保存・読取・削除、Codex subprocess の追跡先環境変数を変更する。
- running abandon で apply 本体または Codex subprocess group を安全に停止する挙動、pidfd 必須条件、PID reuse 対策、zombie child を含む process group 終了判定を確認する。
- session branch や apply branch から対応 worktree を特定する処理、または worktree が見つからない場合のエラーを確認する。

## Do not read this when
- apply の CLI 引数定義、ユーザー向け出力、session state 全体の読み書き、merge や patch 適用の流れだけを確認したい。
- Codex subprocess の起動方法そのもの、LLM 呼び出し、prompt 作成、または apply 以外のサブコマンドの process 管理を確認したい。
- 単に git worktree の一般的な作成・削除処理や、apply branch 命名以外の branch 管理を確認したい。

## hash
- 25625f4e91acd37a8ef3835a54cfb3b03718bb4b8ecb56db40212f4f3f026937

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
- apply fork の実行制御を担う実装。session branch 上で isolated apply worktree と apply branch を作り、scope に応じた対象列挙、Codex による finding 列挙と適用、差分 commit、report 出力、apply state 更新、process id 管理、失敗時 report 生成までを一つの apply run として扱う。
- 対象 file の正規化、apply scope ごとの候補算出、直近 join 済み apply merge commit の解決、finding 由来または差分由来の commit subject 生成もここに含まれる。

## Read this when
- apply fork サブコマンドの実行条件、状態遷移、worktree 作成、apply branch 命名、process id の扱い、report 出力、終了コードを確認・変更したいとき。
- apply fork がどの file を finding 列挙対象にするか、rolling/session/full scope の対象範囲、oracle や INDEX/AGENTS や ignore 対象の除外条件を確認・変更したいとき。
- Codex に依頼する finding 列挙・finding 適用 loop、未収束時の扱い、変更 file の再キュー、apply commit の作成条件や commit subject 生成を確認・変更したいとき。
- apply join 後の rolling scope が基準にする過去 merge commit の解決条件を確認・変更したいとき。

## Do not read this when
- apply fork の report 本文生成や error report の内容だけを確認・変更したいときは、report 生成側を直接読む。
- Codex に渡す apply fork 用 parameter の文面や structured output だけを確認・変更したいときは、parameter builder 側を直接読む。
- apply process id の永続化 API や tracking context manager の内部だけを確認・変更したいときは、apply runtime 側を直接読む。
- session state、git 実行、worktree 作成、config 読み込みなど共通 runtime primitive の内部挙動だけを確認・変更したいときは、runtime 側を直接読む。

## hash
- a08e0d2d4d3a760cfe9f8a3dce58486926d6b47ae20e5fc7f6475b2848c0dbd3

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を扱う。
- apply fork worktree の fork commit 以降の変更差分を集め、Codex による構造化要約または変更 path の fallback 要約へ変換する。
- report の frontmatter、作業結果、所見数推移、変更内容要約の組み立てを担う。

## Read this when
- apply fork 完了時・失敗時に生成される report の内容、保存先、生成タイミングを確認したいとき。
- apply fork の変更要約がどの差分を対象にし、未追跡ファイルをどう扱うかを確認または変更したいとき。
- 変更要約生成に失敗した場合や空要約だった場合の fallback 表示を確認または変更したいとき。
- report に出力される result label、所見数推移、branch・commit・worktree 情報の扱いを確認したいとき。

## Do not read this when
- apply fork のループ制御、所見列挙、収束判定そのものを調べたいとき。
- apply fork の変更要約プロンプトや構造化出力 schema の詳細を調べたいとき。
- git コマンド実行 helper、report directory 解決、timestamp 生成、session state 定義の共通実装を調べたいとき。
- apply 以外の sub command の report 生成や通常ログ出力を調べたいとき。

## hash
- 186ef04236529c1d7562192dcb8b72c304f536d3faa14511b89b4366a768f69c

# `join.py`

## Summary
- apply run の join 実行を担う実装。session branch または apply branch 上で実行され、対象 apply branch を session branch へ merge し、apply state を初期化して ready 相当に戻し、結果レポートを保存する。
- join 前の worktree 清潔性確認、cmoc ignore 確保、active session と completed/error apply run の検証、oracle snapshot commit と apply branch の特定、merge 後の apply worktree・apply branch の掃除を扱う。
- apply/session branch 上の想定外差分を分類し、通常時はレポート付きで中止し、force-resolve 時は基準 commit へ戻して commit する処理を含む。INDEX.md だけの merge conflict は削除 commit で機械解決し、それ以外の conflict はレポートして手動解決へ回す。

## Read this when
- apply join の実行条件、成功時の state 更新、apply branch の merge、apply worktree や branch の削除条件を確認したいとき。
- apply join で想定外差分がどのように検出・分類され、--force-resolve でどの branch 側の変更がどの基準 commit へ戻されるかを調べるとき。
- apply join 結果レポートの記録内容、merge conflict 時の中止条件、INDEX.md conflict の自動解決挙動を変更または検証するとき。
- session branch 上と apply branch 上の許可差分の境界、root memo・oracle・.agents・git ignored path の扱いを追うとき。

## Do not read this when
- apply run の開始、apply branch や worktree の作成、session state への apply 情報の書き込みを調べたいだけのとき。
- apply join 以外の apply サブコマンドの CLI option 定義や Typer command 登録だけを確認したいとき。
- git 実行、state 読み書き、reports directory、worktree 探索などの共通 runtime helper の低レベル実装を調べたいとき。
- oracle file の正本仕様そのもの、または apply join の仕様文書を確認したいとき。

## hash
- fff7ab6917b17a245a6a01863838ed827e5fe02fffaba951e76fddb05210aabf
