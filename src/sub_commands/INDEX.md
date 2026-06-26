# `apply`

## Summary
- apply 系サブコマンドの実装群をまとめる領域。apply run の開始、破棄、join、実行状態管理、実行結果 report 生成までの入口になる。
- apply 用 worktree と branch、session state、process id、実行中 process の停止、差分適用 loop、merge・cleanup・report 出力など、apply run のライフサイクルに関わる実装へ進むための案内対象。

## Read this when
- apply run の開始から完了・破棄までの状態遷移、実行条件、cleanup、利用者向け出力のどの実装を読むべきか切り分けたいとき。
- apply branch や apply worktree の作成・探索・削除、session branch への join、running process の停止、process id の永続化など、apply 実行時状態に関係する処理を調べる入口が必要なとき。
- apply fork の調査対象列挙、finding 適用 loop、commit 作成、編集禁止対象の差分検出、通常終了・エラー終了 report の生成経路を追いたいとき。
- apply abandon、apply join、apply fork のどれに関係する変更か未確定で、同階層の具体的な実装対象へ進む前に責務境界を確認したいとき。

## Do not read this when
- apply 以外のサブコマンド、CLI 共通実行ラッパー、git 実行 helper、worktree 操作 helper、状態ファイル I/O の共通処理だけを調べたいとき。
- session state file 全体の schema、path model、oracle や routing 文書の一般仕様など、apply 固有ではない定義を確認したいとき。
- finding 列挙や finding 適用の parameter 構築、変更要約 prompt、indexing preflight など、apply から呼ばれる別責務の詳細だけを調べたいとき。
- 特定の apply サブコマンドや低レベル runtime helper が読む対象として既に分かっており、この領域全体の責務境界を確認する必要がないとき。

## hash
- 859759017c6fd0dddf84700124302cab37fd3f8e5e6db1bae1acfef65c421b54

# `indexing.py`

## Summary
- 現在の work root に対するルーティング目次の更新を実行するサブコマンド実装。実行前条件の確認、排他ロック、対象ディレクトリ走査、既存エントリーの再利用、Codex による不足エントリー生成、更新差分のコミットまでをまとめて扱う。
- 目次生成対象から除外する条件、対象内容の取り出し、鮮度判定用ハッシュ、Structured Output から Markdown エントリーへ変換する処理の入口になる。

## Read this when
- 目次更新サブコマンドの実行フロー、preflight 連携、排他制御、更新後コミットの挙動を確認または変更したいとき。
- 目次生成対象に含めるファイル・ディレクトリ、除外条件、既存エントリー再利用条件、深い階層から再生成する順序を調べたいとき。
- Codex 呼び出しで目次エントリーを生成する経路、生成 prompt に渡す対象内容、Structured Output の検証と Markdown 描画を追いたいとき。
- 目次エントリーのハッシュ検証、必須セクション判定、古いエントリーを再生成する条件に関わる不具合を調査するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや利用者向け機能を調べたいだけで、目次更新処理に関係しないとき。
- Codex 実行ラッパー、git コマンド実行、設定読み込み、ignore 判定などの共通 runtime 実装そのものを変更したいとき。
- 生成される目次エントリーの内容方針や prompt パラメータの仕様だけを確認したいときは、その構築元を直接読む。
- 正本仕様やルーティング文書の記述方針を確認したいだけで、実装上の走査・生成・コミット処理を追う必要がないとき。

## hash
- b861a2700ec18e93a2f924e78d4298110459a99188cc9fb4e01cdb656da25187

# `init.py`

## Summary
- 作業ツリーを cmoc が扱える初期状態へ同期するサブコマンド実装を扱う。実行前の利用者差分を init commit に混ぜないよう staged 差分と .gitignore 状態を退避・復元し、cmoc 用 ignore と設定同期、必要な初期化 commit、成功時の Markdown 出力をまとめて担う。

