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
- INDEX.md の検査・生成・更新・commit を一貫して管理する共通実装。対象ディレクトリの走査、既存 entry の hash による再利用、Codex による不足 entry の生成、内容検証、書き込み、Git commit、排他制御を扱う。
- INDEX.md の生成 lifecycle に関する実装や、directory traversal、entry schema 検証、hash 鮮度判定、Codex 実行、更新 commit の挙動を変更・調査する際の入口。

## Read this when
- INDEX.md の preflight 更新、深さ順の再生成、既存 entry の再利用条件を変更するとき
- INDEX.md entry の Structured Output 検証、Markdown レンダリング、hash 計算を調査・変更するとき
- INDEX.md の書き込み、symlink・binary・ignored path の扱い、Git commit、repository lock を調査・変更するとき
- indexing から Codex を呼び出す際の context、parallel 実行、worktree・ログ root の扱いを確認するとき

## Do not read this when
- INDEX.md entry の正本 schema や prompt 定義そのものを変更するときは、対応する oracle source または prompt builder の実装を直接読む
- INDEX.md の利用者向け仕様だけを確認するときは、indexing の oracle document を直接読む
- indexing と無関係な CLI command、runtime、Git 操作を変更するとき

## hash
- 533e34ad0f58c8793413ab55929fe7f9d2e4b43036ea58386f9ee9ac41e5cb9f

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
- Codex exec の単一試行ループを実行制御する中核モジュール。Structured Output の厳格な JSON/schema 検証、capacity retry、quota の代表 probe と待機、resume token による再開、prompt・stdout・stderr・output・call log の保存、console/subcommand event の記録を一体で扱う。exec 実行制御の実装を確認する入口であり、ログ整形や Codex プロファイル処理の詳細は分離先モジュールを参照する。

## Read this when
- Codex exec の再試行、quota 待機・probe、resume 継続、Structured Output 検証、実行ログ保存、Codex call event の挙動を変更または調査するとき。
- Codex subprocess の argv、cwd、環境、schema、prompt stdin、失敗分類から最終結果生成までの制御フローを確認するとき。

## Do not read this when
- Codex のエラー分類、schema 準備、resume token 抽出、subprocess 起動など個別 helper の実装だけを確認したいときは、分離された runtime プロファイル系モジュールを直接読む。
- Codex call の console 出力形式だけを確認したいときは、runtime logging 系モジュールを直接読む。
- TUI 起動や exec 以外のサブコマンド実装を調査するとき。

## hash
- c17d813410337f225e231d93db7fc75d7cac6319af7803abc68f0d8aadfed1d0

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
- Codex CLI subprocess 境界の実装。sandbox・argv・CODEX_HOME・provider 設定・schema 配置・process tracking・子プロセス停止・JSONL 出力解析・capacity/quota/error 判定を扱う。Codex 起動環境の構築と、機械的な実行結果を利用者向けエラーや retry 判定へ変換する下位実装への入口。

## Read this when
- Codex CLI の起動引数、sandbox mode、model provider の TOML override、CODEX_HOME、schema 配置を変更・調査するとき。
- editing run の Codex subprocess tracking、process group の安全な停止、PID reuse 対策、signal・lock・cleanup を変更・調査するとき。
- Codex の stdout/stderr、JSONL event、thread resume token、capacity・quota・unexpected error の判定を変更・調査するとき。

## Do not read this when
- Codex CLI の呼び出し元が担う run 全体の orchestration、retry 待機、利用者向けコマンドフローだけを調査するときは、呼び出し元の実装を直接読む。
- Codex の設定値そのものの正本仕様や editing run の外部仕様を確認するときは、対応する oracle file を先に読む。
- Codex CLI と無関係な共通 path・content・config helper の挙動だけを調査するとき。

## hash
- fabe86808acb56a908b0492aef070308c4411cf5630d6829eee1230caeacad6f

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
- Git コマンド実行、branch・HEAD・worktree の検証と作成・削除、Git ignore の安全な更新・検査、oracle/realization file の分類を担う共通境界。repository path、Git index、ignore 状態、worktree metadata の安全性を横断して扱うため、これらの挙動を変更・調査する際の入口となる。

## Read this when
- Git subprocess のエラー変換、branch 状態、clean worktree、status path の扱いを変更・調査するとき
- cmoc 管理 worktree の作成・削除、branch 名からの path 解決、symlink や Git metadata の安全性を確認するとき
- `.cmoc/gu` の ignore 設定、Git ignore source の検証、oracle/realization file の分類条件を変更・調査するとき

