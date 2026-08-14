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
- cmoc のランタイム共通公開 API を集約するモジュール。CLI サブコマンド実行、Codex プロセス制御、設定・状態管理、パス解決、Git 操作、ログ、コンテンツハッシュ、エラー処理など、各ランタイム機能から再利用される関数・定数・型を公開する。個別機能の実装ではなく、これらの共通 API の構成や公開名を確認するための入口。

## Read this when
- cmoc ランタイムの共通 API や公開シンボルを確認・変更するとき
- CLI、Codex 実行、設定、状態、Git、ログ、パスなど複数のランタイム機能を横断して依存関係を調査するとき
- 他のモジュールから利用される共通エラー・結果型・状態型の公開元を確認するとき

## Do not read this when
- 特定のランタイム機能の内部実装を変更・調査する場合は、対応する個別 runtime モジュールを直接読むとよい
- CLI の個別サブコマンドの挙動だけを確認する場合
- このモジュールが再公開する機能の具体的なアルゴリズムや仕様を確認する場合

## hash
- d4bdb41ff7df1879f0483a1bb3d9a2c72156a9d3598d0babfbe45b128997574d

# `indexing.py`

## Summary
- INDEX.md の検査・生成・鮮度検証・書き込み・commit まで、リポジトリ内の indexing lifecycle を一貫して実行する共通実装。
- directory traversal、既存 entry の再利用、Codex による不足 entry の生成、hash 検証、symlink・binary・除外対象の扱い、排他 lock と Git commit を扱う。
- INDEX.md 更新処理の preflight や、index 対象の列挙・hash 計算・Structured Output の entry 描画へ進む入口となる。

## Read this when
- INDEX.md の自動更新、entry の再生成、鮮度判定、indexing 用 commit の挙動を変更・調査するとき。
- index 対象の directory traversal、除外規則、symlink・binary の扱い、hash の算出方法を確認するとき。
- Codex 呼び出しを伴う entry 生成、並列実行、排他 lock、Git worktree・ログ root の扱いを確認するとき。

## Do not read this when
- INDEX.md の entry の文章ルールや生成 prompt の仕様だけを確認したいときは、indexing 用の prompt・schema 定義を直接読む。
- 通常の CLI 実行や INDEX.md 更新結果だけを確認し、indexing lifecycle の実装詳細を調べる必要がないとき。
- 個別の runtime helper や Git path 操作の責務だけを確認するときは、対応する helper 実装を直接読む。

## hash
- cce67e25b81ad2f2321d59a3cfa50c5da7c1e76e756a1d174ae0f2753d9d2cab

# `prompt_editor_input.py`

## Summary
- エディタから受け取る利用者プロンプトを、予約した入力ファイルへ保存・読込し、完全な prompt skeleton のプレースホルダーを置換して確定する共通境界。エディタ選択、入力コメント除去、プレースホルダー検証、`.cmoc` ignore 保証も扱う。プロンプト編集フローや editor input の入出力処理を確認するときの入口。

## Read this when
- 利用者プロンプトのエディタ入力、完全 prompt の確定、入力ファイルの予約、利用可能なエディタの選択を変更または調査するとき。
- 入力から HTML コメントや前後空白を除去する処理、prompt skeleton のプレースホルダー検証、エディタ用 `.cmoc` ignore の保証を確認するとき。

## Do not read this when
- prompt skeleton の内容やエディタ入力案内の正本仕様を確認する場合は、prompt builder または対応する oracle 文書を直接読む。
- prompt editor input と無関係なランタイムエラー、Git 操作、パス生成、または一般的な CLI 処理を調査する場合。

## hash
- f3eac66d141d815806253a176c70dd6d9e83e8ecdea2d0ffcf68db71b2021567

# `runtime_cli.py`

