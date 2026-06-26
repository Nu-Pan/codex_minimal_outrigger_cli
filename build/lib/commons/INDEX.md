# `__init__.py`

## Summary
- cmoc の共有ランタイム補助機能を束ねる Python パッケージの入口であることを示すだけの初期化モジュール。現時点では公開 API、初期化処理、具体的な helper 定義は持たない。

## Read this when
- 共有ランタイム補助機能のパッケージ境界そのものに、初期化時の副作用や公開シンボルがあるかを確認したいとき。
- 共有 helper 群を import する際に、パッケージ入口で追加処理が行われるかを確認したいとき。

## Do not read this when
- 個別の共有 helper の実装、入出力、例外処理、責務分担を確認したいとき。この対象には具体的な helper 定義は含まれていない。
- CLI 挙動、永続状態、パスモデル、テスト方針など、共有ランタイム補助機能のパッケージ境界以外を調べたいとき。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- Codex 実行、プロファイル、設定、コンテンツ、CLI、エラー、Git、ログ、パス、結果、状態管理など、実行時に使う commons 群の公開名をまとめて取り込む集約モジュール。
- 個別の実装責務は各 runtime_* モジュール側にあり、この対象自体はそれらを一箇所から参照できる入口として位置づけられる。

## Read this when
- runtime_* モジュールに分かれた共通機能を、利用側がどの集約入口から import しているか確認したいとき。
- Codex 実行、Git 操作、設定、状態、パス、ログ、エラー処理など複数の commons 実行時機能を横断して公開名の一覧を確認したいとき。
- commons 配下の runtime 系モジュールを分割・移動・改名した結果、この集約入口の import 群を更新する必要があるとき。

## Do not read this when
- 個々の関数・クラスの挙動、入出力、副作用、例外条件を確認したいときは、それを定義している各 runtime_* モジュールを直接読む。
- Codex preflight、profile、config、content、CLI、Git、logging、paths、state など特定領域だけを変更する場合は、該当する実体モジュールを直接読む。
- ビルド成果物ではなく正本の実装を変更したいときは、対応する src 側の commons 実装を確認する。

## hash
- 47965e9d088c7a23b67c3e3a667e6c40549df203e7d5e544a2fd4b02e2a3715e

# `runtime_cli.py`

## Summary
- CLI サブコマンド実装を共通の実行ライフサイクルで包むための実装。work root 実行前提の検査、事前検査、サブコマンド logger の設定、開始・実行・完了の標準 stdout、戻り値から終了コードへの変換、例外時のエラー表示と終了コード化を一箇所で扱う。
- runtime state を通常は repo root、初期化対象を扱う場合だけ work root に置く分岐と、サブコマンドログを常に repo root に置く方針を持つ。
- サブコマンド完了時の elapsed、quota_wait、returncode などの標準サマリー出力と、現在ディレクトリが work root であることを検査する補助処理も含む。

## Read this when
- CLI サブコマンドの共通 wrapper、実行開始から完了までの標準表示、終了コード処理、例外処理を変更する。
- サブコマンド単位の logger 設定、command_invoked・step_started・command_finished の記録、現在 logger の設定解除に関わる挙動を確認する。
- runtime state とサブコマンドログをどの root に置くか、または初期化系コマンドだけ work root runtime を使う挙動を確認する。
- cmoc を work root 以外で実行した場合のエラー化や、そのエラーメッセージの生成元を確認する。
- サブコマンド完了時に stdout へ出る標準サマリー項目や経過時間表示を変更する。

## Do not read this when
- 個別サブコマンドの業務ロジック、入力検証、永続状態の内容そのものを調べたい場合。
- logger の内部実装、ログファイル形式、quota_wait の加算方法を調べたい場合。
- repo root・work root の探索方法、timestamp や duration の具体的な整形処理を調べたい場合。
- CmocError の表現形式や render_error の詳細を調べたい場合。
- Typer のコマンド定義や CLI option の宣言場所を探している場合。

## hash
- ad800ae98a54ec51782f366d2b447f6dbc7e398b9c60bee0df9a6cd98a32ad89

