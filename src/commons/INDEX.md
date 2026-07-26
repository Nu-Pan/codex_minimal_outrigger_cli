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
- cmoc の実行時共通 API を集約するモジュール。Codex 実行・設定・Git・パス・状態・ログ・結果・エラー処理など、CLI サブコマンド間で共有される定数、型、関数を再公開する。

## Read this when
- commons の共有ランタイム API を変更・利用するとき
- Codex subprocess の起動、sandbox 設定、プロセス追跡や終了処理を確認するとき
- 設定、コンテンツハッシュ、Git worktree、ログ、パス、セッション状態の共通処理を確認するとき

## Do not read this when
- 特定のランタイム領域の内部実装だけを変更する場合は、対応する runtime_* モジュールを直接読むとき
- CLI サブコマンド固有の制御フローや入出力を確認する場合

## hash
- b5cc7caba70403189a082bb2808982aa6794f01f1553bc93b9c08706a2af16d5

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
- CLI サブコマンドの共通実行ライフサイクルを提供する実装モジュール。work root 検査、doctor preprocess、サブコマンドログ、step 通知、完了サマリー、終了コード化、例外表示を一元管理する。
- サブコマンド固有の実装を run_cli_subcommand に渡して実行するための入口であり、ログ記録や標準出力・標準エラーの扱いを確認する際の基点となる。

## Read this when
- CLI サブコマンドの実行前処理・終了処理・例外処理を変更または調査するとき
- サブコマンドログ、step 通知、完了サマリー、終了コードの挙動を確認するとき
- work root 検査や doctor preprocess の共通実行経路を確認するとき

## Do not read this when
- 特定サブコマンドの業務処理や個別の引数定義だけを変更・調査するとき
- ログの保存形式やエラー文面そのものを変更・調査するときは、それぞれの担当モジュールや正本仕様を直接確認するとき

## hash
- 256fd6112f362a6036e13f5ee7d0c78927df7bd1b13d3cb04924fa612ac6d8e4

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
- Codex CLI subprocess 境界の実装。実行前の sandbox・cwd・CODEX_HOME・設定 override argv・schema 配置を準備し、subprocess の環境と起動を管理する。
- Codex child の PID・start time・process group を追跡し、pidfd と advisory lock を用いた安全な停止・終了待機・tracking 更新を提供する。
- Codex の JSONL stdout、stderr、構造化出力を読み取り、resume token の抽出と capacity・quota・予期しない error の判定を行う。

## Read this when
- Codex CLI の起動引数、sandbox、cwd、CODEX_HOME、model provider 設定、schema 配置を変更・調査するとき。
- editing run における Codex subprocess の PID tracking、process group 停止、SIGTERM/SIGKILL、PID reuse 対策を変更・調査するとき。
- Codex の JSONL 出力解析、quota/capacity retry、malformed event、error 判定を変更・調査するとき。

## Do not read this when
- Codex CLI 呼び出し元の editing run 制御や retry orchestration 自体を調査するときは、該当する上位モジュールを先に読む。
- cmoc の一般的な設定値の定義・検証や runtime path の共通処理だけを調査するときは、それぞれの設定・path モジュールを直接読む。

## hash
- 163bf4974d5a509df2f4240c51f47a2f172ccb005627c060829ec5d91d1fd0a5

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
- doctor 前処理の実装を担い、Git common directory 単位の排他ロック下で設定・refactor state・ignore 規則・`.agents` 追跡状態を同期し、修復差分だけを一時 index 経由で commit する。
- current/index の退避・復元、worktree 間の修復範囲分離、一時 Git index 操作、修復後の追跡状態検証までを扱う。

## Read this when
- doctor サブコマンドの前処理、修復 commit、Git index の退避・復元、linked worktree 対応を変更または調査するとき。
- `.gitignore`、`.agents/.gitkeep`、config、refactor state の doctor による同期や追跡状態検証を確認するとき。
- doctor の並行実行防止や、一時 index を用いた staged 状態保全の挙動を確認するとき。

## Do not read this when
- doctor 前処理以外の一般的な設定同期、refactor state の仕様、Git コマンド共通処理だけを調べるときは、それぞれの専用モジュールや oracle 文書を先に読む。
- doctor の利用者向け仕様やエラー文言の正本を確認するだけの場合は、実装ではなく対応する oracle 文書を読む。