## Do not read this when
- CLI の個別コマンドや state/report の処理だけを変更・調査し、Git 境界の共通挙動に関係しないとき
- Git 管理外の一般的な path 操作や、worktree・ignore・oracle/realization 分類を直接利用しない処理を確認するとき

## hash
- d72d562b804fb6f6985663b8e7994bf6cce6a3338a7308f6f675e6edcf3adfd8

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
- リポジトリ・worktree・cmoc ルートの解決、実行時 timestamp と duration の整形、各種 runtime 保存先 path の構築、cwd の一時切替を提供する共通 runtime path helper。関連する CLI の保存先、ログ、session、worktree、root 解決、pushd の挙動を確認する際の入口。

## Read this when
- root placeholder の実パス解決や、repo/worktree/cmoc root の runtime error 処理を変更・調査するとき
- session、report、log、schema、worktree など cmoc 管理ディレクトリの保存先を変更・調査するとき
- timestamp、console timestamp、duration 表示、timestamp path の排他的予約を変更・調査するとき
- process-global な cwd 切替や、cwd 起点の root 解決の thread safety を変更・調査するとき

## Do not read this when
- 特定サブコマンドの保存内容やログ形式そのものを確認する場合は、該当するサブコマンドの実装・oracle doc を直接読む
- path placeholder の定義や root 探索アルゴリズム自体を確認する場合は、basic.path_model の実装・oracle src を直接読む
- runtime path helper と無関係な CLI 入出力、agent call、schema 内容を変更・調査するとき

## hash
- 106740a2370f965eb4c136399ac4b2a49cad93ae5c26c7a975d9599b1c6e13a7

# `runtime_refactor.py`

## Summary
- oracle/realization file の調査履歴を管理する state の読み込み・検証・保存・同期を担当する。対象 file の列挙、未調査対象の選択、調査要否の更新、path・entry・日時・SHA256 の schema 検証、および不正 state の利用者向け例外変換を含む。

## Read this when
- realization refactor の調査対象選択、調査履歴の同期・更新、state file の読み書きや schema 検証を変更・確認するとき。
- oracle file と realization file の列挙条件や、調査履歴の妥当性検証を確認するとき。

## Do not read this when
- CLI の個別サブコマンド処理、一般的な runtime helper、refactor state の仕様そのものを確認したいとき。後者は対応する oracle document を直接読む。

## hash
- 0dc268da40f4c5d47ff20fe8e687d82a25f89103fd82551ce70e5174536860ed

# `runtime_results.py`

## Summary
- Codex exec の構造化出力契約、外部コマンド結果、および exec 実行に伴う生成物・ログ・設定パスを表す型を定義する。runtime 結果の型や呼び出し側契約を確認する必要がある場合の入口となる。

## Read this when
- Codex exec の戻り値契約や構造化出力へのアクセス方法を変更・確認するとき
- 外部コマンドの終了コード、標準入出力、実行ログや生成物のパスを保持する結果型を利用するとき

## Do not read this when
- Codex exec の実行処理そのものを変更・確認するとき
- CLI 入出力やログ保存処理の具体的な挙動だけを調べるとき

## hash
- 9f6e365d5335be51796785b3abc187d63c1d32111ecb9b0ad30308780df063e4

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
- Editing run の開始・active run の解決と復旧、state 遷移、work unit の rollback/commit、INDEX 更新、Git 差分分類、agent/run/session の想定外変更検出、oracle 差分取得、run target の予約を一体で扱う lifecycle 共通処理。EditingRunContext と lifecycle lock を共有するため、editing run lifecycle の実装入口として読む。

## Read this when
- editing run の開始、active run の解決・復旧、joinable/error state の保存を変更または調査するとき
- run worktree の commit、rollback、INDEX 更新、cleanup 判定や branch/worktree lifecycle を扱うとき
- agent・run・session の変更許可範囲、rename を含む Git 差分分類、想定外 path 検出の挙動を確認するとき

## Do not read this when
- CLI の個別 editing run 仕様や state schema の正本を確認したいときは、参照されている oracle 文書を直接読む
- INDEX 更新処理そのものの実装を変更するときは、indexing の共通実装を直接読む
- runtime の path、Git、state、process-id など単一領域の低レベル処理だけを調査するときは、対応する runtime モジュールを直接読む

## hash
- a51c86c1635645a44168f64e286fdb15823ba397a154d07c541eb79c1699f057

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
