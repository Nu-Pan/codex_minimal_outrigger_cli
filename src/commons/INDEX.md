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
- 共通 runtime 層の主要 API を 1 か所から import できるように集約する薄い入口である。Codex 実行、profile・config・content・CLI・error・git・logging・path・result・state など、複数の runtime helper の公開名を再公開する。
- 独自ロジックは持たず、下位 runtime module 群へのルーティング用 facade として位置づく。

## Read this when
- 共通 runtime helper を利用する呼び出し側が、どの公開名をまとめて import できるか確認したいとき。
- runtime 関連の import 経路を整理し、集約入口で再公開されている名前を追加・削除・確認したいとき。
- Codex 実行、設定、git 操作、path、状態、結果型など複数の runtime 領域を横断して使う上位コードの依存先を確認したいとき。

## Do not read this when
- 個別 helper の挙動、引数、失敗時処理、永続化内容を調べたいときは、対応する下位 runtime module を直接読む。
- CLI サブコマンド固有の処理や UI 出力の詳細を調べたいときは、呼び出し側の実装を直接読む。
- runtime API の再公開一覧ではなく、正本仕様や設計意図を確認したいときは oracle 側の本文を読む。

## hash
- 27afe62020c91412f5b3bc611a23155d28e3ef2dbe1974f771f522e0cde0a461

# `indexing.py`

## Summary
- Codex 呼び出し前の索引更新 preflight を登録し、排他制御下で各階層の索引を再生成して必要な commit を作る実装をまとめる。
- 索引対象の directory/child 列挙、既存 entry の hash 検証、対象内容の抽出、Codex への entry 生成依頼、Structured Output から Markdown entry への描画を扱う。
- 索引更新処理全体の入口と、索引 entry の鮮度判定・生成・保存の流れを追うための中心実装である。

## Read this when
- Codex 実行前に索引更新を走らせる preflight 登録や実行順序を確認・変更したいとき。
- 索引更新時の lock、git add/commit、深い directory からの再生成順、並列生成数の扱いを調べたいとき。
- 索引対象から除外される child、既存 entry の再利用条件、hash 計算、Codex に渡す対象内容の作り方を確認したいとき。
- Structured Output の検証失敗時の扱いや、索引 entry Markdown の必須 section 構造を実装側から確認したいとき。

## Do not read this when
- 索引 entry に書くべき意味情報や bullet-only 形式など、正本仕様そのものを確認したいだけのとき。
- runtime の git 実行、hash 計算、binary 判定、設定読み込みの詳細を調べたいとき。
- Codex 実行 parameter の構築内容や prompt 部品の詳細を確認したいとき。
- 特定 directory のルーティング内容を読みたいだけで、索引生成ロジックを変更しないとき。

## hash
- b9a71a5e66c6844ff709f179677be506e1db7cac6984ee44f2df3cb7117b4f41

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実装。work root 検査、サブコマンドログの作成と現在 logger の設定、開始・実行・完了の標準出力、戻り値の終了コード化、例外時のエラー表示と終了コード化を一箇所で管理する。
- 標準サマリー以外に追加の stdout を返すサブコマンド用の結果型、work root で実行されていることの検査、完了時の標準サマリー出力 helper も含む。

## Read this when
- CLI サブコマンド実行時の共通フロー、標準サマリー出力、終了コード、例外表示、typer.Exit への変換を確認または変更したいとき。
- サブコマンドログの生成場所、現在のサブコマンド logger の設定・解除、command_invoked や command_finished の記録内容を追うとき。
- init など、runtime state を通常の root ではなく初期化対象 root に置く挙動や、その前後の pre-log check の呼び出し位置を確認したいとき。
- サブコマンドが標準サマリーに加えて独自 stdout を返す契約を扱うとき。
- cmoc が work root 以外で実行された場合のエラー内容や検査条件を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、永続状態の具体的な読み書きを調べたいだけのとき。
- ログファイルの内部形式、step timing の記録実装、quota wait の加算処理そのものを確認したいとき。
- root path の検出規則、timestamp や duration の整形規則そのものを変更したいとき。
- CmocError の構造や render_error の詳細な表示形式を確認したいとき。

