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
- 複数の `commons.runtime_*` モジュールから、CLI 実行・Codex 起動・設定・Git・パス・状態管理などの共通 API を集約して再公開する互換用ランタイム窓口。個別ランタイム機能の実装を確認する入口ではなく、複数機能を横断する公開シンボルの利用箇所や import 構成を調べる場合に読む。

## Read this when
- 共通ランタイム API の公開名、再公開元、利用可能な例外・型・関数を確認したいとき
- `commons.cmoc_runtime` 経由の import や公開 API の変更影響を調べるとき

## Do not read this when
- 特定のランタイム機能の実装詳細を調べるときは、対応する `commons.runtime_*` モジュールを直接読む
- CLI サブコマンドの処理フローを調べるときは、サブコマンド実装や `runtime_cli` を直接読む

## hash
- b40ef70d07f2c05922acdeceb300a23e1ee94554c2931305aee9a25c4534bc50

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

# `runtime_apply.py`

## Summary
- cmoc apply の linked worktree 特定と、apply プロセスおよび Codex 子プロセスの同一性確認・追跡・停止・cleanup を担う共通ランタイム処理。apply/abandon のプロセス状態管理を確認する入口。

## Read this when
- apply または abandon の process ID file、PID 再利用対策、プロセスグループ停止、子プロセス追跡を変更・調査するとき
- session branch や apply branch から linked worktree のパスを解決する処理を変更・調査するとき

## Do not read this when
- CLI の apply/abandon の利用者向け仕様や状態遷移を確認したいとき
- プロセス管理や worktree 解決を使わないサブコマンドの実装を調査するとき

## hash
- cfb232f9ad8bc672cd032a565f3911658c8c6394d6688e5c8e6cad1e4c1aa3e4

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
- Codex exec の単一試行ループを実行制御するモジュール。Codex subprocess の argv・cwd・環境・schema・prompt を準備し、prompt/call/stdout/stderr/output の実行記録を保存する。
- Structured Output の JSON parse・schema 検証、capacity retry、quota 回復待機と代表 probe、resume token による継続、失敗分類、console/subcommand event 記録を共有状態機械として扱う。
- 変更された worktree path と git status code の取得も提供する。TUI 起動や正本仕様の定義を扱うモジュールではない。

## Read this when
- Codex exec の再試行、Structured Output 検証、quota 待機・probe、resume 継続、Codex call log/event の挙動を変更または調査するとき。
- Codex subprocess の実行条件、ログ path、失敗分類、実行結果の組み立てを確認するとき。
- agent call 後の worktree 変更 path と git status の取得処理を変更または調査するとき。

## Do not read this when
- TUI 起動処理そのものを変更または調査するとき。
- Codex exec の正本仕様を確認するときは、参照されている oracle の app_spec 文書を先に読む。
- 単に Codex の profile、path、設定、subprocess 呼び出しの個別 helper を調査するだけなら、対応する commons runtime module を直接読む。

## hash
- 3c67f726bea710cc9d52e2d206f5df5a5a03ae936c7e69be0e360abd20ca465e

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
- Codex CLI subprocess 境界を一括して扱う実装。sandbox・argv・cwd・CODEX_HOME・managed Ollama provider・schema 配置などの起動前設定と、child process の tracking／安全な停止、JSONL 出力・resume token・capacity/quota/unexpected error 判定などの実行結果解釈を担う。Codex 呼び出しの実行環境や失敗時の制御を確認する際の主要な入口。

## Read this when
- Codex CLI に渡す sandbox、model、config、argv、cwd、環境変数を調査・変更するとき
- CODEX_HOME、認証情報、schema 配置、managed Ollama provider の準備を確認するとき
- Codex subprocess の起動、process group、PID reuse 対策、SIGTERM／SIGKILL、apply process tracking を調査するとき
- Codex の stdout／stderr、JSONL event、resume token、capacity・quota・unexpected error の判定を確認するとき

## Do not read this when
- Codex CLI の業務フローや apply／abandon の利用者向け仕様だけを確認する場合は、対応する oracle 文書や上位のコマンド実装を直接読む
- Codex 以外の subprocess 実行、一般的な runtime path・error・config の実装だけを調査する場合

## hash
- 3ecfab05393ab739b31c09b44edded28c11208ef6830ff710652ace7baf260d6

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
- cmoc 設定を JSON と runtime の CmocConfig 間で変換・永続化するモジュール。設定値の既定値補完、型・enum・model 検証、不正設定や JSON 構文の利用者向けエラー化、設定ファイルの生成・読み込み・同期を担う。

