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
- 複数の実行経路で共有する cmoc runtime API の公開窓口。
- CLI、Codex 実行、設定、Git、ログ、パス、結果、状態など、各 runtime サブモジュールの公開要素をまとめて利用する入口。

## Read this when
- 複数の実行経路から共有 runtime API を利用・追加・確認するとき。
- runtime サブモジュールを横断して公開される関数、型、定数の入口を確認するとき。

## Do not read this when
- 特定の runtime サブモジュールの内部実装や個別挙動を調査するとき。
- CLI、設定、Git、Codex 実行、ログ、パス、状態などの具体的な責務を直接確認する場合。

## hash
- 2282038ccfafc69ddc768e194cb1fbd33abaf42e4e7d481c102882236996ac05

# `indexing.py`

## Summary
- INDEX.md の検査・生成・更新・復元・commit を担う indexing lifecycle の共通実装です。
- directory traversal、既存 entry の hash による再利用判定、不足 entry の Codex 生成、深さ順の INDEX.md 更新を一体で扱います。
- INDEX.md の snapshot 復元、symlink・特殊 file・binary file の扱い、index 対象 hash の計算、entry の render と形式検証を提供します。

## Read this when
- INDEX.md の preflight 更新や indexing 用 lock、更新差分の commit 動作を変更・調査するとき。
- directory ごとの INDEX.md entry の再利用条件、生成対象の列挙、深さ順更新、並列 Codex 呼び出しを確認するとき。
- INDEX.md の hash 鮮度判定、既存 entry の形式検証、ファイル種別ごとの復元・書き込み挙動を確認するとき。

## Do not read this when
- INDEX.md entry の生成 parameter や Structured Output の定義だけを確認したいときは、index entry builder 側を直接読む。
- Codex subprocess の preflight、profile、isolation など個別の実行制御だけを調べるときは、対応する runtime 実装を直接読む。
- INDEX.md の正本仕様や利用者向けの indexing ルールを確認したいときは、仕様文書を直接読む。

## hash
- 7eb8d50ee98b933ab01d70d2e3eb16b9bacc05edb8b32c8f7285bb176cce83b8

# `prompt_editor_input.py`

## Summary
- エディタ入力の共通ライフサイクルを担い、作業ファイルと保存コピーの予約、利用可能なエディタの起動、handoff を含む入力確定、保存、抽出、完了後の削除を提供する。
- TUI と oracle 系サブコマンドが共有する入力境界として、パス検証、symlink 防止、保存先の限定、editor root の `.cmoc` ignore 保証も扱う。

## Read this when
- TUI または oracle edit・investigation のエディタ入力処理を追跡するとき。
- editor work file の予約、エディタ選択、handoff 起動、最終読み取り、入力保存、プロンプト抽出、作業ファイル削除の挙動を確認・変更するとき。
- editor input の保存先検証、symlink 対策、保存コピーの path 制約、`.cmoc` ignore 保証を確認するとき。

## Do not read this when
- サブコマンド固有の完全 prompt 構築や起動パラメータの仕様を確認したいときは、各サブコマンドの builder または正本仕様を先に読む。
- handoff target の生成・通信・ガイド内容の詳細だけを確認したいときは、runtime の handoff 実装または handoff 正本仕様を直接読む。
- エディタ入力を利用する呼び出し元の処理順序だけを確認したいときは、TUI または oracle サブコマンド実装を直接読む。

## hash
- 4284e8dbedca6c2cd5e537f7cd5dc50fc7719fe2096a6a918ac16af2b019662e

# `runtime_cli.py`

## Summary
- 最外側 CLI サブコマンドの実行ライフサイクルを統括し、診断ログ、feedback、primary report、terminal result、終了コード、通知、例外・中断処理を一貫して確定する実行境界。
- サブコマンドの開始前処理、step 進行、正常終了・ユーザー中断・エラーの分類、および terminal result のコンソール／ログ出力を確認するための入口。

## Read this when
- 最外側サブコマンドの起動から終端までの制御フローを追うとき。
- KeyboardInterrupt、実装例外、非ゼロ戻り値、TUI 起動前後の中断がどのように扱われるか確認するとき。
- 診断ログ、feedback collector、primary report、Windows 通知、terminal result の確定順序や失敗時のフォールバックを変更・調査するとき。
- サブコマンド step の記録、work root 検査、終了結果の Markdown／JSON 表現を確認するとき。

## Do not read this when
- 個別のエラー型、feedback の収集実装、primary report の保存実装、ログの詳細実装、通知実装そのものを直接調べるとき。
- 特定サブコマンドの業務ロジックや CLI 引数定義だけを確認するとき。
- terminal result のデータ型や固有のエラー文言だけを確認する場合は、それぞれの定義元を直接読むとき。

## hash
- e6438f5a8ca342c6f004fcf777e8cc289634e8b22ead2a9b6a2016cfd255c94a

# `runtime_codex.py`

## Summary
- Codex exec と TUI の実行 API を公開する commons の入口。

## Read this when
- Codex exec または TUI の実行 API を利用・変更する入口を確認するとき。

