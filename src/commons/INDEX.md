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
- cmoc のランタイム共通 API を集約して再公開するモジュール。設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果型など、CLI 実装が横断的に利用する関数・定数・型の入口となる。

## Read this when
- 複数の runtime commons 機能を利用する CLI 実装や、その公開 API の追加・変更・参照箇所を確認するとき。
- cmoc の共通ランタイム API の import 元や再公開対象を確認するとき。

## Do not read this when
- 特定のランタイム機能の内部実装を調査・変更するとき。その機能に対応する個別の runtime モジュールを直接読む。
- CLI コマンド固有の処理やテストだけを確認するとき。

## hash
- dc703041a3d3ddd031bd81f5153d7b230cf31a10617c2debfc6ce34e7f295a74

# `indexing.py`

## Summary
- INDEX.md の検査・生成・再利用判定から、hash 検証、ファイル書き込み、更新 commit までの indexing lifecycle を一括して担う共通実装。directory traversal と Codex 呼び出し、並列実行、排他制御も扱う。

## Read this when
- INDEX.md の自動生成・更新・commit lifecycle を変更または調査するとき
- 既存 entry の再利用条件、対象 hash、Structured Output の検証、symlink・binary・除外対象の扱いを確認するとき
- indexing 処理の並列実行、lock、Codex context、worktree または Git failure の挙動を確認するとき

## Do not read this when
- INDEX.md entry の文章内容や schema 定義そのものを変更するときは、対応する oracle src または prompt builder の定義を先に読む
- 通常の CLI サブコマンドや indexing 以外の Git 操作を変更するとき
- INDEX.md の個別 entry を確認するだけで、生成 lifecycle の実装を調査しないとき

## hash
- 96d04e24f13776c6683bd0158693cfa494c207e3ee43598b2d925e5d88e1a72c

# `prompt_editor_input.py`

## Summary
- エディタまたはTUIからAI Agent用Markdownプロンプトを受け取り、テンプレート保存、エディタ選択・起動、入力読み込み、HTMLコメント除去、`.cmoc` ignore保証を担う共通境界。プロンプト編集フロー、エディタ選択仕様、入力完了時のエラー処理を確認する入口。

## Read this when
- プロンプト編集入力の保存・読み込み・コメント除去を変更または調査するとき
- code、nano、vim、viの選択順やエディタ起動失敗を確認するとき
- editor/TUI用ディレクトリの`.cmoc` ignore保証やtimestamp付きパス予約を確認するとき

## Do not read this when
- AI Agentへのプロンプト内容やテンプレート仕様だけを確認したいときは、対応するoracle文書を直接読む
- プロンプト編集後のCLI/TUI全体の実行フローや呼び出し元の責務を調査するときは、該当する上位実装を直接読む

## hash
- 5b4c8b92cfd723b9bd31e33b234cc9809fdc7e597e4129aa31e3007a5af482d1

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを提供する。work root 検査、doctor preprocess、サブコマンドログ、step 通知、完了サマリー、終了コード処理、例外のエラー表示を一元管理する。関連する CLI 実行フローや共通ログ・エラー処理を確認するときの入口。

## Read this when
- CLI サブコマンドの実行前後処理、共通ログ、step 表示、完了表示、終了コード、例外処理を変更または調査するとき。
- work root の実行条件や doctor preprocess の共通適用範囲を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、runtime ログの永続化実装、エラー内容の定義だけを確認したいときは、それぞれの専用実装を直接読む。

## hash
- 0fdfe0cf2a299838bfd4b72f21b187a24772db84ad908b9b7c233ebe6feae934

# `runtime_codex.py`

## Summary
- Codex 実行系の公開入口をまとめる薄い再エクスポートモジュール。exec 実行と TUI 実行の起動関数を同じ import 元から参照できるようにする。

## Read this when
- Codex 実行ランタイムの利用側で、exec 実行または TUI 実行の起動関数をどこから import するか確認したいとき。
- 実行方式ごとの実装詳細ではなく、runtime_codex 系の公開 API 境界だけを確認したいとき。

## Do not read this when
- exec 実行の具体的な処理、引数処理、プロセス制御を確認したいときは、exec 実行側の実装を直接読む。
- TUI 実行の具体的な処理、端末制御、対話実行の挙動を確認したいときは、TUI 実行側の実装を直接読む。
- 新しい実行ロジックや分岐を追加する場所を探しているときは、この再エクスポートではなく各実行方式の実装へ進む。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex exec の単一試行と再試行を制御する状態機械。Structured Output の JSON/schema 検証、capacity retry、quota availability probe と待機、resume token による継続、Codex subprocess の cwd・環境・設定・ログ管理、console/subcommand event 記録を一体で扱う。

