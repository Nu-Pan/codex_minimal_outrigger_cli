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
- INDEX.md の検査・生成・鮮度判定・書き込み・commit を一貫して扱う indexing lifecycle の共通実装。
- directory traversal、既存 entry の hash 検証と再利用、不足 entry の Codex 生成、深さ順更新、排他 lock、更新差分の commit が責務範囲である。
- INDEX.md 更新処理の実装入口として、indexing の挙動や lifecycle の変更を調査するときに進む対象。

## Read this when
- INDEX.md の自動生成、entry の再利用条件、hash による鮮度判定を変更・調査するとき。
- indexable なファイル・directory の列挙、symlink・binary・ignored path の扱いを確認するとき。
- Codex による entry 生成、並列実行、preflight、lock、INDEX.md 更新 commit の流れを確認するとき。

## Do not read this when
- 個別の INDEX.md entry の内容やルーティング方針だけを確認したいとき。
- Codex prompt の entry schema や生成 parameter の定義だけを調べるときは、該当する prompt builder の実装を直接読む。
- indexing と無関係な runtime path、git、Codex profile、結果処理の単独仕様を調べるとき。

## hash
- d1a409629aa6096f9c87d815521f50f668ac4cf632b6133acdd514c521ebbc7e

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
- CLI サブコマンドの共通実行ライフサイクルを提供する実装。work root 検査、doctor 前処理、サブコマンドログ、feedback invocation、step 通知、完了・失敗記録、エラー表示、終了通知を一元管理する。
- サブコマンド実装の実行ラッパーと、現在のサブコマンド状態を操作・参照する補助関数が含まれる。各 CLI サブコマンドの実行経路や共通終了処理を確認する入口。

## Read this when
- CLI サブコマンドの実行順序、共通前処理、ログ記録、終了コード処理を変更・調査するとき
- サブコマンドの step 通知、ユーザー中断状態、失敗時の summary、Windows 通知連携を確認するとき
- work root と repository root の runtime state・ログ配置の扱いを確認するとき

## Do not read this when
- 個別サブコマンドの業務ロジックや引数定義だけを変更・調査するとき
- ログ出力、エラー描画、doctor 前処理、feedback 保存、通知機能そのものの詳細実装を確認するときは、それぞれの専用 runtime モジュールや正本仕様を先に読む

## hash
- 3c6af065355fc1192633bd3dc793bf66ff93d39ea248e23debf3b2c693e16770

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
- 1 回の Codex exec における subprocess 実行ループを統括する状態機械。Structured Output の schema・JSON・事後条件検証と補正 turn、capacity retry、quota 待機および代表 probe、resume 継続を扱う。各呼び出しの prompt・stdout・stderr・output・call log を保存し、console と subcommand event へ結果を記録する。TUI 起動や低水準の Codex 実行補助ではなく、exec 実行制御全体を確認する入口である。

## Read this when
- Codex exec の再試行、Structured Output の補正・検証、quota 待機や代表 probe、resume session の継続処理を変更または調査するとき。
- Codex call の prompt log、stdout/stderr、output、call log の保存や、console・subcommand event の状態記録を変更または調査するとき。
- 作業成果物の snapshot、補正 turn による変更検出・復元、最終的な CodexExecResult の組み立てを確認するとき。

## Do not read this when
- TUI の起動や TUI 固有の分岐を変更・調査するときは、TUI 用 module を直接読む。
- Codex の argv、環境変数、Codex home、schema 準備、出力 JSON 読み取りの個別実装だけを変更・調査するときは、runtime_codex_profile を直接読む。
- Codex call の console 表示や共通 error formatting だけを変更・調査するときは、runtime_codex_logging を直接読む。
- 設定読み込み、feedback、worktree snapshot、パス生成など単独の補助機能だけを変更・調査するときは、それぞれの専用 module を直接読む。