## Summary
- 対象ファイルは、CLIサブコマンドに共通する実行ライフサイクルと状態管理を集約する。work root の検査、サブコマンドログ、doctor 前処理、feedback invocation、step 通知、成功・中断・失敗時の終了処理、エラー表示、完了通知を一元的に扱い、個別サブコマンド実装から共通運用を確認する入口となる。
- 中断状態や TUI プロセス起動境界の印付け、step 開始通知、失敗終了処理、完了サマリー生成など、サブコマンド共通 runner の補助 API と内部処理も含む。

## Read this when
- CLIサブコマンドの実行順序、ログ生成、doctor 前処理、feedback lifecycle、step 表示、戻り値・例外の終了処理を確認するとき。
- KeyboardInterrupt、TUI 起動後の終了、Windows terminal result 通知、サブコマンド完了サマリーの挙動を変更または調査するとき。
- 個別サブコマンドが共通 runner の引数や補助関数を利用しており、共通の実行境界を確認する必要があるとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、doctor・feedback・logging など各機能の詳細仕様だけを確認したいときは、それぞれの実装または正本仕様を直接読む。
- CLI共通ライフサイクルやこのファイルが提供する補助 API に関係しない設定、パス処理、通知実装の調査では、該当する対象へ直接進む。

## hash
- 7a4b235c65908724cdfe59780a3318f8aae179b485fd4de3e2831d0249879008

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
- 1 回の agent call における Codex CLI exec の実行制御を担う中核モジュール。prompt・call・stdout/stderr・output のログ保存、Codex subprocess 起動、エラー分類と capacity retry、quota availability probe による待機・resume、Structured Output の JSON parse／schema／事後条件検証と同一 session での補正、作業成果物変更の検出・復元、subcommand event と診断情報の記録を一体的に扱う。TUI 起動など別責務の実装入口ではなく、exec の再試行・検証・実行記録の挙動を確認または変更するときの入口である。

## Read this when
- Codex exec の subprocess 起動条件、argv、cwd、環境変数、prompt stdin、Codex Home、Structured Output schema の扱いを確認するとき
- capacity error の再試行、quota 枯渇時の代表 probe・待機・resume、session ID の継続挙動を調査または変更するとき
- Structured Output の parse／schema／宣言済み事後条件検証、補正 prompt、補正回数上限、補正中の成果物保護を確認するとき
- Codex call の prompt・実行条件・stdout/stderr・output・console／subcommand event の記録や失敗診断を確認するとき

## Do not read this when
- TUI の起動や画面制御そのものを調査するときは、TUI 起動を担う別 module を直接読む
- Codex exec の個別ログ整形、profile 判定、config 読み込み、quota probe parameter の生成など、既に分離された補助機能だけを確認するときは該当する runtime module を直接読む
- 単に Codex の出力 schema の項目や形式を確認するだけのときは、対応する schema 定義を直接読む

## hash
- 0d1578ed5cffacb9d486b35a92516c3268d1435470dabfe488b9c07598eee77c

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
- Codex exec/TUI 呼び出しに対して、実行前の INDEX 更新 preflight、呼び出し境界通知、再入抑止と直列化を提供するランタイム仲介層。preflight の登録・解除と、Codex 設定から作業 root を決める処理を含み、実際の Codex 実行は runtime_codex へ委譲する。Codex 呼び出し前処理や INDEX 更新 preflight の動作を変更・調査する際の実装入口。

## Read this when
- Codex exec または TUI の起動前に indexing preflight を実行する経路を変更するとき
- indexing preflight の登録・解除、再入抑止、スレッド間の直列化を調査するとき
- preflight 実行後に workload 本体へ境界を通知する呼び出し契約を確認するとき

## Do not read this when
- Codex 実行本体の subprocess 処理や結果型の仕様を確認したいときは、委譲先の runtime_codex または runtime_results を直接読む
- AgentCallParameter の定義や agent call のパスモデルを確認したいときは、それぞれの定義元を直接読む
- INDEX 文書の生成規則や preflight の具体的な実装内容を確認したいだけのとき

