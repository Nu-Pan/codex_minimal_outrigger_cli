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
- Codex CLI subprocess の起動境界を担当し、sandbox・argv・cwd・CODEX_HOME・環境変数・process tracking・schema 配置を構成する。
- Codex CLI の実行結果を扱う入口として、JSONL の session ID 抽出、stderr・event message の集約、capacity・quota・unexpected error の判定を提供する。

## Read this when
- Codex CLI の起動引数、sandbox、cwd、CODEX_HOME、provider・MCP・hook の invocation-local 設定を確認または変更するとき。
- Codex subprocess の process group tracking、PID reuse 対策、停止・cleanup、起動失敗時の実行時エラーを確認するとき。
- Structured Output schema の配置、Codex JSONL 出力の解析、capacity・quota・malformed・unexpected error の扱いを確認するとき。

## Do not read this when
- Codex CLI subprocess の argv・環境・実行結果の境界に関係しない、上位の agent call 制御や編集実行フローを確認するとき。
- Codex CLI の一般仕様や利用者向け設定を直接確認したいときは、subprocess 境界の実装ではなく対応する仕様または設定の対象を読む。

## hash
- 3c58df41b1156236a7221a5fe0df990eb99891bcbfd7f4f3f94ab068e9fed1fe

# `runtime_codex_tui.py`

## Summary
- `run_codex_tui` と内部の process 実行処理を通じて、設定・環境・通知 hook を準備し、Codex TUI を起動する入口。
- Codex 呼び出しごとの call log、feedback call、成功・失敗 event、実行時間、return code を記録し、起動失敗や CLI/TUI 失敗を所定の例外へ変換する。

## Read this when
- Codex TUI の起動経路、agent call 用の argv・環境・設定上書き、通知 callback のライフサイクルを確認したいとき。
- Codex 呼び出しの call log や logger event の記録内容、feedback call の開始・終了、失敗時の例外変換を追跡したいとき。

## Do not read this when
- Codex の設定値や provider・model の解決規則そのものを確認したいときは、各 runtime_codex_profile や設定関連の対象を直接読む。
- call log の保存先や timestamped path の予約規則だけを確認したいときは、runtime_paths の対象を直接読む。

## hash
- 386f2f9b23ada07addbe00da7eb6efba9afc64949cd203eaebe904da24615bf6

# `runtime_config.py`

## Summary
- cmoc 設定の JSON/TOML 互換値を検証し、設定オブジェクトと永続化 JSON の相互変換、設定ファイルの読み書き・同期を担う実装。
- 設定値の型・範囲・循環参照・symlink・特殊ファイルを検証し、不正な設定を利用者向け CmocError に変換する処理への入口。

## Read this when
- cmoc 設定のシリアライズ形式、既定値補完、model provider や agent call の復元処理を変更・確認するとき。
- 設定 JSON の読み込み・保存・初回生成・同期の挙動、または設定値の入力検証やエラー境界を調査するとき。

## Do not read this when
- 設定項目そのものの正本型定義や既定値を確認したい場合は、先に設定モデル定義を読むとき。
- 設定ファイルのパス決定だけを確認したい場合や、一般的な実行時エラー型の定義だけを確認したい場合。

## hash
- 50d11ec84799a24f75697920c189c3058d059833d38d2f601447ffe4497f7611

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
- editor 待機中に公開する一時 handoff target と、認証付き loopback TCP による prompt editor input の IPC 境界を扱う。対象ファイルの検証、request の認証・検証、同一 target への content 上書き、受付終了と後処理を担う。

## Read this when
- prompt editor から待機中の editor work file へ入力を引き渡す経路、target の lifecycle、loopback IPC の protocol/repository/target 検証、または安全なファイル上書き動作を確認・変更するとき。

## Do not read this when
- editor input handoff の protocol 定数・target ID 生成・入力 schema の定義自体を確認したいときは protocol module を直接読む。
- editor work directory のパス決定や一般的な runtime error の定義だけを確認したいときは、それぞれの専用 module を直接読む。

## hash
- 9bb3f12d65911e0ade82686e13551167ce9078ee4a8d6d378cde4772ba866f69

