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
- apply fork の実行制御を担う実装。session branch 上での事前条件確認、apply branch/worktree 作成、apply state 更新、対象ファイル列挙、Codex による finding 列挙と適用、差分 commit、report 生成、失敗時の error report と state 復旧を一つの apply run として扱う。
- apply scope ごとの対象選択、apply finding 対象として扱えるファイルの正規化、重複排除、前回 join 済み apply merge commit の探索、適用差分からの commit subject 生成もこの制御ループ内に含む。

## Read this when
- apply fork サブコマンドの実行条件、state 遷移、worktree/branch 作成、process id 管理、report 出力、終了コードを確認または変更したいとき。
- scope に応じた apply 対象ファイル列挙、oracle や git ignore 対象の扱い、変更後ファイルの再キュー条件を確認または変更したいとき。
- Codex に渡す finding 列挙・finding 適用処理の呼び出し順、loop 収束判定、適用後 commit の作成条件や commit subject 生成を確認したいとき。
- apply fork 失敗時に state、process id、error report、stdout 用 report path がどう扱われるかを追うとき。

## Do not read this when
- apply fork の report ファイル本文の生成内容だけを変更したい場合は、report 生成側の実装を直接読む。
- Codex に渡す prompt や parameter の組み立て内容だけを確認したい場合は、builder 側の apply fork 用実装を直接読む。
- apply process id の保存形式や tracking helper の内部だけを確認したい場合は、apply runtime 側を直接読む。
- apply fork 以外の apply サブコマンドや join 側の挙動を調べたい場合は、それぞれのサブコマンド実装を読む。

## hash
- 5df4bc5c860a258c6b78a92eac6b0ee37c45e24b27440ca2e0148d387c9f8cc8

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として生成し、所見数の推移、結果ラベル、apply branch の変更要約をまとめる。
- apply worktree の fork commit 以降の管理対象差分、未コミット差分、staged 差分、untracked file 差分を集め、Codex による構造化要約または path 一覧の fallback を report に反映する。

## Read this when
- apply fork の report 生成内容、frontmatter、本文見出し、未収束時の注意文を確認・変更したいとき。
- apply fork の変更要約に含める git diff の範囲、rename・deleted path・untracked file の扱いを確認・変更したいとき。
- apply fork の変更要約生成が失敗した場合や空だった場合の fallback 表示を確認・変更したいとき。

## Do not read this when
- apply fork のループ制御、所見列挙、apply branch の作成・削除など report 出力以外の処理を確認したいとき。
- 変更要約を生成する Codex prompt parameter の内容だけを確認したいとき。
- cmoc 全体の report 保存先規則、timestamp、git 実行 wrapper の実装を確認したいとき。

## hash
- f83951bd570f6adfcfede4efacbd4bf7c87b06f26647a27f24109280f7c194b4

# `join.py`

## Summary
- apply 実行結果を session 側へ取り込む処理を担う。対象 branch と session state を検証し、想定外差分の検出または force-resolve、merge、state 更新、report 作成、apply worktree と branch の cleanup、利用者向け結果出力まで扱う。
- apply/session branch 上で許可される差分の分類、managed branch の変更 path 抽出、想定外差分の復元、INDEX.md だけの merge conflict の機械解決もこの対象に含まれる。

## Read this when
- apply run 完了後または error 後に session branch へ取り込む制御を調べるとき。
- apply join の実行条件、clean worktree 要求、session state の更新、apply state の初期化、apply branch/worktree の削除条件を変更するとき。
- apply join の想定外差分判定、force-resolve による復元、merge conflict report、結果 report の内容を確認するとき。
- apply branch と session branch で許可される変更範囲、root memo や oracle/INDEX.md/.agents/.gitignore 対象 path の扱いを調べるとき。
- INDEX.md だけの merge conflict を自動解決する挙動、または未解決 conflict 時の停止条件を確認するとき。

## Do not read this when
- apply run の開始、apply branch/worktree の作成、agent 実行そのものを調べたいときは、apply 開始側の実装を読む。
- worktree 探索や apply branch 共通 helper の責務だけを確認したいときは、apply 共通 runtime を読む。
- git コマンド実行、state の永続化、report 保存先、branch 削除などの低レベル共通処理を変更したいだけなら、runtime 側の定義を読む。
- CLI command の登録や Typer の option 定義だけを確認したいときは、command 配線側を読む。

## hash
- 7f4e4ccebfff79c1b2716b6c79a7ba2403622c9ae774b1bc52a1caaf1df02b63
