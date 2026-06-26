# `apply`

## Summary
- apply 系サブコマンドの実装群をまとめる領域。未 join の apply run を作成して findings を適用する処理、成果を session branch へ取り込む処理、未完了 run を破棄する処理、実行時 process・worktree・branch・state の管理、fork 結果レポート生成への入口になる。
- apply run の lifecycle 全体に関わる高レベルな CLI 制御と、branch/worktree/process/report などの apply 専用 runtime 補助処理が分かれているため、apply の開始・完了・破棄・停止・レポートのどこを調べるかを選ぶための起点として使う。

## Read this when
- apply run の開始、join、abandon、process 停止、worktree/branch cleanup、state 更新、report 生成のどの実装へ進むべきかを判断したいとき。
- apply fork が対象 file を列挙し、Codex に finding 列挙・適用を行わせ、commit や report を作成する一連の制御を確認・変更したいとき。
- apply join で apply branch の成果を session branch へ merge し、想定外差分や merge conflict を扱い、apply state を ready 相当に戻す処理を調べたいとき。
- 未 join の apply run を破棄し、実行中 process の停止、apply worktree・branch・pid file の削除、state 初期化を行う処理を調べたいとき。
- apply 専用の pid file、pidfd、process start time、linked worktree 探索、branch から worktree path を導く処理など、実行時状態の低レベル操作を確認したいとき。
- apply fork 後に保存される Markdown/frontmatter 付き report、差分要約、要約失敗時 fallback、changed path 収集を確認・変更したいとき。

## Do not read this when
- apply 以外のサブコマンドの CLI 登録、共通 runtime、git 実行 wrapper、state file の汎用 schema、path keyword の定義だけを調べたいとき。
- oracle の正本仕様、INDEX.md 生成規則、path model、文書ルーティング方針そのものを確認したいとき。
- 個別の apply サブコマンドや helper の責務がすでに分かっており、その本文へ直接進めるとき。
- 生成済み report の内容を読むだけで、report 生成ロジックや fallback 挙動を変更しないとき。
- process 停止、pid file、worktree 探索、report 生成、fork/join/abandon のいずれにも関係しない差分適用外の実装を調べたいとき。

## hash
- a34cf8411c3efec99e4047ded56c40f46eef0b3d207ed5641664e560a731c196

# `indexing.py`

## Summary
- 作業ツリー内のルーティング目次を保守するサブコマンド実装。実行前条件の検査、排他 lock、目次対象の列挙、既存エントリーの再利用判定、Codex による不足エントリー生成、更新差分の commit までを扱う。
- 目次生成の対象から memo、git ignore、隠し項目、binary、既存の目次ファイルを除外し、対象内容の hash によって再生成要否を決める。
- Structured Output から目次エントリー Markdown を組み立て、必須セクションと hash 形式を満たす既存エントリーだけを鮮度判定に利用する。

## Read this when
- 目次保守サブコマンドの実行フロー、preflight 登録、clean worktree などの実行前条件を確認したいとき。
- どのディレクトリやファイルが目次生成対象になるか、対象除外条件、hash 計算、深い階層からの更新順を調べたいとき。
- 既存目次エントリーの parse、必須セクション検証、Structured Output からの Markdown 生成、Codex 呼び出し失敗時の扱いを変更したいとき。
- 目次更新差分を git add/commit する条件や、同時実行を防ぐ lock file の扱いを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや CLI 引数全体の定義を探しているだけなら、該当するサブコマンド実装や CLI 登録側を読む。
- Codex 呼び出し用 parameter の具体的な prompt 構築を変更したい場合は、builder 側のエントリー生成 parameter 実装を読む。
- path keyword の意味、work root や repo root の定義そのものを確認したい場合は、path model や runtime 側の path 解決実装を読む。
- 目次エントリー本文の望ましい書き方や仕様判断を確認したいだけなら、正本仕様文書を読む。

## hash
- cc5fcceee8b98c869e9abc5472d39f82e218ab00c62e7999912c4bee7105176f

# `init.py`

## Summary
- `cmoc init` サブコマンドの実行本体を扱う。CLI runtime 経由で初期化処理を起動し、work root の `.cmoc` ignore 保証、設定同期、初期化コミット作成、利用者が事前に持っていた staged 差分と `.gitignore` 状態の復元をまとめて担う。
- 初期化成功時に stdout へ出す Markdown 形式の結果文もここで組み立てる。

## Read this when
- `cmoc init` の実行順序、初期化コミット、設定同期、または `.cmoc` を `.gitignore` に含める処理を確認・変更したいとき。
- 初期化前から存在する `.gitignore` の worktree/index/HEAD 状態や、利用者が事前に staged していた差分を `cmoc init` 後にどう戻すかを調べるとき。
- `cmoc init` のログ作成前に行う ignore 保証と、その副作用を後続の復元処理から区別する仕組みを確認したいとき。
- `cmoc init` 成功時の利用者向け Markdown 出力を変更・検証したいとき。

## Do not read this when
- 個別の git コマンド実行 wrapper、runtime 共通処理、repo/work root 解決、設定同期、または ignore パターン生成そのものの実装を調べたいだけのときは、それらを定義する共通 runtime 側を読む。
- 他のサブコマンドの CLI 挙動、出力、状態復元を調べたいときは、対象サブコマンドの実装へ進む。
- `cmoc init` の外部挙動をテスト観点から確認したいだけのときは、対応するテストを読む。

## hash
- a7f12d58923b83b9f3941a0e829e20e9ed445db35c3a5fc9c20b6112c3620faf

# `review.py`