## Do not read this when
- Codex exec／TUI の個別実装や、実行 API を使わない commons 配下の処理を直接確認したいとき。

## hash
- cc80041004f69b74468dbd703e186f058a367b85f21904b0b419d3a38cd687c2

# `runtime_codex_exec.py`

## Summary
- Codex exec の subprocess 実行を中心に、capacity retry、quota 回復待ちと代表 probe、resume 継続、Structured Output の検証・補正、call log と subcommand event の記録を一つの状態機械として制御する実装。
- Structured Output の schema・JSON parse・宣言済み事後条件を検証し、補正 turn で成果物変更を検出・復元しながら、最終的な CodexExecResult または診断可能な CmocError を返す処理の入口。

## Read this when
- Codex exec の retry、quota 待機・probe、resume、Structured Output 補正、成果物不変性、実行ログやイベント記録の挙動を確認または変更するとき。
- Codex の subprocess argv、prompt/output/call log の生成、session ID の扱い、structured output 検証失敗時の診断経路を追うとき。

## Do not read this when
- TUI 起動や exec 以外のサブコマンド実装を確認したいとき。
- Codex subprocess の個別エラー分類、設定・環境解決、schema 準備、output JSON 読み取りの単独仕様だけを確認したいときは、対応する runtime_codex_profile などの補助 module を先に読む。

## hash
- 2f53955269033d64eb92b5d498316132559a84e98e517c086c95047603301bf8

# `runtime_codex_logging.py`

## Summary
- Codex 呼び出し失敗を console と event で共有できるエラーテキストへ変換する共通処理。
- CmocError は要約と詳細を組み合わせ、その他の例外は文字列表現へフォールバックする。

## Read this when
- Codex 呼び出し失敗時に表示・記録するエラーテキストの変換規則を確認するとき。
- CmocError と一般例外で異なるエラー表現を確認するとき。

## Do not read this when
- CmocError の定義や分類を確認したいときは、runtime_errors の定義を直接読む。
- console や event のログ仕様、または呼び出し側の処理経路を確認したいとき。

## hash
- 3aa3362456bf077cfb72f5407ab784e4f4d46eff44fb6df4722e2fb2f92d0586

# `runtime_codex_preflight.py`

## Summary
- Codex exec／TUI 実行前に INDEX 更新 preflight を挟む実行境界。preflight の登録・解除、再入抑止、直列化、実行起点 root の決定、本体ランナーへの委譲を扱う。

## Read this when
- Codex 実行前の INDEX 更新処理を登録・解除・統合するとき。
- Codex exec／TUI 呼び出しの preflight 境界、再入制御、並行実行時の直列化を確認するとき。
- preflight が作成した管理 commit と本命 workload の境界通知を確認するとき。

## Do not read this when
- INDEX 更新そのものの探索・生成規則を確認したいとき。
- Codex 実行本体の subprocess 挙動や結果型を直接調べるときは、委譲先の runtime 実装や結果定義を読む。
- Codex 呼び出し設定や work root のパスモデルだけを確認したいとき。

## hash
- ea72c61aa6a3ec3477625e6e39c0cc470f0b56a61209f2d456784eea2045ba15

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界を担当し、file access の sandbox 変換、TOML/config override、provider・MCP・hook 設定、CODEX_HOME と schema 配置、環境構築、subprocess 実行をまとめて扱う。
- editing run 向けに process group の同一性検証、pidfd による安全な signal、tracking file のロック・登録・cleanup を提供する。
- Codex の JSONL/stdout/stderr を解析し、出力 JSON、resume token、capacity/quota/unexpected error を呼出し側が判定できる形へ変換する。

## Read this when
- Codex CLI に渡す sandbox・環境変数・config override・schema・MCP/hook 設定の生成または変更を調べるとき。
- Codex subprocess の起動、process group tracking、abandon 時の停止、PID reuse 対策、tracking file の扱いを調べるとき。
- Codex の JSONL 出力や終了時エラー、resume token、capacity/quota retry 判定の実装を確認するとき。

## Do not read this when
- Codex の上位コマンドフローや run lifecycle の方針だけを確認したい場合は、呼出し側の runtime_run・runtime_run_lifecycle を直接読む。
- Codex TUI 固有の通知・表示制御だけを確認したい場合は runtime_codex_tui を直接読む。
- 設定ファイルの正本仕様や Codex CLI の一般仕様を確認したい場合は oracle 文書または外部 CLI 仕様を先に読む。

## hash
- 0c928eeb004c40d69520732734e8b536223b9a3fd02a2ae22e24eb55e12321d9

# `runtime_codex_tui.py`

## Summary
- Codex TUI の実行 API と、その起動前設定・環境準備・通知フック設定を担う。
- Codex CLI を単一プロセスとして起動し、呼び出し情報を call log に記録し、フィードバック連携、エディター入力引き渡し、終了結果・失敗情報をサブコマンドログへ反映する。
- TUI の起動条件、Codex ホームやモデル設定の検証、バージョンに応じた通知フック、戻り値と例外の扱いを確認するための共通ランタイム入口である。

