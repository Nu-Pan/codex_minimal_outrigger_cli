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
- INDEX.md の検査・再生成・復元・Git commit までのライフサイクルを統括する共通実装。
- 対象ディレクトリと子要素を列挙し、既存 entry の hash による再利用判定、不足 entry の Codex 生成、Structured Output の描画を行う。
- symlink・特殊ファイル・binary・git ignore・memo などを除外し、対象ファイルやディレクトリの内容から鮮度判定用 hash を計算する。
- 更新時は repository 単位の lock、深さ順処理、失敗時の INDEX.md 復元、必要な差分だけの indexing commit を扱う。

## Read this when
- INDEX.md の自動生成や更新順序、entry の再利用条件を変更・調査するとき
- INDEX.md 対象の除外規則、hash 計算、既存 entry の形式検証を確認するとき
- indexing の並列 Codex 呼び出し、lock、失敗時復元、Git commit の挙動を確認するとき
- Codex の Structured Output から INDEX.md entry を組み立てる処理を変更するとき

## Do not read this when
- INDEX.md entry の内容そのものを作成・修正したいだけで、生成ライフサイクルの実装を確認する必要がないとき
- Codex 呼び出し用の entry 生成パラメータ仕様を直接確認したいときは、index entry builder の対象を読むとき
- INDEX.md の正本仕様や運用ルールを確認したいときは、oracle の indexing 仕様を直接読むとき

## hash
- 4ba775165c440665c11e7e25f5005aeb4fd35e013cccda0e900ef6a2893f9c39

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
- 最外側 CLI サブコマンドの実行ライフサイクルを統括し、作業ディレクトリ検査、doctor 前処理、診断ログ、feedback 回収、例外処理、終了コードを管理する。
- 正常完了・ユーザー中断・エラーの terminal result を統合し、primary report の保存、サブコマンドログへの終了イベント記録、コンソール表示、Windows 通知までを一元化する。
- step 開始通知、中断状態や TUI 起動境界の記録、terminal result の JSON/Markdown 変換など、CLI 共通ランタイム処理への入口となる。

## Read this when
- CLI サブコマンド全体の開始から終了までの制御、終了分類、終了コード、例外時の表示やログ記録を調査・変更するとき。
- primary report、feedback observation の回収、診断ログ、terminal result、Windows 通知がサブコマンド終了時にどう連携するか確認するとき。
- トップレベル step の進行通知や、work root 実行前提、ユーザー中断・TUI プロセス境界の共通処理を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや、その実装が返す固有の TerminalResult 内容だけを調べたいとき。
- エラー型、ログ出力、feedback 保存、primary report 保存、パス解決、Windows 通知の個別実装を直接確認したいときは、それぞれの専用 runtime モジュールを先に読むべきである。

## hash
- f9dfb095fd9f0ffaf1bf2f1c624175119f0fbb102a5debfa87ad5c730d715266

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
- 1回の agent call に含まれる Codex CLI 実行の状態機械を担当し、Structured Output の読み取り・JSON Schema 検証・補正、capacity retry、quota 回復待ちと probe、resume 継続、subprocess 結果・call log・subcommand event・各種 counter の共有を一体的に扱う。
- TUI 起動など別の実行経路ではなく、Codex exec の subprocess 起動制御、prompt/output ログ、session ID、検証失敗時の補正処理を調べるための入口である。

## Read this when
- Codex CLI の起動引数、環境、標準入出力、prompt または output log の保存方法を確認・変更するとき。
- Structured Output の JSON parse・schema・事後条件検証、補正 prompt、capacity retry、quota 待機、resume 継続の挙動を確認するとき。
- Codex exec に関する call log、subcommand event、session ID、worktree snapshot の連携を追うとき。

## Do not read this when
- TUI 起動や exec 以外の実行経路の実装を確認したいときは、該当する別 module を読む。
- Codex 実行を利用する上位ワークフローの目的や分岐だけを確認したいときは、まず呼び出し側を読む。
- Codex CLI 自体のプロファイル・エラー分類・subprocess 低レベル補助の詳細だけを確認したいときは、import されている runtime_codex_profile を直接読む。