## hash
- 12d767988ff06e195adb190cfc1ca30c609459ff946465f94ba4704500e131a5

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界の実装を担い、起動前後の実行環境・argv・CODEX_HOME・schema 配置と、実行中 process の tracking/停止・identity 検証を扱う。Codex の JSONL 出力から session ID や error 種別を抽出し、capacity/quota retry 対象と予期しない失敗を判定する下位実装への入口でもある。

## Read this when
- Codex CLI の sandbox、config override、model provider、通知、feedback MCP、環境変数、schema 配置を変更または調査するとき。
- editing run における Codex subprocess の process group tracking、PID reuse 対策、停止・cleanup、signal 処理を確認するとき。
- Codex subprocess の起動失敗、JSONL output、session resume、capacity/quota retry、unexpected error の判定を変更または調査するとき。

## Do not read this when
- Codex CLI 境界の具体的な実装や実行結果の判定を扱わず、呼び出し元の prompt 構築や上位の run 制御だけを確認する場合は、まずそれぞれの直接の実装対象を読む。
- 一般的な runtime 設定値の検証や runtime path の仕様だけを確認する場合は、対応する設定・path 実装へ直接進む。

## hash
- 29fe3b161dca11ec0febe4e361857687b470c2423fb2c72ca40d1d4b5c6d872e

# `runtime_codex_tui.py`

## Summary
- Codex TUI プロセスの起動を担当する実行入口。呼び出しパラメーターと設定から作業ディレクトリ、Codex ホーム、ログ保存先、Windows 通知 callback を準備し、設定上書き付きで Codex CLI/TUI を実行する。
- Codex 呼び出しごとの call log、feedback call、実行時間、終了コード、エラー、subcommand logger へのイベント記録を扱う。Codex CLI/TUI の起動経路や呼び出し結果・ログ連携を変更または確認するときの入口であり、個別の設定解決やログ形式の詳細は参照コメントが示す下位モジュール・仕様文書へ進む。

## Read this when
- Codex TUI の起動、argv・環境変数・作業ディレクトリの準備、設定上書きを調べるとき
- Codex 呼び出しの call log、feedback lifecycle、通知 callback、終了結果や logger event の連携を調べるとき

## Do not read this when
- Codex ホームや Codex subprocess 環境の解決規則だけを確認するときは、runtime_codex_profile と関連仕様を直接読む
- ログディレクトリや timestamped path の生成規則だけを確認するときは、runtime_paths とログ仕様を直接読む
- Codex CLI/TUI 以外のサブコマンド実行や一般的なエラー型の仕様を確認するときは、対応する runtime モジュールを直接読む

## hash
- 0d2b6611877622b0572e061b1d80775ae53c7b34760be2a94098459e9d47a4aa

# `runtime_config.py`

## Summary
- cmoc 設定の JSON 永続化境界を担う。正本設定型と JSON object の相互変換、JSON/TOML 互換値の再帰的な型検証、既定値を補った設定復元、設定ファイルの安全な読み書き、設定同期を扱う。設定値の検証や config ファイル入出力を調べる際の入口であり、個別の設定型定義やパス計算・共通エラー定義そのものの入口ではない。

## Read this when
- 設定 JSON の保存・読み込み・同期の挙動を変更または確認するとき
- Codex の model、model provider、reasoning effort、Oracle Review の反復回数、並列数を JSON へ変換または復元するとき
- JSON/TOML に保存できる値の型制約、循環コンテナ、深いネスト、Unicode surrogate、NaN・Infinity、64-bit 範囲外整数の扱いを確認するとき
- 設定ファイルの symlink、非通常ファイル、欠落、JSON 構文エラーに対する拒否と利用者向けエラー境界を確認するとき

## Do not read this when
- 設定項目の正本型、既定値、enum の定義だけを確認したいとき
- 設定ファイルのパス計算だけを確認したいときは runtime_paths を直接読むとき
- 共通の実行時エラー表現だけを確認したいときは runtime_errors を直接読むとき

