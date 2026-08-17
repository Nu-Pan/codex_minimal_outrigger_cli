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
- cmoc の実行時共通 API を集約する公開モジュール。CLI サブコマンド実行、Codex subprocess、設定・ログ・パス・Git worktree、プロセス制御、状態管理、コンテンツハッシュ、エラー処理など、複数の実行経路から共有される runtime 機能への入口を提供する。これらの共通 runtime API の責務や公開シンボルを確認・変更するときに読む。個別機能の詳細な実装挙動を調べる場合は、対応する runtime モジュールを直接読む。

## Read this when
- CLI 実行や Codex subprocess の起動・中断・終了待機の共通処理を確認するとき
- 設定、ログ、パス、Git worktree、状態ファイル、プロセス追跡などの runtime 共通 API の利用箇所を調べるとき
- cmoc の runtime 公開インターフェースにシンボルを追加・変更するとき

## Do not read this when
- 特定の runtime 機能の内部実装だけを確認する場合
- CLI の個別サブコマンドや Codex preflight の具体的な挙動だけを調べる場合

## hash
- 69a287946e5eacc33fcb4a1c73860d4f4815172adb652d774738f5dae37980cf

# `indexing.py`

## Summary
- INDEX.md の検査・再生成・ハッシュ検証・書き込み・commit を一つの lifecycle として扱う共通実装。
- directory traversal、既存 entry の再利用、不足 entry の Codex 生成、深さ順の更新、失敗時の復元、indexing lock による直列化を担う。
- 下位 directory の INDEX.md 更新から repository root の INDEX.md 更新まで、indexing preflight の入口として利用される。

## Read this when
- INDEX.md の自動生成や preflight の動作を変更・調査するとき。
- 既存 entry の再利用条件、対象 hash の計算、entry の schema 形式検証を確認するとき。
- indexing の並列実行、Git commit、lock、失敗時の snapshot 復元を確認するとき。
- symlink、binary file、git ignore、特殊 file、root memo の indexing 対象外条件を確認するとき。

## Do not read this when
- INDEX.md entry の出力項目や Structured Output schema 自体を確認したいときは、index entry parameter または schema の定義を直接読む。
- Codex 呼び出し前後の一般的な preflight 登録や process tracking の実装だけを調べるときは、対応する runtime module を直接読む。
- indexing 以外の Git 操作、path 解決、hash primitive の一般仕様だけを調べるときは、それぞれの runtime または cmoc_runtime の定義を直接読む。

## hash
- b2bc2dc4201e5c78cf2b460d664e329c65df4ad2f56d993b303a9d1bfba13f4c

# `prompt_editor_input.py`

## Summary
- エディタを使った AI Agent prompt 入力の共通境界を担う。作業用ファイルと入力保存先の予約、初期 prompt の書き込みとエディタ起動、編集後の安全な読み取り・保存・抽出、完了時の削除、関連 repository の ignore 保証を扱う。prompt editor の入出力挙動、エディタ選択、作業ファイル検証、入力保存の安全性を確認・変更するときの入口となる。

## Read this when
- prompt editor の作業ファイル予約・編集・収集・確定処理を変更するとき
- 利用可能なエディタの選択規則や editor work file の検証を確認するとき
- HTML comment 除去を含む最終 prompt 入力の抽出・保存境界を確認するとき

## Do not read this when
- prompt の内容や skeleton の生成規則だけを確認する場合は prompt builder の正本を直接読む
- 一般的な runtime error、git ignore、path 解決の仕様だけを確認する場合は、それぞれの専用実装・正本を直接読む
- prompt editor を使わない Agent prompt の構築や入力処理を確認する場合

## hash
- 1d4a3162e3adb15aa78f7080838350612f461c281b606557b2732f786705354e

# `runtime_cli.py`

## Summary
- 最外側の CLI サブコマンド実行を統括するランタイム境界。work root 検査、doctor preprocess、進行 step、診断ログ、feedback 回収、primary report 保存、terminal result の生成・表示、終了コード、Windows 通知までを一連の終端処理として扱う。
- サブコマンドの正常完了、ユーザー中断、handled failure、internal failure、TUI 起動前後の KeyboardInterrupt を分類し、エラー詳細・次の操作・警告・実行時間・診断ログをログとコンソールへ反映する。
- 最外側サブコマンドのライフサイクル、terminal result の形式、失敗時の終了処理、進行 step や中断状態の共有コンテキストを変更・調査するときの入口であり、個別機能の実装や各種ログ・通知・report 保存の詳細は対応する下位モジュールを直接読む。