# `runtime_codex.py`

## Summary
- Codex 実行系の公開入口をまとめ、非対話実行用と TUI 実行用のランタイム関数を同じ import 元から参照できるようにする薄い再エクスポートモジュール。

## Read this when
- Codex ランタイムの呼び出し側で、非対話実行と TUI 実行の公開 API がどこから import されるかを確認したいとき。
- ランタイム実行関数の公開名を増減させる変更や、呼び出し元の import 経路を整理する変更を行うとき。

## Do not read this when
- 非対話実行の具体的な処理内容、引数組み立て、外部コマンド実行の詳細を確認したいときは、非対話実行側の実装を直接読む。
- TUI 実行の具体的な処理内容、端末起動、入出力制御の詳細を確認したいときは、TUI 実行側の実装を直接読む。
- Codex 以外のランタイムや CLI 全体のルーティングを確認したいだけのとき。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex exec の 1 回の呼び出し試行から、capacity retry、quota 待機と代表 probe、resume 継続、Structured Output 検証、call log と subcommand event 記録までを一体で制御する実行ループを扱う。
- Codex profile・schema・log path・subprocess argv の準備、stdout/stderr/output/call log の保存、成功時の実行結果組み立て、失敗時の CmocError 生成を担う。
- REALIZATION_WRITE で oracle 配下の書き込み許可がある場合、許可対象外の oracle 変更を検出して拒否する guard も含む。

## Read this when
- Codex CLI を subprocess で実行する制御、再試行、resume token、quota 枯渇時の待機・probe、capacity error の指数 backoff を調べるとき。
- Structured Output schema を渡した Codex exec の出力検証、検証失敗時の semantic retry、output JSON 読み取りの流れを確認するとき。
- Codex 呼び出しごとの stdout/stderr/output/call log、console 表示、subcommand log event、quota wait 計測の記録内容や生成タイミングを確認するとき。
- REALIZATION_WRITE 中に oracle 変更をどう監視し、許可対象外の oracle path 変更をどう検出するかを確認するとき。

## Do not read this when
- Codex profile 名、Codex home、schema file、resume token、quota/capacity error 判定などの個別 helper の実装だけを確認したい場合は、それらを定義する profile 関連 module を直接読む。
- TUI 起動や対話 UI の実行制御を調べる場合は対象外であり、exec の非対話 subprocess 制御を扱う module へ進む必要がある。
- cmoc の設定値そのものの読み込み規則、path model の定義、結果 dataclass の構造だけを確認したい場合は、それぞれの専用 module を読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は対象外であり、この対象は呼び出し制御と検証・記録の制御ロジックだけを扱う。

## hash
- 0f36f7d17bdfaf05c4986758ec8bc10088d623f3c60475a4d367b390966d2ade

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しが完了した時に、目的、呼び出しログの場所、経過時間、終了コードを利用者向け console にまとめて出力する小さな runtime logging helper を定義している。
- 時刻表示と経過時間整形は runtime path 系 helper に委ね、この対象は完了サマリーの見出し・項目構成と標準出力への即時 flush に責務を限定している。

## Read this when
- Codex CLI 呼び出し単位の完了サマリーを console に出す処理を確認・変更したいとき。
- 利用者に表示される Codex call の目的、call log、elapsed、returncode の表示形式や並びを確認したいとき。
- Codex 呼び出し後の runtime logging がどこで console 出力を組み立てているかを追いたいとき。

## Do not read this when
- 時刻文字列の生成規則や経過時間の整形ロジックを確認したいだけのときは、それらを提供する runtime path 系 helper を読む。
- Codex CLI 呼び出しの実行、プロセス起動、ログファイル作成、戻り値判定そのものを調べたいときは、呼び出し制御や runtime 実行側の実装を読む。
- 永続ログの内容、保存先、ローテーションなど console 表示以外のログ管理を調べたいときは、この対象ではなくログ保存側の実装を読む。

## hash
- 65cfde582382659dd394662fe73f4e8796945c7ad06a7f2d2240181e63abaab8

# `runtime_codex_preflight.py`

