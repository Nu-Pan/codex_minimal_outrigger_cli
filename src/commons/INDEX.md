# `__init__.py`

## Summary
- cmoc 共通 runtime helper を提供する commons パッケージの初期化ファイル。commons 配下の共通実行時補助機能を確認・変更するときの入口。

## Read this when
- 共通 runtime helper の提供箇所や commons パッケージの初期化を確認するとき
- commons 配下の機能を利用・変更する前にパッケージの入口を確認するとき

## Do not read this when
- 特定の runtime helper の実装詳細を確認したいとき
- commons 配下に対象となる個別実装ファイルがある場合

## hash
- 8b50d22749d6fd880d430c393e14c6dcb919038e7b9c7ec76288c523c3d58b34

# `cmoc_runtime.py`

## Summary
- cmoc の実行時機能を横断して公開する共通 API 集約モジュール。CLI 実行、Codex プロセス制御、設定・状態・パス管理、Git 操作、ログ、結果型、エラー処理などの runtime 部品を再エクスポートし、上位実装からの共通入口を提供する。

## Read this when
- cmoc runtime の共通 API、公開シンボル、または複数の runtime サブモジュールを横断する依存関係を確認するとき
- CLI サブコマンドやセッション・worktree・設定・状態処理が、共通 runtime API を通じてどの機能に依存するか調査するとき

## Do not read this when
- 特定の runtime 機能の実装詳細だけを調査・変更するときは、対応する runtime_* モジュールを直接読む
- Codex の preflight、Git、設定、状態、パスなど単一領域の挙動だけを確認する場合

## hash
- 7ca0f0765cda341c73ce13d5f085c20c8907c7c64ad270a4ec1f2fe389c7a83f

# `indexing.py`

## Summary
- INDEX.md の検査・生成・更新・commit までを担う indexing lifecycle の共通実装。対象ディレクトリの列挙、既存 entry の hash による再利用、Codex による不足 entry の生成、Markdown 検証・書き込み、更新差分の commit、排他制御を扱う。

## Read this when
- INDEX.md の自動生成・鮮度判定・entry 再利用・Structured Output 検証を変更または調査するとき
- indexing の対象除外、hash 計算、symlink・binary・Git ignore の扱いを確認するとき
- Codex 呼び出しの並列実行、preflight、lock、worktree・ログ保存先の制約を確認するとき
- INDEX.md 更新の commit や Git failure の処理を変更または調査するとき

## Do not read this when
- INDEX.md entry の文章内容そのものを作成・修正するときは、対象ファイルの本文と entry 生成用の oracle を直接読む
- indexing 以外の CLI 機能、Codex 実行一般、Git 共通処理だけを調査するときは、それぞれの専用実装を読む
- INDEX.md の正本仕様や entry schema の定義を確認するときは、この実装ではなく対応する oracle file を読む

## hash
- 3a12bb8da2be10b857727872e4a63a8e7a443059cb0175388a08707a080ca3ab

# `prompt_editor_input.py`

## Summary
- エディタから AI Agent 用プロンプトを受け取り、初期テンプレートの保存、エディタ選択・起動、入力内容のコメント除去と読み込みを担う共通境界。
- エディタ入力用ディレクトリの作成や一意なタイムスタンプ付きファイルの予約、エディタ終了エラーの cmoc 利用者向け例外への変換、現在の worktree と対象 root の `.cmoc` ignore 保証も扱う。
- プロンプト編集フロー、エディタ選択順、編集ファイルの読み込み・コメント除去、または prompt editor 用 root の ignore 設定を変更・調査するときの実装入口。

## Read this when
- prompt editor または TUI の入力保存・編集フローを調査するとき。
- 利用可能なエディタの選択順、起動引数、終了失敗時のエラー処理を変更するとき。
- HTML コメントを除去したプロンプト入力の読み込みや、編集用ファイルの timestamp 衝突回避を調査するとき。
- editor/TUI が利用する `.cmoc` ignore の保証処理を変更するとき。

## Do not read this when
- プロンプト本文の正本テンプレートや利用者向け仕様を確認することが目的の場合は、対応する oracle doc を直接読む。
- prompt editor 入力を利用した後続の agent 呼び出し、CLI 実行、runtime path・git の詳細を調査する場合は、それぞれの呼び出し元または専用 runtime モジュールを直接読む。
- 一般的なエディタ設定や prompt の内容編集だけが目的で、入力境界の実装を変更しない場合。

## hash
- 5e7022e4bf219323a09a46511b3e637d461996a044331792505fabfcad318d99

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを管理するモジュール。work root 検査、doctor preprocess、サブコマンドログ、step 通知、完了サマリー、戻り値と例外のエラー処理を一元化する。