## Read this when
- CLI サブコマンドの起動から終了までの共通処理を確認するとき
- terminal result、終了コード、primary report、診断ログ、feedback 件数、Windows 通知がどの経路で確定するかを調査するとき
- 正常完了・ユーザー中断・エラー分類や KeyboardInterrupt、TUI プロセス境界の挙動を変更・レビューするとき
- サブコマンド共通の進行 step、work root 制約、現在の logger や中断状態の管理を確認するとき

## Do not read this when
- 特定のサブコマンド固有の業務処理だけを調べるとき
- ログ出力、feedback、primary report、エラー描画、通知の内部仕様だけを調べるときは、それぞれの専用モジュールや正本仕様を直接読む場合
- terminal result のデータ型や個別コマンドの引数定義だけを確認したいとき

## hash
- 5d5bb786c861c2fae583bb445504686458d24d6cc8d749662c55f8535525fd95

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
- 1 回の Codex exec 呼び出しにおける実行制御の中心的な状態機械。Structured Output の schema 準備・JSON parse・JSON Schema・事後条件検証と、失敗時の同一 session による出力補正を扱う。
- Codex subprocess の argv、cwd、環境、prompt stdin、session ID、agent/call ID を組み立て、prompt・stdout・stderr・output・call log と subcommand event を記録する。
- capacity error の指数 backoff retry、quota error の代表 probe と待機・resume、Codex failure の分類、補正 turn による成果物変更の検出・復元を一体で制御する。TUI 起動、個別の設定・ログ・probe builder の実装詳細は下位 module が入口となる。

## Read this when
- Codex exec の再試行、quota 待機・代表 probe・resume、または Structured Output 補正の挙動を変更・調査するとき
- Structured Output の schema 読み込み、厳格な JSON parse、JSON Schema 検証、宣言済み事後条件、検証失敗時の diagnostic を確認するとき
- Codex call の prompt、stdout、stderr、output、call log、subcommand event、session ID の記録や失敗分類を追跡するとき
- 補正 turn が作業成果物を変更しないこと、変更時の復元と失敗通知を確認するとき

## Do not read this when
- TUI の起動や画面処理そのものを調べるとき
- Codex subprocess 内部の実装、設定ロード、ログ整形、quota probe parameter の生成だけを調べるとき
- Structured Output を使わない別の実行経路の仕様だけを確認するとき

## hash
- 5a9ef3187eb5c646066a559333f0ce6ec2b601bc9f7728b26ac27f78f9b2b8f4

# `runtime_codex_logging.py`

## Summary
- Codex 起動失敗時の例外を、console と event で共通利用するエラーテキストへ変換する関数を扱う。CmocError では summary と detail を結合し、それ以外の例外では文字列表現を返す。

## Read this when
- Codex の起動失敗メッセージを表示またはイベント記録用に整形する処理を確認・変更するとき。

## Do not read this when
- Codex 起動失敗のエラーテキスト変換を扱わず、例外クラスの定義や他のログ出力処理を確認するとき。

## hash
- ef6a79517ca30e97d6182505b400d2e7885ee67924795356eaa3d4a59c90826f

# `runtime_codex_preflight.py`

## Summary
- Codex の exec/TUI 実行前に INDEX 更新用の preflight を挟むランタイム境界を提供する。preflight の登録・解除、再入抑止、直列実行、実行対象 root の決定を担い、実際の Codex 実行は runtime_codex へ委譲する。Codex 呼び出し前処理や INDEX 更新連携の実装を確認・変更するときの入口となる。

## Read this when
- Codex exec または TUI の起動前に indexing preflight がどのように適用されるか確認するとき
- preflight の登録・解除、再入防止、ロックによる直列化、work root の決定を変更するとき
- Codex 実行本体への委譲境界や before_agent_call の通知タイミングを確認するとき

## Do not read this when
- Codex 実行本体のプロセス起動や結果処理だけを確認・変更するときは、委譲先の runtime_codex または runtime_results を直接読む
- AgentCallParameter や agent call path の定義自体を確認するときは、それぞれの定義元を直接読む

