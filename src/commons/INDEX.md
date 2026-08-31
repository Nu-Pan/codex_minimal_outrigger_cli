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
- INDEX.md の検査・生成・更新・commit までを一貫して担う indexing lifecycle の共通実装。directory traversal、entry の再利用・生成、hash による鮮度判定、更新前 snapshot への復元、排他 lock、Git commit を扱い、INDEX 更新処理の実装入口となる。

## Read this when
- INDEX.md の preflight、深さ順更新、entry の生成・再利用、hash 検証、更新失敗時の復元、または indexing commit の挙動を変更・調査するとき。
- INDEX.md の対象 directory・child の除外条件、symlink や特殊 file の扱い、Codex 呼び出し時の並列性・実行 context を確認するとき。

## Do not read this when
- INDEX.md entry の生成 prompt parameter や Structured Output schema 自体を確認したいときは、index_entry の builder または schema 定義を直接読む。
- Codex の preflight、process tracking、Git pathspec、runtime path の個別仕様だけを確認したいときは、対応する runtime 実装または正本仕様を直接読む。

## hash
- 4d76cecb438382386aacd46f0d7c9dc5e22cf5260b4203438d75e57174039496

# `prompt_editor_input.py`

## Summary
- AI Agent 用 prompt のエディタ入力を受け付ける共通境界。作業用ファイルと保存用ログの確保、エディタ起動、入力の一度限りの収集・抽出、完了後の作業ファイル削除を扱う。
- prompt editor の作業ルートに必要な `.cmoc` ignore の保証も担う。

## Read this when
- prompt editor input の予約からエディタ起動、入力収集、保存、後片付けまでのライフサイクルを確認するとき
- エディタ選択、original prompt placeholder の検証、HTML comment と前後空白の除去、編集ファイルの妥当性検証の責務を確認するとき
- prompt editor input を利用する CLI や TUI の共通境界を変更・調査するとき

## Do not read this when
- prompt の初期表示内容や skeleton の構築規則を確認したいときは、prompt builder の対象を直接読む
- editor handoff の通信・drain・無効化の内部仕様を確認したいときは、runtime editor input handoff の対象を直接読む
- エラー型、Git ignore 実装、パス生成、timestamp の詳細を確認したいときは、それぞれの runtime helper を直接読む

## hash
- a699ab42a10395da76d252741020bf4b989721f53e0b7159f0759fe3df10bcfc

# `runtime_cli.py`

## Summary
- 最外側 CLI サブコマンドの実行ライフサイクルを統括する。doctor 前処理、work root 検査、進行通知、feedback invocation、診断ログ、primary report、terminal result、終了コード、Windows 通知を連携する。
- 正常終了、ユーザー中断、handled/internal failure を分類し、それぞれのエラー情報・次の操作・警告・経過時間・診断ログを console と command_finished イベントへ反映する。
- サブコマンド実装から呼び出す step 記録、中断状態・TUI 起動状態の印付け、terminal result の安全な通知、値の表示・記録変換を提供する。

## Read this when
- 最外側 CLI サブコマンドの実行順序、終了処理、終了コード、例外処理を変更または確認するとき
- 診断用サブコマンドログ、feedback observation、primary report、terminal result の統合を変更または確認するとき
- ユーザー中断、TUI プロセス起動後の KeyboardInterrupt、Windows terminal 通知の境界を変更または確認するとき
- サブコマンドの step 進行通知や work root 実行条件を変更または確認するとき

## Do not read this when
- 個別の doctor 前処理、feedback 保存、logging、primary report 保存、TerminalResult の定義や通知実装そのものを直接確認すれば足りるとき
- 個別サブコマンドの業務処理や引数定義だけを変更または確認するとき

## hash
- fd802b8e31167a5741d279a40eb036ccd4b8c682a915e5e728f04834a1cf15c8

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
- 1 回の Codex agent call における exec 実行制御の中心。Structured Output の検証・補正、capacity retry、quota 回復待ちと代表 probe、resume 継続、実行ログおよび subcommand event の記録を共有状態で統合する。

## Read this when
- Codex exec の再試行、quota 待機・回復、Structured Output の schema／事後条件検証や補正、resume session の扱いを確認・変更するとき。
- Codex subprocess の prompt・stdout・stderr・output・call log の保存や、実行結果および診断 event の記録経路を追うとき。

