# `__init__.py`

## Summary
- apply サブコマンド実装群のパッケージであることを示すだけの初期化モジュール。現内容では、個別の処理、公開 API、初期化副作用は定義していない。

## Read this when
- apply サブコマンド実装群のパッケージ境界だけを確認したいとき。
- この階層の初期化モジュールに、import、公開名、初期化副作用が追加されているかを確認したいとき。

## Do not read this when
- apply サブコマンドの具体的な挙動、引数処理、入出力、状態変更を調べたいとき。
- 個別の apply 実装ファイルやテストを読むべき変更・調査をしているとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `_runtime.py`

## Summary
- apply 処理に必要な linked worktree の特定、apply branch 名から期待される worktree パスの導出、apply process の PID 状態ファイルの読み書き、実行中 process の停止確認を担う runtime helper 群。
- git worktree の porcelain 出力を参照して branch に対応する worktree を探し、見つからない場合や apply branch 形式が不正な場合は CmocError で利用者向けの確認事項を返す。
- apply abandon などから使われる process 制御として、自 process の停止禁止、存在確認、SIGTERM から SIGKILL への段階的停止、PID ファイルの生成・読取・削除をまとめて扱う。

## Read this when
- session branch または apply branch から対象 worktree をどう特定するかを確認・変更したいとき。
- apply process の PID をどこに保存し、どの操作で読み書き・削除するかを確認・変更したいとき。
- apply abandon が実行中 apply process を停止する条件、待機時間、SIGTERM/SIGKILL の扱い、停止失敗時のエラーを確認・変更したいとき。
- process の存在判定や PermissionError を生存扱いにする挙動を確認・変更したいとき。

## Do not read this when
- apply サブコマンドの CLI 引数、表示、上位のコマンド分岐だけを確認したいとき。
- session state file の schema や apply branch の生成元を確認したいとき。
- git worktree の作成・削除・checkout そのものの処理を確認したいとき。
- PID ファイルの具体的な利用箇所ではなく、apply の全体フローやユーザー操作単位の仕様を把握したいとき。

## hash
- 9d43928760557507a0e04d8c88e82d54d6d3eaed0d02298e8b76fe2a0f5eee0b

# `abandon.py`

## Summary
- 未 join の active apply run を破棄し、apply state を ready に戻す CLI 処理を実装する。
- session branch または apply branch 上で実行されることを前提に、対象 session state を読み取り、apply branch と apply worktree の削除、apply process id の削除、状態更新、結果表示までを担う。
- running 状態では apply process id を読んで停止を試み、削除済みの worktree や branch など復旧不能ではない状況は warnings として出力に集約する。

## Read this when
- apply abandon の実行条件、対象 branch 判定、active apply run が存在しない場合のエラー条件を確認したいとき。
- apply run の破棄時に apply process、apply worktree、apply branch、apply process id file、session state がどの順序で処理されるかを追いたいとき。
- apply abandon の CLI 出力、before/after state、warnings の生成条件を確認したいとき。
- session branch から実行した場合と apply branch から実行した場合の root 解決や current branch 退避処理を確認したいとき。

## Do not read this when
- apply run の開始、join、一覧表示など、破棄以外の apply サブコマンドの挙動を調べたいとき。
- worktree や branch の低レベル操作、state file の永続化、clean worktree 判定そのものの実装を調べたいとき。
- apply process id file のパス規則、process 停止方法、apply worktree の期待パス計算だけを詳しく確認したいとき。
- oracle 上の正本仕様やユーザー向け仕様文書を確認したいとき。

## hash
- c244472d3c7aab7bfbdafb0b800c434a34ed297fbd8116a6861c168385636c51

# `fork.py`

## Summary
- apply fork サブコマンドの実行本体を定義し、session branch 上で isolated apply worktree を作成して、対象ファイルの finding 列挙、finding 適用、変更コミット、レポート生成、状態更新までの apply loop を制御する。
- apply 対象の scope 解決、対象ファイルの正規化、重複除去、worktree の変更検出、Codex CLI による commit subject 生成など、apply fork の制御ロジックに必要な補助処理も同じ入口から確認できる。
- 編集禁止対象に差分が出た場合の検出、未コミット差分のロールバック、再実行、最終的なエラー化を扱い、apply fork 中に保護領域を変更させないためのガードを実装している。

