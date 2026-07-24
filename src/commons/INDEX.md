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
- Codex exec の単一試行ループを実装し、prompt・stdout・stderr・output・call log の保存、Structured Output の JSON/schema 検証、capacity retry、quota 回復待機と代表 probe、resume token による継続、subcommand event 記録を一体的に制御する。
- 同じ実行状態とログ・イベントを共有するため、quota 処理を含む exec 実行制御の変更・調査における中心的な入口となる。
- 変更 path の取得では、git status の結果をファイル単位の絶対 path として返す。

## Read this when
- Codex exec の再試行、Structured Output 検証、quota/capacity error、resume 継続の挙動を変更・調査するとき
- Codex call log、prompt/output log、subcommand event、quota 待機状態の記録を変更・調査するとき
- exec 後の worktree 変更 path の収集処理を変更・調査するとき

## Do not read this when
- TUI 起動処理だけを変更・調査するとき
- Codex subprocess の低レベル実行、設定・profile 判定、path・logging の共通処理そのものを変更・調査するときは、対応する commons module を直接読む
- exec の呼び出し側や結果型の定義だけを変更・調査するとき

## hash
- a89c9f1220e0e42f56abd7d173ce605c8342574e696fc11d47eae9d1295ccef3

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
- Codex CLI subprocess 境界を一元的に扱う実装。起動時の sandbox・cwd・CODEX_HOME・argv/config override・schema 配置、実行中 process group の追跡と安全な停止、Codex の JSONL 出力・resume token・capacity/quota/error 判定を提供する。

## Read this when
- Codex CLI の起動引数、sandbox、cwd、CODEX_HOME、provider 設定、Structured Output schema 配置を変更・調査するとき。
- Codex subprocess の process tracking、pidfd による停止、SIGTERM/SIGKILL、abandon 処理を変更・調査するとき。
- Codex の終了結果、JSONL error、capacity/quota retry、resume token、malformed output の判定を変更・調査するとき。

## Do not read this when
- Codex CLI 境界ではなく、一般的な設定値の定義や runtime path の共通処理だけを変更・調査するときは、それぞれの設定・path 実装を直接読む。
- Codex CLI の利用者向けコマンドフローや editing run 全体の仕様を確認したいだけの場合は、対応する app specification と上位の実装を先に読む。

## hash
- 99d47efac4017c48b29f1a463504303e61618e144eff884ba9664893fc8d8989

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
- 設定オブジェクトを JSON 永続化形式へ変換・検証し、設定 JSON から実行時設定へ復元する共通モジュール。設定ファイルの生成・読み込み・同期と、不正値・欠損値に対する既定値補完および利用者向けエラー変換を扱う。

## Read this when
- cmoc 設定 JSON の schema、型検証、既定値補完、読み書き、同期処理を変更・調査するとき。
- Codex model provider、model、reasoning effort、oracle review の設定永続化境界を確認するとき。

## Do not read this when
- CLI コマンド固有の設定操作や設定型そのものの定義を確認したいだけのとき。
- 設定 JSON の入出力境界に関係しない実行時パス、エラー型、モデル変換の実装を調査するとき。

## hash
- fba52d5c7459f502b543bfaf9ab26cf63b9e0470308ee533a71a86200d599879

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
- Git index と common directory 単位のロックを使い、doctor 前処理の修復を排他実行する runtime 実装。設定・refactor state・ignore 規則・.agents placeholder を同期し、ユーザーの staged 状態を保ったまま修復差分だけを一時 index から commit する。
- doctor 用ロック、index の保存・復元、一時 index 操作、Git blob staging、修復対象の検証など、doctor 前処理に必要な内部 helper 群を提供する。

## Read this when
- doctor 前処理の実行、排他制御、修復 commit、Git index の保存・復元に関する挙動を変更または調査するとき
- config や refactor state、.gitignore、.agents placeholder の doctor による同期・追跡処理を確認するとき
- 一時 GIT_INDEX_FILE を使った Git 操作や、修復後にユーザーの staged 状態を復元する処理を確認するとき

## Do not read this when
- doctor 前処理ではなく、通常の設定同期や refactor state の具体的な仕様だけを調査するときは、対応する commons モジュールや oracle 文書を直接読む
- CLI の doctor サブコマンドの引数・表示・上位の実行フローだけを確認するときは、CLI command 実装を直接読む
- 一般的な Git 操作や repository path 解決の実装だけを確認するときは、このファイルではなく runtime_git または runtime_paths を読む

## hash
- 9f5ad372719dc0e231356db2541ddd15380233534818de36294088bdecc144cd

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
- Git コマンド実行、branch・HEAD・status・worktree の作成／削除、Git ignore 判定、oracle／realization file の分類を担う共通境界。path の正規化、symlink 検査、managed worktree の安全性検証もここで扱う。

## Read this when
- Git の状態取得や clean worktree 前提を実装・変更するとき
- cmoc 管理 branch／linked worktree の作成・削除や安全性検証を調べるとき
- `.cmoc/gu` の ignore 設定や Git exclude、追跡状態を扱うとき
- oracle file／realization file の path 分類や Git 状態判定を変更・確認するとき

