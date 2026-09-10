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
- src/commons/indexing.py は、INDEX.md の検査・再利用・生成・ハッシュ鮮度確認・書き込み・復元・Git commit までを一つの indexing lifecycle として実装する共通モジュールです。
- INDEX.md を深いディレクトリから更新する処理、既存 entry の検証と再利用、Codex による不足 entry の生成、更新失敗時の復元を確認したいときの入口です。

## Read this when
- INDEX.md の自動更新順序、対象ディレクトリ・子要素の選別、entry の hash による鮮度判定を調べるとき
- INDEX.md entry の生成 prompt、Structured Output の描画、並列生成、Codex 実行時のコンテキストやログ設定を調べるとき
- INDEX.md の lock、symlink・特殊ファイルの扱い、更新失敗時の snapshot 復元、更新差分の commit を調べるとき

## Do not read this when
- INDEX.md entry の生成 schema や agent 向け prompt の定義そのものを変更・確認するときは、index entry parameter の実装を直接読むとき
- Codex 実行前 preflight の登録や Codex 実行プロファイルの詳細だけを調べるときは、対応する runtime モジュールを直接読むとき
- INDEX.md の利用者向け仕様や更新ルールの正本を確認するときは、app_spec 配下の仕様文書を直接読むとき

## hash
- 8727115c4b41324a52633d2dd9222879c69da53497983ba73d586d48d1775a32

# `prompt_editor_input.py`

## Summary
- AI Agent 向け prompt をエディタで編集し、入力結果を安全に保存・抽出・確定する共通境界を提供する。
- 作業用 file と保存 copy の path 準備、エディタ起動、最終内容の一度だけの保存、完了後の作業 file 削除を扱う。
- 保存先の symlink・親 directory・通常 file 性、入力 copy の repository 内 path、prompt skeleton の placeholder 一意性を検証する。
- prompt editor/TUI 用 repository と現在の worktree の `.cmoc` ignore を保証し、利用可能な editor command を優先順で選択する。

## Read this when
- prompt の editor input 境界、作業 file／保存 copy のライフサイクル、または入力内容の抽出・確定処理を確認したいとき。
- editor input の保存先検証、symlink 防止、path 制約、prompt skeleton の placeholder 検証、エディタ選択や handoff を調査・変更するとき。

## Do not read this when
- prompt の完全な構築規則や editor 初期表示文の正本を確認したいときは、prompt builder 側を直接読む。
- editor handoff の内部実装や runtime error・path・git ignore の一般機能だけを調べる場合は、それぞれの専用 runtime module を直接読む。

## hash
- 5218b3489e652ae0a1eac8fa1e97d33db6170bbb05a02de5bb68d3c557bdf395

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
- 日本語技術文書のルーティング情報として、Codex CLI subprocess 境界の実行環境・argv・設定配置・process tracking・JSONL 結果判定を案内する。
- Codex の起動条件、実行中 process の同一性確認と停止、Structured Output schema の配置、stdout/stderr の error・resume token・capacity/quota 判定を確認する入口である。

## Read this when
- Codex subprocess の sandbox、CODEX_HOME、MCP/environment override、schema 配置、起動失敗、process tracking、abandon 時の process group cleanup を調べるとき。
- Codex JSONL の malformed event、error message、session ID、capacity error、quota error の判定経路を確認・変更するとき。

## Do not read this when
- Codex CLI 呼び出し境界の実装や機械的な結果判定を扱わず、個別の agent call 設定、上位の run orchestration、または MCP reporter 自体の仕様だけを調べるとき。
- 対象の下位関数を直接変更する作業で、既に呼び出し契約と失敗時の境界が明確になっているとき。

## hash
- a53cff5e171b02c01742c1dd432ca6b444d1e9fb607ff447ba2974c725a2ca71

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
- サブコマンド実行中の JSON Lines event、step timing、quota 待機時間、warning、Codex call を記録・集約する logger。
- ContextVar を介して、現在のサブコマンド logger を runtime helper から参照・差し替え・復元するための入口。