## Read this when
- Codex TUI の起動引数、作業ディレクトリ、設定上書き、環境変数、通知フックを変更・調査するとき。
- TUI 呼び出しの call log、フィードバック呼び出し、エディター入力引き渡し、成功・失敗時のログや例外処理を確認するとき。
- `runtime_codex.py` から公開される `run_codex_tui` の実行経路を追い、関連テストの挙動を確認するとき。

## Do not read this when
- Codex exec のみの実装を確認する場合は、`runtime_codex_exec.py` を直接読む。
- 画面表示や個別ウィジェットの挙動、Windows 通知の具体的実装だけを調査する場合は、それぞれの UI・通知モジュールを直接読む。
- Codex の設定値やプロファイル解決の詳細だけを確認する場合は、`runtime_codex_profile.py` と設定定義を直接読む。

## hash
- 484ec3d3df272bc8fac044d36fa032c05aef5351ee5bf6e8e97142d097b8ae40

# `runtime_config.py`

## Summary
- 設定値を JSON/TOML の安全な永続化形式へ検証・変換し、正本の cmoc 設定型との相互変換を担う実装。
- 設定ファイルの読み込み・書き込み・同期を通じて、既定値補完、JSON 構文エラー、型不正、symlink や特殊ファイルの拒否を利用者向けエラー境界として扱う。

## Read this when
- cmoc 設定の JSON 表現、model provider や agent call の検証・復元、既定値補完の挙動を確認または変更するとき。
- config.json の生成・読み込み・同期、設定ファイルのパス安全性や不正入力時のエラー処理を確認または変更するとき。

## Do not read this when
- 設定型そのもののフィールド定義や既定値を確認したい場合は、まず設定モデル定義を読むとよい。
- CLI の個別コマンドや実行処理の挙動だけを確認する場合で、設定の永続化・読み込み境界に関係しないとき。

## hash
- 051dcb5a07d96c2e41ef049286df1e4f4eb077030364608b282482b3aa4b1196

# `runtime_content.py`

## Summary
- ファイル内容と文字列の SHA-256 hash を計算し、hash を含む名前で内容を保存する共通処理を提供する。
- symlink の扱いを含む内容 hash と、先頭データおよび読み取り可否に基づく粗い binary 判定への入口となる。

## Read this when
- state 同期対象などのファイル内容を識別したいとき。
- 内容 hash を名前に含むファイルを安全に保存する処理を確認したいとき。
- 対象ファイルを text と binary のどちらとして扱うかの判定処理を確認したいとき。

## Do not read this when
- 特定の caller における state 同期や schema store の全体仕様を確認したいとき。
- 個別の CLI や上位処理の責務を確認したいとき。
- hash 値を利用する具体的な機能の実装を直接確認したいとき。

## hash
- 655ad0b996b073ecc238dbb4e924f6d0e8137ef4dbec086d3f7dcc9b36b4d7df

# `runtime_doctor.py`

## Summary
- doctor preprocess 全体の排他実行と修復 commit lifecycle を扱う境界。
- Git common directory の doctor lock を起点に、current/main worktree の修復対象同期、一時 index の退避・合成・復元、修復差分の commit を追跡する入口。
- .gitignore と .agents の追跡保証、および config・refactor state の同期と既存差分を保った commit 分離を確認する対象。

## Read this when
- doctor preprocess の失敗時を含む index 復元、並行実行の排他、または修復 commit の対象範囲を確認するとき。
- current worktree と main worktree の修復責務や、runtime state の同期を含む doctor の処理順序を調べるとき。
- 一時 Git index を使った staged 状態の保持、修復差分の合成、commit 後の元 index 復元を変更・検証するとき.

## Do not read this when
- config の同期仕様だけを確認したい場合は runtime config の個別実装・仕様を読むとき。
- refactor state の同期仕様だけを確認したい場合は runtime refactor の個別実装・仕様を読むとき。
- doctor preprocess を経由しない通常の Git index 操作や commit の一般的な手順を調べるとき。

## hash
- 47aa1a6d33f394de15f116746c342bff525e8b83b47332f7c35bf14b27b0498d

# `runtime_editor_input_handoff.py`

## Summary
- editor work file に対応する一時的な editor input handoff target を管理する実行時モジュール。
- 認証付き loopback IPC の開始・受付・終了、target ID による要求検証、handoff ガイド取得、検証済みファイルへの UTF-8 全面上書きを担当する。
- editor work file とガイドの regular file・配置・symlink 境界を再検証し、受付済み submission の完了後に target とガイドを破棄する。
- protocol の定数・target ID の構築や認証方式そのものは protocol モジュール、agent-facing MCP の schema と公開 tool は MCP モジュール、ガイド本文の生成は oracle 側 guide モジュールへ進む。

## Read this when
- editor input handoff の target lifecycle、loopback IPC、要求受付、ガイド取得、または editor work file の handoff 上書き処理を確認・変更するとき。
- handoff 対象のパス検証、symlink 防止、repository・target ID の照合、終了時の cleanup を調べるとき。
- prompt editor 待機中に handoff target を開始する呼び出し経路から、実際の runtime 処理へ追跡するとき。