## hash
- 0c9bb28b1042abee475a9ac7fca04abed8c089c8eeae43a6b96c80d8925e54c1

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
- Codex CLI の subprocess 境界を担い、実行環境・sandbox/argv・CODEX_HOME・MCP/Hook 設定・schema 配置、プロセス追跡と停止、JSONL 出力・resume token・エラー分類をまとめて扱う。

## Read this when
- Codex CLI の起動引数、環境変数、設定 override、schema、または実行結果の解釈を変更・確認するとき
- Codex subprocess の PID/プロセスグループ追跡、停止、PID 再利用対策、tracking file の安全性を確認するとき
- Codex CLI の capacity/quota/unexpected error 判定や resume token 抽出の実装を確認するとき

## Do not read this when
- Codex CLI 境界ではなく、一般的なランタイム設定・パス・エラー・feedback の個別実装を確認するときは、それぞれの専用モジュールを直接読むべきです
- このモジュールを呼び出す上位の run/edit フロー全体の仕様や UI 挙動だけを確認するときは、先に該当する呼び出し元を読むべきです

## hash
- 4a7ae4470fcd971c79a731969723791dc46d8fffff04b7a11d253b1f57f5aa6e

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動前検証、設定上書き argv の構築、通知・入力引き渡し・feedback 用環境の準備、call log の保存、Codex サブプロセス実行、成功・失敗イベント記録を一体で担うランタイム入口。

## Read this when
- Codex TUI の起動条件、実行時環境、設定上書き、通知フック、editor input handoff、feedback 連携、call log、終了コードや失敗処理を確認・変更するとき。

## Do not read this when
- Codex CLI の argv や provider 設定そのものの定義だけを確認したいときは、設定・profile 側の実装を直接読む。
- ログの JSON 形式や共通 logger の動作だけを確認したいときは、ログ関連の実装を直接読む。
- Windows 通知、feedback、editor input handoff の個別実装だけを確認したいときは、それぞれの専用モジュールを直接読む。

## hash
- 62811e0fac78a60c799432f482ea88bcb59880589f1a73896fff0f978d61e428

# `runtime_config.py`

## Summary
- cmoc の実行時設定を JSON と正本設定型の間で変換・検証・保存・読み込み・同期するモジュール。
- Codex の model provider、agent call、モデル名、reasoning effort、整数設定、および JSON/TOML 互換値を検証し、不正値や循環・深すぎる構造を利用者向け CmocError に変換する。
- 設定パスの symlink・特殊ファイルを拒否し、既定値を補完した設定の復元、未作成時の既定設定生成、安定した JSON 書き戻しを提供する。

## Read this when
- 設定 JSON の形式、既定値補完、型検証、Codex 関連設定の復元方法を確認したいとき。
- 設定ファイルの読み書き、同期、symlink や不正 JSON に対するエラー処理を変更・調査するとき。
- JSON/TOML の双方で保存可能な provider-local 設定値の制約を確認したいとき。

## Do not read this when
- 個別の設定値が実行時にどう利用されるかだけを知りたいときは、その設定を消費する呼び出し元を直接読む。
- 設定項目の正本定義や利用者向け仕様を確認したいときは、oracle の設定型・仕様文書を直接読む。
- 設定ファイルの実際の場所やパス計算だけを確認したいときは runtime_paths.py を読む。

## hash
- a457e807e76725701f62337ebeeb9a20f81ee490608cef1010c117ed9c3b9609

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
- エディタ待機中に単一の editor work file を一時 target として公開し、認証付き loopback TCP 経由でガイド取得または UTF-8 内容の全体上書きを受け付ける実行時 handoff 境界。
- 対象ファイルの regular file・非 symlink・所定 editor work directory 内という制約を検証し、target ID、プロトコル、repository、入力 payload を検査する。
- handoff guide の生成・提供・安全な削除、接続の直列化、受付終了後の cleanup、失敗時の利用者向けエラー変換までを担う。

## Read this when
- editor work file を editor 待機期間に公開・取得・上書きする実行時フローを確認するとき。
- loopback IPC の認証、target ID、handoff request の検証、取得・上書き結果の扱いを追跡するとき。
- editor work file や一時 guide の symlink 対策、所在検証、cleanup の安全性を確認するとき。

