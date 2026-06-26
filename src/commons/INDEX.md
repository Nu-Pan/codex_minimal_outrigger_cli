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
- 実行時処理で共通利用される helper・型・定数を一箇所から import できるように集約する入口。Codex 実行、profile、設定、ファイル内容、CLI 前提確認、エラー、git、logging、path、結果型、状態管理の公開 import 面を束ねるだけで、個別処理の実装は持たない。

## Read this when
- 実行時共通機能を利用する側で、どの helper・型・定数をまとめて import できるか確認したいとき。
- 実行時共通 API の集約面に、新しい helper の公開や不要になった公開 import の削除を行うとき。
- サブコマンド周辺の実装が参照する実行時 helper 群の入口を確認したいとき。

## Do not read this when
- Codex 実行、profile、設定、ファイル内容、CLI、エラー、git、logging、path、結果型、状態管理それぞれの具体的な挙動や副作用を確認したいとき。その場合は該当する個別実装を読む。
- 特定 helper の仕様、入力、出力、失敗時挙動を変更したいとき。この集約入口ではなく、その helper が定義されている実装を読む。
- テスト観点や利用者向け挙動を確認したいだけで、実行時共通 API の import 面を扱わないとき。

## hash
- 028f4dbeed1e9bc071b8b98b7f13a8b8e8c31ded9fe29841cc9cf665e8a110f1

# `runtime_cli.py`

## Summary
- CLI サブコマンドの実行共通処理を扱う実装。実行前にカレントディレクトリが work root であることを確認し、必要なら事前検査を行ったうえで、サブコマンド単位のログ設定、開始・実行・完了の標準出力、戻り値の終了コード化、例外の利用者向け表示をまとめて担う。
- サブコマンド実装本体ではなく、その周囲で共通に必要になる実行ライフサイクル、ログイベント、Typer の終了制御、実行時間・quota wait を含む完了サマリー出力の入口として読む対象。

## Read this when
- サブコマンド実行時の共通ラッパー、開始・実行・完了の表示順、サブコマンドログの生成と current logger の設定・解除を確認または変更したいとき。
- サブコマンドの戻り値を終了コードとして扱う挙動、非 0 戻り値での Typer 終了、例外発生時のログ記録・エラー表示・終了コードを調べたいとき。
- cmoc を work root 以外で実行した場合のエラー条件や、実行前チェックをサブコマンドログ生成前に差し込む流れを確認したいとき。
- CLI の完了サマリーに出る実行時間、quota wait、returncode、ログパスの出力内容や計算元を追いたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向けコマンド構成を調べたいだけのとき。
- ログファイルの形式、イベント保存方法、current logger の内部状態管理そのものを変更したいとき。
- repo root、work root、時刻文字列、duration 表示の算出規則を調べたいとき。
- cmoc 独自エラーのデータ構造や表示整形そのものを変更したいとき。

## hash
- ed43ac970f83fd30c27eda352236ccfaf0c3172624a017e3b0758e6c15bd27a5

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
- Codex CLI の exec 実行を 1 回の状態機械として制御する実装。profile/schema/log path の準備、subprocess 呼び出し、stdout/stderr/output/call log の保存、subcommand event 発行、Structured Output 検証、capacity retry、quota polling と resume 継続、oracle 書き込み guard をまとめて扱う。
- TUI 起動や profile 生成そのものではなく、Codex exec 呼び出しの再試行・検証・記録・結果返却の分岐を追う入口として読む。

## Read this when
- Codex CLI の exec 呼び出し条件、argv、cwd/env、profile/schema/output path、call log の内容を確認・変更したいとき。
- Structured Output schema 検証失敗時の semantic retry、capacity error 時の指数 backoff、quota error 時の代表 probe・待機共有・resume token 継続の制御を確認・変更したいとき。
- Codex 呼び出しの stdout/stderr/output/call log、console 出力、subcommand log event、quota wait 計上の関係を追いたいとき。
- REALIZATION_WRITE 時に oracle 配下の許可外変更を検出する guard の対象・タイミング・失敗時挙動を確認したいとき。
- CodexExecResult に入る実行結果、ログ path、profile/schema 情報、経過時間、quota wait 情報の生成元を確認したいとき。

## Do not read this when
- Codex profile 名、Codex home、resume token 抽出、capacity/quota error 判定、output JSON 読み取りなどの個別 helper の仕様を確認したいだけなら、それらを定義する runtime profile 側を読む。
- cmoc config の読み込みや設定値の構造を確認したいだけなら、config 読み込み・設定定義側を読む。
- subcommand logger の構造、event 保存形式、runtime path の意味、または CodexExecResult 型そのものを確認したいだけなら、それぞれの logging・paths・results 側を読む。
- Codex TUI 起動や exec 以外の Codex 実行経路を調べたいときは、この対象ではなく該当する起動制御 module を読む。

## hash
- 0f36f7d17bdfaf05c4986758ec8bc10088d623f3c60475a4d367b390966d2ade

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
- Codex CLI 呼び出し用の実行プロファイルと周辺ランタイム値を組み立てる共通処理を扱う。file access mode から sandbox/permission profile 設定へ変換し、読み書き可能範囲、読み取り禁止範囲、追加 read-only パスを TOML 断片として生成する。
- Codex home の解決・検証、認証情報の存在確認、hashed profile/schema ファイルの準備、子プロセス環境変数、出力 JSON・JSONL エラー・resume token・capacity/quota 判定など、Codex CLI 実行前後の補助処理への入口になる。