## Do not read this when
- 特定の CLI サブコマンドの業務フローだけを確認する場合は、そのサブコマンドの実装や対応する oracle 文書を直接読む
- Git と無関係な path 操作、実行時エラー、結果型の詳細だけを確認する場合は、それぞれの専用共通 module を読む

## hash
- b82639b183c8387b636c54303818d9f4cd1805d922cfb6f58e3325b6ec695ff3

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
- oracle/realization file の調査履歴を表す state を読み込み、検証・同期・保存する共通処理を提供する。対象 file の列挙、未調査 target の選択、調査必須状態の一括設定、path・entry・SHA256・時刻形式の検証を扱う。

## Read this when
- refactor state の schema、読み書き、履歴同期、調査対象選択の挙動を変更・調査するとき
- oracle/realization file の列挙条件や、state entry の妥当性検証を確認するとき

## Do not read this when
- 個別の oracle/realization file の内容や調査ロジックだけを確認するとき
- refactor state を利用する上位処理の CLI 挙動を調べるときは、まずその呼び出し元を読むべき場合

## hash
- c34d722f7f4d8a30123df58f4bd13a6430a171c5846b55d3e0cc67db25e049fe

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
- editing run の process identity と managed worktree を扱うランタイム共通処理。run branch から worktree を検証・解決し、session 単位の tracking file とロックで run 本体および Codex child process group の追跡・削除・安全な停止を提供する。

## Read this when
- cmoc run の abandon、join、lifecycle lock、process tracking、run process の停止処理を変更・調査するとき
- run branch と managed worktree の対応検証や、PID 再利用を避けた process 同一性確認を扱うとき

## Do not read this when
- 通常の CLI コマンド定義や run のユーザー向け出力形式だけを変更・調査するとき
- git worktree の作成・削除処理そのものを扱うときは、worktree 操作を直接実装する対象を先に確認する

## hash
- ff7be4b16bff140e3accc5272a9ab50e5e166aa6e1664227f12ba94eead8d86c

# `runtime_run_lifecycle.py`

## Summary
- editing run のライフサイクル全体を管理する共通モジュール。session から isolated run worktree を開始し、active run の解決、state 遷移、work unit の rollback/commit、INDEX 更新、Git 差分分類、agent/run/session の変更 path 検査、oracle diff、cleanup 判定に必要な処理を提供する。run branch の不変条件と lifecycle lock を共有するため、editing run lifecycle の実装入口として扱う。

## Read this when
- editing run の開始、active run の解決、joinable/error への state 遷移を変更または調査するとき
- run worktree の commit・rollback、INDEX 更新、差分 path の分類や許可範囲検査を変更または調査するとき
- run/session branch の変更検証、oracle diff、refactor state path の扱いを確認するとき

## Do not read this when
- CLI の個別サブコマンド仕様や利用者向け editing run の契約だけを確認する場合は、対応する oracle doc を先に読む
- Git 操作や session state の低レベル共通処理そのものを変更する場合は、各 commons モジュールを直接読む
- INDEX 更新機構だけを調査する場合は、indexing モジュールを直接読む

## hash
- c0b14b1a9edb6b34185d024b2f90d3b4497fea34189f7ebde749e818824fdccc

# `runtime_run_report.py`

## Summary
- editing run と run lifecycle の処理結果を Markdown + YAML Front Matter の report として保存する共通モジュール。fork report と lifecycle report の生成、YAML scalar の安全な表現を扱う。

## Read this when
- editing run の fork report 保存処理を変更・調査するとき
- run の join/abandon など lifecycle report の保存処理を変更・調査するとき
- report の共通メタデータ、変更パス、警告、YAML scalar 表現を確認するとき

## Do not read this when
- 実行時パスや timestamp の定義だけを確認したいとき
- EditingRunContext の状態管理や lifecycle 自体の仕様を確認したいとき
- report を利用する個別コマンドの処理だけを変更・調査するとき

## hash
- b1fdda23ac29567dd637aff0ac007b781e09ee044050c7859d8c544a8436a9e3

# `runtime_state.py`

## Summary
- cmoc の session state を表す dataclass、JSON schema 検証、保存・読み込み、branch からの session 特定、session fork 用排他 lock を提供する共通 runtime モジュール。session/run の lifecycle state、不変条件、不正 state の利用者向け例外変換を扱う。
- session state の永続化仕様や session/run branch との対応を確認する際の、commons 層からの実装入口。

## Read this when
- session state JSON の schema、読み書き、検証、不変条件を変更・調査するとき
- cmoc session branch または run branch から state を解決する処理を変更・調査するとき
- session fork の repository 共通 lock や state file の保存先を確認するとき

## Do not read this when
- session や run の CLI 操作手順・利用者向け仕様だけを確認したいとき
- oracle edit や session fork の正本仕様を確認することが目的のときは、対応する oracle doc を先に読むべき場合
- runtime state と無関係な git 操作、path 処理、CLI 出力の実装を調査するとき

## hash
- 2153d5db1c52ba9f0c0abb938b35fe691ca0315c265844e35a4303471bb05467
