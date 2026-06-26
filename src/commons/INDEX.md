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
- Codex 実行、profile、設定、content hashing、CLI 補助、error、git、logging、path、result、state など、runtime 系の共通 API をまとめて再公開する入口である。
- この対象自体は処理ロジックを持たず、複数の runtime 領域から import した関数・型・定数を一か所から参照できるようにする集約層として位置づけられる。

## Read this when
- runtime 系 helper を利用する呼び出し側で、どの共通 API が集約入口から import 可能かを確認したいとき。
- 複数の runtime 領域をまたぐ利用箇所で、直接の依存先を増やす代わりに集約入口を使うべきか判断したいとき。
- runtime 共通 API の再公開範囲を追加・削除・整理する変更を行うとき。

## Do not read this when
- Codex 実行、profile 準備、設定読み書き、hash 書き込み、git 操作、logging、path 解決、state 永続化など、個別処理の実装詳細や失敗時挙動を確認したいときは、それぞれの責務を持つ実装本文を直接読む。
- 特定の関数・型・定数の仕様、引数、副作用、保存先、外部コマンド呼び出し内容を調べたいだけのとき。
- 集約入口を経由しない個別 runtime module 内の内部整理やテスト変更だけを行うとき。

## hash
- 47965e9d088c7a23b67c3e3a667e6c40549df203e7d5e544a2fd4b02e2a3715e

# `runtime_cli.py`

## Summary
- CLI サブコマンド実行時の共通ライフサイクルを扱う実装。work root で実行されていることの検査、runtime/log root の選択、サブコマンド単位の logger 設定、開始・実行・完了サマリー出力、戻り値の終了コード化、例外時のエラー表示と終了コード化をまとめて担う。
- サブコマンド完了時の標準 stdout サマリー出力と、現在ディレクトリが work root であることを要求する実行前提の検査もこの対象に含まれる。

## Read this when
- CLI サブコマンドに共通する開始表示、完了表示、終了コード処理、例外処理、サブコマンドログ記録の挙動を確認または変更したいとき。
- サブコマンド実行時に repo root と work root のどちらを runtime state の配置先として使うか、またサブコマンドログをどこへ置くかを確認したいとき。
- cmoc が work root 以外で実行された場合の検査条件や利用者向けエラー内容を確認または変更したいとき。
- サブコマンド実装関数の戻り値を CLI の終了コードへ変換する扱いや、非ゼロ終了時の Typer 終了処理を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、入出力内容を調べたいだけのときは、そのサブコマンド本体を直接読む。
- エラー型やエラーメッセージ描画の詳細を変更したいときは、エラー処理の定義側を読む。
- サブコマンドログのイベント保存形式、現在 logger の管理方法、ログファイル構造を変更したいときは、ログ処理の定義側を読む。
- repo root、work root、時刻表示、経過時間表示の算出方法を変更したいときは、runtime path や表示整形の定義側を読む。

## hash
- ad800ae98a54ec51782f366d2b447f6dbc7e398b9c60bee0df9a6cd98a32ad89

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
- Codex CLI の exec 呼び出しを 1 回の状態機械として制御する実行中核。profile/schema 準備、subprocess 起動、call log・stdout/stderr/output 記録、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume token による再開、subcommand event への記録をまとめて扱う。
- TUI 起動や profile 解析そのものではなく、exec 分岐における再試行・検証・ログ出力・結果オブジェクト生成の接続点を読む入口となる。

## Read this when
- Codex CLI を非対話 exec として呼び出す制御フロー、引数構築、stdin prompt、cwd/env、profile/schema の渡し方を確認・変更したいとき。
- Structured Output の schema 検証失敗時の semantic retry、capacity error 時の指数 backoff、quota error 時の polling/probe/resume の挙動を調べるとき。
- Codex call の call log、stdout/stderr/output 保存先、console 表示、subcommand log event、quota wait 集計がどのタイミングで記録されるかを追うとき。
- CodexExecResult に入る実行結果、各 log path、profile/schema 情報、経過時間、quota 待機時間・poll 回数の生成元を確認するとき。

