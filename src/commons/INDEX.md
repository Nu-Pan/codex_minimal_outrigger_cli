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
- INDEX.md を対象ファイル・ディレクトリごとに生成・更新する indexing 処理を提供する。
- 既存 entry の再利用判定、対象 hash の計算、Structured Output の検証と Markdown 化、更新差分の commit、並列生成と排他制御を担う。

## Read this when
- INDEX.md の自動生成・更新、entry の鮮度判定、indexing 用 lock、生成結果の検証を変更するとき
- Codex 呼び出し前の indexing preflight、並列処理、worktree や process-global 制約を調査するとき
- INDEX.md entry の Markdown 形式や対象ファイルの列挙・除外条件を確認するとき

## Do not read this when
- 特定の CLI サブコマンドの実装や一般的な Codex 実行規則だけを調べるとき
- INDEX.md の正本仕様や prompt の定義を変更するときは、対応する oracle 文書・oracle source を先に読む

## hash
- c2036b77730c939744ffd6c1152de3017fb5cddeba96a3f7330ebb0357c2fbae

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
- Codex CLI subprocess 境界を一括して扱う実装。sandbox・argv・cwd・CODEX_HOME の設定、schema 配置、process group の追跡と安全な停止、Codex subprocess の実行、JSONL 出力の解析および capacity/quota/予期しないエラー判定を担う。Codex 起動条件や実行結果の解釈を変更・確認する際の入口。

## Read this when
- Codex CLI の argv、sandbox、model/provider、network、cwd、CODEX_HOME、環境変数を変更または調査するとき
- Codex subprocess の起動、process tracking、PID reuse 対策、SIGTERM/SIGKILL、process group 停止を変更または調査するとき
- Structured Output schema の配置、Codex JSONL 出力、resume token、capacity/quota/error 判定を変更または調査するとき

## Do not read this when
- Codex CLI のプロンプト生成や agent call の組み立てだけを変更するとき
- editing run の利用者向けライフサイクル仕様そのものを確認するときは、先に対応する oracle doc を読む
- 一般的な runtime path、設定定義、エラー型の実装だけを変更するときは、それぞれの直接担当ファイルを読む

## hash
- 7ff6cb13c077bf5a64e9df606d289c64ed792690bb97e321530dc82b0e5b5e57

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
- 設定オブジェクトを永続化 JSON と runtime の CmocConfig 型の間で相互変換するモジュール。enum キー、モデル仕様、整数値、起動動作を検証し、不足項目は既定値で補完する。設定ファイルの読み込み・書き込み・初期生成・同期も担当する。

## Read this when
- cmoc config の JSON スキーマ、既定値補完、編集値の検証、設定ファイルの読み込み・保存動作を変更または確認するとき
- 設定不正・JSON 構文エラー・設定ファイル未存在時の CmocError 境界を調査するとき
- config_path を介した設定ファイルの生成や同期処理を追跡するとき

## Do not read this when
- runtime の設定型そのものや既定値の定義を確認したい場合は config.cmoc_config を直接読むとき
- 設定ファイルのパス定義だけを確認したい場合は commons.runtime_paths を直接読むとき
- 設定値を利用する個別の CLI 処理や oracle review の実行ロジックを調査するとき

## hash
- d61091135d0e0a5fe74e3e0f684c164aee0adb184ec73c8cd14de9054de49a4f

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
- doctor 前処理の実装を担うモジュール。Git common directory 単位の排他制御下で、設定・refactor state・ignore 規則・.agents placeholder・Ollama 状態を同期し、doctor による修復だけを一時 index から commit する。Git index の保存・復元、修復対象の staging、tracked runtime file の検証も含む。

## Read this when
- doctor 前処理の動作、修復 commit、Git index の保存・復元、doctor lock の競合制御を変更・調査するとき
- doctor が設定・refactor state・.gitignore・.agents・Ollama をどの条件で同期するか確認するとき
- 一時 Git index を用いた修復差分の分離や、doctor 完了後の tracked runtime file 検証を確認するとき

## Do not read this when
- doctor 前処理の正本仕様や利用者向け要件を確認する場合は、まず対応する oracle doc を読むとき
- 設定値の定義自体を変更・調査する場合は、設定実装または oracle src を直接読むとき
- Git 操作や Ollama 同期の共通仕様だけを確認する場合は、それぞれの共通 runtime モジュールを直接読むとき

## hash
- a26674859efb3437f1d2e11a6ff081eb2374e40bd4bf31ec8293447cf1200f2b

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
- managed Ollama の単一 preflight を担当し、archive からの executable 配置、systemd user service の同期・起動、procfs による listener 所有者確認、HTTP 応答確認、設定対象 model の pull・load・GPU 利用確認を一つの lock 内で順序制御する。runtime の Ollama 関連処理を読む入口。

## Read this when
- managed Ollama の install、service 起動・再起動、127.0.0.1:11434 の所有者検証、model の取得・load、GPU 推論確認を変更または調査するとき。
- cmoc provider model やテスト用 SLM の起動保証、Ollama の systemd user unit、procfs の process/socket 判定を確認するとき。

## Do not read this when
- Ollama 以外の runtime 設定、path、error 定義だけを調査するときは、それぞれの専用 module を直接読む。
- CLI の公開仕様や managed Ollama の正本要件を確認するときは、対応する oracle 文書を先に読む。

## hash
- f115ad6071dd487c6c1f8b2cbebcadc1010b3d56c976304a440cda35d7e367fd

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
- session state の JSON schema、状態値、不変条件、読み書き処理を提供する共通ランタイムモジュール。session/run branch から state を特定し、検証・保存・active session 検索を行う。session fork 用の repository 共通排他 lock と branch 名解析も扱う。

## Read this when
- session state の schema、状態遷移、JSON の検証・保存・読み込みを変更または調査するとき
- cmoc session branch / run branch と session state file の対応付けを調査するとき
- session fork の排他制御や active session の検索処理を確認するとき

## Do not read this when
- CLI サブコマンド固有の処理や lifecycle の正本仕様を確認したいときは、対応する oracle doc とそのサブコマンド実装を直接読む
- git 操作、path 解決、エラー型そのものの仕様だけを調査するときは、各責務の専用モジュールを読む

## hash
- 09af13c435640db15738af2c6fc628b05bac76a3255b63c79c8e981ce2fb56ee
