# `__init__.py`

## Summary
- cmoc の共有ランタイム helper 群に属するパッケージ入口であることを示すだけの、ごく小さい初期化本文。現時点では公開 import や初期化処理を持たない。

## Read this when
- 共有ランタイム helper 群のパッケージ境界や、この階層が cmoc の共通実行時支援を扱う領域かを確認したいとき。

## Do not read this when
- 個別の helper 関数、クラス、定数、具体的な runtime 挙動を調べたいとき。その場合は同階層の責務別 runtime 実装本文へ進む。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- 共通ランタイム機能への単一入口として、Codex 実行、プロファイル、設定、内容ハッシュ、CLI 前提条件、エラー、Git、ログ、パス、結果型、状態管理の公開要素をまとめて再公開する集約モジュール。
- 個別の処理実装は各 runtime 系モジュール側にあり、この対象自体は呼び出し側がまとめて import できる境界を担う。

## Read this when
- 複数の共通ランタイム機能をまとめて利用する呼び出し側の import 経路を確認したいとき。
- 共通ランタイム API として外部へ露出している関数、型、定数の一覧を把握したいとき。
- runtime 系モジュール間の公開入口を整理し、集約 import の追加・削除・移動を判断するとき。

## Do not read this when
- Codex 実行、設定、Git 操作、パス解決、状態保存など個別機能の具体的な処理内容や失敗時挙動を確認したいときは、それぞれの実装モジュールを直接読む。
- 新しい共通処理の実装場所を探しているだけで、公開入口への追加要否をまだ判断しないとき。
- CLI サブコマンドの制御フローや利用者向け挙動を確認したいときは、呼び出し側または該当 runtime 実装を優先する。

## hash
- 553825cc815dfaed7496bdf6134689343ec5e2274a6502bbfc4709462f0e8002

# `runtime_cli.py`

## Summary
- CLI サブコマンド共通の実行ライフサイクルを管理する実装。work root 検査、サブコマンドログの作成と current logger 設定、開始・検査・実行・完了の標準出力、戻り値の終了コード化、例外の利用者向け表示と終了コード化を扱う。
- サブコマンドログは repo root に置きつつ、通常の runtime state は repo root、初期化対象を扱う場合だけ work root を runtime root として事前検査へ渡す、という実行時 root の使い分けを含む。
- 完了時の stdout サマリーには、ログパス、実行時間、総経過時間、quota wait、returncode を統一形式で出力する。

## Read this when
- CLI サブコマンド実装を共通ラッパー経由で実行したいとき、またはサブコマンド開始・実行・完了・失敗時の標準出力と終了コードの扱いを確認したいとき。
- サブコマンドログの生成場所、current logger の設定とリセット、command_invoked・step_started・command_finished イベント記録の流れを追う必要があるとき。
- work root で実行されていることの検査や、repo root と work root のどちらを runtime state 用 root として扱うかを確認・変更するとき。
- CmocError を含む例外を CLI 表示用エラーへ変換し、Typer の終了として扱う共通例外処理を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、状態ファイルの具体的な読み書きを調べたいだけのとき。
- runtime path の解決規則、タイムスタンプや duration の整形、repo root・work root の算出そのものを確認したいとき。
- サブコマンドログのファイル形式、イベント保存形式、quota wait の計測実装を調べたいとき。
- CmocError のデータ構造やエラーメッセージのレンダリング仕様そのものを確認したいとき。

## hash
- ebf798912f11e74a26e55eee92c6c692e197576e2fb08ca97ed5b56f58378c85

# `runtime_codex.py`

## Summary
- Codex CLI 呼び出し runtime の互換 import 入口。exec 実行本体と TUI 起動本体を責務別 module から再 export し、既存の `commons.runtime_codex` import path を維持する。
- この file 自体は実行制御を持たず、分割後の公開面を小さく保つための橋渡しだけを担う。

