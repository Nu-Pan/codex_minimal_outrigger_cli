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
- CLI サブコマンド共通の実行ライフサイクルを管理する。work root 検査、doctor preprocess、サブコマンドログ、step 通知、feedback invocation、完了・失敗処理、エラー表示、終了通知を扱う。
- サブコマンド横断の中断状態、実行 step、完了サマリー、終了コード、経過時間、quota 待機時間の記録を提供する共通入口である。

## Read this when
- CLI サブコマンドの共通実行処理、ログ記録、step 通知、doctor preprocess、エラー終了、feedback invocation、Windows terminal result 通知を変更または確認するとき。
- サブコマンドの work root 実行条件や、成功・失敗・ユーザー中断時の終了経路を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックだけを変更または確認するとき。
- ログ保存、feedback store、エラー描画、パス解決、Windows 通知の具体的な実装だけを確認するときは、それぞれの専用モジュールへ直接進む。

## hash
- ea74f93b9ea5f993cbb88c5c8788b0c2be5a184723c88c1a43b95e6db03f0233

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
- doctor preprocess の修復処理全体を担う実装。doctor lock による排他、config・refactor state・ignore・.agents の同期、Git 一時 index の退避・合成・復元、修復 commit、失敗時の index 復元と追跡状態検証を一つの lifecycle として扱う。

## Read this when
- doctor preprocess の修復順序、排他制御、修復対象の同期、修復 commit、または Git index の退避・復元挙動を変更・調査するとき。
- 修復処理が staged 状態、worktree、Git common directory、HEAD 起点の一時 index とどう連携するかを確認するとき。
- doctor が .agents、.gitignore、config、refactor state の追跡状態を保証できない原因を調べるとき。

## Do not read this when
- doctor preprocess の正本仕様や期待する外部挙動を確認する場合は、先に参照されている oracle の仕様文書を読む。
- config の同期処理そのものを変更・調査する場合は、config 同期を担当する実装へ直接進む。
- refactor state の同期処理そのものを変更・調査する場合は、refactor state を担当する実装へ直接進む。
- 一般的な Git 実行や runtime error・feedback・path 解決の共通仕様だけを確認する場合は、対応する共通実装へ直接進む。

## hash
- b6269b70373b8681f7e0229c210f835d26e351f391b04802aa35e6d14df5eb24

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
- feedback reporter の capability 発行、Codex call ごとの受付・drain・無効化、Unix socket collector、agent observation の保存、degraded event の記録、feedback event の allowlist 検出を統合する invocation-scoped runtime モジュール。feedback のライフサイクルと非致命的な利用不能処理を確認するための入口であり、保存形式や reporter protocol の詳細は対応する runtime_feedback_store / runtime_feedback_reporter と oracle 仕様へ進む。

## Read this when
- feedback collector の起動・停止、Codex call context、reporter capability の環境継承、observation 受付や rate limit、degraded event、detector の挙動を変更・調査するとき。
- feedback reporter の利用可能性検証や、並行 Codex call における受付停止・drain・保存結果を確認するとき。

## Do not read this when
- observation の永続化形式、入力 schema、RFC3339 や observation ID の生成を直接調査するときは runtime_feedback_store を読む。
- MCP reporter の tool 公開面・stdio protocol 自体を調査するときは runtime_feedback_reporter を読む。
- feedback の正本となる人間向け要件を確認するときは対応する oracle 仕様を直接読む。

## hash
- a1795666ecedc77f1ecedf228f9e6420eaced6ac6e1363e7defab739cfb78cb8

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
- feedback の repository-local state を単一の integrity boundary で管理する中核実装。report cut の作成・再開・checkpoint、active generation と current pointer の検証・公開、canonical JSON・SHA256・symlink・atomic write による artifact 整合性、publication 後の cleanup、legacy state の read-only migration projection を扱う。feedback state の永続化・復旧・公開・削除処理へ進む入口であり、観測収集や report 集約の個別実装そのものではない。

