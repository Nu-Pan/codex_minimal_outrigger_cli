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
- INDEX.md の検査・生成・更新・復元・commit を一貫して扱う indexing lifecycle の共通実装です。
- 対象ディレクトリを走査し、既存 entry の hash による再利用判定、不足 entry の Codex 生成、INDEX.md の書き込みを行います。
- 更新時の排他 lock、ファイル snapshot による失敗時復元、Git 差分確認と indexing commit までを担当します。

## Read this when
- INDEX.md の自動生成・鮮度判定・entry 再利用の挙動を変更または調査するとき。
- directory traversal、除外対象、hash 計算、Codex による entry 生成、更新の並列化を確認するとき。
- INDEX.md 更新の排他制御、失敗時復元、または commit lifecycle を変更するとき。

## Do not read this when
- INDEX.md entry の生成 prompt や Structured Output schema 自体を変更するときは、index entry builder または schema の対象を直接読む。
- Codex 実行の preflight・profile・isolation の一般仕様だけを確認するときは、対応する runtime 実装または oracle 仕様を直接読む。
- INDEX.md の利用者向けルーティング規則だけを確認するときは、indexing の正本仕様を直接読む。

## hash
- 66f2b0b29051fe7125e7b44e66cf4cdd014494a75ef6fa10c7031b7959d2e1ef

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
- 最外側 CLI サブコマンドの実行開始から終了までを統括し、作業ディレクトリ検査、診断ログ、feedback 回収、primary report 保存、terminal result 表示、終了コード、TUI 通知を管理する入口。
- サブコマンドの正常完了、ユーザー中断、実行エラーを分類し、例外や警告を診断情報と次の操作へ統合する終端処理を提供する。
- サブコマンド内の step 通知、ユーザー中断状態、TUI 起動境界の記録など、最外側ライフサイクルに連動する補助 API を含む。

## Read this when
- 最外側 CLI サブコマンドの起動・終了ライフサイクル、例外処理、終了コード、terminal result の表示やログ記録を変更・確認するとき。
- サブコマンドの作業ディレクトリ制約、doctor preprocess、feedback invocation、primary report、Windows 通知の連携を調査するとき。
- ユーザー中断や TUI process 起動前後での KeyboardInterrupt の扱い、step 進捗通知の実装を確認するとき。

## Do not read this when
- terminal result のデータ構造や個別エラー型だけを確認する場合は、それぞれの定義元を直接読むとよい。
- サブコマンド固有の業務処理、doctor・feedback・logging・primary report の内部仕様だけを調査する場合は、各専用モジュールや正本仕様を直接読むとよい。
- INDEX.md のルーティング情報だけを更新する場合。

## hash
- 614a76ab85097ee4d149a6c74833698082f693ef68108b9e087247704a81cc63

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
- Structured Output の parse・JSON Schema・宣言済み事後条件を検証し、違反時の同一 session による補正 turn と成果物不変性を管理する。
- Codex exec subprocess の argv、prompt、stdout/stderr、output、call log を生成・保存し、capacity retry、quota availability probe／待機／resume、失敗分類を一つの実行ループで制御する。
- agent call・Codex call・subcommand event と quota／Structured Output の診断情報を関連付け、最終的な CodexExecResult または CmocError を返す実行制御の入口。

## Read this when
- Codex exec の subprocess 起動条件、prompt／output／call log の保存、Structured Output 検証・補正の挙動を確認するとき。
- capacity error の retry、quota 回復 probe と resume、session ID の扱い、実行イベントの記録を変更・調査するとき。
- CodexExecResult の生成や Codex 呼び出し失敗の分類・診断情報の責務を確認するとき。

## Do not read this when
- TUI の起動・表示や exec 以外の CLI 分岐を扱うときは、TUI／CLI 分岐を担当する対象を直接読む。
- Codex の設定値・profile・schema 準備・subprocess 低レベル処理そのものを変更するときは、対応する runtime_codex_profile などの専用対象を直接読む。
- call log の一般的な出力形式、feedback store、git snapshot、path／logging の共通実装だけを確認したいときは、各専用 runtime module を直接読む。