## Read this when
- 初期化サブコマンドの実行順序、ログ作成前の ignore 保証、設定同期、初期化 commit の条件を確認・変更したいとき。
- 利用者の既存 staged 差分や .gitignore の作業ツリー・index・HEAD 状態を、初期化処理後にどう復元するかを調べたいとき。
- 初期化成功時に標準出力へ出す Markdown 形式の結果表示を確認・変更したいとき。

## Do not read this when
- 初期化以外のサブコマンドの CLI 制御や出力を調べたいとき。
- cmoc 用 ignore の具体的な追記規則そのものや、設定同期処理の中身を調べたいとき。
- git 実行ラッパー、work root・repo root の解決、共通のサブコマンド実行基盤を調べたいとき。

## hash
- d458d8f2867e4dcf14fa58d8f2b16b6ca84c25b5cadf47172131cd16b9070d32

# `review.py`

## Summary
- `review oracle` サブコマンドの実行入口と全体制御を担う実装。indexing preflight、CLI 実行ラッパーへの接続、scope 検証、active session branch と clean worktree の前提確認、isolated review worktree の作成・削除、oracle 対象列挙、レビュー loop 実行、INDEX 変更 commit・merge、成功時または例外時の report 書き出しまでを一連の処理として接続する。
- レビュー対象の列挙、review loop、finding の反映、report 描画、index 変更 commit や merge conflict 解決などの詳細処理は下位 helper から import して公開し、このモジュール自体はそれらを組み合わせる orchestration の入口として位置づく。

## Read this when
- `cmoc review oracle` のコマンド入口、実行前提、scope の扱い、または `run_cli_subcommand` や `run_codex_exec` との接続を確認したいとき。
- review 用の一時 branch と worktree をどのタイミングで作成・削除し、どの commit を fork/join として report に渡すかを追いたいとき。
- oracle file の列挙から review loop、INDEX 変更 commit、現在 worktree への merge、report 出力までの高レベルな制御順序を確認したいとき。
- レビュー処理中に例外が起きた場合でも report を書き、report path を出力してから例外を再送出する流れを確認したいとき。

## Do not read this when
- review report の本文構成、finding section の描画、path 表示など、report 生成の詳細だけを確認したいときは report 用 helper を読む。
- oracle file の列挙条件や scope ごとの対象選択だけを確認したいときは target 列挙用 helper を読む。
- review loop 内で Codex をどのように呼び、finding をどう解釈・反映するかを確認したいときは loop 用 helper を読む。
- review branch の merge、INDEX 変更 commit、conflict 解決、worktree status path の詳細だけを確認したいときは index 操作用 helper を読む。

## hash
- e6a30374dc3d17a3e77459083f51a96bf3a2585853e31e1e614e2cee1f266c19

# `review_index.py`

## Summary
- review 用 worktree で生成されたルーティング文書の差分を検査し、許可された変更だけを commit する処理を担う。
- review branch を session branch へ merge し、競合がルーティング文書だけに限定される場合は現在側を採用または削除して自動解決する。
- git の status、diff、merge、checkout、rm、commit などを呼び出す制御と、想定外差分や merge 失敗時の cmoc 向けエラー化をまとめている。

## Read this when
- review oracle が作成したルーティング文書差分だけを commit する条件や、ルーティング文書以外の差分を拒否する挙動を確認したいとき。
- review branch の merge 後 HEAD 取得、merge 失敗時の扱い、未解決競合の自動解決条件を確認したいとき。
- git status の porcelain 出力から変更パスを抽出する処理、rename/copy の扱い、unmerged stage の確認方法を調べたいとき。

## Do not read this when
- 通常のサブコマンド引数定義、CLI 出力形式、ユーザー入力の parsing を調べたいだけのとき。
- ルーティング文書の内容生成、要約文作成、Structured Output の schema 定義を調べたいとき。
- oracle file と realization file の概念やルーティング文書そのものの仕様を確認したいとき。