## Read this when
- CLI サブコマンドの共通実行経路、ログ記録、step 通知、完了表示、終了コード化、例外表示を変更・調査するとき
- サブコマンド実行前の work root 検査や doctor preprocess の適用範囲を確認するとき

## Do not read this when
- 特定サブコマンド固有の処理、doctor preprocess の修復内容、ログの保存形式自体を変更・調査するときは、それぞれの実装モジュールや対応する oracle を先に読む

## hash
- 32db723142717e6b038a1ae8c3fba66bc7e23e144d95477b0dd2638a40440e4c

# `runtime_codex.py`

## Summary
- Codex 実行処理と TUI 実行処理を外部から利用するための公開入口。各処理の具体的な実装は下位モジュールに委譲する。

## Read this when
- Codex の実行 API の公開入口や、exec/TUI 両方の実行関数を利用する箇所を確認するとき。

## Do not read this when
- Codex exec の具体的な挙動だけを調査するときは exec 実装へ、TUI の具体的な挙動だけを調査するときは TUI 実装へ直接進む場合。

## hash
- 102a2c0a12a693cfc7a6292ea3353fcaf61c1d963a5449f5d577b476f5614756

# `runtime_codex_exec.py`

## Summary
- Codex exec の単一試行ループを実行制御する中核モジュール。Structured Output の厳格な JSON/schema 検証、capacity retry、quota 回復待機と代表 probe、resume token による継続、Codex subprocess の起動、prompt・stdout・stderr・output・call log の保存、console/subcommand event の記録、最終的な CodexExecResult の組み立てを一つの状態機械として扱う。

## Read this when
- Codex exec の実行、再試行、quota/capacity エラー処理、resume 継続の挙動を変更・調査するとき
- Structured Output の検証失敗、Codex subprocess の preflight、実行ログや subcommand event の記録を確認するとき
- quota availability probe、共有 polling 状態、retry counter、待機時間の連携を理解する必要があるとき

## Do not read this when
- TUI 起動処理だけを変更・調査するとき
- Codex のログ出力フォーマット単体や profile/path helper 単体の実装を確認するときは、対応する runtime helper module を直接読む
- Codex exec と無関係な CLI サブコマンドや設定処理を変更するとき

## hash
- 36f0b51e816d0d9a9194ac7ed61c2e3060e1901a66831eb89e70865e10ecdf18

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しの利用者向け console 通知と、起動失敗時の共通エラー文字列変換を担当する。呼び出し目的・ログパス・経過時間・終了状態・エラーを整形して出力する処理の入口。

## Read this when
- Codex CLI 呼び出し結果の console 表示、stderr/stdout の振り分け、起動失敗エラーの整形を変更・確認するとき。

## Do not read this when
- Codex CLI の実行そのもの、呼び出しログの保存形式、時間やパスの共通フォーマットを変更するときは、実行側または対応する共通 runtime モジュールを直接確認する。

## hash
- 75c1cb639881681a4ab4ec39887e5e1e5900864477aa2d445b30df9ed478b7a1

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行前に INDEX 更新 preflight を挟むランタイム連携を担当する。preflight の登録・解除、再入抑止と直列実行、実行対象からの indexing 起点 root 算出、実行本体への委譲を扱う。

## Read this when
- Codex exec または TUI の起動前処理、INDEX 更新 preflight、preflight の有効化・無効化を変更するとき。
- Codex 呼び出し設定から作業 root を決める処理や、preflight の再入・並列実行制御を確認するとき。

## Do not read this when
- Codex 実行本体の subprocess・TUI 実装を変更または調査するときは、runtime_codex の実装を直接読む。
- INDEX の生成規則や oracle 編集サブコマンド固有の仕様を確認するときは、対応する oracle 文書を直接読む。

## hash
- 9a17bb577fe0ed64e036ca1f99b85af81357514dd6f87db9bde3a1d7bbe25e19

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界を担当し、起動前の sandbox・cwd・CODEX_HOME・argv・schema 配置と、実行中の process tracking・group 停止を扱う。
- Codex CLI の JSONL 出力、resume token、capacity/quota/予期しない error の機械的判定を提供する。

## Read this when
- Codex CLI の起動引数、環境変数、作業ディレクトリ、Structured Output schema 配置を変更・調査するとき
- Codex subprocess の process tracking、pidfd、process group 停止、abandon 処理を変更・調査するとき
- Codex の JSONL 出力解析、error 判定、quota retry 判定を変更・調査するとき