## hash
- 8bb5f0e82054e384de8c8a13bfea921d37a01ddb7c6ebc77b20dad939f73fddf

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
- Codex CLI subprocess 境界の実行環境・argv・schema 配置・process tracking・出力解析を扱う。Codex 起動条件の組み立てから、JSONL の error、capacity、quota、resume token の判定までを確認する入口。

## Read this when
- Codex CLI に渡す sandbox、CODEX_HOME、環境変数、model provider、MCP、hook、schema、callback の設定を確認・変更するとき。
- editing run の Codex subprocess tracking、process group の安全な停止、PID 再利用対策を調査するとき。
- Codex の終了結果、JSONL event、schema output、capacity/quota retry、unexpected error の解釈を確認するとき。

## Do not read this when
- Codex CLI 境界の外側にある agent call の業務フロー、設定定義そのもの、または利用者向けエラーの上位制御だけを確認するとき。
- Codex subprocess の実装変更ではなく、個別の oracle 仕様や test 実行規則を直接確認すべきとき。

## hash
- 60c0ba3e7d4921e7c247f59cea4bfd16f2a7c29c01e2555b71280f3f8a9f9678

# `runtime_codex_tui.py`

## Summary
- Codex TUI を設定済みの実行環境と argv で起動し、呼び出し情報・実行時間・終了状態・エラーを call log と logger event に記録する実行入口。
- TUI 通知フック、エディター入力引き渡し、feedback call の環境設定を呼び出し期間に組み込み、Codex subprocess の成功結果または cmoc エラーへ変換する。

## Read this when
- Codex TUI の起動処理、Codex subprocess の実行条件、call log の生成、実行結果や失敗時の記録・例外変換を確認するとき。
- TUI 起動時の通知 callback や feedback call のライフサイクルを含む、Codex 呼び出し全体の制御経路を調べるとき。

## Do not read this when
- Codex のホーム解決、環境変数、TUI hook 対応判定、override argv の具体的な規則だけを調べるときは runtime_codex_profile を直接読む。
- ログ出力 API、コマンド結果型、通知 callback、feedback 保存処理の内部仕様だけを調べるときは、それぞれの専用モジュールを直接読む。

## hash
- be1879e7d1cc6fa657d85ca4575847c2644aa61983618789a58ad6c443e699c7

# `runtime_config.py`

## Summary
- cmoc 設定を JSON/TOML 互換値として検証し、正本設定型との相互変換、ファイルの読み書き、既定値との同期を担う。
- 設定値の型・範囲・循環参照・文字列制約と、設定ファイルの symlink・特殊ファイル・不正 JSON に対する利用者向けエラー境界を提供する。

## Read this when
- cmoc 設定の永続化形式と正本設定型の変換を確認するとき。
- 設定値の検証条件や、既定値を補完した設定復元の挙動を調べるとき。
- 設定ファイルの生成・読み込み・同期、または symlink や特殊ファイルを含むファイルアクセス時のエラー処理を確認するとき。

## Do not read this when
- Codex のモデルや agent call 自体の定義・既定値を確認したいときは、設定型を直接読む。
- 設定パスの算出規則だけを確認したいときは、パス管理の対象を直接読む。
- 設定以外の実行時エラーや CLI の処理フローを調べるとき。

## hash
- 9154ffee4c49ac3c9ee053e54dcd941ae727615d614618f49cf461fc18f19283

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
- prompt editor の待機中に一時 handoff target を公開し、認証済み loopback TCP の IPC request を検証して、指定された editor work file の内容を安全に UTF-8 で上書きする処理を担う。
- target ID・repository・protocol・payload を検証し、接続単位の受付を直列化しながら、認証失敗・不一致・書き込み失敗を content なしの結果で返す入口。

