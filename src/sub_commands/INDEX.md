# `apply`

## Summary
- apply 系サブコマンドの実処理をサブコマンド単位に収める package。`apply/fork.py`、`apply/join.py`、`apply/abandon.py` が各コマンドの本命処理を持つ。
- fork の isolated worktree 作成と finding loop、join の merge/force-resolve/report、abandon の cleanup/state reset と、それらで共有する apply runtime helper への入口になる。

## Read this when
- apply fork/join/abandon の実行条件、状態遷移、副作用、report、cleanup、対象 path 選定を確認または変更したいとき。
- apply 系コマンドのどの本命処理ファイルまたは共通 helper を読むべきか選びたいとき。

## Do not read this when
- CLI の Typer command 宣言や option 定義だけを確認したいときは、`main.py` を読む。
- finding の生成プロンプトや apply fork 用パラメータ構築の詳細を確認したいときは、acp.builder.apply.fork 側を読む。
- git 操作、state 読み書き、worktree 作成削除などの低レベル runtime helper の実装だけを確認したいときは、runtime 側を読む。

## hash
- 989e62e355b578d97dae091a8444e2b0543c9a351c7e8abe48ef7c31c15923cb

# `indexing.py`

## Summary
- 現在の work root に対する INDEX.md maintenance サブコマンドの実処理を担う実装。clean worktree 確認、cmoc ignore 確保、深いディレクトリからの INDEX.md 再生成、更新差分だけの git commit、対象 hash による既存エントリー再利用、Codex CLI による個別エントリー生成、Structured Output から Markdown エントリーへの描画を扱う。
- INDEX.md の対象列挙では、隠しパス、memo、git ignored、binary file、INDEX.md 自体を除外し、ディレクトリは子要素 hash の合成で鮮度判定する。

## Read this when
- INDEX.md maintenance の実行順序、更新対象の列挙条件、既存エントリーの再利用条件、または indexing commit の作成条件を確認・変更したいとき。
- INDEX.md エントリー生成で Codex CLI に渡す対象内容、Structured Output から Markdown へ変換する fallback、hash セクションの扱いを確認したいとき。
- memo、隠しファイル、git ignored、binary file、INDEX.md を索引対象から外す制御や、directory hash の再帰計算を調べたいとき。

## Do not read this when
- 個別のサブコマンド登録、Typer app への接続、または CLI のルート構成だけを確認したいとき。
- Codex CLI 呼び出しパラメータの詳細な prompt 構築や Structured Output schema の定義を確認したいとき。
- path keyword の定義、git wrapper、config 読み込み、binary 判定、ignore 判定など runtime helper の内部仕様を確認したいとき。

## hash
- a4f9705b93a50e6ce0a719f324ce891ba8149574d1c806f1494123659bb6c23e

# `init.py`

## Summary
- `cmoc init` の実処理と成功時表示を担う実装。work root の repository root を取得し、`.cmoc` を ignore 対象へ同期し、設定を同期したうえで、必要な場合だけ `.gitignore` をコミットする初期化フローを扱う。
- 初期化完了後に stdout へ出す Markdown 形式の結果文もここで組み立てる。

## Read this when
- `cmoc init` の副作用、特に `.cmoc` の ignore 設定、設定同期、`.gitignore` の git add/commit 条件を確認または変更したいとき。
- `cmoc init` 成功時の stdout 表示内容、見出し、repository root や ignored path の出し方を確認または変更したいとき。
- 初期化コマンドが runtime helper をどの順序で呼び出すか、また未コミット差分がある場合にどの git 操作を行うかを追いたいとき。

## Do not read this when
- CLI アプリ全体へのサブコマンド登録、Typer の command 定義、引数や option の追加位置だけを確認したいとき。
- repository root の判定方法、`.cmoc` ignore の具体的な書き換え規則、設定同期、git 実行 wrapper の内部仕様を確認したいとき。
- `cmoc init` 以外のサブコマンドの挙動や出力を確認したいとき。

## hash
- f50ebd2eb96fa024f3634c6b14a5882d4866a2532cf05a13d3b5fe06134d561c

# `review.py`

## Summary
- active な session branch 上で oracle review を実行するサブコマンド統括フローを定義している。
- session 状態確認、clean worktree 確認、review 用一時 branch/worktree のライフサイクル、対象列挙・finding loop・INDEX 取り込み・レポート生成 helper の呼び出し順序を扱う入口になる。