## Summary
- review oracle サブコマンドの実行入口と実行順序を担う実装。active session branch 上で clean worktree を要求し、isolated review worktree と一時 review branch を作成して oracle 対象列挙、Codex によるレビュー、INDEX 変更 commit、必要時の merge、worktree/branch cleanup、review report 出力までを統括する。
- 対象列挙、レビュー loop、INDEX 変更処理、report 描画・書き込みなどの詳細処理は専用モジュールへ委譲し、この実装は CLI runtime 連携、事前条件検証、実行ライフサイクル、例外時 report 出力を結合する上位制御として位置づけられる。

## Read this when
- review oracle コマンドの全体フロー、実行前条件、scope の扱い、一時 worktree と review branch の作成・削除、review 結果の merge 条件、成功時または失敗時の report 出力タイミングを確認したいとき。
- review oracle 実行時にどの下位モジュールが呼ばれるか、対象列挙・レビュー実行・INDEX 変更 commit・report 書き込みがどの順序で接続されるかを追いたいとき。
- active session branch 以外、dirty worktree、不正 scope などで review oracle が拒否される条件を調べたいとき。
- review oracle の例外処理で、途中まで収集した oracle file、findings、review branch 情報を report に残してから再送出する挙動を確認したいとき。

## Do not read this when
- oracle file の列挙規則、scope ごとの対象選択、session state からの対象抽出の詳細だけを確認したいときは、対象列挙を担う下位実装を読む。
- Codex に渡す review prompt、finding の解釈、finding からの merge operation 適用など、レビュー loop 内部の詳細だけを確認したいときは、レビュー loop を担う下位実装を読む。
- INDEX 変更の conflict 解決、review worktree の status 判定、review branch の merge 手順だけを調べたいときは、review index 操作を担う下位実装を読む。
- review report の本文構成、finding section の描画、path 表示、report ファイルの保存内容だけを確認したいときは、report 生成を担う下位実装を読む。
- CLI 全体の subcommand 登録や Typer app のコマンド宣言だけを確認したいときは、サブコマンド登録側の実装を読む。

## hash
- 811bc3705ec0a8a9aebfe4af0e926474c1ffbee713bdf047fb94d2b067e99064

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
- session 系サブコマンドの実行実装をまとめるディレクトリ。active session の作成、home branch への取り込み、merge せず破棄する処理を扱う。
- 各サブコマンド実装は CLI runtime wrapper 経由で本体処理を実行し、session/apply state、branch、clean worktree、cmoc ignore 設定などの前提条件確認と、成功時または失敗時の利用者向け出力・エラー情報を担う。
- session パッケージ自体の初期化処理は最小限で、具体的な挙動は下位モジュールごとに分かれている。

## Read this when
- session 系サブコマンドの実装入口を探し、fork、join、abandon のどの処理へ進むべきか判断したいとき。
- active session branch の作成、home branch への merge、merge せず破棄する操作の事前条件、状態更新、branch 操作、CLI 出力の実装を調べたいとき。
- session 操作と clean worktree、managed branch、session/apply state、cmoc ignore 設定、rollback、merge conflict 解消制御の関係を追いたいとき。
- session 系サブコマンドに関する利用者向けエラー、警告、成功メッセージ、復旧案内の実装箇所を探したいとき。

## Do not read this when
- session state や apply state の schema、永続化形式、branch から state を読み込む共通処理そのものを調べたいとき。
- git command wrapper、worktree clean 判定、repo/work root 解決、cmoc ignore 判定など、session サブコマンドから呼ばれる共通 helper の内部実装を調べたいとき。
- CLI 全体のサブコマンド登録、runtime wrapper の共通構造、または session 以外のサブコマンド実装を調べたいとき。
- oracle 上の正本仕様、ルーティング文書の規則、またはテスト側の検証内容を確認したいとき。

## hash
- a4bb4b50a56075611bced5f6a9655f6ce56b4a7e6e81b7e64c38b00aadf9c96b

# `tui.py`

## Summary
- `cmoc tui` の実行フローを実装するサブコマンド本体。利用者が編集する依頼文の作成、エディタ起動、依頼文の読み取り、TUI 用パラメータ解決、完全 prompt の保存、Codex TUI 起動までを扱う。
- TUI 起動時の AgentCallParameter 構築、TUI で許容する file access mode の検証、Markdown 依頼文の見出し構造化、解決済み JSON からの値取り出しを担う。

## Read this when
- `cmoc tui` の起動手順、依頼文編集から Codex TUI 実行までの制御フローを確認・変更したいとき。
- TUI 実行時に作成される元 prompt と完全 prompt の保存場所・命名・読み取り処理を確認したいとき。
- TUI で利用するエディタ選択、エディタ異常終了時のエラー、利用可能な editor command の優先順を確認・変更したいとき。
- TUI 用の file access mode 制限、解決済みパラメータから AgentCallParameter を作る処理、complete prompt に含める標準指示フラグの扱いを確認したいとき。
- Markdown の見出しと fenced code block を考慮して、利用者 prompt を StructDoc 階層へ変換する挙動を確認・変更したいとき。

## Do not read this when
- TUI 以外のサブコマンドの CLI 制御や実行フローを調べたいだけのとき。
- Codex CLI/TUI の実際の外部プロセス実行、config 読み込み、repository root や work root の解決など、runtime 共通処理を調べたいとき。
- TUI パラメータ解決用の prompt/schema そのものや、許容される file access mode の定義元を調べたいとき。
- complete prompt 全体の組み立て規則や StructDoc の markdown 描画規則を調べたいとき。
- indexing preflight の詳細な条件や、INDEX 生成・更新の実装を調べたいとき。

## hash
- 10df8d618f0de7d5b9f8e1b914e10a117d9388932d95cedb196ef89fd330681b