## Read this when
- 旧来の `commons.runtime_codex` import path がどの実装 module へ接続されるか確認したいとき。
- Codex runtime の責務分割後も、公開 import 面として `run_codex_exec` と `run_codex_tui` を維持する必要があるか判断したいとき。

## Do not read this when
- Codex exec の retry、Structured Output 検証、quota/capacity 制御、call log 記録を調べたいときは `runtime_codex_exec.py` を読む。
- Codex TUI の起動準備、call log、subcommand event、失敗時例外化を調べたいときは `runtime_codex_tui.py` を読む。
- Codex profile 名、Codex home、schema file、resume token、quota/capacity error 判定、output JSON 読み取りなどの個別 helper 実装だけを確認したいときは、それらを定義する profile 周辺の runtime helper を直接読む。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex CLI の exec 呼び出しを 1 回の状態機械として制御し、profile/schema 準備、subprocess 実行、stdout/stderr/output/call log 保存、Structured Output 検証、capacity retry、quota wait/probe、resume 継続、subcommand event 記録、成功時の結果生成をまとめて扱う実行制御モジュール。
- quota 処理や resume token、log/event、retry counter が同じ subprocess 結果を共有するため、exec 実行中の再試行・待機・検証・記録の流れを追う入口になる。
- 同一プロセス内で Codex call log 名の timestamp を単調増加させ、壁時計の後退や同時生成による log path 衝突を避ける補助処理も含む。

## Read this when
- Codex CLI の `exec` 実行時にどの argv、profile、schema、cwd、環境変数、入力 prompt が使われるかを確認したいとき。
- Structured Output schema の準備、検証、semantic retry、検証失敗時の error/log の扱いを調べるとき。
- capacity error の指数 backoff retry、quota error の代表 probe、他スレッドの quota wait 共有、quota wait 秒数・poll 回数の記録を変更または確認するとき。
- Codex CLI 失敗時に保存される stdout/stderr/output/call log と、console/subcommand log へ出る `codex_call` event の内容や status を追うとき。
- quota 回復後や quota 待機後に resume token を使って同じ作業を継続する制御を調べるとき。
- Codex exec の戻り値として result object に入る path、profile、schema、elapsed、quota wait 情報を確認するとき。

## Do not read this when
- Codex profile 名、Codex home、schema file の具体的な生成・解決・検証 helper の内部だけを調べたいときは、それらを提供する profile/config 系の共通処理を直接読む。
- TUI 起動や対話 UI の制御を調べたいときは、この対象ではなく TUI 側の実行制御を読む。
- subcommand logger 自体の保存形式、event writer、quota wait 集計の実装を調べたいだけなら logging 系の共通処理を読む。
- path model、repo/work/log directory、timestamp 生成の一般ルールを調べたいときは path 系の共通処理を読む。
- Codex exec 成功後の result object の型定義や利用側だけを確認したいときは、結果型または呼び出し元を読む。

## hash
- 416908caa21d6d09e16717099112ef44e519f787d81cf214b68a1f8543a3a22a

# `runtime_codex_logging.py`

## Summary
- Codex exec/TUI 呼び出し単位の完了サマリーを利用者の console へ出力する小さな共有 helper を扱う。
- Codex call log path、purpose、elapsed、returncode を同じ表示形式にそろえるための補助であり、exec/TUI の起動制御や retry は持たない。

## Read this when
- Codex exec/TUI 共通の console 表示形式、表示項目、timestamp や duration の出し方を変更・確認したいとき。
- Codex runtime の呼び出し完了サマリーだけを調べたいとき。

## Do not read this when
- Codex exec の retry、Structured Output 検証、quota/capacity 制御を調べたいときは `runtime_codex_exec.py` を読む。
- Codex TUI の起動準備や失敗時例外化を調べたいときは `runtime_codex_tui.py` を読む。
- サブコマンド単位の JSON Lines event 保存や quota 待機時間の集計を調べたいときは logging 側の runtime helper を読む。

## hash
- 65cfde582382659dd394662fe73f4e8796945c7ad06a7f2d2240181e63abaab8