## Read this when
- prompt editor からの入力受け渡し、editor work file の検証・上書き、loopback IPC の認証や target lifecycle（開始・終了・接続処理）を変更または調査するとき。
- handoff の拒否コード、対象 repository／target の対応付け、受付済み submission 完了後の close 動作を確認するとき。

## Do not read this when
- handoff protocol の定数・認証方式・target ID 生成・payload schema 自体を変更または確認する場合は、まず runtime_editor_input_handoff_protocol 側を読むべきとき。
- editor work directory のパス定義や一般的なエラー型の仕様だけを確認する場合は、runtime_paths または runtime_errors を直接読むべきとき。

## hash
- b6f65e64a4f979d542579cdc933cddbd02af03ede3296f98288d933354448d44

# `runtime_editor_input_handoff_mcp.py`

## Summary
- Codex TUI の editor input handoff 用 stdio MCP server として、JSON-RPC の initialize・ping・tools/list・tools/call を処理する。
- overwrite tool の入力を同一 repository の active target へ認証付き TCP 転送し、受理または定義済み domain failure を MCP structuredContent と text で返す。

## Read this when
- Codex TUI から prompt editor input の全体置換を active target へ引き渡す経路を確認するとき。
- editor input handoff の MCP JSON-RPC transport、入力検証、target 認証、repository 一致、転送結果の検証を調べるとき。
- overwrite tool の MCP 公開定義や、target unavailable・transport unavailable などの失敗応答の扱いを確認するとき。

## Do not read this when
- editor input handoff の target 側プロトコル、target ID の解析、認証処理そのものを調べるときは、runtime_editor_input_handoff_protocol の定義を直接読む。
- Codex TUI の editor input file の生成・管理や、MCP server の起動元を調べるとき。
- この server を介さない一般的な MCP tool や JSON-RPC の仕様だけを確認するとき。

## hash
- 83c1262909560b30ccadb74b693fabe1bfcfa31e1c993dce8ebe5414a9e8f723

# `runtime_editor_input_handoff_protocol.py`

## Summary
- editor input handoff の共有基盤。overwrite input schema の読み込み・適合検査、repository に紐づく loopback target ID の生成と解析、MCP subprocess 環境への repository context 付与を扱う。
- editor input handoff の socket transport と capability 認証を担う。nonce と role-separated HMAC proof による client/server 認証、deadline 制御下の固定長 frame 通信、newline-framed response の読み取りを確認する入口。

## Read this when
- editor input handoff の schema 適合、target ID routing、repository context、loopback 通信、認証 handshake、response framing の挙動を調査・変更するとき。
- editor input handoff protocol version 2 の timeout、token、nonce、proof、response size 制約を確認するとき。

## Do not read this when
- editor input handoff の overwrite input schema 本文そのものを確認したいときは、oracle package の overwrite_input.json を直接読む。
- MCP client/server の呼び出し側の責務や editor UI の編集挙動だけを調査する場合は、各呼び出し側・UI 実装を直接読む。

## hash
- f02e87e636663f8bd6316b0e2cd379e49dc78d47dbed493405e7b17f31195052

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
- サブコマンド invocation 単位の feedback collector を管理し、Codex call ごとの capability 発行、reporter request の並行受付・検証・保存、call 終了時の drain、degraded event の記録、allowlist 対象 event の machine observation 化を統合する。

## Read this when
- feedback observation の受付経路、capability と call context のライフサイクル、collector の起動・停止や並行処理を確認するとき。
- reporter または collector の利用不能時の非致命処理、doctor による protocol/schema 検証、structured output failure などの detector を調べるとき。
- Codex subprocess へ feedback 用環境変数を継承する処理、accepted observation の invocation 内追跡、event から observation への変換条件を確認するとき。

