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
- CLI サブコマンド共通の実行ライフサイクルを扱う実装。work root 検査、pre log check、サブコマンドログ作成、開始・実行・完了の標準出力、戻り値の終了コード化、例外時のエラー表示とログ記録、現在サブコマンド logger の設定解除を一括で管理する。
- cmoc を work root で実行していることを検査する helper と、完了時に elapsed・quota wait・returncode などの標準サマリーを出力する helper を含む。

## Read this when
- CLI サブコマンド実行時の共通処理、特に開始・完了表示、サブコマンドログ、終了コード、例外表示、logger の runtime state 管理を確認または変更したいとき。
- サブコマンド実装関数の戻り値を CLI の終了コードとしてどう扱うか、または例外をどのように表示して `typer.Exit` へ変換するかを調べたいとき。
- repo root と work root の使い分け、init など一部コマンドで runtime state を work root 側に置く制御、またはサブコマンドログを置く root の扱いを追いたいとき。
- cmoc 実行時に現在ディレクトリが work root であることを要求する検査と、その失敗時の利用者向けエラー内容を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、永続データの具体的な読み書き内容を調べたいだけのとき。
- ログイベントの保存形式や current logger の内部実装そのものを変更したいときは、logging 側の共通実装を直接読む方が適切。
- repo root・work root の検出方法、タイムスタンプや経過時間文字列の生成規則を変更したいときは、path/runtime utility 側を直接読む方が適切。
- エラー型やエラーメッセージの描画規則そのものを変更したいときは、runtime error 側の実装を読む方が適切。

## hash
- ee0d71f61a971465f9e5e88c65e0ddf311be9a83609004cd2560a241a8715f40

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
- Codex CLI 実行時に使う profile/config 文字列、permission profile、Codex home、schema 複製、JSON 出力・JSONL エラー解析を扱う共通実装。
- AgentCallParameter と CmocConfig から model/reasoning_effort/sandbox または権限設定を組み立て、Codex CLI 呼び出し前後の環境・補助ファイル・失敗判定を支える。

## Read this when
- FileAccessMode と Codex sandbox/permission profile の対応、read/write/deny_read/read_only の生成規則を確認・変更したいとき。
- Codex profile の TOML 生成、hashed config file の作成先、profile 名の解釈、CODEX_HOME の解決・検証・サブプロセス環境を扱うとき。
- Codex 実行に渡す schema ファイルの準備、出力 JSON の読み取り、stdout/stderr からのエラーテキスト抽出、resume token 抽出、capacity/quota error 判定を調べるとき。

## Do not read this when
- cmoc のパス語彙や root/work/run の意味そのものを確認したいだけなら、パスモデルや runtime path 側を読む。
- AgentCallParameter、FileAccessMode、CmocConfig の型定義や設定 schema 自体を変更したい場合は、それらを定義する basic/config 側を直接読む。
- hashed file 書き込みの実装や schema store directory の配置規則そのものを変更したい場合は、runtime content または runtime paths 側を読む。

## hash
- ad405245d67f40e3cf691a364e1ab3b270b61498464ecf515c47681119078638

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
- ファイル内容または文字列内容から SHA-256 digest を計算し、その digest を名前に含めた内容ベースのファイル保存を行う小さな共通 helper 群を扱う。
- 出力先 directory を必要に応じて作成する保存処理と、既存 directory へ保存する処理を分け、同一内容なら既存ファイルを再利用する責務を持つ。
- 先頭 chunk の NUL byte と読み取り可否を使って、ファイルが binary かどうかを粗く判定する補助処理も含む。

## Read this when
- ファイル内容や文字列内容の SHA-256 digest 計算方法を確認・変更したいとき。
- 内容 hash をファイル名に含めて保存する runtime 生成物やキャッシュ的な出力の保存処理を確認・変更したいとき。
- 保存先 directory を自動作成する場合と、既存 directory 前提で保存する場合の挙動差を確認したいとき。
- ファイルが binary かどうかを判定する簡易 heuristic や、読み取り失敗時の扱いを確認・変更したいとき。

