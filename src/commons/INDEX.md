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
- 実行時共通機能を一箇所から参照できるようにする集約モジュール。Codex 実行、プロファイル、設定、ファイル内容、CLI 実行、エラー、Git、ログ、パス、結果、状態管理に関する既存の共通部品をまとめて取り込む入口になっている。

## Read this when
- 複数の実行時共通部品をまとめて利用している呼び出し側の依存関係を確認したいとき。
- Codex 実行、設定同期、Git worktree 操作、状態ファイル、ログ、パス解決などにまたがる runtime 層の公開入口を把握したいとき。
- runtime 系モジュールの分割済み責務を横断して、どの部品が共通入口から利用可能かを確認したいとき。

## Do not read this when
- 個別機能の実装詳細を確認したいとき。この対象は集約入口なので、Codex 実行、Git 操作、設定、状態管理などの各責務を持つ個別モジュールを直接読む方がよい。
- 新しい処理の実装場所を探しているとき。ここに処理を追加するのではなく、該当責務の個別 runtime モジュールを読む方がよい。
- CLI サブコマンド固有の振る舞いやテストを確認したいとき。共通実行時部品ではなく、サブコマンド実装またはテストを読む方がよい。

## hash
- 4d7b5f772aa040e806c9cb9341fa0ba3457dc3d2229a4646c298217a24affbb8

# `runtime_cli.py`

## Summary
- CLI サブコマンド実装を共通ライフサイクルで実行するための実装。work root 実行前提の検査、サブコマンドログ作成、開始・実行・完了の標準 stdout、戻り値の終了コード化、例外のエラー表示、現在のサブコマンド logger の設定と解除をまとめて扱う。
- 標準サマリー以外の stdout 契約を持つサブコマンド向けに、終了コードと追加 stdout を返す小さな結果型を提供する。
- サブコマンド完了時の共通サマリー出力と、現在ディレクトリが work root であることの検査をこの実行経路の補助責務として持つ。

## Read this when
- CLI サブコマンドの実行開始・完了表示、サブコマンドログ、戻り値から終了コードへの変換、例外時の表示先や終了コードを確認または変更したいとき。
- コマンド固有の stdout 契約を標準サマリーと両立させる方法、または標準サマリーを抑止する実行経路を確認したいとき。
- runtime state を repo root と work root のどちらに置くか、または init のように初期化対象 root を使う呼び出しの扱いを確認したいとき。
- cmoc が work root で実行されていることをどこで検査し、失敗時にどの共通エラーを出すかを確認したいとき。
- サブコマンド実行中の current subcommand logger がどの範囲で設定・解除されるかを追いたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、入出力内容そのものを確認したいだけのとき。
- ログイベントを実際に保存する logger の内部構造、ログファイルの形式、quota wait の計測方法を確認したいとき。
- repo root、work root、時刻表示、経過時間表示の算出規則を確認したいとき。
- cmoc 固有例外の型、エラーメッセージ整形、エラー表示文言の詳細を確認したいとき。
- Typer アプリケーション全体のコマンド登録や CLI ルーティングを確認したいとき。

## hash
- 62037f1fd86cf541184332d899e752c036c0692b4d67b52f28fa5e583ff7661f

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
- Codex CLI の exec 呼び出しを 1 回の状態機械として制御する実装。profile/schema 準備、prompt/call/stdout/stderr/output log の保存、subprocess 実行、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、subcommand event 記録、`.agents` 変更拒否を同じ実行文脈で扱う。
- TUI 起動ではなく exec 分岐の実行制御に責務を限定しており、quota 処理も resume token と log/event の文脈を共有するため同一箇所で読む前提の凝集した処理として置かれている。

## Read this when
- Codex CLI の exec 実行条件、profile 名、schema 指定、resume token、標準入出力、実行結果の扱いを確認または変更したいとき。
- Structured Output 検証失敗時の semantic retry、capacity error 時の指数 backoff、quota error 時の polling/probe/resume の制御を調べるとき。
- Codex 呼び出しごとの prompt/call/stdout/stderr/output log、console 出力、subcommand event、quota 待機時間や poll 回数の記録内容を確認したいとき。
- Codex 呼び出し中に `.agents` 配下が変更された場合の検出と拒否の挙動を確認したいとき。
- Codex exec の実行結果として返す path、profile、schema、経過時間、quota 待機情報、output JSON/text の組み立てを追うとき。

## Do not read this when
- Codex profile の具体的な生成、Codex home の解決、error text や resume token の抽出、output JSON 読み取りなどの低レベル helper だけを調べたいときは、それらを提供する profile/runtime helper を直接読む。
- TUI 起動や exec 以外の Codex 実行経路を調べたいときは、この対象ではなく該当する起動制御の実装を読む。
- subcommand log の保存形式や logger 自体の実装を変更したいだけのときは、logging 側の実装を読む。
- repository/work/codex log directory など runtime path の解決規則を調べたいだけのときは、path 解決側の実装を読む。
- Codex exec の戻り値データ構造そのものを変更したいだけのときは、実行結果型の定義を読む。