## Do not read this when
- TUI の起動や表示制御だけを確認・変更するとき。
- Codex subprocess の環境、schema 準備、エラー分類など個別の補助処理だけを確認し、exec の再試行・検証・ログ連携を扱わないとき。

## hash
- 6b06256429db8ed183e22ed0aba5bcde099e77a232f92803bf7ea9a0fb9b94bf

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
- Codex CLI subprocess の起動境界を担当し、sandbox、argv、環境変数、CODEX_HOME、schema 配置を構成する。
- Codex subprocess の process tracking、PID reuse を考慮した process group の停止、stdout の JSONL error・resume token・capacity/quota 判定を扱う。
- Codex CLI の実行環境と機械的な実行結果を解釈するための、呼び出し側から利用する境界入口である。

## Read this when
- Codex CLI の sandbox、model/provider、MCP、hook、notification を含む invocation-local argv を構成または確認するとき。
- CODEX_HOME や subprocess 環境の継承・除外、schema の hash store 配置、Codex CLI 不在時の実行時エラーを確認するとき。
- editing run の Codex child tracking、process group の安全な停止、PID reuse 対策を変更または調査するとき。
- Codex JSONL の malformed event、error、capacity/quota、resume token の判定や復旧分岐を確認するとき。

## Do not read this when
- Codex CLI 境界の外側にある agent call の業務フロー、prompt 内容、oracle/realization の仕様だけを確認したいとき。
- Codex の実行結果ではなく、cmoc の一般的な設定値の定義や runtime path・content の実装を直接確認する場合。
- Codex subprocess を起動せず、既存のテストや仕様書の内容だけを確認する場合。

## hash
- d3b25d89af852458219a3d5125022399df8a18746e1726ace5ebe8237004c313

# `runtime_codex_tui.py`

## Summary
- Codex TUI を設定上書き argv、作業ディレクトリ、検証済み環境変数とともに起動する実行ラッパー。
- 呼び出しごとの call log、フィードバック連携、通知フック、成功・失敗イベント、サブプロセス異常の処理を担う。

## Read this when
- Codex TUI の起動引数や実行環境を組み立てる処理を確認するとき。
- Codex 呼び出しの call log、実行時間、return code、成功・失敗イベントの記録経路を調べるとき。
- Codex CLI/TUI の起動失敗や subprocess の失敗がどのように例外化されるかを確認するとき。
- TUI 通知フック、editor input handoff、feedback call の実行時連携を追うとき。

## Do not read this when
- Codex CLI の設定値やプロファイル解決そのものを調べる場合は、対応する runtime_codex_profile 実装を直接読むとき。
- Windows 通知の具体的な生成・終了処理を調べる場合は、runtime_windows_toast 実装を直接読むとき。
- フィードバックの保存形式や識別子生成の詳細を調べる場合は、runtime_feedback_store などの下位実装を直接読むとき。
- Codex TUI の呼び出し経路を扱わず、一般的なサブコマンドのログや設定読込だけを調べるとき。

## hash
- 926736ab4e7fc5704331236c2ffb5513e530902f883e6fa242b276144ecbfa01

# `runtime_config.py`

## Summary
- 設定オブジェクトを JSON として永続化・復元し、Codex provider／agent call と oracle review の設定値を検証するランタイム設定境界。
- 設定ファイルの読み書き、既定値補完、型・値・循環構造・symlink・特殊ファイルの検査、および利用者向け CmocError への変換を担う。

## Read this when
- cmoc の設定 JSON の保存形式や復元時の既定値補完を確認するとき。
- Codex model provider、agent call、reasoning effort、oracle review loop の入力検証や設定エラーの扱いを変更・調査するとき。
- config ファイルの symlink、通常ファイル判定、JSON/TOML 互換値、読み書きの安全境界を確認するとき。

## Do not read this when
- Codex の設定型そのものや既定値の定義を確認したい場合は、参照先の正本設定型を直接読むとき。
- CLI のコマンド処理、agent call の実行、oracle review のロジックを調べる場合は、それぞれの実装入口を直接読むとき。
- 設定 JSON の具体的な利用箇所だけを確認する場合は、設定を呼び出す実装またはテストを直接読むとき。