## Read this when
- oracle をレビューするサブコマンドの実行条件、作業ツリーの清潔性確認、一時 worktree/branch のライフサイクル、または active session branch 制約を確認したいとき。
- review oracle 全体の呼び出し順序、失敗時にも report を書く制御、または下位 helper の接続を確認・変更したいとき。

## Do not read this when
- 通常の CLI アプリ登録、Typer の command wiring、または他サブコマンドの引数定義だけを調べたいとき。
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、INDEX.md と binary file を除外する対象選定だけを調べるときは、`review_targets.py` を読む。
- finding を列挙・統合・反証/擁護検証・判定するループ制御、Structured Output の finding list への適用、finding id や verdict の扱いを変更するときは、`review_loop.py` を読む。
- review worktree で生成された INDEX.md 差分だけを commit/merge する制御、INDEX.md 以外の差分検出、merge conflict を session 側採用で解消する挙動を確認するときは、`review_index.py` を読む。
- review 結果レポートの frontmatter、判定区分、対象 oracle file 一覧、fatal/minor finding 表示、path 表示の整形を変更するときは、`review_report.py` を読む。
- oracle review 用 prompt parameter の具体的な文面や Structured Output schema の定義を確認したいときは、builder 側の該当実装を読む。
- git command 実行、worktree 操作、branch 操作、設定読み込み、session state 読み込み、report directory 解決などの共通 runtime helper 自体を調べたいときは、runtime 側の実装を読む。
- oracle file の正本仕様内容そのものや、INDEX.md エントリーとして何を書くべきかの規則を確認したいときは、oracle 側の仕様断片を読む。
- 生成済みレポートの個別内容や過去実行結果を確認したいだけのときは、レポート出力先の生成物を読む。

## hash
- da34890c9d586595154820a8b028253f100cb4b390c3742335e67d7621ffc2b5

# `review_index.py`

## Summary
- oracle review 用 worktree で生成された INDEX.md 差分の commit と、review branch から session branch への merge を扱う。
- INDEX.md 以外の差分検出、porcelain status の path 抽出、INDEX.md だけが conflict した場合に session 側採用で解決する処理をまとめている。

## Read this when
- review worktree の INDEX.md 変更だけを commit する条件、INDEX.md 以外の差分をエラーにする制御、または status parsing を確認・変更したいとき。
- review branch merge の失敗時に INDEX.md conflict だけを自動解決する挙動、merge 後 commit の取得、手動解決へ回す条件を調べたいとき。

## Do not read this when
- review oracle 全体の一時 worktree 作成・削除順序や active session 制約を確認したいときは、`review.py` を読む。
- oracle file の対象列挙、finding loop、または report rendering を確認したいときは、それぞれ `review_targets.py`、`review_loop.py`、`review_report.py` を読む。
- git command 実行 wrapper や worktree 操作 helper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- 42f2f7a768474b5b07e47ec55750ce65ea6bba3439c7cd667355dc5c6ca6efa9

# `review_loop.py`

## Summary
- oracle review の finding enumerate/merge/validate/judge loop を実行する実装。
- Codex に渡す review oracle 用 AgentCallParameter builder を呼び分け、finding id、advocate/challenger reasons、verdict、judge reason を Structured Output から更新する。

## Read this when
- finding の列挙、統合、反証/擁護検証、判定のループ回数や停止条件を確認・変更したいとき。
- merge finding operation の delete/replace/merge 適用、finding id の採番、finding list の更新規則を調べたいとき。
- review oracle 用 Codex 呼び出し purpose、作業 cwd、既存 finding JSON の渡し方を変更したいとき。

## Do not read this when
- oracle review の active session 制約、一時 worktree 作成、INDEX.md commit/merge、report rendering を確認したいときは、それぞれ該当する review 系 module を読む。
- prompt parameter の文面や Structured Output schema の定義そのものを確認したいときは、acp.builder.review.oracle 側を読む。

## hash
- 56a9c39c86337277ad4be649704deccd9415f64ce48f6e2194b06b95ca3d9fd5

# `review_report.py`

## Summary
- oracle review 結果を Markdown + YAML frontmatter の report として描画し、report directory へ書き出す処理を扱う。
- verdict 判定、frontmatter fields、評価対象 oracle file の表、fatal/minor finding section、path 表示整形をまとめている。

