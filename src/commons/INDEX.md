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
- Codex CLI を外部プロセスとして呼び出す実行時処理を担う実装。exec 呼び出しでは profile・Structured Output schema・ログ出力先を準備し、容量エラーの指数バックオフ、quota 枯渇時の代表プローブによる待機、Structured Output 検証リトライ、結果オブジェクト化までを扱う。
- 対話型呼び出しでは profile と call log を準備して CLI/TUI を起動し、終了コードに応じたイベント記録と cmoc エラー化を行う。Codex 呼び出しの実行制御、ログ記録、待機時間集計、失敗時メッセージの境界を確認する入口になる。

## Read this when
- Codex CLI の exec 呼び出し手順、引数構築、標準出力・標準エラー・最終出力・call log の保存先や記録内容を確認したいとき。
- Structured Output schema を指定した呼び出しで、schema 準備、出力 JSON 読み取り、jsonschema 検証、検証失敗時の semantic retry の挙動を調べるとき。
- Codex CLI の capacity error や quota error に対する retry・polling・resume token 利用・待機時間集計の制御を変更または検証するとき。
- Codex CLI 呼び出し結果から返される実行結果オブジェクト、または CLI/TUI 呼び出し失敗時に投げる cmoc エラーの内容を確認するとき。
- サブコマンドログへ記録される Codex 呼び出しイベント、quota wait 集計、コンソールに出す呼び出し概要の責務を追うとき。

## Do not read this when
- Codex profile の生成内容、Codex home の解決・検証、quota/capacity error の判定、resume token 抽出、出力 JSON 読み取りの詳細を確認したいだけのときは、それらを提供する下位 helper を直接読む。
- cmoc 設定ファイルの読み込み規則や設定値の構造を調べたいときは、設定読み込み・設定型定義を扱う対象を読む。
- repo root、work root、ログディレクトリ、timestamp、duration 表示などの path・時刻 helper の仕様を確認したいだけのときは、runtime path 系の対象を読む。
- Codex 呼び出しを使う各サブコマンド側の業務ロジック、prompt 作成、AgentCallParameter の構築条件を調べたいときは、呼び出し元のコマンド実装を読む。
- 一般的なコマンド結果型や Codex 実行結果型のフィールド定義だけを確認したいときは、結果型を定義する対象を読む。

## hash
- 6a391ab01e0f28e9c47f5918dd0be660951f467492bc952bbff75b902ac57a0a

# `runtime_codex_profile.py`

## Summary
- Codex CLI 呼び出しに使う設定プロファイル文字列の組み立て、権限プロファイルの生成、Codex home の解決・検証、生成物保存、サブプロセス環境、JSON 出力や JSONL エラーからの情報抽出をまとめて扱う実装。
- ファイルアクセスモードを Codex の sandbox / permission profile 表現へ変換し、実行 root・追加 read path・memo や oracle などの読み書き制約を TOML 断片として出力する入口になる。
- Codex 実行後の標準出力・標準エラーから、通常の JSON 出力、エラーメッセージ、resume token、capacity / quota 系失敗を判定する補助処理も同じ責務内に含む。

## Read this when
- AgentCallParameter と設定値から Codex CLI 用の profile を作る処理、sandbox_mode や permission profile の出力内容を確認・変更したいとき。
- FileAccessMode ごとの read / write / deny_read / read_only / writable_roots の対応関係を調べるとき。
- CODEX_HOME の解決、auth.json を含む Codex home 検証、Codex subprocess に渡す環境変数の扱いを確認したいとき。
- schema source を実行 root 側の schema store へハッシュ付きで保存する処理、または Codex の出力 JSON 読み取り処理を変更するとき。
- Codex JSONL 出力から error message、thread_id、capacity error、quota error を抽出する条件を調べるとき。

## Do not read this when
- FileAccessMode、AgentCallParameter、モデルクラス、reasoning effort などのデータ構造そのものを調べたいだけのとき。
- Codex model 名や reasoning effort の設定値をどこで定義するかを調べたいだけのとき。
- ハッシュ付きファイル保存や schema store のディレクトリ決定の実装詳細を調べたいとき。
- Codex CLI 以外の実行ランタイム、別エージェントのプロファイル、または一般的な path model の定義を調べたいとき。
- oracle file と realization file の概念定義や編集ルールを確認したいだけのとき。

## hash
- 9d6d54e0104886b39a93dc0605316f91f472203c7bebc930a6da4a5e53169b6e

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
- cmoc の session state file を表すデータ構造と、その JSON 読み書き、session-id 解決、管理 branch からの状態ロードを扱う実装。
- session 側と apply 側の状態値、home branch、開始 commit、oracle snapshot commit など、session/apply の永続状態を Python の dataclass と dict/JSON の間で変換する入口になる。
- 管理 branch 名から対応する session state file を特定し、存在しない状態ファイルや不正な branch 名を cmoc の実行時エラーとして扱う責務を持つ。

## Read this when
- session state file の schema、初期値、JSON への保存形式、または既存 JSON から dataclass へ復元する挙動を確認・変更したいとき。
- cmoc の session branch や apply branch から session-id を取り出す規則、または不正な branch 名に対するエラー条件を確認・変更したいとき。
- 現在の管理 branch に対応する session state file を読み込む処理、状態ファイルの保存処理、home branch に紐づく active session の探索処理を扱うとき。

## Do not read this when
- CLI コマンドの引数定義、表示文言、コマンド全体の制御フローだけを確認したいとき。
- sessions directory そのものの配置規則や root path の定義だけを確認したいとき。
- CmocError の表示形式やエラー出力処理そのものを変更したいとき。

## hash
- c348b133dcab2a30614395d8281cb2c70a9b5c16188bdc32eb21f55671e17ff4
