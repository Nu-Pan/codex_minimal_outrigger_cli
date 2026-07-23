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
- Codex CLI subprocess 境界を担当し、起動前の sandbox・cwd・CODEX_HOME・argv/config override・schema 配置と、起動中の process tracking・安全な停止、起動後の JSON/JSONL 出力・error・capacity/quota 判定をまとめる。Codex CLI との実行環境および機械的結果の解釈を扱う下位実装への入口。

## Read this when
- Codex CLI の起動引数、sandbox、cwd、CODEX_HOME、model provider、reasoning 設定を変更・調査するとき
- Codex subprocess の process group tracking、PID reuse 対策、停止・signal・abandon 処理を変更・調査するとき
- Structured Output schema の配置、JSONL error、resume token、capacity/quota retry 判定を変更・調査するとき

## Do not read this when
- Codex CLI を呼び出さない通常の設定処理や、Codex のプロンプト本文生成だけを変更・調査するとき
- 編集 run 全体の状態遷移や CLI サブコマンドの責務を確認したい場合は、対応する app_spec の oracle または上位実装を先に読むとき

## hash
- d05b39c70db0cb3030d6fb85c6e8e3ee06563bae47084a3663a3bb5743ed1e77

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
- CmocConfig と永続化 JSON の相互変換、JSON/TOML 互換値の検証、設定ファイルの読み込み・書き込み・同期を担うランタイム設定モジュール。設定値の型検証、不正設定や未作成設定に対する CmocError 境界も扱う。

## Read this when
- cmoc 設定 JSON の保存形式、読み込み時の既定値補完、設定値の型・値検証を変更または確認するとき
- 設定ファイルの生成・同期、JSON 構文エラーや不正値の利用者向けエラー処理を調査するとき

## Do not read this when
- Codex モデルや oracle review の設定型そのものを変更するときは、先に設定型定義を読む
- CLI コマンドの引数や設定ファイルのパス定義だけを確認するときは、対応する CLI 実装または runtime paths の定義を直接読む

## hash
- d51140e809f9fe2896a271d24eac994702009dcee0a7080c7202d737fae4320e

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
- Git 操作、branch・commit・worktree の検証と作成・削除、Git ignore 状態、oracle/realization file 判定を担う共通 runtime helper。cmoc の session/run 処理や repository path 分類で Git 境界・安全性を確認する入口。

## Read this when
- Git subprocess の実行結果や利用者向けエラー変換を変更するとき
- managed branch、linked worktree の作成・削除・安全な path 検証を変更するとき
- `.cmoc/gu` の ignore 設定や oracle/realization file の分類ロジックを変更するとき
- Git status、branch、commit、common directory の取得 helper の利用箇所を調査するとき

## Do not read this when
- 特定の CLI サブコマンド固有の session・run 業務フローだけを変更するとき
- Git や file 分類を介さない runtime path・result 型の定義を確認するとき
- worktree や ignore の安全性ではなく、oracle 文書に定義された仕様そのものを確認するとき

## hash
- cb039903662a4790595648b7bc06df613e2e6339e3aa19a1804861658b32e4d9

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
- oracle/realization file のリファクタリング調査状態を管理する共通ランタイム機能。状態ファイルの読み込み・厳密な schema 検証・安定した JSON 保存・対象ファイル集合との同期・未調査対象の選択・調査要求の一括設定を扱う。

## Read this when
- refactor state の schema、履歴保持、JSON 保存形式、調査対象ファイルの列挙や選択優先順位を変更・確認するとき
- oracle file または realization file の変更に伴うリファクタリング調査状態の同期処理を変更・確認するとき

## Do not read this when
- 個別の oracle/realization file の内容やリファクタリング実施方法だけを確認したいとき
- refactor state と無関係な CLI、パス処理、エラー処理の実装を確認するとき

## hash
- a7e16f2c283ac51e458a1d41fca8642cc394b724915d7104e42876c0760fad07

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

# `runtime_state.py`

## Summary
- cmoc の session state を表す dataclass、JSON schema 検証、state file の読み書き、branch と session の対応付け、session fork 用排他 lock を提供する共通 runtime モジュール。session/run の lifecycle、branch 名、fork 情報、run payload の不変条件を扱い、session 関連サブコマンドが利用する下位実装への入口となる。

## Read this when
- session state の schema、検証、永続化、読み込みエラーを変更または調査するとき
- cmoc session branch・run branch から session state を特定する処理を変更または調査するとき
- home branch に紐づく active session の検索や session fork 排他を扱うとき

## Do not read this when
- oracle の session state 仕様そのものを確認したいときは、先に対応する oracle 文書を読む場合
- 特定の session サブコマンドの業務フローだけを変更・調査し、state の読み書きや検証の責務に触れない場合

## hash
- 0334e4521f90f260020a9da3d7f298c4645d0160b356c418c7a5c7953c4f657f