## hash
- b8557009906e7ff053e9a08070b99f4ed51bc2cddec44cca8ce3cf27a6cc0cfd

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
- Codex 実行前の INDEX 更新 preflight を管理する共通ランタイム実装。preflight の登録・解除、exec/TUI 実行前の呼び出し、再入防止と直列化、work root の導出を扱い、実際の Codex 実行は既存 runtime 実装へ委譲する。

## Read this when
- Codex exec または TUI の起動前処理、INDEX 更新 preflight、preflight の登録・解除、再入防止や実行直前フックを変更・調査するとき
- Codex 呼び出し時の work root 導出や、preflight が作成する commit と本命 agent 処理の境界を確認するとき

## Do not read this when
- INDEX 更新そのものの探索・生成ロジックを変更するときは、preflight 実装ではなく登録された preflight の実装を直接読む
- Codex の実行本体や結果型を変更・調査するときは、委譲先の runtime_codex または runtime_results を直接読む
- preflight を使わない通常の agent call パラメータや CLI 入力処理だけを変更するとき

## hash
- ba58f854a5afc4c46c6fb221b18acbaa9f059d67ef91f749684051b15dd5bec9

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界の実装を担い、起動時の sandbox・argv・CODEX_HOME・環境変数・schema 配置と、実行後の process tracking・JSON/JSONL 出力・capacity/quota/error 判定を扱う。Codex 呼び出しの実行環境構築と機械的な結果解釈を確認する入口である。

## Read this when
- Codex CLI の起動引数、sandbox 権限、model/provider 設定、通知や feedback MCP の上書きを調べるとき。
- CODEX_HOME、subprocess の process group・pidfd・tracking file、abandon 時の停止や cleanup を変更・調査するとき。
- Structured Output schema の配置、Codex JSONL の session/error event、capacity・quota・unexpected error の判定を確認するとき。

## Do not read this when
- Codex CLI を呼び出す上位の業務フローや editing run 全体の仕様を確認する場合は、対応する app_spec または subcommand の実装・仕様を直接読む。
- Codex CLI 以外の一般的な subprocess 実行、設定値の検証、feedback reporter 自体の挙動を調べる場合は、それぞれの専用実装を直接読む。

## hash
- 217a2d18c640e54151b133627b31e6c7d59a727df335d174c5ee017625898afa

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動処理を担当する実装。設定上書き引数、作業ディレクトリ、Codex HOME、通知 callback、呼び出しログ、feedback 用環境、成功・失敗イベントを準備し、Codex subprocess を実行する。TUI 起動経路や Codex 呼び出しログ・終了処理を確認する際の入口となる。

## Read this when
- Codex TUI の起動、設定上書き、Codex subprocess の実行結果、呼び出しログ、通知 callback、feedback 連携を調査・変更するとき。

## Do not read this when
- Codex の通常の非 TUI 実行処理だけを調査するとき。設定値の定義や個別のログ形式の正本を確認する場合は、参照コメントで示された設定・仕様ファイルを直接読む。

## hash
- beb932fb492747edaf1009a5537bea7b381cc5c99218079dc803ae42f47f6bd6

# `runtime_config.py`

## Summary
- cmoc 設定の JSON 永続化境界を担当するモジュール。設定オブジェクトと JSON/TOML 互換値の相互変換、型・値・循環参照の検証、既定値補完、不正設定の利用者向けエラー化を行う。
- 設定ファイルの symlink・特殊ファイルを拒否し、安全に読み込み・書き込み・初期同期する。設定形式、Codex のモデル・provider・reasoning effort、oracle review の試行回数を変更・検証するときの実装入口。

## Read this when
- 設定の JSON 保存形式や復元処理を変更するとき
- Codex model/provider、reasoning effort、試行回数などの設定値検証を変更するとき
- 設定ファイルの生成・読み込み・書き戻し、symlink や特殊ファイルへの対応を調査するとき
- 不正な設定入力が CmocError として報告される境界を確認するとき