## Read this when
- cmoc 設定 JSON の形式や復元処理を変更・確認するとき
- 設定ファイルの読み込み、書き込み、既定値補完、入力検証の挙動を調べるとき
- config doctor や設定同期処理から設定永続化の入口を確認するとき

## Do not read this when
- CmocConfig の型定義や既定値そのものを確認したいときは、直接 config.cmoc_config を読む
- Codex の model 名や reasoning effort の正本定義を確認したいときは、直接 oracle.other.cmoc_config を読む
- 設定値を利用する個別の CLI 処理だけを調べるとき

## hash
- 20d30041bf2f6efe5bfe928fd329d2516a685e7e13bbb6f258fb512a19c1bbc3

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
- doctor 前処理を担当する実装モジュール。current worktree と main worktree をロック下で処理し、設定同期、Git ignore・.agents 追跡・Ollama 準備、修復差分の commit、元の index 復元までを行う。
- 一時 Git index を使って利用者の staged 状態を保護しながら修復を分離し、設定追跡や Git 操作の失敗を CmocError として扱う。doctor の排他制御、修復対象、index 操作、commit 挙動を確認するための実装入口。

## Read this when
- doctor サブコマンドの前処理、修復 commit、設定同期、Ollama 準備を変更・レビューするとき
- worktree 間の doctor 排他制御や Git common directory の lock file を調査するとき
- doctor 実行前後の Git index 復元、一時 index、staged 差分分離の挙動を確認するとき
- .gitignore、.agents/.gitkeep、cmoc 設定の追跡処理や失敗時の CmocError を調査するとき

## Do not read this when
- doctor の CLI 引数や利用者向け仕様だけを確認したいときは、まず該当する command 実装または oracle doc を読む
- 一般的な Git 操作、設定同期、Ollama 接続処理の詳細だけを調査するときは、この orchestration module ではなく各 commons.runtime_* モジュールを直接読む
- doctor 前処理と無関係なサブコマンドや通常の worktree 操作を変更するとき

## hash
- a5250231069b6f1aeeefd31fef4b92165a42f375876296ad15746e6080e9fed3

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
- Git 操作、branch 判定、linked worktree の安全な作成・削除、.cmoc/gu の ignore 管理、oracle/realization file 判定を担う共通ランタイム helper。Git 境界のエラー変換や管理対象 path の安全性検証もここに集約される。

## Read this when
- Git subprocess の呼び出し、branch・commit・worktree 操作を変更または調査するとき
- cmoc 管理領域の path 検証、symlink 防止、worktree 削除条件を確認するとき
- .cmoc/gu の ignore 設定や oracle/realization file の分類判定を変更するとき

## Do not read this when
- CLI サブコマンド固有の処理や state/report の仕様だけを確認するとき
- Git や file 分類の共通 helper を利用するだけで、実装方針を変更しないとき

## hash
- 192565eae91a021558e915dff0f243a426c37e5bf21b69c6d1dfa9c58568414e

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
- リポジトリ・worktree root、時刻、経過時間、各種 runtime directory/path を解決する共通ユーティリティ。cwd の一時切替を排他制御し、root 解決失敗を CmocError に変換する。

## Read this when
- root path、runtime の保存先、timestamp・duration 表記、cwd 切替、agent 読み取りディレクトリの扱いを変更または確認するとき。

## Do not read this when
- 特定のサブコマンドの処理や、root 解決・runtime path・cwd 制御を直接扱わない機能を変更するとき。

## hash
- 89e875751c526a76452c8635292807bb73828e1d42cb22c090cd71b04fe556c0

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

# `runtime_state.py`

## Summary
- session/apply の永続 state dataclass、JSON schema 検証・読み書き、branch からの session_id 解決を担当する共通モジュール。session state file の保存先、home branch に紐づく active session の検索、linked worktree 間の session fork 排他 lock も提供する。

## Read this when
- session または apply の state file schema、状態値、必須 field、JSON の検証・保存挙動を変更または確認するとき
- cmoc 管理 branch から session_id を解決する処理や、branch に対応する state の読み込みを調査するとき
- session fork 時の排他制御や active session の検索処理を変更または調査するとき

## Do not read this when
- CLI サブコマンド固有の session/apply 操作フローだけを確認するとき
- state schema の正本仕様を確認する必要があるときは、先に対応する oracle 文書を読むべき場合
- git branch 操作や session/apply の上位 orchestration の実装だけを調査するとき

## hash
- 0ea55b2d5d91d5756ff8c9e3de9fa3c6be599d37707c026e7d7985463e8ec72a
