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
- INDEX.md の検査・生成・更新・commit までを担う indexing lifecycle の共通実装。対象ディレクトリの列挙、既存 entry の hash による再利用、Codex による不足 entry の生成、Markdown 検証・書き込み、更新差分の commit、排他制御を扱う。

## Read this when
- INDEX.md の自動生成・鮮度判定・entry 再利用・Structured Output 検証を変更または調査するとき
- indexing の対象除外、hash 計算、symlink・binary・Git ignore の扱いを確認するとき
- Codex 呼び出しの並列実行、preflight、lock、worktree・ログ保存先の制約を確認するとき
- INDEX.md 更新の commit や Git failure の処理を変更または調査するとき

## Do not read this when
- INDEX.md entry の文章内容そのものを作成・修正するときは、対象ファイルの本文と entry 生成用の oracle を直接読む
- indexing 以外の CLI 機能、Codex 実行一般、Git 共通処理だけを調査するときは、それぞれの専用実装を読む
- INDEX.md の正本仕様や entry schema の定義を確認するときは、この実装ではなく対応する oracle file を読む

## hash
- 3a12bb8da2be10b857727872e4a63a8e7a443059cb0175388a08707a080ca3ab

# `prompt_editor_input.py`

## Summary
- エディタから AI Agent 用プロンプトを受け取り、初期テンプレートの保存、エディタ選択・起動、入力内容のコメント除去と読み込みを担う共通境界。
- エディタ入力用ディレクトリの作成や一意なタイムスタンプ付きファイルの予約、エディタ終了エラーの cmoc 利用者向け例外への変換、現在の worktree と対象 root の `.cmoc` ignore 保証も扱う。
- プロンプト編集フロー、エディタ選択順、編集ファイルの読み込み・コメント除去、または prompt editor 用 root の ignore 設定を変更・調査するときの実装入口。

## Read this when
- prompt editor または TUI の入力保存・編集フローを調査するとき。
- 利用可能なエディタの選択順、起動引数、終了失敗時のエラー処理を変更するとき。
- HTML コメントを除去したプロンプト入力の読み込みや、編集用ファイルの timestamp 衝突回避を調査するとき。
- editor/TUI が利用する `.cmoc` ignore の保証処理を変更するとき。

## Do not read this when
- プロンプト本文の正本テンプレートや利用者向け仕様を確認することが目的の場合は、対応する oracle doc を直接読む。
- prompt editor 入力を利用した後続の agent 呼び出し、CLI 実行、runtime path・git の詳細を調査する場合は、それぞれの呼び出し元または専用 runtime モジュールを直接読む。
- 一般的なエディタ設定や prompt の内容編集だけが目的で、入力境界の実装を変更しない場合。

## hash
- 5e7022e4bf219323a09a46511b3e637d461996a044331792505fabfcad318d99

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
- Codex exec の単一試行ループを実装する中核モジュール。Codex subprocess の起動、prompt・stdout・stderr・output・call log の保存、Structured Output の JSON/schema 検証、semantic retry、capacity retry、quota availability probe と待機、resume token による再開を一つの状態機械として制御する。exec 実行制御を確認する際の入口であり、TUI 起動処理は扱わない。

## Read this when
- Codex exec の subprocess 起動条件、argv・cwd・環境・CODEX_HOME の検証を調べるとき
- prompt、出力、call log、subcommand event の保存内容や失敗時の記録を確認するとき
- Structured Output の検証と semantic retry の挙動を変更・調査するとき
- capacity error の retry、quota error の代表 probe・待機・resume 継続を変更・調査するとき
- Codex exec の成功・失敗結果や CodexExecResult の組み立てを確認するとき

## Do not read this when
- Codex CLI のログ出力フォーマットや console 表示だけを確認したいときは、専用の logging module を先に読む
- Codex のエラー分類、環境構築、schema 準備、resume token 抽出など個別 helper の実装だけを確認したいときは、runtime_codex_profile を先に読む
- TUI の起動や TUI 固有の分岐を確認したいとき
- 設定の読み込み、パス計算、subcommand logger、結果型の定義だけを確認したいときは、それぞれの専用 runtime module を直接読む

## hash
- b13f481022d9a0c3347bb2a5750f60c79097272697507baa3f19b9e40dede035

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
- Codex exec/TUI 実行前に INDEX 更新 preflight を挟むランタイム連携を担当する。preflight の登録・解除、再入抑止と直列実行、実行対象からの indexing 起点 root 算出、実行本体への委譲を扱う。

## Read this when
- Codex exec または TUI の起動前処理、INDEX 更新 preflight、preflight の有効化・無効化を変更するとき。
- Codex 呼び出し設定から作業 root を決める処理や、preflight の再入・並列実行制御を確認するとき。

## Do not read this when
- Codex 実行本体の subprocess・TUI 実装を変更または調査するときは、runtime_codex の実装を直接読む。
- INDEX の生成規則や oracle 編集サブコマンド固有の仕様を確認するときは、対応する oracle 文書を直接読む。

## hash
- 9a17bb577fe0ed64e036ca1f99b85af81357514dd6f87db9bde3a1d7bbe25e19

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界の実装を担い、起動前の sandbox・cwd・CODEX_HOME・argv/config override・schema 配置と、起動後の process tracking・process group 停止・JSONL 出力解析・error/retry 判定をまとめる。Codex CLI との実行環境および機械的な実行結果を扱う下位実装への入口である。

