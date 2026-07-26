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
- INDEX.md の検査・生成・再利用・鮮度検証・書き込み・Git commit を一貫して扱う indexing lifecycle の共通実装。directory traversal、entry 生成、並列実行、排他制御、Structured Output 検証を提供する。

## Read this when
- INDEX.md の自動更新、entry の生成または再利用条件を変更するとき
- INDEX.md の hash 鮮度判定、Markdown 構造検証、書き込み、indexing commit を調査するとき
- indexing の並列実行、Codex context 継承、worktree 間 lock、preflight 動作を変更または検証するとき

## Do not read this when
- 通常の CLI サブコマンド処理や INDEX.md 以外のファイル生成を調査するとき
- INDEX.md entry の意味内容そのものを定義・変更するときは、まず対応する oracle 文書または entry 生成処理を確認するとき

## hash
- c7f948d005811a6a2336a9f8077428c43b275afa74627744481d483fd40bdbb0

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
- CLI サブコマンドの共通実行ライフサイクルを提供するモジュール。doctor preprocess、サブコマンドログ、step 通知、完了サマリー、戻り値の終了コード化、例外のエラー表示を一元管理する。
- work root・repo root の選択、実行前提の検査、サブコマンドロガーのコンテキスト管理、step 開始通知と完了時間の出力を扱う。
- CLI サブコマンドの実行フロー、ログ配置、標準出力／標準エラーへのエラー表示、step 表示を変更・調査するときの共通入口。

## Read this when
- 複数の CLI サブコマンドに共通する実行前処理・後処理を変更するとき
- サブコマンドログ、doctor preprocess、step 通知、完了サマリーの挙動を確認するとき
- work root 実行制約や例外・非 0 returncode の終了処理を調査するとき

## Do not read this when
- 特定サブコマンド固有の処理や引数定義だけを変更・調査するとき
- ログの永続化形式そのものを確認するときは、ロガー実装を直接読む方が適切な場合
- doctor preprocess の修復規則そのものを確認するときは、doctor preprocess の仕様・実装を直接読む方が適切な場合

## hash
- f3980a3980441a68abae7601d30bfce8e6680702831dbea8dc1d295958c667cf

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
- Codex exec の単一試行ループを実装する中核モジュール。subprocess 実行、Structured Output の JSON/schema 検証、capacity retry、quota availability probe と待機、resume 継続、call log・stdout/stderr・prompt・subcommand event の記録を一つの状態機械として扱う。
- Codex 実行結果の失敗分類・再試行・quota 待機や、変更された worktree path の取得を担う。TUI 起動など exec 実行制御以外の責務は扱わない。

## Read this when
- Codex exec の起動引数、cwd/CODEX_HOME、schema、prompt または各種実行ログの扱いを変更・調査するとき
- Structured Output 検証、semantic retry、capacity retry、quota polling、代表 probe、resume token 継続の挙動を変更・調査するとき
- Codex call の console/subcommand event、失敗分類、実行結果、worktree 変更 path の実装を確認するとき

## Do not read this when
- TUI の起動や画面制御を変更・調査するとき
- Codex exec の共通 path・profile・subprocess・設定・結果型の詳細だけを確認したいときは、対応する commons/runtime_codex_profile.py、runtime_paths.py、runtime_results.py などを直接読む

## hash
- ad7f7e3321152ad6471732406951479c59a8dae16477dbc2d17f99e5e4158b34

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しの開始結果・目的・呼び出しログ・経過時間・終了コードを console へ通知する共通処理と、起動失敗時のエラー文を整形する処理を提供する。Codex 実行通知やエラー表示の挙動を確認・変更するときの入口となる。

## Read this when
- Codex CLI 呼び出しの console 通知、終了コードや起動失敗の表示、共通エラー文の整形を確認・変更するとき。

## Do not read this when
- Codex CLI の実行そのもの、イベントログへの保存、パスや時間のフォーマット実装を変更するときは、それぞれの担当モジュールや正本仕様を直接読む。

## hash
- 73393347eab098c2a0dad80281ead3c513dc71f9f9c20a68fd5981b99307f245

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
- cmoc 設定を正本の設定型と永続化 JSON の間で変換し、JSON/TOML互換値・enum・model provider・整数値を検証する実装。設定の読み込み、既定値補完、書き込み、未作成時の初期生成と同期を担う。

## Read this when
- cmoc 設定 JSON の保存形式や型検証を変更するとき
- 設定の読み込み・書き込み・既定値補完・エラー処理を調査するとき
- 設定ファイルの生成や現在形式への同期処理を確認するとき

## Do not read this when
- Codex 実行時のモデル選択や設定値の定義自体を変更するとき
- 設定型や設定項目の正本定義を確認するとき
- 設定ファイルのパス定義だけを確認するとき

## hash
- 51fa59bd7f8b572d4e04846082edd08c9f11d78291f68e507a4d3e6338c2aaa7

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
- doctor 前処理を担う実装。current と main worktree の設定・refactor state・ignore 規則・.agents 追跡状態を修復し、Git index を保全しながら修復差分だけを commit する。doctor の排他ロック、一時 index 操作、復元、追跡状態検証までをまとめて扱う。

## Read this when
- doctor 前処理の修復対象、commit 単位、worktree 間処理を確認するとき
- doctor 実行時の Git index 保全、一時 index、lock、復元動作を変更または検証するとき
- config・refactor state・.gitignore・.agents の追跡状態に関する doctor の挙動を調べるとき

