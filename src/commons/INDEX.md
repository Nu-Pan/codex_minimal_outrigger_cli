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
- 最外側 CLI サブコマンドの実行ライフサイクル全体を統括する入口。
- doctor 前処理、実装呼び出し、診断ログ、feedback 回収、primary report 保存、terminal result の記録・表示を一元管理する。
- 正常完了、ユーザー中断、handled failure、internal failure の終端処理と終了コードを扱う。
- サブコマンド step の進捗通知、work root 実行前提の検査、TUI 起動後の中断境界、終端通知の安全な分離を確認するための上位実装。

## Read this when
- CLI サブコマンドの開始から終了までの制御フローを調べるとき。
- terminal result、診断ログ、primary report、feedback observation、Windows 通知が終端時にどう連携するか確認するとき。
- KeyboardInterrupt やその他の例外、非ゼロ return code、TUI process 起動前後の中断処理を確認するとき。
- サブコマンド step のログ記録と stderr 進捗通知、work root の実行前提を確認するとき。

## Do not read this when
- runtime_errors のエラー型や表示文言の定義だけを確認する場合。
- runtime_feedback、runtime_logging、runtime_primary_report、runtime_results など下位モジュールの固有実装を直接調べる場合。
- 個別サブコマンドの業務ロジックや TUI 自体の実装を確認する場合。

## hash
- 8f4ac5632a4344000bad4298ad3a8bcd2b9b2436597b81aaee9f959ceb3dd9ed

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
- Codex TUI を設定済みの実行環境で起動し、呼び出し単位の識別情報・設定・実行結果を call log とイベントへ記録する入口。
- Codex CLI/TUI の起動前準備から subprocess 実行、feedback call の管理、成功・失敗時の CommandResult または CmocError までの実行経路を扱う。

## Read this when
- Codex TUI の起動引数、作業ディレクトリ、Codex home、環境変数、通知フックの組み立てを確認するとき。
- Codex 呼び出しの call log、実行時間、return code、feedback call、logger event、起動失敗や subprocess 失敗の処理を追うとき。

## Do not read this when
- Codex の設定値や profile の解決、通知 callback、ログ payload の整形など、個別の補助責務だけを確認する場合は担当モジュールを直接読むとよい。
- Codex TUI の起動および呼び出し結果の記録に関係しない CLI 処理や一般的な結果型の確認では、この対象を読む必要はない。

## hash
- d46880f576c62bfb24e597933c0fb67f8654a1db7a36f402a90862948ff6c863

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
- サブコマンド invocation に紐づく feedback collector を管理し、Codex call ごとの capability 発行、reporter request の受付・保存・drain、および invocation 終了処理を担う。
- agent observation の payload・protocol・context・rate limit を検証して保存し、collector や reporter の利用不能を degraded event と warning に変換する。
- allowlist 済みの reporter unavailable および Structured Output validation exhausted event を machine observation として検出・保存する。
- doctor が feedback reporter の schema、protocol、MCP tool 面、loopback collector の可用性を検証するための入口を提供する。

## Read this when
- feedback observation の受付・保存経路を確認または変更するとき
- Codex call 単位の capability context、subprocess environment、call 終了時の drain 順序を確認するとき
- invocation-scoped collector の起動・停止、並行 request 処理、rate limit、context 検証を確認するとき
- reporter または collector の degraded event、allowlist detector、doctor による可用性検証を確認するとき

## Do not read this when
- feedback observation の永続化形式や RFC3339・UUID などの store 共通処理だけを確認するときは runtime feedback store を直接読む
- reporter の MCP tool 実装や input schema 自体を確認するときは runtime feedback reporter を直接読む
- feedback と無関係な Git context、logging、または一般的な CLI subcommand 処理だけを扱うとき

## hash
- bed26c8238de67a48450134505611237f0de001ad94562e90d0c9da4758841e2

# `runtime_feedback_reporter.py`

## Summary
- Codex 起動時に使う call-scoped stdio MCP reporter として、submit_observation を JSON-RPC の MCP tool として受け付け、collector へ capability 付きで転送する。
- collector との接続失敗や応答不正を agent-facing の accepted/rejected 結果へ変換し、構造化結果と JSON text の両方を返す。

## Read this when
- cmoc_feedback.submit_observation の stdio MCP 通信、initialize・tools/list・tools/call の処理、または collector 転送時の結果検証と拒否分類を確認するとき。