## hash
- 465d27a42a602c0bc59a6bd01f94897f0f560ae35974e1b15d86a7a03afe81ff

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界を一元管理する実装で、起動前の sandbox・argv・CODEX_HOME・schema・環境変数の構成、実行中の child process tracking と安全な process group 停止、起動失敗の cmoc エラー化、終了後の JSON/JSONL・resume token・capacity/quota/unexpected error 判定を扱う。Codex の実行環境や機械的な実行結果の解釈を変更・調査する際の入口であり、呼び出し側の run 制御や利用者向けエラー文言そのものを扱う対象ではない。

## Read this when
- Codex subprocess に渡す sandbox、model/provider、TOML config override、notification、feedback MCP、CODEX_HOME、環境変数を変更または確認するとき。
- editing run の process tracking、PID reuse 対策、pidfd、process group の signal・cleanup・lock を変更または調査するとき。
- Codex CLI の起動失敗、schema 配置、stdout JSON、JSONL error、resume token、capacity/quota の retry 判定を変更または調査するとき。

## Do not read this when
- Codex CLI 境界の実行結果ではなく、上位の editing run 制御、agent call の業務フロー、利用者向け仕様だけを確認したいときは、対応する上位実装や正本仕様を直接読む。
- Codex CLI 以外の subprocess、一般的な設定検証、feedback の収集処理自体を変更するときは、それぞれの専用実装を直接読む。

## hash
- 462693a369d66b479d5d7f12d456f0b2cc29fbd8f338f4b20ee46d7edbffbe2f

# `runtime_codex_tui.py`

## Summary
- Codex TUI の 1 回の呼び出しを、設定上書き・作業ディレクトリ・Codex Home・通知 callback・call log・feedback 環境を準備して実行するランタイム入口。
- Codex CLI/TUI の起動失敗や終了失敗を cmoc のエラー形式へ変換し、成功・失敗イベントと実行時間を記録する処理を扱う。

## Read this when
- Codex TUI の起動方法、argv や環境変数の組み立て、Codex Home の検証を変更・調査するとき。
- Codex 呼び出しの call log、feedback callback、通知 callback、実行結果やエラー記録の連携を確認するとき。

## Do not read this when
- Codex 呼び出し以外の cmoc CLI サブコマンドの実装を調べるとき。
- Codex の設定上書き規則や subprocess 実行の詳細だけを確認したい場合は、直接それらを担当する runtime_codex_profile などの対象を読むとき。

## hash
- 3a3fe23d6ec54b6490a9c1aa19f80b98fb46e5e93432d08ee10b15a7648db334

# `runtime_config.py`

## Summary
- 対象ファイルは、cmoc の設定オブジェクトと永続化 JSON の相互変換を担う実行時設定境界です。Codex の model provider・model・reasoning effort、並列数、oracle review のループ回数を型検証し、既定値補完済みの設定へ復元します。
- JSON/TOML に安全に保存できる値、非空モデル名、int 型、循環・深すぎるコンテナなどを検証し、不正入力を利用者向け CmocError に変換します。
- 設定ファイルの symlink・特殊ファイルを拒否し、既定設定の生成、読み込み、安定した JSON 書き出し、既存設定の同期までをまとめて提供するため、runtime config の読み書きや設定値の境界検証を調べる際の入口です。

## Read this when
- cmoc config の JSON 永続化形式、設定値の型検証、既定値補完、読み込み・書き出し・同期の挙動を確認または変更するとき
- Codex model provider/model/reasoning effort や oracle review の設定が runtime の CmocConfig に変換される経路を追うとき
- 設定ファイルの symlink、特殊ファイル、不正 JSON、Unicode・数値・循環コンテナに対するエラー境界を確認するとき

## Do not read this when
- 設定型そのものの定義や既定値を確認したいだけの場合は、参照先の CmocConfig・Codex 設定型を直接読むとよい
- CLI のコマンド仕様、oracle review の処理ロジック、Codex 実行そのものを調べる場合は、この変換・ファイル I/O 境界ではなく各機能の実装を直接読むとよい
- INDEX.md のルーティングやリポジトリ全体の開発手順だけを確認する場合