## hash
- 2303cfb43d52881e01e9a7573d905cf78aef084eb56b600ec84472aafa9c4612

# `runtime_content.py`

## Summary
- ファイル内容の SHA-256 ハッシュ計算、UTF-8 文字列の SHA-256 計算、内容ハッシュを名前に含むファイルの安全な保存、NUL バイトと読み取り可否による粗いバイナリ判定を提供する共通ランタイム処理。状態同期対象の regular file、symlink、ハッシュ付き schema store の保存処理など、ファイル内容と一時ファイル置換を扱う実装へ進む入口。

## Read this when
- ファイルや文字列の SHA-256 値を算出する処理を確認・変更するとき。
- 内容ハッシュを使った出力ファイルの生成、既存同一内容ファイルの再利用、一時ファイルからの置換処理を確認するとき。
- ファイルをバイナリとして粗く判定する処理を確認するとき。

## Do not read this when
- 同期対象の列挙規則や上位のアプリケーション仕様を確認したい場合は、参照されている oracle 仕様を直接読む。
- この共通処理を利用する個別 caller の挙動だけを確認したい場合は、caller の実装やテストを直接読む。

## hash
- 3b078af87a040009e5f907b968ec8dd5717a28db9647f5ea77fc1fe87b7709e4

# `runtime_doctor.py`

## Summary
- doctor preprocess の修復処理と commit lifecycle を担う実装。Git common directory 単位の排他、修復対象の同期、元の index の退避・復元、修復差分だけの commit、runtime state の追跡確認までを一つの lifecycle として扱う。
- doctor の同時実行、修復による .gitignore・.agents・config・refactor state の更新、または staged 状態や unstaged hunk を保った index 復元を調査・変更するときの入口。

## Read this when
- doctor preprocess の lock、修復対象、修復 commit、index の退避・合成・復元の挙動を確認するとき
- doctor が .gitignore、.agents、config、refactor state を修復・同期する経路を調査するとき
- 一時 Git index、HEAD 起点の repair commit、利用者の staged 状態の分離を変更・検証するとき

## Do not read this when
- doctor preprocess 以外の一般的な Git 操作や runtime 設定の内容だけを確認するときは、対応する runtime_git または runtime_config の実装を直接読む
- doctor の利用者向け仕様や CLI からの呼び出し条件だけを確認するときは、対応する app specification や呼び出し側を先に読む
- refactor state の同期規則そのものだけを確認するときは、runtime_refactor の実装を直接読む

## hash
- f7f3dc1e4bd88e1c3f4fd108b53c430f1f6ce250e4722ceb63a3a431f3208826

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

# `runtime_feedback.py`

## Summary
- サブコマンド invocation 単位の feedback collector lifecycle を担う中核モジュール。Codex call ごとの capability 発行、agent observation の IPC 受付・検証・保存、call 終了時の drain、degraded event の記録、allowlist 済み event の machine observation 化をまとめて扱う。feedback reporter、collector、detector の挙動や invocation-scoped な非致命エラー境界を確認する入口。

## Read this when
- feedback observation の受付、保存、rate limit、capability、protocol、または context 検証を変更・調査するとき
- Codex call の reporter 環境継承、call 終了時の drain、並行 request 処理、collector の起動・停止を確認するとき
- reporter/collector 利用不能 event や Structured Output validation exhausted event の検出・保存経路を確認するとき
- feedback reporter の doctor 検査や MCP interface compatibility を変更・調査するとき

## Do not read this when
- feedback observation の永続化形式、RFC3339・ID 生成、または保存先の詳細だけを確認する場合は runtime feedback store を直接読む
- reporter MCP process の公開 tool 実装だけを確認する場合は runtime feedback reporter を直接読む
- 一般的な invocation logging、Git context 取得、または runtime state の仕様だけを確認する場合は対応する runtime module や oracle specification を直接読む