## Do not read this when
- handoff protocol の定数・認証・target ID 形式だけを確認したい場合は runtime_editor_input_handoff_protocol.py を直接読む。
- MCP tool の入力 schema、送信元情報、または agent-facing の公開処理だけを確認したい場合は runtime_editor_input_handoff_mcp.py と対応する oracle schema を直接読む。
- handoff ガイドや上書き本文の正本フォーマットを確認したい場合は oracle/editor_input_handoff 配下を直接読む。
- prompt editor の起動順序や最終入力確定処理だけを確認したい場合は、その lifecycle を担当する subcommand・prompt editor 実装を直接読む。

## hash
- 87e4f7bbfb5df163c6d96e59e5e73ddcc9f63b5f9c9be8f59097558ff3ca01c2

# `runtime_editor_input_handoff_mcp.py`

## Summary
- Codex TUI向けのstdio MCPサーバーとして、JSON-RPCのinitialize・ping・tools/list・tools/callを処理し、activeなeditor input targetへのガイド取得と入力全体の上書きを仲介する。
- 入力schema検証、repositoryとtargetの照合、起動時コンテキストに基づく送信元の付与、認証済みTCP handoff、応答のdomain結果化を一体で確認したい場合の入口である。

## Read this when
- Codex TUIのeditor input handoff MCPが提供するツール、JSON-RPC応答、targetへの認証付き通信、またはガイド取得・上書き結果の扱いを調べるとき。
- active targetへのhandoffが失敗・不明結果になる条件や、入力本文の生成から送信までの境界を確認するとき。

## Do not read this when
- editor input handoffの通信 protocol、payload schema、target側listenerの実装を直接確認したいときは、対応するprotocol定義やtarget実装を先に読む。
- MCP handoffを使わない一般的なJSON-RPC処理、Codex TUIの起動制御、入力本文の正本生成規則だけを調べるとき。

## hash
- 9f2add3e38e2d306ff499ae271e5f5d7624273e4f742f1862921fc347f00170f

# `runtime_editor_input_handoff_protocol.py`

## Summary
- エディタ入力ハンドオフの共有プロトコル層として、正本 schema の読み込み・payload 検証、MCP subprocess 環境と送信元情報の変換、repository に束縛した opaque target ID の生成・解析、loopback socket の期限管理、HMAC capability 認証、newline-framed 応答の受信を提供する。

## Read this when
- エディタ入力ハンドオフの schema 適合性、送信元環境変数、repository route・capability の target ID、または client/server 認証と socket transport の挙動を調査・変更するとき。
- ハンドオフ通信の timeout、受信サイズ上限、固定長認証 frame、応答 JSON の受信処理を確認するとき。

## Do not read this when
- エディタ入力ハンドオフ機能そのものの呼び出し側フローや TUI/MCP の具体的な画面・コマンド処理を確認する場合は、それぞれの呼び出し元を直接読むとき。
- 正本 schema の内容や EditorInputHandoffSource の型定義だけを確認したい場合は、oracle 側の schema または型定義を直接読むとき。

## hash
- 17d3c7257e2338323ead131a3d0f8beb583dbd014227078b8c17c2fbd1b7e5b3

# `runtime_errors.py`

## Summary
- cmoc の実行時例外と利用者向け失敗レポート描画を担う。
- CmocError にエラー概要、復旧・調査手順、原因詳細、任意の終端結果を保持させ、render_error で handled failure を利用者向けテキストへ整形する。

## Read this when
- cmoc の実行時例外に利用者向けの概要・次の操作・詳細情報を持たせる必要があるとき。
- ログ初期化前などの境界で例外を簡潔な失敗レポートとして描画する処理を確認・変更するとき。
- CmocError と一般例外で表示内容や既定の次の操作がどう分かれるか確認するとき。

## Do not read this when
- 実行時結果の型や終端状態そのものを確認したい場合は、まず runtime_results の定義を読むとき。
- 特定の呼び出し元が例外を送出・捕捉する流れだけを調べる場合は、その呼び出し元を直接確認するとき。

## hash
- b85627317e4500c89817fba814fe8a9f12af599767725957be6b045711aa2245

# `runtime_feedback.py`

## Summary
- サブコマンド invocation に一つだけ存在する feedback collector と、Codex call ごとの capability context を管理する。
- reporter request の loopback TCP 受付、protocol 検証、並行処理、rate limit、call 終了時の drain、observation 保存を統合する。
- collector や reporter の利用不能を degraded event と warning に変換し、allowlist 済み event を machine observation として検出・保存する。
- doctor から reporter schema、MCP tool 面、collector protocol の可用性を非破壊に検証する入口を提供する。

## Read this when
- feedback reporter の capability・context 伝播、Codex call lifecycle、request の受付制御または終了時 drain を確認・変更するとき
- invocation-scoped collector の起動・停止、並行 Codex call、rate limit、observation の受理・保存経路を追跡するとき
- reporter unavailable や Structured Output validation exhausted の event detector、machine observation 化、または doctor の可用性検証を調べるとき