## hash
- 72d97496bf04e4e7f30816fcaca3e738285db31e1de0d8300ecb8d2dc791295a

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
- doctor preprocess の一連の lifecycle を実装する中心モジュール。Git common directory 単位の doctor lock を保持しながら、current/main worktree の修復、config と refactor state の同期、.gitignore と .agents の追跡保証、修復専用 commit、元の Git index の退避・合成・復元、修復後の追跡状態検証を扱う。
- Git index と worktree の状態を保ったまま doctor 修復だけを commit する必要がある処理、doctor の並行実行制御、修復失敗時の index 復元、.agents や runtime state の安全な修復条件を確認する際の入口となる。関連する個別 runtime 処理の実装ではなく、これらを共有する doctor preprocess lifecycle 全体を追う場合に読む。

## Read this when
- doctor preprocess の修復対象、修復 commit、Git index の退避・復元、または Git common directory の排他制御を変更・調査するとき。
- config または refactor state の同期を doctor の commit 対象から分離する条件を確認するとき。
- .gitignore、.agents/.gitkeep、.cmoc/gu の修復・除外と、current/main worktree 間の適用範囲を確認するとき。
- doctor 実行前の staged/unstaged 状態を保持し、失敗時にも元の index を復元する挙動を確認するとき。
- doctor 修復後に runtime state が Git index へ登録されていることを検証する経路を確認するとき。

## Do not read this when
- doctor preprocess と無関係な通常の Git 操作や、個別の config・refactor state 同期処理だけを確認したいときは、それぞれの runtime モジュールを直接読む。
- feedback reporter の可用性判定そのものや、ignore 規則の生成そのものを変更・調査するときは、対応する runtime モジュールを直接読む。
- INDEX.md の既存エントリーや、対象ファイルの機械的な識別情報だけを確認したいとき。

## hash
- 2bd5d7e71390af933dfd0092fb4e04a68ad8d52699de326f261c07d9f9996761

# `runtime_errors.py`

## Summary
- cmoc の実行時エラーを利用者向けレポートへ変換する共通処理を提供する。CmocError は概要、復旧手順、詳細、任意の TerminalResult を保持し、render_error は handled failure を固定形式の日本語テキストとして描画する。
- エラー例外の定義や、ログ初期化前などの境界でエラー表示を生成する実装を確認する入口であり、個別の実行結果型や通常の成功結果の仕様を直接扱う対象ではない。

## Read this when
- CmocError の属性、初期化引数、利用者向けエラー情報の保持方法を変更・確認するとき。
- CmocError と一般例外で異なるエラー概要、次の操作、詳細の描画規則を確認するとき。
- ログを初期化できない境界での handled failure の出力形式や既定の復旧案を調査するとき。

## Do not read this when
- TerminalResult 自体の構造や実行結果の成功・失敗判定を確認したいときは、runtime_results の定義を直接読む。
- 特定の処理がどのエラーを生成するか、または個別コマンドの復旧手順を調査するときは、その処理の実装・仕様を直接読む。
- 通常のログ初期化後のロギングやエラー報告経路を確認するときは、対応するロギング・呼び出し側の対象を読む。

## hash
- 33042ac16a1d08c3bf2b74c523eeb675d85d4eea29573495d298544666abb45f

# `runtime_feedback.py`

## Summary
- invocation-scoped な feedback collector と Codex call 単位の capability lifecycle を統合する実装。
- reporter からの request を Unix socket で並行受付し、protocol・capability・payload・HEAD commit・観測数の制約を検証して agent observation を保存する。
- call 終了時には新規受付を停止し、in-flight request を drain して capability context を破棄する。collector 全体の停止時も同じ lifecycle を適用し、socket と worker を後処理する。
- collector や reporter が利用不能な場合は本命処理を妨げず degraded call と stable な reporter_unavailable event／warning に移行する。doctor 用に collector protocol、reporter MCP interface、schema、protocol version を非破壊検査する。
- allowlist 済みの reporter_unavailable および Structured Output validation exhausted event を検出し、安定した context と rule を付与した machine observation として保存する。feedback の invocation context、Git、log、runtime state 連携を確認する際の実装入口である。

## Read this when
- feedback observation の収集・保存経路を変更または調査するとき。
- Codex call の並行受付、call 終了時の drain、capability の伝播・無効化を確認するとき。
- reporter／collector の degraded 境界、doctor の可用性検査、または stable event detector を確認するとき。