## hash
- a466afe8e6879cc65200f1014b108f67cebc42f41f437a41f34fc04250e0234d

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
- Codex CLI の exec 呼び出しを 1 回の状態機械として制御する実装。profile・sandbox cwd・Structured Output schema を準備し、prompt/stdout/stderr/output/call log を保存しながら subprocess を実行する。
- capacity retry、quota wait と代表 probe、resume token による継続、Structured Output の JSON 読み取りと schema 検証、subcommand event 記録を同じ実行文脈で扱う。
- 16,000 文字を超えるが、retry counter、resume 状態、log/event、subprocess 結果を分離すると文脈が分断されるため、exec 実行制御として凝集させている。

## Read this when
- Codex CLI の exec 実行、再試行、quota 枯渇時の待機・probe、capacity error の exponential backoff、resume 継続の挙動を確認または変更したいとき。
- Structured Output schema の準備、output file の必須 JSON 読み取り、schema validation 失敗時の semantic retry、検証失敗エラーの扱いを確認または変更したいとき。
- Codex call log、prompt/stdout/stderr/output の保存先、call log の内容、console/subcommand log に記録される codex_call event を追いたいとき。
- CODEX_HOME の解決・検証、Codex profile 名、Codex subprocess の環境、file access mode から Codex cwd を決める exec 実行前処理の流れを読む必要があるとき。

## Do not read this when
- Codex profile の具体的な生成内容、Codex subprocess の低レベル実行、resume token 抽出、quota/capacity error 判定 helper の詳細だけを調べたいときは、それらを提供する profile 系の共通実装を直接読む。
- TUI 起動や exec 以外の Codex 実行モードを調べたいときは、この実装ではなく対象モードの runtime module を読む。
- subcommand log 全般、runtime path の定義、config load、AgentCallParameter や CodexExecResult の型そのものを確認したいだけなら、それぞれの定義元を読む。
- oracle の正本仕様を確認したいときは、コード内コメントが参照する app spec や run isolation の正本文書を読む。

## hash
- 25300d9e1216e2cf92d7207e8b9c2f40e1b945636d5a1ce07bad989e0aa6acd3

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
- Codex CLI を起動する subprocess 境界で共有される実行 profile、sandbox/cwd、CODEX_HOME、child process tracking、Structured Output schema 配置、JSONL error 判定をまとめる実装。
- cmoc の FileAccessMode を Codex CLI profile が理解する sandbox 設定と writable/read path 制約へ変換し、追加許可 path が cmoc の読み書き境界を広げないことを検査する。
- Codex subprocess の実行、apply abandon 用の child process pid tracking、Codex CLI 不在時の利用者向けエラー化、stdout/stderr/JSONL からの error・resume・capacity・quota 判定を扱う。

## Read this when
- Codex CLI に渡す profile 本文、sandbox mode、writable_roots、cwd、CODEX_HOME、または追加 read/write path の挙動を確認・変更したいとき。
- FileAccessMode ごとの読み取り・書き込み境界、PURE_ORACLE_READ の cwd、REALIZATION_WRITE/ORACLE_WRITE/REPO_WRITE の sandbox 許可範囲を調べるとき。
- Codex subprocess の起動失敗、apply 実行中の child process tracking、pid file の記録・削除、または process start time による pid 同一性確認を扱うとき。
- Structured Output schema を実行 root 配下の hash store へ配置する処理、schema なし output JSON の読み取り、Codex JSONL stdout/stderr からの error detail・resume token・capacity/quota retry 判定を追うとき。