# `runtime_editor_input_handoff_mcp.py`

## Summary
- Codex TUI の editor input handoff 用 stdio MCP server として、JSON-RPC/MCP の initialize・ping・tools/list・tools/call を処理する。
- overwrite ツールの入力を検証し、同一 repository の active editor input target へ認証付き TCP 転送して、受付結果または転送結果不明を返す。
- editor input handoff のプロトコル詳細や入力スキーマ自体ではなく、stdio MCP の公開インターフェースと target 転送境界を確認するための入口。

## Read this when
- Codex TUI の editor input handoff MCP server の起動方式、newline-framed stdio 通信、JSON-RPC 応答を確認するとき。
- overwrite ツールの公開仕様、入力検証、active target への転送、認証付き通信、受付結果の扱いを調査・変更するとき。
- MCP の initialize、ping、tools/list、tools/call、未知 method、parse error への応答を確認するとき。

## Do not read this when
- editor input handoff の target ID 解析、認証、入力スキーマ、応答プロトコルの詳細を直接確認する場合は、参照先の protocol helper を読むとき。
- Codex TUI 側での editor input file の生成・active target 管理・実際の上書き処理を調査する場合。
- MCP server と無関係な一般的な stdio 入出力や、別の tool の実装を確認する場合。

## hash
- 092019b886475559163d5680b5c50d7f07682ab54f5d56b36f68c53d44aee490

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
- feedback run の immutable wave、issue checkpoint、seal、join 記録を検証・復旧する実装への入口。run の identity、入力の append-only 性、wave の順序と high-watermark、artifact の hash/path 対応、remediation checkpoint の schema・判定根拠・実差分整合性を扱う。

## Read this when
- feedback run の lifecycle、report cut の封印、join 完了条件、wave/checkpoint の不変性や整合性を確認・変更するとき。
- artifact 保存と manifest 更新の中断からの復旧、remediation の正式 checkpoint と issue commit・verification の対応を追うとき。

## Do not read this when
- feedback run artifact の低レベルな canonical JSON 保存・hash 計算だけを確認したいときは、artifact store の実装を直接読む。
- report cut の正本仕様や lifecycle の意味を確認したいときは、対応する仕様書・run lifecycle 実装を先に読む。

## hash
- ca512d58c8152bdbf1c7511e173c03f7ce0695583418b170599a8945a0f5bf54

# `runtime_feedback_state.py`

## Summary
- feedback の repository-local state を一元管理し、report cut、active generation、current pointer、publication、incomplete 診断、checkpoint、artifact cleanup の整合性を検証・保存・復旧する。
- observation envelope と machine aggregate の canonical identity、参照 hash、閾値、時刻、状態遷移を検査し、異常終了後の report cut 再開や publication 後の cleanup を安全に進めるための主要な state 管理入口である。

## Read this when
- feedback report の state transition、active issue／machine aggregate、current pointer、generation publication の整合性を調べるとき
- report cut の入力 snapshot、normalization／remediation checkpoint、incomplete 診断、publication artifact、cleanup target の検証や復旧を確認するとき
- feedback state の破損検出、canonical JSON／SHA256 artifact reference、writer lock、publication 後 cleanup の挙動を追跡するとき

## Do not read this when
- observation の受付・保存や reporter 入力の収集だけを調べるとき
- feedback report の実行 orchestration や remediation call の具体的な run state 検証だけを調べるとき
- Markdown report の表示内容や app specification の正本を確認することが目的のとき

## hash
- b02d842124283f94ffd2958432289e41adbfe6e6730e090b5957318b4ae111a2

# `runtime_feedback_store.py`

## Summary
- `runtime_feedback_store.py` は、agent および allowlist machine rule の feedback observation を検査・秘匿化・正規化し、重複排除可能な immutable raw record として durable store に発行する境界である。
- reporter schema 検証、payload サイズ制限、secret masking、repository 内 evidence path の fingerprint、UUIDv7／決定的 observation ID、content hash、atomic publish、temporary recovery、pending 件数・蓄積警告までを一体として扱う。