## hash
- fd46086c773e71294be6c9b8ed3da758d0729bfa1dc795d5f35336f661efd447

# `review_loop.py`

## Summary
- review oracle による finding の列挙、統合、検証、判定を Codex 実行ループとして制御する実装。oracle ごとの dirty 管理、finding_id や検証理由・判定結果の初期値付与、merge 操作の適用と妥当性検証、finding の oracle_path 解決を扱う。

## Read this when
- review oracle の finding enumerate/merge/validate/judge の実行順序、反復回数、dirty 条件、Codex 呼び出しパラメータ生成との接続を確認したいとき。
- finding の merge 操作で delete/replace/merge がどの条件で受理され、既存 finding がどう削除・追加されるかを確認したいとき。
- finding に含まれる oracle_path を実パスへ解決し、特定 oracle に関連する finding を絞り込む挙動を確認したいとき。
- review oracle が finding_id、advocate_reasons、challenger_reasons、verdict、judge_reason をどの段階で補完・更新するかを確認したいとき。

## Do not read this when
- 個々の Codex プロンプトや Structured Output parameter の本文を確認したいだけの場合は、review oracle 用 parameter builder を直接読む。
- CLI サブコマンドの引数定義、設定読み込み、ログルートや worktree の準備を確認したい場合は、呼び出し元のサブコマンド実装を読む。
- review oracle の反復回数など設定値の定義やデフォルトを確認したい場合は、設定モデルを読む。
- oracle file の正本仕様そのものや review 観点を確認したい場合は、対象の oracle 文書を読む。

## hash
- d116a58b5c91dcc0446b89b792e5dd64c675efd7a66b3858cb3fbbfd92e54581

# `review_report.py`

## Summary
- review oracle の実行結果を、人間が読む Markdown レポートとして生成する処理を扱う実装。レビュー対象 oracle、findings、ブランチ・コミット情報、セッション情報を集計し、YAML frontmatter と判定本文を含む report を組み立てて保存する。
- レポート全体の結果判定、finding の fatal/minor・accept/reject 別集計、oracle path の表示用正規化、finding セクションの表示形式を確認する入口になる。

## Read this when
- review oracle のレポートファイルの生成先、ファイル名、本文構成、frontmatter の項目、または Markdown 表示内容を変更したいとき。
- review oracle の結果が error、no_targets、fatal、minor、ok のどれになるかという判定条件を確認・変更したいとき。
- finding の verdict や severity に基づく集計、accepted/rejected findings の表示、finding セクションの文言を扱うとき。
- oracle file のパスをレポート上でどのように相対表示するか、特に oracle 配下の path 表示を確認したいとき。

## Do not read this when
- review oracle の対象 oracle をどう収集するか、findings をどう作るか、レビュー処理をどう実行するかを調べたいだけのとき。
- cmoc 全体の CLI 引数定義、サブコマンド登録、セッション状態の永続化、reports directory や timestamp の基本仕様を調べたいとき。
- review oracle 以外の report 形式や、oracle ではない対象のレビュー結果出力を扱うとき。
- INDEX.md 生成、oracle file の正本仕様そのもの、または realization/oracle の概念定義を調べたいとき。

## hash
- a5221d79c1395efd3e3b7f959854e3d8eedebdc33cbfc97660b2e8cead1f8bb9

# `review_targets.py`

## Summary
- review oracle の対象となる oracle file を列挙するための実装。scope が full の場合は全 oracle file、差分対象の場合は session_start_commit から HEAD までに oracle 配下で変更された oracle file だけを返す。
- oracle 配下を再帰的に探索し、ファイルであり、INDEX.md ではなく、git ignore 対象でもないものを review 対象候補として扱う。

## Read this when
- review oracle の対象ファイル選定ロジックを確認・変更したいとき。
- full scope と差分 scope で review 対象がどう変わるかを確認したいとき。
- oracle file の列挙条件、特に INDEX.md 除外や git ignore 除外の扱いを確認したいとき。
- session_start_commit がない場合の差分 review 対象の扱いを確認したいとき。

