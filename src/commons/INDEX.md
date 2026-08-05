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
- CLI サブコマンドの共通実行ライフサイクルを管理するモジュール。work root 検査、doctor preprocess、サブコマンドログ、step 通知、完了サマリー、戻り値と例外のエラー処理を一元化する。

## Read this when
- CLI サブコマンドの共通実行経路、ログ記録、step 通知、完了表示、終了コード化、例外表示を変更・調査するとき
- サブコマンド実行前の work root 検査や doctor preprocess の適用範囲を確認するとき

## Do not read this when
- 特定サブコマンド固有の処理、doctor preprocess の修復内容、ログの保存形式自体を変更・調査するときは、それぞれの実装モジュールや対応する oracle を先に読む

## hash
- 32db723142717e6b038a1ae8c3fba66bc7e23e144d95477b0dd2638a40440e4c

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
- 1 回の Codex exec 呼び出しにおける subprocess 実行、実行条件・prompt・入出力ログの保存、失敗分類、capacity retry、quota 待機と代表 probe、session resume、Structured Output の JSON Schema・事後条件検証、出力補正、成果物復元、console/subcommand event 記録を統合制御する状態機械。exec 実行制御とその再試行・検証ライフサイクルを確認する必要がある場合の実装入口であり、ログ形式や個別の Codex profile 処理、設定、パス、結果型の詳細だけを確認する場合は対応する分離 module を読む。

## Read this when
- Codex exec の呼び出し結果、retry、quota 回復待機、resume、Structured Output 検証・補正、作業成果物の保護、call log/event の記録動作を変更または調査するとき。
- 1 回の agent call における subprocess 実行から最終結果返却までの状態遷移や責務境界を把握するとき。

## Do not read this when
- Codex CLI の引数・環境変数・エラー分類・schema 準備など個別の補助処理だけを確認するときは、対応する profile module を直接読む。
- console/subcommand ログの形式だけを確認するときは、logging module を直接読む。
- 設定読み込み、パス生成、git snapshot、結果型の定義だけを確認するときは、それぞれの専用 module を直接読む。
- TUI 起動や exec 以外の CLI 分岐を調査するとき。

## hash
- 14672b4dd11482d7537a16d7e35e3004ed10f70a19e2c276b95aea4acb526206

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
- Codex CLI subprocess 境界の実装。起動前の sandbox・argv・CODEX_HOME・schema 準備、実行中の child process tracking と安全な process group 停止、実行後の JSON/JSONL 出力解析および capacity・quota・予期しない error 判定を担う。Codex 呼び出しの実行環境や機械的結果を扱う下位実装への入口。

## Read this when
- Codex CLI に渡す sandbox、config override、model provider、CODEX_HOME、subprocess 環境を変更・調査するとき
- editing run における Codex child process の tracking、PID reuse 対策、process group の停止や cleanup を変更・調査するとき
- Structured Output schema の配置、Codex JSONL の session ID 抽出、error・capacity・quota 判定を変更・調査するとき
- Codex subprocess の起動失敗や実行結果の利用者向けエラー変換を確認するとき

## Do not read this when
- Codex CLI 境界を呼び出す上位の業務フローや editing run 全体の仕様を確認することが目的のときは、まず該当する oracle 仕様または呼び出し側実装を読む
- Codex subprocess と無関係な設定値の検証、ファイル内容の hash store、一般的なパス解決の実装を調べるとき
- Codex CLI 以外のプロセス管理、出力形式、エラー分類を調べるとき

## hash
- 45eaeb28c80306a97db3a0786ddbd2fbb9a23aa8bb0997c6daa84125704c94ef

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動処理を担う共通モジュール。設定上書き引数、作業ディレクトリ、Codex ホーム、呼び出しログ、成功・失敗イベントを準備・記録し、Codex CLI/TUI を実行する。