## Do not read this when
- observation の永続化形式や reporter 入力 schema の定義だけを確認する場合は、runtime feedback store または reporter 実装を直接読むとき
- feedback 機能の正本仕様や利用者向け要件だけを確認する場合は、対応する仕様文書を直接読むとき
- feedback context・collector・detector に関係しない通常の subprocess 実行やログ処理を調べるとき

## hash
- 847c2b8a0b1acb62d7737dda1971470d944fe7685bbd2d0da83d02bb013f30d9

# `runtime_feedback_intake.py`

## Summary
- Collector が受理した observation の durable な順序付けと feedback intake 境界を管理し、intake wave の high-watermark を提供する。
- raw observation の receipt を検証・登録し、指定範囲の入力列挙と publication 後の receipt 削除を担う。

## Read this when
- feedback observation の accepted 後の受理順序、intake wave、high-watermark、または pending receipt の整合性を確認するとき。
- raw observation の ledger 登録、既存 raw の取り込み、publication 対象 receipt の cleanup 境界を追うとき。

## Do not read this when
- feedback observation の内容そのものの保存形式や publication 処理を確認したいときは、raw store または publication 側を直接読む。
- 一般的な runtime state の canonical JSON 読み書きや参照パス解決だけを確認したいときは、共通 state helper を直接読む。

## hash
- d730f6473bea9a4f073c847ff531d9441da323b88e7ab22bff7e38c078e740e6

# `runtime_feedback_reporter.py`

## Summary
- Codex が起動する call-scoped stdio MCP サーバーとして、initialize・ping・tools/list・tools/call を処理し、submit_observation の payload を capability envelope とともに feedback collector へ転送する境界実装。collector 応答の検証と、agent 向け accepted/rejected 結果の MCP structuredContent・text 形式への変換も担う。

## Read this when
- feedback reporter の MCP JSON-RPC 通信、newline-framed stdio ループ、initialize や tools/call の応答、または collector 到達時の結果変換を確認・変更するとき
- collector への接続条件、protocol mismatch、transport failure、collector 応答の妥当性検証など、agent-facing の拒否結果を調べるとき

## Do not read this when
- submit_observation の入力スキーマ、UUID や redaction を含む永続化・検証規則そのものを確認するときは runtime_feedback_store の定義を直接読む
- collector の受付処理、capability の発行、rate limit や secret 検査など collector 内部の挙動だけを調べるとき
- MCP reporter を介さない feedback の仕様や、上位の問題報告ポリシーだけを確認するとき

## hash
- 0dd124d5c38a80dfd33af41625b587248d28cbfe98a57b1d9450903d751c0f26

# `runtime_feedback_run_state.py`

## Summary
- feedback run の immutable wave、seal、join、merge、completion artifact と remediation checkpoint の整合性を検証する実装。
- run identity、入力、wave の順序・high-watermark、artifact hash/path、publication 前提を検査する処理への入口。

## Read this when
- feedback report cut の run lifecycle、immutable artifact、seal/join 記録、wave 境界、または remediation checkpoint の検証条件を確認・変更するとき。
- feedback の intake 入力や checkpoint が append-only か、artifact の canonical hash と manifest が一致するかを調査するとき。

## Do not read this when
- feedback の一般的な状態モデルや lifecycle の正本仕様だけを確認する場合は、まず対応する仕様書を読む。
- feedback store の低レベルな canonical JSON・hash・immutable 書き込み処理だけを確認する場合は、直接その実装へ進む。

## hash
- 0404f94e892378154337bd1f7a78b743a2ad2a3013549ee94d88c531b1ea22cc

# `runtime_feedback_state.py`

## Summary
- feedback の repository-local active state と report cut を一体の integrity boundary で管理する。
- current pointer、generation、publication、incomplete 診断、checkpoint、artifact の整合性を検証する。
- feedback state の生成、公開、復旧、cleanup、破棄に使う path・ID・hash・canonical JSON の処理を提供する。

## Read this when
- feedback の active state、current pointer、generation、report cut の整合性を調べるとき
- publication 後の cleanup、incomplete 診断、checkpoint の復旧や検証を確認するとき
- feedback state artifact の保存、公開、削除、hash 検証の実装入口を探すとき

## Do not read this when
- observation の受付・保存や reporter 入力の処理だけを確認したいとき
- feedback report の上位実行フローや remediation の実行内容だけを確認したいとき
- state の正本仕様や subcommand の利用者向け契約を確認する場合は、対応する oracle 文書を直接読むとき

## hash
- b9e12ba3380ce025ad0f63bc7b211b53e3cec0061e94c1787ad86db49932ac93

# `runtime_feedback_store.py`

## Summary
- feedback observation の入力検証と raw observation の durable store を担う境界。
- agent と machine rule の observation を secret masking、path 正規化、fingerprint、content hash、重複排除、atomic publish に通す。
- 保存済み observation の列挙、未処理件数、蓄積時の warning を提供する。

## Read this when
- feedback observation の受理条件、安全性検査、secret masking、repository 内 path 制約を確認するとき。
- immutable raw record の保存、UUID または rule・event に基づく observation ID、重複・破損時の扱いを確認するとき。
- 通常サブコマンド完了時の pending feedback 件数や report 実行 warning の計算元を確認するとき。