# `runtime_codex_preflight.py`

## Summary
- Codex 実行/TUI 起動の直前に、設定済みの indexing preflight を一度だけ走らせるための薄い実行ラッパーを定義している。
- preflight の登録・解除、実行対象 root の決定、再入防止、排他制御、indexing 用途や conflict resolution 用途では preflight を省略する判定を扱う。
- 実際の Codex 実行処理そのものは runtime 側へ委譲し、この対象は実行前フックの制御だけを担当する。

## Read this when
- Codex exec または Codex TUI を呼び出す前に、INDEX.md 生成などの indexing 処理を自動実行する経路を確認・変更したいとき。
- indexing preflight の登録、無効化、再入防止、スレッド間排他、skip 条件の挙動を調べたいとき。
- Codex 呼び出し時の cwd/root から、indexing 対象 root がどう決まるかを確認したいとき。
- indexing 自体がさらに Codex exec を呼ぶ場合の循環防止や、conflict resolution 時に preflight を避ける理由を追うとき。

## Do not read this when
- Codex CLI プロセスの実際の起動、コマンドライン構築、戻り値変換、標準入出力処理を調べたいだけのとき。
- repo root、work root、cwd 変換などの path model や runtime path 解決そのものを調べたいとき。
- Codex 実行結果やコマンド実行結果のデータ構造を確認したいだけのとき。
- INDEX.md の内容生成ロジック、エントリー生成プロンプト、ファイル探索ルールそのものを調べたいとき。

## hash
- 3878cafea4f3209a564a38a3ebe0f67ca85915e34f09112258511701c00f4c48

# `runtime_codex_profile.py`

## Summary
- Codex CLI を呼び出すための実行時プロファイルと周辺入出力を組み立てる実装。モデル・reasoning_effort・sandbox/permission profile を設定文字列へ変換し、Codex home の解決と検証、profile/schema の一時生成、サブプロセス環境、Codex 出力 JSON/JSONL からのエラー・resume token・容量/ quota 判定を扱う。

## Read this when
- AgentCallParameter と設定値から Codex CLI 用の profile 内容を生成・変更したいとき。
- FileAccessMode ごとの sandbox mode、permission profile、読み書き許可・deny/read_only・writable_roots の対応を確認したいとき。
- CODEX_HOME の解決、存在・ディレクトリ・auth.json 検証、Codex サブプロセスへ渡す環境変数を扱うとき。
- Codex 実行前に schema を hashed file として配置する処理や、Codex 実行後の JSON 出力、stderr/stdout 由来のエラー文、resume token、capacity/quota error 判定を扱うとき。

## Do not read this when
- Codex CLI の呼び出しそのもののプロセス起動、コマンドライン引数構築、retry 制御を調べたいだけのとき。
- cmoc 全体の path model や schema store のディレクトリ定義そのものを調べたいとき。
- AgentCallParameter、FileAccessMode、CmocConfig のデータ構造や設定読み込み仕様を確認したいとき。
- hashed file の保存方式や内容ハッシュ生成の詳細を変更したいとき。

## hash
- 95ca96368d1a286017946077d159e05e5bf50859c6739eecb4caeea42c8df740

# `runtime_codex_tui.py`

## Summary
- Codex CLI の対話型 TUI 起動を扱う runtime 層。profile と call log を準備して `codex` を起動し、console/subcommand log へ結果を記録して、失敗時は cmoc 用例外へ変換する。
- exec retry や Structured Output 検証は持たず、対話起動に必要な profile、argv、call log、戻り値変換だけを担う。

## Read this when
- Codex TUI の argv、cwd/env、profile 準備、extra read path、call log、subcommand event、失敗時例外化を確認または変更したいとき。
- 対話起動の runtime 制御を exec の retry 制御から切り離して調べたいとき。

## Do not read this when
- Codex exec の retry、Structured Output 検証、quota/capacity 制御を調べたいときは `runtime_codex_exec.py` を読む。
- Codex profile 生成や Codex home 検証の低レベル helper だけを調べたいときは profile 周辺の runtime helper を読む。