## Do not read this when
- prompt 本文に利用者へ提示する file access rule を生成する処理だけを確認したいとき。
- hash 名ファイルの書き込み処理や schema store のパス定義そのものを確認したいだけのとき。
- cmoc config の model や reasoning effort の定義・読み込み方法を確認したいだけのとき。
- Codex CLI を呼ばない通常のアプリケーションロジック、サブコマンド仕様、または oracle 文書そのものの内容を調べたいとき。

## hash
- 2a0a866f98a54047a71d418e78dc8b0ef1b4b0bb6d1a9f42313fb94e1f48dd5a

# `runtime_codex_tui.py`

## Summary
- Codex TUI 起動の実行経路を担う実装。agent call parameter、設定、作業ディレクトリから Codex profile、call log、CODEX_HOME、実行 cwd を準備し、Codex CLI を TUI 用引数で起動する。
- 呼び出し結果の console 表示、subcommand logger への codex_call event 記録、失敗時の cmoc 用エラー化までをまとめて扱う入口。

## Read this when
- Codex TUI 呼び出し時の profile 作成、CODEX_HOME 解決、file access mode に応じた cwd 決定、Codex subprocess 起動引数を確認・変更したいとき。
- TUI 呼び出しの call log に保存される項目、ログ保存先、console 表示、codex_call event の payload を確認・変更したいとき。
- Codex CLI/TUI の subprocess 失敗を cmoc のエラーとしてどう扱うか、returncode や call log path をどう伝えるかを確認したいとき。

## Do not read this when
- Codex profile の具体的な生成内容、CODEX_HOME の検証規則、subprocess 実行 helper 自体を確認したいだけの場合は、それらを定義する profile 実行系の実装へ進む。
- cmoc 設定ファイルの読み込み規則や設定 schema を確認したいだけの場合は、設定読み込み・設定定義の実装へ進む。
- Codex call console 表示の文言や表示形式だけを確認したい場合は、Codex logging の実装へ進む。
- repo root、work root、log directory、timestamp など path 計算の規則を確認したいだけの場合は、runtime path 系の実装へ進む。

## hash
- d88502f297a1b2add75009e8364e9bf6df2d7e66843e26fc0f5744a308b5c5ab

# `runtime_config.py`

## Summary
- cmoc の実行時設定を JSON 永続形式と設定モデルの間で変換し、設定ファイルの読み込み・書き込み・初期同期を扱う実装。
- 既定値を基準に、Codex のモデル・推論努力、apply fork、review oracle、並列数の設定を復元し、不正な JSON や型変換失敗を利用者向けエラーへ変換する。

## Read this when
- 設定ファイルの保存形式、既定値の補完、enum key を持つ設定 map の復元方法を確認したいとき。
- 設定ファイルが存在しない、JSON として読めない、top-level が object でない、不正値を含む場合のエラー文言や失敗時挙動を変更するとき。
- 設定項目を追加・削除・改名し、実行時設定の dict 変換、読み込み、書き込み、初期同期に反映する必要があるとき。

## Do not read this when
- 設定モデルそのもののフィールド定義や既定値だけを確認したいときは、設定モデル定義を直接読む。
- 設定ファイルのパス決定だけを確認したいときは、runtime path 側の実装を直接読む。
- 個別コマンドが設定値をどう利用するかを調べたいときは、そのコマンドや呼び出し側の実装を読む。

## hash
- a6a3e9f90e4fd4ccd00387650d0b445f05b7c211843dbf10bd887c4a69592116

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
- git subprocess 実行と worktree/branch 操作を cmoc の共通エラー・戻り値表現へそろえる実装。detached HEAD や未コミット差分の事前条件検査、cmoc 管理 branch 判定、linked worktree 作成・削除、branch 削除を扱う。
- .cmoc を git 追跡対象外にするための ignore 判定・更新処理を担う。通常の ignore 初期化、clean worktree を保つための exclude 更新、初期化済み repository の検査、任意 path の ignore 判定への入口になる。