## hash
- e49e094dfcfbed4f835910da9addc64ab91da1b60cd43d238abe84a161658b0b

# `runtime_content.py`

## Summary
- 対象ファイルは、通常ファイルまたはシンボリックリンクの内容を SHA-256 でハッシュ化する処理と、UTF-8 文字列のハッシュ化を提供する。さらに、内容ハッシュをファイル名に含めた出力ファイルを一時ファイル経由で安全に保存し、先頭チャンクの NUL byte と読み取り可否でバイナリファイルを粗く判定する。
- ハッシュ値に基づくファイル保存、ファイル種別の粗い判定、または regular file と symlink の内容取得規則を確認・変更するときの実装入口である。

## Read this when
- ファイル内容・文字列の SHA-256 計算を使う処理を調査または変更するとき
- 内容ハッシュ付きファイルの作成、既存同一内容ファイルの再利用、一時ファイルからの置換保存を確認するとき
- regular file と symlink のハッシュ対象、またはバイナリ判定の挙動を確認するとき

## Do not read this when
- ハッシュ化やハッシュ名付き保存の具体的な実装を扱わず、呼び出し側の同期・列挙規則だけを確認するときは、対応する仕様または呼び出し側へ直接進む
- 出力スキーマや CLI の一般的な実行規則だけを確認するとき

## hash
- ee0348e76dcc63e9049ce53594a5bcd34ef47aa665fe1567dcd6bb8062d92018

# `runtime_doctor.py`

## Summary
- doctor preprocess の修復処理と、その排他実行から修復 commit・元の Git index 復元までの lifecycle を扱う。current/main worktree の config・refactor state・.gitignore・.agents の同期、および一時 index による利用者の既存差分との分離を確認するための入口である。

## Read this when
- doctor preprocess の修復、Git common directory 単位の doctor lock、修復差分だけの commit を調査するとき。
- 一時 index の退避・合成・復元、失敗時の index 復元、既存 staged/unstaged 差分の保持を確認するとき。
- config・refactor state・.gitignore・.agents の doctor 同期や、追跡状態の検証を確認するとき。

## Do not read this when
- doctor preprocess の正本仕様だけを確認する場合は、doctor_preprocess.md を直接読む。
- config または refactor state の個別同期ロジックだけを確認する場合は、対応する runtime_config.py または runtime_refactor.py を直接読む。
- Git 共通処理、パス解決、エラー処理、feedback reporter の個別仕様だけを確認する場合は、対応する runtime_* ファイルを直接読む。

## hash
- 134306bb5efc707045ace71a3d0639f1d447d3a00329773c9b03aa351c189f91

# `runtime_editor_input_handoff.py`

## Summary
- editor 待機中に一時的な editor work file へ入力を IPC 経由で上書きする処理を確認するとき
- handoff target の開始・終了、Unix socket 通信、request 検証、submission の直列化を調べるとき
- editor work file の regular file・非 symlink・所定ディレクトリ内という安全性検証や UTF-8 上書き処理を確認するとき

## Read this when
- editor 待機中の入力 handoff の実装や、target のライフサイクルを変更・調査するとき
- Unix socket 経由の submission 受付、repository・protocol・target の検証、受付結果の扱いを確認するとき
- editor work file の安全な再検証と内容置換の挙動を確認するとき

## Do not read this when
- editor input handoff の protocol version や payload schema の定義だけを確認したいとき
- editor work directory や socket path の算出規則だけを確認したいとき
- editor の起動・待機処理、または handoff 以外の runtime error 処理を確認するとき

## hash
- 296d8647d0f6f864963ec55203aa6a97d2e3a6afa035c421a11d56a07e0013e2

# `runtime_editor_input_handoff_mcp.py`

## Summary
- Codex TUI の active な prompt editor input file 全体置換を受け付ける stdio MCP server。
- MCP JSON-RPC の初期化・疎通確認・tool 列挙・overwrite 呼び出しを処理し、同一 repository の active target へ Unix socket 経由で転送する。
- 入力検証、target 応答検証、転送失敗の domain result を MCP の structuredContent と text で返す入口。

