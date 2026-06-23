# `apply.py`

## Summary
- apply fork の実行、apply branch の session branch への join、未 join apply run の abandon を扱うサブコマンド実装。
- apply 用 linked worktree と branch の作成・削除、session state の apply 状態遷移、finding の列挙・refine・適用 loop、join 時の想定外差分検査と INDEX.md conflict の機械解決をまとめて扱う。
- apply run のライフサイクル、許可される apply/session 差分、apply branch と session branch の worktree 解決に関する入口になる。

## Read this when
- apply fork/join/abandon の事前条件、状態遷移、終了コード、表示内容、cleanup 挙動を確認または変更したいとき。
- apply branch・apply worktree の作成、merge、削除、force-resolve、unexpected changes 判定に関わる挙動を追いたいとき。
- finding の refine/application loop、dirty target 更新、apply report/error report の呼び出しタイミングを確認したいとき。
- apply 中に許可される差分と禁止される差分、INDEX.md だけの merge conflict をどう扱うかを確認したいとき。

## Do not read this when
- CLI の typer command 宣言や option 定義だけを確認したいときは、サブコマンドの登録側を読む。
- finding の生成プロンプトや apply fork 用パラメータ構築の詳細を確認したいときは、acp.builder.apply.fork 側を読む。
- git 操作、state 読み書き、worktree 作成削除などの低レベル runtime helper の実装を確認したいときは、runtime 側を読む。
- 設定 schema や apply fork の loop 回数などの設定項目定義だけを確認したいときは、設定モデル側を読む。

## hash
- 600a025e951f9f61cd05e6ccdc05afe51907c243ee4b203e5ef76521cd113635

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
- 764ded2bfb5029ee6e4e562dc675abe45a11a4f36591f0e50e2d56ece73da8d8

# `session.py`

## Summary
- cmoc の session 操作の実装であり、通常 branch から session branch を作成し、session branch を home branch へ join し、または merge せず abandon する制御を扱う。
- session 状態ファイルの生成・更新、cmoc 管理 branch での実行拒否、worktree clean 確認、`.cmoc` ignore 確保、session home branch への切り替え、session branch の削除を含む。
- join 時の merge conflict では、conflict 対象を検出して Codex CLI 用の conflict resolution parameter を組み立て、解決後の marker 残存・unmerged path を確認して merge commit を完了する入口になる。

## Read this when
- session fork、join、abandon の実行条件、状態遷移、git 操作、副作用、CLI 出力を確認または変更したいとき。
- active session の重複検出、session branch 名、session home branch、session state file の扱いを追いたいとき。
- session join の merge conflict 解決フロー、Codex CLI 呼び出し、conflict marker 検査、git add/commit の制御を確認したいとき。
- session 操作で発生する CmocError の条件や利用者向け復旧案を調べたいとき。

## Do not read this when
- session 以外の sub command の CLI 定義、引数宣言、Typer app への登録だけを確認したいとき。
- SessionState のデータ構造、状態ファイルの path 規則、git helper、branch 判定、worktree 判定そのものの実装を確認したいとき。
- session join conflict resolution parameter の文面や AgentCallParameter の組み立て詳細だけを確認したいとき。
- oracle 側の正本仕様断片、path keyword の定義、INDEX.md 生成規則を確認したいとき。

## hash
- 1ac7da085f1c6dab065f696400c7fce368e566dccb93384559fce067eaca0cb1

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実処理を担う実装。`.cmoc` の git ignore 保証、オリジナルプロンプト用 markdown ファイルの初期生成、エディタ起動、HTML コメント除去と strip、パラメータ解決 agent call、完全 prompt 生成、Codex CLI/TUI 起動を扱う。

## Read this when
- `cmoc tui` の実行フロー、エディタ選択、プロンプト保存先、コメント除去、解決済みパラメータからの最終 `AgentCallParameter` 構築を確認または変更したいとき。

## Do not read this when
- TUI 用パラメータ解決 prompt や JSON schema の詳細だけを確認したいときは、`acp/builder/tui` 側を読む。
- Codex CLI/TUI subprocess の profile 生成や CODEX_HOME 検証そのものを調べたいときは、runtime helper を読む。

## hash
- manual