## Do not read this when
- Codex profile 名、CODEx home、schema ファイル準備、resume token 抽出、quota/capacity error 判定などの個別 helper の詳細だけを調べたいときは、それらを定義する runtime profile 側を直接読む。
- TUI 起動、対話 UI、または exec 以外の Codex 呼び出し経路を調べたいとき。
- 実行結果データ構造そのものの型定義や、subcommand logger の実装詳細を確認したいだけのときは、それぞれの結果型・logging 側を読む。
- repository root、work root、log directory、timestamp などの path 解決規則を調べたいだけのときは、runtime paths 側を読む。

## hash
- 05bb62ba5ade89f1bcfa5592678c4da07925ad5cf6b303f175e2ad8bc97aed22

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
- Codex CLI を cmoc から起動するための実行時プロファイル、権限設定、CODEX_HOME、補助入出力を扱う実装。
- AgentCallParameter と設定から model・reasoning_effort・sandbox/permission profile を TOML 文字列として組み立て、必要に応じて Codex home 配下へハッシュ付き設定ファイルとして配置する。
- Codex home の解決・検証、サブプロセス用環境変数、schema JSON の保存、Codex 実行結果 JSON/JSONL からの出力・エラー・resume token・capacity/quota 判定の入口になる。

## Read this when
- FileAccessMode ごとの Codex sandbox_mode、read/write/deny_read/read_only、writable_roots の対応を確認または変更したいとき。
- cmoc が Codex CLI 用の設定ファイルをどの内容で生成し、どこへ保存するかを追いたいとき。
- CODEX_HOME の環境変数解決、存在確認、auth.json 必須条件、Codex サブプロセスへ渡す環境を扱う変更をするとき。
- Codex 実行に渡す schema ファイルの準備、出力 JSON の読み取り、stdout/stderr からのエラーテキスト抽出、thread_id の抽出、capacity/quota エラー判定を調べるとき。

## Do not read this when
- Codex CLI 呼び出し全体のプロセス制御、コマンドライン引数、作業ディレクトリ、リトライなど、プロファイル生成後の実行 orchestration を調べたいだけのとき。
- cmoc の設定ファイルそのものの schema、model_class や reasoning_effort の定義、設定値の読み込み規則を調べたいとき。
- FileAccessMode や AgentCallParameter のデータモデル定義を確認したいとき。
- パスモデル全般、run/work/root/oracle などの概念定義、または runtime ディレクトリや schema store の場所だけを確認したいとき。
- Codex が生成した本文の品質や LLM 応答内容そのものを評価・解析したいとき。

## hash
- b810d07a9cfa54d653563506bbea37d97de8ad10928b4599a9ad00865c3de3d6

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
- session branch と apply branch に紐づく永続 state のデータ構造、JSON 復元・保存、branch 名からの session_id 抽出、現在 branch に対応する state file の読み込みを扱う。
- home branch に紐づく active session state file を探索する入口も持ち、session state file の保存先と内容を扱う共通処理の集約点になっている。

## Read this when
- session state file の schema、既定値、未知 field の扱い、JSON への保存形式を確認したいとき。
- cmoc 管理 branch 名から session_id を取り出す処理、または session branch と apply branch の branch 名検証を変更・確認したいとき。
- 現在 branch に対応する session state file を読み込む処理や、state file が存在しない場合のエラーを確認したいとき。
- home branch に対して active な session が既に存在するかを判定する処理を調べたいとき。

## Do not read this when
- 実際の git branch 作成・切替・commit 操作そのものを調べたいとき。
- session state file の配置先を決める path model や sessions directory の定義だけを確認したいとき。
- CLI 引数定義、コマンド dispatch、利用者向け出力の組み立てを調べたいとき。
- CmocError の表示形式やエラー出力共通処理そのものを変更したいとき。

## hash
- 6210da600bbbe647a5df4d5a14ac143209c4ebd6dfbc83a1ef6b359ba006b31c