## Do not read this when
- doctor の仕様上の修復条件や利用者向け挙動を確認したいだけのときは、対応する oracle 文書を直接読む
- Git 共通処理、設定同期、refactor state 同期そのものを変更するときは、それぞれの runtime モジュールを直接読む
- doctor 前処理と無関係な CLI サブコマンドや一般的な Git 操作を調べるとき

## hash
- f4f8de2567fc3c81f42374ceb76d6e80d498b7d517798ee763b7680bb240aee4

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
- Git コマンド実行、branch と commit の取得、worktree の作成・削除・検証、Git ignore 状態の管理、および oracle/realization file の分類を担う共通境界。Git 状態・path 正規化・管理領域の安全性を共有するため、これらの処理を実装または変更するときの入口となる。

## Read this when
- Git subprocess の実行結果や利用者向けエラー処理を変更するとき
- branch、linked worktree、worktree path の作成・削除・安全性検証を変更するとき
- `.cmoc/gu` の ignore 設定や Git index・exclude の扱いを変更するとき
- oracle file または realization file の path 分類・Git 追跡状態判定を変更するとき

## Do not read this when
- Git 境界の挙動を変更せず、個別の CLI command や上位の session 処理だけを変更するとき
- worktree や Git ignore の具体的な正本仕様を確認することが目的の場合は、対応する oracle 文書を先に読むとき

## hash
- 7cb4d8f73237b867609e837ad24e722a0df73c354ad4b215cf7bfe7463530fd0

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

# `runtime_preprocess_command.py`

## Summary
- doctor preprocess を実行する共通 CLI コマンド処理を提供する。サブコマンド名を受け取り、CLI 実行ラッパー経由で preprocess を実行した後、repo_root を含む cmoc の見出しを出力する。

## Read this when
- doctor preprocess を実行する CLI サブコマンドの共通処理や、preprocess 実行後の出力を確認・変更するとき。
- サブコマンドのステップ表示、work_root・repo_root の取得、CLI 実行ラッパーとの接続を調べるとき。

## Do not read this when
- doctor preprocess 自体の内部仕様や処理内容だけを確認したいときは、doctor preprocess の仕様・実装を直接読む。
- CLI 共通実行ラッパーの詳細だけを確認したいときは、runtime_cli の実装を直接読む。

## hash
- 6d6ae7bdbfd820181a212ac092a503f72a70d8955c32fa42d3b4187fb371b691

# `runtime_refactor.py`

## Summary
- oracle/realization file の調査履歴を管理する共通ランタイム処理。state の読み込み・schema 検証・安定した JSON 保存、対象 file 集合との同期、未調査対象の選択、調査必須状態の一括設定を担う。
- refactor state の path、entry、調査結果、SHA-256、調査日時の妥当性検証と、不正時の利用者向け例外変換を提供する。refactor 機能の state 管理や調査対象選定の実装を確認するときの入口。

## Read this when
- refactor state の読み込み・保存・schema 検証を変更または調査するとき
- oracle/realization file の列挙、state との同期、調査対象の選択ロジックを確認するとき
- refactor 調査履歴の SHA-256、日時形式、不正値処理を確認するとき

## Do not read this when
- INDEX.md の生成や routing 文書の内容だけを確認するとき
- refactor 機能の正本仕様を確認するときは、先に対応する oracle document を読む
- refactor state と無関係な CLI、runtime、filesystem 処理を調査するときは、該当する実装 file を直接読む

## hash
- 2766e4fdc615470002adf3b36d2d03ec5bd5add8538b4521420c467c22f33d4c

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
- editing run の worktree 解決、プロセス識別情報の保存・読取・削除、実行中 run と Codex subprocess group の安全な停止を担うランタイム補助モジュール。run abandon や実行ライフサイクル制御の実装を調べる際の入口となる。

## Read this when
- editing run の process tracking、lifecycle lock、abandon 処理を変更・調査するとき
- PID 再利用対策、start time や pidfd によるプロセス同一性検証、process group 停止の挙動を確認するとき
- branch から worktree を解決する処理や run process tracking file の形式を確認するとき

## Do not read this when
- 一般的な git worktree 操作だけを調べるときは、worktree 管理を直接実装する対象を読む
- Codex subprocess の起動・追跡登録処理そのものを調べるときは、subprocess 起動側の実装を直接読む
- CLI の利用者向け編集 run 仕様やコマンド引数を確認するときは、対応する oracle doc またはサブコマンド実装を読む

## hash
- e3e9ed3c6385e566e0c5ad094352ea9d1a466fdac38bc44785f678a5dfa6667c

# `runtime_run_lifecycle.py`

## Summary
- 明示的な join を必要とする editing run のライフサイクル共通処理を担う。session の事前条件確認、run worktree の作成・状態管理・終了、work unit の rollback/commit、INDEX 更新、Git 差分の分類と許可範囲検査、cleanup 判定に必要な関数群を提供する。

## Read this when
- editing run の開始・join・状態遷移・終了処理を変更または調査するとき
- run branch/worktree の作成、commit、rollback、cleanup、process ID 管理を確認するとき
- realization file・oracle file・INDEX.md の差分許可範囲や rename を含む Git 差分分類を確認するとき
- run worktree から INDEX.md を更新・commit する処理を変更するとき

## Do not read this when
- editing run lifecycle や Git 差分検査ではなく、個別サブコマンドの処理だけを変更するとき
- session state のデータ構造や永続化形式そのものを確認したい場合は、state 定義・永続化を直接扱うモジュールを読むとき
- INDEX.md の生成規則そのものを確認したい場合は、index 更新機構や対応する oracle 文書を直接読むとき

## hash
- 73f162b9c1921c7eb01151772739dd591be7209e56159ae363abc615666ca030

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