## Read this when
- feedback observation の受理条件、保存される raw envelope、secret masking、evidence path の安全性、immutable storage、重複・破損検査を確認するとき。
- agent または machine rule の observation 保存経路、publication の atomicity、pending observation の列挙・完了件数警告を調べるとき。

## Do not read this when
- feedback report の cut、state 更新、公開済み cleanup、または MCP の外部報告契約そのものを確認したいときは、対応する feedback state／report 実装を直接読む。
- 一般的な console・file log の仕様や reporter input schema の定義だけを確認したいときは、この store の実装ではなく各正本仕様・schema resource を読む。

## hash
- 941cc06d8889d6a0169f11c96313b20c2dac590c088e5b2a1a1ae275b943ef3b

# `runtime_git.py`

## Summary
- Git コマンド実行、branch と linked worktree の作成・削除、安全性検証を共通化する境界。
- 追跡状態と Git ignore を検証し、worktree の filesystem snapshot 復元や oracle/realization file の列挙・分類を担う。
- repository path、Git index、ignore source、symlink・特殊 file の扱いを横断して確認するための入口。

## Read this when
- Git の状態、branch、linked worktree、worktree path の安全な作成・削除を調べるとき。
- 作業成果物の snapshot、復元、symlink や特殊 file を含む filesystem 状態の扱いを確認するとき。
- oracle file または realization file の列挙・分類、追跡状態、Git ignore 判定の実装を変更・調査するとき。

## Do not read this when
- Git 境界を利用する個別 caller の業務フローだけを確認すればよく、共通の Git・path 安全性や file 分類の挙動を調べないとき。
- oracle または realization の正本仕様や分類根拠そのものを確認したいときは、対応する仕様文書を直接読むとき。
- 単一のエラー型、path 定義、結果型の詳細だけを確認する場合。

## hash
- 74ab70dc5c7b257b39a0441b309587dd6023faa9930a21304f46b6901b6274d9

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
- 非対話サブコマンドの primary report を、確定済みの runtime 情報から保存・検証・更新する共通処理。
- 個別 report が未作成の終了経路では、command 別 spec と terminal 結果から fallback report を生成する。
- report context の管理、項目の alias 解決、保存失敗時の cleanup、既存 report の原子的更新を担う。

## Read this when
- 非対話サブコマンドの primary report 保存、fallback 生成、既存 report の再利用を確認するとき。
- report 項目の確定値、command 別の補正、context と result details の統合を調べるとき。
- report 保存の失敗処理、部分 file の除去、通常 file・symlink・空 file の検証を確認するとき。

## Do not read this when
- primary report の項目定義や Markdown 表現を確認したいとき。
- 個別サブコマンドの処理手順や終了条件を確認したいとき。
- runtime logging、path、result 型の専用責務だけを確認したいとき。

## hash
- 95a22909f6d96cb2b44038b59c2fbf853761033dbb0f3f2764c0b12832c7121d

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
- editing run の worktree 解決、run state のライフサイクルロック、親 run process と Codex child process group の tracking・同一性検証・停止・cleanup を束ねる共通 runtime 境界。

## Read this when
- editing run の join、abandon、error cleanup、process tracking、worktree lookup の挙動を確認または変更するとき。
- run process や Codex child group を PID・start time・process group の検証付きで停止する処理を追跡するとき。
- run worktree の安全な解決条件、tracking file の fail-closed な扱い、cleanup 前の process 停止順序を確認するとき。

## Do not read this when
- run の公開仕様や worktree 配置規則そのものを確認する場合は、先に該当する oracle/app specification を読むとき。
- Codex process の起動・tracking file への child 登録など、この module が呼び出す個別の低レベル実装だけを直接確認する場合。
- editing run と無関係な Git 操作、一般的な process 制御、または別の runtime 境界を調べる場合。

## hash
- a30b60027e1b29689ed75c899c6ff56b1da6dd685a01d697ccad6f5b8d351a34

# `runtime_run_join.py`