## Read this when
- Codex exec の実行失敗、Structured Output 検証、capacity retry、quota 待機・probe、resume 継続の挙動を変更または調査するとき。
- Codex subprocess の argv、cwd、CODEX_HOME、prompt/stdout/stderr/output/call log、実行イベントの記録方法を確認するとき。
- Codex exec の retry counter、quota wait 状態、代表 probe、schema validation の制御ロジックを追うとき。

## Do not read this when
- TUI の起動や TUI 固有の分岐を変更・調査するときは、TUI 起動を担当する別 module を読む。
- Codex 呼び出し元の prompt 生成や AgentCallParameter の定義だけを確認したいときは、該当する builder または parameter 定義を直接読む。
- 一般的な runtime logging、path、profile、config の共通実装だけを確認したいときは、対応する commons module を直接読む。

## hash
- 5efe48afeab7b47779262e7a22324567df11f7327132395b260f504d7dea88a0

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しの利用者向け console 通知と、起動失敗時の共通エラーテキスト整形を担当する。呼び出し目的・ログパス・経過時間・終了状態を出力し、異常時は stderr へ通知する。

## Read this when
- Codex CLI 呼び出し時の console 通知、終了コードや起動失敗の表示、エラー文字列の整形を変更または確認するとき。

## Do not read this when
- Codex CLI の実行処理、呼び出しログの保存形式、runtime path や時間表示の仕様そのものを変更するとき。

## hash
- 1398891b8c46be913d7f8bdc8a255c0c8426012bb7f58d0afc2f44bb1b0bd350

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
- Codex CLI subprocess 境界の実装。sandbox・cwd・CODEX_HOME・provider/config override などの起動引数と環境を構築し、schema 配置、JSONL 出力解析、capacity/quota/予期せぬエラー判定を担う。editing run の child process tracking、pidfd による安全な signal 送信、process group 停止も扱う。

## Read this when
- Codex CLI の起動引数、sandbox mode、cwd、CODEX_HOME、model provider 設定を変更・調査するとき
- Codex subprocess の process tracking、停止、PID reuse 対策、SIGTERM/SIGKILL 処理を変更・調査するとき
- Structured Output schema の配置、Codex JSONL 出力、resume token、capacity/quota/error 判定を変更・調査するとき

## Do not read this when
- Codex CLI 呼び出し元の編集 run 制御や retry の全体フローを調査する場合
- 一般的な設定値の定義、runtime path、JSON/TOML 検証、エラー型の実装だけを調査する場合は、それぞれの責務を直接扱うファイルを読む

## hash
- 7f34712c7c764c9181e168bf980dfb1511352256c2df19cb1f897f1825aba16b

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動処理を担う実装。設定上書き引数、作業ディレクトリ、CODEX_HOME の検証、呼び出しログ、成功・失敗イベント記録、例外変換までを一括して扱う。Codex subprocess の起動や TUI 呼び出し結果の扱いを確認する入口。

## Read this when
- Codex TUI または Codex subprocess の起動条件・引数・作業ディレクトリを変更または調査するとき
- Codex 呼び出しログ、コンソール通知、logger event、失敗時の例外処理を確認するとき
- Codex HOME や設定上書きの検証経路を確認するとき

## Do not read this when
- Codex 呼び出し全体のパラメータ型や設定値の定義だけを確認したいときは、AgentCallParameter や CmocConfig の定義を直接読む
- Codex 実行環境の一般規則やログ仕様の正本を確認したいときは、対応する oracle 文書を直接読む
- Codex TUI の呼び出し結果ではなく、他の subprocess 実行処理だけを調査するとき

## hash
- f7c796bb30a6bcfe91a2eb3cbc5323a43341d8262cfac90e0463536299ea8cb9

# `runtime_config.py`

## Summary
- cmoc 設定の永続化境界を担当し、設定オブジェクトと JSON 表現の相互変換、JSON/TOML 互換値・各設定値の検証、設定ファイルの読み込み・書き込み・同期を提供する。設定モデルやパス定義そのものではなく、設定の runtime 入出力処理へ進む入口となる。

## Read this when
- cmoc config の JSON 保存形式、設定値の型検証、既定値補完、読み込み・書き込み・同期の挙動を変更または調査するとき
- 不正な設定値や設定ファイル欠落・JSON 読み込み失敗時の CmocError 境界を確認するとき