## Do not read this when
- feedback observation の永続化形式や payload/schema 自体を変更・確認する場合は、対応する runtime feedback store または oracle の仕様を直接読むとき。
- MCP reporter 単体の公開 tool 実装や stdio protocol の詳細だけを調べる場合は、reporter 実装を直接読むとき。
- 一般的な invocation lifecycle や subcommand logging の仕様だけを確認する場合は、関連する lifecycle・logging 実装を直接読むとき。

## hash
- 818036fcfefd91330cf8d6fd10d3b3286aa9498c7f8cb60b5ccbcbd3231fed0b

# `runtime_feedback_intake.py`

## Summary
- Collector が durable な受理順序を管理し、feedback raw observation の receipt 登録・high-watermark 固定・publication 後の receipt 削除を担う。
- intake ledger の整合性、raw artifact 参照、重複登録、単調増加 sequence、collector 排他境界を検証する feedback intake の実装入口。

## Read this when
- feedback observation の受理順序、intake high-watermark、pending receipt の永続化または削除を変更・調査するとき。
- collector の受理境界、raw observation の hash 検証、publication と intake の排他連携を確認するとき。

## Do not read this when
- feedback の canonical state や artifact 参照解決そのものを確認する場合は runtime_feedback_state を直接読むとき。
- observation の保存場所、ID 判定、列挙処理そのものを確認する場合は runtime_feedback_store を直接読むとき。
- publication の処理や collector の呼び出し順序を確認する場合は、それぞれの呼び出し元を直接読むとき。

## hash
- 3999eb3f98548ed171437d9300115a961e7764a1117b9a55368f1baf9d71d598

# `runtime_feedback_reporter.py`

## Summary
- 対象は、Codex が起動する call-scoped stdio MCP feedback reporter/client であり、MCP の初期化・ping・ツール一覧・submit_observation 呼び出しを newline-framed JSON-RPC として処理する。
- feedback collector への接続情報と capability envelope を検証・分離して payload を転送し、collector の accepted/rejected domain result を検証して MCP の structuredContent と text の両方で返す。
- collector context 不備、protocol 不一致、接続・応答異常を定義済みの rejection code と retryability に変換する。

## Read this when
- feedback observation の submit_observation 呼び出し経路、MCP stdio JSON-RPC の reporter 動作、または collector との call-scoped transport 契約を確認・変更するとき。
- collector から返る accepted/rejected 結果の agent-facing 検証や、MCP 応答への変換を確認するとき。
- feedback reporter の protocol、capability、collector port 環境変数に関わる接続障害・再試行可否の扱いを調べるとき。

## Do not read this when
- feedback observation の payload schema、UUID 生成、保存・redaction・collector 側の受理処理そのものを確認したいときは、対応する runtime_feedback_store または collector の実装を直接読む。
- MCP reporter ではなく、feedback observation の正本仕様や運用上の報告条件だけを確認したいとき。

## hash
- 567f7eb4ab1a8bd68506702b9cefeb1cd52eae339a640aca15f4464c7ec7b21e

# `runtime_feedback_run_state.py`

## Summary
- feedback run の immutable wave、seal、join 記録、および remediation checkpoint の整合性を検証する実装。
- report cut manifest の run identity、入力、high-watermark、artifact path、canonical hash、commit、verification 記録を検査する。
- artifact 保存と manifest 更新の間に停止した場合は、固定 path から未登録 artifact reference を復旧する。

## Read this when
- feedback report の run artifact、wave の順序、seal 後の変更禁止、join lifecycle の整合性を確認・変更するとき。
- remediation checkpoint の schema、issue identity、変更 path、commit、差分 hash、機械検査、verification 記録の検証を調べるとき。
- report cut manifest の更新規則や artifact 保存後の recovery 動作を確認するとき。

