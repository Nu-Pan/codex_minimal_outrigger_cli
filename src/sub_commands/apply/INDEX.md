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
- 未 join の apply run を破棄し、apply state を ready に戻す apply abandon サブコマンド実装。session branch または対象 apply branch 上で実行され、状態ファイルが指す apply branch の同一 session 性を検証してから、実行中 process の停止、apply worktree・branch・process id の削除、状態更新、結果表示を行う。

## Read this when
- apply abandon の実行条件、失敗条件、状態遷移、cleanup 対象、警告出力を確認したいとき。
- active apply run の破棄時に、apply process、apply worktree、apply branch、session state file がどの順序・条件で扱われるかを調べるとき。
- session branch と apply branch のどちらから apply abandon を実行できるか、また現在 branch と state file 上の apply branch の整合性検査を変更したいとき。

## Do not read this when
- apply run の開始、join、通常完了、または apply 以外のサブコマンドの挙動を調べたいとき。
- apply worktree や apply process id を扱う共通 helper の低レベルな実装だけを確認したいとき。
- CLI runtime の共通エラー処理、状態ファイル形式、branch 名規則そのものを調べたいとき。

## hash
- cc1ef6c21e576b047fd5dcd081d5be71569f1601edcab95ebb79358169e43177

# `fork.py`

## Summary
- apply fork の 1 回の実行を開始し、isolated worktree 上で対象ファイル列挙、Codex による finding 列挙と適用、変更 commit、apply state 更新、report 生成までを制御する。
- scope、session state、前回 join 履歴、変更差分から apply finding の調査対象を決め、oracle file・realization file・除外対象の境界に従って対象を正規化する。
- apply fork の orchestration 全体を一つの loop として扱い、apply state、worktree、再キュー、commit subject、失敗時 report の復旧条件を同じ文脈で管理する。

## Read this when
- apply fork サブコマンドの事前条件、branch/worktree 作成、apply state の running/completed/error 遷移、process id 管理を確認または変更したいとき。
- apply fork がどのファイルを finding 列挙対象にするか、scope ごとの差分基準、oracle file や git ignored file の除外条件を確認または変更したいとき。
- Codex による finding 列挙・finding 適用の呼び出し、適用後の再キュー、commit message 生成、converged/unconverged/error report の扱いを確認または変更したいとき。
- apply fork の失敗時に state や report path がどう更新されるか、stdout や returncode がどう決まるかを追うとき。

## Do not read this when
- apply fork の report 本文の書式や出力内容だけを変更したいときは、report 生成側を直接読む。
- Codex に渡す finding 列挙・finding 適用プロンプトや parameter の詳細だけを変更したいときは、builder 側を直接読む。
- apply 以外のサブコマンド、join 処理、session 作成処理、共通 CLI runtime の一般仕様を調べたいだけのときは、それぞれの担当箇所を読む。
- oracle file や realization file の定義そのもの、INDEX.md 生成規則、path model の正本仕様を確認したいだけのときは、oracle 側の該当文書を読む。

## hash
- b248a93c6cd1cce17d3f14a48961350a5cf2b13ef24acef803841c1ba626a0c1

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown レポートとして保存する処理を担う。
- apply worktree 上の fork 起点以降の管理対象差分と未追跡ファイル差分を集め、Codex による変更要約または機械的な fallback 要約をレポートへ含める。
- 収束状態、所見数推移、apply branch や fork commit などの作業文脈を YAML frontmatter と本文に描画する。

## Read this when
- apply fork の作業レポート生成、失敗時レポート生成、保存先、frontmatter、本文構成を確認または変更したいとき。
- apply fork の変更内容要約がどの git diff 範囲、未追跡ファイル、fallback 条件から作られるかを確認したいとき。
- 未収束時の警告文、所見数推移、変更なし表示など、apply fork レポート上の利用者向け文言を扱うとき。

## Do not read this when
- apply fork のループ制御、所見列挙、作業ブランチ作成や worktree 管理そのものを確認したいだけのとき。
- Codex に渡す変更要約用パラメータの schema や prompt の詳細を確認したいとき。
- apply fork 以外のサブコマンドのレポート生成や git 差分取得を扱うとき。

## hash
- 690ca1ebff01a6a1ac9195d36ffc86e75bd1813b5048748f25df508d82db8524

# `join.py`

## Summary
- `apply join` サブコマンドの実行本体を担い、apply branch を session branch へ join し、状態更新・レポート作成・後片付けを行う実装。
- join 前に session/apply 側の想定外差分を分類し、通常時は中止レポート、force-resolve 時は基準 commit への復元 commit を作る。
- merge conflict、INDEX.md conflict の機械解決、apply worktree/branch の削除可否、警告付き CLI 出力まで含む apply join 処理の入口。

## Read this when
- `cmoc apply join` の挙動、失敗条件、force-resolve、join 結果レポート、cleanup 表示を変更する。
- apply branch と session branch の差分分類、許可される apply/session 側変更、rename や deleted path の扱いを確認する。
- apply join 後の session state 更新、apply state 初期化、apply worktree や apply branch の削除条件を調べる。
- apply join の merge conflict 処理、INDEX.md conflict の自動解決、想定外差分の revert 処理を修正する。

## Do not read this when
- apply join 以外の apply サブコマンド、apply run の開始・実行・状態生成を調べたい場合。
- worktree 検索、git wrapper、状態ファイルの読み書き、oracle file 判定などの共通 runtime API 自体を変更したい場合。
- CLI 全体の Typer 登録、サブコマンド一覧、外側のコマンドルーティングだけを確認したい場合。

## hash
- ba3b712d92e694756ee73feda605ac7f3fd7a4495269501935bd89bf15fc2951