## Do not read this when
- report cut の公開状態、cleanup、または report 処理の状態遷移を確認したいとき。
- reporter input schema の項目定義だけを確認したいとき。
- feedback observation と無関係な一般的なファイル保存処理を調べるとき。

## hash
- cd470dabdd57221f2964d0db231c6a7ddd75aa12302e26a85ca77bbbaf894062

# `runtime_git.py`

## Summary
- Git subprocess と repository 状態の共通境界を担う。
- branch、linked worktree、worktree snapshot の作成・削除・復元と安全性検証を扱う。
- Git ignore の保証・検査、および oracle/realization file の列挙・分類・判定への入口となる。

## Read this when
- Git コマンドの実行結果を cmoc のエラーへ統一したいとき。
- branch や linked worktree の対応、管理領域、symlink、Git metadata を検証または操作するとき。
- Codex call 前後の作業成果物を snapshot・復元するとき。
- `.cmoc/gu` の ignore 状態を初期化・保証・検査するとき。
- repository path の Git ignore 状態や oracle/realization file の分類を判定するとき。

## Do not read this when
- branch/worktree の利用規約や oracle/realization file の分類基準そのものを確認したいとき。
- 個別サブコマンドの orchestration、state 管理、利用者向けエラー仕様を確認したいとき。
- Git repository 状態、ignore、worktree、oracle/realization file に関係しない一般的な filesystem 操作を調べるとき。

## hash
- ff2ec68eb452b3eb58854ef6c8bb97c043c85543d0b98a0754685e7bd6cd000c

# `runtime_logging.py`

## Summary
- サブコマンド実行中のイベントを JSON Lines に即時記録し、保存済みイベントのスナップショットを提供する中心的なロガー。
- ステップ計測、quota 待機時間、warning、Codex call の集約と、実行コンテキストから現在の logger を参照・切り替えするための入口を担う。

## Read this when
- サブコマンドの実行イベント、ログファイルへの記録順序、terminal event、warning、feedback detector 連携を確認するとき。
- 完了サマリー用の step elapsed や quota 待機時間、Codex call 記録の集約方法を調べるとき。
- 深い runtime helper から現在のサブコマンド logger を取得・設定・復元する方法を確認するとき。

## Do not read this when
- ログ保存先や timestamp 付きファイル予約の規則だけを確認したいときは、runtime paths の対象を直接読む。
- feedback event の検出仕様や観測報告の判定を確認したいときは、feedback runtime の対象を直接読む。
- コンソールやファイルログ全体の正本仕様を確認したいときは、対応する仕様書を直接読む。

## hash
- 3641ebc01ef48a1c4506bb5fd9bcb09d10c81d60c29c932688207564b049c712

# `runtime_paths.py`

## Summary
- cmoc の repository root・worktree root・cmoc 自身の root を解決し、session・report・log・editor・worktree・schema・config などの保存先 path を返す共通 runtime path API。
- 実行時刻・console 時刻・duration の表示形式を整え、timestamp 付き path の排他的予約を行う。
- process-wide な cwd 切替を直列化する pushd と、context 単位の cwd override 状態判定を提供する。
- root 配下の memo 判定を symlink を追跡しない path 境界で行う。

## Read this when
- root 解決、cmoc 管理データの保存先、ログ・レポート・schema・editor 入出力の directory、config や refactor state の path を確認または変更するとき。
- timestamp、console 時刻、duration の正規化表示、timestamp path の衝突回避を確認または変更するとき。
- 外部 API の実行前提に合わせた cwd 切替、cwd override の状態、または process-wide な cwd の並列実行制御を確認するとき。
- {{work-root}}/memo の所属判定や、root anchor から repository/worktree root を探索する処理を確認するとき。

## Do not read this when
- 対象の保存先や時刻・cwd 制御ではなく、各サブコマンド固有の処理、ログ内容、prompt 編集、設定値の意味を直接調べるとき。
- root 解決の基盤である path model の仕様や、runtime error の型・表示契約そのものを確認する場合は、それぞれの定義元を直接読むとき.

## hash
- 232a5aa40dc95f04e9e1498892cdbffae13d4deeb8e02dc38aebdeb589ec80d0

# `runtime_primary_report.py`

## Summary
- 非対話サブコマンドの primary report context を管理し、個別 report が未作成の終了経路では確定済み runtime 情報から fallback report を生成・保存する実装。既存 report の検証、実行記録の追記、予約済みパスへの安全な書き込み・更新、および保存失敗時の internal failure を扱う。

## Read this when
- 非対話サブコマンドの primary report がどの終了経路で生成されるか、また fallback 保存時にどの runtime 項目や alias を report fields へ反映するか確認したいとき
- primary report の保存確認、既存 report の安全な更新、保存失敗時の例外処理を変更・調査するとき

## Do not read this when
- 特定サブコマンドの report 項目定義や分類仕様そのものを確認したいときは、primary report の spec・render 実装や各サブコマンドの正本仕様を直接読む
- ログ出力の一般的な仕組み、runtime path の生成規則、TerminalResult の構造だけを確認したいとき

