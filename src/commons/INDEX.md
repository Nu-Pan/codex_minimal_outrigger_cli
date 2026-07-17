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
- INDEX.md の更新前処理を担うモジュール。対象ツリーを走査し、欠落・変更されたエントリーを生成して保存・コミットするほか、既存エントリーの検証と Structured Output の Markdown 化を行う。

## Read this when
- INDEX.md の自動生成、更新順序、並列生成、排他ロック、更新コミットの挙動を変更・調査するとき
- INDEX.md エントリーの解析・ハッシュ鮮度判定・Structured Output 検証・描画処理を変更するとき
- Codex 呼び出し前の indexing preflight や実行コンテキストの扱いを確認するとき

## Do not read this when
- INDEX.md エントリーの文章内容そのものを確認・変更するときは、生成対象のファイルまたはディレクトリを直接読む
- 一般的な CLI 実行や preflight 以外の処理を調査するときは、対象の実装モジュールを直接読む
- INDEX.md の仕様上の要件や Codex 実行・ログ保存規則を確認するときは、対応する oracle 文書を読む

## hash
- 7d3ba54486aa619f6e7d1f7ee33dd68dc6127783afba2ae338d8cc400d21c606

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
- Codex CLI 呼び出し時の console 通知と、その失敗理由を console/event で共通化する error text 変換を扱う。

## Read this when
- Codex 呼び出しの開始通知、経過時間、終了コード、起動失敗メッセージの表示を変えたいときに読む。
- Codex 固有の失敗情報を、人間向け console 表示とイベント記録で同じ文面に揃えたいときに読む。

## Do not read this when
- 一般的なログ出力の整形や保存先を変えたいだけなら、汎用の runtime logging 側を読む。
- `codex exec` の引数構成、プロンプト生成、実行制御を変えたいだけなら、呼び出し本体の実装を読む。

## hash
- 6ca8648503df249ad1c39cf3d01e3c95496fd6762ca7d903a9caaa7b39b6f9d6

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行前に indexing preflight を挟む共通ランタイム層。preflight の登録・解除、再入抑止、直列実行、実行対象からの indexing root 決定を扱い、実際の Codex 呼び出しは runtime_codex へ委譲する。

## Read this when
- Codex exec または TUI の実行前 indexing 処理、preflight の設定・解除、再入防止や実行順序を変更・調査するとき。
- Codex 呼び出し設定から preflight の起点 root が決まる仕組みを確認するとき。

## Do not read this when
- Codex の実行本体やコマンド結果の詳細を変更・調査するときは、委譲先の runtime_codex または runtime_results を直接読む。
- リポジトリや作業ディレクトリの root 解決そのものを変更・調査するときは、runtime_paths を直接読む。

## hash
- 050693a5a2472180e927055cc8255f07e16e96627d7f16e6877a50b002eacfd4

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
- cmoc の実行時例外と利用者向け Markdown エラーレポート生成を担当する。CmocError が概要・次の行動・詳細を保持し、render_error が未知の例外も含めて Summary、Next actions、Detail、Call stack の共通形式へ変換する。

## Read this when
- 実行時エラーの構造、利用者向けエラーレポートの出力形式、復旧案の補完、コールスタックの扱いを変更・調査するとき。

## Do not read this when
- 特定の CLI コマンドの入力検証や業務処理だけを変更・調査するとき。
- エラーレポートの表示先や呼び出し側の制御を確認したいときは、まずその呼び出し側を直接読む。

## hash
- 152fcb4b8030f5fb2be82569787d2862effba44076d46afbc39bdb088b736e9a

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
- cmoc provider の local SLM を managed Ollama で利用可能にする単一の preflight 実装。Ollama の archive install、user systemd service の同期・起動、procfs による listener と executable の所有者確認、model の取得・load、GPU 使用確認までを一連の処理として扱う。

## Read this when
- cmoc provider の model を Ollama で serve・load する処理を変更または調査するとき
- Ollama の archive install、systemd user service、127.0.0.1:11434 の検証、procfs による process/socket 確認を扱うとき
- Ollama model の pull、API 応答、VRAM 使用確認や、それらの失敗時エラーを扱うとき

## Do not read this when
- cmoc provider の model を使用しない処理を扱うとき
- Ollama 以外の provider、一般的な runtime config、runtime path、runtime error の実装だけを扱うとき
- 既存の managed Ollama preflight の内部順序・検証・失敗条件を確認する必要がなく、別の上位処理を直接調べるとき

## hash
- de8547c0be605cfb5d80c3dce084e41a92885ad5d7ccce48e162927b3e692d30

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
