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
- Codex CLI subprocess 境界の実行環境構築と実行結果解釈を担う。sandbox、argv、CODEX_HOME、provider 設定、Feedback MCP、process tracking、schema 配置、JSONL 出力・エラー判定を扱い、呼び出し側が Codex の起動条件や失敗時の分類を確認するための入口となる。

## Read this when
- Codex CLI に渡す sandbox、model/provider、通知、Feedback MCP、環境変数、schema の設定を変更・確認するとき。
- editing run における Codex subprocess の process group tracking、PID 再利用対策、停止・cleanup を調査するとき。
- Codex の JSONL 出力から session ID、capacity/quota/unexpected error を判定する処理を確認するとき。

## Do not read this when
- Codex 呼び出し側の prompt 生成や run 全体の業務フローだけを確認する場合。
- Codex CLI と無関係な設定、エラー型、Feedback reporter 実装の詳細を直接調査する場合は、それぞれの担当対象へ進む。

## hash
- 54a3a9a36d244a6741c0893e94d1d66f6f6873337702b65c3412f399c939871e

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動処理を担う実装。エージェント呼び出しパラメーターから作業ディレクトリ、設定上書き argv、CODEX_HOME、通知 callback、call log、feedback 用環境を準備し、Codex サブプロセスを実行する。
- Codex 呼び出しの成功・失敗をコンソールおよび logger に記録し、起動失敗は再送出し、サブプロセス失敗は call log の場所を含む CmocError に変換する。Codex TUI 呼び出し全体の実行経路を確認する入口として使用する。

## Read this when
- Codex TUI または Codex CLI サブプロセスの起動経路を追跡するとき。
- Codex の設定上書き、作業ディレクトリ、CODEX_HOME、通知 callback、feedback 連携、call log の生成を変更・確認するとき。
- Codex 呼び出しのログ記録、例外処理、終了コードの扱いを変更・確認するとき。

## Do not read this when
- Codex サブプロセスを起動せず、設定上書き argv の組み立てだけを確認する場合は runtime_codex_profile 側を直接読む。
- Codex 呼び出しの設定ファイル読込だけを確認する場合は runtime_config 側を直接読む。
- ログ保存、feedback、Windows 通知の個別仕様や実装だけを確認する場合は、それぞれの専用モジュールまたは正本仕様を直接読む。

## hash
- ce6c1bbf3143cad0b3d566c85d9899ff5b122f3b56ce56d146b68afcb809e691

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
- doctor preprocess における Git common directory 単位の排他ロック、修復対象の同期、元の index の退避・復元、一時 index の合成、修復 commit を一体として扱う実装。
- config・refactor state・.gitignore・.agents の修復と、利用者の既存 staged/unstaged 変更を分離した commit lifecycle を提供する。
- doctor 実行時の symlink や追跡状態の検証、Git index を指定して操作する補助処理、失敗時の index 復元を含む。

## Read this when
- doctor preprocess の排他実行、修復対象の同期、修復 commit、または処理失敗時の Git index 復元の挙動を変更・調査するとき。
- 一時 Git index を使った staged 状態の保持、HEAD 起点の修復差分分離、config・refactor state・ignore・.agents の追跡処理を確認するとき。
- doctor lock の path、Git common directory、修復対象 path の検証や Git 操作の安全性を確認するとき。

## Do not read this when
- doctor preprocess の仕様や利用者向け挙動を確認するだけで、実装上の lifecycle や index 操作を調べないときは、doctor preprocess の正本仕様を直接読む。
- config 同期、refactor state 同期、Git 共通操作など単一機能の詳細だけを変更・調査するときは、それぞれの専用実装を直接読む。
- 一般的な doctor コマンドの入口や CLI 引数の扱いを確認するときは、呼び出し元の CLI・command 実装を読む。

## hash
- 9e53b1272e85e36ba69ea22b5a22bb7cfa3999fabe5da4a2883b02322b0a534c

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
- サブコマンド invocation 単位の feedback collector lifecycle を担い、Codex call ごとの capability 発行、並行する observation request の受付、call 終了時の drain、collector 利用不能時の degraded event、および stable event の detector を統合する。
- feedback reporter と collector の IPC、rate limit、保存 context、call 終了順序、doctor による reporter availability 検査を確認するための入口である。

