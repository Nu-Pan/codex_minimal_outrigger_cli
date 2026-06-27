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
- apply fork サブコマンドの実行本体と、その実行中に使う対象列挙、finding 列挙、finding 適用、禁止対象差分の巻き戻し、commit subject 生成、完了・失敗レポート連携をまとめて扱う。
- session branch 上で ready 状態の apply を isolated worktree に分岐し、scope に応じた調査対象を巡回して Codex に所見列挙と適用を行わせ、変更を commit しながら収束・未収束・エラーを状態とレポートへ反映する処理の入口になる。

## Read this when
- apply fork の CLI 実行条件、状態遷移、apply branch/worktree 作成、process id 管理、完了時や失敗時の出力・戻り値を確認したいとき。
- apply scope が full・session・rolling のとき、どの変更ファイルや oracle/python ファイルを finding 列挙対象にするかを確認したいとき。
- apply fork 中に Codex が編集禁止対象へ差分を出した場合の検出、rollback、再実行、最終エラー化の挙動を確認したいとき。
- finding 適用後の変更検出、追加調査対象の正規化、commit message 生成、git add/commit の流れを追いたいとき。
- 最後に join された apply の merge commit を git 履歴から推定し、rolling scope の差分基点にする処理を確認したいとき。

## Do not read this when
- apply fork の人間向けレポート本文の構成や書き込み形式だけを確認したいときは、レポート生成側を読む。
- Codex に渡す finding 列挙用または finding 適用用の prompt/schema の詳細だけを確認したいときは、対応する builder 側を読む。
- apply process id の保存先や削除処理そのものの詳細だけを確認したいときは、apply runtime 側を読む。
- repo root、worktree 作成、git 実行、状態ファイル読み書きなど共通 runtime helper の実装詳細だけを確認したいときは、runtime 側を読む。
- apply fork を起動する CLI option 定義や Typer command 登録だけを確認したいときは、上位のサブコマンド定義側を読む。

## hash
- 340771a79766e49748f23e36b859798f893ef2a3a4944aa43a34329ff50d21af

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を、YAML frontmatter 付き Markdown report として保存する処理を扱う。
- fork 起点からの git diff を集め、Codex による変更要約を試み、失敗時や空差分時は変更 path ベースの fallback 要約を生成する。
- report には session/apply branch、fork commit、apply worktree、結果ラベル、所見数推移、変更要約を含める。

## Read this when
- apply fork の完了時・失敗時に生成される report の内容、保存先、生成タイミングを確認したいとき。
- apply fork の差分取得範囲、未コミット差分、staged 差分、fork commit が無い場合の扱いを確認したいとき。
- apply fork の変更要約生成で Codex 実行を呼ぶ箇所、構造化要約が空または例外になった場合の fallback 挙動を変更したいとき。
- report の result 表示文、finding count の列挙、change summary の Markdown 描画を変更したいとき。

## Do not read this when
- apply fork のループ制御、所見検出、収束判定そのものを確認したいだけのとき。
- apply fork 用の変更要約プロンプトや structured output parameter の詳細を確認したいとき。
- git 実行 helper、timestamp、reports directory の共通 runtime 実装を確認したいとき。
- apply 以外のサブコマンド report 生成や、一般的な report 保存規約を確認したいとき。

## hash
- 31f7ed1870c8087c24f1b489b1a8bbe1d4458668e1ba212d6a0441870c257427

# `join.py`

## Summary
- apply 実行結果を session 側へ取り込むサブコマンド実装。session/apply branch の状態確認、想定外差分の検出と必要時の force resolve、apply branch の merge、状態更新、report 作成、apply worktree と branch の cleanup を扱う。
- 想定外差分の分類、許可される apply/session 側差分の判定、指定 commit への path 復元、INDEX.md だけの merge conflict の機械解決も同じ実行経路内の補助処理として持つ。

## Read this when
- apply 実行完了後またはエラー後に、結果を session branch へ join する挙動を確認・変更したいとき。
- join 実行前の branch/state/clean worktree 検証、apply branch の特定、oracle snapshot commit を基準にした差分確認、--force-resolve 時の revert 動作を調べるとき。
- apply join の report 内容、merge conflict 時の中断条件、INDEX.md conflict の自動解決、join 後の apply state 初期化や apply worktree/branch cleanup を追うとき。

## Do not read this when
- apply run の開始、apply branch/worktree の作成、または apply 作業そのものの実行経路を調べたいだけのとき。
- session state のデータ構造、git helper、worktree helper、report 保存先などの共通 runtime API の定義だけを確認したいとき。
- join 以外の apply サブコマンドや、oracle/realization の一般仕様、INDEX.md 生成規則を調べたいとき。

## hash
- e0da755eb6e4e81bd8624d90cd195156d3656dd3adcd27f189216b593a54fbf8
