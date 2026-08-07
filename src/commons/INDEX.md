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
- エディタから AI Agent 用 prompt を受け取る共通境界を提供する。初期 prompt 用ファイルの予約・保存、エディタ起動、終了確認、HTML コメントと前後空白を除去した入力の返却を扱う。TUI やエディタ入力に関わる `.cmoc` の ignore 保証と、PATH 上のエディタ選択も担う。

## Read this when
- エディタ経由の prompt 入力フローを変更・調査するとき
- 初期 prompt の保存先予約、エディタ選択順、終了失敗時のエラー処理を確認するとき
- 入力から HTML コメントや前後空白を除去する処理を確認するとき
- prompt editor が利用する repository または worktree の `.cmoc` ignore 設定を確認するとき

## Do not read this when
- prompt の初期本文の構築仕様を変更・調査するときは、prompt 初期本文の builder を直接読む
- エディタを使わない prompt の生成・変換・実行処理だけを変更・調査するとき
- パス生成や timestamp の一般的な仕様だけを確認するときは、runtime paths の実装を直接読む
- cmoc のエラー型や ignore 操作の詳細だけを確認するときは、それぞれの runtime module を直接読む

## hash
- 714e1b66bc934aac54a81b9a64255547f48b5ea06cbcf7092367be60ddf8c4e3

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを管理する実装。work root 検査、ログ生成、feedback invocation、doctor preprocess、step 通知、完了サマリー、戻り値・例外のエラー処理を一元化する。関連するサブコマンド実装から共通実行経路や失敗時の記録動作を確認したいときの入口。

## Read this when
- 複数の CLI サブコマンドに共通する開始・終了処理、ログ、step 通知、doctor preprocess、feedback 処理を調査または変更するとき。
- サブコマンドの非 0 戻り値、例外、KeyboardInterrupt、エラー表示の扱いを確認するとき。
- 現在の実行ディレクトリや runtime state の配置規則を伴う共通実行処理を確認するとき。

## Do not read this when
- 特定サブコマンド固有の業務処理や引数定義だけを調査するときは、そのサブコマンドの実装を直接読む。
- ログの詳細な保存形式や logger 自体の挙動だけを調査するときは、runtime logging 関連の実装を直接読む。
- doctor preprocess、feedback、エラー描画の個別仕様や実装だけを確認するときは、それぞれの専用実装または正本仕様を読む。

## hash
- 739223b826e6d604a5fde1fce140f9914b55c3a257415acab30e7f1a79dfa935

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
- Codex CLI subprocess 境界の実装。起動前の sandbox、argv、CODEX_HOME、provider/MCP 設定、Structured Output schema 配置を準備し、起動後の process tracking、PID reuse を避けた process group 停止、JSONL 出力・error・resume token の解釈を担う。Codex CLI と cmoc の実行環境・機械的結果の変換が必要な場合の入口。

## Read this when
- Codex CLI の argv、sandbox、model/provider、MCP、CODEX_HOME、schema 配置を変更または確認するとき
- Codex subprocess の起動、process group tracking、abandon 時の停止、PID reuse 対策を変更または確認するとき
- Codex の JSONL 出力、session ID、capacity/quota/unexpected error 判定を変更または確認するとき

## Do not read this when
- Codex CLI 境界ではなく、呼び出し側の editing run 業務フローや retry 方針そのものを確認するときは、該当する上位の実行制御を読む
- Codex の設定値の正本や利用者向け仕様を確認するときは、設定・仕様の oracle 文書を直接読む
- 一般的な process 操作や JSON/TOML 変換だけを調べる場合は、これを包括的なユーティリティ実装として読む必要はない

## hash
- 0b29f6adb7e3496b14a2189bcde3655267fc313229fc7de75c7b2339af95f5f1

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動処理を担う実装。エージェント呼び出しパラメータと設定から Codex CLI の実行引数・環境・作業ディレクトリを準備し、呼び出しログとフィードバック処理を管理する。
- Codex CLI の起動結果をコンソールおよびサブコマンドログへ記録し、起動失敗や非ゼロ終了を cmoc のエラーとして返すための入口。

