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
- INDEX.md のエントリー生成を支える indexing 実装。対象ファイルやディレクトリの内容を検査し、Codex によるエントリー生成、鮮度判定、INDEX.md の更新・コミットを管理する。

## Read this when
- INDEX.md の自動生成・更新・コミット処理を変更または調査するとき
- indexable なファイル・ディレクトリの判定、既存エントリーの再利用、ハッシュ検証を確認するとき
- Codex 呼び出しの並列化、排他ロック、worktree 間の実行分離を変更するとき

## Do not read this when
- INDEX.md のエントリー内容の仕様だけを確認したいときは、indexing の oracle 文書を直接読む
- 特定の CLI サブコマンドの実装を変更するときは、そのサブコマンドの実装ファイルを直接読む

## hash
- 26246975f2dccf84ecfc768c704d2ec6d0c715e4a6916086c3904375d088bdfd

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
- Codex exec の単一試行ループを実行制御する中心モジュール。subprocess 起動、prompt・stdout・stderr・output・call log の保存、Structured Output の JSON/schema 検証、capacity retry、quota 待機と代表 probe、resume token による継続、console/subcommand event 記録、実行結果の構築を一体の状態機械として扱う。併せて worktree の変更 path と git status の取得も提供する。

## Read this when
- Codex exec の起動条件、argv・cwd・環境変数・schema 指定を変更するとき
- Structured Output 検証、semantic retry、capacity retry、quota polling、代表 probe、resume 継続の挙動を調査・変更するとき
- Codex call log、prompt/output log、console event、subcommand event、CodexExecResult の記録内容を確認するとき
- exec 失敗時の分類・エラー処理やログ path の生成を確認するとき
- agent call 後の worktree 変更 path と git status の取得処理を確認するとき

## Do not read this when
- TUI の起動や TUI 固有の分岐を変更・調査するときは、TUI を担当する別 module を直接読む
- Codex subprocess の低レベル実装、エラー分類、resume token 抽出、path・logging・config の共通処理だけを変更するときは、対応する commons module を直接読む
- exec の正本仕様や retry・quota の規則を確認するときは、この実装ではなく参照されている oracle 文書を読む

## hash
- c3c82b6b3be9e7b66d266cd43d168a282cc5cc14882db1c8c02057fe656c3d29

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しの利用者向け console 通知と、起動失敗時の共通エラーテキスト変換を担う。呼び出し目的・ログパス・経過時間・終了コード・エラーを整形して出力し、CmocError と一般例外を処理する実装への入口。

## Read this when
- Codex CLI 呼び出し通知の出力内容、出力先、エラー表示を確認・変更するとき
- Codex CLI 起動失敗時のエラーテキスト変換を確認・変更するとき

## Do not read this when
- Codex CLI の実際の起動処理やイベントログ保存の実装を確認するとき
- 時刻や経過時間のフォーマット規則そのものを確認するとき

## hash
- 05b23e2ca6cdd39b230b9972c682ac09f9ffefed8a27e0537e7a34a627f19ee4

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 呼び出し前に INDEX 更新 preflight を挟む共通ランタイム制御を提供する。preflight の登録・解除、再入抑止、スレッド直列化、呼び出し設定からの indexing 起点決定を扱い、実際の Codex 実行は runtime_codex へ委譲する。

## Read this when
- Codex exec または TUI 実行時の INDEX 更新 preflight の呼び出し条件・実行順序を変更するとき
- indexing preflight の登録、解除、再入防止、スレッド間の直列化を確認するとき
- Codex 呼び出し設定から preflight の起点 root を決定する処理を変更するとき

## Do not read this when
- Codex 実行本体の subprocess 処理や TUI 実装を変更するときは runtime_codex を直接読む
- リポジトリ root・work root の解決規則だけを確認するときは runtime_paths を読む
- Codex 実行結果の型や結果変換だけを確認するときは runtime_results を読む

## hash
- 9c401fd077a0fc1e1781739a0b1dac7b0d6c01c245b3351c5a907f0d3de749c8

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界を担当し、起動前の sandbox・argv・cwd・CODEX_HOME・環境変数・schema 配置と、起動後の process tracking・停止制御・JSON/JSONL 出力および capacity/quota/error 判定をまとめる。Codex 実行環境の構築と機械的な実行結果の解釈に関する実装・エラー処理の入口。

## Read this when
- Codex CLI の起動引数、sandbox または file access mode の変換、model provider 設定、cwd/CODEX_HOME/env の扱いを変更・調査するとき
- Codex subprocess の PID/process group tracking、pidfd による停止、SIGTERM/SIGKILL、abandon 対応を変更・調査するとき
- Structured Output schema の配置、Codex の JSON/JSONL 出力解析、resume token や capacity/quota/unexpected error 判定を変更・調査するとき

