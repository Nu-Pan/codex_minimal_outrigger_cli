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
- 共通 runtime 層の主要な関数・型・定数を一箇所から取り込めるようにする集約入口。Codex 実行、profile・設定・content hash、CLI 前提条件、error 表示、git 操作、logging、path、実行結果、session state などの下位 runtime 要素への公開面をまとめる。
- 個別処理の実装本体ではなく、上位コードが共通 runtime 機能へアクセスするための import 境界を示す位置づけ。

## Read this when
- 共通 runtime API の公開入口にどの下位要素が含まれているかを確認したいとき。
- 上位モジュールから使える runtime helper、結果型、状態型、git helper、path helper などの import 経路を調整するとき。
- 共通 runtime 層の分割後に、既存の呼び出し側へ提供する symbol の追加・削除・移動影響を確認するとき。

## Do not read this when
- Codex 実行、profile 準備、設定同期、hash 書き込み、git 操作、logging、path 解決、session state などの具体的な挙動を変更したいとき。その場合は対応する下位実装を直接読む。
- 特定の CLI subcommand の処理順やユーザー向け出力を調べたいとき。より直接の command 実装や runtime helper を読む。
- 単一 helper の仕様・例外条件・副作用を確認したいとき。この集約入口ではなく、その helper が定義されている本文を読む。

## hash
- 697b93d9c8274835fd24b4573bca6b2be260ed6d224fcf13d28febda9d441568

# `runtime_cli.py`

## Summary
- CLI サブコマンドを共通実行するための実行ラッパーを定義している。work root での実行確認、repo root 取得、任意の事前チェック、サブコマンドログの開始・現在 logger の設定、進行状況の標準出力、実装関数の呼び出し、完了サマリー、例外の利用者向け表示、終了コード変換をまとめて扱う。
- 実行ディレクトリが work root であることを検証し、違う場合は利用者向けの cmoc エラーとして cwd と work_root を示す補助関数を持つ。
- サブコマンド完了時に、ログパス、実行時間、全体経過時間、quota wait、returncode を一貫した形式で表示する内部 helper を持つ。

## Read this when
- CLI サブコマンドの共通実行フロー、進行表示、完了表示、終了コード処理、例外処理を変更または確認したいとき。
- サブコマンドログの生成、current subcommand logger の設定・リセット、command_invoked / step_started / command_finished event の記録タイミングを確認したいとき。
- cmoc コマンドが work root 以外で実行された場合のエラー文言や判定条件を確認・変更したいとき。
- 個別サブコマンド実装を共通ラッパーから呼ぶ際の引数、任意の事前チェック、コマンド名、argv 記録の扱いを確認したいとき。

## Do not read this when
- 個別サブコマンド自体の業務処理、引数定義、Typer app への登録箇所だけを確認したいとき。
- ログファイルの具体的な保存形式、logger class の内部実装、quota wait の加算方法を確認したいとき。
- repo root や work root の探索規則、タイムスタンプや duration 文字列の整形規則を確認したいとき。
- cmoc 独自エラー型やエラーメッセージ描画の詳細を確認したいとき。

## hash
- 1c6305228cc49ae2ccad1da1862db8870c8e05b768b86a5564848648d01b6c4b

# `runtime_codex.py`

## Summary
- Codex CLI の exec/TUI 呼び出しを実行し、プロファイル準備、Structured Output schema の適用、呼び出しログ作成、標準出力・標準エラー・最終出力の保存、実行結果オブジェクトへの変換を担当する。
- exec 呼び出しでは capacity error の指数バックオフ再試行、quota error 時の代表プローブによる待機共有、resume token を使った再開、schema validation 失敗時の意味的再試行、成功・失敗イベントの記録まで扱う。
- TUI 呼び出しでは対話用の Codex CLI 起動、call log 記録、コンソール表示、subcommand logger へのイベント送信、失敗時の cmoc エラー化を行う。

## Read this when
- Codex CLI を外部プロセスとして起動する exec/TUI 実行経路、引数構築、作業ディレクトリ、環境変数、Codex home、プロファイル名の扱いを確認したいとき。
- Codex 呼び出しログ、stdout/stderr/output の保存先、call log の JSON 内容、コンソールに出る呼び出しサマリ、subcommand logger の codex_call event を変更・調査するとき。
- Structured Output schema を Codex exec に渡す流れ、出力 JSON の読み取り、jsonschema validation、validation 失敗時の再試行と失敗エラーを扱うとき。
- Codex CLI の capacity error、quota error、quota 回復プローブ、quota 待機時間集計、resume token による再開、関連するスレッド間待機制御を変更・調査するとき。
- Codex CLI 呼び出し失敗時に CmocError へ変換されるメッセージ、detail、ログパスの出し方を確認したいとき。

## Do not read this when
- Codex profile、Codex home、schema file の準備、quota/capacity 判定、出力 JSON 読み取りなどの個別 helper の中身を確認したいだけなら、それらを定義する profile 関連の実装を読む方が直接的。
- cmoc 設定ファイルの読み込み仕様や設定モデルそのものを確認したいだけなら、設定読み込み・設定定義の実装を読む方が直接的。
- ログディレクトリ、timestamp、work root、repo root、duration 表示などパス・時刻 helper の仕様を確認したいだけなら、runtime path 関連の実装を読む方が直接的。
- CodexExecResult や CommandResult のデータ構造だけを確認したい場合は、結果型を定義する実装を読む方が直接的。
- AgentCallParameter の項目、model class、reasoning effort、file access mode の定義だけを確認したい場合は、呼び出しパラメータ定義を読む方が直接的。