## Summary
- Codex 実行/TUI 呼び出しの直前に、設定済みの indexing preflight を一度だけ走らせるためのラッパー実装。実際の Codex 実行処理へ委譲する前に、目的文字列と実行ルートから indexing 対象を決め、再入防止と排他制御をかける。
- indexing preflight の登録・無効化、Codex exec/TUI の事前処理付き呼び出し、cwd/root からの indexing root 解決、特定 purpose での preflight スキップ判定を扱う。

## Read this when
- Codex exec または TUI 起動前に indexing を自動実行する制御を確認・変更したいとき。
- indexing preflight が再帰的に Codex を呼ぶ場合の再入防止、ロック、ContextVar による active 状態管理を調べるとき。
- Codex 呼び出し時の cwd/root から、どのルートを indexing 対象にするかを確認・変更したいとき。
- purpose によって indexing preflight をスキップする条件を確認・変更したいとき。

## Do not read this when
- 実際の Codex CLI コマンド実行、TUI 起動、プロセス実行結果の組み立てを調べたいだけのときは、委譲先の runtime 実装を読む。
- repo root や work root のパスモデルそのものを確認したいときは、パス解決を担う実装を読む。
- Codex 実行結果やコマンド結果のデータ構造だけを確認したいときは、結果型を定義する実装を読む。
- indexing の本文生成・差分反映・INDEX 更新ロジックを調べたいときは、この事前フックではなく indexing 本体を読む。

## hash
- 3878cafea4f3209a564a38a3ebe0f67ca85915e34f09112258511701c00f4c48

# `runtime_codex_profile.py`

## Summary
- Codex CLI を呼び出すための実行時プロファイルと周辺入出力を組み立てる実装。AgentCallParameter と設定からモデル・reasoning effort・sandbox/permission profile を TOML 文字列として生成し、Codex home の解決と検証、hashed profile/schema の保存、サブプロセス環境、Codex JSONL 出力からのエラー・resume token・quota/capacity 判定を扱う。

## Read this when
- FileAccessMode ごとの Codex sandbox_mode、permission profile、read/write/deny_read/read_only/writable_roots の対応を確認または変更したいとき。
- Codex profile の生成、保存先、profile 名の導出、CODEX_HOME の解決・検証、Codex サブプロセスへ渡す環境変数を調べるとき。
- Codex 実行結果の JSONL/stdout/stderr からエラー文、resume token、capacity error、quota error を抽出する処理を確認または変更したいとき。
- schema source を schema store へ hashed file として保存する処理や、出力 JSON ファイルを読み取る処理を確認したいとき。

## Do not read this when
- Codex profile の内容ではなく、AgentCallParameter や FileAccessMode 自体のデータ定義を確認したいだけのとき。
- CmocConfig の設定ファイル構造や model/reasoning_effort の定義元を確認したいだけのとき。
- hashed file の保存方式、schema store のパス規則、CmocError の構造そのものを調べたいとき。
- Codex CLI 起動コマンド全体の制御フローや、生成済み profile をどのタイミングで使うかを追いたいとき。

## hash
- fab6b85ee96c7a66017972b494731a4c6f9b3c265ee116c790ffe0191c31c808

# `runtime_codex_tui.py`

## Summary
- Codex TUI を起動する実行時処理を担う。AgentCallParameter と設定から Codex profile を準備し、call log を保存し、Codex CLI を対話モード相当で subprocess 実行して、コンソール表示・サブコマンド logger へのイベント記録・失敗時の CmocError 変換までをまとめる入口である。

## Read this when
- Codex TUI 呼び出し時に、profile 作成、codex home 検証、作業ルート、追加 read path、環境変数がどのように渡されるかを確認したいとき。
- Codex CLI/TUI 呼び出しの call log に保存される項目、保存先、目的名、モデル種別、推論努力、ファイルアクセスモードの記録内容を確認したいとき。
- Codex TUI subprocess の cwd、argv、戻り値、経過時間計測、成功・失敗ログ、失敗時例外の扱いを変更または調査したいとき。