## Do not read this when
- プロンプト本文の生成や editor input handoff guide の文面定義そのものを確認したいときは、guide 生成側を直接読む。
- エディタからの入力要求を発行する上位フローや、IPC プロトコル定数・認証方式の定義を確認したいときは、利用側または protocol モジュールを直接読む。
- editor work file の内容解析・編集操作・CLI の通常の入力処理を確認したいとき。

## hash
- ef3c7e60d6e7c3fc5f224b72ccaa3c7dcfe7e88554c19a18579be955053ce91d

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
- cmoc の実行時例外と利用者向け失敗メッセージの共通処理を提供する。
- CmocError にエラー概要、復旧・調査手順、詳細情報、任意の端末結果を保持させ、safe_text で診断値を UTF-8 表示可能な文字列へ変換する。
- render_error は CmocError と未処理例外を利用者向けの簡潔な handled failure 形式へ描画し、ログ初期化前などの失敗境界から利用される。

## Read this when
- 実行時エラーを利用者向けレポートへ変換する処理を変更・確認するとき。
- CmocError の保持情報、既定の次の操作、診断値の安全な文字列化を確認するとき。
- サブコマンドや共通処理が CmocError を生成・捕捉する際の共通インターフェースを確認するとき。

## Do not read this when
- 特定サブコマンド固有のエラー発生条件や復旧手順を確認したい場合は、そのサブコマンド実装を直接読む。
- 端末結果の構造や意味だけを確認したい場合は runtime_results の定義を直接読む。
- エラー報告の保存・更新やログ初期化後の一次レポート処理を確認したい場合は、対応するレポート実装を直接読む。

## hash
- 7aebf501056b06c1339e7a20e20c997aec60001f55a492420dbdf02dc935e836

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
- Gitコマンド実行、ブランチとworktreeの管理、worktree状態のスナップショット・復元を担う共通境界。
- Git ignore の検証・設定と、oracle／realization file の分類および nested repository を含むファイル走査を提供する。
- 同階層の個別ランタイム実装ではなく、Gitのpath正規化・状態検証・安全性不変条件を横断的に扱う入口として読む対象。

## Read this when
- Gitコマンドの実行結果、現在のbranchやHEAD、clean worktree判定を確認または変更するとき。
- run worktreeの作成・削除、managed branchの判定、snapshot取得・復元の挙動を追うとき。
- `.cmoc/gu/` のignore制御、Git ignore判定、oracle／realization fileの分類規則を確認するとき。

## Do not read this when
- Gitとは無関係な共通ランタイム機能を調べるときは、該当するruntime実装を直接読む。
- 上位機能の呼び出し順や利用目的だけを確認する場合は、まずその呼び出し元を読み、このファイルのGit境界実装まで進む必要はない。
- 特定のoracle／realization仕様本文の意味を確認する場合は、分類処理ではなく該当するoracle文書を直接読む。

## hash
- 259518514122fe14c7657e049c409f288381405c4a12e2d72eafa2975b1f19e4

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines 実行イベント、警告、step 計測、Codex quota 待機時間をスレッド安全に記録・集約する共通 logger と、現在の実行コンテキストから参照するための ContextVar 操作を提供する。

## Read this when
- サブコマンドのイベントログ、ログファイルへの即時 flush、step の経過時間、警告、quota 待機時間の集計を変更または調査するとき
- runtime helper から現在のサブコマンド logger を取得・差し替え・復元する流れを確認するとき

## Do not read this when
- 個別サブコマンドの業務処理やイベント payload の生成元を調べるときは、その呼び出し元を直接読む
- ログ保存先のパス生成やフィードバック検出の詳細だけを調べるときは、それぞれの専用モジュールを直接読む

## hash
- 40bb2fff7a655247514fdf91c55a4f3375c733d25c84e0a751771d45edd6147a

# `runtime_paths.py`

## Summary
- cmoc の repository root・worktree root・cmoc 自身の root を解決し、解決失敗を実行時エラーへ変換する共通 API。
- timestamp と console 用時刻、duration の表示整形、および timestamp 付きファイルの排他的予約を提供する。
- session・report・log・editor・worktree・schema・config・refactor state など、cmoc が利用する保存先 path を一元的に組み立てる。
- process-wide な cwd 切替を lock と context state で安全に管理し、cwd 前提の処理を直列化する。

