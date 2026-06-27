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
- cmoc の実行時共通機能を直接実装せず、Codex 実行、設定、内容ハッシュ、CLI 呼び出し、エラー描画、git 操作、ログ、パス、結果型、状態管理などの下位 runtime API をまとめて公開する集約入口。
- この対象自体の責務は、各 runtime 領域の具体処理を置くことではなく、呼び出し側が複数の共通機能へ一つの import 面から到達できるようにすることにある。

## Read this when
- runtime 系の共通 API がどの機能群から集約されているかを確認したいとき。
- 呼び出し側の import 面を整理する変更で、既存の共通 runtime API が集約入口から公開されているかを確認したいとき。
- Codex 実行、設定、git、パス、状態など複数領域をまたぐ処理を読む前に、利用可能な共通 API の入口を把握したいとき。

## Do not read this when
- 各 API の具体的な挙動、入出力、副作用、例外処理を知りたいとき。その場合は該当する責務を実装している下位の runtime 本体を読む。
- 新しい runtime 処理の実装場所を探しているとき。この対象は集約入口であり、処理本体を追加する場所ではない。
- 設定、内容ハッシュ、git 操作、パス解決、状態ファイル操作など単一領域だけを変更する場合。その領域を担当する下位対象へ直接進む。

## hash
- 2685ce534f01e5ce3f6f5191a1baeff4bd5e26e471f8610d4dc55ad3d2401846

# `indexing.py`

## Summary
- Codex 呼び出し前の preflight として、各ディレクトリのルーティング文書を再生成し、更新分だけを専用 commit にまとめる処理を担う。
- 対象候補の列挙、既存エントリーの hash 検証、欠落・古いエントリーの Codex 生成、Markdown への描画、鮮度判定用 hash 計算までをまとめて扱う。
- root memo、git ignore、バイナリ、隠し要素を除外しながら、深い階層から順に更新するための indexing 実行経路の入口になる。

## Read this when
- Codex 実行前にルーティング文書を自動更新する流れ、排他制御、更新 commit の作成条件を確認したいとき。
- 対象ディレクトリや子要素が indexing 対象になる条件、除外条件、処理順序を変更したいとき。
- 既存エントリーを再利用する hash 検証、必須セクションの解析、Structured Output からのエントリー描画を調べたいとき。
- エントリー生成用 Codex 呼び出しに渡す対象本文、実行 root、設定、エラー条件を確認したいとき。

## Do not read this when
- 個別のエントリー本文の品質基準や、ルーティング文書がどうあるべきかという正本仕様だけを確認したいとき。
- Codex 実行そのものの低レベル実装、git コマンド実行、hash 計算、設定読み込みの共通 runtime 挙動を調べたいとき。
- preflight 登録先の汎用 hook 機構だけを変更したいとき。
- 実際に生成されたルーティング文書の内容を読むだけで、生成・更新ロジックを追う必要がないとき。

## hash
- 70ffda6afef81e3c3d389ed94c06ac982c54bc051e157b9fc673d2e0f7f9cee6

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実装。work root 実行検査、サブコマンドログの作成と現在 logger の設定、開始・実行・完了の標準 stdout サマリー、戻り値の終了コード化、例外の整形表示、logger state の後始末を一箇所に集約する。
- 標準サマリー以外の stdout 契約を持つサブコマンド向けに、終了コードと任意 stdout を返す結果型も定義する。
- runtime state を repo root に置く通常経路と、初期化対象である work root に置く経路を切り替えつつ、サブコマンドログは常に repo root 側に置く責務を持つ。

## Read this when
- CLI サブコマンド実装を共通 wrapper 経由で実行する方法、戻り値を終了コードや stdout に変換する契約、または `console_output` の有無による stdout 挙動を確認したいとき。
- サブコマンド実行時のログ作成、`command_invoked`・`step_started`・`command_finished` の記録、現在サブコマンド logger の設定と解除に関わる変更をするとき。
- cmoc が work root で実行されていることの検査、cwd 不一致時の利用者向けエラー、または work root と repo root の使い分けを確認したいとき。
- サブコマンド例外を `CmocError` 系の表示形式へ変換する処理、stdout と stderr の出し分け、例外に付与された command-specific stdout/stderr 指示の扱いを変更するとき。
- サブコマンド完了時に出る標準サマリーの項目、時刻・経過時間・quota wait・returncode の表示を確認または変更するとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、入力解析、永続データ更新、ファイル生成内容を知りたいだけのときは、そのサブコマンド本体を読む。
- エラー文面のレンダリング規則そのものやエラー型の定義を変更したいときは、エラー処理を担う共通実装を読む。
- runtime path の算出規則、work root・repo root・時刻や duration の書式定義を変更したいときは、path と runtime 表示を担う共通実装を読む。
- サブコマンドログの保存形式、イベント JSON の具体構造、quota wait の計測方法を変更したいときは、ログ機構を担う共通実装を読む。
- Typer のコマンド登録や CLI option の宣言を探しているときは、コマンド定義側を読む。

