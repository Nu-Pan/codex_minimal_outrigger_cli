# `apply`

## Summary
- apply run の開始、進行、破棄、取り込み、実行時状態管理、実行結果 report 生成を扱うサブコマンド実装群への入口。
- session branch と apply branch/worktree をまたぐ状態検証、isolated worktree 上での Codex CLI 実行、process id 管理、成果の merge、後片付け、警告・report 出力など、apply 系操作の制御フローを調べる起点になる。
- 個別の責務は、破棄、fork 実行、fork report、join、process/worktree runtime helper に分かれており、apply の利用者向け挙動と低レベル実行時状態の両方へ分岐する階層。

## Read this when
- apply 系サブコマンド全体のどの実装へ進むべきかを選びたいとき。
- apply run の開始から join または abandon までの状態遷移、branch/worktree 操作、process id 管理、report 出力の関係を把握したいとき。
- apply branch/worktree の作成・探索・削除、session state の更新、clean worktree 検証、merge conflict、warning 出力など、apply 操作の副作用を調べたいとき。
- apply fork の反復制御、finding 適用、禁止対象差分の rollback、commit 作成、converged 判定、通常・エラー report の生成経路を確認したいとき。
- running 状態の apply process を停止する処理、pid file、pidfd、process start time、stale pid の扱いなど、apply 実行時状態の低レベル処理へ進みたいとき。

## Do not read this when
- apply 以外のサブコマンド、session 管理、config schema、git wrapper の一般挙動だけを調べたいとき。
- oracle file、realization file、INDEX.md 生成規則など、仕様文書やルーティング文書の方針そのものを確認したいとき。
- Codex CLI に渡す prompt や parameter 構築だけを調べたいときは、それを組み立てる実装へ直接進む。
- 共通 runtime の branch 操作、state 読み書き、report 保存先、git command 実行など、apply 固有でない helper の詳細だけを確認したいときは共通実装へ直接進む。
- 特定の apply 操作に読む対象がすでに決まっており、破棄、fork、join、report、process 管理のいずれかの本文へ直接進めるとき。

## hash
- 24780d44ae972d7a71c690bc14fd580e3fc7af0149192836ce6395259484cda7

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
- active session branch 上の oracle を isolated review worktree でレビューするサブコマンド実装の入口を扱う。
- scope 検証、session branch と worktree 状態の前提確認、review 用 branch/worktree の作成と後始末、対象 oracle file の列挙、Codex 実行ループ、INDEX 変更の commit/merge、review report 出力までの orchestration を担う。
- レビュー対象の列挙、レビュー実行ループ、report 描画、merge conflict 解決などの詳細処理は下位 helper module に委譲し、この対象はそれらを CLI コマンドとして接続する位置づけにある。

## Read this when
- oracle review サブコマンドの実行順序、前提条件、失敗時 report 出力、または一時 review worktree と一時 branch のライフサイクルを確認したいとき。
- review scope の受け付け条件や、active session branch・clean worktree・cmoc ignore 確保などの preflight がどこで行われるかを追うとき。
- oracle review の処理全体で、対象列挙、Codex review loop、INDEX 変更 commit、review branch merge、report 書き込みがどの順でつながるかを把握したいとき。
- CLI 層から review 関連 helper へ渡される主要な値、特に session state、config、review worktree、review branch、fork/join commit、findings の流れを確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択の詳細だけを確認したい場合は、対象列挙を担当する helper を読む。
- Codex に渡す review prompt、review loop の反復制御、finding の merge operation 適用の詳細だけを確認したい場合は、review loop 側の helper を読む。
- review report の表示形式、finding section の描画、report file の書き込み内容だけを変更したい場合は、report 生成を担当する helper を読む。
- review branch の merge、INDEX 変更 commit、conflict 解決、worktree status path の扱いだけを調べたい場合は、review index 操作を担当する helper を読む。
- 通常の indexing preflight の中身や、Codex 実行・git worktree 作成・branch 削除など runtime 共通処理の実装詳細を確認したい場合は、それぞれの共通 helper を直接読む。

## hash
- 683f45afe7813f49a04b82cb6d1ba48c5faf9f4a588193292002d1d82a68fc2d

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
- session 系サブコマンドの実装をまとめるパッケージで、session branch の作成、home branch への取り込み、破棄などの個別操作へ進む入口になる。
- 各サブコマンドは、session state、branch 状態、clean worktree などの事前条件を確認し、git 操作と状態更新を組み合わせて session のライフサイクルを制御する。
- CLI 入口は共通のサブコマンド実行ラッパーに接続され、利用者向け出力や失敗時の CmocError 報告もこの配下の各実装が担う。

## Read this when
- session branch の作成、home branch への merge、merge せずに破棄する処理など、session 操作のサブコマンド実装を探したいとき。
- session 操作で確認される事前条件、state 遷移、branch 切り替え・削除、clean worktree 判定の呼び出し位置を追いたいとき。
- session 系 CLI の実処理が共通 CLI ラッパーへどう接続され、成功時出力や失敗時エラーをどう扱うかを確認したいとき。

## Do not read this when
- session state のデータ構造、state file の schema、branch 判定、git 実行 helper、path model などの共通部品そのものを調べたいとき。
- session 以外のサブコマンド、Typer アプリ全体の登録構造、共通 CLI ルーティングを調べたいとき。
- apply、review、indexing など、session 操作から呼ばれる可能性はあっても主責務が別サブコマンドや共通機能にある処理を調べたいとき。

## hash
- 6ed35528e60bc98827337d369834f9c4e5c314839c1a58ba3a70b12539ffdc82

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