## Do not read this when
- 観測 payload の永続化仕様や reporter tool の schema だけを確認する場合。
- feedback lifecycle や detector を使わない一般的な logging、Git context 解決、または別の runtime helper を調査する場合。

## hash
- 52e99c67d8ad337f62f769559452b61d9fb64248c1addb602c0ede41ee77bc00

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
- Git repository の状態・worktree・path 分類を担う共通ランタイム境界。Git command の実行とエラー変換、branch・commit・status の取得、managed branch/worktree の作成・検証・削除、snapshot の取得・復元を扱う。
- Git ignore の安全な検証・更新と `.cmoc/gu` の ignore 保証、oracle/realization file の列挙・分類・判定を提供する。symlink、特殊 file、nested repository、Git index/tree fallback など、path の安全性と追跡状態に関する不変条件を一元化している。
- Git 操作、linked worktree、ignore 設定、oracle/realization file 判定、またはそれらを利用する caller の実装を確認・変更するときの共通入口。個別の CLI や state 管理の仕様そのものを読む場合は、各 caller や oracle 仕様を直接確認する。

## Read this when
- Git command の共通実行境界、branch・commit・status の取得、未コミット差分の検査を変更または調査するとき
- cmoc 管理下の branch/worktree の命名、作成、削除、登録検証、symlink 防止を扱うとき
- Codex call 前後の作業成果物 snapshot、復元、filesystem object の安全な読み書きを扱うとき
- `.gitignore`、Git info/exclude、global ignore の検証や `.cmoc/gu` ignore 保証を変更するとき
- oracle file または realization file の列挙・分類・Git 追跡状態判定を変更するとき

## Do not read this when
- Git 境界や oracle/realization の分類に関係しない機能の実装だけを確認するとき
- 個別 command の利用目的や session、branch、path 分類の正本仕様を確認する場合は、まず対応する oracle 文書や caller を直接読むとき

## hash
- 59e010da369c018012b289b2a0b8203c80f6f315e87eda68c94c93f97b74cf59

# `runtime_logging.py`

## Summary
- サブコマンド実行中の logger として、JSON Lines event の記録、warning の集約、step・quota 待機時間の計測、Codex call の取得を担う。ContextVar によって深い runtime helper から現在の logger を参照・差し替えでき、ログ出力後の feedback event 検出もここから起動する。サブコマンドの実行ログ、console summary の timing、runtime feedback detector との接続を確認する際の入口である。

## Read this when
- サブコマンドの event ログ形式、ログファイル生成、flush 済み event の保持を変更・調査するとき。
- step timing、quota 待機時間、warning、Codex call の集計や console summary への入力を確認するとき。
- 現在のサブコマンド logger を ContextVar 経由で runtime helper から利用する処理を調査するとき。
- logger が feedback event detector を起動する条件や detector failure の非致命的な扱いを確認するとき。

## Do not read this when
- サブコマンド固有の業務処理や CLI の引数解釈を調査する場合は、該当するサブコマンド実装を直接読む。
- ログイベントの正本仕様や console 表示仕様を確認する場合は、対応する app specification を直接読む。
- feedback の検出条件・保存処理そのものを調査する場合は、runtime feedback 実装または feedback observation の仕様を直接読む。

## hash
- 2afaa317415da4da8034e74b84d55c6471df24bdaa31771a3ea3411f7248d35a

# `runtime_paths.py`

## Summary
- cmoc の実行時パスを解決・生成する共通機能を提供する。repository/worktree/cmoc の root 解決、session・report・log・schema などの保存先取得、editor/worktree の作業先取得を扱う。
- cwd を一時変更する処理を process-wide に直列化し、timestamp・console timestamp・duration の表示形式を定義する。memo 配下判定や timestamp 付き path の排他的予約も含む。
- runtime path や実行時表示、cwd 切替、session/report/log の保存先を変更・調査する際の共通実装入口である。

## Read this when
- cmoc の repository root、worktree root、cmoc 自身の root の解決動作を確認または変更するとき
- session、report、log、schema、editor input、worktree などの runtime 保存先を確認または変更するとき
- cwd の一時切替、timestamp 付き path の予約、duration の表示形式、memo 配下判定を確認または変更するとき

## Do not read this when
- 個別のサブコマンド処理や report の内容だけを確認し、runtime path の解決・保存先・表示形式に関係しないとき
- root placeholder や runtime directory の契約を変更せず、対象機能の上位仕様または呼び出し側だけを確認するとき