## Do not read this when
- 設定項目の定義や既定値そのものを確認したいときは設定モデル側を直接読む
- 設定ファイルのパス定義だけを確認したいときは runtime path 側を直接読む
- Codex 実行、oracle review、CLI コマンドの処理自体を調査するとき

## hash
- c78a4ceca303c20a2e74d7af5dd4f2722fe30291462fb572ae1ade2e712556c4

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
- doctor preprocess における Git 共通ディレクトリ単位の排他ロック、修復対象の同期、一時 index の退避・合成・復元、修復 commit の lifecycle を扱う。current worktree と main worktree の修復差分を、利用者の staged 状態と分離して commit するための内部実装。

## Read this when
- doctor preprocess の修復処理、Git index の退避・復元、一時 index の操作、.gitignore や .agents の追跡修復、修復 commit、linked worktree 間の排他制御を調査・変更するとき。

## Do not read this when
- doctor の設定同期や refactor state 同期の仕様だけを確認したいときは、対応する同期モジュールを直接読む。
- doctor preprocess の利用者向け仕様やエラー条件の正本を確認したいときは、参照されている oracle doc を直接読む。

## hash
- 9a652882dfc53495fc8596c47b181fcb17256c905f8b27bfb935f1ef62e1604a

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
- Git repository と worktree を操作する共通境界。Git command 実行、branch/HEAD/status の取得・検証、managed worktree の作成・削除・安全性確認、branch 削除を扱う。.gitignore・exclude・Git index に関する `.cmoc/gu` の ignore 管理と、oracle/realization file の path 分類も提供する。

## Read this when
- Git command の実行結果を `CmocError` や `CommandResult` に統一したいとき
- branch、HEAD、worktree、clean worktree、managed branch の検証や操作を変更するとき
- run worktree の path 対応、安全な削除、symlink・Git metadata 検証を確認するとき
- `.cmoc/gu` の ignore 設定、Git index、`.gitignore`、info/exclude の扱いを変更するとき
- oracle file または realization file の Git 状態・path 分類を確認するとき

## Do not read this when
- Git 境界や path 分類ではなく、個別の CLI command の業務ロジックだけを変更するとき
- Git 操作を伴わない runtime error、path、result の共通型そのものを確認するとき

## hash
- e8bf3d251b34ef21d5d52292f13062557667c94619b1210facae46e15f80a5e7

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines ログ出力と step/quota 待機時間の計測を担当する runtime logging モジュール。ContextVar による現在の logger の設定・復元・参照も提供し、ログ記録や実行時間集計を行う実装の入口となる。

## Read this when
- サブコマンドのイベントログ、step timing、quota 待機時間の集計を変更・調査するとき
- runtime helper から現在のサブコマンド logger を取得する処理を変更・調査するとき
- 並列実行時のログ追記や集計の同期を確認するとき

## Do not read this when
- コンソール表示形式やログ仕様そのものを確認したいときは、対応する oracle 文書を先に読む
- ログ保存先や timestamped path の生成だけを変更・調査するときは、runtime paths の実装を直接読む
- サブコマンド固有の処理や Codex event の生成を変更・調査するときは、その呼び出し元を直接読む

## hash
- 6242674523c98429906ea81fe6ab017cb54110f18d1b979ca099099f831630bb

# `runtime_paths.py`

## Summary
- リポジトリ、worktree、cmoc ルートの解決と、実行時の timestamp・duration 表示、各種 session/report/log/schema/config/state 保存先 path の構築を担う共通 runtime path モジュール。cwd の一時切替を process-wide に直列化する `pushd` と、memo 配下判定も提供する。

## Read this when
- runtime path の解決、root placeholder の扱い、cmoc 管理ディレクトリの保存先を確認・変更するとき
- timestamp、console timestamp、duration の書式や予約処理を確認・変更するとき
- cwd 切替の並行実行制御、context 単位の切替状態、root・memo 判定を確認・変更するとき

## Do not read this when
- 特定サブコマンドの処理内容、report・log の出力形式、設定 JSON の schema 自体を確認したいとき
- root placeholder の解決ロジックそのものを変更・確認したいときは、path model 側の実装を直接読む

## hash
- 731c950d030dd27d68799c7bc70603ddde37f79b668f94142de0bbbd159459c5

# `runtime_refactor.py`

## Summary
- oracle/realization file の調査履歴を読み込み、検証・同期・保存する共通ランタイム処理を提供する。対象ファイルの列挙、未調査対象の選択、調査状態の更新、相対パス・結果・SHA-256・時刻の schema 検証、および不正 state の CmocError 変換を扱う。