## hash
- 6faa06d58117c257cad1d99551bed4fa4b1c1086fd76df7d3ee82db5669c6e96

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
- Git コマンド実行、branch・HEAD・worktree の検証と管理、Git ignore 状態の更新・検査、および oracle/realization file の path 分類を担う共通境界。Git repository の path 正規化、安全な worktree 操作、追跡状態判定が必要な処理から参照する。

## Read this when
- Git の状態取得、clean worktree 判定、branch 判定、commit 取得を変更・調査するとき
- cmoc 管理 worktree の作成・削除、branch と worktree path の対応、安全性検証を扱うとき
- `.cmoc/gu` の ignore 設定や Git index・exclude の更新を扱うとき
- oracle file または realization file の分類条件、Git の追跡・ignore 判定を確認するとき

## Do not read this when
- 個別の CLI サブコマンドの業務ロジックだけを変更・調査する場合
- Git や worktree、ignore、oracle/realization 分類に関係しない runtime helper を扱う場合
- prompt の仕様や path model の正本を確認することが目的で、実装境界の挙動を調べる必要がない場合

## hash
- 875bf3459a8308ef9bf93dc16dd4f6c5fbffc3e987a972c3e6ef144a1956b50d

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
- editing run の worktree 解決とプロセス追跡・停止を担う共通ランタイムモジュール。
- branch から worktree を検証付きで特定し、session 単位の tracking file と lifecycle lock で run 本体および Codex 子プロセス群を管理する。
- PID の再利用を避けるため開始時刻や process group を検証し、安全側に倒して run の停止・tracking file の削除を行う。

## Read this when
- editing run の worktree 解決、run process の追跡、abandon 時の停止処理を変更・調査するとき。
- PID、process group、pidfd、process start time を用いたプロセス同一性検証や停止失敗時の挙動を確認するとき。
- session ごとの run lifecycle lock、tracking file の読み書き・削除条件を確認するとき。

## Do not read this when
- Codex subprocess 自体の起動や tracking 情報の登録形式を変更する作業で、呼び出し元や runtime_codex_profile の実装を直接確認すべきとき。
- git worktree の配置規則そのものを変更する作業で、branch model の oracle 文書や expected_run_worktree の実装を直接確認すべきとき。
- 一般的な git 操作、パス処理、エラー型の仕様だけを調べるとき。

## hash
- 1e5a555654f260ca2de6edeb06a9e081bb043266bd9690d7c22b3d8853999729

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始から state 遷移、commit、差分分類、INDEX 更新、cleanup 判定までを担う共通 lifecycle 実装。EditingRunContext と lifecycle lock を共有し、session/run branch と worktree の整合性、許可された変更 path、oracle 差分を管理する。

## Read this when
- editing run の開始、active run の解決、joinable/error 遷移を変更するとき
- run worktree の commit、rollback、INDEX 更新、差分分類や変更 path の許可判定を確認するとき
- session branch と run branch の worktree/state 整合性や cleanup 対象を調査するとき

## Do not read this when
- 単一の CLI サブコマンド固有の処理や、state schema 自体の定義を確認したいとき
- INDEX 更新処理そのもの、Git 操作の低レベル実装、run state の永続化実装を直接変更・調査するときは、それぞれの専用 module を先に読む

## hash
- ab5c8fdf8e82b063133213dd34ed9d3439b330ea3e40f6ccee74c7398b619331

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
- session と run の永続状態を表す dataclass、状態値と payload の schema 検証、JSON state file の読み書きを提供する。
- session branch / run branch から session-id と対応する state file を解決し、branch 単位で state または session 部分を読み込む。
- repository 共通の lock による session fork 排他制御、home branch に紐づく active session の検索、不正 state の CmocError 変換を扱う。

## Read this when
- session または run state の schema、状態遷移用 payload、不正値の検証条件を変更・確認するとき
- session branch / run branch と state file の対応付け、state の永続化や読み込み処理を調査するとき
- session fork の排他 lock、active session の検索、state file 起因のエラー処理を確認するとき

## Do not read this when
- oracle の session state 仕様や fork 排他の正本を確認したいとき
- 個別の CLI サブコマンドの session/run lifecycle 操作そのものを調査するときは、対応する app_spec またはサブコマンド実装を先に読むとき
- 一般的な git branch 操作、パス解決、利用者向けエラー形式だけを調査するとき

## hash
- 4e4bc973556d30feb8270c7a031ed20a4892d627207bb4b2e54de939cf9d1464