## hash
- 125bd504a2962ebefc813cf58b5590524a0fb3be570ea31acc114532578a708b

# `runtime_codex_profile.py`

## Summary
- Codex CLI 実行用の profile 文字列と関連ファイルを準備する runtime helper。AgentCallParameter と CmocConfig から model・reasoning_effort・sandbox/permission profile を TOML 断片として組み立て、CODEX_HOME の解決・検証、schema/output JSON の入出力、Codex JSONL 由来のエラー文・resume token・capacity/quota 判定を扱う。

## Read this when
- Codex CLI 呼び出し前に渡す profile 内容、sandbox_mode、permission_profile、writable_roots、read_only_paths、deny_read の生成規則を確認・変更したいとき。
- FileAccessMode と Codex 側の read-only/workspace-write 権限設定の対応、または root 指定時の詳細なファイルアクセス制御を追いたいとき。
- CODEX_HOME の解決、auth.json を含む Codex home 検証、profile ファイル生成、サブプロセスへ渡す環境変数の扱いを確認したいとき。
- Codex 実行に渡す structured output schema の保存、実行結果 JSON の読み取り、stdout/stderr からのエラー抽出、resume token 抽出、capacity/quota エラー判定を扱うとき。

## Do not read this when
- AgentCallParameter や FileAccessMode そのもののデータ定義・意味を確認したいだけなら、その基本型を定義する対象を読む。
- CmocConfig の設定ファイル構造や codex model/reasoning_effort の設定値定義を確認したいだけなら、設定定義を扱う対象を読む。
- runtime root、schema store directory、hashed file 書き込みの具体的なパス規則や保存実装を確認したいだけなら、runtime path/content を扱う対象を読む。
- Codex CLI を実際に起動する subprocess 制御、コマンドライン引数構築、実行フロー全体を確認したいだけなら、呼び出し側の実行制御を扱う対象を読む。

## hash
- a43192a0de11efb9376d2fdca1aa250ae46d782ab577941dfcd0b1715aec2e0f

# `runtime_config.py`

## Summary
- cmoc の実行時設定を、設定オブジェクト、dict、JSON ファイルの間で読み書きするための実装を扱う。
- 設定ファイルが存在しない場合の初期生成、既存設定の既定値とのマージ、不正な JSON や不正な設定値を利用者向けエラーへ変換する入口になる。

## Read this when
- `.cmoc/config.json` の読み込み、同期、書き戻し、既定値補完の挙動を確認または変更したいとき。
- 設定項目の JSON 表現、モデル種別や reasoning effort の文字列表現、並列数や review oracle / apply fork 関連の設定値変換を追うとき。
- 設定ファイルがない場合の自動生成、不正な JSON、不正な top-level 型、不正な enum 値や数値変換失敗時のエラー文言を確認したいとき。

## Do not read this when
- 設定値そのものの定義や既定値だけを確認したいときは、設定データ構造の定義を読む。
- 設定ファイルの配置パスや `<repo-root>/.cmoc/config.json` の導出規則だけを確認したいときは、runtime path の定義を読む。
- cmoc 共通エラー型の表示形式や出力処理を確認したいだけのときは、エラー定義やエラー表示側を読む。

## hash
- 9854b81ae9a3dd9422ac1d3e5f51d45a68e904bc34caa1d5bd25944acf91c495

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
- cmoc 管理 branch に対応する session state のデータ構造、JSON 読み書き、branch 名からの session-id 抽出、home branch に紐づく active session 探索を扱う実装。
- session 側と apply 側の状態断片を dataclass として保持し、永続化された状態ファイルとの相互変換を提供する。
- branch 現在位置から対象 session state を特定する処理や、状態ファイル不存在・不正な branch 名を cmoc の実行時エラーとして扱う入口になる。

## Read this when
- session state の schema、既定値、JSON への保存形式、または読み込み時に未知 key をどう扱うかを確認・変更したいとき。
- cmoc/session 系 branch または cmoc/apply 系 branch から session-id や状態ファイルを特定する処理を確認・変更したいとき。
- session state file の作成・更新・探索、特に home branch に対する active session の重複確認に関わる挙動を追うとき。
- branch 名が cmoc 管理 branch でない場合、apply branch 名が不完全な場合、状態ファイルが存在しない場合の CmocError を確認・変更したいとき。

## Do not read this when
- 単に cmoc のディレクトリ配置や sessions 保存先の root からの組み立て規則だけを確認したいときは、path 解決を担う対象を読む。
- CLI サブコマンドの引数定義、標準出力、コマンド全体の制御フローを確認したいときは、各コマンド実装を読む。
- git branch の作成・切替・削除など、git 操作そのものの実装を確認したいときは、git 操作を担う対象を読む。
- oracle snapshot の内容生成や比較ロジックを確認したいだけなら、その処理を担う対象を読む。

## hash
- 670b52609d707564d645840554dcef6f53815cb7114dd016f9d04599217fc42c
