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
- `apply abandon` サブコマンドの実行本体を提供する。session branch または apply branch 上で、未 join の active apply run を破棄し、apply process の停止、apply worktree と apply branch の削除、process id の削除、session state の ready 復帰、結果表示までを扱う。

## Read this when
- `cmoc apply abandon` の実行条件、失敗条件、状態遷移、削除対象、出力内容を確認したいとき。
- running 状態の apply run を abandon する際の process id 読み取り、停止処理、警告の扱いを確認したいとき。
- apply branch 上と session branch 上のどちらから実行した場合に、どの worktree・branch・state file を対象にするかを調べたいとき。

## Do not read this when
- apply run の開始、join、状態生成など abandon 以外の apply 操作を調べたいとき。
- worktree 削除、branch 削除、process 停止、state 読み書きの低レベル実装そのものを確認したいとき。
- CLI subcommand 共通の実行ラッパーやエラー表示の仕組みを調べたいとき。

## hash
- ef1be500d0c01731d346c9b7fd3cce45a56737e2215aa3760b4307ca13925785

# `fork.py`

## Summary
- apply fork の実行本体を扱う。session branch 上で apply 用 branch/worktree を作成し、scope から対象ファイルを列挙し、Codex による finding 列挙と適用、差分 commit、apply state 更新、report 出力までの一連の制御を担う。
- apply 対象の正規化、再キュー、重複排除、commit subject 生成、前回 join 済み apply commit の解決など、apply fork loop の復旧条件や継続条件に関わる補助処理も同じ制御単位として含む。

## Read this when
- apply fork の開始条件、作成される branch/worktree、apply state の running/completed/error 更新、process id 管理、report 出力の流れを確認したいとき。
- apply scope ごとの対象ファイル列挙、oracle file と realization file の扱い、git ignored や管理外ディレクトリの除外条件を確認したいとき。
- Codex による finding 列挙、finding 適用、変更ファイルの再キュー、apply commit 生成、未収束時の終了コードを変更または調査したいとき。
- 前回 join 済み apply merge commit 以降の差分を apply 対象にする判定や、同一 session の apply branch 履歴解決を確認したいとき。

## Do not read this when
- apply fork の report 本文の書式や保存内容だけを確認したいときは、report 生成を担当する対象を読む。
- Codex に渡す finding 列挙用または finding 適用用 prompt/parameter の内容だけを確認したいときは、それぞれの builder を読む。
- apply fork 以外の apply subcommand、session 作成、join、共通 CLI runtime の挙動を調べたいだけのときは、それらを担当する対象へ進む。
- 一般的な path model、oracle file 判定、git 実行、worktree 作成、state 入出力の共通実装を調べたいだけのときは、runtime 側の対象を読む。

## hash
- 1ae085c188d67a880ca283370781127c422afc55c5905e109f174b88c778286c

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存し、frontmatter、作業結果、所見数推移、変更内容要約を組み立てる実装。
- apply worktree の fork 以降の管理対象差分、未 staged 差分、staged 差分、untracked file 差分を収集し、Codex による構造化要約または path のみの fallback 要約へ変換する。
- apply fork report の出力内容、未収束時警告、変更なし・要約失敗時の表示、削除済み path を除外した差分扱いに関する処理の入口となる。

## Read this when
- apply fork の作業レポート生成、失敗時レポート生成、保存先、Markdown 構成、YAML frontmatter の内容を確認または変更したいとき。
- apply fork で発生した変更差分の集め方、untracked file の扱い、rename や deleted path の扱い、変更 path の重複排除を確認または変更したいとき。
- Codex による apply fork 変更要約の入力、出力が空の場合の扱い、例外時の fallback 要約を確認または変更したいとき。
- 未収束時に所見数推移へ残す注意文や、converged・unconverged・error の report 表示文を確認または変更したいとき。

## Do not read this when
- apply fork のループ制御、branch 作成、worktree 作成、session state 更新そのものを確認したいだけのとき。
- 変更要約を依頼する Codex parameter の prompt や Structured Output schema を確認したいとき。
- report 保存ディレクトリや timestamp の共通仕様、git 実行 wrapper、session state 型の定義を確認したいとき。
- apply fork 以外の sub command の report 生成や差分収集を確認したいとき。

## hash
- a8d4396799cbe46740ee05059b78a5f5dbb4ed8b96b8c2bcb4da78df99122cb3

# `join.py`

## Summary
- apply run の完了またはエラー状態を session branch へ join する CLI 処理を扱う。apply branch/session branch の検証、想定外差分の検出と force-resolve、merge、state 更新、report 出力、apply worktree/branch の後片付けまでを担う。
- apply join 時に許可される差分範囲、INDEX.md conflict の機械解決、root memo や oracle file の扱いなど、join 固有の branch 差分分類ロジックへの入口になる。

## Read this when
- apply join の実行条件、失敗条件、force-resolve の挙動、merge conflict 処理、join 後の state 更新や cleanup を確認・変更したいとき。
- apply branch と session branch のどの変更を想定内または想定外として扱うかを確認・変更したいとき。
- apply join の結果レポート内容、保存先、CLI 表示内容を確認・変更したいとき。
- INDEX.md の merge conflict を自動解決する条件や、apply worktree/branch を削除せず残す条件を確認したいとき。

## Do not read this when
- apply run の開始、apply branch の作成、agent 実行そのものを扱う場合は、apply join ではなく apply 開始側の処理を読む。
- session state のデータ構造、git wrapper、worktree 探索、report directory の共通実装だけを確認したい場合は、runtime や共通 helper を直接読む。
- oracle file や realization file の一般定義、ファイルアクセス規則そのものを確認したい場合は、仕様文書を読む。

## hash
- 53094712717080e09e22d5e504c61f7e7180669a215ad4abb5ef24366a828982