## Read this when
- refactor state の読み込み、書き込み、schema 検証、対象 file 集合との同期を変更・調査するとき
- refactor investigation target の選択や調査済み状態のリセット処理を確認するとき
- runtime の oracle/realization file 判定、SHA-256、相対 path、調査履歴時刻の制約を確認するとき

## Do not read this when
- refactor state や調査対象選択に関係しない共通ランタイム処理を調査するとき
- refactor サブコマンド固有の実行フローや利用者向け CLI 挙動だけを確認するときは、まず対応するサブコマンド実装・仕様を読むとき

## hash
- 9a8701e186324807b9165059c1b7509c427d68f90ab32dc3c8a582afe12ba8b4

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
- Git worktree 上の branch とパスの対応を解決し、editing run の process identity・tracking file・ライフサイクルロックを管理する共通ランタイムモジュール。run の停止時には PID、start time、process group を検証し、PID 再利用や不確実な対応関係による誤停止を避けながら親 process と Codex child group を停止する。

## Read this when
- editing run の worktree 解決、process tracking、run の abandon・cleanup・停止処理を変更または調査するとき。
- PID 再利用防止、process group の停止、tracking file の読み書き、run lifecycle の排他制御を確認するとき。

## Do not read this when
- 通常の Git 操作や worktree 一般の仕様だけを確認したいときは、worktree 解決を利用する呼び出し元または Git 関連の仕様を先に読む。
- editing run の外部仕様や CLI 入出力だけを確認したいときは、このランタイム実装ではなく対応する oracle 文書やサブコマンド実装を読む。

## hash
- 484952085f9be242b4a1a6e240b4eb017b67910246fed2c8ccd1b9f812cd4283

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始から state 遷移、worktree・branch の管理、commit、差分分類、INDEX 更新、cleanup 判定までを担う共通 lifecycle 実装。EditingRunContext と lifecycle lock を共有し、run/session の不変条件と許可差分を検証する下位機能への入口となる。

## Read this when
- editing run の開始・復旧・終了や state 更新を変更するとき
- run/session worktree・branch の作成、検証、削除を調査するとき
- workload 差分、oracle 差分、INDEX 更新、想定外 path の分類規則を確認するとき
- run worktree の commit、rollback、cleanup 判定の共通処理を変更するとき

## Do not read this when
- 特定サブコマンド固有の workload 処理だけを変更するとき
- state file のデータ構造そのものを変更するときは runtime_state の実装を直接確認する
- INDEX の生成ロジックだけを変更するときは indexing 関連の実装を直接確認する

## hash
- 2563a452693983a9664f9d42e8005c6613cfe05fdaf8ccb21e085aeb385aaa80

# `runtime_run_report.py`

## Summary
- editing run の fork report と lifecycle report を Markdown + YAML Front Matter 形式で保存する共通処理を提供する。実行コンテキスト、状態遷移、完了理由、変更パス、警告、詳細情報を記録し、timestamped path の予約によって report の上書きを防ぐ。YAML scalar の安全な文字列表現も担当する。

## Read this when
- editing run の fork report または run の join/abandon lifecycle report の生成・保存処理を変更するとき
- report の Front Matter 項目、本文構成、timestamped path の予約、YAML scalar 変換を確認するとき

## Do not read this when
- report の正本仕様や編集 run の状態遷移仕様を確認したいときは、記載された oracle document を直接読む
- runtime path の構築や EditingRunContext の定義自体を変更・調査するとき

## hash
- 37b70b344bbdcff0b02251e6fa3eb6eb63b0f1b6e46fa48aa9d4b10494fc97bf

# `runtime_state.py`

## Summary
- session の永続 state を表す dataclass、JSON schema 検証、読み書き、branch からの session 特定、active session 検索を提供する共通 runtime モジュール。session fork の排他 lock も扱い、session/run 操作から state 管理を参照する入口となる。

## Read this when
- session state の schema、状態値、不変条件、JSON 保存形式を変更または確認するとき
- session branch・run branch と state file の対応付けや、state の読み書き・検証を調査するとき
- session fork の排他制御や active session の検索処理を変更するとき

## Do not read this when
- CLI サブコマンド固有の session 操作仕様や lifecycle を確認したいときは、対応する oracle 文書またはサブコマンド実装を直接読む
- session state と無関係な git 操作、path 解決、エラー型の一般仕様だけを調べるとき

## hash
- e0b35333320120922fa7b0dc327f3f8e884f62a884378b435bbef5e550647fff