## Do not read this when
- Codex CLI 境界以外の設定値検証や path 操作だけを変更するときは、該当する runtime helper を直接読む
- Codex subprocess の呼び出し元の業務フローや編集 run 全体の仕様を確認したいときは、対応する上位の command 実装・仕様を先に読む

## hash
- 6f44989fdb06dc1a10665bb7e69ab37cc44b46debc45a95f8fdd4921494b244d

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを担当する実装。設定上書き argv、作業ディレクトリ、Codex HOME の検証、呼び出しログ、コンソール・イベントログ、成功・失敗時の戻り値や例外処理をまとめて扱う。Codex CLI/TUI の起動経路や実行ログ、失敗処理を確認する際の入口。

## Read this when
- Codex TUI の起動方法、argv や実行環境の準備を変更・調査するとき
- Codex 呼び出しの call log、イベントログ、実行時間、戻り値、例外処理を変更・調査するとき
- Codex の作業ディレクトリや CODEX_HOME の解決・検証を確認するとき

## Do not read this when
- Codex の設定値そのものを変更・調査するときは設定ロード・構成定義側を読む
- Codex の非対話実行やプロファイル解決の内部仕様だけを調査するときは、対応する runtime モジュールを直接読む
- 一般的な CLI ロギングやパス操作だけを調査するときは、各責務を実装する専用モジュールを直接読む

## hash
- d993891d52da34ab34c73d79c78451be3d6dc6a3ff3099fc404558d61b75bf65

# `runtime_config.py`

## Summary
- cmoc の設定値を、正本の設定型と JSON 永続化形式の間で変換・検証するランタイム設定モジュール。model provider、model、reasoning effort、各種 int 値の型・値検証、既定値補完、不正設定の CmocError 化を扱う。
- 設定 JSON の安全な読み書きを担当し、symlink 経由のアクセス、特殊ファイル、不正 JSON、欠落ファイルを拒否する。config の生成・読み込み・書き戻し処理への入口となる。

## Read this when
- cmoc config の JSON 永続化形式、設定値の検証、既定値補完、不正設定時のエラー境界を変更または調査するとき
- config path の symlink・特殊ファイル対策や、設定ファイルの生成・読み込み・同期処理を確認するとき

## Do not read this when
- Codex の設定型そのものや既定値を変更する場合は、先に設定型を定義するモジュールを読むとよい
- CLI コマンドの引数定義や、設定 path の算出だけを確認する場合は、対応するコマンド・path モジュールを直接読むとよい

## hash
- 3777f708f12dc5b235bc71cbd925805374428c5b124a790ad2be309efec24709

# `runtime_content.py`

## Summary
- ファイル内容の SHA-256 ハッシュ計算、UTF-8 文字列のハッシュ計算、内容ハッシュを含む一時ファイルの安全な保存、バイナリ判定を提供する共通ランタイム処理。symlink や dangling symlink、既存ファイルとの整合性、原子的な置換を扱う。

## Read this when
- ファイル分類や状態同期で、通常ファイルと symlink のハッシュ方法を確認するとき
- 内容ハッシュ付きファイルの生成・再利用・原子的な保存処理を変更するとき
- ファイルのバイナリ判定ロジックを変更または利用するとき

## Do not read this when
- 特定のプロンプト生成処理や oracle/realization の仕様を確認したいとき
- この共通ランタイム処理を利用する上位機能の挙動だけを調査するとき

## hash
- ddf0f66390f4aaf71281fa12bd36f060b80ff0d272148ee758ccd73e2714c1c6

# `runtime_doctor.py`

## Summary
- doctor preprocess の排他ロック、修復対象の同期、Git index の退避・一時 index 合成・復元、修復 commit を一つの lifecycle として実装するモジュール。`.gitignore`、`.agents/.gitkeep`、config、refactor state の修復と、修復後の追跡状態検証を扱う。

## Read this when
- doctor preprocess の修復処理、Git common directory 単位の排他制御、修復 commit、または現在の index の保存・復元を調査・変更するとき
- `.gitignore` や `.agents/.gitkeep` の doctor 修復、config/refactor state の同期、修復差分と利用者の staged 状態の分離を確認するとき
- doctor 実行時の失敗処理、一時 index、Git index の不変条件、tracked runtime file の検証を確認するとき

## Do not read this when
- 通常の Git 操作、doctor 以外の CLI 処理、config や refactor state の同期実装そのものだけを調査するとき
- runtime のパス・Git 共通 helper・エラー型の定義を直接確認する必要があるときは、それぞれの専用モジュールを先に読む

## hash
- 12ecb44653b8c3df1995c37c68a8554114c9f66fb410588ed2b61e48ec82bdaf