## hash
- 3ed236afcdeaea95975325e2dab8c6d80a050e4201c18805ba9d8dbf3f875a99

# `runtime_config.py`

## Summary
- cmoc 設定を、内部設定オブジェクトと永続化用 JSON object の間で相互変換し、設定ファイルの読み込み・書き込み・存在しない場合の初期同期を扱う実装。
- 設定値の既定値補完、列挙値キーの復元、不正な型・値・JSON 構文・top-level 非 object に対する利用者向けエラー化を担う。

## Read this when
- cmoc 設定ファイルの JSON schema 相当の入出力形、既定値補完、設定項目追加・削除・名称変更に伴う永続化形式を確認または変更したいとき。
- 設定ファイルが存在しない、不正 JSON、top-level が object でない、列挙値や数値へ変換できない場合のエラー文言・補足案内・例外経路を確認または変更したいとき。
- 設定ファイルの生成、再書き込み、読み込み、既存設定の正規化を行う処理の入口を確認したいとき。

## Do not read this when
- 個々の設定データクラスのフィールド定義や既定値そのものを確認したいだけの場合は、設定モデル定義を直接読む。
- 設定ファイルの配置場所やパスキーワードの意味を確認したいだけの場合は、パス解決を担う実装またはパスモデル仕様を直接読む。
- CLI コマンドの引数解釈、サブコマンドの実行順、設定値を使う各機能の挙動を調べたい場合は、それぞれの呼び出し側や機能実装を読む。

## hash
- aef509c7c07682149b5db71e9bfcdce5c7fcab10722f26d36d70d3ad0e3ad2f7

# `runtime_content.py`

## Summary
- 文字列やファイル内容の SHA-256 ダイジェスト計算と、そのダイジェストを名前に含む内容アドレス型ファイルの書き込みを扱う小さな共通 helper 群。
- 出力先ディレクトリを作成してから書く場合と、既存ディレクトリ前提で書く場合を分け、既存ファイルの内容が同じなら不要な再書き込みを避ける。
- ファイル先頭の一部を読み、NUL バイトの有無や読み取り失敗から binary file とみなす判定も提供する。

## Read this when
- 実行時に生成する一時・キャッシュ・成果物などを、内容ハッシュを含むファイル名で保存する処理を確認または変更したいとき。
- 文字列またはファイル内容から SHA-256 digest を得る共通処理を探しているとき。
- 保存前に出力先ディレクトリを作るべきか、既存ディレクトリ前提で書くべきかという hashed file 書き込み helper の使い分けを確認したいとき。
- 対象ファイルが text として扱えるかを粗く判定する binary 判定の挙動を確認したいとき。

## Do not read this when
- cmoc のパス概念、root 種別、パス正規化、または `<cmoc-root>` などの定義を確認したいだけのとき。
- 特定の CLI command、oracle file、INDEX.md 生成、Git 操作などの業務ロジックを確認したいとき。
- ハッシュ付きファイル名を使わない通常のファイル読み書き、JSON 入出力、設定読み込みの実装を探しているとき。
- 暗号用途の署名、認証、鍵管理、セキュリティポリシーとしてのハッシュ利用を調べたいとき。

## hash
- 7116a86511c8ee8fe0abca1e4b8778ee6e54c94c0ac049c0193c7173040e2524

# `runtime_errors.py`

## Summary
- cmoc 共通の実行時エラー表現を定義し、利用者向けエラー出力を一定の見出し構造に整形する小さな共通モジュール。
- 独自例外では Summary、Next actions、Detail を保持し、それ以外の例外では既定の案内と例外表現を使って Call stack 付きのエラー文面を生成する。