## Read this when
- Codex CLI の起動引数、sandbox 権限、cwd、CODEX_HOME、provider 設定、Structured Output schema の配置を変更・調査するとき
- Codex subprocess の PID/start time/process group tracking、signal による停止、abandon 時の cleanup を変更・調査するとき
- Codex の JSONL stdout/stderr、thread resume token、capacity・quota・unexpected error の判定を変更・調査するとき

## Do not read this when
- Codex CLI 境界以外の一般的な設定検証、runtime content の hash store、パス解決だけを直接調査するときは、それぞれの専用実装を読む
- Codex のプロンプト本文生成や agent call の上位オーケストレーションの仕様・挙動を調査するとき

## hash
- d9aac07884cd53bf1e07d7a7358cd389ef41c05ee824b19fb92bd0033422c8bd

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを担当する実装。設定上書き argv、作業ディレクトリ、Codex HOME の検証、呼び出しログ、コンソール・イベントログ、成功・失敗時の戻り値や例外処理をまとめて扱う。Codex CLI/TUI の起動経路や実行ログ、失敗処理を確認する際の入口。

## Read this when
- Codex TUI の起動方法、argv や実行環境の準備を変更・調査するとき
- Codex 呼び出しの call log、イベントログ、実行時間、戻り値、例外処理を変更・調査するとき
- Codex の作業ディレクトリや CODEX_HOME の解決・検証を確認するとき

## Do not read this when
- Codex の設定値そのものを変更・調査するときは設定ロード・構成定義側を読む
- Codex の非対話実行やプロファイル解決の内部仕様だけを調査するときは、対応する runtime モジュールを直接読む
- 一般的な CLI ロギングやパス操作だけを調査するときは、各責務を実装する専用モジュールを直接読む

## hash
- d993891d52da34ab34c73d79c78451be3d6dc6a3ff3099fc404558d61b75bf65

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
- Git コマンド実行、branch・HEAD・status、linked worktree の作成削除、安全検証を担う共通境界。
- Git ignore の検査・更新と、oracle file／realization file の repository path・追跡状態による分類を提供する。
- Git repository の状態確認、worktree 操作、ignore 初期化・診断、oracle／realization 判定を実装または変更するときの入口。

## Read this when
- Git subprocess のエラー処理、branch・worktree・commit・status の取得や検証を変更するとき。
- cmoc 管理 worktree の作成・削除、安全な path 検証、symlink や Git metadata の扱いを確認するとき。
- `.cmoc/gu` の ignore 保証、Git ignore source の安全性検証、oracle／realization file の分類条件を変更するとき。

## Do not read this when
- Git 境界や path 分類を使うだけで、共通 helper の挙動を変更しない作業。
- 個別サブコマンドの業務ロジック、prompt の組み立て、runtime error 型や結果型そのものを変更する作業。

## hash
- 09796c4fde82b463f4f3b67c77f1686d5fd4031165bc2a9391d88611b1834d1a

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
- リポジトリ・worktree・cmoc root の解決、実行時 timestamp と duration の整形、session/report/log/schema/config などの標準保存先の算出を提供する runtime path ユーティリティ。cwd を一時変更する処理は process-wide lock と ContextVar で直列化する。

## Read this when
- root path の解決、cmoc 管理ディレクトリや各種ログ・レポート保存先の扱いを変更または調査するとき
- timestamp、duration 表示、timestamp 付き path の排他的予約、cwd 切替の挙動を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容、ログ出力形式、設定スキーマそのものを確認したいとき
- path 解決の基盤実装や root placeholder の定義を確認したいときは、path model 側を直接読む

## hash
- a6083e682746a50b8a97e22b8003317e0fd2b04e7074f12e33e8f228b944ceaa

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
- editing run の process identity と tracking file を管理し、run process および Codex child process group の安全な停止・cleanup を担う共通ランタイムモジュール。worktree 解決や lifecycle lock も提供する。

## Read this when
- editing run の abandon、error cleanup、process tracking、Codex subprocess group の停止処理を変更・調査するとき
- PID 再利用、start time、pidfd、process group snapshot 検証に関わる挙動を確認するとき
- run branch の worktree 解決や run lifecycle の排他制御を確認するとき

## Do not read this when
- CLI の editing run の公開仕様や状態遷移そのものを確認したいときは、対応する oracle doc や上位の run 実装を先に読む
- git 操作、runtime path、runtime error の個別実装だけを変更・調査するとき

## hash
- 2f70df13f070689934af61b2b3650763f3f6852bdc15a6df2798c863d1f955ad

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始から state 遷移、commit、差分分類、INDEX 更新、cleanup 判定までを担う共通 lifecycle 実装。EditingRunContext と lifecycle lock を共有し、session/run の branch・worktree・state の不変条件を管理する各処理への入口。

## Read this when
- editing run の開始、active run の解決・復旧、joinable/error state への遷移を変更または調査するとき
- worktree 差分の commit、rollback、INDEX 更新、agent/run/session の許可 path 判定を変更または調査するとき
- run branch・session branch・state file・managed worktree の整合性や cleanup 処理を確認するとき

## Do not read this when
- 単一の git 操作、path 判定、state model、INDEX 更新処理の詳細だけを確認したいときは、対応する runtime・indexing module を直接読む
- editing run の利用者向け仕様や状態遷移の正本を確認したいときは、対応する oracle document を直接読む

## hash
- 69d910c7db522a9fe1c5847164720a31f4be0b88230d905aa79763e905ec786e

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