## hash
- 9516bae549aeef5b486e5c1b6f835d140d919dab46bb9eebba233228fc38d595

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
- Codex CLI の exec 呼び出しを 1 回の実行状態機械として制御する実装。profile/schema 準備、prompt/stdout/stderr/output/call log の生成、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume token による継続、subcommand event 記録、`.agents` 変更拒否をまとめて扱う。
- TUI 起動や profile 生成そのものではなく、Codex subprocess を実行して結果を `CodexExecResult` として返すまでの再試行・検証・記録の分岐を読む入口になる。

## Read this when
- Codex CLI exec の呼び出し引数、cwd、CODEX_HOME、profile、schema、prompt 入力、出力 JSON の扱いを確認または変更したいとき。
- Codex call log、prompt/stdout/stderr/output log、console 表示、subcommand log event に記録される内容やタイミングを調べるとき。
- Structured Output の JSON Schema 検証失敗時の semantic retry、capacity error 時の指数 backoff retry、quota error 時の polling/probe/resume 継続の制御を変更するとき。
- Codex CLI 呼び出し後に `.agents` 配下の変更を検出して拒否する挙動や、その失敗を log/event に残す順序を確認するとき。
- 複数回の Codex exec log 名を同一プロセス内で単調増加させる必要や、retry 間で共有される resume token・retry counter・quota wait 集計を追うとき。

## Do not read this when
- Codex profile の具体的な作成、file access mode から cwd への変換、quota/capacity error 判定、resume token 抽出、出力 JSON 読み取りなどの低レベル helper 自体を変更したい場合は、それらを定義する profile/runtime helper を直接読む。
- Codex call の console 表示形式だけ、または subcommand logger の基盤だけを変更したい場合は、それぞれの logging 実装を直接読む。
- TUI 起動や exec 以外の Codex 実行形態を扱う場合は、この対象ではなく該当する起動制御 module を読む。
- 単に `CodexExecResult` のデータ構造や downstream の利用箇所を確認したいだけなら、結果型や呼び出し側を直接読む。

## hash
- e08692e3225f6309605899e2c0eb152d6eba22e413d5fbd2cfa5f2f7974b8cec

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
- Codex CLI 実行時に使う profile 本文の組み立て、CODEX_HOME の解決・検証、profile 名の抽出、hash 化した profile/schema の配置を扱う。
- FileAccessMode を Codex の sandbox mode、cwd、writable_roots に変換し、memo や .agents、oracle 専用読み取りなどのアクセス境界を Codex profile 上で表現する。
- Codex subprocess の起動ラッパーとして、Codex CLI 不在時の cmoc error 化、子プロセス tracking、JSONL stdout からの error・quota・capacity・resume token 抽出を担う。

## Read this when
- AgentCallParameter や repo config から Codex CLI 用 profile を生成・再利用する処理を確認または変更したいとき。
- FileAccessMode ごとの sandbox mode、Codex cwd、読み取り追加 path、書き込み root の許可判定を確認したいとき。
- CODEX_HOME の解決、auth.json 存在検査、Codex subprocess に渡す環境変数の扱いを調べたいとき。
- Codex CLI 呼び出し失敗、子プロセス追跡、Codex JSONL stdout/stderr からの利用者向け error text・retry 判定・resume token 抽出を調べたいとき。
- Structured Output schema を work root 側の hash store に配置する処理や、Codex output JSON の読み取り失敗時挙動を確認したいとき。

## Do not read this when
- FileAccessMode や AgentCallParameter そのものの定義を確認したいだけなら、それらを定義する基本モデルを読む。
- CmocConfig の設定 schema や model/reasoning_effort の読み込み規則を確認したいだけなら、設定側の実装を読む。
- hash 付きファイルの書き込み方式や schema store の実体 path を確認したいだけなら、content 書き込み helper や runtime path helper を読む。
- Codex 実行プロンプト本文、prompt parts、またはユーザー向け file access rule の文章を調べたい場合は、対応する oracle または prompt 生成側を読む。

## hash
- 1f5503345407e67c8db297eabfadc3d15d634ced1005fb1809da856bdc29734b

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを行うための実行時処理を提供する。設定読み込み、call log 作成、Codex profile 準備、作業ディレクトリと CODEX_HOME の解決、外部 Codex プロセス起動、結果ログ出力、失敗時の cmoc 用エラー化を一連で扱う。

## Read this when
- AgentCallParameter から Codex TUI を起動する制御フローを確認・変更したいとき。
- Codex 呼び出し時の profile 名、CODEX_HOME、作業ディレクトリ、file access mode に応じた cwd 解決、追加 read path の渡し方を追いたいとき。
- Codex TUI 呼び出しの call log に記録される項目、保存先、コンソール通知、subcommand logger へのイベント記録を確認したいとき。
- Codex CLI/TUI の subprocess 失敗を cmoc の CommandResult または CmocError として扱う境界を確認したいとき。

## Do not read this when
- Codex profile の具体的な生成内容、環境変数の組み立て、CODEX_HOME 検証、file access mode から cwd への変換そのものを変更したいだけのときは、それらを定義する profile 系の実行時処理を読む。
- 設定ファイルの読み込み規則そのものを確認したいときは、設定読み込みの実行時処理を読む。
- ログディレクトリ、repo root、work root、timestamp などの path 解決規則そのものを確認したいときは、path 系の実行時処理を読む。
- Codex 呼び出し結果のコンソール表示形式や共通ログ基盤だけを変更したいときは、それぞれの logging 系の実行時処理を読む。