## hash
- a9f9fcc3b402f3de63397e933192ed895f4a6860fb68e3aa0a565d15f9473021

# `runtime_feedback_reporter.py`

## Summary
- Codex起動時のcall-scoped stdio MCP feedback reporterを実装するモジュール。collectorとのUnixソケット通信、capability envelope付きpayload転送、collector結果の検証、MCP JSON-RPCのinitialize・ping・tools/list・tools/call処理を担う。
- 人間対応が必要なobservationをsubmit_observationツールとして公開するfeedback機能の実行入口であり、MCP reporterの通信契約や失敗時のdomain resultを確認する必要がある場合に読む。

## Read this when
- feedback observationのMCP送信処理、collectorとの接続、プロトコル検証、再試行可能な拒否結果の扱いを変更または調査するとき
- submit_observationのMCPツール公開内容やJSON-RPCメッセージ処理を確認するとき
- reporterとcollector間の環境変数、Unixソケット、レスポンス検証の連携を確認するとき

## Do not read this when
- observationの保存形式や入力スキーマの詳細だけを確認するときは、runtime_feedback_storeの定義を直接読む
- feedback機能の仕様全体や利用条件を確認するときは、対応するfeedback observationのoracle仕様を直接読む
- feedbackと無関係なMCPサーバー、CLI処理、または他のruntime機能を調査するとき

## hash
- 21e09ad163751f78770bbfbc9b3559d50a3a50ad1b4ca30f5a35b618b553d812

# `runtime_feedback_state.py`

## Summary
- feedback の repository-local state を一元管理する実装。report cut、active generation、current pointer、issue／machine aggregate、checkpoint、publication、incomplete 診断、cleanup、discard、排他 writer lock の整合性を検証し、atomic／immutable artifact の保存・切替・復旧を担う。feedback state transition や active state integrity の実装を追う際の中心的な入口。

## Read this when
- feedback report の report cut 作成・再開・publication・cleanup・discard の状態遷移を確認するとき
- current pointer、generation manifest、active issue／machine aggregate、Markdown report、checkpoint の相互参照と SHA256 検証を調べるとき
- observation envelope、machine rule の allowlist、canonical identity、incomplete 診断、異常終了後の checkpoint recovery を確認するとき

## Do not read this when
- observation の収集・保存処理や低レベルの JSON／ID ユーティリティだけを確認するとき
- report の集約・正規化・検証ロジック、CLI の引数処理、Markdown report の内容生成が主題のとき
- feedback の正本仕様や利用者向けコマンド契約そのものを確認するとき

## hash
- 44a0d20282cf5752afb702a2fafb2cbb6d46d11a97ac91391ee397a2a5fe86fd

# `runtime_feedback_store.py`

## Summary
- agent および machine rule の feedback raw observation を検査し、secret masking、repository 内 evidence path の正規化、fingerprint 付与、content hash に基づく重複排除を行って immutable durable store へ保存する実装。atomic publish、UUIDv7 または deterministic ID、RFC 3339 日付配置、pending 件数と蓄積 warning も扱う raw observation store の境界であり、feedback の受理・保存・未処理判定に関する下位実装への入口になる。

## Read this when
- feedback observation の入力 schema 検査、安全性検査、secret masking、evidence path 境界、fingerprint、ID、canonical JSON、content hash、atomic な immutable 保存の挙動を確認するとき
- agent または machine rule が生成する observation の raw envelope と重複・衝突時の保存規則を変更または調査するとき
- raw observation の列挙、未処理判定、通常サブコマンド完了時の pending 件数や warning の計算を確認するとき

## Do not read this when
- feedback の正本となる受理条件や report cut、cleanup、公開状態の仕様だけを確認する場合は、対応する oracle または runtime state の実装を先に読むとき
- raw observation の保存処理を呼び出す上位 MCP tool や collector の責務だけを確認し、検査・永続化の内部挙動を調べないとき

## hash
- a2366392e08049378b6d393969dfaf84706fc68918598e6f506c7a076d8f1051