## hash
- 45acbdb0c40b1fca093a1a7594a079e5c6f1eee83974e1a1a83964ba785eaa80

# `runtime_primary_report_render.py`

## Summary
- 確定済みの runtime 情報と terminal 分類から、サブコマンド別の fallback primary report 本文・実行記録・状態要約を描画する。feedback invocation、refactor fork、session join 固有の report 形式と共通の warning・終端結果・関連ログ表示を扱う。

## Read this when
- fallback primary report の構成、サブコマンド別 template の描画、Codex call や feedback observation の実行記録、または report 上の実行状態表示を確認・変更するとき。

## Do not read this when
- primary report の仕様や記載項目の根拠を確認するときは、参照される app specification を直接読む。runtime 情報の収集・event 記録・terminal result の生成を調べるときは、それぞれの store、logger、result 実装を直接読む。

## hash
- 921e40d8504b1db6e56f552bee4d4c69a5d4cc8be2f7d3c845d794ad7badbf81

# `runtime_primary_report_specs.py`

## Summary
- fallback primary report を生成する非対話末端サブコマンドごとの仕様を登録し、command 名から保存先・役割・タイトル・必須項目・テンプレートを取得する定義。

## Read this when
- doctor、indexing、session、oracle edit、realization、run、feedback report の fallback report 仕様や必須項目を確認・変更するとき。
- command 名に対応する primary report 定義の取得処理を確認するとき。

## Do not read this when
- TUI の通知境界を使う tui や oracle investigation の仕様を確認するとき。
- fallback report の実際の保存処理や個別サブコマンドの実行ロジックを直接調べるとき。

## hash
- 6cea29e517f04e01d25b2f9ca945ebb055cd05542cb349451a16ed5030e42062

# `runtime_refactor.py`

## Summary
- realization refactor の調査 state を読み込み、schema 検証、oracle/realization file 集合との同期、path 順保存、調査対象選択、再調査要求、state path の安全性検査を担う。
- refactor state の entry と work-root 相対 path の形式・履歴整合性を検証し、不正な state を CmocError に変換する処理への入口。

## Read this when
- realization refactor の調査履歴 state の読み込み・保存・同期仕様や、次に調査する対象の選択を確認するとき。
- oracle file または realization file の列挙結果を refactor state に反映する処理、digest 変更時の再調査要求、full refactor cycle の開始条件を追うとき。
- refactor state の JSON schema、相対 path の正規化、SHA256・調査日時・未調査 entry の妥当性検証や symlink 経由アクセス拒否を確認するとき。

## Do not read this when
- realization refactor の実際の調査内容や findings の判定方法を確認したいとき。この対象は state の管理だけを扱う。
- oracle/realization file の分類・列挙規則そのものを確認したいときは、列挙処理の正本を直接読む。
- refactor state を利用する CLI の実行フローや利用者向け操作を確認したいときは、呼び出し側の sub-command 実装を先に読む。

## hash
- 14b8d96aa7dd9311a0f1c964035b9f9c4abdb2bbce6b7d6aae0e4b55376efc2b

# `runtime_results.py`

## Summary
- CLI、外部コマンド、Codex exec の実行結果を共通形式で扱うためのデータモデルと型契約を定義する。
- TerminalResult は最外側サブコマンドの完了情報、報告書、詳細、次のアクション、警告を表す。
- CommandResult は外部コマンドの終了コードと標準出力・標準エラーを表す。
- CodexExecResult と関連する型は、Codex exec の structured output、検証問題、ログ・出力パス、実行時間や quota 待機結果を保持する。

## Read this when
- CLI や外部コマンドの実行結果を返すデータ構造を確認・変更するとき。
- Codex exec の structured output 検証結果、補正 prompt 用の問題形式、実行ログや出力の保持契約を確認するとき。
- サブコマンド固有の完了情報や primary report の指定規則を確認するとき。

## Do not read this when
- 特定の CLI サブコマンドの処理手順や業務ロジックを確認したいとき。
- console/file log の表示仕様そのもの、または Codex exec の呼び出し・検証アルゴリズムの詳細を確認したいときは、対応する app_spec や実装対象を直接読む。
- 結果モデルを利用する側の個別処理や、テスト固有の期待値だけを確認するとき。

## hash
- 3d29a5c0f283e675489d76978d04a1592c13debe5aaadb82159ccaec7f281fb4

# `runtime_run.py`

## Summary
- editing run の lifecycle 共通境界として、branch の安全な worktree 解決、run process tracking、親 run と Codex child process group の同一性検証付き停止・cleanup を扱う。

## Read this when
- editing run の join・abandon・error cleanup で、session state と同じ lock を使う worktree 解決や process tracking の読み書き・停止処理を確認するとき。
- run process または Codex child group を PID・start time・process group の検証付きで安全に停止する経路を調べるとき。
- run branch の worktree が managed path と linked worktree metadata を満たすか、tracking file の破損や stale process を fail-closed に扱う実装を確認するとき。