## Do not read this when
- Codex CLI 境界の外側にある editing run の業務フローや利用者向けコマンド仕様だけを確認するときは、対応する app_spec または上位 orchestration 実装を直接読む
- 一般的な process 管理や JSON 処理の実装を確認するだけで、cmoc の Codex subprocess 入出力境界に関係しないとき

## hash
- 2c92ef3c235cda1242818e645d8ceacf344e4671dfc33ff5d551991c94d2a759

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動処理を担当する実装。設定上書き引数、作業ディレクトリ、CODEX_HOME の検証、call log の保存、コンソール・イベントログ、失敗時の例外変換をまとめて扱う。Codex CLI/TUI の呼び出し経路や実行ログ・失敗処理を変更または確認するときの入口。

## Read this when
- Codex TUI の起動引数、実行環境、作業ディレクトリ、CODEX_HOME の扱いを変更・調査するとき
- Codex 呼び出しの call log、実行時間、戻り値、成功・失敗イベントの記録を変更・調査するとき
- Codex CLI/TUI 起動失敗時の例外処理を変更・調査するとき

## Do not read this when
- Codex の設定値そのものや設定上書き規則を確認する場合は、設定・プロファイル関連の実装を直接読む
- Codex 呼び出し以外の一般的なサブコマンドログやパス生成だけを確認する場合は、それぞれの担当モジュールを直接読む

## hash
- 6a7fbedb2ab6e7738c9b43a0dd709133cd798a53ebc700d62d2e727915750b7d

# `runtime_config.py`

## Summary
- cmoc 設定を runtime 型と永続化 JSON の間で相互変換する実装。設定値の型・enum・model provider を検証し、不足項目は既定値で補完する。設定ファイルの読み込み、書き込み、未作成時の生成までを担う。

## Read this when
- cmoc 設定 JSON の schema、読み込み・保存処理、設定値の検証や既定値補完を変更・調査するとき。

## Do not read this when
- CLI の設定項目そのものや runtime 型の定義だけを確認したいときは、それぞれの設定型・正本定義を直接読む。設定以外の runtime path やエラー処理を調査するとき。

## hash
- d44b19cec1a20d911104f6b3b0c7d79a872d92e74ce8edfa849a2eb9bb05a250

# `runtime_content.py`

## Summary
- ファイル内容または文字列内容から SHA-256 digest を計算し、digest をファイル名に含めた内容アドレス型ファイルを書き出す小さな runtime content helper 群。
- 出力先 directory の作成有無が異なる 2 種類の書き出し関数と、先頭 chunk の NUL byte と読み取り可否による簡易 binary 判定を扱う。

## Read this when
- 内容 hash を使った成果物ファイル名の生成、重複書き込み回避、または内容アドレス型の一時・補助ファイル保存を確認・変更するとき。
- ファイル内容や文字列内容の SHA-256 digest 計算処理を使う箇所を探すとき。
- テキスト対象と binary 対象を粗く分けるための簡易判定ロジックを確認・変更するとき。

## Do not read this when
- path model、run/work/root の意味、またはパス表記そのものの仕様を確認したいとき。
- CLI 引数、サブコマンド、標準出力、終了コードなど利用者向けの公開面を確認したいとき。
- hash 値を使わない通常のファイル読み書き、設定読み込み、永続状態管理の実装を探しているとき。

## hash
- d121b59cd941f68e101d0bf9b1eb0f0fdd2fe8c928d89dd6447b3079581fb905

# `runtime_doctor.py`

## Summary
- Git common directory 単位のロックを使い、設定・refactor state・ignore 規則・`.agents` placeholder・Ollama 状態を同期・修復する doctor 前処理を提供する。
- 一時 Git index を用いて doctor の修復差分だけを commit し、利用者の staged 状態や元の index を復元する。
- Git index の保存・復元、blob 登録、修復対象ファイルの検証など、doctor 前処理に必要な内部補助処理を含む。

## Read this when
- doctor 前処理の修復対象、排他制御、commit、index 復元の挙動を変更・調査するとき
- config や refactor state の同期、`.agents` の追跡、`.gitignore` 修復、Ollama 起動確認との連携を確認するとき
- doctor 実行時の staged 状態保護や一時 Git index の扱いを確認するとき

## Do not read this when
- 通常の設定値や設定ファイルの仕様だけを確認したいときは、runtime config の実装・仕様を直接読む
- refactor state の内容や同期規則だけを確認したいときは、runtime refactor の実装・仕様を直接読む
- Ollama の提供状態だけを確認したいときは、runtime ollama の実装・仕様を直接読む

## hash
- e268fba035da2adf3fea3b9b279a5d9db36f799827308279c0892fd625f90cab

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
- Git 操作、branch・commit・worktree 管理、.cmoc ignore 状態、oracle/realization file 判定を担う共通 runtime helper。安全な worktree 作成・削除、Git 状態検査、path と追跡状態に基づく分類処理の入口となる。