## Read this when
- apply fork サブコマンドの事前条件、session state から running/completed/error へ遷移する流れ、apply branch と apply worktree の作成、プロセス ID 管理、レポート出力の制御を確認したいとき。
- apply loop がどの scope でどのファイルを finding 列挙対象にするか、変更後のファイルを次の調査対象へ戻す条件、unconverged と converged の判定を追いたいとき。
- finding 適用時に編集禁止対象の差分をどう検出し、どの差分を restore または削除し、再試行後も残る場合にどう失敗させるかを確認したいとき。
- apply fork が Codex CLI に渡す finding 列挙、finding 適用、commit message 生成の呼び出し境界や、Codex 出力を commit subject として丸める処理を変更したいとき。

## Do not read this when
- apply fork 用の Codex 呼び出しプロンプトそのものや structured parameter の内容だけを確認したいときは、builder 側の該当処理を直接読む。
- apply fork の成功・失敗レポート本文の構成や出力ファイルの詳細だけを変更したいときは、レポート生成側を直接読む。
- apply process ID の保存・削除処理そのものの永続化形式だけを確認したいときは、apply runtime 側を直接読む。
- git 実行、worktree 作成、state 読み書き、設定読み込みなどの共通 runtime API の実装詳細を確認したいだけなら、runtime 側を直接読む。

## hash
- 571226ee0c7d1c40ee03cb77e7a3b672e1ff784d6ebd8ec67a09353207ea2b02

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を扱う。apply 用 worktree の差分から変更要約を作り、要約生成に失敗した場合は変更 path の列挙にフォールバックし、session/apply branch、fork commit、結果種別、所見数、変更要約を含む report 本文を組み立てる。

## Read this when
- apply fork の完了時または失敗時に生成される report の内容、保存先、生成タイミングを確認したいとき。
- apply fork report の YAML frontmatter、Result、Finding Count、Change Summary の出力内容を変更したいとき。
- apply fork の差分要約生成、要約生成失敗時のフォールバック、変更 path 収集の挙動を確認または変更したいとき。
- apply fork の結果ラベルと人間向け説明文の対応を確認または変更したいとき。

## Do not read this when
- apply fork の変更要約を Codex に依頼するための parameter 構築だけを確認したいときは、その builder 側を読む。
- reports directory、timestamp、git 実行、session state の基本 API を確認したいだけのときは、それぞれの runtime や state 定義を読む。
- apply fork のループ制御、所見検出、worktree 作成、branch 操作の流れを確認したいときは、呼び出し元の apply fork 実行処理を読む。
- 生成済み report を利用者がどう閲覧するか、または report 一覧をどう扱うかを確認したいだけのときは、この report 生成処理ではなく表示・参照側を読む。

## hash
- 970d90ece648fc4a499da74ba1ccb67fa6a3b78d33d87cfd2639a698bb71a42d

# `join.py`

## Summary
- 完了済みまたはエラー状態の apply run を session branch へ取り込み、apply state を ready 相当に戻す処理を担う実装。
- session branch または apply branch 上での実行位置判定、作業ツリー清潔性確認、想定外差分の検出と force resolve、merge、report 作成、apply worktree と branch の後片付けまでを扱う。
- apply join の結果 report 生成、想定外差分の分類、INDEX.md だけの merge conflict の機械解決、指定 commit への path 復元に関する helper の入口でもある。

## Read this when
- apply join の実行条件、対象 branch の決定、apply branch から session branch への merge 手順を確認または変更したいとき。
- apply join が許可する apply 側・session 側の差分範囲、想定外差分の検出条件、force resolve 時の revert と commit の挙動を確認したいとき。
- apply join の失敗時 report、merge conflict report、成功時 report の内容や保存タイミングを確認または変更したいとき。
- apply join 後に apply state を初期化する処理、last joined oracle snapshot commit の更新、apply worktree 削除や apply branch 削除の cleanup 条件を追いたいとき。
- INDEX.md だけが衝突した merge conflict を自動的に削除 commit で解決する制御を確認したいとき。

## Do not read this when
- apply run の開始、apply branch や apply worktree の作成、apply state を completed または error にする処理を調べたいだけのとき。
- session state のデータ構造、永続化形式、branch 名や root path の基礎定義そのものを調べたいとき。
- git command 実行 wrapper、branch 削除、worktree 削除、report directory 算出などの共通 runtime helper の実装詳細を調べたいとき。
- INDEX.md エントリー生成や oracle routing の仕様を調べたいだけで、apply join の merge・cleanup 挙動に関心がないとき。
- apply join 以外の apply 系サブコマンドの CLI 表面や実行フローを調べたいとき。

## hash
- db531dc6c7d8aed77c5678dc687dbaa7f52d1681cacaf8da526854a53562291f