## Summary
- editing run の join 処理で、session と run の差分検査、merge、INDEX 再生成、refactor state 同期、失敗時の復元・report 記録を共有する処理の入口。
- merge 済み run の worktree と branch を到達可能性と削除結果を確認しながら cleanup する処理も担う。

## Read this when
- editing run の join が想定外差分、INDEX.md 限定 conflict、merge 後処理、session 復元、run 資源 cleanup の挙動を確認・変更するとき。
- 明示的な join と self-joining workload が共有する検証・merge・post-join の流れを追うとき。

## Do not read this when
- run の開始や通常の process tracking、状態モデル、report の個別フォーマットだけを確認したいときは、それぞれの専用 runtime モジュールを直接読む。
- join や cleanup に関係しない refactor、doctor、INDEX 生成の一般仕様だけを確認したいとき。

## hash
- ce45163af61ed1866924e7db60775bdf49b90c93c76866c8a9f16a69c436eb5e

# `runtime_run_lifecycle.py`

## Summary
- 明示的な join を必要とする editing run の開始から終了までを、EditingRunContext と lifecycle lock で一貫して管理する共通処理。
- run の state 遷移、worktree・commit 管理、差分分類、INDEX 更新、cleanup 判定を担当する editing run lifecycle の実装入口。

## Read this when
- editing run の開始、active run の解決・recovery、joinable/error への state 遷移を確認するとき。
- run worktree の commit・rollback、変更 path の分類、想定外差分の検出、INDEX 更新、branch/worktree cleanup の挙動を確認するとき。

## Do not read this when
- editing run lifecycle の正本となる設計・挙動仕様を確認する場合は、先に対応する oracle 文書を読むとき。
- editing run と無関係な runtime 共通処理や、個別の realization 実装・テストだけを確認するとき。

## hash
- c70574929f48b54fff769df3d424fa780771a96561cfa7365458a4d275830e30

# `runtime_run_report.py`

## Summary
- editing run の fork report と lifecycle report を、YAML Front Matter、完了結果、変更パス、実行段階、関連ログを含む Markdown として生成・保存する共通処理。
- run join/abandon のライフサイクルレポートでは、既存の pending report を安全に最終結果へ更新する入口も担う。

## Read this when
- editing run の fork または run join/abandon に関するレポート生成・保存・更新処理を確認したいとき
- 実行レポートへ状態、完了理由、変更パス、実行段階、関連ログを反映する処理の入口を探すとき
- レポート内で Git path を Markdown として安全に描画する処理を確認したいとき

## Do not read this when
- レポートに含める共通項目や canonical な配置規則を確認したいときは、参照コメントに示された設計・仕様文書を読むとき
- EditingRunContext の状態や run lifecycle 自体の定義を確認したいときは、その専用実装へ進むとき
- 実行段階や関連ログの具体的な内容を確認したいときは、それらを提供する logging 実装へ直接進むとき

## hash
- 7d1e833ac3dfed7166aa0416f412a5bb1bf7da3f834eafeefcd6695a870bc3b9

# `runtime_state.py`

## Summary
- session と editing run の永続 state を表すデータ構造を定義し、JSON schema の厳密な検証・復元・安定保存を担う。
- session branch / run branch から対応する session-id と state を解決し、state file の安全な読み書き、symlink・path 種別・session-id・branch 形式の検査を提供する。
- session fork の repository 共通排他 lock と、home branch に紐づく active session state の検索を提供する。

## Read this when
- session state JSON の構造、状態値、必須 field、不変条件を確認したいとき。
- session branch または run branch から state を読み込む処理、state の永続化や安全性検証を変更・調査するとき。
- session fork の排他制御や home branch に対する active session の解決経路を確認するとき。

## Do not read this when
- session や run の具体的な CLI 操作手順・状態遷移の仕様を確認したいときは、対応する sub_command または正本仕様を直接読む。
- git branch の命名規則全体や worktree isolation の設計を確認したいときは、branch model / run isolation の仕様を直接読む。
- CmocError の共通形式や個別コマンドのエラー処理だけを調べるとき。

## hash
- ebff5adf5cf78205ad0b5c21374ad6f6b3c0574eab63f5cd56b0677345dde4da

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
