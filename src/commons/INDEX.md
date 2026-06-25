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
- CLI サブコマンド実行を共通化する runtime helper。work root での実行確認、pre-log 検査、サブコマンドログの開始・現在 logger の設定、3 段階の進捗表示、実装関数の戻り値処理、完了 summary 出力、例外の cmoc 向け表示と終了コード化をまとめて扱う。
- サブコマンド本体そのものではなく、複数の CLI command から共有される実行ラッパーと、work root 強制、完了時の経過時間・quota wait・returncode 表示を担う。

## Read this when
- CLI サブコマンドの共通実行フロー、進捗表示、終了コード、例外表示、サブコマンドログ生成・current logger 設定の挙動を確認または変更したいとき。
- コマンド実行前に cwd が work root であることを強制する条件や、その失敗時に利用者へ出す cmoc error の内容を確認したいとき。
- サブコマンド完了時に標準出力へ出る timestamp、log path、execute elapsed、quota wait、returncode の summary 形式を扱うとき。
- 個別サブコマンド実装を、共通の logging・error handling・Typer exit 処理に載せる呼び出し側を調べるとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、ファイル生成内容を知りたいだけのときは、そのサブコマンド実装を読む。
- ログファイルの具体的な保存形式、event の JSON 構造、quota wait の加算処理を調べたいときは、runtime logging 側を読む。
- repo root、work root、timestamp、duration format の算出規則を調べたいときは、runtime paths 側を読む。
- cmoc error の型や render 形式そのものを調べたいときは、runtime errors 側を読む。

## hash
- caa3c7d49cc50dc8cb9ca6c702be554b196f73a77bafb93b9c90b5017b3a1610

# `runtime_codex.py`

## Summary
- Codex CLI を実行する runtime 層で、exec 呼び出しと TUI 呼び出しの組み立て、call/stdout/stderr/output のログ記録、Structured Output 検証、失敗時の CmocError 化を担う。
- exec 呼び出しでは profile・schema・環境を準備し、capacity error の指数バックオフ再試行、quota error の共有 polling 待機と resume token による再開、成功時の実行結果オブジェクト生成までを扱う。
- TUI 呼び出しでは profile 準備、呼び出しログ作成、Codex CLI/TUI の subprocess 実行、subcommand logger へのイベント記録を扱う。

## Read this when
- Codex CLI の exec/TUI 呼び出し方法、引数、作業ディレクトリ、環境変数、profile、schema の受け渡しを確認・変更したいとき。
- Codex CLI 呼び出しのログファイル作成、ログ payload、subcommand logger へ出す codex_call / codex_tui_call event を追いたいとき。
- Structured Output の出力読み取り、jsonschema 検証、検証失敗時の semantic retry、最終的な実行結果への詰め替えを確認したいとき。
- capacity error や quota error に対する再試行、待機、代表 probe、resume token 再利用の制御を変更・調査したいとき。
- Codex CLI の subprocess returncode や stderr/stdout から CmocError を発生させる境界を確認したいとき。

## Do not read this when
- Codex home の解決、profile ファイル生成、schema ファイル準備、quota/capacity error 判定、resume token 抽出の個別ロジックだけを確認したいときは、それらを提供する profile/runtime 補助層を直接読む。
- log directory、timestamp、duration 表示、repo/work root など path・時刻 helper の定義だけを確認したいときは、runtime path 補助層を直接読む。
- 設定ファイルの読み込みや設定型そのものを確認したいときは、config 読み込み・設定定義側を読む。
- 実行結果型や command result 型のフィールド定義だけを確認したいときは、runtime result 定義側を読む。
- AgentCallParameter の構造、model class、reasoning effort、file access mode の定義だけを確認したいときは、basic/acp 側を読む。

## hash
- 31ac1cf68d1e0f8081562b151041c2532f726ac2266cefae884065d90a7ba167

# `runtime_codex_profile.py`

## Summary
- Codex CLI 呼び出し用の runtime 設定を組み立てる共通実装。file access mode から sandbox/permission profile 設定へ変換し、model・reasoning effort と合わせた profile text を生成する。
- Codex home の解決・検証、hashed profile/schema file の準備、subprocess 用環境変数、Codex JSONL 出力からの error/resume token 抽出、capacity/quota error 判定を扱う。

## Read this when
- Codex CLI に渡す profile の model、reasoning_effort、sandbox_mode、permission profile、writable_roots、read_only_paths、read/deny_read/write 制約の生成内容を確認・変更するとき。
- FileAccessMode ごとの read/write/deny_read/read_only の対応、memo・oracle・.agents の扱い、root 指定時と未指定時の設定差を確認するとき。
- CODEX_HOME の解決規則、auth.json を含む Codex home 検証、profile 生成失敗時の CmocError 内容、Codex subprocess に渡す環境変数を扱うとき。
- schema source を runtime 用 schema store に複製する処理、output JSON の読み取り失敗時の扱い、Codex stdout/stderr から表示用 error text や resume token を抽出する処理を確認するとき。
- Codex CLI の capacity error や quota/usage/spend cap 系 error を文字列から分類する条件を確認・変更するとき。

## Do not read this when
- runtime path の概念定義や schema store の場所そのものを確認したいだけの場合は、path model や runtime paths を扱う対象を読む。
- FileAccessMode や AgentCallParameter の型定義、model class や reasoning effort の入力構造を確認したいだけの場合は、basic/acp 側を読む。
- Codex の model 名や reasoning_effort の設定値をどこから読むかだけを確認したい場合は、config 側を読む。
- hashed file の保存方法、ファイル名生成、既存ディレクトリへの書き込み仕様を確認したいだけの場合は、runtime content 側を読む。
- Codex CLI を起動する全体フローや command orchestration を追いたい場合は、この対象ではなく呼び出し側の runtime/runner 実装から読む。

## hash
- 296abc08aa97b9d9925d630c8548d44e1810ed04c4ba04ce077bae38160a70a9

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
- session と apply の永続状態を dataclass と JSON dict の相互変換で表し、session-id から状態ファイルの保存先を決める実装を扱う。
- cmoc 管理 branch 名から session-id を取り出し、現在 branch に対応する session state file を読み込む入口を提供する。
- 状態ファイルの書き込みと、home branch に対応する active session の探索を行う。

## Read this when
- session state file の schema、既定値、JSON 変換、読み書き処理を確認・変更したいとき。
- cmoc session branch または cmoc apply branch から session-id を特定する処理や、branch 名不正時のエラーを確認・変更したいとき。
- home branch に紐づく active session の重複確認や探索処理を追いたいとき。

## Do not read this when
- run-root、work-root、sessions directory などの path 定義そのものを確認したいだけのとき。
- CmocError の表示形式、例外クラスの構造、エラーメッセージ整形を確認したいとき。
- 個別 CLI command の引数解釈、git 操作、ユーザー向け出力の流れを追いたいとき。

## hash
- 13842c792e49e2acba1d662558682cc15ba6e450a37bda153abb5a32f7fe4bff