## Read this when
- cmoc 全体で使う独自実行時エラーの構造、保持する情報、呼び出し側が渡すべきエラー要約・次アクション・詳細を確認したいとき。
- 例外を利用者向けの `# ERROR` 形式へ変換する処理や、Summary、Next actions、Detail、Call stack の並びを変更・検証したいとき。
- 独自例外ではない通常の例外が発生した場合に、どの既定メッセージや detail が出力されるかを確認したいとき。

## Do not read this when
- 個別コマンドがどの条件でエラーを発生させるか、どの summary や detail を渡すかを調べたいだけのとき。
- エラー出力後のプロセス終了コード、CLI 引数処理、標準出力・標準エラーへの書き込み経路を調べたいとき。
- パスモデル、作業ツリー状態、設定値など、エラー原因そのものの判定ロジックを確認したいとき。

## hash
- f5ef88c7fd0b75421e70d11bae48427f49c53acc612809b234a7aa9a7f073a8b

# `runtime_git.py`

## Summary
- Git コマンド実行を共通化し、失敗時に cmoc の実行時エラーへ変換するための低レベル helper 群を扱う。
- 現在 branch、HEAD commit、worktree 清潔性、管理対象 branch 判定、branch 存在確認、run worktree 作成・削除、branch 削除など、Git 状態と worktree 操作の共通処理を提供する。
- cmoc の内部ディレクトリを Git 追跡対象外にする初期化・検証と、任意 path が Git ignore 対象かを判定する処理もここにまとまっている。

## Read this when
- cmoc の各コマンドから Git を実行する共通方法、戻り値の扱い、失敗時の CmocError 化を確認・変更したいとき。
- 実行用 worktree の作成・削除、管理 branch の判定、branch の存在確認や削除に関する実装を追うとき。
- 未コミット差分がある場合の拒否、detached HEAD の拒否、現在 branch や HEAD commit の取得など、Git 状態の前提条件を扱う処理を確認するとき。
- cmoc の内部ディレクトリを .gitignore と git index 上で追跡対象外にする処理、または ignore 判定の挙動を確認・変更したいとき。

## Do not read this when
- CLI 引数の解析、サブコマンドの組み立て、ユーザー向け出力形式だけを確認したいとき。
- Git 以外の path モデル、設定読み込み、構造化結果の定義、または Codex 実行制御の詳細を調べたいとき。
- 個別コマンドがどのタイミングで Git helper を呼ぶかという上位フローを知りたいだけの場合は、先にそのコマンド実装を読む。
- Git 操作のテストケースや期待される外部挙動を確認したい場合は、対応するテストを読む。

## hash
- 31172a71170d0136db6767dbc6b344927cc2fa5c6abf5a9046f156013e5bb090

# `runtime_logging.py`

## Summary
- サブコマンド実行中のイベントを JSON Lines 形式で実行ログへ追記するための共有実装。
- サブコマンド名、発生時刻、任意 payload を含むログ record を作り、実行開始からの経過時間と quota 待機時間を保持する。
- 現在のサブコマンド用 logger を context-local に設定・解除・取得する入口を提供する。

## Read this when
- サブコマンド単位の実行ログの生成場所、record に含まれる基本項目、追記タイミングを確認したいとき。
- ログ保存先ディレクトリの作成、ログファイル名の作り方、JSON Lines 書き込みの副作用を追う必要があるとき。
- quota 待機時間の累積や、サブコマンド実行時間の計測を変更・確認したいとき。
- 現在のサブコマンド logger を contextvars 経由で受け渡す処理を確認したいとき。

## Do not read this when
- ログ保存先パスや timestamp 文字列そのものの定義を確認したいだけのときは、runtime path を扱う対象へ進む。
- ログ内容を読む側、集計する側、表示する側の仕様や実装を探しているときは、それらの処理を持つ対象へ進む。
- CLI サブコマンドの引数定義、dispatch、終了コード、利用者向け出力を確認したいときは、CLI 実行制御を扱う対象へ進む。
- 通常の path model や root 種別の概念定義を確認したいときは、path model を扱う対象へ進む。

## hash
- e2e4d1e5000c03dde22b8c79c07e036859d091813787c5b6d8a7efb15fe08d44