## Read this when
- feedback observation の受付・保存経路、Codex call の capability context、invocation-scoped collector の開始・停止・drain を変更または調査するとき
- reporter/collector の利用不能 event、structured output validation failure などの検出、または doctor の reporter availability 検査を変更するとき

## Do not read this when
- observation の保存形式や RFC3339・ID 生成などの永続化 primitive だけを確認する場合は、feedback store の実装を直接読む
- reporter が公開する MCP tool の schema や stdio protocol だけを確認する場合は、reporter 実装を直接読む

## hash
- 8daf2ff9f779537dc535e9a076a000b4af784ebc3c01b078e230667851a45f3c

# `runtime_feedback_reporter.py`

## Summary
- Codex が起動する call-scoped stdio MCP feedback reporter/client。collector との Unix ソケット通信、MCP JSON-RPC の初期化・ping・tool 一覧・観測送信、collector 応答の検証と agent-facing 結果整形を担う。feedback 報告機能の通信境界として、関連する runtime feedback 実装から送信処理の確認へ進む入口。

## Read this when
- 人間対応が必要な問題の observation 送信経路、feedback collector との通信、reporter の MCP JSON-RPC 挙動、collector 応答の受理・拒否検証を調査または変更するとき。

## Do not read this when
- feedback の観測内容の仕様や保存・検証規則を確認するときは、対応する oracle file や runtime feedback store を直接読む場合。feedback 機能と無関係な MCP server や CLI 実装を調査するとき。

## hash
- 1065a0e3d846f06e17628770d8a51947c789ad4091fa0c04661ac64b1b4383f7

# `runtime_feedback_state.py`

## Summary
- feedback の repository-local state を一つの integrity boundary で管理する中核 module。report cut、active generation、current pointer、checkpoint、publication、incomplete 診断、cleanup の生成・検証・復旧・破棄を扱う。
- 観測 envelope、machine aggregate、active issue、report cut manifest、artifact reference の schema・identity・canonical JSON・SHA256・path containment を検証し、異常終了後の checkpoint recovery と publication 後 cleanup を支える。
- feedback state の遷移や永続 artifact の整合性を確認する際の実装入口であり、raw observation の入力仕様や Markdown report の表示仕様そのものを読む入口ではない。

## Read this when
- feedback state の保存形式、current pointer、active generation、report cut の処理状態を確認するとき。
- feedback の publication、incomplete 診断、checkpoint、artifact hash、symlink 防止、writer lock、cleanup または recovery の挙動を調べるとき。
- feedback state の corruption 検出や、state transition を複数 module に分散させない責務を確認するとき。

## Do not read this when
- raw observation の envelope や reporter 入力の仕様だけを確認する場合は、feedback observation の仕様・実装を直接読む。
- feedback report の Markdown 内容や subcommand の利用者向け契約だけを確認する場合は、feedback report の仕様・実装を直接読む。
- feedback state を変更せず、単に個別の共通 ID・時刻・JSON helper の定義だけを確認する場合は、runtime feedback store を直接読む。

## hash
- b02d17fd46c20b2db47c84b98ef7f13a913d672ca24bfd877e280acf1af80ba9

# `runtime_feedback_store.py`

## Summary
- feedback raw observation の受理検査と immutable durable store を担う。reporter schema 検証、payload の secret masking、repository 内 evidence path の正規化と fingerprint、observation ID・content hash による同一性検査、atomic publish と一時ファイル回収を扱う。agent report と machine rule の raw observation 保存、保存済み observation の列挙・未処理判定・完了時の pending 件数および warning 算出への入口となる。

## Read this when
- feedback observation の入力検証、secret masking、evidence path の安全性、raw record の保存・重複排除・atomicity・durabilityを変更または確認するとき。
- agent または machine rule の observation 保存形式、observation ID、fingerprint、content hash、pending 判定の実装を追跡するとき。
- feedback report の前段となる raw observation の列挙や、通常サブコマンド完了時の pending 件数・蓄積 warning の挙動を確認するとき。

