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
- apply 系処理で使う runtime helper をまとめる実装。session branch や apply branch から linked worktree を特定し、apply process の pid file を読み書きし、pidfd と process start time で同一性を確認しながら実行中 apply process を停止する責務を持つ。
- git worktree の porcelain 出力、`.cmoc/state/apply_processes` 配下の永続 pid、Linux の `/proc` と pidfd をまたぐ、apply 実行時状態の低レベル操作の入口になる。

## Read this when
- apply branch 名から期待される worktree path を導く処理、または branch が checkout されている linked worktree の探索処理を確認・変更したいとき。
- apply 実行中 process の pid file の生成、読み取り、削除、破損値や stale pid の扱いを確認・変更したいとき。
- apply abandon などで既存 apply process を安全に停止する制御、SIGTERM/SIGKILL の順序、pidfd、process start time、権限不足時のエラーを確認・変更したいとき。
- apply process の同一性確認に関係する Linux 依存の `/proc/<pid>/stat` 読み取り、pidfd open、pidfd signal、終了待機の挙動を調べたいとき。

## Do not read this when
- apply サブコマンドの CLI 引数、利用者向け出力、上位の実行フローだけを確認したいとき。
- session state file 全体の schema や apply 状態遷移の高レベル仕様を確認したいとき。
- git worktree 作成・削除そのものの処理や、apply 用 branch の作成手順を確認したいとき。
- process 停止や pid file に関係しない apply の差分適用、commit、merge、検証処理を調べたいとき。

## hash
- a921a309f8c677277658a3382f49adbccec6bb581f6e74b9946773ccd4bebe85

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
- apply fork サブコマンドの実行本体を担う実装。session branch 上で isolated apply worktree を作成し、scope に応じた対象列挙、Codex による finding 列挙と適用、変更の commit、report 作成、state と process id の更新・後始末までの制御フローを扱う。
- apply 中に編集禁止対象へ差分が出た場合の検出、ロールバック、再実行、失敗時エラー化を含み、apply fork の安全制約と収束判定に関わる helper もこの対象にまとまっている。
- finding 適用後の commit subject 生成、Codex 出力の commit message 正規化、変更 path や apply 対象 file の正規化、rolling/session/full scope ごとの対象抽出、直近 join 済み apply merge commit の解決を扱う。

## Read this when
- apply fork の起動条件、session state の遷移、apply branch/worktree の作成、process id の記録・削除、成功・失敗時の report 出力を確認または変更したいとき。
- apply fork がどの file を調査対象にするか、scope ごとの対象範囲、oracle・INDEX.md・binary・git ignored file・編集禁止領域の除外条件を確認したいとき。
- Codex による finding 列挙、finding 適用、編集禁止差分の rollback と再試行、適用後 commit の作成という apply loop の制御を追いたいとき。
- apply fork の収束・未収束判定、未収束時の終了コード、finding count、result_label、CLI 表示内容に関わる挙動を調べるとき。
- apply finding から git commit subject を生成する prompt、Codex 出力を 1 行 commit message に丸める fallback 挙動を確認したいとき。

## Do not read this when
- apply fork のレポート本文の書式や保存内容だけを確認したい場合は、report 生成を担当する対象へ進む方がよい。
- Codex に渡す finding 列挙用または finding 適用用 parameter の詳細だけを確認したい場合は、builder 側の対象へ進む方がよい。
- apply fork 以外の apply サブコマンド、CLI command 登録、または一般的な runtime helper の実装を調べたいだけなら、より直接の対象へ進む方がよい。
- oracle の正本仕様そのものや path keyword の定義を確認したい場合は、実装ではなく該当する oracle 側の対象を読むべき。
- INDEX.md 生成・更新の一般規則やルーティング文書の方針を確認したいだけなら、この apply fork 実行制御ではなく仕様・文書生成側の対象を読む方がよい。

## hash
- e4de887c4b01a0187891e7fae1fc79fde0f656f664bc4060550dcd45e112cdf1

# `fork_report.py`

## Summary
- apply fork の実行結果レポートを生成する実装。通常終了・エラー終了のレポート作成、実装差分の要約生成、要約生成失敗時の changed path fallback、Markdown と YAML frontmatter の描画を担当する。

## Read this when
- apply fork 後に保存されるレポートの内容、保存先、frontmatter、Result・Finding Count・Change Summary の出力を確認または変更したいとき。
- apply fork の差分要約を Codex 実行結果から組み立てる処理、差分がない場合の文言、要約生成に失敗した場合の fallback 挙動を確認したいとき。
- fork commit からの変更 path 収集や、staged/unstaged diff をレポート用に扱う制御を確認したいとき。

## Do not read this when
- apply fork のループ実行、worktree 作成、branch 操作、状態更新そのものを確認したいだけのとき。
- 差分要約プロンプトや構造化出力パラメータの定義を確認したいとき。
- 生成済みレポートを読むだけで、レポート生成ロジックや fallback 挙動を変更しないとき。

## hash
- fac29034274e0665667ef6dcc6dd9f738abcdb3e77d2b6f5a34924f00b7fd3aa

# `join.py`

## Summary
- apply run の join 処理を実行し、apply branch を session branch へ merge して apply state を ready 相当に戻す CLI 実装。session/apply branch 上での実行位置調整、clean worktree 確認、想定外差分の検出と force resolve、merge conflict 処理、report 生成、apply worktree と branch の後始末を扱う。
- join 時に許可される apply/session 側の差分判定、想定外差分を基準 commit へ戻す処理、INDEX.md だけの merge conflict を機械解決する補助処理も含む。

## Read this when
- apply join の実行条件、状態遷移、merge、cleanup、report 出力、warning 出力を確認または変更したいとき。
- apply branch と session branch の想定外差分検出、--force-resolve の revert 挙動、許可される差分の境界を確認したいとき。
- apply join 中の merge conflict、特に INDEX.md conflict の自動解決条件や、未解決 conflict report の生成を調べたいとき。
- apply state の apply_branch や oracle snapshot commit を使った join 制御、last joined snapshot の更新、apply run 完了後の state 初期化に関わる変更を行うとき。

## Do not read this when
- apply join 以外の apply subcommand の開始・実行・完了処理を調べたいだけのとき。
- CLI runtime の共通ラップ、git 実行、state の読み書き、worktree 探索などの共通基盤そのものを変更したいときは、それぞれの定義元を読む。
- join report の保存先や timestamp など、reports や path の共通規約だけを確認したいときは、共通 runtime 側を読む。
- oracle file や INDEX.md の仕様そのものを確認したいときは、正本仕様側を読む。

## hash
- d48181bc0a5c37a70ada7b31a1a4b16b39177aaf23f8ad22b3d744af322b2255