## Read this when
- Agent call parameter と設定値から Codex CLI に渡す model、reasoning_effort、sandbox_mode、permission profile をどう生成するか確認したいとき。
- readonly、oracle read、realization write、oracle write、repo write の各 file access mode が、読み取り・書き込み・deny_read・read_only・writable_roots にどう反映されるか確認したいとき。
- realization write で oracle 配下の一部だけを書き込み許可する場合に、他の oracle パス、memo、.agents をどう read-only 扱いにするか確認したいとき。
- CODEX_HOME の解決規則、Codex home の妥当性検査、認証ファイル欠落時のエラー、Codex 子プロセスへ渡す環境変数を扱う変更をするとき。
- Codex profile や schema を hashed file として配置する処理、またはその失敗時に利用者へ返す CmocError を確認・変更するとき。
- Codex CLI の stdout/stderr から JSON 出力、エラーメッセージ、thread id、capacity error、quota error を読み取る処理を確認・変更するとき。

## Do not read this when
- cmoc のパス語彙や root/work/run の概念定義そのものを確認したいだけの場合は、パスモデル側の仕様・実装を直接読む。
- hashed file の書き込み方式、保存先ディレクトリ作成、内容ハッシュ化の詳細を確認したい場合は、ランタイム content 管理側を読む。
- FileAccessMode や AgentCallParameter の型定義、モデルクラス・reasoning effort の列挙を確認したい場合は、basic 側の agent call parameter 定義を読む。
- CmocConfig の読み込み元、既定値、設定 schema を確認したい場合は、config 側を読む。
- Codex CLI を実際に起動する制御フロー、subprocess の呼び出し順、リトライや上位 command の振る舞いを確認したい場合は、この補助処理の呼び出し元を読む。

## hash
- 94d548b8af6d5efb6fa6b87d39cad6a716b7d1457a3519e867f41a0ae486e076

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
- file/text sha256、内容 hash 付きファイル生成、binary 判定を扱う。

## Read this when
- hash に基づく生成ファイル名、ファイル内容更新判定、binary 判定の共通処理を変更したいとき。

## Do not read this when
- git ignore 判定や INDEX.md の hash 更新ロジックを調べたいとき。

## hash
- a914c083a867428af66f067f4a90c2f94123f6c97d0af270e8802bfbef05b28f

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
- Git コマンド実行を共通化し、失敗時に cmoc 向けの実行時エラーへ変換する実装を扱う。
- 現在 branch、HEAD commit、worktree の clean 判定、branch 存在確認、managed branch 判定など、Git repository 状態を調べる helper 群を提供する。
- run 用 worktree の作成・削除、branch 削除、worktree prune など、cmoc が一時的に使う Git worktree と branch の後始末を扱う。
- .cmoc が Git 追跡対象外であることの初期化・検証と、任意 path が Git ignore 対象かどうかの判定を扱う。

## Read this when
- Git コマンド呼び出しの共通エラー処理、標準出力・標準エラー・終了コードの扱いを確認または変更したいとき。
- cmoc 実行前に detached HEAD、未コミット差分、branch 存在、HEAD commit など Git repository 状態を検査する処理を追うとき。
- cmoc が生成・削除する一時 worktree や managed branch の命名判定、作成、削除、prune の挙動を確認または変更したいとき。
- .cmoc を Git index から外し、ignore されている状態を保証する初期化・検証処理を確認または変更したいとき。
- Git ignore 判定を cmoc の実行時制御に使う箇所の低レベル helper を確認したいとき。

## Do not read this when
- CLI 引数定義、サブコマンドの dispatch、ユーザー向け出力形式を調べたいだけのとき。
- cmoc 固有の path keyword や root path モデルの定義を調べたいとき。
- Git 以外の永続状態、設定ファイル、prompt、実行記録の schema を調べたいとき。
- 外部コマンド一般の抽象化ではなく、特定サブコマンドの業務フローや高レベルな制御順序を確認したいとき。
- テストケースや fixture 側から期待挙動を確認する方が直接的なとき。

## hash
- 0a6dd3fc4a430ad1017e13f7297d632b7f3fcc98fa1e7c75d3738ce06deb4522

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
- session branch と apply branch に紐づく永続 state の構造、保存先、読み書き、branch 名からの session-id 抽出を扱う共通実装。
- session state file を dataclass へ復元し、未知 field を無視しつつ欠落 field を既定値で補う互換的な読み込みと、canonical JSON 形式での書き戻しを提供する。
- home branch に対応する active session の探索や、cmoc 管理 branch ではない場合・state file が存在しない場合の利用者向けエラー生成の入口になる。

## Read this when
- session state file の schema、既定値、JSON 永続化形式、読み込み時の未知 field・欠落 field の扱いを確認または変更したいとき。
- cmoc/session または cmoc/apply branch 名から session-id を特定する処理や、branch 名不正時のエラー文言・判定条件を確認または変更したいとき。
- active session にぶら下がる apply run の状態、session と home branch の対応、最後に join した oracle snapshot commit の保持方法を追うとき。
- home branch から active session state file を探す処理、または state file の保存場所を決める処理を確認したいとき。

## Do not read this when
- CLI サブコマンドの引数定義、画面出力、コマンド全体の制御フローだけを確認したいときは、各 command 実装を読む。
- session state file の親ディレクトリや run/work/cmoc root の定義そのものを確認したいときは、runtime path を扱う共通実装を読む。
- CmocError の表示形式、例外クラスの責務、エラー出力全体の整形を確認したいときは、runtime error を扱う共通実装を読む。
- git branch の作成・切替・削除など、実際の git 操作を確認したいだけのときは、git 操作や各 workflow の実装を読む。

## hash
- 624c3a7d79aca459ea3b8c59120e7ebf3f0c478b5898b5c35fa77cb313245791