# `runtime_git.py`

## Summary
- Git repository と worktree の安全な操作を一元化する共通境界。Git command の実行結果・branch・HEAD・status を扱い、managed worktree の作成・削除・branch 判定を担う。
- worktree snapshot の取得・復元、symlink や特殊 file の検証、Git ignore の保証・判定を提供する。oracle/realization file の列挙と、repository path・Git 状態に基づく分類判定もここで行う。
- path 正規化、nested repository、Git index、ignore source、linked worktree metadata の安全性を横断して確認する必要がある処理から読むべき共通実装入口。個別の CLI や prompt 構築の仕様を確認する場合は、それぞれの仕様・呼び出し元へ進む。

## Read this when
- Git command の共通エラー処理、branch・HEAD・status の取得、managed branch の判定を変更または調査するとき
- run worktree の作成・削除、worktree path の検証、linked worktree metadata や symlink 安全性を扱うとき
- worktree snapshot の取得・復元や、Codex call 前後の作業成果物差分を扱うとき
- `.cmoc/gu` の ignore 保証、Git ignore source の検証、oracle/realization file の列挙・分類判定を変更または調査するとき

## Do not read this when
- Git 境界の内部実装を使うだけで、呼び出し側の CLI 挙動や仕様を確認することが目的の場合
- prompt 構築、path model、branch model、doctor、session などの正本仕様そのものを確認する場合
- Git や worktree と無関係な runtime helper、データ型、利用者向けエラーの実装だけを調べる場合

## hash
- 356e6f3b03da25a353c2c89dc7e85a6def0fc85f05de83b77eb3e3f69daa67d3

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines ログを管理し、実行イベント、step の経過時間、Codex quota 待機時間を集約する runtime logger。ContextVar による current logger の参照・差し替え・復元も提供し、並行 event 追記をロックで直列化する。

## Read this when
- サブコマンドのログファイル生成、JSON event の記録、step timing や quota 待機時間の集計を確認・変更するとき。
- 深い runtime helper から現在のサブコマンド logger を参照する処理や、並行実行時のログ追記を調査するとき。
- ログ event flush 後の feedback detector 呼び出しと、detector failure の非致命的な記録を確認するとき。

## Do not read this when
- ログやコンソールの正本仕様を確認する場合は、対象実装ではなく対応する oracle 仕様を直接読む。
- runtime path や timestamped path の生成規則だけを確認する場合は、対象ファイルではなく runtime path 実装を直接読む。
- feedback observation の保存形式や判定条件だけを確認する場合は、対象ファイルではなく feedback 仕様を直接読む。

## hash
- 930482a77490b4906a7dd1a33d718f6ed7b2070cb34ae6718a2461ace42152dd

# `runtime_paths.py`

## Summary
- リポジトリ、worktree、cmoc 自身の root 解決と、実行時の各種ディレクトリ・設定・状態ファイルのパス導出を担う共通 runtime path モジュール。timestamp 生成、duration 表示整形、timestamp 付きパス予約、root memo 判定、cwd の一時切替も提供する。
- root 解決や runtime directory の保存先、ログ・report・schema・worktree などのパスを利用する下位実装へ進むための共通入口。

## Read this when
- リポジトリ root、worktree root、cmoc root の解決挙動を変更・確認するとき
- session、report、log、schema、worktree、設定、refactor state などの保存先を扱う処理を変更・確認するとき
- timestamp、duration 表示、timestamp 付きファイル予約、cwd 切替、memo 配下判定の共通挙動を変更・確認するとき

## Do not read this when
- 特定のサブコマンド固有のログ・report 内容や保存処理を確認する場合は、そのサブコマンドの実装・仕様へ直接進むとき
- root placeholder の定義や実パス解決そのものの仕様を確認する場合は、path model の実装・仕様へ直接進むとき

## hash
- 4eae4e541f9b83357378196e3c7349a0369a99264dbb3a6aa3786bfd7db8fccc

