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
- apply fork の実行制御を担う実装。session branch 上で isolated apply worktree と apply branch を作成し、対象ファイル列挙、Codex による finding 列挙と適用、差分 commit、report 出力、apply state 更新、失敗時 report 生成までを一つの apply run として扱う。
- apply scope、session state、前回 join 済み apply commit から調査対象を決め、git 管理外・除外領域・INDEX/AGENTS・必要に応じた oracle 除外を反映して apply 対象を正規化する。
- finding 適用後の変更ファイルを再キューし、重複排除しながら収束または上限到達まで apply loop を進める orchestration の入口。

## Read this when
- apply fork コマンドの事前条件、worktree/branch 作成、apply state の running/completed/error 遷移、process id 管理、report path 出力を確認または変更したいとき。
- apply fork がどのファイルを finding 列挙対象にするか、scope full/session/差分時の挙動、oracle や git ignored file の扱いを確認したいとき。
- Codex に渡す finding 列挙・finding 適用の呼び出し順、変更後の再キュー、commit subject 生成、収束判定や unconverged 終了コードを追いたいとき。
- apply fork の失敗時に state と error report がどう更新され、例外へ report path がどう渡るかを調べたいとき。

## Do not read this when
- apply fork の利用者向け report 本文の生成内容だけを変更したい場合は、report 生成を担う対象を直接読む。
- Codex に渡す prompt/parameter の中身だけを確認したい場合は、apply fork 用 builder の対象を直接読む。
- apply join、apply abort、session 作成など apply fork 以外のサブコマンド挙動を調べる場合は、それぞれのサブコマンド実装を読む。
- 共通の git 実行、worktree 作成、state 読み書き、Codex exec runtime の基本挙動だけを調べる場合は、共通 runtime 側を読む。

## hash
- 89eda996430eb4665fed7ed1d99c87b7a2c670150c07701c4c9d1aea30dedd39

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
- apply join サブコマンドの実行本体を担い、apply branch を session branch へマージして apply state を初期状態へ戻す。
- join 前のブランチ種別、session/apply state、作業ツリーの clean 状態、想定外差分、merge conflict を検査し、必要に応じて report 作成・エラー終了・force-resolve による復元を行う。
- apply/session branch 上の許可差分判定、想定外差分の分類、INDEX.md conflict の機械解決、apply worktree と apply branch の cleanup も扱う。

## Read this when
- apply join の実行条件、成功時の状態更新、apply branch/worktree の削除条件を確認したいとき。
- apply join が検出する想定外差分の分類基準、force-resolve 時の復元・commit 挙動、report 内容を変更したいとき。
- apply branch の merge conflict 処理、特に INDEX.md だけの conflict を自動解決する挙動を確認したいとき。
- apply branch 上と session branch 上で許可される変更範囲の判定を調べたいとき。

## Do not read this when
- apply join 以外の apply サブコマンドの作成・実行・状態遷移を調べたいとき。
- CLI 共通のエラー表示、git 実行、state 読み書き、worktree 探索などの基盤処理だけを調べたいとき。
- oracle file や realization file の一般的な定義・ルールを確認したいとき。
- INDEX.md のルーティング文書生成ルールそのものを確認したいとき。

## hash
- 0af4c5756155990fb87e3bd82613cdeeb0953bc7b2f3dd54be6877238e9ac34f