## hash
- 99b11da4723965e801b7f86bb2fac0414612cc394d291d0169d8006956c2b117

# `runtime_primary_report.py`

## Summary
- 非対話サブコマンドの primary report 保存を保証する共通処理。既存 report の検証、未作成時の fallback report 生成、予約済みファイルへの安全な書き込み、保存失敗時の内部エラー化を担う。
- invocation 中に確定した report 項目を ContextVar で保持し、サブコマンド固有の初期値、結果詳細、completion reason、alias を統合して描画入力を組み立てる。

## Read this when
- 非対話サブコマンドの終了経路で primary report を必ず保存・検証する処理を確認するとき。
- fallback report の項目収集、サブコマンド別の初期値や completion reason の補完、保存失敗時の扱いを変更するとき。

## Do not read this when
- primary report の項目定義や描画形式を確認したいときは、primary report の specs・render 実装を直接読む。
- ログ記録、runtime path の生成、terminal result のデータ構造そのものを確認したいときは、それぞれの専用実装を直接読む。

## hash
- 9efef3bfa97c0f61d3f677f5d6e15609ae708fb0e6f21da029a16343c077762e

# `runtime_primary_report_render.py`

## Summary
- 確定済み runtime 情報から、テンプレート別の fallback primary report を構築する描画入口。front matter、通常 summary、oracle review、feedback invocation の本文を選択し、実行段階・終端結果・warning/error・次の操作・関連ログを出力する。
- Codex event、publication event、checkpoint、processing status から oracle edit の agent call 状態や feedback publication・cleanup 状態を判定し、report に表示する補助関数群を含む。

## Read this when
- primary report の描画形式やテンプレート分岐を変更・確認するとき
- terminal classification、TerminalResult、logger の確定情報が report の各節へどう反映されるかを確認するとき
- oracle review または feedback invocation の状態表示、agent call status、publication cleanup status を追跡するとき

## Do not read this when
- runtime のログ記録方法や event の生成責務を確認したいとき
- TerminalResult、PrimaryReportSpec、TerminalClassification の型・生成規則を確認したいとき
- console/file log や各サブコマンドの report 内容の正本仕様を確認したいときは、対象の app_spec を直接読むとき

## hash
- 77c22b878a93f2adbda20d2efcdbcfb9e4532e0ace9fd0045552b5d4b7f416ae

# `runtime_primary_report_specs.py`

## Summary
- 非対話末端サブコマンドに対応する fallback primary report の定義を集約する。コマンド名から保存先、役割、タイトル、必須項目、テンプレートを引く必要がある場合の入口であり、`primary_report_spec` が対応する仕様を返す。doctor、indexing、session 操作、oracle edit/review、realization apply/refactor、run join/abandon、feedback report の report 定義を扱う。

## Read this when
- fallback report の保存先、役割、タイトル、必須 front matter 項目、テンプレートをコマンド別に確認するとき
- `primary_report_spec` の対応コマンドや、登録対象の primary report を変更するとき
- 非対話末端サブコマンドの report 仕様と TUI 通知境界の対象範囲を確認するとき

## Do not read this when
- TUI の通知境界を使う tui や oracle investigation の挙動だけを確認するとき
- report の保存・生成処理そのものを調べるときは、まずその処理を実装する対象を読むとき
- 個別サブコマンドの実行仕様や report 内容の詳細を確認するときは、対応する oracle の仕様書を直接読むとき

## hash
- 860ffcd81816316046475df972b2d7c9da87f9906eea1cb45ff3226806a8d9c3

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
- CLI実行に関する共有結果モデルを定義するモジュール。最外側サブコマンドの終了情報、外部コマンドの入出力、Codex Structured Output の検証問題、Codex exec の生成物とログパスを表すデータ型および呼び出し契約を扱う。実行結果やログ、Structured Output の受け渡し契約を確認・変更するときの入口となる。

## Read this when
- サブコマンドの terminal result や完了理由・次アクション・警告の共有表現を確認するとき
- Codex exec の検証問題、生成された JSON、ログ・出力ファイルの保持契約を確認するとき
- 外部コマンドの終了コードや標準入出力を表す共通結果型の利用箇所を調査するとき