## Read this when
- review report の出力 path、frontmatter 項目、result/verdict の判定条件、または fatal/minor finding の表示形式を確認・変更したいとき。
- oracle path の表示整形、finding section の Markdown 文面、エラー時 report の描画を調べたいとき。

## Do not read this when
- review oracle の実行順序、一時 branch/worktree、対象 oracle file の列挙、finding loop、INDEX.md merge を確認したいときは、それぞれ該当する review 系 module を読む。
- 生成済み report の個別内容だけを読みたいときは、report 出力先の生成物を直接読む。

## hash
- 5a4bc1bc25bc2c3390133302a704cfab266f75d5d961859b561a4a82777866ee

# `review_targets.py`

## Summary
- oracle review の対象 oracle file を scope 別に列挙する処理を扱う。
- full scope では全 oracle file、session scope では session 開始 commit から変更された oracle file のうち、INDEX.md、git ignored、binary file を除外した対象を返す。

## Read this when
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、または INDEX.md・binary・git ignored file の除外条件を確認・変更したいとき。
- session 開始 commit から oracle 配下の変更 path を取得し、列挙済み oracle file と照合する処理を調べたいとき。

## Do not read this when
- review oracle 全体の実行順序、一時 worktree、finding loop、INDEX.md merge、report rendering を確認したいときは、それぞれ該当する review 系 module を読む。
- binary 判定、git ignored 判定、git diff wrapper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- f42029951fa3338498710cca446b7ee6dbf8f87039fc10726d2cecc385a0c05c

# `session`

## Summary
- session 系サブコマンドの実処理をサブコマンド単位に収める package。`session/fork.py`、`session/join.py`、`session/abandon.py` が各コマンドの本命処理を持つ。
- 通常 branch からの session branch 作成、home branch への join、merge せず破棄する abandon の入口になる。
- join 時の merge conflict resolution は `session/join.py` 内で扱う。

## Read this when
- session fork/join/abandon の実行条件、状態遷移、git 操作、副作用、CLI 出力を確認または変更したいとき。
- session 系コマンドのどの本命処理ファイルを読むべきか選びたいとき。

## Do not read this when
- session 以外の subcommand の CLI 定義、引数宣言、Typer app への登録だけを確認したいとき。
- SessionState のデータ構造、状態ファイルの path 規則、git helper、branch 判定、worktree 判定そのものの実装を確認したいとき。
- session join conflict resolution parameter の文面や AgentCallParameter の組み立て詳細だけを確認したいとき。
- oracle 側の正本仕様断片、path keyword の定義、INDEX.md 生成規則を確認したいとき。

## hash
- 1ac7da085f1c6dab065f696400c7fce368e566dccb93384559fce067eaca0cb1

# `tui.py`

## Summary
- 対話的な依頼入力を一時 Markdown として作成し、利用可能なエディタで編集させた後、入力内容を解決用 Codex 実行に渡して TUI 用の AgentCallParameter を組み立てる処理を扱う。
- プロンプト本文からコメントを除去し、Markdown 見出しを StructDoc 階層へ変換し、解決済み設定に基づいて file access mode や各種標準フラグを complete prompt へ反映する入口になる。

## Read this when
- `cmoc tui` の実行フロー、特に元プロンプトファイルの初期化、エディタ起動、入力読み取り、解決済みパラメータから Codex TUI 呼び出しを作る処理を確認したいとき。
- TUI 実行時に使うエディタ探索順、エディタ失敗時の CmocError、または Markdown コメント除去・見出し分解の挙動を変更したいとき。
- 解決済みパラメータの nested `value` 形式から file access mode や oracle/realization/index-entry 標準フラグを取り出す既定値処理を確認したいとき。

## Do not read this when
- サブコマンドの登録、CLI 引数解析、または `cmoc tui` を呼び出す外側のコマンド構成だけを確認したいとき。
- Codex 実行そのもの、Codex TUI プロセスの起動実装、または AgentCallParameter の汎用定義を確認したいとき。
- TUI 用パラメータ解決プロンプトの内容や complete prompt 全体の構築規則を確認したいだけで、このファイルがそれらを呼び出す箇所に関心がないとき。

## hash
- a92ec4d509d7f4e77762e013475cb1996e063376a6d00f39b4a530332d5aa72e
