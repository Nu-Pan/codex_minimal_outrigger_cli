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
- active な session branch 上で oracle を isolated review worktree に列挙・レビュー・検証・判定し、INDEX.md 変更だけを取り込んで Markdown レポートを出力するサブコマンド処理を定義している。
- review 用の一時 branch/worktree 作成、対象 oracle file の scope 別列挙、finding の enumerate/merge/validate/judge loop、INDEX.md 差分だけの commit と merge conflict 解消、レビュー結果レポート描画までを扱う。

## Read this when
- oracle をレビューするサブコマンドの実行条件、作業ツリーの清潔性確認、一時 worktree/branch のライフサイクル、または active session branch 制約を確認したいとき。
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、INDEX.md と binary file を除外する対象選定を調べるとき。
- finding を列挙・統合・反証/擁護検証・判定するループ制御、Structured Output の finding list への適用、finding id や verdict の扱いを変更するとき。
- review worktree で生成された INDEX.md 差分だけを commit/merge する制御、INDEX.md 以外の差分検出、merge conflict を session 側採用で解消する挙動を確認するとき。
- review 結果レポートの frontmatter、判定区分、対象 oracle file 一覧、fatal/minor finding 表示、path 表示の整形を変更するとき。

## Do not read this when
- 通常の CLI アプリ登録、Typer の command wiring、または他サブコマンドの引数定義だけを調べたいとき。
- oracle review 用 prompt parameter の具体的な文面や Structured Output schema の定義を確認したいときは、builder 側の該当実装を読む。
- git command 実行、worktree 操作、branch 操作、設定読み込み、session state 読み込み、report directory 解決などの共通 runtime helper 自体を調べたいときは、runtime 側の実装を読む。
- oracle file の正本仕様内容そのものや、INDEX.md エントリーとして何を書くべきかの規則を確認したいときは、oracle 側の仕様断片を読む。
- 生成済みレポートの個別内容や過去実行結果を確認したいだけのときは、レポート出力先の生成物を読む。

## hash
- f3d43d08484e7e18e8755048a786721d887662c40d59c1c86c9a68c8774c0e7b

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