## Do not read this when
- 設定型そのものの定義や既定値を確認したい場合は、参照先の設定型定義を直接読む
- CLI コマンドの引数解析や実行処理だけを調べる場合
- 設定とは無関係な runtime path や一般的なエラー処理を調べる場合

## hash
- b747b382b51d18e1111ca14c92645c9b8c1915179905a77ab2712deed7439000

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
- doctor preprocess の修復処理、Git common directory 単位の排他ロック、一時 index の退避・合成・復元、修復 commit の生成を一体として扱う実装。
- config・refactor state・.gitignore・.agents の追跡状態を同期・検証し、利用者の staged 状態や unstaged hunk を保ったまま doctor の修復差分だけを commit する。
- doctor の実行ライフサイクル、Git index 操作、修復対象の安全性検証を確認する必要がある場合の実装入口。

## Read this when
- doctor preprocess の修復対象、commit、lock、Git index 復元の挙動を変更または調査するとき
- current worktree と main worktree の修復差分分離、config・refactor state の同期、.agents や .gitignore の追跡保証を確認するとき
- 一時 index を用いた staged deletion・rename・未 staged 変更の保持や、修復失敗時の復元処理を確認するとき

## Do not read this when
- doctor preprocess 以外の CLI 処理や runtime 設定の詳細だけを調べるときは、それぞれの直接の実装を読む
- 正本仕様や doctor の利用者向け挙動を確認するだけの場合は、対応する oracle 文書を先に読む
- 一般的な Git 操作や feedback reporter の個別実装だけを調べる場合は、この lifecycle 実装全体を読む必要はない

## hash
- 8cfeaf3289f1b93ed4eb92279118878345cef2f76f8d01424a8744e0c7871843

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
- feedback observation の invocation-scoped collector と Codex call 単位の capability lifecycle を統合する中核 runtime 実装。Unix socket による reporter request の受付、並行処理、rate limit、保存、call 終了時の drain、degraded event の発行、allowlist 済み event の machine observation 化を担う。collector の開始・停止、現在 invocation の取得、call context の開始、doctor 用 reporter/collector 検証、accepted observation の取得が、この機能群への主な入口である。

## Read this when
- feedback reporter、collector、observation の保存経路を変更・調査するとき
- Codex call の capability、subprocess 環境、受付停止、drain、並行 request の挙動を確認するとき
- reporter unavailable や Structured Output validation exhausted の event 検出・machine observation 化を確認するとき
- doctor における reporter schema、MCP protocol、collector socket の可用性検証を変更するとき

## Do not read this when
- 保存形式や observation payload の schema・永続化規則だけを確認したい場合は、runtime_feedback_store の実装または対応する oracle を直接読む
- MCP reporter 自体の tool 実装や stdio protocol の詳細だけを確認したい場合は、runtime_feedback_reporter を直接読む
- 一般的な subcommand logging や git context の仕様だけを確認したい場合は、対応する runtime_logging・runtime_git・runtime_state の実装を直接読む

## hash
- 455d13200beda2c58cee6982200b1d490d0c4fc0a842e4e0a1f3cbf52d895f21

# `runtime_feedback_reporter.py`

## Summary
- call-scoped stdio MCP サーバーとして動作し、フィードバック observation の送信機能を提供する。
- collector への Unix ソケット接続、capability envelope の付与、プロトコル検証、transport failure の domain result 化を担当する。
- MCP の initialize、ping、tools/list、tools/call を newline-framed JSON-RPC で処理する実装への入口である。

## Read this when
- feedback observation の MCP reporter、collector 通信、capability または protocol 検証の挙動を確認・変更するとき。
- stdio JSON-RPC サーバーのリクエスト処理や submit_observation tool の公開仕様を確認するとき。

## Do not read this when
- feedback observation の保存・検証ルール自体を確認するときは、対応する runtime feedback store や oracle specification を直接読む。
- MCP reporter を利用する側の runtime 環境変数や起動条件だけを確認するときは、runtime feedback の定義を直接読む。