## Do not read this when
- feedback の正本状態仕様や lifecycle の意味を確認したいだけで、実装上の検証・復旧処理を調べる必要がないとき。
- canonical JSON の保存・hash 生成そのものを確認する場合は、共通の feedback store 実装を直接読むとき。
- report cut artifact の基本構造や参照 path の共通検証を確認する場合は、feedback state の共通実装を直接読むとき。

## hash
- 5512c681ec97b4e2ec363f7a51c8375a8d889169f51ef5598bc385f4398ef49f

# `runtime_feedback_state.py`

## Summary
- feedback の repository-local active state と report cut の整合性を一元管理する。current pointer、generation、issue／machine aggregate、publication、incomplete 診断、checkpoint、cleanup の検証・保存・切替・回収を担い、異常終了時の復旧可能性と artifact 間の hash／identity 整合性を保つ。

## Read this when
- feedback report の state transition、active generation の構築・公開、current pointer の切替、publication 後 cleanup、report cut の再開・破棄を実装または調査するとき
- repository-local feedback artifact の schema、path／SHA256 reference、canonical JSON、symlink 防御、writer lock、current／work／cleanup state の整合性を確認するとき
- incomplete 診断や remediation／normalization checkpoint と、正式 publication との相互排他・復旧規則を確認するとき

## Do not read this when
- raw observation の収集・受付・receipt 管理だけを扱うときは observation intake／store の実装を直接読む
- feedback report の Markdown 内容や agent 向け reference の生成規則だけを扱うときは report／report cut の生成実装または対応する oracle を直接読む
- 個別の runtime error、CLI 引数、機械ルールの検出ロジックだけを扱い、repository state の遷移・整合性に触れないときはこのモジュールを読まない

## hash
- 60f65f4eb1273cc75069f75fa45ff270f94f8225c46a1b8e4367f746325165b0

# `runtime_feedback_store.py`

## Summary
- feedback raw observation の受理・安全化・immutable 保存を担う境界。schema 検査、secret masking、repository 内 evidence path の正規化と fingerprint、UUIDv7 または machine rule に基づく observation ID、atomic publish、重複・破損検査を一体として扱う。
- 保存済み raw observation の列挙、未処理判定、完了時の pending 件数と蓄積 warning の計算を提供し、collector/report 間で同一 byte 表現と保存先を共有する入口になる。

## Read this when
- feedback observation の入力検証、secret masking、evidence path 境界、fingerprint、observation ID、raw record の durable 保存または atomic publish の挙動を確認するとき。
- raw observation の重複・衝突・一時ファイル回収、未処理件数、publication 後の処理済み判定を調べるとき。

## Do not read this when
- feedback の正本 schema や受理・公開状態の仕様そのものを確認する場合は、対応する oracle の仕様または schema を直接読むとき。
- MCP feedback tool の呼び出し契約や report cut の業務フローだけを確認する場合は、この raw store の実装ではなく専用の reporter/reporting 対象を読むとき。

## hash
- 799eb1fc8e066827ddc5bdadbbc81e6e7d18e235c871956a7dda3d85103c1a7b

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
- サブコマンド実行中の JSON Lines event、step timing、quota 待機時間、warning、Codex call 記録を集約する runtime logging の中核。
- サブコマンド logger の生成・current context への設定・event 記録・step 計測結果の参照が必要な作業の入口。

## Read this when
- サブコマンド単位の実行ログや計測値の記録・集約方法を確認するとき。
- SubcommandLogger の event、step timing、warning、quota 待機、Codex call の扱いを変更または調査するとき。
- 深い runtime helper から current logger を参照・差し替え・復元する処理を確認するとき。

## Do not read this when
- ログファイルの保存先や timestamp 付きパス予約の規則だけを確認したいときは runtime_paths を読む。
- feedback event の検出・観測報告の仕様だけを確認したいときは runtime_feedback 関連の対象を直接読む。
- サブコマンド固有の業務処理や console 表示の詳細だけを確認したいとき。

## hash
- 69426c7fe39b7f0c2f0c22a9d968d01c668c6534c04403297b742d6d9f7c4bea