## Read this when
- root の解決、保存先ディレクトリや設定・state path の場所、時刻・duration の表記、または cwd 切替の並行実行時の挙動を調べるとき。
- runtime path API を利用する複数のサブシステムにまたがるパス関連の不具合を、共通実装から確認するとき。

## Do not read this when
- 特定サブコマンドの業務ロジック、ログ内容、設定値の意味そのものを調べるとき。
- 個別の保存データ形式や root 解決元の低レベル実装を直接確認すべきときは、それぞれの呼び出し側・設定実装・path model を読むべきである。

## hash
- 4216425d84f307e83f7abb0d1ba5e7535b57366d97e092ac9a51f953d2021079

# `runtime_primary_report.py`

## Summary
- 非対話サブコマンドの primary report context を管理し、既存レポートの検証・追記または未作成時の fallback レポート生成を担う。
- レポート項目を実行結果・終了分類・logger・invocation 中の確定値から組み立て、安全な一時ファイル置換と保存確認を行う。

## Read this when
- 非対話サブコマンド終了時の primary report 保存経路や fallback 生成を確認したいとき
- report の項目収集、既存レポートへの実行記録追記、保存失敗時の扱いを変更・調査するとき

## Do not read this when
- レポートの項目定義や Markdown 描画形式そのものを確認したいときは、先に runtime_primary_report_specs.py または runtime_primary_report_render.py を読む
- 終了結果の生成やサブコマンド固有の処理を確認したいだけで、primary report の保存・補完経路に関係しないとき

## hash
- b9af89f7a318419a73703cefb4869c39e19347779f569cdaaea1fe0d708a5e9c

# `runtime_primary_report_render.py`

## Summary
- 確定済みの runtime 情報と処理分類に基づき、複数の invocation 種別（doctor、indexing、session 操作、feedback、oracle edit、realization apply など）に対応する fallback primary report の front matter・本文・実行記録を描画する共通レンダラー。
- Codex 最終出力、受理済み feedback observation、実行済み step、警告・エラー、次の操作、関連ログを安全に Markdown 化する補助関数群も提供する。

## Read this when
- runtime の実行結果を primary report としてどの形式で表示するか確認・変更したいとき。
- 特定の invocation 種別に固有の report セクション、状態表示、checkpoint、cleanup、merge、feedback publication の表現を調べたいとき。
- 実行記録や Codex 出力、feedback observation の Markdown 埋め込み方法を確認したいとき。

## Do not read this when
- report の仕様上の正本や各 invocation の入力・状態遷移そのものを確認したいときは、参照される oracle 文書や runtime の spec・results・呼び出し元を直接読む。
- ログの記録方法、feedback の保存・マスキング、端末結果の分類ロジックを変更・調査するだけなら、それぞれの担当モジュールを直接読む。

## hash
- e1696f196e1379586669839e4d1e6905712024504a45bb92b3879fa60968dfc1

# `runtime_primary_report_specs.py`

## Summary
- fallback primary report のサブコマンド別仕様を登録し、保存先・役割・タイトル・必須フィールド・テンプレートを一元化する定義ファイル。
- command 名から対応する PrimaryReportSpec を取得する lookup 関数を提供し、doctor、indexing、session、realization、run、feedback 系の非対話末端サブコマンドを対象とする。
- TUI 通知境界の tui と oracle investigation は登録対象外であり、primary report 仕様を確認する入口としてこのファイルを読む。

## Read this when
- fallback primary report の対象コマンド、保存先、front matter の役割、タイトル、必須フィールド、テンプレート対応を確認・変更するとき。
- command 名から primary report 仕様を解決する lookup の挙動や、登録済みサブコマンドの範囲を調べるとき。

## Do not read this when
- 実際の report ファイル生成、保存処理、出力タイミングだけを調べる場合は、生成処理を実装する対象を直接読むとき。
- TUI 通知や oracle investigation の仕様、または個別テンプレートの本文形式だけを調べる場合は、それぞれの専用仕様・実装を直接読むとき。

## hash
- 65ca5fc4c11b5cba1fbf37529e57f05ec073d09bc90569b39c1607b75bbc6ed1

