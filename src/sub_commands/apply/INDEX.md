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

# `abandon.py`

## Summary
- apply abandon サブコマンドの実行本体を定義する実装。session branch または apply branch 上で、未 join の active apply run を破棄し、apply worktree・apply branch・process id を掃除して apply state を ready に戻す。
- apply run の状態検証、実行中 process の停止、session worktree への退避、削除後の orphan 確認、利用者向け結果出力を一連の制御として扱う。

## Read this when
- apply abandon の外部挙動、失敗条件、出力内容を確認または変更したいとき。
- apply run の破棄時に、apply branch、apply worktree、apply process id、session state がどう扱われるかを調べたいとき。
- session branch と apply branch のどちらから実行できるか、また current branch と state 上の apply branch の整合性を確認したいとき。

## Do not read this when
- apply start、apply join など abandon 以外の apply サブコマンドの制御を調べたいとき。
- branch・worktree・state file・process id を操作する低レベル helper の実装詳細だけを確認したいとき。
- CLI runtime の共通ラップ処理や run_cli_subcommand 自体の挙動を調べたいとき。

## hash
- bcdcc131818c1e23500761134a43a75f1277f85f8fc017f5fd2040a8a12a3b7f

# `fork.py`

## Summary
- apply fork の実行制御を担い、session branch 上で isolated apply worktree と apply branch を作成し、対象ファイル列挙、Codex による finding 列挙・適用、差分 commit、report 出力、apply state 更新までを一つの apply run として進める。
- apply scope に応じた調査対象の決定、apply 対象の正規化・重複除去、前回 join 済み apply merge commit の解決、finding からの commit subject 生成など、apply fork loop の復旧条件と進行条件を共有する補助処理も含む。

## Read this when
- apply fork の開始条件、scope validation、session/apply state の遷移、apply branch や run worktree の生成、process id 管理、report 出力、終了コードを確認または変更したいとき。
- apply fork がどのファイルを finding 列挙対象にするか、rolling・session・full の scope ごとの差分基準、oracle や git ignored file の扱いを確認または変更したいとき。
- Codex に apply fork 用の finding 列挙や finding 適用を依頼する制御、適用後差分の commit 作成、commit subject 生成、未収束時の再キュー処理を確認または変更したいとき。
- 前回 join された apply merge commit の探索、last joined oracle snapshot を使った rolling scope の基準、apply fork の失敗時 state 更新や error report 生成を調べたいとき。

## Do not read this when
- apply fork の CLI 引数定義やコマンド登録だけを確認したいときは、CLI parser や command routing を扱う対象を読む。
- apply fork report の本文構成や report file の書き込み形式だけを変更したいときは、report 生成を扱う対象を読む。
- Codex に渡す finding 列挙・finding 適用 prompt parameter の内容だけを変更したいときは、apply fork 用 builder を扱う対象を読む。
- apply join、apply status、session 作成など、apply fork 以外の subcommand の外部挙動を確認したいだけのときは、それぞれの subcommand 実装を読む。

## hash
- cc43a5b04b8c2d04bfea12696d6c830f4f71cf12886f39b1642701eeeebf3286

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
- apply run の完了またはエラー後に、apply branch を session branch へ取り込み、apply state を初期状態へ戻す CLI 処理を実装する。
- join 実行前の branch・worktree・state 検証、想定外差分の検出と force resolve、merge conflict 報告、結果 report 作成、apply worktree と branch の cleanup を扱う。
- apply 側と session 側で許可される変更範囲の判定、managed branch 上の変更 path 抽出、INDEX conflict の機械解決など、apply join 固有の制御ロジックへの入口になる。

## Read this when
- apply run を session branch に取り込む処理、join 可否判定、apply state の reset、last joined oracle snapshot commit の更新を確認・変更したいとき。
- apply join 時の想定外差分、force resolve による差分復元、apply branch と session branch の変更範囲分類を調べたいとき。
- apply join の結果 report、merge conflict report、cleanup 成否や warning 出力の内容を確認・変更したいとき。
- apply worktree 上または session worktree 上から join を実行した場合の branch 解決、worktree 削除、apply branch 削除の挙動を追いたいとき。
- INDEX conflict だけを自動解決する条件や、削除 path・rename path の扱いを確認したいとき。

## Do not read this when
- apply run の開始、apply branch の作成、agent 実行、または apply state を completed/error にする処理を調べたいだけのとき。
- session の作成・終了・状態ファイル形式そのものを調べたいときは、session 管理や状態定義を扱う対象を先に読む。
- git command 実行 wrapper、worktree 探索、report 保存先、ignore 判定などの共通 runtime helper の詳細だけを調べたいとき。
- oracle file 判定や path model の仕様そのものを調べたいときは、正本仕様または共通判定処理を読む。

## hash
- 9c5a5e5ab5cbb865ce3106ec028468a933a079b8361df794b92887d5ab1d7abd