# `runtime_errors.py`

## Summary
- cmoc の実行時エラーを共通 Markdown レポートへ変換する実装。
- CmocError にエラー概要・復旧案・詳細を保持させ、通常例外には既定の案内を適用する。
- Next actions を最低 2 件に補完し、Summary、Detail、Call stack を含む利用者向けエラー出力を組み立てる。

## Read this when
- cmoc の実行時例外、利用者向けエラーレポート、復旧案、スタックトレースの出力を確認・変更するとき。

## Do not read this when
- 特定のサブコマンド固有のエラー発生条件や、エラー原因となる個別機能の実装だけを調査するとき。

## hash
- 19293509934218345593f574c4afed40ab4c72ae4d921b9864a95b3fa9f8cf66

# `runtime_git.py`

## Summary
- Git コマンド実行、branch・commit・status、linked worktree の作成・削除・安全性検証を担う共通境界。Git ignore 状態の更新・検査と、oracle/realization file の path 分類も扱い、これらの責務を利用する実装やテストの入口となる。

## Read this when
- Git の branch、worktree、HEAD、未コミット差分を扱う処理を変更・調査するとき
- cmoc 管理領域の worktree 作成・削除や symlink 安全性を確認するとき
- `.cmoc/gu` の ignore 設定、Git exclude、ignore 判定を変更・調査するとき
- oracle file または realization file の分類条件を変更・調査するとき

## Do not read this when
- 特定の CLI サブコマンドの業務フローだけを変更・調査し、Git 境界や path 分類の挙動に関係しないとき
- runtime error、path、result の型や実装を直接確認する必要があるときは、それぞれの担当モジュールを先に読む

## hash
- 9b00658a0ba279f52c90c2c4619df201f91921e3f9860a364f39a0b0f5f60969

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines ログ記録と実行時間集計を担う runtime logging モジュール。イベント追記、step timing、quota 待機時間、ContextVar 経由の logger 参照を提供する。

## Read this when
- サブコマンドのログイベント形式、step の開始・完了計測、経過時間や quota 待機時間の集計を変更・調査するとき
- runtime helper から現在のサブコマンド logger を取得・設定・復元する処理を確認するとき
- ログファイルの生成先や一意な timestamped path の確保と、この logger の連携を確認するとき

## Do not read this when
- CLI サブコマンド固有の処理や console 出力の表示仕様だけを調査するときは、該当する command 実装または console 関連モジュールを直接読む
- runtime path の一般的な定義やログディレクトリの構成だけを調査するときは、runtime_paths モジュールと対応する oracle 文書を直接読む

## hash
- 37a9742cfd233aebdde8d02ae426db9eb479df2f0e94238fee7aae903baa44eb

# `runtime_paths.py`

## Summary
- リポジトリ・worktree・cmoc root の解決、実行時 timestamp と duration の整形、session/report/log/schema/config などの標準保存先の算出を提供する runtime path ユーティリティ。cwd を一時変更する処理は process-wide lock と ContextVar で直列化する。

## Read this when
- root path の解決、cmoc 管理ディレクトリや各種ログ・レポート保存先の扱いを変更または調査するとき
- timestamp、duration 表示、timestamp 付き path の排他的予約、cwd 切替の挙動を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容、ログ出力形式、設定スキーマそのものを確認したいとき
- path 解決の基盤実装や root placeholder の定義を確認したいときは、path model 側を直接読む

## hash
- a6083e682746a50b8a97e22b8003317e0fd2b04e7074f12e33e8f228b944ceaa

# `runtime_refactor.py`

## Summary
- oracle/realization file の調査履歴を管理する state の読み込み・検証・保存・同期を担当する。対象 file の列挙、未調査対象の選択、調査要否の更新、path・entry・日時・SHA256 の schema 検証、および不正 state の利用者向け例外変換を含む。

## Read this when
- realization refactor の調査対象選択、調査履歴の同期・更新、state file の読み書きや schema 検証を変更・確認するとき。
- oracle file と realization file の列挙条件や、調査履歴の妥当性検証を確認するとき。

## Do not read this when
- CLI の個別サブコマンド処理、一般的な runtime helper、refactor state の仕様そのものを確認したいとき。後者は対応する oracle document を直接読む。

## hash
- 0dc268da40f4c5d47ff20fe8e687d82a25f89103fd82551ce70e5174536860ed

# `runtime_results.py`

## Summary
- Codex exec の構造化出力契約、外部コマンド結果、および exec 実行に伴う生成物・ログ・設定パスを表す型を定義する。runtime 結果の型や呼び出し側契約を確認する必要がある場合の入口となる。