## Read this when
- editor input handoff を agent-facing MCP tool として起動・接続・呼び出しする処理を確認するとき
- overwrite tool の MCP 公開情報、JSON-RPC message の処理、target への転送結果と失敗コードの境界を確認するとき

## Do not read this when
- overwrite payload の schema、socket path、handoff response の詳細なプロトコル定義を確認したいときは、参照される protocol module を直接読む
- Codex TUI 側の editor input file 更新処理や active target の実装を確認したいとき

## hash
- a4bc2632f4628546168371b741912abf2a7ec677458c02efe2810d0470373cde

# `runtime_editor_input_handoff_protocol.py`

## Summary
- editor input handoff の共有 schema 読み込み、環境変数による repository context の引き渡し、短い socket path の導出、newline-framed response の受信を定義する共通モジュール。
- overwrite input の正本 schema を読み込み、validator を構築し、payload の適合性だけを判定する処理への入口。

## Read this when
- editor input handoff の schema 検証、MCP subprocess への repository context 追加、handoff socket path の生成、または socket response の受信処理を確認するとき。
- 複数の editor input handoff 実装が共有する protocol version、環境変数、response size limit などの共通定義を確認するとき。

## Do not read this when
- overwrite input schema のプロパティや制約そのものを確認したいとき。正本の oracle package resource を直接確認する。
- 特定の editor input handoff 呼び出し元の業務処理や、個別 MCP client/server の接続手順だけを確認したいとき。

## hash
- ca5ef865f63fd20f1a75edb959817dd7fd99882d9cc9ea4268da8823c234c1dd

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
- Git subprocess、branch、linked worktree、path 安全性、Git ignore、oracle/realization file の列挙・分類を担う共通境界。
- Git repository の状態確認と path 正規化を集約し、worktree 操作や file 分類で共有される安全性・追跡状態の不変条件を一箇所で検証する。
- 同階層の個別機能ではなく、Git 状態または repository path の所有・ignore・oracle/realization 分類を扱う実装から参照する。

## Read this when
- Git command の実行結果を cmoc のエラーへ変換する処理を確認するとき。
- branch の判定、run 用 linked worktree の作成・削除、管理対象検証、commit や status の取得を確認するとき。
- symlink、特殊 file、path traversal、managed worktree path など、filesystem と Git metadata の安全性検証を確認するとき。
- Git ignore の更新・検査、候補 file の一括 ignore 判定、oracle/realization file の列挙または分類を確認するとき。

## Do not read this when
- Git 状態や repository path の所有・分類に関係しない CLI の個別処理を確認するとき。
- oracle または realization の具体的な仕様内容を確認するときは、対応する oracle または realization file を直接読む。
- worktree の利用側における session state や command orchestration の挙動だけを確認するときは、対応する caller と仕様を直接読む。

## hash
- adebf2a2bea7594efce925188ad0605fbb6e7230433e6a57ec302d3e2124dfab

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
- 対象は cmoc の実行時に必要な repository root・worktree root・cmoc root の解決、時刻・経過時間の整形、session/report/log/schema/editor/worktree などの保存先 path 取得、cwd 切替の直列化を担う共通 runtime path ユーティリティ。root 解決や runtime 保存先、時刻・duration 表示、pushd による process-wide な cwd 制御の挙動を確認・変更するときの入口となる。

## Read this when
- repository・worktree・cmoc の root 解決、または root 起点の path 解決を調査・変更するとき
- session、report、log、schema、editor input、worktree など cmoc の runtime 保存先を調査・変更するとき
- timestamp、console timestamp、duration の表示形式や予約処理を調査・変更するとき
- pushd や cwd override の thread-safe な process-wide cwd 制御を調査・変更するとき

## Do not read this when
- 個別の runtime error の文言や例外契約だけを確認する場合は runtime_errors.py を直接読むとよい
- root placeholder の定義や実パス解決の詳細だけを確認する場合は basic.path_model の定義を直接読むとよい
- 各保存先に記録される session・report・log・schema の内容や subcommand 固有の仕様を確認する場合は、それぞれの app specification または利用側実装を直接読むとよい