# `runtime_paths.py`

## Summary
- 実行時に必要な root path の解決、cmoc 管理ディレクトリや設定ファイルの path 組み立て、時刻文字列、作業ディレクトリ一時変更を扱う共通 helper 群。
- <repo-root>、<work-root>、<cmoc-root> の特定に失敗した場合は利用者向けの CmocError に変換し、呼び出し側が path 解決失敗を共通のエラー形式で扱える入口になる。
- `.cmoc` 配下の sessions、reports、log、worktrees、state、config の保存先を、渡された root から一貫して導出する責務を持つ。

## Read this when
- 実行時に <repo-root>、<work-root>、<cmoc-root> をどのように特定し、失敗時にどの CmocError を出すかを確認・変更したいとき。
- `.cmoc` 配下の sessions、reports、sub command log、codex log、worktrees、schema state、config の配置規則を確認・変更したいとき。
- レポート名、ログ名、表示用時刻などに使う timestamp 文字列や duration 表示の形式を確認・変更したいとき。
- 処理中だけ作業ディレクトリを変更し、終了時に元のディレクトリへ戻す共通処理を使う箇所を調べたいとき。

## Do not read this when
- path キーワードそのものの意味や <cmoc-root>、<repo-root>、<run-root>、<work-root> の概念定義を確認したいだけのときは、path model の定義を直接読む。
- CmocError の表示形式、属性、レンダリング、終了処理を確認したいときは、runtime error を扱う対象を直接読む。
- 個別サブコマンドが sessions、reports、logs、worktrees をどのタイミングで作成・更新・削除するかを調べたいときは、そのサブコマンド実装や状態管理の対象を読む。
- git repository や git worktree の探索アルゴリズム自体を変更したいときは、root 解決を実装している path model 側を読む。

## hash
- ba602d99cbeee08c3659843f561c7cd76d53a274fcf996e15f9945ef32ede11f

# `runtime_results.py`

## Summary
- 外部コマンド結果 `CommandResult` と Codex exec 結果 `CodexExecResult` の共有データ型を定義する。

## Read this when
- subprocess や Codex 呼び出し wrapper の戻り値として共有されるフィールドを確認・変更したいとき。

## Do not read this when
- 実際の git/Codex 実行処理、ログ保存、retry 制御を変更したいとき。

## hash
- bc07588fcd418f58345aaaf5fa48ed9b3883bbf1e0d628d07ed74c959c60c719

# `runtime_state.py`

## Summary
- session state file の永続化モデルと、cmoc 管理 branch から対応する session state を特定・読み書きする処理を担う。
- session と apply の状態断片を dataclass として集約し、未知 field を無視して既定値で復元する JSON 変換、保存先 path の組み立て、canonical JSON での書き戻しを扱う。
- 現在 branch が session branch または apply branch であることを検証し、branch 名から session-id を取り出して state file を読み込む入口を提供する。

## Read this when
- session state file の schema、既定値、前方互換的な読み込み挙動を確認・変更したいとき。
- cmoc/session または cmoc/apply branch 名から session-id を取り出す規則や、branch 不正時の CmocError を確認・変更したいとき。
- session state file の保存場所、読み込み、書き戻し、home branch に紐づく active session 検出の挙動を調べたいとき。
- apply run の進行状態と session branch と home branch の関係を、永続状態としてどの field に持つか確認したいとき。

## Do not read this when
- CLI 引数の定義、サブコマンドの入出力、利用者向け表示だけを調べたいとき。
- cmoc 管理ディレクトリ全体の path 定義や sessions directory の基準を変更したいときは、path を定義する対象を直接読む。
- git branch の作成・削除・checkout など、実際の git 操作手順を調べたいとき。
- state file を使わない一時的な実行状態、ログ、設定値、oracle 文書の仕様を調べたいとき。

## hash
- 6210da600bbbe647a5df4d5a14ac143209c4ebd6dfbc83a1ef6b359ba006b31c