## hash
- 68db4ed0ce2485bfe53e92ca8edd95bc5b93a2185f6f157900b66d9f5a5f87df

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
- Codex CLI 起動時に使う profile 本文、sandbox 設定、CODEX_HOME 検証、schema 配置、Codex JSONL 出力からのエラー・resume 情報抽出を扱う実装。
- cmoc の file access policy を Codex CLI の sandbox mode と writable_roots に変換し、AgentCallParameter と設定から再利用可能な Codex profile を生成する責務を持つ。
- Codex subprocess 周辺の実行準備と失敗判定をまとめる入口であり、認証 home、Structured Output schema、出力 JSON、capacity/quota retry 判定を確認するときの読む先になる。

## Read this when
- cmoc から Codex CLI を起動するための profile 内容、model/reasoning effort、sandbox mode、writable_roots の組み立てを変更・確認したいとき。
- FileAccessMode と Codex CLI の read-only/workspace-write sandbox の対応、追加 writable path の扱い、保護対象 path の除外条件を調べるとき。
- CODEX_HOME の解決、auth.json の存在検査、Codex subprocess に渡す環境変数の扱いを確認するとき。
- Structured Output schema を実行用 work root 側へ配置する処理、Codex output JSON の読み取り失敗時の扱いを確認するとき。
- Codex JSONL stdout/stderr から利用者向け error detail、resume 用 thread id、capacity error、quota error を判定する処理を調べるとき。

## Do not read this when
- AgentCallParameter や FileAccessMode の型定義・意味そのものを確認したいだけなら、basic 側の定義を読む。
- cmoc config の model 名や reasoning effort の設定値そのものを確認したいだけなら、config 側の設定定義を読む。
- hashed file の保存方式や schema store directory の実体を調べたいだけなら、runtime content や runtime paths の担当実装を読む。
- Codex CLI を実際に呼び出す subprocess 制御全体、retry ループ、待機方針を確認したい場合は、この補助処理の呼び出し元を読む。
- oracle file や realization file の正本上の file access policy を確認したい場合は、実装ではなく対応する oracle 文書を読む。

## hash
- b3e879e3ccc9ec9b9d932837d86dea576841e50aa8eeb74dd326ba87ffb6755b

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
- Git コマンド実行を共通化し、失敗時の CmocError 変換、現在 branch・HEAD commit・clean worktree 判定など、Git 状態を読むための低レベル helper を提供する。
- cmoc 管理 branch の判定、run worktree の作成・削除、branch 削除など、session/apply/run 系処理が利用する Git worktree と branch 操作を扱う。
- `.cmoc` を Git 追跡対象外に保つための `.gitignore` または Git exclude 更新、index からの除外確認、任意 path の ignore 判定を担う。

## Read this when
- Git コマンド呼び出しの失敗時メッセージ、戻り値、標準出力・標準エラーの扱いを確認または変更したいとき。
- 現在 branch、HEAD commit、未コミット差分の有無など、cmoc 実行前提となる Git 状態チェックを追うとき。
- cmoc が作る管理 branch、run worktree の作成・削除、worktree prune、branch 削除の挙動を確認または変更したいとき。
- `.cmoc` を Git 管理対象から外す処理、clean worktree を保つための exclude 利用、`.gitignore` への ignore pattern 追加、Git index からの除外処理を調べるとき。
- Git ignore 判定を cmoc 内で再利用したい、または `check-ignore` の呼び出し条件を確認したいとき。

## Do not read this when
- CLI 引数定義、サブコマンドの入出力、ユーザー向け表示だけを調べたいとき。
- Git 操作を伴わない path model、設定読み込み、ファイル永続化、構造化データの処理だけを調べたいとき。
- oracle file の正本仕様を確認したいとき。この対象は実装 helper であり、仕様判断の根拠そのものではない。
- 個別サブコマンドの高レベルな制御フローを知りたいだけで、Git 状態確認や worktree/branch/ignore 操作の詳細まで追う必要がないとき。

## hash
- 94f45d788ecf056c0e13e7d98ded1cf5803c827b1d9632210d7b63ff64aa7a3e

# `runtime_logging.py`

## Summary
- サブコマンド実行中に発生した検査用 event を JSON Lines として記録し、サブコマンド単位の経過時間と Codex quota 待機時間を集約する runtime logger を定義している。
- 現在の制御文脈から logger を参照できるようにする context variable と、logger の設定・復元・取得 helper を提供する。

## Read this when
- サブコマンド実行ログの生成先、JSON record の内容、追記タイミング、flush の挙動を確認または変更したいとき。
- サブコマンド完了表示や集計で使う経過秒、quota 待機時間の加算方法を確認または変更したいとき。
- 深い runtime helper から現在のサブコマンド logger を任意に利用する仕組み、または context variable による logger の差し替えと復元を扱うとき。

## Do not read this when
- ログディレクトリの位置や timestamp 文字列の生成規則だけを確認したいときは、runtime path を扱う対象を読む。
- 個別サブコマンドの処理内容や CLI 引数の意味を確認したいだけなら、そのサブコマンド実装を読む。
- JSON Lines に残された実行ログを解析・表示する利用側の処理を探しているときは、ログを読み取る側の対象を読む。

## hash
- 3714c924c277c9b4bc72263497f6db15cd64518cf63712f4cc0730d2e2b11319

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