## Do not read this when
- Codex profile の具体的な生成内容、profile 名の決め方、codex home の解決・検証、subprocess 用環境変数の詳細だけを確認したい場合は、それらを定義する profile 関連の実装を直接読む。
- 設定ファイルの読み込み規則、runtime path の定義、logger や console 出力の内部形式、CommandResult や CmocError の構造だけを調べたい場合は、それぞれの責務を持つ実装を直接読む。
- Codex CLI を非対話実行する別経路、複数 agent 実行、または TUI 起動以外のサブコマンド挙動を調べたい場合は、この対象ではなく該当する呼び出し経路を読む。

## hash
- 3ed236afcdeaea95975325e2dab8c6d80a050e4201c18805ba9d8dbf3f875a99

# `runtime_config.py`

## Summary
- cmoc の設定オブジェクトを JSON 互換の辞書へ変換し、設定ファイルから読み込み、存在しない場合は既定値で同期する実行時設定の入出力を扱う。
- 設定の top-level、codex、apply_fork、review_oracle の各セクションを既定値で補完しながら型付き設定へ復元し、不正な JSON・非 object・不正値を利用者向けエラーに変換する。

## Read this when
- cmoc の設定ファイルを読み込む処理、初期生成・同期処理、または設定オブジェクトと JSON 表現の対応を確認・変更したいとき。
- 設定項目の既定値補完、model class や reasoning effort の文字列表現、並列数や review oracle ループ回数の永続化形式に関わる挙動を追うとき。
- 設定ファイルが存在しない、JSON として読めない、top-level が object でない、または値変換に失敗する場合のエラー文言と復旧案を確認するとき。

## Do not read this when
- 設定データクラスそのもののフィールド定義や既定値を確認したいだけなら、設定型を定義している対象を読む。
- 設定ファイルの配置パスやリポジトリ内パスモデルだけを確認したいなら、実行時パス解決を扱う対象を読む。
- CLI サブコマンドの引数解析、コマンド実行フロー、または設定値を使う各機能の挙動を確認したい場合は、それぞれの呼び出し側を読む。

## hash
- aef509c7c07682149b5db71e9bfcdce5c7fcab10722f26d36d70d3ad0e3ad2f7

# `runtime_content.py`

## Summary
- 実行時に扱う内容の同一性判定と保存を支える小さな共通 helper 群。ファイル内容または文字列から SHA-256 digest を計算し、その digest を名前に含むテキストファイルを書き出す処理と、ファイル先頭の NUL byte による binary 判定を扱う。
- 内容ベースのファイル名生成、同一内容なら再書き込みを避ける保存処理、読み取り不能なファイルを binary 扱いする判定が必要な箇所への入口となる。

## Read this when
- 文字列やファイル内容から SHA-256 digest を計算する共通処理を確認・変更したいとき。
- content-addressed な一時ファイル・生成ファイルの書き出し方、親ディレクトリ作成の有無、既存ファイルとの内容比較による書き込み抑制を確認したいとき。
- ファイルが binary かどうかを判定する基準や、読み取り時に OSError が起きた場合の扱いを確認したいとき。

## Do not read this when
- CLI の引数、コマンド構造、利用者向け出力 schema を調べたいとき。
- path model の定義や、<cmoc-root> などのパス語彙の意味を調べたいとき。
- 生成物全体の配置方針、oracle file と realization file の責務境界、INDEX.md 生成規則そのものを調べたいとき。
- 特定のサブコマンドや上位ワークフローが、どの内容をいつ保存するかという業務ロジックを調べたいとき。

## hash
- 7116a86511c8ee8fe0abca1e4b8778ee6e54c94c0ac049c0193c7173040e2524

# `runtime_errors.py`

## Summary
- cmoc 共通の実行時エラー表現と表示整形を担う実装。利用者向けのエラー見出し、要約、次の行動、詳細、呼び出しスタックを 1 つのテキストに組み立てる責務を持つ。
- 独自例外では要約・次の行動・詳細を保持し、それ以外の例外では例外文字列と既定の次の行動からエラー表示を生成する。次の行動が不足する場合に既定文で補う小さな補助処理も含む。