## Do not read this when
- パス概念そのものや `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の定義を確認したいだけのとき。
- CLI command、出力 schema、状態遷移、実行 workflow の仕様や制御ロジックを確認したいとき。
- INDEX.md の生成・更新・ルーティング文書そのものの仕様を確認したいとき。
- 特定の利用箇所で、どの prefix・suffix・content を渡すかという上位ロジックだけを確認したいとき。
- 構造化テキストの解析、markdown 処理、oracle/realization の分類判断を確認したいとき。

## hash
- 327f8182b1ab2047a3f5f70e49d2feb4fba2029da38769d649f9ed82f4175106

# `runtime_errors.py`

## Summary
- cmoc 共通の実行時例外と、任意の例外を利用者向け Markdown エラーレポートへ変換する処理を扱う。
- エラー概要、復旧・調査手順、詳細、Call stack を含む共通エラー表示の責務を持ち、独自例外と通常例外の両方を同じ出力構造へ寄せる入口になる。

## Read this when
- 利用者向けエラーレポートの出力内容、見出し、復旧案、詳細情報、Call stack の扱いを確認または変更したいとき。
- cmoc 内で投げる実行時例外に、Summary、Next actions、Detail として表示される情報を持たせたいとき。
- 通常例外が共通エラーレポートへ変換される際の既定メッセージや detail 表現を確認したいとき。
- Next actions が不足している場合に既定案内を補う挙動を確認または変更したいとき。

## Do not read this when
- 個別コマンドや個別入力検証で、どの条件をエラーにするかだけを調べたいとき。この対象はエラーの表示形式と共通例外の器を扱う。
- 設定、作業ツリー、path、git 操作など特定ドメインの失敗原因を調べたいとき。まずその責務を持つ実装を読む。
- エラー以外の通常出力、成功時の Markdown、JSON schema、永続状態の形式を確認したいとき。
- スタックトレース生成そのものや Python 標準例外機構の詳細を調べたいとき。

## hash
- 51eb58dfc241cb76b6debfce4a06a3169cb6a2a29d0a6f123f7c5b6c0bd03e95

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
- 外部コマンド実行結果と Codex exec 呼び出し結果を、変更不可の小さなデータ構造として共有する実装。終了コード、標準出力・標準エラー、生成出力、ログやプロファイル・schema へのパス、実行時間や quota 待機情報を、処理間で受け渡すための型を定義する。

## Read this when
- 外部コマンドの実行結果を返す・受け取る処理の戻り値構造を確認したいとき。
- Codex exec の呼び出し後に、出力本文、JSON 出力、ログ保存先、利用した codex home・profile・schema、経過時間や quota 待機情報をどの入れ物で扱うか確認したいとき。
- 実行系 helper や CLI 処理から返される runtime result の属性名を、利用側の実装やテストで合わせたいとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する手順、subprocess 呼び出し、ログファイル作成処理を調べたいとき。
- Codex exec の出力 JSON schema の意味や内容そのものを調べたいとき。
- profile、codex home、schema path の決定規則やパス解決規則を調べたいとき。
- 実行結果を CLI 出力へ変換する表示・整形ロジックを調べたいとき。

## hash
- d4046ead30e379a37a0dc1acdfaadc9477008c8aa79371515827408aec5f9971

# `runtime_state.py`

## Summary
- session branch と apply branch に紐づく永続 session state のデータ構造と JSON 入出力を扱う共有実装。
- session state file の保存先解決、branch 名からの session-id 抽出、現在 branch に対応する state 読み込み、canonical JSON 書き戻し、home branch に紐づく active session 探索をまとめて担う。

## Read this when
- session state file の schema、既定値、未知 field の扱い、session/apply の state 断片を確認したいとき。
- cmoc 管理 branch 名から session-id を取り出す処理や、不正な branch 名に対する CmocError の条件を確認したいとき。
- session state file の保存場所、読み込み、書き戻し、active session 検索に関わる実装を変更・調査するとき。

## Do not read this when
- CLI 引数定義、サブコマンドの dispatch、利用者向け出力形式だけを確認したいとき。
- git command の実行、branch 作成・切替・削除そのものの処理を調べたいとき。
- sessions directory を含む runtime path model 全般の定義だけを確認したいとき。

## hash
- 53330c5884ce75bb5beb6fd70ac0ba068730287d694504fcfedbcc95fa99e57f
