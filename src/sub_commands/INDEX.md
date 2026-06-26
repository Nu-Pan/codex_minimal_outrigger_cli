# `apply`

## Summary
- apply 系サブコマンドの実行ロジックをまとめる領域。apply run の開始、隔離 worktree 上での Codex apply loop、完了・エラー後の session branch への取り込み、未 join run の破棄、実行中 process の管理、fork/join report 生成を扱う。
- session branch、apply branch、apply worktree、session state、process id file、git merge・branch・worktree 操作をまたいで apply のライフサイクルを追うための入口になる。
- 主要な関心は、apply fork による finding 列挙と適用、apply join による成果取り込み、apply abandon による破棄、実行時補助処理、レポート生成に分かれている。

## Read this when
- apply fork、apply join、apply abandon の実行条件、状態遷移、CLI 出力、終了コード、失敗時の扱いを調べたいとき。
- apply run が session state の ready、running、completed、error をどのタイミングで更新し、apply branch や apply worktree をどのように作成・削除するかを確認したいとき。
- Codex を使った finding 列挙、finding 適用、commit subject 生成、差分要約生成の呼び出し順や、scope ごとの対象 file 選定を追いたいとき。
- apply 中に oracle、memo、.agents、INDEX.md、git ignored file などがどのように対象外・許可・ロールバック・自動解決されるかを確認したいとき。
- apply process id file、pidfd、process start time、SIGTERM/SIGKILL など、running apply run の安全な停止や stale pid 判定を調べたいとき。
- apply fork report や apply join report の保存、frontmatter、結果表示、finding count、変更要約、merge conflict・想定外差分の記録を確認または変更したいとき。

## Do not read this when
- apply 以外のサブコマンド、session 作成、設定読み込み、汎用 git wrapper、worktree 作成・削除 helper、state file schema 全体などの共通 runtime 実装だけを調べたいとき。
- Codex に渡すプロンプトや構造化出力パラメータの本文だけを確認したいときは、ACP parameter builder 側を直接読む。
- 生成済み report の内容を読むだけで、report 生成ロジックや fallback 挙動を変更しないとき。
- INDEX.md エントリー生成規則、oracle file と realization file の一般方針、ルーティング文書全体の仕様を確認したいとき。
- 単に apply 実装パッケージの docstring だけを確認したい場合を除き、パッケージ初期化処理や再 export の調査目的で深い実行ロジックを読む必要がないとき。

## hash
- c56096d50da06ca5c1c61af64cd1da8bb7a8d04524c1a970739a126b68aa88be

# `indexing.py`

## Summary
- INDEX.md の自動メンテナンスを担う subcommand 実装で、work root 配下の対象を走査し、既存 entry の hash 再利用、Codex による entry 生成、Markdown 描画、更新差分の commit までを制御する。
- Codex 呼び出し前の indexing preflight 登録と実行、CLI 実行時の clean worktree などの前提条件検査、repository 単位の排他 lock による直列化を扱う。
- indexable な directory・child の選別、memo・git ignored・binary の除外、対象内容と鮮度判定 hash の計算、Structured Output の検証をまとめて実装している。

## Read this when
- INDEX.md の生成・更新・commit がどの順序で行われるかを確認または変更したいとき。
- indexing subcommand、Codex preflight、排他 lock、clean worktree 前提条件の挙動を調査・修正するとき。
- INDEX.md entry の再生成判定、hash 抽出、対象ファイル・ディレクトリの走査除外条件、Structured Output からの Markdown 変換に関わる実装を扱うとき。

## Do not read this when
- 個別の INDEX.md entry 文面そのものや、各 directory のルーティング内容だけを確認したいとき。
- Codex CLI 呼び出しパラメータの詳細な組み立てだけを調べたいときは、その builder 側を直接読む。
- git コマンド実行、設定読み込み、path model、binary 判定、ignore 判定などの共通 runtime helper の内部実装を調べたいときは、それぞれの定義元を読む。

## hash
- f198b74f77eba78abea39b281408b2a92d8c8fe51cb93cbe9cef7297c734e256

# `init.py`

## Summary
- work root を cmoc 管理の初期状態へ同期する init サブコマンドの実装。`.cmoc` ignore と設定同期を行い、必要なら初期化コミットを作成しつつ、実行前の利用者の staged 差分と `.gitignore` の worktree/index 状態を復元する。
- CLI ランタイム経由で `cmoc init` を実行する入口、ログ作成前に `.cmoc` ignore を保証する前処理、git blob/index 操作を含む復元 helper、成功時の Markdown 出力生成をまとめて扱う。

## Read this when
- `cmoc init` の挙動、初期化コミット作成条件、`.cmoc` ignore の追加、設定同期、成功時 stdout の内容を確認・変更したいとき。
- init 実行前に staged だった利用者差分を初期化コミットへ混ぜない制御や、実行後に staged patch を復元する処理を調べるとき。
- `.gitignore` の HEAD/index/worktree 状態を一時的に退避し、cmoc ignore pattern を含めて復元する処理を確認・修正するとき。
- サブコマンドを共通 CLI ランタイムへ渡す実装や、init 専用の pre-log check の副作用管理を確認するとき。

## Do not read this when
- init 以外のサブコマンドの引数、出力、実行フローを調べたいとき。
- `.cmoc` ignore pattern の具体的な生成規則、work root/repo root の解決規則、設定同期の中身そのものを調べたいとき。
- git コマンド実行 wrapper や CLI ランタイム wrapper の汎用的な仕様を調べたいとき。
- init の外部挙動をテストで確認したいだけで、実装内部の状態退避・復元ロジックを読む必要がないとき。

## hash
- 586b69dd9d3a71e00758c605c7b1ff18bc05ba64f59e49ebe4e1c10f0ea21598

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
- session 系サブコマンド群の実装をまとめるディレクトリで、session branch の作成、home branch への取り込み、merge しない破棄といった利用者操作の入口を担う。
- 各モジュールは共通の runtime 実行ラッパーへ処理を渡しつつ、session state、git branch、worktree 条件、利用者向け出力や失敗時の回復処理をそれぞれのコマンド単位で扱う。

## Read this when
- session 系サブコマンドのどの実装へ進むべきかを選びたいとき。
- session branch の作成、join、abandon に関する CLI 入口、実行前条件、state 遷移、branch 操作、エラー時の扱いを調べたいとき。
- session 操作が runtime の共通サブコマンド実行基盤、git helper、state 管理とどう接続されるかを確認したいとき。

## Do not read this when
- CLI 全体のコマンド登録、runtime 共通処理、git helper、path model、state file schema そのものを調べたいとき。
- session 以外のサブコマンドや、oracle と realization の一般仕様を調べたいとき。
- 個別コマンドの詳細だけが必要で、読む対象が fork、join、abandon のいずれかに既に決まっているとき。

## hash
- 98b8ab5fa2306838b7e40aa53fa2e71de5c4bdc8a55f1e176717a8ccd483e677

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
