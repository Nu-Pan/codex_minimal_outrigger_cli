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
- cmoc の実行時共通 API をまとめて公開する集約モジュール。Codex 実行、プロファイル、設定、ファイル内容、CLI、エラー、Git、ログ、パス、結果、状態管理に関する下位 runtime モジュールの主要な関数・クラス・定数を、利用側が一か所から import できる入口として扱う。

## Read this when
- cmoc の実装から共通 runtime 機能をどの名前で import できるか確認したいとき。
- 複数の runtime_* モジュールに分かれている実行時 helper の公開入口を確認したいとき。
- 新しい共通 runtime 機能を既存の集約 import 面へ加える必要があるか判断するとき。

## Do not read this when
- 個々の関数・クラス・定数の挙動、引数、副作用、エラー処理を調べたいとき。その場合は対応する下位 runtime モジュールを直接読む。
- Codex 実行、Git 操作、設定、状態、パス処理など特定領域の実装を変更したいとき。その場合はこの集約入口ではなく、責務を持つ下位実装を読む。
- cmoc の正本仕様断片を確認したいとき。このファイルは realization implementation の import 集約であり、仕様本文ではない。

## hash
- e5d4066344eb6e9174bca7f06b7aba9734d0ef516610c1300c7544a7e89a6c44

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
- Codex CLI の exec 呼び出しを 1 回の状態機械として制御する実行基盤。profile/schema 準備、`codex exec` argv 構築、prompt/stdout/stderr/output/call log の保存、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume token による継続、subcommand event への記録をまとめて扱う。
- TUI 起動ではなく exec 分岐の実行制御に責務を限定しており、quota 処理も resume token と log/event の文脈を共有するため同じ流れの中で読む対象として位置づけられている。

## Read this when
- Codex CLI を subprocess として呼び出す実行ループ、retry、resume、Structured Output 検証、quota 待機の挙動を確認・変更したいとき。
- Codex 呼び出しごとの prompt/stdout/stderr/output/call log の生成内容、命名順序、保存先、subcommand event payload、console 表示の関係を追いたいとき。
- capacity error と quota error の扱い、代表 probe による quota 回復確認、同一プロセス内での quota polling 共有、待機時間・poll 回数の集計を調べたいとき。
- Codex 実行結果として返す値と、profile、schema、log path、経過時間、quota wait 情報がどこで組み立てられるかを確認したいとき。

## Do not read this when
- Codex profile の具体的な作成、Codex home の解決・検証、error 判定、resume token 抽出、output JSON 読み取りなどの個別 helper の詳細だけを調べたいときは、それらを定義する profile/runtime helper 側を読む。
- TUI 起動や exec 以外の Codex 実行形態を調べたいときは、この対象ではなく起動形態ごとの実行制御を読む。
- subcommand log の基盤、path model、設定読み込み、実行結果 dataclass の定義そのものを確認したいだけなら、それぞれの共通 module を読む。
- CLI 利用者向けの公開仕様や oracle file の正本仕様断片を確認したいときは、この realization implementation ではなく該当する oracle doc/source を読む。

## hash
- 22c246354d733f9d51dc5d8d941cc56f8c8c99d8f8bdafa2d8ca284219906125

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
- Codex CLI 呼び出し用の実行時 profile を組み立て、Codex home の解決・検証、profile/schema のハッシュ保存、サブプロセス環境、Codex JSONL 出力からの結果・エラー・resume token 判定を扱う共通実装。
- AgentCallParameter と CmocConfig から model、reasoning_effort、sandbox/permission profile を TOML 文字列として生成し、FileAccessMode ごとの read/write/deny/read_only 境界を Codex の設定形式へ変換する入口になる。
- Codex CLI 実行後の標準出力・標準エラーを解析し、エラーテキスト抽出、capacity/quota 判定、空または壊れた JSON 出力の扱いを確認するための入口になる。

## Read this when
- Codex CLI に渡す profile 内容、sandbox_mode、permission_profile、writable_roots、read_only_paths、deny_read の生成規則を確認・変更したいとき。
- FileAccessMode と Codex 側の読み書き権限の対応、追加 read/write path による read_only 範囲の絞り込み、memo や .agents や oracle の保護扱いを調べたいとき。
- CODEX_HOME の解決、存在検証、auth.json 検証、Codex サブプロセスへ渡す環境変数の扱いを確認したいとき。
- Codex profile や JSON schema をハッシュ付きファイルとして保存する流れ、または保存失敗時の CmocError を確認したいとき。
- Codex CLI の JSONL 出力から resume token、利用制限エラー、capacity エラー、利用者向けエラー文面を取り出す処理を変更・調査したいとき。

## Do not read this when
- cmoc 全体のパス語彙や <cmoc-root>、<work-root> などの定義だけを確認したいときは、パスモデルを扱う仕様・実装を読む方が直接的。
- AgentCallParameter、FileAccessMode、CmocConfig のデータ構造や設定値の定義そのものを確認したいときは、それぞれの定義元を読む方が直接的。
- ハッシュ付きファイル保存の具体的な命名・書き込み実装や schema store directory の配置規則だけを確認したいときは、コンテンツ保存や実行時パスを扱う共通実装を読む方が直接的。
- Codex CLI を実際に起動するコマンド組み立て、プロセス実行、入出力ファイルのライフサイクル全体を追いたいときは、この対象だけでなく呼び出し側の実行制御を読む必要がある。