# `runtime_refactor.py`

## Summary
- realization refactor の調査状態を管理する共通実装です。state JSON の読み込み・スキーマ検証・安全な保存、oracle/realization file 集合との同期、調査対象の選択、調査要否の更新、相対パス・digest・時刻などの入力検証を担います。

## Read this when
- realization refactor の調査履歴 state の形式、保存・復元・同期規則を確認または変更するとき。
- oracle/realization file から調査対象を列挙し、次の対象を選ぶ処理や調査要否の扱いを確認するとき。
- state path の symlink・非通常ファイル拒否、JSON entry の検証、正規化相対パスや SHA256・timestamp の検証挙動を確認するとき。

## Do not read this when
- realization refactor の正本仕様や state の契約そのものを確認したいときは、先に参照元の oracle 文書を読みます。
- state を利用するサブコマンド固有の処理や UI を確認したいだけのときは、該当する呼び出し元・利用側の実装を直接読みます。
- oracle/realization file の分類・列挙規則だけを確認したいときは、列挙を担う runtime_git 側の実装または対応する仕様を直接読みます。

## hash
- ce6d02c55f306b2ef28ece6045424dd668556d9e5a880211f5224de89953f27d

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
- editing run の worktree 解決、lifecycle lock、run process tracking、process identity 検証、親 run と Codex child process group の安全な停止・cleanup を担う共通 runtime 境界。run の join/abandon や error cleanup で、worktree の安全性または追跡 process の停止確認が必要な場合の入口。

## Read this when
- editing run の branch から安全な worktree を解決する処理を確認したいとき
- run の lifecycle 操作を直列化する lock や process tracking file の読み書きを確認したいとき
- abandon・error cleanup で親 run process または追跡済み Codex child group を PID 再利用や stale tracking に配慮して停止する処理を確認したいとき

## Do not read this when
- run process の起動方法や Codex profile 固有の process tracking 実装を確認したいときは runtime_codex_profile.py を読む
- Git command の実行や worktree metadata の詳細を確認したいときは runtime_git.py を読む
- run state や session fork の正本仕様そのものを確認したいときは oracle/doc 配下の関連仕様を直接読む

## hash
- e4b79dd7896358d8e93f2bde8bb0c9e1a3698c3d4ac4aee8d1405cb328391624

# `runtime_run_join.py`

## Summary
- editing run の join と cleanup で共有するランタイム処理を担う。join 前の doctor 修復差分の分類、session/run worktree の差分検査、run branch の merge、INDEX 再生成、refactor state 同期、失敗時の復元、merge 済み run の worktree・branch cleanup をまとめて扱う。

## Read this when
- editing run の join 処理で、想定外差分の検出・force-resolve、merge conflict の扱い、post-join の INDEX/state 同期、または join 後の資源削除を変更・確認するとき。

## Do not read this when
- session join コマンド固有の入力処理や conflict 解決の入口を確認したいときは、まず該当する subcommand 実装を読むべき。
- doctor、git 操作、state、lifecycle report など個別共通機能そのものの仕様や実装を確認したいときは、それぞれの runtime モジュールを直接読むべき。

## hash
- 46506c97e11174a974708f743af245fcb53f4671b5c59fa683b7a3aba38d237e

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始・復旧・状態遷移と、session/run branch および worktree の整合性を管理する共通実装です。
- work unit の rollback/commit、INDEX 更新、Git 差分の分類、agent や run が変更できる path の検証までを一体として扱います。

## Read this when
- editing run の開始・終了・復旧、state 遷移、run lifecycle lock、branch/worktree の検証を確認または変更するとき。
- work unit の commit/rollback、INDEX 更新、run/session/agent の想定外差分検出や許可 path 判定を調べるとき。

## Do not read this when
- 個別の CLI サブコマンドや workload の実行内容だけを調べる場合は、そのサブコマンドの実装を直接読んでください。
- Git 操作、state ファイル、INDEX 生成の個別プリミティブだけを確認する場合は、それぞれを定義する共通モジュールへ直接進んでください。

## hash
- 0e3867daa6f9b04b9e687306fe011b2ca3f0e46ddccb22bac0f811ef48516b9b

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