# `runtime_paths.py`

## Summary
- cmoc の repository・worktree・cmoc root 解決、runtime 用ディレクトリや保存先 path の算出、時刻・duration の整形、process-wide に直列化した cwd 切替を提供する共通基盤。

## Read this when
- root の解決や root 起点の保存先 directory/path を確認・変更するとき。
- timestamp、console timestamp、duration 表示の形式や境界条件を確認するとき。
- cwd を一時的に切り替える処理、または cwd 切替中かどうかの判定を扱うとき。

## Do not read this when
- 特定のサブコマンド固有の処理や report・log の内容仕様だけを確認したいとき。
- root/path のモデル自体の解決規則を確認したいときは、root resolver の定義を直接読む。

## hash
- e94a83841f4c5ef59de9af7daa87785e733d26992b7d669a96c5f50010deba67

# `runtime_primary_report.py`

## Summary
- 非対話サブコマンドの primary report 保存を共通化する実行時モジュール。既存 report の検証、未作成時の fallback report 生成、保存失敗の internal error 化、invocation-local な report 項目の保持と確定値・alias の収集を担う。

## Read this when
- 非対話サブコマンドの終了経路で primary report を保存・再利用・検証する処理を確認または変更するとき
- fallback report の共通項目、個別 command の確定項目、terminal classification、completion reason の扱いを確認するとき
- oracle edit、feedback report、realization apply/refactor fork の report 保存前後の状態や status を追跡するとき
- report 保存失敗時の例外、予約 path の後始末、空 file・symlink の検証を確認するとき

## Do not read this when
- primary report の項目定義や command ごとの必須 field を確認するだけで、保存処理や fallback 生成を扱わないときは runtime_primary_report_specs を読む
- report の Markdown 形式や execution record、status の描画規則だけを確認するときは runtime_primary_report_render を直接読む
- runtime path の timestamp 付き保存先生成だけを扱うときは runtime_paths を直接読む
- 実際の各サブコマンド固有の処理や oracle の仕様を確認するときは、その command の実装または対応する oracle 文書を直接読む

## hash
- f17e671e162ef4d65a9372533f58fce0846495ba96157054542d42cb14bc10ae

# `runtime_primary_report_render.py`

## Summary
- 確定済み runtime 情報から、通常 invocation summary と feedback report invocation summary を Markdown 形式で描画する report writer。実行段階、終端分類、warning/error、次の操作、関連ログ、Codex 最終出力、新規 feedback observation を report に組み立てる。
- PrimaryReportSpec の template に応じた本文生成に加え、YAML scalar、安全な inline 表現、Codex call の状態、feedback publication・cleanup の状態を補助関数として提供する。

## Read this when
- runtime 情報から primary report または feedback invocation summary を生成・変更するとき
- report の実行段階、終端結果、warning/error、checkpoint、publication 状態、関連ログの表示規則を確認するとき
- Codex call の最終出力や受理済み feedback observation を実行記録へ含める処理を調べるとき

## Do not read this when
- feedback observation の受理・送信処理そのものを変更または調査するとき
- PrimaryReportSpec、TerminalResult、SubcommandLogger などの確定情報源の定義を直接確認するとき
- コンソール表示やファイルログの仕様自体を確認するときは、先に参照元の app specification を読むべき場合

## hash
- 5b1e7706d781c004100b7c30cf2a89f59ba279e0d30a6e0f8d9ecdcdc1f7b540

# `runtime_primary_report_specs.py`

## Summary
- 非対話末端サブコマンドごとの fallback primary report 定義を集約する入口。
- command 名から report の保存先、役割、タイトル、追加必須項目、テンプレート種別を確認するための対象。
- TUI と oracle investigation を除く現行サブコマンドの report 対応範囲を確認できる。