## hash
- fe6f07cf0d561bb501d32d8a726672004cf4ba1f0e635c5744fd03abafaa60e2

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
- Git コマンド実行を共通化し、失敗時の cmoc 向けエラー化、現在 branch・HEAD commit・worktree cleanliness の確認、branch 存在確認、run 用 worktree の作成・削除、branch 削除を扱う実装。
- .cmoc を Git 追跡対象外に保つための .gitignore 更新、index からの除外、ignore 状態の検証、および任意 path が Git ignore 対象かどうかの判定も担う。

## Read this when
- Git コマンド呼び出しの失敗処理、stdout/stderr/returncode の扱い、または CmocError への変換を確認・変更したいとき。
- cmoc が管理する branch prefix、現在 branch の取得、detached HEAD の拒否、HEAD commit 取得、未コミット差分の拒否に関わる挙動を確認・変更したいとき。
- run 用 worktree の作成・強制削除・prune、または branch の存在確認・削除に関わる処理を追うとき。
- .cmoc を .gitignore に追加する処理、Git index から除外する処理、追跡対象外として初期化済みか要求する処理を確認・変更したいとき。
- 特定 path が Git ignore 対象かどうかを、リポジトリ root 基準の相対 path として判定する処理を確認・変更したいとき。

## Do not read this when
- Git 以外の外部コマンド実行、プロセス起動全般、または CLI 出力整形だけを調べたいとき。
- cmoc の path keyword や root 種別の定義を調べたいとき。
- run の高レベルな状態管理、セッション記録、プロンプト生成、またはサブコマンドのユーザー向け制御フローだけを調べたいとき。
- Git ignore の個別判定ではなく、INDEX.md や oracle/realization の分類規則を調べたいとき。

## hash
- dcc541d48e81f8c1b468b3a21221d90007082bbe88e14bdf008308b9648a8622

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
- 実行時に必要なルートパス、時刻文字列、cmoc 管理ディレクトリ、設定ファイル位置を組み立てる共通 helper 群を定義する。
- `<repo-root>`・`<work-root>`・`<cmoc-root>` の解決失敗を cmoc 用エラーへ変換し、呼び出し側が利用者向けの失敗理由を扱える入口になる。
- 作業ディレクトリの一時変更、`<work-root>/memo` 配下判定、`.cmoc` 配下の sessions・reports・log・worktrees・state・config へのパス生成を扱う。

## Read this when
- 実行時のルート解決、特に `<repo-root>`・`<work-root>`・`<cmoc-root>` の取得や失敗時エラー文言を変更する。
- `.cmoc` 配下に作成・参照する sessions、reports、log、worktrees、schema state、config の配置規則を確認または変更する。
- サブコマンドや状態管理処理から使うタイムスタンプ形式、コンソール表示用時刻、経過時間表示の形式を確認または変更する。
- `<work-root>/memo` 自体またはその配下を判定する制御や、処理中だけカレントディレクトリを切り替える処理を扱う。

## Do not read this when
- `<repo-root>` や `<work-root>` というパス概念そのものの定義・探索規則を確認したいだけなら、パスモデル側の定義を直接読む。
- cmoc 用例外クラスの表示形式、終了処理、エラー集約の責務を調べたいだけなら、エラー定義側を読む。
- 個別サブコマンドが各ディレクトリへ何を書き込むか、状態ファイルの内容やレポート内容を調べたい場合は、そのサブコマンドまたは状態管理の実装を読む。
- oracle や realization の分類、INDEX 生成規則、ルーティング文書の仕様を調べたい場合は、この共通 runtime helper ではなく該当する仕様・生成処理を読む。

## hash
- 90f70eda32a0954890b23bea22629dc2a18dce740fb3e55c206f05feb8551820

# `runtime_results.py`

## Summary
- 外部コマンド実行結果と Codex exec 実行結果を受け渡すための、不変なデータ保持クラスを定義する。
- 終了コード、標準出力・標準エラー、生成テキスト・JSON、各種ログや出力先、使用 profile/schema、実行時間や quota 待機状況をまとめる共有の結果モデルである。

## Read this when
- 外部コマンドの実行結果を戻り値として扱うコードの型や保持項目を確認したいとき。
- Codex exec 呼び出し後に、生成物、ログパス、profile 情報、schema 情報、実行時間、quota 待機情報をどのデータ構造で運ぶか確認したいとき。
- 実行結果を返す関数、結果を受け取る処理、テスト fixture の期待値を変更するとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する制御フロー、subprocess 呼び出し、リトライ処理を調べたいとき。
- ログファイルや出力ファイルの生成・保存・削除条件そのものを調べたいとき。
- profile や schema の読み込み、検証、選択ルールを調べたいとき。
- CLI の利用者向け出力形式や JSON schema の仕様を確認したいとき。

## hash
- 149af60f60abfd4347d39a62b9b27d873af9cb1148cba531f191e860be3a9e8b

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