## Read this when
- cmoc の例外を利用者向けエラーテキストへ変換する挙動を確認または変更したいとき。
- 独自例外に持たせる要約、次の行動、詳細の扱いを確認したいとき。
- エラー表示に含まれる Summary、Next actions、Detail、Call stack の構成や順序を確認したいとき。
- 次の行動が空または少ない場合に既定文がどう補われるかを確認したいとき。

## Do not read this when
- 特定サブコマンドがどの条件で失敗するかを調べたいだけのとき。失敗条件を定義している呼び出し元の実装を先に読む。
- 作業ツリー、設定、パス、外部コマンドなど個別領域の検証ロジックを調べたいとき。各領域の実装を直接読む。
- エラー表示を受け取った後の CLI 終了コード、標準出力、標準エラーへの出し分けを調べたいとき。上位の CLI 実行制御を読む。

## hash
- f5ef88c7fd0b75421e70d11bae48427f49c53acc612809b234a7aa9a7f073a8b

# `runtime_git.py`

## Summary
- git コマンド実行と git 状態操作の共通処理を集約する実行時 helper。コマンド結果を共通の結果型に包み、失敗時は共通エラーへ変換し、branch・HEAD・worktree・追跡除外状態などを扱う。
- .cmoc を git 追跡対象外に保つ初期化確認や、管理対象 branch 判定、run 用 worktree の作成・削除、branch 削除など、複数の上位処理から使われる git 境界処理の入口になる。

## Read this when
- git コマンド呼び出しの失敗時メッセージ、戻り値、check の扱いを確認または変更したいとき。
- 現在 branch、HEAD commit、clean worktree 判定、branch 存在確認、管理対象 branch prefix の扱いを確認または変更したいとき。
- run 用 worktree の作成・削除、branch 削除、worktree prune の挙動を確認または変更したいとき。
- .cmoc が gitignore 対象か、git index に残っていないかを確認・初期化・必須条件化する処理を確認または変更したいとき。
- 任意の path が git ignore 対象かを判定する共通処理を確認または変更したいとき。

## Do not read this when
- CLI 引数解析、サブコマンドの入出力、利用者向け表示の構成だけを確認したいとき。
- git 以外の外部コマンド実行、プロセス管理、ファイル探索、path model の仕様だけを確認したいとき。
- oracle file と realization file の概念、ルートパス表記、INDEX.md 生成方針など、正本仕様側の文書を確認したいとき。
- テストケースや fixture の期待値だけを確認したいとき。
- build 成果物ではなく実装正本側の同等処理を変更する必要があるときは、対応する実装配置を直接確認する。

## hash
- 0a6dd3fc4a430ad1017e13f7297d632b7f3fcc98fa1e7c75d3738ce06deb4522

# `runtime_logging.py`

## Summary
- サブコマンド実行中のランタイムログを JSON Lines として保存するための小さな実装。ログファイルの作成先を実行ルート配下のログ領域に決め、イベント種別・コマンド名・時刻・任意 payload を 1 行ずつ追記する。
- 現在のサブコマンド用 logger を contextvars で保持・取得・リセットする入口も持ち、サブコマンド処理の別レイヤーから同じ logger にアクセスするための共有状態を扱う。
- 実行開始からの経過秒数と quota 待機時間の累積を logger インスタンス内で管理する。

## Read this when
- サブコマンド単位の実行ログ、イベントログ、JSONL 追記、ログ保存先の生成を確認または変更したいとき。
- 現在実行中のサブコマンド logger をコンテキスト経由で共有する仕組みを確認したいとき。
- 実行時間や quota 待機時間をログやサブコマンド制御で扱う箇所の責務を追いたいとき。

## Do not read this when
- ログ保存先ディレクトリやタイムスタンプ文字列そのものの定義だけを確認したいときは、runtime path 系の実装を読む方が直接的。
- 個別サブコマンドの処理内容、CLI 引数、ユーザー向け出力を確認したいだけのとき。
- 構造化ログを読む側、集計する側、またはテスト fixture の期待値だけを確認したいとき。

## hash
- e2e4d1e5000c03dde22b8c79c07e036859d091813787c5b6d8a7efb15fe08d44