## Read this when
- Codex TUI の起動方法、設定上書き引数、CODEX_HOME の検証、呼び出しログの生成を変更・調査するとき
- Codex CLI 呼び出しの成功・失敗判定、終了コード、フィードバック呼び出し、ログイベントの挙動を確認するとき

## Do not read this when
- Codex CLI のサブプロセス実行そのものや環境変数構築の詳細を変更・調査する場合は、専用のランタイムプロファイル実装を直接読むとき
- 設定ファイルの読み込み規則やエージェント呼び出しパラメータの定義だけを確認する場合は、それぞれの定義元を直接読むとき
- Codex TUI 以外の CLI サブコマンドの処理を調査するとき

## hash
- d2a7dda0948a1d6552cd2f501bfc5d34304e986ddce2d754eb23237550effbee

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
- doctor preprocess の修復処理と commit lifecycle を一元的に扱う実装。Git common directory 単位の排他 lock、現在の index の退避・復元、.cmoc の ignore、.agents の追跡用 placeholder、config/refactor state の同期、feedback reporter の degraded 処理、修復差分の分離 commit を担当する。
- 一時 index を使って利用者の staged 状態や unstaged hunk、staged deletion、rename を保ちながら doctor 修復を合成し、失敗時には元の index を復元する。Git index 上の runtime state の追跡も最後に検証する。
- doctor preprocess の呼び出し、Git index/common directory のライフサイクル、修復 commit の挙動、.agents の安全なパス検証、または関連する一時 index 操作を調査・変更するときの入口となる。

## Read this when
- doctor preprocess の修復、同期、commit、失敗時復元の挙動を確認するとき
- Git common directory の lock、複数 worktree、現在 index と一時 index の分離を扱うとき
- .cmoc の ignore、.agents/.gitkeep、config、refactor state の追跡状態を修復・検証するとき
- doctor 修復が利用者の staged 状態や staged deletion を保持する仕組みを調査するとき

## Do not read this when
- doctor preprocess 以外の一般的な Git 操作や runtime 設定だけを調査するときは、それぞれの Git・設定関連実装を直接読む
- feedback reporter の単独の検証・通知仕様だけを調査するときは、reporter 関連の実装や仕様を直接読む
- doctor が同期する config や refactor state の内容・同期規則だけを調査するときは、各同期実装を直接読む

## hash
- cc0d7ce2aada85fc97d644d0e62be6e7dedc780ff8005e93397e6dcb4af9fe8f

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
- feedback の append-only tracked state を表す record の構築・保存・検証・参照を一元管理する中核モジュール。
- 観測、issue identity、revision、occurrence、assessment、disposition、ingestion、report の schema、content-addressed ID、record 間参照整合性を扱う。
- tracked state から effective issue view を構築し、作業ツリーまたは指定 Git commit 時点の feedback 状態を読み取る下位機能への入口となる。

## Read this when
- feedback state の record schema、ID 生成、append-only 保存、JSON 検証、issue 間参照の整合性を変更・調査するとき。
- 観測の正規化処理や report が利用する effective issue 選択、Git commit 時点の state 読み取りを確認するとき。
- feedback の新しい record 種別や field を追加し、構築・検証・読み取りの一貫性を確認するとき。

## Do not read this when
- agent からの feedback 入力 schema や issue 正規化の具体的な生成規則だけを確認したいときは、対応する oracle 仕様または専用の builder/schema を先に読む。
- feedback の収集、イベント検出、Git 操作、CLI の実行制御だけを調べるときは、それぞれの担当モジュールへ直接進む。
- 単純な runtime error 定義や canonical JSON、UUID、path 解決の共通実装だけを確認したいときは、インポート元の runtime 共通モジュールを読む。