## Do not read this when
- feedback の正本となる受理条件や state 遷移の仕様自体を確認する場合は、対応する oracle の app specification を直接読むとき。
- report cut、runtime state の publication cleanup、MCP reporter 呼び出しの詳細だけを確認する場合は、それぞれの直接の実装対象へ進むとき。
- feedback と無関係な保存処理、一般的な JSON schema、または CLI の他サブコマンドの実装を調べるとき。

## hash
- c890b4cc3f6d18f6733ee96f017a23080d24d967e600c6659dbe846a09950ded

# `runtime_git.py`

## Summary
- Git repository と linked worktree の安全な操作、および oracle/realization file の分類を担う共通ランタイム境界。Git コマンド実行、branch・worktree の作成削除、snapshot 復元、ignore 検証、path 種別判定を一箇所に集約し、各 caller が repository path・Git 状態・symlink 安全性を個別に実装せずに済むようにする。

## Read this when
- Git command の実行結果を cmoc 向けエラーへ変換する処理を変更するとき。
- branch の取得・管理判定、linked worktree の作成・削除、worktree path と Git metadata の安全性を扱うとき。
- 作業成果物の snapshot、復元、Git status path の解析を変更するとき。
- `.cmoc/gu` の ignore 保証や Git ignore source の検証を扱うとき。
- repository path が oracle file または realization file に該当するか、あるいは対象 file を列挙する処理を変更するとき。

## Do not read this when
- CLI の個別サブコマンドの利用者向け挙動だけを確認したいときは、該当する subcommand の実装や仕様を直接読む。
- Git や worktree の正本仕様、branch 命名規則、path model の設計意図を確認したいときは、対応する oracle 文書を直接読む。
- runtime error、path、result 型の定義だけを確認したいときは、それぞれの専用 module を直接読む。

## hash
- 40cf4fc74ef248517ff72b28caee24e872c2559829c9ffcaec20b70aae805e0e

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
- refactor state を管理する共通ランタイム実装。state file の読み込み・保存時の安全性確認、entry schema 検証、oracle／realization file 集合との同期、調査対象の列挙・選択・再調査要求を担う。refactor state の処理経路を確認する際の入口となる。

## Read this when
- refactor state の読み込み、保存、schema 検証、file 集合との同期、調査対象の選択を変更または調査するとき
- oracle／realization file の変更検知や調査履歴の状態遷移を確認するとき

## Do not read this when
- refactor state を扱わない runtime 共通処理を調査するとき
- 個別の oracle／realization file の仕様や doctor preprocess の契約を確認することが目的で、対応する oracle file を直接読むべきとき

## hash
- 4048f5639be7781644c6692ffa62e9bffb1ac3d872066a1747d51f5722af2ef7

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
- 明示的な join を必要とする editing run の lifecycle 共通処理を担う。session からの run 開始、state 解決・遷移、branch/worktree 管理、workload の rollback・commit、差分分類、INDEX 更新、cleanup に関わる共通入口である。
- 同じ EditingRunContext と lifecycle lock を共有するため、run の開始から差分確定までの不変条件を一箇所で確認する必要がある場合に読む。個別 subcommand の仕様や realization 実装ではなく、複数の editing run 処理にまたがる lifecycle 制御を調べる際の入口である。

## Read this when
- editing run を開始、再開、joinable/error へ遷移、または active run として解決するとき。
- run branch/worktree の作成・検証・削除、session state と process tracking の整合性を確認するとき。
- workload 差分の rollback・commit、許可された realization・INDEX・refactor state の判定、oracle 差分や rename を含む差分分類を調べるとき。
- run worktree の INDEX 更新や、未確定 run の recovery・cleanup 条件を確認するとき。

## Do not read this when
- 個別の editing subcommand が要求する入力・出力・利用者向け挙動だけを確認したいときは、該当する subcommand 仕様を直接読む。
- realization file の実装内容や realization 固有の変更規則だけを確認したいときは、該当する realization file またはその仕様を直接読む。
- INDEX.md 生成規則、Git 実行補助、state schema など単一の下位責務だけを調べる場合は、対応する専用対象を直接読む。

## hash
- 4fa54bd7c712da95de56c17c022bb61c54870eee5b41971fbe058fd47a535288

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