# `runtime_refactor.py`

## Summary
- oracle と realization file の調査履歴を管理する共通ランタイムで、state file の読み込み・厳密な schema 検証・安全な保存・対象 file 集合との同期を担う。
- 未調査対象の生成、調査対象の優先選択、全対象の再調査要求化、work-root 相対 path の正規化検証、state path の symlink・非通常 file 拒否、履歴 entry の値検証を提供する。
- refactor state を扱う subcommand や preprocess、oracle/realization file の列挙・調査サイクルを実装または変更する際の共通入口であり、個別の CLI 表示や調査ロジックそのものを扱う対象ではない。

## Read this when
- refactor state の読み書き、schema 検証、調査履歴の保持、または oracle/realization file 集合との同期挙動を変更・確認するとき。
- 次に調査すべき対象の選択順、全対象を再調査対象に戻す処理、未調査 entry の初期値を確認するとき。
- state file の path 安全性、相対 path の正規化、SHA256 や調査日時など entry 値の受入条件を確認するとき。

## Do not read this when
- refactor state を利用する個別 subcommand の利用者向け仕様や CLI フローだけを確認する場合は、対応する app_spec または CLI realization を直接読む。
- oracle/realization file の列挙規則、file hash 計算、state path の決定規則そのものだけを確認する場合は、それぞれの専用 runtime または正本仕様を直接読む。
- 調査対象の内容をレビューする場合は、この state 管理実装ではなく対象となる oracle または realization file を読む。

## hash
- 7cb5fa2cd8fd6fe8e6a5487eb0059a2d28b1567ecea64ad3b46602d7ae7df062

# `runtime_results.py`

## Summary
- Codex exec 呼び出しの出力契約と、外部コマンド実行結果・Structured Output 検証結果・呼び出しログのパスを表す不変データ型を定義する。runtime 処理でこれらの結果型や callable protocol が必要な場合の入口となる。

## Read this when
- Codex exec の呼び出し結果、Structured Output、検証エラー、コマンド実行結果の型定義を確認したいとき。

## Do not read this when
- Codex exec の具体的な実行処理や prompt 生成規則を確認したいとき。
- 正本仕様や Structured Output の詳細な要件を確認したいときは、参照コメントに示された oracle 文書を直接読む。

## hash
- 5a643d9a702449bdf4fd5200a3ac5eea054dcef56d0df3eea35015dbef021e73

# `runtime_run.py`

## Summary
- editing run の worktree 解決、run state のライフサイクルロック、process tracking、親 run process と Codex child process group の安全な停止・cleanup を束ねる共通 runtime 境界。

## Read this when
- editing run の join・abandon・error cleanup を変更または調査するとき
- branch から worktree を解決する処理や、run process tracking の読み書き・検証を確認するとき
- PID 再利用、process group、pidfd、snapshot 検証を含む fail-closed な process 停止挙動を確認するとき

## Do not read this when
- worktree lookup や process cleanup を伴わない一般的な git 操作だけを扱うとき
- Codex process の低レベル操作そのものを変更する場合は、まず runtime の process profile 実装を読むとき

## hash
- e435abee016574bdf85d45d1393afa02f710f287b982efaef73336e7993f0082

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始から state 遷移、worktree・branch の管理、commit、差分分類、INDEX 更新、cleanup／recovery までを一貫して扱う共通 lifecycle 実装。EditingRunContext と lifecycle lock を共有し、run の不変条件と workload の差分許可範囲を検査する。
- session の ready 確認、isolated run の作成・公開・回収、joinable/error 遷移、work unit の rollback／commit、INDEX の再生成、Git tree change の解析、oracle・realization・生成 INDEX・refactor state の許可判定を提供する。

## Read this when
- editing run の開始・再開・終了、session state と run state の遷移、run branch／worktree の recovery や cleanup を変更・調査するとき。
- realization workload 後の差分許可範囲、unexpected path の検出、rename／copy を含む Git 差分分類、oracle diff の取得を確認するとき。
- run worktree の commit、INDEX 更新、lifecycle lock、process tracking、refactor state の扱いを変更するとき。