## Do not read this when
- 観測内容の業務上の採否、保存、秘匿情報検査、レート制限など collector 内部の規則を確認するときは、対応する feedback observation の oracle file を直接読む。
- feedback collector の環境変数、プロトコル定数、入力スキーマの定義だけを確認するときは、参照される runtime feedback 関連ファイルを直接読む。

## hash
- cd16242e628b6df7a2c87c475e91b41af685604592468dd8fdbd10c110a7160a

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
- 非対話サブコマンドの primary report 保存を統括する共通ランタイム処理。
- 個別処理が report を保存していない終了経路では、確定済みの invocation 情報から fallback report を生成し、保存済み report の検証と結果へのパス付与を行う。
- サブコマンド別仕様に応じた必須項目、状態、完了理由、alias を集約して report renderer へ渡す入口。

## Read this when
- 非対話サブコマンドで primary report が作成される条件、fallback 保存、保存済み file の検証を確認するとき。
- oracle edit、feedback report、realization apply/refactor fork などの終了経路で report 項目がどう補われるか調べるとき。
- report context の開始・更新・リセットや、report 保存失敗時の内部エラー処理を追うとき。

## Do not read this when
- 特定サブコマンドの primary report の項目定義や描画形式そのものを確認したいときは、primary report specs または renderer を直接読む。
- report の保存先・timestamp 予約の一般的な仕組みだけを確認したいときは、runtime paths を直接読む。
- 非対話サブコマンドの処理フローや終了分類の定義を確認したいだけで、report 保存経路を調べないとき。

## hash
- d924aa5d44738e53605e8fcdc9d8bbb27487c48557b75ed85e3852c0aef12793

# `runtime_primary_report_render.py`

## Summary
- 確定済み runtime 情報から invocation 用の fallback primary report を描画する。通常の実行概要に加え、feedback publication と混同しない部分結果・checkpoint・cleanup 状態を出力する。
- oracle edit の agent call 状態、feedback publication 状態、実行段階、終端結果、warning/error、関連ログを report 用の確定値として集約する。

## Read this when
- runtime 情報を primary report の Markdown/YAML 表現へ変換する処理を確認するとき
- feedback report invocation の publication・checkpoint・cleanup 状態の表示規則を確認するとき
- 実行済み step、Codex call、warning/error の report 出力内容を追跡するとき

## Do not read this when
- primary report の仕様や分類・結果データ構造そのものを変更または確認するとき
- runtime logging の event 記録方法や logger のライフサイクルを確認するとき
- feedback report の publication 処理自体や active state の管理を確認するとき

## hash
- e8be5ae39e941ecbf5e0297b9bf6c92defef62c05ac7830e74993f811bfbf7f9

# `runtime_primary_report_specs.py`

## Summary
- 日本語の技術文書として、対象モジュールの責務と、fallback primary report のサブコマンド別定義への入口を簡潔に示す。
- 非対話末端サブコマンドの report 保存先・役割・タイトル・必須項目・テンプレートを登録し、command 名から定義を取得する箇所として位置づける。

## Read this when
- fallback primary report のサブコマンド対応を追加・変更・確認するとき。
- command 名に応じた report 仕様、保存先、必須 front matter 項目、テンプレート選択の登録元を探すとき。

## Do not read this when
- TUI の通知境界や oracle investigation の仕様を確認したいとき。
- 個別サブコマンドの report 形式そのものや保存処理を直接確認したいときは、対応する app specification または report 実装を読む。

## hash
- 03ab3079ba4eec09a22bbdb38539c3625c8d8d55adb318403c5d932dfeca0e65

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
- session と editing run の state schema を検証し、JSON として永続化する共通実装。
- session branch・run branch と session state file の対応付け、state の読み込み、session の検索を提供する。
- session fork の排他 lock と、session-id・branch 名・state path の安全性検証を担う。

## Read this when
- session state の JSON schema、state 値、session/run payload の不変条件を確認するとき
- session branch または run branch から state を読み込む処理を調べるとき
- state file の保存、復元、symlink・特殊 file・不正な session-id の拒否を確認するとき
- session fork の同時実行を防ぐ共通 lock の扱いを確認するとき

## Do not read this when
- session や editing run のライフサイクル手順・利用者向けコマンド仕様を確認したいとき
- branch 命名規則全般や worktree 分離の設計だけを確認したいとき
- state schema の具体的な field 定義だけを確認する必要があり、正本の session state 仕様を直接読めるとき

## hash
- 516116886eabbf58130ecd20a993172ec62f0a609709ddafa8d1383447dcd196

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