## Read this when
- Git コマンド実行結果の統一、branch や HEAD の取得、clean worktree 検証を変更するとき
- cmoc の managed worktree 作成・削除、branch 管理、symlink や Git metadata の安全性を確認するとき
- .cmoc/gu の ignore 初期化・検査や .gitignore / exclude 更新を変更するとき
- oracle file または realization file の path 判定規則を変更するとき

## Do not read this when
- 特定の CLI サブコマンドの業務フローや session state の仕様だけを確認する場合
- Git 操作を伴わない runtime path・結果型・エラー型の実装を確認する場合
- この module の共通 helper を利用するだけで、Git 状態判定や worktree 安全性の挙動を変更しない場合

## hash
- 0c15d7ae94df60a2e2a0627574ff79dafd58b81d2338a17edd753520c9750efe

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

# `runtime_ollama.py`

## Summary
- cmoc が管理する Ollama の単一 preflight 実装。設定された cmoc provider 用モデルを対象に、lock 内で archive install、user systemd service の生成・起動・所有者確認、127.0.0.1:11434 の API 応答確認、model の pull/load、GPU 用 VRAM 使用確認までを順序どおりに実行する。runtime 共通処理から呼び出される managed Ollama の実装入口であり、Ollama の service・procfs・HTTP・model 検証の詳細を確認するための対象。

## Read this when
- cmoc provider の local SLM が利用できない、または Ollama の install・起動・model pull/load・GPU 検証を調査・変更するとき
- managed Ollama の systemd user service、固定 endpoint 127.0.0.1:11434、procfs による process/listener 所有者確認を確認するとき
- Ollama 関連の lock、managed environment、CmocError 変換、設定からの対象 model 抽出を確認するとき

## Do not read this when
- Ollama 以外の provider、一般的な runtime 設定の読み込み、または CLI の上位 command routing だけを調べるとき
- Ollama の正本仕様や利用条件を確認したい場合は、この実装ではなく対応する oracle doc を直接読むとき

## hash
- 7e1826673ee1b45f02ae4cc798e8d9711c966392967ddc60bbcf664354a34910

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
- oracle/realization file の refactor state を管理する共通ランタイムモジュール。state の読み込み・schema 検証・安定保存、対象 file 集合との同期、調査対象の選択、調査要求の一括設定を扱う。refactor 状態管理や対象 file 列挙の実装を確認する際の入口。

## Read this when
- refactor state の schema、保存形式、調査履歴の検証を変更・確認するとき
- oracle/realization file の列挙や調査対象選択の挙動を変更・確認するとき
- refactor cycle の開始や investigation required の更新処理を確認するとき

## Do not read this when
- 特定の oracle/realization file の内容や refactor 対象そのものを調査するとき
- refactor state の file path 定義だけを確認するときは、path 定義を担当するモジュールを直接読む場合
- CLI の表示・実行処理や個別 runtime helper の仕様を確認するとき

## hash
- 3e2c22c73de04a17eb0f7ba7cf25608e17336a0c5db8934c0aa069a8db0ba907

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
- run の worktree 特定、editing run のプロセス識別情報の保存・読込・削除、親 run process と Codex child process group の安全な停止を担う共通ランタイムモジュール。session 単位の lifecycle lock と tracking 用環境変数も扱う。

## Read this when
- run の worktree 解決や branch と worktree の対応を変更・調査するとき
- editing run の process tracking、abandon、join、停止処理、PID 再利用対策を変更・調査するとき
- run process tracking file の形式、検証、削除条件を確認するとき

## Do not read this when
- 通常の CLI サブコマンド固有ロジックや session state の仕様だけを変更・調査するとき
- Codex subprocess の起動方法そのものや一般的な git 操作の実装を確認するときは、それぞれの専用モジュールを直接読む

## hash
- bb3c53ea9b23af4c567abc630c54eccd070ea62b4c76c5f59f782c8517bb2e5e

# `runtime_state.py`

## Summary
- session state の永続化・検証・復元を担うランタイム共通モジュール。session/run の状態 schema、branch からの session-id 解決、state file の読み書き、home branch に紐づく active session の検索、session fork 用排他 lock を扱う。

## Read this when
- session state の JSON schema、状態値や run field の不変条件を確認したいとき
- session branch または run branch から state を読み込む処理を変更・調査するとき
- session state file の保存・復元・検証や active session の検索を変更するとき
- repository 共通の session fork 排他 lock の挙動を確認するとき

## Do not read this when
- CLI サブコマンド固有の session 操作手順や利用者向け仕様を確認したいときは、対応する oracle doc やサブコマンド実装を直接読む
- git branch の作成・join・apply など、state の低レベルな表現を超える処理を調査するとき
- 一般的な runtime error、git 操作、path 解決の実装だけを確認したいときは、各担当モジュールを直接読む

## hash
- 90df33de780017aa2ee8e8a191090fc6396cf9c3d0b054602649fc740a8e0dec