## Read this when
- サブコマンドの実行イベントを永続ログへ記録する処理を確認したいとき
- step の開始・終了時間、quota 待機時間、warning、Codex call の集約方法を確認したいとき
- 現在の実行文脈に紐づくサブコマンド logger の取得や一時的な差し替えを確認したいとき

## Do not read this when
- feedback detector の判定や報告処理そのものを確認したいとき
- ログ保存先のパス予約や timestamp 生成の実装を確認したいとき
- サブコマンド logger が生成した primary report の利用側を直接確認したいとき

## hash
- d3550a9d5474f92ae25e4e13b18b45d3ee377682eb578bc909ff4ae4e1fb3f96

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
- 確定済みの runtime 情報から、通常・feedback invocation・refactor fork の fallback primary report を構築する描画処理。実行段階、終端結果、warning/error、次の操作、診断ログ、Codex 最終出力、新規 observation を report へ反映する。
- primary report の YAML front matter、template 別本文、実行記録、feedback publication 状態、Codex call 状態を扱う下位描画ロジックへの入口。

## Read this when
- fallback primary report の出力構造や template 別の本文を確認したいとき
- 実行済み step、終端分類、warning/error、feedback publication 状態、Codex call 記録の report への反映方法を調べるとき
- report に記録される Codex 最終出力や新規 feedback observation の扱いを確認するとき

## Do not read this when
- primary report の仕様上の項目定義や publication の業務要件を確認したいときは、参照元の仕様文書を直接読むとき
- runtime 情報の収集・ログ記録・結果分類そのものを変更または調査するとき
- fallback report の呼び出し側や report 保存処理の責務だけを確認したいとき

## hash
- bf5e67cf6d37203e73a7fefc399eae4ee16e0206f8d0d1c3750c8d82a6ef9a67

# `runtime_primary_report_specs.py`

## Summary
- fallback primary report の個別サブコマンド定義を確認する入口。doctor、indexing、session、oracle edit、realization、run、feedback report の各非対話末端サブコマンドについて、レポート保存先・役割・タイトル・必須項目・テンプレートを登録し、command 名から定義を取得する。

## Read this when
- fallback primary report のサブコマンド追加・変更時に、対象コマンドの保存先、レポートの役割、タイトル、必須項目、テンプレート登録を確認したいとき。
- command 名から個別の primary report 定義を解決する処理を調査するとき。
- session、realization、run、feedback report などの非対話末端サブコマンドが生成するレポート項目の定義を確認するとき.

## Do not read this when
- TUI の通知境界や oracle investigation の仕様を調査するとき。
- レポートの実際の生成・保存処理や、各サブコマンドの実行ロジックを直接調査するとき。
- fallback primary report の個別サブコマンド登録や command 名からの定義解決に関係しない処理を調査するとき。

## hash
- adc63e8e13151af1225a3a6f3ed8e55c17596eda042385c33b258fd216c98974

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
- `runtime_windows_toast.py` は、Windows toast 通知と Codex TUI callback の transport 境界を担う。
- 最外側コマンドの terminal result 通知、TUI の root session 記録と turn 重複排除、通知用一時 state のライフサイクルを扱う。
- 通知内容を短く正規化し、PowerShell/WinRT transport や callback の失敗を本命処理へ返さない非致命的な実行入口を提供する。

## Read this when
- Windows toast 通知の生成・送信経路、通知内容の制約、または transport の timeout／失敗時挙動を確認・変更するとき。
- Codex TUI の SessionStart と turn-complete callback の関連付け、root session の識別、turn 単位の重複排除を調べるとき。
- TUI callback 用の一時 state、実行中 marker、callback drain、cleanup の扱いを確認するとき。

## Do not read this when
- 通知や TUI callback ではなく、コマンド本体の terminal result を決定する処理を変更・調査するとき。
- Codex hook の仕様そのものや、通知を呼び出す上位の CLI orchestration だけを確認すれば足りるとき。
- Windows 以外の一般的な表示・ログ出力 transport を扱うとき。

## hash
- 7742546cee921a9da07c022eab3f6a9212d4d1e5cadf6da59f6f8c626e7b948c