## Read this when
- feedback state の schema、artifact reference、generation、current pointer、report cut、publication、cleanup、discard、checkpoint の挙動を変更または調査するとき
- active issue や machine aggregate の identity、threshold、bounded evidence、時刻・hash・canonical order の検証を確認するとき
- 異常終了後の report cut 復旧、publication 後 cleanup、legacy state の移行検証を確認するとき

## Do not read this when
- 観測 envelope の生成・入力受付・reporter validation だけを扱うとき
- 観測の正規化、issue 候補の生成、verification、Markdown report の内容生成だけを扱うとき
- CmocError や共通の JSON・hash・runtime utility の定義だけを確認するとき

## hash
- 265f5586a73f45715b1030a86db4a260b602cfa4851ff22e12596821383da7e9

# `runtime_feedback_store.py`

## Summary
- agent および machine rule の feedback observation を検証し、secret masking、path 正規化、fingerprint、canonical JSON hash、重複排除、atomic な immutable 保存を行う raw observation store。
- 保存済み observation の列挙・未処理判定と、通常サブコマンド完了時の pending 件数および蓄積警告を提供する。feedback observation の受理・永続化境界を確認するための入口。

## Read this when
- feedback observation の schema 検査、安全性検証、secret masking、evidence path 処理を変更・調査するとき
- raw observation の ID、hash、重複、atomic publish、temporary recovery、symlink 対策を確認するとき
- pending observation の列挙や feedback completion count の挙動を確認するとき

## Do not read this when
- feedback の正本 payload schema や受理条件の仕様を確認したいときは、対応する oracle specification を直接読む
- report の state 管理や publication cleanup の詳細を確認したいときは、runtime feedback state の実装・仕様を直接読む
- MCP tool の公開インターフェースや reporter 呼び出し経路だけを確認する場合

## hash
- f433514efc0977a4f4451d30d7221dd3b6f1094c6f83d10387c88ca87b5a9dda

# `runtime_git.py`

## Summary
- Git repository の状態取得・検証、branch と linked worktree の作成／削除、安全性確認、ignore 判定、worktree snapshot、oracle／realization file の列挙・分類を担う共通境界。Git path、filesystem object、symlink、ignore 状態に関する不変条件を共有する下位実装の入口。

## Read this when
- Git status、branch、HEAD、Git common directory、linked worktree を扱う処理を変更または調査するとき。
- worktree の snapshot／復元や、symlink・path traversal・管理領域の安全性を扱うとき。
- `.cmoc/gu` の ignore 設定、Git ignore source の検証、oracle／realization file の列挙または分類を扱うとき。

## Do not read this when
- Git や worktree、ignore、oracle／realization file の分類に関係しない runtime helper や CLI 挙動だけを扱うとき。
- 特定の subcommand の利用者向け仕様や branch 命名規則だけを確認する場合。必要な仕様文書や、その subcommand の実装を直接読む。

## hash
- 648a7f2224493da4d4289cdccbaabf751a24fa54abcf740865481948e17ec52f

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
- 明示的な join を必要とする editing run のライフサイクル共通処理を担う。session からの run 開始、active run の解決・復旧、state 遷移、work unit の commit/rollback、差分分類、INDEX 更新、worktree・branch の cleanup 判定を一つの文脈と lifecycle lock のもとで扱う。

## Read this when
- editing run の開始・join・復旧・終了処理を変更または調査するとき
- run や session の state 遷移、branch/worktree の整合性検査、lifecycle lock を確認するとき
- agent または run による変更 path の許可判定、oracle 差分、rename 対応の差分分類を確認するとき
- work unit の commit/rollback や run worktree の INDEX 更新処理を確認するとき

## Do not read this when
- 単純な session state のデータ構造や永続化形式だけを確認したいときは、state 管理の実装を直接読む
- INDEX の生成規則や個別の indexing 処理だけを確認したいときは、indexing 実装を直接読む
- Git の低レベル操作や run process ID の読み書きだけを確認したいときは、対応する runtime helper を直接読む

## hash
- f1e496317cee6391aa20f16955004648c572ab5e48753c117c31b61691913187

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