## Do not read this when
- review の出力形式、診断内容、表示文言、または実際の review 実行処理を確認したいだけのとき。
- oracle file の概念定義や正本仕様としての扱いを確認したいとき。
- oracle 以外の realization file やテストファイルの列挙条件を探しているとき。
- git command 実行 helper や git ignore 判定 helper の内部挙動を確認したいとき。

## hash
- e4fe225944db001b5a92abe25348f5974e8b0f165bb69cba1f701a019706deaa

# `session`

## Summary
- session 系サブコマンドを実装するパッケージで、通常 branch から session branch を作る処理、active session を home branch へ取り込む処理、merge せず破棄する処理を入口ごとに分けて収める。
- 各サブコマンドは、branch/state/worktree の事前条件確認、git 操作、状態更新、利用者向け出力、共通 CLI 実行ラッパーへの接続を担い、個別の session 操作を調べる起点になる。

## Read this when
- session fork、join、abandon のどれを読むべきかを選びたいとき。
- session branch の作成、home branch への merge、merge しない破棄など、session 系サブコマンドの実行条件や状態遷移を確認または変更したいとき。
- session 系サブコマンドが共通 CLI runner、indexing preflight、git 操作、session state 更新とどう接続されているかを追いたいとき。
- session 操作の失敗時挙動、rollback、merge conflict 解消、利用者向け出力、CmocError の発生条件を調べる入口を探しているとき。

## Do not read this when
- session state の schema、state path 算出、branch 判定、worktree clean 判定、git 実行 wrapper、timestamp 生成などの共通 runtime 実装そのものを確認または変更したいとき。
- Typer アプリへのサブコマンド登録、session 以外のサブコマンド、または CLI 全体のルーティングを調べたいとき。
- merge conflict 解消依頼に渡す Codex CLI parameter や indexing preflight の内部挙動を確認または変更したいとき。
- 個別の処理対象が session fork、join、abandon のいずれかに明確に決まっているときは、この階層ではなく該当する実装モジュールへ直接進む。

## hash
- 2c94229e6bf4e07f89b80f8307aedabd1e6dbb7912b2d12d0ad472bef5b69bdf

# `tui.py`

## Summary
- 利用者が編集した依頼文を起点に、TUI 用の実行パラメータ解決、完全 prompt の生成・保存、Codex TUI 起動までをつなぐサブコマンド実装。
- 依頼文テンプレートの作成、エディタ選択・起動、HTML コメント除去、解決済み JSON からの AgentCallParameter 構築、Markdown 見出しの StructDoc 変換を扱う。

## Read this when
- 対話的に依頼文を編集して Codex TUI を起動する処理の流れを確認・変更したいとき。
- TUI 起動時の file access mode、model class、reasoning effort、完全 prompt 生成、structured output schema の扱いを確認したいとき。
- 利用可能なエディタの選択順、エディタ異常終了時のエラー、依頼文テンプレートや保存先 log 領域の扱いを変更したいとき。
- TUI 向けパラメータ解決結果の JSON から値や真偽値を取り出す規則、または Markdown 見出しを構造化 prompt に変換する規則を確認したいとき。

## Do not read this when
- 通常の非対話 CLI 実行、Codex exec の低レベル実行、または TUI 以外のサブコマンド起動処理だけを調べたいとき。
- TUI パラメータ解決用 prompt の具体的な schema や選択肢定義そのものを調べたいときは、その解決パラメータを構築する側を読む。
- 完全 prompt の共通フォーマットや StructDoc の markdown レンダリング仕様を調べたいときは、prompt 構築・構造化文書レンダリング側を読む。
- INDEX 生成の preflight 処理そのものを調べたいときは、indexing の preflight 実装を読む。

## hash
- da24e922e6a1930a64a5667c2c3867e90de41524c59de1c97005abece970b630