## Read this when
- git コマンド実行失敗を cmoc 利用者向けエラーへ変換する境界処理を確認・変更したいとき。
- 現在 branch、HEAD commit、clean worktree 必須条件、cmoc 管理 branch namespace の扱いを確認・変更したいとき。
- run/apply/session などで使う linked worktree の作成・削除や一時 branch 削除の挙動を確認・変更したいとき。
- .cmoc の git ignore 初期化、git exclude による ignore 保証、追跡対象外検査、または path が ignore されるかの判定を確認・変更したいとき。

## Do not read this when
- git 操作を呼び出す個別サブコマンドの CLI 入出力、引数解析、レポート生成だけを調べたいとき。
- cmoc の永続状態ファイルの schema や読み書き処理そのものを調べたいとき。
- git 以外の runtime error 型や command result 型の定義だけを確認したいとき。
- oracle の path keyword 定義や repository/worktree path model の仕様を確認したいとき。

## hash
- 025c1d2a729bdb9d9943161c3426f9b67ae8bd8268f74c27d8d4979c1b16ff20

# `runtime_logging.py`

## Summary
- サブコマンド実行中のイベント記録、step の開始・経過時間、quota 待機時間を集約する実行時 logger を定義する。
- 実行ごとに logs 配下へ JSON Lines の log file を確保し、event record を追記する責務を持つ。
- 深い runtime helper から現在のサブコマンド logger を参照できるよう、context ごとの current logger の設定・復元・取得を提供する。

## Read this when
- サブコマンド単位の実行 log、JSON Lines event、step_started event、完了サマリー用の step timing を調べるとき。
- Codex quota 待機時間を実行全体の待機時間として集計する処理を確認・変更するとき。
- 実行中の制御文脈に紐づく current logger を設定、リセット、参照する runtime helper の挙動を確認するとき。
- log file の生成場所、timestamp 名による排他的な確保、event record の基本項目を確認するとき。

## Do not read this when
- CLI の表示文言や利用者向けの console 出力仕様だけを確認したいとき。
- logs 配下のパス解決や timestamp 文字列の生成規則そのものを確認したいとき。
- 個別サブコマンドの業務処理、引数解析、状態更新の実装を探しているとき。
- 生成済み log を解析・集計する読み取り側の処理を探しているとき。

## hash
- 6c9b4a4c583c28c18afd061c8230290bf642e6b5004f5889d6039988207fbd45

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
- session state file の永続化モデルと読み書き操作を扱う実装。session/apply の state 断片、JSON schema 検証、cmoc 管理 branch 名からの session_id 抽出、現在 branch に対応する state 読み込み、canonical JSON 書き戻し、home branch に紐づく active session 探索をまとめている。
- session state file の不正構造や不正な state 値、cmoc 管理外 branch、欠落した state file を CmocError として扱う境界もここにある。

## Read this when
- session state file の JSON 構造、必須 field、許容される session/apply state 値を確認または変更したいとき。
- cmoc session branch や cmoc apply branch の命名から session_id を取り出す処理、または branch 種別ごとの state file 解決を扱うとき。
- session state file の読み込み、検証、書き戻し、保存先 path、active session 探索に関する挙動を調べるとき。
- session/apply の進行状態を更新する上位処理から、永続 state の表現やエラー条件を確認したいとき。

## Do not read this when
- CLI subcommand の引数定義、画面出力、コマンド全体の制御フローを調べたいだけのとき。
- session state file の仕様意図そのものを確認したいときは、対応する oracle doc を直接読む方がよい。
- runtime path の基準ディレクトリ定義や sessions directory の組み立てだけを調べたいとき。
- CmocError の表示形式や例外クラス自体の責務を調べたいとき。

## hash
- 639a3107fd6c4d1ad5208798d2042e7bdaa8b70ba12f3984bd72b4432b5dab30