## hash
- 111588f6ba1a4fadde593bcc9f66d645c80e55dd66afb17f773b62e16941eb82

# `runtime_feedback_state.py`

## Summary
- repository-local feedback の append-only normalized state を一元的に扱う実装。record の構築、ID 生成、観測 envelope と各 record の schema 検査、record 間参照検証、effective issue view 選択を担う。
- normalization unit の recovery・publish、effective state の読み込み、state snapshot の生成・復元、report publication の recovery・検証・履歴管理までを扱う。
- feedback state の不変条件と読み取り規則を共有する下位実装への入口であり、対応する正本仕様は oracle 側の feedback state 仕様。

## Read this when
- feedback observation や normalized record の schema、ID、content hash、path、参照関係を変更または調査するとき
- effective issue の revision・assessment・disposition 選択、normalization unit の確定・再開、state snapshot の復元を確認するとき
- feedback report の publication、recovery、predecessor 連鎖、snapshot 参照を変更または検証するとき
- feedback state の永続化、writer lock、immutable artifact の整合性検証を調査するとき

## Do not read this when
- feedback の正本仕様や不変条件そのものを確認することが目的の場合は、対応する oracle の仕様を読む
- report の表示内容や agent に渡す normalization 入出力だけを調査する場合は、それぞれの report 生成処理または feedback builder/schema を直接読む
- feedback state と無関係な CLI、runtime error、一般的なファイル保存処理を調査する場合は、該当する専用実装を直接読む

## hash
- 9be3f5bc9ffabb8cfe87e2bc01746d532b8b210a03c25a5773823ff871e6b236

# `runtime_feedback_store.py`

## Summary
- feedback observation の入力検査と raw observation の durable store を担う実装。正本 schema による検証、secret masking、payload サイズ・evidence・repo 内 path の検査、path fingerprint、canonical JSON と SHA-256、UUIDv7 または machine rule に基づく observation ID、immutable record の atomic publish/recovery を扱う。
- agent および machine rule の observation 保存、raw observation の列挙、ingestion receipt に基づく未処理件数、直近 report snapshot と比較した増加件数、蓄積時の warning を提供する。feedback の正本仕様や normalized state/report chain の詳細ではなく、raw observation の保存境界から確認する入口。

## Read this when
- feedback reporter の payload 検証、secret masking、evidence path の正規化または fingerprint を変更・調査するとき
- raw observation の ID、canonical JSON、hash、immutable 保存、atomic publish、temporary recovery、重複・collision 処理を確認するとき
- agent rule observation の保存形式、observation file の列挙、未処理件数や完了時 warning の算出を確認するとき

## Do not read this when
- feedback の正本 schema や受理条件の意図を確認したいだけのときは oracle の feedback observation 仕様を読む
- normalized feedback state、ingestion receipt の有効性、report chain や snapshot publication の詳細を調査するときは runtime feedback state または report 実装を直接読む
- MCP tool の公開インターフェースや agent 側の報告判断だけを確認するときは、その呼び出し元・tool 実装を読む

## hash
- c5ab7ee2aa3490a29c63ab34b5ab7825dd2339720de50dd0c2c7b809f49b7758

# `runtime_git.py`

## Summary
- Git repository と worktree を扱う共通境界。Git コマンド実行、branch・linked worktree の作成／削除、path の安全性検証、ignore 判定、oracle／realization file の列挙・分類を提供する。Git 状態や repository path、cmoc 管理領域の安全な操作が必要な実装の入口。

## Read this when
- Git コマンドを共通のエラー処理付きで実行・検証するとき
- cmoc 管理下の branch や linked worktree を作成、削除、検証するとき
- Git ignore 状態、oracle file、realization file の判定や列挙を変更・利用するとき
- worktree snapshot の取得・復元や path／symlink の安全性境界を確認するとき

## Do not read this when
- Git や worktree、ignore、oracle／realization file 分類に関係しない機能を変更するとき
- 個別の runtime error、path、result 型の定義だけを確認したいときは、それぞれの専用モジュールを直接読む