# `runtime_paths.py`

## Summary
- 実行時に必要なルートパス、cmoc 管理ディレクトリ、時刻文字列、作業ディレクトリ一時変更を扱う共通 helper 群。
- リポジトリルートや worktree ルートの解決失敗を cmoc 用エラーへ変換し、セッション・レポート・ログ・状態・設定などの保存先パスを組み立てる入口になる。

## Read this when
- コマンド実行時の <repo-root>、<work-root>、<cmoc-root> の解決方法や、解決失敗時の CmocError の内容を確認・変更したいとき。
- `.cmoc` 配下に作られる sessions、reports、log、worktrees、state、config などの実行時パスの組み立てを確認・変更したいとき。
- run ID やコンソール表示に使う時刻形式、経過時間表示、処理中だけカレントディレクトリを切り替える挙動を確認・変更したいとき。

## Do not read this when
- 個別サブコマンドの処理内容、CLI 引数、出力 schema、永続状態の中身を調べたいだけのとき。
- パスモデルそのものの定義や、ルート解決アルゴリズムの詳細を調べたいとき。
- cmoc 用エラー型の構造や表示仕様を調べたいとき。

## hash
- ba602d99cbeee08c3659843f561c7cd76d53a274fcf996e15f9945ef32ede11f

# `runtime_results.py`

## Summary
- 外部コマンド実行結果と Codex 実行結果を受け渡すための不変データ構造を定義する実装ファイル。戻り値、標準出力・標準エラー、生成ログや出力ファイルのパス、実行プロファイル、スキーマ、経過時間、quota 待機情報をひとまとまりの結果オブジェクトとして扱う入口になる。

## Read this when
- コマンド実行や Codex 呼び出しの結果を表すオブジェクトのフィールドを確認・変更したいとき。
- 実行結果からログファイル、出力ファイル、Codex home、プロファイル、スキーマ、経過時間、quota 待機情報へアクセスするコードを書くとき。
- 戻り値と標準出力・標準エラーだけを持つ汎用コマンド結果と、Codex 固有の実行結果を区別して扱う必要があるとき。

## Do not read this when
- 実際に外部コマンドや Codex を起動する処理、ログを書き出す処理、出力 JSON を解析する処理を探しているとき。
- 結果オブジェクトの保存先ディレクトリ作成、プロファイル生成、quota 待機の制御ロジックを変更したいとき。
- テストや仕様文書から期待される実行結果の意味を確認したいだけで、データ構造のフィールド確認が不要なとき。

## hash
- bc07588fcd418f58345aaaf5fa48ed9b3883bbf1e0d628d07ed74c959c60c719

# `runtime_state.py`

## Summary
- session ごとの永続 state を dataclass と JSON 変換で扱い、session 部分と apply 部分の既定値・復元・書き戻しをまとめる。
- cmoc 管理 branch 名から session-id を取り出し、現在 branch に対応する session state file を読み込む入口を提供する。
- home branch に紐づく active session state file を探索するなど、session/apply の進行状態と保存先を扱う共通 runtime helper として位置づく。

## Read this when
- session state file の JSON 構造、既定値、未知 field の扱い、読み書き形式を確認したいとき。
- cmoc/session または cmoc/apply branch 名から session-id を解決する処理や、その失敗時エラーを変更・調査するとき。
- 現在 branch に対応する session state file の読み込み、保存先 path、active session の探索ロジックを追うとき。
- session と apply の状態遷移に関わる実装で、永続 state に保存される field 名や更新対象を確認したいとき。

## Do not read this when
- 個々の CLI command の引数解析、表示文言、コマンド実行順だけを確認したいとき。
- git branch の作成・切替・削除など、実際の git 操作 helper の詳細を調べたいとき。
- runtime path の基準ディレクトリ定義や sessions directory の組み立て規則そのものを確認したいとき。
- oracle snapshot の内容生成や差分適用の実装詳細を調べたいとき。

## hash
- 6210da600bbbe647a5df4d5a14ac143209c4ebd6dfbc83a1ef6b359ba006b31c
