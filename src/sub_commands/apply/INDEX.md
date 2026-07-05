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
- apply fork の実行制御を担い、session branch 上で isolated apply worktree と apply branch を作成して、対象 file の列挙、Codex による finding 列挙と適用、差分 commit、apply state 更新、report 出力までを 1 回の apply run として進める。
- apply scope に応じた対象 file の正規化・重複排除、再調査キュー、前回 join 済み apply merge commit の解決、finding 由来または差分由来の commit subject 生成も同じ apply loop の復旧条件と合わせて扱う。

## Read this when
- apply fork サブコマンドの開始条件、実行中 state、終了時 state、return code、report path 出力を確認または変更したいとき。
- apply fork がどの file を finding 列挙対象にするか、scope ごとの対象差分、oracle 除外、git ignore・管理外領域・AGENTS/INDEX 除外の扱いを確認したいとき。
- Codex に finding 列挙や finding 適用を依頼する parameter、cwd、log root、purpose、subcommand logger の渡し方を確認または変更したいとき。
- apply fork の loop 内で変更 file を再キューする条件、commit する条件、unconverged と converged の判定、finding 件数の report 連携を扱うとき。
- apply branch、apply worktree、apply process id、oracle snapshot commit、前回 join 済み apply merge commit の関係を調べるとき。

## Do not read this when
- apply fork の report 本文生成や error report の書式だけを変更したい場合は、report 生成側を直接読む。
- Codex に渡す finding 列挙・finding 適用 prompt や parameter の詳細だけを変更したい場合は、builder 側を直接読む。
- apply 以外のサブコマンド実行基盤、git wrapper、state の読み書き、worktree 作成、設定読み込みの汎用挙動を調べたい場合は、runtime や config 側を直接読む。
- apply join の merge 処理そのものを確認または変更したい場合は、join 側を読む。

## hash
- d500937020bc92d2e20161e0f30d8b0d796141e77a344d0b90c31994508a1993

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
