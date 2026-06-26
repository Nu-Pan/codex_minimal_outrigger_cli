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
- 未 join の apply run を破棄し、apply state を ready に戻すための apply abandon サブコマンド実装を扱う。
- 実行場所が session branch または apply branch であること、active apply run が存在すること、対象 worktree が clean であることを検証し、必要に応じて実行中 apply process の停止、apply worktree と apply branch の削除、process id の削除、state の初期化を行う。
- 処理結果として対象 apply branch、apply worktree、破棄前後の状態、警告一覧を CLI 出力する。

## Read this when
- apply abandon の実行条件、失敗条件、破棄対象 apply run の特定方法を確認したいとき。
- running 状態の apply run を abandon する際の process id 読み取り、process 停止、停止警告の扱いを確認したいとき。
- apply worktree、apply branch、apply process id、session state の削除または初期化順序と、欠落・残存時の warning 出力を確認したいとき。
- session branch 上と apply branch 上で abandon を実行した場合の current working directory 移動や対象 worktree 解決を確認したいとき。

## Do not read this when
- apply run の開始、join、status など、破棄以外の apply サブコマンドの挙動を確認したいとき。
- apply process id file の読み書きや process 停止 helper の低レベル実装だけを確認したいときは、apply runtime 側を直接読む。
- branch 操作、worktree 削除、state 読み書き、clean worktree 検証などの共通 runtime 処理そのものを確認したいときは、共通 runtime 側を読む。
- INDEX.md の生成規則やルーティング文書の方針を確認したいとき。

## hash
- 6cce3ca85362df7858aed3d594cf712cb341066c5d0e52b8d31220f5d4316adf

# `fork.py`

## Summary
- isolated apply worktree 上で apply loop を実行し、scope に応じた調査対象の列挙、finding 列挙、finding 適用、変更コミット、レポート作成、session state 更新までを統括する実装。
- apply 実行中に編集禁止対象へ差分が出た場合の検出・ロールバック・再試行、apply 対象として扱える通常テキストファイルへの正規化、Codex CLI による commit subject 生成もここで扱う。

## Read this when
- apply fork サブコマンドの実行条件、session/apply state 遷移、apply branch/worktree 作成、process id 管理、成功・失敗時のレポート出力を確認または変更したいとき。
- apply scope ごとの finding 列挙対象、変更済み path の再投入、重複排除、oracle・memo・INDEX・binary・git ignored file の除外条件を確認したいとき。
- finding 適用時に編集禁止対象の差分を戻す制御、再試行後も差分が残る場合のエラー処理、適用後 commit message 生成と commit 作成の流れを確認したいとき。

## Do not read this when
- apply fork の Codex 呼び出し用 prompt や AgentCallParameter の詳細だけを確認したい場合は、その builder 側を読む。
- apply fork のレポート本文やエラーレポートの構成だけを確認したい場合は、レポート生成側を読む。
- apply process id の保存形式や共通 runtime helper の実装だけを確認したい場合は、apply runtime または cmoc runtime 側を読む。

## hash
- 571226ee0c7d1c40ee03cb77e7a3b672e1ff784d6ebd8ec67a09353207ea2b02

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗時の report を生成する実装。git diff から変更要約を作り、要約生成に失敗した場合は変更 path の記録へフォールバックし、結果・所見数・変更要約を Markdown report として書き出す。

## Read this when
- apply fork の report 出力内容、frontmatter、結果ラベル、所見数、変更要約の描画を確認・変更したいとき。
- apply fork の差分要約生成、差分なし時の扱い、要約生成失敗時のフォールバック、変更 path 収集の挙動を確認・変更したいとき。
- apply fork 実行後またはエラー時に reports 配下へ保存される report の生成タイミングや保存内容を追いたいとき。

## Do not read this when
- apply fork のループ制御、所見検出、作業ツリー作成、branch 操作そのものを確認したいだけのとき。
- Codex に渡す変更要約生成プロンプトや structured output の詳細を確認したいとき。
- report 保存先の基礎ルール、timestamp 生成、git コマンド実行 wrapper の共通挙動を確認したいとき。

## hash
- 970d90ece648fc4a499da74ba1ccb67fa6a3b78d33d87cfd2639a698bb71a42d

# `join.py`

## Summary
- apply run 完了後またはエラー後に、apply branch の成果を session branch へ merge して apply state を初期状態へ戻す処理を担う。
- session/apply branch の状態検証、想定外差分の検出と force-resolve 時の復元、merge conflict の扱い、join report 作成、apply worktree と branch の後片付けまでを扱う。
- apply join の CLI ラッパーと実処理、join report の描画、想定差分判定、復元、INDEX.md だけの conflict 自動解決 helper への入口になる。

## Read this when
- apply run の結果を session branch に取り込む join 処理の条件、状態遷移、副作用を確認したいとき。
- apply join がどの branch 上で実行可能か、clean worktree や apply state をどう検証するかを調べるとき。
- apply/session branch の想定外差分判定、--force-resolve による復元 commit、merge conflict 時の report 出力を変更したいとき。
- apply join 後に apply worktree を削除し apply branch を消す条件や、削除できない場合の warning 出力を確認したいとき。
- INDEX.md だけの merge conflict を機械的に解決する特例を確認したいとき。

## Do not read this when
- apply run の開始、apply branch の作成、または作業用 worktree の初期化だけを調べたいとき。
- session state のデータ構造そのもの、永続化形式、branch からの state 読み込み規則を確認したいだけのとき。
- git wrapper、worktree 探索、report 保存先、cmoc ignore 判定などの共通 runtime helper の詳細を調べたいとき。
- apply join 以外の subcommand の CLI 定義や dispatch だけを確認したいとき。
- oracle file や realization file の仕様上の扱い、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- db531dc6c7d8aed77c5678dc687dbaa7f52d1681cacaf8da526854a53562291f
