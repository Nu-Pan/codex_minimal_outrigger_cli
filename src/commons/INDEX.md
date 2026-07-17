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
- apply 実行に関する共通ランタイム処理を提供するモジュール。branch から worktree を解決し、apply process と Codex child process の PID・開始時刻・process group を追跡、排他、停止、stale 状態の cleanup までを扱う。apply/abandon の process lifecycle 実装を読む際の入口。

## Read this when
- cmoc apply の実行中 process 管理、abandon による停止、PID file の読み書きや cleanup を変更・調査するとき。
- apply branch と managed worktree の対応付け、worktree lookup、process 同一性確認、process group 停止の挙動を確認するとき。
- apply state の公開と abandon cleanup の競合防止、Codex subprocess tracking の環境変数連携を確認するとき。

## Do not read this when
- apply の CLI 引数や利用者向け仕様だけを確認したいときは、対応する subcommand の oracle doc を先に読む。
- 一般的な process 実行・signal・git 操作の共通実装を調べる場合は、ここではなく cmoc_runtime 側の定義を直接読む。
- apply と無関係な worktree、PID、process group 管理を扱う場合。

## hash
- 777ef88da7816a6ae26dc6cb4223eb37f946cdf42401eab770ce56942f4797a5

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
- doctor 前処理として、worktree と main worktree の共有修復を排他実行し、cmoc ignore 規則、`.agents/.gitkeep`、worktree 設定、Ollama 状態を整える。
- Git の一時 index を使って doctor の修復差分だけを commit し、呼び出し元の index を復元する。Git common directory 単位の lock、index/tree 操作、blob staging、設定追跡確認などの内部処理を含む。
- doctor 前処理の実行経路、Git 修復差分の分離・commit、worktree 間の修復、設定や Ollama の同期挙動を確認するための実装入口。

## Read this when
- doctor 前処理や修復処理の実装・変更を行うとき
- Git index の保護、一時 index による修復 commit、worktree 間の差分分離を調査するとき
- `.gitignore`、`.agents/.gitkeep`、cmoc 設定の追跡状態、Ollama 起動状態が doctor でどう扱われるか確認するとき

## Do not read this when
- doctor の利用者向け仕様や修復条件の正本を確認したい場合は、対応する oracle 文書を先に読むとき
- doctor 以外の CLI サブコマンドや一般的な Git・設定処理だけを調査するとき
- 単に Ollama の実装や設定同期の詳細を確認する場合は、それぞれの専用モジュールを直接読むとき

## hash
- e4d3dda80587e676bf3e56a5b21a96f6c0fe54a3816de495f6fb8f937c00e191

# `runtime_errors.py`

## Summary
- cmoc の実行時エラーを利用者向け Markdown レポートへ統一変換する実装。CmocError の概要・復旧案・詳細の保持、既定の Next actions 補完、未知の例外の要約・詳細化、Call stack の出力を扱う。

## Read this when
- cmoc のエラー報告形式、CmocError の生成・利用、Next actions の補完、例外発生時の Markdown 出力を変更または調査するとき。

## Do not read this when
- エラー報告の正本仕様や利用者向け文面を確認したいだけのときは、対応する oracle/doc の仕様を先に読む。エラー処理と無関係な CLI、設定、永続化、業務ロジックを変更するとき。

## hash
- 9aa2a62b5d16f6050dae80940272adea036fabed6bb694e2790823974254e831

# `runtime_git.py`

## Summary
- Git 操作、branch・HEAD・worktree の管理、`.cmoc/gu` の ignore 状態、oracle file 判定を担う共通ランタイム helper。Git subprocess のエラーを `CmocError` に統一し、cmoc 管理領域外の worktree や symlink 経由の操作を拒否する。関連する Git 状態判定や path 安全性検証の実装へ進む入口。

## Read this when
- Git コマンド実行、branch 判定、HEAD 取得、未コミット差分検査を変更・調査するとき
- cmoc の managed worktree 作成・削除、branch 削除、worktree path 検証を扱うとき
- `.cmoc/gu` の ignore 設定・検査や oracle file 判定の挙動を確認するとき

## Do not read this when
- CLI のサブコマンド固有の処理や session/apply の業務フローだけを調査するとき
- Git や worktree、ignore、oracle/realization file 判定に関係しない共通処理を調査するとき

## hash
- 8a23fa03b1277eff01583ca053888de81d7f00aae78e56cce3187cd08b1ff1cb

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines ログ記録と step timing・quota 待機時間の集約を担う runtime logging モジュール。logger の context 間共有機能も提供する。

## Read this when
- サブコマンドのイベントログ形式、ログファイル生成、step の開始・完了計測、経過時間や quota 待機時間の集計を変更・調査するとき
- 深い runtime helper から現在のサブコマンド logger を参照・差し替え・復元する処理を変更するとき

## Do not read this when
- ログ仕様そのものや console 表示との互換性を確認したい場合は、先に対応する oracle 文書を読むとき
- ログディレクトリや timestamp 付きパス予約の共通処理だけを調査する場合は、runtime paths の実装を直接読むとき

## hash
- 01fababfe41483ba8194c1aec614beda27fe55ad5010a54e0b61e8a190f71a09

# `runtime_ollama.py`

## Summary
- cmoc が管理する Ollama の単一 preflight を担うモジュール。cmoc provider 用モデルの抽出から、Ollama archive の導入、systemd user service の同期・起動、procfs によるプロセス／listener 所有者確認、HTTP 応答、モデル取得・load、GPU 使用確認までを同一 lock 内で順序どおりに実行する。

## Read this when
- cmoc provider の local SLM を Ollama で提供する処理を変更・調査するとき
- Ollama の archive install、systemd user service、固定 endpoint、モデル pull/load、GPU 検証の挙動を確認するとき
- managed Ollama の起動失敗・所有者不一致・API 応答失敗・GPU 未使用エラーを追跡するとき

## Do not read this when
- Ollama 以外の provider や一般的な設定読み込みだけを変更・調査するとき
- Ollama の正本仕様を確認したいときは、先に oracle/doc/app_spec/cmoc_managed_ollama.md を読む
- runtime path、runtime error、config の共通実装だけを確認する場合は、それぞれの直接担当ファイルを読む

## hash
- baaeb5ace3ecda0e9dcd841aa96e6301077bf539e09750fea44bf549a1481323

# `runtime_paths.py`

## Summary
- リポジトリ、worktree、cmoc の各 root 解決と、実行時の timestamp・duration 表示を提供する共通 runtime path/時刻ユーティリティ。session、report、log、schema、config、worktree などの保存先を一元化し、cwd の一時切替をスレッド安全に管理する。

## Read this when
- runtime directory や設定ファイル、session/report/log/schema/worktree の保存先を確認または変更するとき
- root placeholder の解決、cwd 起点の path 解決、timestamp・duration 表示、pushd の動作を確認するとき
- 複数の runtime path helper や agent 読み取り用 directory 判定の入口を探すとき

## Do not read this when
- 特定のサブコマンドの処理や出力仕様だけを調べるとき
- root 解決元の enum・path model 自体を変更または確認するときは、先に path model の実装を読むべき場合
- config JSON の内容や prompt/file access の規則そのものを確認するとき

## hash
- d64cab99562de13d029af8bc2ede34c6dded3394c30bf5f1ee9ec0cfe6c2f64a

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