## hash
- 463ff20ca4d39a8e6d35768b7fb4338f44ba2f8c7028e43331f73539bf0fe84f

# `runtime_logging.py`

## Summary
- サブコマンド実行時の JSON Lines ログとステップ計測を集約するランタイムロガーを提供する。ログイベントの排他追記、フィードバック検出器の失敗記録、経過時間・quota 待機時間の集計、ContextVar による現在の logger 参照を扱う。サブコマンドのログ出力、ステップ進捗計測、実行時フィードバック連携を実装・調査するときの入口である。

## Read this when
- サブコマンド単位のログファイル生成や JSON Lines event の記録を変更・調査するとき。
- step の開始・終了、経過時間、quota 待機時間の集計を変更・調査するとき。
- 現在のサブコマンド logger を runtime helper から参照する ContextVar の利用を変更・調査するとき。
- feedback detector の呼び出しや detector failure の nonfatal な記録を変更・調査するとき。

## Do not read this when
- ログ形式や console 表示の正本仕様を確認することが目的の場合は、先に対応する oracle 文書を読む。
- ログ保存先や timestamped path の生成規則だけを確認する場合は、runtime paths の実装またはその正本仕様を直接読む。
- サブコマンド固有の処理や CLI の公開挙動を調査する場合は、該当するサブコマンド実装を直接読む。

## hash
- 6315c00333bab7613d8a5cd856c54a34c603e525661d79d7a0fe967374f22b12

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
- refactor state の読み込み・検証・保存・同期を担う共通ランタイム実装。state path の安全性、JSON schema、work-root 相対 path、調査履歴の SHA256 と時刻形式を検証する。
- oracle/realization file の列挙、未調査対象の優先選択、全対象への再調査要求を提供する。refactor state に関する実装の入口であり、上位 CLI フローや正本仕様の入口ではない。

## Read this when
- refactor state の読み込み、書き込み、schema 検証、path 検証、file 集合との同期を変更・調査するとき。
- refactor workload の対象列挙、未調査対象の優先選択、全対象への再調査要求を確認するとき。
- state path の symlink・非通常ファイル拒否や、調査履歴の整合性検証を確認するとき。

## Do not read this when
- doctor preprocess や realization refactor の利用者向け仕様を確認することが目的で、実装の詳細が不要なとき。対応する oracle doc を直接読む。
- CLI のコマンド受付や上位 orchestration の挙動だけを確認するとき。呼び出し側の実装を直接読む。
- refactor state と無関係な共通 runtime 機能を調査するとき。

## hash
- 7fe3e1176584aba4799f1f9356120e8d1eec3d1e75a410014b938a7ff4b8c79f

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
- editing run の開始から state 遷移、workload commit、差分分類、INDEX 更新、cleanup 判定までを共通管理する lifecycle 実装。
- EditingRunContext と lifecycle lock を中心に、session/run の事前条件検査、run worktree の作成・復旧・状態保存、許可外差分の検出を担う。
- git 差分の安全な列挙、oracle 差分抽出、run target の確保など、editing run の下位処理から利用される共通入口である。

## Read this when
- editing run の開始、joinable/error 遷移、復旧、worktree cleanup の挙動を変更または調査するとき
- realization agent の変更範囲、run branch・session branch の差分許可判定を確認するとき
- workload commit、INDEX 更新、rename/copy を含む Git 差分処理を変更または調査するとき

## Do not read this when
- session state のデータ構造や永続化形式だけを確認する場合は runtime_state の実装を読むとき
- INDEX の生成アルゴリズムだけを確認する場合は indexing の実装を直接読むとき
- editing run の利用者向け仕様や中断時の要件を確認する場合は対応する oracle doc を先に読むとき

## hash
- 1bc627c17c3ce127fa032a0b71340fbd854498a11ffcbc56780e8cdee78ba73f

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