## hash
- 36fc5e6fe26b8c7d3a2dc82bc79bf43d1fb5d97765db55f07bf6ec80faa92277

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
- realization refactor の state を管理する実装であり、state file の読み込み・schema 検証・保存・oracle/realization file 集合との同期を担う。
- 未調査対象の初期化、調査対象の優先選択、全対象の再調査要求化を提供する。
- state path の symlink や非通常ファイルを拒否し、相対 path、調査結果、SHA256、調査日時を検証して不正状態を CmocError に変換する。

## Read this when
- realization refactor の state を読み込み、保存、検証、同期する処理を確認するとき
- oracle/realization file の列挙結果から調査対象を選ぶ処理や、調査履歴の再調査要否を確認するとき
- state path の安全性や state 内容の入力検証、利用者向けエラー変換を確認するとき

## Do not read this when
- refactor state、oracle/realization file の列挙、調査対象選択、または state の検証に関係しない処理だけを確認するとき
- state の具体的な field、型、JSON 形式だけを確認する場合は、対象実装を直接読むとき

## hash
- 59291ea72c1b2056cb2a9ac596ca072e96b6fb1b35b894d91b36f33de10e6c87

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
- editing run の worktree 解決と process cleanup を束ねる共通 runtime 境界。run state の lock、tracking file、worktree identity を共有する join/abandon 復旧処理の入口であり、worktree lookup と process 停止を一体として確認するための対象。

## Read this when
- editing run の join または abandon における復旧処理を確認するとき
- branch から安全な run worktree を解決する処理を確認するとき
- run process と Codex child process group の tracking、同一性検証、停止、cleanup を確認するとき

## Do not read this when
- Git worktree 操作の低レベル実装だけを確認する場合
- pidfd、process group、process signal など個別の process 操作プリミティブだけを確認する場合
- editing run の外部仕様や fail-closed 方針そのものを確認する場合

## hash
- e70fc9aa7b1834e8dcefa5cac37842db71d1ad4c6e34ff8aec856645028a5754

# `runtime_run_lifecycle.py`

## Summary
- editing run のライフサイクルを一元管理する共通実装。session の事前条件検査、run branch/worktree の作成・公開・回収、active run の解決、state 遷移、process tracking、rollback/commit を扱う。
- run worktree の INDEX 更新と commit、Git tree 差分の列挙・平坦化、agent・run・session ごとの想定外 path 検査、oracle diff、generated INDEX・refactor state の許可判定を提供する。
- realization_apply と realization_refactor の workload が共有する lifecycle 境界の入口であり、各 workload 固有の編集処理や state schema の定義そのものは扱わない。

## Read this when
- editing run の開始、joinable/error 遷移、cleanup、recovery の挙動を確認するとき
- session branch・run branch・run worktree の対応や fork commit の不変条件を追跡するとき
- workload 差分、oracle 差分、INDEX 更新、想定外 path の分類・許可範囲を確認するとき

## Do not read this when
- workload 固有の realization 編集処理を確認するときは、対応する realization 実装を直接読む
- state のデータ構造や永続化形式を確認するときは、runtime_state.py を直接読む
- Git 操作の低レベル実装を確認するときは、runtime_git.py を直接読む
- INDEX 生成アルゴリズム自体を確認するときは、indexing.py または対応する仕様を直接読む

## hash
- 8c8b1600e08046fb1a53d73bd49e9318dfe8211e01208d2e12fc8d6921ce6763

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
- Windows toast 通知と Codex TUI callback の transport 境界を提供する。
- 最外側サブコマンドの terminal result 通知、root session の記録、turn callback の重複排除と入力待ち通知を扱う。
- 通知処理や callback state の失敗を本命処理へ伝播させない非致命的な入口である。

## Read this when
- Windows toast の通知内容、PowerShell transport、または通知の失敗隔離を確認するとき。
- Codex TUI の SessionStart と agent-turn-complete callback の紐付け、root session 判定、turn 重複排除を調べるとき。
- 通知 callback の生成・終了処理や repository 識別子の短縮化を確認するとき。

## Do not read this when
- 通常のコマンド実行結果や TUI の本命処理そのものを調べるとき。
- 通知仕様の正本や Codex hook の外部契約を確認する必要があり、この実装の境界では足りないとき。
- 通知を使わない CLI 機能や、callback state と無関係な一時ファイル処理を変更するとき。

## hash
- 2efbe0e8881fd50469f78d3cd87bdd8827465cd56493851394b4c94ceab522ff