## hash
- e3724f24e4687b8cc664e76aae331f40f4e7aae4e1f3d0e790b7ec088e22d6e7

# `runtime_feedback_store.py`

## Summary
- feedback raw observation の入力検証と immutable durable store を担う中核モジュール。schema 検査、secret masking、リポジトリ内 evidence path の正規化と fingerprint、UUID・hash による observation 識別、atomic publish、machine/agent observation の保存、ingestion receipt に基づく未処理件数と警告を扱う。feedback observation の受理・保存・report 完了件数や安全性を変更または確認するときの実装入口である。

## Read this when
- feedback reporter の payload 検証、secret masking、evidence path 境界、fingerprint の挙動を確認するとき
- agent または machine rule の raw observation 保存、重複排除、content hash、atomic な永続化を変更するとき
- 未処理 feedback の集計、report snapshot との照合、蓄積警告の挙動を調査・変更するとき
- feedback observation の ID、RFC 3339 時刻、canonical JSON、immutable record の保存形式に関係する作業をするとき

## Do not read this when
- feedback の正本 schema や期待する payload 契約を確認することが目的の場合は、対応する oracle schema・仕様を直接読む
- MCP tool の公開インターフェースや report の生成・正規化処理だけを変更する場合は、それぞれの直接の実装入口を読む
- feedback と無関係な共通 runtime 機能や通常の CLI サブコマンドを扱う場合

## hash
- 11ff908b5137a3decf37f1dc85e674b26d5b45b6c1f8e7150c780c55203a8a62

# `runtime_git.py`

## Summary
- Git repository と worktree の安全な操作を一元化する共通境界。Git コマンド実行、branch・commit・status の取得、linked worktree の作成・削除、管理対象検証、snapshot の取得・復元を扱う。
- Git ignore の検証・更新と、oracle file / realization file の分類を repository path と Git index の状態に基づいて判定する。関連する CLI 操作や path 分類、worktree 操作の実装から参照する共通 runtime helper。

## Read this when
- Git コマンドの実行失敗を cmoc のエラーへ変換する処理を変更するとき。
- branch、linked worktree、worktree snapshot、Git status、managed path の作成・削除・安全性検証を扱うとき。
- `.cmoc/gu` の ignore 保証、Git ignore source の検証、oracle / realization file の分類ロジックを変更または調査するとき。

## Do not read this when
- 個別の CLI コマンドの利用者向け仕様や branch 運用ルールだけを確認したいときは、対応する oracle doc を直接読む。
- Git 境界を利用する caller の業務フローや prompt 生成仕様を確認したいときは、その caller または正本仕様を直接読む。

## hash
- ad5f6745b8aa25ae8c9587fb3fe2b8caf9b0302a45b4fff22cb6cd64d9a9e9a9

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
- 対象は、realization file の調査履歴を管理する refactor state の読み込み・検証・同期・保存と、調査対象ファイルの列挙・選択を担う共通ランタイムモジュールです。state の schema、path・SHA-256・時刻の検証、symlink など安全性の拒否、調査状態の更新規則を確認したい場合の実装入口です。

## Read this when
- refactor state の load/write/sync、調査対象の列挙や優先選択、state entry の validation、path・digest・timestamp の妥当性検証を変更または調査するとき。
- realization refactor の state file と runtime 層の連携、未調査・調査済み状態の遷移、変更検知による再調査要求を確認するとき。

## Do not read this when
- refactor state の利用側コマンドや、state schema の正本仕様だけを確認したいときは、まずそれぞれの直接の実装・oracle 文書を読む。
- 一般的な runtime utility、Git path 判定、例外型、ファイル hash の詳細だけを調べる場合は、それぞれの担当モジュールへ直接進む。

## hash
- b2393d480925d0ef423511a4abc0a0b89bbdc64bff2058ec06a6fc3f268b9f79

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