## Do not read this when
- 特定サブコマンド固有の結果内容やレポート形式だけを確認する場合
- console と file log の詳細仕様そのものを確認する場合は、参照コメントに示された正本仕様を直接読むとき
- Codex exec の呼び出し手順や Structured Output の正本ルールだけを確認する場合は、対応する app_spec を直接読むとき

## hash
- 351ca05032b66720e0fd5eedb5be1085eaa4a8f98d16754aab43b35cdce94a83

# `runtime_run.py`

## Summary
- editing run の worktree 解決と process cleanup を同じ run lifecycle 境界として扱う共通 runtime module。branch からの worktree lookup、run state の lock、process tracking、PID・start time・process group の検証、親 run process と Codex child group の fail-closed な停止、tracking file の cleanup を提供する。join/abandon や error cleanup の復旧処理で、同一 lock・tracking file・worktree identity の不変条件を確認する入口となる。

## Read this when
- editing run の join、abandon、error cleanup、worktree 解決、または追跡中 process の停止処理を調べるとき
- run process tracking file、PID 再利用防止、process group の snapshot 検証、停止後の tracking 整理の挙動を確認するとき

## Do not read this when
- 通常の worktree 操作だけを調べる場合は runtime_git の直接の実装を読むとよい
- process identity や Codex subprocess の低レベル操作そのものを変更・確認する場合は runtime_codex_profile を直接読むとよい

## hash
- e1ae36c6e31f7c4e3ebf3a5cad991784081e8d9560adf69d439c8fe52fbfb730

# `runtime_run_lifecycle.py`

## Summary
- 明示的な join を必要とする editing run の lifecycle を一元管理する共通処理。session の準備状態確認から isolated run branch/worktree の作成・公開・復旧、active run の解決、joinable/error への state 遷移、work unit の rollback/commit、INDEX 更新までを扱う。
- Git の変更を rename/copy を含めて分類し、agent・run・session に許可された差分と想定外 path を判定する。oracle file の raw diff、生成 INDEX.md、refactor state の扱いもここで定義する。
- editing run の branch/worktree・state・lifecycle lock にまたがる不変条件を追跡する必要があるため、関連する lifecycle 処理の入口として読む。

## Read this when
- editing run の開始、active run の解決、context 公開後の復旧、state 遷移、worktree の commit/rollback を確認するとき
- run branch と session branch の差分許可範囲、agent が変更可能な realization file、想定外 path の検出を確認するとき
- run lifecycle 中の INDEX 更新、oracle diff、rename/copy を含む変更分類、cleanup 対象の判定を確認するとき

## Do not read this when
- 個別の session state の表現や永続化だけを確認するときは runtime_state の実装を直接読む
- Git branch・worktree・status 操作の低レベル仕様だけを確認するときは runtime_git の実装を直接読む
- editing run の利用者向け外部仕様だけを確認するときは app_spec の editing run 文書を直接読む

## hash
- 67da812593827e07c7e43fa86a43fe1aad440fb85241bccf44b58a468d9aba68

# `runtime_run_report.py`

## Summary
- 対象ファイルは、editing run の fork report と run join/abandon の lifecycle report を、共通の YAML Front Matter、Markdown 本文、実行段階、関連ログ付きで保存する処理を担う。レポートの保存先・タイムスタンプ付きパス予約・終了分類・実行結果項目の組み立て、および変更パスや YAML 値の安全な描画を扱う。レポート生成や run lifecycle の出力形式、または変更パスの Markdown 安全性を確認・変更するときの入口であり、個別の report 出力仕様や canonical 配置の判断は参照先の仕様文書から始める。

## Read this when
- editing run の fork report または run join/abandon の lifecycle report の生成処理を確認・変更するとき
- レポートの YAML Front Matter、Markdown セクション、実行段階、関連ログの共通構造を確認するとき
- Git path や YAML 値をレポートへ安全に描画する処理を確認するとき

## Do not read this when
- レポート本文の個別仕様だけを確認する場合は、参照先として示された editing run の正本仕様を先に読む
- 共通処理の配置や CLI 実装責務だけを判断する場合は、canonical な設計ルールを先に読む
- 実行ログの収集機構や run lifecycle の状態管理そのものを変更する場合は、それぞれの担当モジュールを直接読む

## hash
- 035a933571e86ee1771aa202a9a5d1636e59a567e650251bdb315a590306c38c

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
