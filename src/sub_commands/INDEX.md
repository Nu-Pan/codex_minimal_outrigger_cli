# `apply`

## Summary
- apply run の開始、完了取り込み、破棄を担うサブコマンド実装と、それらに付随する実行時 helper、process id 管理、worktree・branch 解決、実行結果 report 生成をまとめる領域。
- session branch と apply branch の状態検証、isolated worktree 上での所見列挙・適用・commit、join 時の想定外差分検出・force resolve・merge、abandon 時の cleanup など、apply lifecycle の制御フローへの入口になる。
- apply 中の編集禁止対象差分の rollback、INDEX.md conflict の限定的な自動解決、Linux pidfd と /proc による apply process 同一性確認など、apply 固有の安全制御も扱う。

## Read this when
- apply fork、apply join、apply abandon の実行条件、状態遷移、終了時 cleanup、CLI 出力、report 出力を確認・変更したいとき。
- apply worktree、apply branch、oracle snapshot commit、session state の関係や、apply run が ready・running・completed・error の間をどう遷移するかを追いたいとき。
- apply scope から調査対象ファイルを選ぶ処理、所見列挙・所見適用・変更 path 検出・commit 生成を含む apply loop を調べたいとき。
- apply join の想定外差分判定、force resolve、merge conflict 処理、INDEX.md だけの conflict 自動解決を確認したいとき。
- apply abandon で実行中 process を停止し、apply worktree・branch・process id・state を破棄する順序や警告出力を確認したいとき。
- apply process id file、pidfd、process start time、linked worktree 探索など、apply 専用の低レベル実行時状態を確認したいとき。

## Do not read this when
- apply 以外のサブコマンドの CLI 実装、状態遷移、report 形式を調べたいとき。
- session state file の schema、path model、branch 名規則、git・worktree 操作 helper、設定読み込みなどの共通定義そのものを確認したいとき。
- Codex 呼び出し用 prompt や structured output schema の詳細だけを変更したいときは、apply 用 builder 側を直接読む。
- oracle file、realization file、INDEX.md 生成規則など、仕様文書やルーティング文書の一般方針を調べたいとき。
- apply fork report や join report の保存先管理、timestamp 生成、git command wrapper の低レベル挙動だけが目的で、apply 固有の制御フローを読む必要がないとき。

## hash
- 8cbd022e6a31da6350e456a9c9ef78cc48bab129c306012a8146431f11de510f

# `indexing.py`

## Summary
- 現在の work root を対象に、階層ごとのルーティング文書を再生成し、差分がある場合は専用 commit として保存するサブコマンド実装。
- 対象の直下要素を列挙し、既存エントリーの hash を再利用できるか判定し、必要な要素だけ Codex 実行でエントリー生成する処理をまとめている。
- 排他 lock、事前条件確認、git ignored・binary・memo 除外、ディレクトリ hash 計算、Structured Output から Markdown エントリーへの描画までを扱う。

## Read this when
- ルーティング文書の生成・更新・commit 作成の流れを確認または変更したいとき。
- エントリー再生成の鮮度判定、hash 抽出、既存エントリー再利用、対象ファイル・ディレクトリの除外条件を調べたいとき。
- インデックス更新の preflight、CLI 実行時の前提条件、repository ごとの排他制御を扱う必要があるとき。
- Codex に渡すエントリー生成入力や、Structured Output から Markdown へ変換する処理を変更したいとき。

## Do not read this when
- 個別サブコマンドの一般的な起動ラッパーやログ記録の仕組みだけを調べたいときは、共通の CLI 実行基盤を読む。
- Codex 実行前 preflight の共通登録・設定方法だけを調べたいときは、preflight 用の共通モジュールを読む。
- エントリー生成 prompt の内容や AgentCallParameter の組み立て自体を変更したいときは、builder 側のエントリー生成パラメータ実装を読む。
- パス概念、git 実行、設定読み込み、binary 判定、ignored 判定などの低レベル runtime helper の仕様を調べたいときは、runtime 側の実装を読む。

## hash
- cce0bc7a9800ec49ec7d474d6f224adefc9d446a99f3f0dbc7eaf161b451fa01

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
- active session branch の oracle レビューを、隔離した review worktree 上で実行するサブコマンド実装の入口を担う。
- scope 検証、session 状態確認、clean worktree 確認、review 用 branch/worktree の作成・削除、レビュー対象列挙、レビュー loop 実行、INDEX 変更 commit と merge、レポート出力までの制御フローをまとめる。
- レビュー対象列挙、レビュー loop、レポート描画、INDEX 変更の conflict 解決などの詳細処理は別モジュールへ委譲し、この対象はそれらを組み合わせる orchestration 層として位置づけられる。

## Read this when
- oracle レビューサブコマンドの実行順序、事前条件、失敗時のレポート出力、review branch/worktree のライフサイクルを確認したいとき。
- active session branch 上でのみ実行する制約、scope の許容値、clean worktree や cmoc ignore の確認がどこで行われるかを追うとき。
- レビュー結果の INDEX 変更が session 側へ merge される条件や、作成した一時 branch/worktree の後片付けを調べるとき。
- CLI command から内部実装へ渡される codex 実行関数や command metadata の接続を確認したいとき。

## Do not read this when
- レビュー対象となる oracle file の列挙条件だけを知りたいときは、対象列挙を担当するモジュールを読む。
- Codex によるレビュー loop の prompt、反復制御、finding の merge 操作を調べたいときは、レビュー loop を担当するモジュールを読む。
- レビュー報告書の本文構成、path 表示、finding section の描画、レポート書き込み形式を確認したいときは、レポート生成を担当するモジュールを読む。
- INDEX 変更の commit、merge、conflict 解決、worktree status path の詳細を調べたいときは、INDEX 変更処理を担当するモジュールを読む。
- indexing preflight 自体の仕様や実装を確認したいだけのときは、preflight を定義するモジュールを読む。

## hash
- cdfc19973f45ae6a8c404fc7ecf1b02aa715e0a6a4de598589c3c70252a28128

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