## Do not read this when
- worktree 解決や run process の lifecycle cleanup に関係せず、通常の Git 操作、session state の一般処理、または Codex subprocess の起動実装だけを調べるとき。
- 実行中 process の停止や tracking file の検証ではなく、個別の低レベル process API の仕様を直接確認したいとき。

## hash
- 5d25161c64bdb367a272d99d14ab61054d48a9f32aedc2a5f1a3d457f409f3ac

# `runtime_run_join.py`

## Summary
- editing run の join 処理で、doctor 前処理、session/run worktree の差分検査、run branch の merge、INDEX conflict の解決、post-join 同期、および cleanup を共有する実装。
- 明示的な join と self-joining workload が共有する検証・merge・失敗時復元・run worktree/branch 削除の入口。

## Read this when
- editing run の join 失敗、想定外差分、merge conflict、post-join の INDEX/state 同期、または join 済み run の worktree/branch cleanup を調べるとき。
- run branch を session branch に統合する共通処理や、INDEX.md だけを再生成して conflict を解消する挙動を変更するとき。

## Do not read this when
- run の開始、通常の workload 実行、または join 前の run 状態解決そのものを調べるとき。
- run lifecycle のデータ構造・差分分類・state/report の個別仕様だけを確認する場合は、対応する下位 runtime モジュールを直接読むとき。

## hash
- 725fef246fa19969636930118d93ee6c13dcc1100e1c64f92215e1281a3cbd92

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始・state 遷移・commit・INDEX 更新・cleanup 判定を、共有 context と lifecycle lock のもとで扱う共通ライフサイクル処理。
- session/run の事前条件、active run 解決、process tracking recovery、Git 差分分類と許可 path 検査の入口。

## Read this when
- editing run の開始や joinable/error 遷移を実装・調査するとき。
- run/session worktree の recovery、workload の commit、INDEX 再生成を確認するとき。
- oracle・realization・生成 INDEX を含む差分の許可範囲や cleanup 判定を確認するとき。

## Do not read this when
- 個別 workload の realization 内容や sub-command 固有処理だけを確認したいとき。
- INDEX 生成、Git 操作、state schema の専用実装そのものを直接確認したいとき。

## hash
- b42694dc0663a5c2bd950713a03cd7a5b38820df5ac68e68b3ba297786f69691

# `runtime_run_report.py`

## Summary
- editing run の fork report と lifecycle report を生成・更新する共通処理を扱う。
- レポートの YAML Front Matter、完了状態、変更パス、実行段階、関連ログなどの出力内容を組み立て、安全な Markdown 描画と保存を担う。

## Read this when
- editing run の fork 実行結果または run join/abandon のライフサイクル結果をレポート化する処理を確認・変更するとき。
- レポートの保存先予約、共通メタデータ、実行ログの反映、変更パスの Markdown エスケープを調べるとき。

## Do not read this when
- レポートの仕様や記載項目の正本を確認したいだけで、生成実装を読む必要がないとき。
- レポート以外の runtime 処理や、個別サブコマンドのワークフローを直接調べるとき。

## hash
- 9dfdc8e5c735a0e989c90fae68c6f227441e5050230ca7e3282c0884b0c1aeac

# `runtime_state.py`

## Summary
- session と editing run の状態 schema を検証し、state file の安全な読み書き、branch からの session 識別、session lifecycle の排他制御を提供する。session state の永続化や branch に対応する state の復元を行う処理への入口。

## Read this when
- session の状態・run の状態を読み込む、検証する、保存する処理を追加または変更するとき
- session branch や run branch から session-id を解決するとき
- session lifecycle の同時実行を防ぐ lock や state file のパス安全性を確認するとき

## Do not read this when
- session や run の具体的な lifecycle 遷移、CLI 操作手順、branch 運用規則そのものを確認したいとき
- state schema の正本仕様や個別 sub-command の振る舞いを直接確認すべきとき

## hash
- 5ea0c7423ab0802ad641c4ab0261df8daafb98ae165de6a3cd56223766a955b0

# `runtime_windows_toast.py`

## Summary
- Windows toast 通知と Codex TUI callback の非致命的な transport 境界を扱う実装。通知内容の短文化、Windows PowerShell 経由の toast 送信、TUI の root session 記録・callback の turn 重複排除・実行中 marker による drain、completion probe 時の無効化をまとめた入口。

## Read this when
- Codex TUI のセッション開始 hook や turn 完了 callback から、最終結果を変えずに入力待ち通知を送る仕組みを確認したいとき
- Windows PowerShell/WinRT toast の解決、有限 timeout、制限された JSON payload、通知失敗の非致命性を確認したいとき
- callback の root session 検証、turn 単位の重複排除、一時 state の cleanup と遅延 callback の drain を調べるとき

## Do not read this when
- 最外側サブコマンドの terminal result 通知を呼び出す側の仕様だけを確認したいとき
- Codex TUI callback や Windows toast に関係しない runtime 共通処理を調べるとき
- 通知 transport の実装詳細ではなく、Windows toast の正本仕様や Codex の外部 hook 契約そのものを直接確認したいとき

## hash
- ec2ff9d13fb19e614e1d22b439fa0d5470ba01bdaeddf51c7c37a9bba7130fde