## Read this when
- Codex exec の戻り値契約や構造化出力へのアクセス方法を変更・確認するとき
- 外部コマンドの終了コード、標準入出力、実行ログや生成物のパスを保持する結果型を利用するとき

## Do not read this when
- Codex exec の実行処理そのものを変更・確認するとき
- CLI 入出力やログ保存処理の具体的な挙動だけを調べるとき

## hash
- 9f6e365d5335be51796785b3abc187d63c1d32111ecb9b0ad30308780df063e4

# `runtime_run.py`

## Summary
- 編集 run の worktree 解決、プロセス識別情報の記録・検証、Codex 子プロセス群の追跡・停止、tracking file の cleanup を担う共通ランタイムモジュール。editing run の abandon/error cleanup と process isolation の実装を確認する入口。

## Read this when
- editing run の abandon、error cleanup、run process tracking、Codex subprocess の停止処理を変更・調査するとき
- PID 再利用や process group の同一性検証、tracking file の破損・stale 状態の扱いを確認するとき
- branch から worktree を解決する処理や managed run worktree の安全性を確認するとき

## Do not read this when
- 通常の run 実行フローや CLI 引数の仕様だけを確認したいときは、editing run の上位実装・oracle doc を先に読む
- 一般的な git 操作、path 生成、エラー型の定義を変更・調査するときは、それぞれの専用 runtime module を直接読む
- Codex subprocess の起動方法や環境設定だけを確認したいときは、process profile 側の実装を直接読む

## hash
- 8175f6fc7e8fc2fc6804b29bcd2681963c14a7ccbac16f714f7b9e3790d882ea

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始から state 遷移、commit、差分分類、INDEX 更新、cleanup 判定までを担う共通 lifecycle 実装。EditingRunContext と lifecycle lock を共有し、session/run の branch・worktree・state の不変条件を管理する各処理への入口。

## Read this when
- editing run の開始、active run の解決・復旧、joinable/error state への遷移を変更または調査するとき
- worktree 差分の commit、rollback、INDEX 更新、agent/run/session の許可 path 判定を変更または調査するとき
- run branch・session branch・state file・managed worktree の整合性や cleanup 処理を確認するとき

## Do not read this when
- 単一の git 操作、path 判定、state model、INDEX 更新処理の詳細だけを確認したいときは、対応する runtime・indexing module を直接読む
- editing run の利用者向け仕様や状態遷移の正本を確認したいときは、対応する oracle document を直接読む

## hash
- 69d910c7db522a9fe1c5847164720a31f4be0b88230d905aa79763e905ec786e

# `runtime_run_report.py`

## Summary
- editing run の fork report と lifecycle report を生成・保存する共通処理。YAML Front Matter、完了情報、変更パス、警告、実行状態を組み立て、timestamp 付きで衝突を避けて Markdown レポートを書き込む。YAML scalar と変更パスの安全な Markdown 表現も提供する。

## Read this when
- fork 実行または run の join/abandon に関するレポート生成・保存処理を変更するとき
- report の Front Matter 項目、完了情報、警告、変更パスの出力形式を確認するとき
- timestamp 付き report path の予約や Markdown/YAML エスケープ処理を調査するとき

## Do not read this when
- editing run の状態遷移や report の仕様そのものを確認したいときは、参照先の oracle 文書を直接読む
- runtime path の生成規則や EditingRunContext の定義だけを確認したいときは、それぞれの専用モジュールを直接読む

## hash
- 3c246b8c9e973646b9b6e7027e9dc6fc069f16a3a44ec8682bea1fb961a7711b

# `runtime_state.py`

## Summary
- cmoc の session state を JSON として復元・検証・保存する共通ランタイム実装。session/run の状態 schema、branch からの session-id 解決、state file の読み書き、symlink 防止、session fork 排他 lock を扱う。session や run の永続状態管理・検証処理の入口として読む。

## Read this when
- session state の schema、状態値、不変条件、JSON の読み書きや検証を変更・調査するとき
- cmoc 管理 branch から session-id や state file を解決する処理を変更・調査するとき
- session fork の排他 lock、symlink 経由アクセス拒否、永続 state のエラー変換を確認するとき

## Do not read this when
- CLI サブコマンド固有の session/run 操作や branch lifecycle の仕様を確認したいときは、対応する oracle doc または上位の実装を直接読む
- 一般的な git 操作、path 解決、CmocError の定義だけを調査するとき

## hash
- c4f029a798d0645fe8272ee93a2a93ed2aa2b6315239d9112c91e1f168505e9b