## hash
- 33918fa90c10f7b7f68a377863266e3409df173636e6c0d539b01a2fceb71d86

# `runtime_config.py`

## Summary
- cmoc の設定データを、既定値付きの内部設定モデルと JSON 保存形式の間で変換し、設定ファイルの読み込み・書き込み・同期を行う実装。
- 設定値の型変換、enum キー付きマッピングの復元、不正な設定 JSON や未初期化状態を利用者向けエラーへ変換する入口を持つ。

## Read this when
- 設定ファイルの JSON schema 相当の保存形、既定値の埋め戻し、モデル名や reasoning effort の文字列マッピングを確認・変更したいとき。
- 設定ファイルが存在しない、JSON として読めない、top-level が object でない、不正な値を含む場合のエラー文言や失敗条件を確認・変更したいとき。
- 初期化済み設定を読み込む処理、未存在時に既定設定を書き出す処理、設定ファイルの保存先 path を使う処理を追いたいとき。

## Do not read this when
- 設定モデルそのもののフィールド定義や既定値を確認したいだけなら、設定モデル定義を直接読む。
- 設定ファイルの保存先 path の規則だけを確認したいなら、runtime path を扱う実装を直接読む。
- CLI サブコマンドの引数、表示、呼び出し順を確認したいだけなら、コマンド層の実装を読む。

## hash
- 7e04d56621b72d05a69e78c781408143eb3810dcb5fd7e2d21dc666b4683665e

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
- サブコマンド実行中に追記される JSON Lines event log を作成し、command・timestamp・任意 payload を安定した record として保存する runtime logging の実装。
- サブコマンド開始からの経過時間と Codex quota 待機時間を集約し、現在の制御文脈から参照できる logger を ContextVar で差し替え・復元・取得できる入口を提供する。
- log 保存先の作成と、サブコマンドごとに一意な timestamp 付き log file を原子的に予約する責務を持つ。

## Read this when
- サブコマンド単位の runtime event を JSON Lines として保存する処理を確認・変更したいとき。
- 完了表示や集計に使うサブコマンド経過時間、または Codex quota 待機時間の加算方法を確認・変更したいとき。
- 深い runtime helper から現在のサブコマンド logger を任意利用するための context 管理を確認・変更したいとき。
- log directory の作成、timestamp 付き log file 名の衝突回避、またはサブコマンドごとの log file 生成単位を確認したいとき。

## Do not read this when
- CLI のサブコマンド定義、引数解析、利用者向け出力そのものを確認したいだけのとき。
- log directory や timestamp のパス規則そのものを確認・変更したいときは、runtime path を扱う対象を読む。
- 保存された JSON Lines の外部仕様や console/file log 全体の正本仕様を確認したいときは、対応する oracle doc を読む。
- 個別の業務処理や git 操作の挙動を確認したいだけで、runtime event log への記録方法に関心がないとき。

## hash
- 61f0584ed72e5b6b43ec405f2d45cc39e3fe9813859ae3d45d8034727ca30b93

# `runtime_paths.py`

## Summary
- 実行中の cmoc が扱うルートパス、時刻文字列、実行状態保存先、ログ・レポート・設定ファイルの配置、memo 判定、作業ディレクトリ一時変更をまとめた共通 helper 群。
- 基本層のパス解決に失敗した場合は利用者向けの共通エラーへ変換し、上位コマンドが `<repo-root>`、`<work-root>`、`<cmoc-root>` や `.cmoc` 配下の標準配置を一貫して参照するための入口になる。

## Read this when
- コマンド実行時に現在位置から `<repo-root>`、`<work-root>`、`<cmoc-root>` を取得する処理や、その失敗時メッセージを確認・変更したいとき。
- セッション、レポート、ログ、worktree、schema store、設定ファイルなど `.cmoc` 配下の標準保存先を使う実装の参照先を探しているとき。
- 内部保存用 timestamp、コンソール表示用 timestamp、経過時間表示の形式を確認・変更したいとき。
- `<work-root>/memo` 自体または配下かどうかを判定する境界、または一時的にカレントディレクトリを変更して必ず戻す処理を確認したいとき。

## Do not read this when
- パス概念そのものの定義や `<cmoc-root>`、`<repo-root>`、`<work-root>` の解決規則を確認したいだけの場合は、基本層のパスモデルを直接読む。
- 共通エラー型の構造、表示形式、終了コードなどを確認したい場合は、エラー定義側を読む。
- 特定サブコマンドがどの保存先をいつ作成・更新・削除するかを知りたい場合は、そのサブコマンド実装や状態操作の本文を読む。
- 実際のファイル入出力、JSON schema の内容、ログ本文の生成規則を調べたい場合は、この helper ではなく各機能の実装を読む。

## hash
- 6a1e0d848764448e62ddac9e8c77a56e3b35314bd0239761d7d1643cc73f4da8

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