## Read this when
- 特定の非対話末端サブコマンドが保存する primary report の定義を確認するとき。
- report の保存先や役割、タイトル、追加項目、テンプレート種別を command 名から調べるとき。
- fallback report の command 対応付けや、`primary_report_spec` による参照方法を確認するとき。

## Do not read this when
- primary report 共通の保存・表示契約を確認したいときは、console と file log の正本仕様を直接読む。
- 個別サブコマンドの処理手順、終了理由、終了コードを確認したいときは、対応する個別サブコマンド仕様を直接読む。
- TUI または oracle investigation の通知境界を確認したいときは、対象の通知仕様を直接読む。

## hash
- 1154d05f178d551bf6a00b4ad66c7fbd37bfca1b37add5c62784b2edc2e08161

# `runtime_refactor.py`

## Summary
- realization refactor の調査 state を読み込み、schema 検証、oracle/realization file 集合との同期、安定した JSON 永続化を担う。
- 未調査・要再調査の対象を正本の優先順位で選択し、調査履歴の保持や新しい refactor cycle の開始を支援する。
- state path の symlink・非通常ファイルを拒否し、相対 path、調査結果、SHA256、調査日時などの refactor 契約を検証する。

## Read this when
- realization refactor の state file の読み書き、schema 検証、調査対象の同期や選択の挙動を変更・確認するとき。
- oracle file と realization file の列挙結果を refactor state に反映する処理や、調査履歴の再利用・再調査条件を確認するとき。
- 不正な state、symlink 経由の state path、path・SHA256・timestamp の検証エラーの原因を調べるとき。

## Do not read this when
- realization refactor の調査処理そのものや、個別 oracle/realization file の内容を確認することが目的で、state 管理を扱わないとき。
- oracle/realization file の列挙規則自体を変更・確認するときは、列挙を実装する対象を直接読む。
- state file の配置や realization refactor コマンド全体の利用者向け仕様を確認するときは、対応する app specification を直接読む。

## hash
- 72b113fcdbd4ab228b598f72f2f630551707c388bc2d31947687aa2316ee10de

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
- 明示的な join を必要とする editing run の共通 lifecycle 処理を担う。run の開始・state 遷移・commit、差分分類、INDEX 更新、cleanup 判定を EditingRunContext と lifecycle lock の共有下で扱う。

## Read this when
- editing run の開始、active run の解決・回収、joinable/error への state 遷移を変更または調査するとき
- run worktree の差分許可範囲、oracle 差分、生成 INDEX.md の判定、work unit の commit・rollback を扱うとき
- editing run lifecycle 全体で共有される不変条件や cleanup 判定を確認するとき

## Do not read this when
- 個別 subcommand の利用者向け挙動や agent call の責務だけを確認する場合
- editing run lifecycle の共通処理ではなく、canonical な配置や設計上の責務境界を確認する場合は design_rule.md を直接読むとき
- INDEX.md の生成規則そのものを確認する場合は indexing の正本仕様を直接読むとき

## hash
- 520604c564eb18319ffb651c3c67108fce6c990528d13d974c2fd03987391b14

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
- session と editing run の永続 state を表す schema、JSON の厳密な検証・復元・保存、session/run branch からの state 解決、session fork 排他 lock、state path の隔離・安全性検査を提供する。

## Read this when
- session state の schema、state file の読み書き、session または run branch に対応する state の取得を実装・調査するとき
- state の状態値、必須 field、run payload、branch 名、session identity の検証規則を確認するとき
- session fork の排他制御や state path の symlink・非通常 file・session-id 検査の責務を確認するとき

## Do not read this when
- session や editing run の業務フロー、branch lifecycle、join/apply の手順そのものを確認したいときは、対応する app_spec または sub_command の仕様を先に読む
- session state を利用する個別 command の振る舞いだけを調査し、state schema・永続化・branch 対応付けの実装詳細を確認する必要がないとき

## hash
- e867e541be6e472cdbb55968e876f035885214d00a56b21331c7e33a84ab05c5

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