## Do not read this when
- session や editing run の外側で完結する CLI 機能、個別の realization 実装、または INDEX 生成規則そのものを確認したいとき。
- Git・state・worktree の共通低レベル API の仕様だけを確認する場合は、対応する runtime／state／indexing モジュールを直接読むとよい。

## hash
- 94a3a00104b763e45f55c6696dbceba1644d80e46d189218813b8ab4679a96e3

# `runtime_run_report.py`

## Summary
- editing run の fork report と lifecycle report を Markdown + YAML Front Matter 形式で保存する共通処理を提供する。レポート用ディレクトリの作成、timestamp に基づく衝突回避、実行状態・完了理由・変更パス・警告・詳細情報の記録を担う。
- YAML scalar、変更パス、Markdown における特殊文字を安全に表現する補助処理も含む。レポート生成やその出力エスケープを変更・調査するときの実装入口である。

## Read this when
- editing run の fork、join、abandon に関するレポート保存処理を変更するとき
- レポートの YAML Front Matter、完了情報、変更パス、警告の出力形式を確認するとき
- レポート出力における YAML・Markdown 特殊文字の安全なエスケープを調査するとき

## Do not read this when
- editing run のライフサイクル自体やコンテキスト管理の仕様を確認したいとき
- レポートの正本仕様を確認するときは、canonical な設計・アプリケーション仕様を先に読むべき場合
- レポートを利用する個別コマンドの挙動だけを調査し、共通出力処理を変更しないとき

## hash
- fbb90dc74d030d75dd110b736a9c3fc9f0125cd7103f7cbea2e1ff75512f4c57

# `runtime_state.py`

## Summary
- session state の dataclass schema、状態値、永続化・復元・検証を担う runtime モジュール。session/run branch と state file の対応付け、path traversal・symlink・不正な file 種別の拒否、排他 lock、active session の検索も提供する。

## Read this when
- session state の JSON schema、session/run lifecycle、state file の読み書きや検証を変更・調査するとき
- session branch または run branch から state を解決する処理、session fork 排他、state file の安全な保存先検証を扱うとき
- runtime state の不正入力・破損 JSON・不正 branch に対する CmocError の挙動を確認するとき

## Do not read this when
- CLI の各サブコマンド固有の処理だけを変更し、state の schema・読み書き・branch 対応付けに触れないとき
- session state の正本仕様そのものを確認する場合は、この実装ではなく oracle/doc/app_spec/session_state.md などの oracle file を直接読むとき

## hash
- 7c345df8bc8ad1c10a5993fce9b60cd0c0f988c6d884b110ba45c40cc928c14e

# `runtime_windows_toast.py`

## Summary
- Windows toast 通知と Codex TUI callback の非致命的な transport 境界を担うランタイム補助モジュール。通知文の短縮・固定化、Windows PowerShell/WinRT への有限時間 transport、TUI callback の invocation-local 状態と turn 重複排除を扱う。通知や callback 実装を確認する際の入口。

## Read this when
- Windows toast 通知の生成・送信、PowerShell executable の解決、通知文の入力制約や長さ制限を変更・確認するとき。
- Codex TUI の agent-turn-complete callback、thread/turn identity の受理、並行 callback の重複排除、callback 用一時 state の cleanup を変更・確認するとき。
- 通知 transport や callback の失敗が本命処理の terminal result に影響しないことを確認するとき。

## Do not read this when
- Codex の通常の terminal result 判定や最外側サブコマンドのライフサイクルだけを調べるとき。
- Windows toast や TUI callback と無関係な共通ランタイム機能、または通知本文の仕様を調べるとき。

## hash
- d26eaaed129a3bddaf5f37f26de7b8533f56efc33bda3aa829ac8978b9dcad53