## Read this when
- Codex TUI の起動方法、引数や環境の準備、作業ディレクトリの指定を変更・調査するとき
- Codex 呼び出しログ、実行時間、終了コード、成功・失敗イベントの記録を変更・調査するとき
- Codex CLI/TUI 起動失敗時の例外変換やエラー報告を変更・調査するとき

## Do not read this when
- Codex の設定値や上書き引数の生成規則そのものを変更・調査するときは、設定・プロファイル関連の実装を先に読む
- Codex 呼び出し以外の共通ログ、パス、コマンド結果の一般仕様だけを変更・調査するときは、対応する専用モジュールを直接読む

## hash
- fc6bd1b828fb6a9abeb346b20ba9165c1f93a27b137d14da41f37c9c2453cfeb

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
- doctor preprocess の修復ライフサイクル全体を担う実装。doctor lock による排他、修復対象の同期、Git index の退避・一時 index への修復差分合成・復元、修復 commit、追跡状態の検証を扱う。doctor preprocess の挙動や Git common directory／index の不変条件を変更・調査するときの主要な入口。

## Read this when
- doctor preprocess の修復処理、修復 commit、並行実行時の排他を変更または調査するとき。
- ユーザーの staged 状態を保ったまま .gitignore、.agents、config、refactor state を修復する処理を確認するとき。
- Git index の退避・一時 index の合成・復元、HEAD 起点の commit lifecycle、失敗時の復元挙動を確認するとき。

## Do not read this when
- doctor preprocess 以外の一般的な Git 操作や runtime 設定同期だけを変更・調査するときは、それぞれの担当モジュールを直接読む。
- doctor の CLI 引数や利用者向けエラー仕様だけを確認するときは、コマンド定義または対応する仕様文書を先に読む。

## hash
- d37e5ea4aa000b9ef2c08b54122aa15f2a9313c6df4e8eca700888205fbd935a

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
- サブコマンド単位の JSON Lines ログ記録と実行時間集計を担う runtime logging モジュール。イベント追記、step timing、quota 待機時間、ContextVar 経由の logger 参照を提供する。

## Read this when
- サブコマンドのログイベント形式、step の開始・完了計測、経過時間や quota 待機時間の集計を変更・調査するとき
- runtime helper から現在のサブコマンド logger を取得・設定・復元する処理を確認するとき
- ログファイルの生成先や一意な timestamped path の確保と、この logger の連携を確認するとき

## Do not read this when
- CLI サブコマンド固有の処理や console 出力の表示仕様だけを調査するときは、該当する command 実装または console 関連モジュールを直接読む
- runtime path の一般的な定義やログディレクトリの構成だけを調査するときは、runtime_paths モジュールと対応する oracle 文書を直接読む

## hash
- 37a9742cfd233aebdde8d02ae426db9eb479df2f0e94238fee7aae903baa44eb

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
- 編集 run と lifecycle の Markdown + YAML Front Matter report を生成する共通処理。report 保存先の作成、timestamp 付きパス予約、実行コンテキストや完了状態などの共通項目の出力、変更パス・警告・詳細情報の Markdown 化を担う。関連する report 仕様や report 出力処理を変更・調査するときの入口となる。

## Read this when
- fork report または lifecycle report の生成内容、YAML Front Matter、Markdown 本文、保存先、ファイル名予約の挙動を変更・調査するとき。
- report に出力する共通実行状態、完了理由、変更パス、警告、追加フィールドの扱いを確認するとき。
- YAML scalar や Git path の Markdown 安全なエスケープ処理を変更・調査するとき。

## Do not read this when
- run のライフサイクル状態遷移や EditingRunContext 自体の仕様を確認したい場合は、runtime_run_lifecycle の実装または対応する仕様を直接読む。
- report の保存先や timestamp 生成の詳細だけを確認したい場合は、runtime_paths の実装を直接読む。
- report の利用者向け出力仕様そのものを確認したい場合は、対応する oracle document を先に読む。

## hash
- aa17bfbf0ae862cd6f69617cb193b9ae00553ee2cc7737d64e8de7f8c1414b00

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
