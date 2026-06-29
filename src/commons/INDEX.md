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
- commons の runtime 系機能を一箇所から参照できるように、Codex 実行、profile、設定、content hash、CLI 実行、error、git、logging、path、result、state などの補助 API を取りまとめて import する集約モジュール。
- ここ自体は挙動を実装せず、各 runtime helper の利用入口をまとめる役割を持つ。

## Read this when
- runtime 系 helper を呼び出す側の import 経路を確認したいとき。
- commons 配下の runtime helper を移動・分割・統合した結果、この集約入口に載せる import を調整する必要があるとき。
- Codex 実行、git、path、state、config など複数の runtime helper 群を横断して、どの API がまとめて公開されているかだけを確認したいとき。

## Do not read this when
- 各 helper の具体的な挙動、引数、失敗時処理、副作用を確認したいとき。その場合は対応する実装元モジュールを直接読む。
- 特定領域だけを変更する作業で、呼び出し元の import 集約を変える必要がないとき。
- 新しい runtime 挙動を実装したいとき。ここではなく、責務に対応する個別の runtime helper 側を読む。

## hash
- 5938d7fab050dcf151579a85b507ed1bc982691d11fabbaad698dccc0f723eaa

# `indexing.py`

## Summary
- Codex 実行前にルーティング用目次を最新化する preflight の登録、排他制御、更新検出、生成、保存 commit までをまとめて担う実装。
- 対象ディレクトリと子要素の列挙、既存エントリーの形式検証、鮮度判定用ハッシュ計算、Structured Output から Markdown への描画を扱う。
- エントリー生成そのものは外部の Codex 実行関数に委譲し、生成対象の本文抽出と実行時の root・cwd・config・purpose の組み立てを行う。

## Read this when
- Codex 呼び出し前に目次更新を走らせる preflight の流れ、排他 lock、更新 commit の挙動を確認したいとき。
- 目次作成対象に含めるディレクトリやファイル、除外する symlink・memo・git ignored・binary の条件を変更したいとき。
- 既存エントリーを再利用する条件、必須セクションと bullet-only 形式の検証、ハッシュ抽出の挙動を調べたいとき。
- Structured Output の検証、エントリー本文のレンダリング、生成失敗時の CmocError を扱う実装を変更したいとき。
- 目次更新時の並列生成数、対象本文の渡し方、Codex 実行関数への引数を追う必要があるとき。

## Do not read this when
- 人間が管理する正本仕様断片としての目次仕様や Codex 実行ルールを確認したいだけなら、対応する oracle 側の文書を読む。
- 個別エントリーの文章品質や生成 prompt の標準を変更したいだけなら、エントリー生成パラメータや prompt builder 側を読む。
- git コマンド実行、設定読み込み、ハッシュ計算、binary 判定、git ignored 判定そのものの共通実装を調べたいだけなら、runtime 側の該当 helper を読む。
- 通常の CLI コマンド定義や利用者向けオプションを調べたいだけなら、CLI 層の実装を読む。

## hash
- d0096b737f0b5da279be6b4d302ad3fcfa44218a969d349d351be94543f150d9

# `runtime_cli.py`

## Summary
- CLI サブコマンド共通の実行ライフサイクルをまとめる実装。work root 検査、pre-log 処理、サブコマンドログ作成、開始・実行・完了の標準出力、戻り値の終了コード化、例外時のエラー表示、現在のサブコマンド logger の設定と解除を扱う。
- 標準サマリー以外の stdout を返すサブコマンド向けの結果型と、cmoc が work root で実行されていることを検査する共通関数、完了時サマリー出力の helper も含む。

## Read this when
- CLI サブコマンドの共通実行順序、標準の進捗表示、完了サマリー、終了コード処理、例外表示の挙動を確認または変更したいとき。
- サブコマンドログの生成場所、runtime state の root 選択、init などでログ作成前に行う検査、現在のサブコマンド logger の扱いを追いたいとき。
- サブコマンド実装から独自 stdout と終了コードを返す契約、または work root 以外で実行された場合の共通エラーを調べたいとき。

## Do not read this when
- 個別サブコマンドの引数定義、CLI アプリへの command 登録、または各サブコマンド固有の処理内容だけを知りたいとき。
- サブコマンドログファイルの内部形式、step timing の記録方法、quota 待機時間の更新方法そのものを調べたいとき。
- repo root や work root の検出規則、タイムスタンプや経過時間の整形規則そのものを確認したいとき。

## hash
- add81e2cda35041a82bd78cd995edbaca0e6561e6da1438a9ee203063373515c

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
- Codex CLI の非 TUI exec 呼び出しを 1 回の状態機械として制御する実装。profile 準備、実行 argv 構築、prompt/stdout/stderr/output/call log 保存、Structured Output 検証、semantic retry、capacity retry、quota 枯渇時の代表 probe と待機中呼び出しの再開、subcommand event 記録を扱う。
- quota 待機と resume 継続は、同じ subprocess 結果、resume token、log/event、retry counter の文脈を共有する必要があるため、この対象が exec 実行制御の中心入口になる。

## Read this when
- Codex CLI を `exec` として起動する通常実行、Structured Output schema 付き実行、または output JSON の読み取り・検証・再試行挙動を確認または変更したいとき。
- capacity error の指数 backoff、quota error 後の代表 probe、quota 回復待ち中の他呼び出しとの同期、resume token による継続実行の制御を確認または変更したいとき。
- Codex call log、prompt/stdout/stderr/output log、console 表示、subcommand logger の `codex_call` event に記録される実行条件や結果を追いたいとき。
- Codex 実行用 profile、CODEX_HOME、Codex cwd、追加 read/write path、oracle conflict write 許可、output schema path が実際の `codex exec` 呼び出しへどう渡るかを追いたいとき。

## Do not read this when
- TUI 起動や対話 UI 側の分岐を調べたいとき。この対象は exec 実行制御に責務を限定している。
- Codex profile の内容生成、CODEX_HOME 解決、capacity/quota error 判定、resume token 抽出、output JSON の低レベル読み取り helper 自体を変更したいときは、それらを定義する runtime profile 側を直接読む。
- quota availability probe の prompt 内容を変更したいときは、probe 用 AgentCallParameter を組み立てる側を直接読む。
- 実行結果を保持する戻り値型、runtime path の算出規則、subcommand logger の実装詳細だけを確認したいときは、それぞれの型・path・logging 定義を読む。

## hash
- 96a8724c9102eedbef2b304a767faa69823f995221c63b28d71a3cfeabea64b9

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し完了時に、目的、呼び出しログ位置、経過時間、終了コードを利用者向け console へ通知するための小さな出力 helper を定義する。
- 時刻表記と経過時間表記は共通の runtime path 系 helper に委ね、oracle が定める console 通知形式に沿った複数行メッセージを標準出力へ即時 flush する入口である。

## Read this when
- Codex CLI 呼び出し後に利用者の console へ出す通知内容、表示順、表示項目を確認または変更したいとき。
- Codex CLI 呼び出しログへの参照、経過時間、終了コードをどのように人間向け表示へ整形しているかを追いたいとき。
- console 用の時刻文字列や duration 文字列を使った Codex CLI 呼び出し通知の実装箇所を探しているとき。

## Do not read this when
- Codex CLI 呼び出しそのものの実行、プロセス起動、標準入出力の捕捉、戻り値制御を調べたいとき。
- ログファイルの生成、保存先決定、ファイルへの書き込み仕様を調べたいとき。
- 汎用的な runtime path の解決、時刻文字列や経過時間文字列の詳細な整形規則を調べたいとき。
- Codex 以外の CLI 通知や、利用者向け console 出力全般の設計を広く調べたいだけのとき。

## hash
- f958a19df4363d9585a17c45b2fee6d85d6cd968c79555d33f83707bdfbf8aca

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
- Codex CLI subprocess 境界で使う profile、sandbox、cwd、CODEX_HOME、schema 配置、process tracking、JSONL error 判定をまとめる実装。
- FileAccessMode を Codex CLI が理解する sandbox/profile 設定へ変換し、追加 read/write path が cmoc の許可境界を越えないことを検査する。
- apply abandon で停止対象を識別できるよう Codex child process の pid と starttime を lock 付き pid file に記録・削除し、Codex 実行失敗や capacity/quota 系 JSONL event を cmoc の実行時判断へ変換する。

## Read this when
- Codex CLI 起動用 profile の生成、再利用、profile 名抽出、sandbox_mode、writable_roots、cwd、CODEX_HOME の扱いを確認・変更するとき。
- FileAccessMode ごとの読み取り・書き込み許可境界、追加 read/write path の検査、REALIZATION_WRITE、REPO_WRITE、ORACLE_WRITE、PURE_ORACLE_READ の sandbox 上の表現を調べるとき。
- apply 実行中の Codex child process tracking、pid file lock、pid 再利用検出、abandon から停止できる subprocess 記録の挙動を確認・変更するとき。
- Codex subprocess 呼び出し時の環境変数、Codex CLI 不在時の CmocError 化、subprocess.run と tracked Popen の境界を調べるとき。
- Structured Output schema の hash store 配置、schema なし output JSON の読み取り、Codex JSONL stdout/stderr から利用者向け error detail、resume token、capacity/quota retry 判定を扱うとき。

## Do not read this when
- prompt 本文に載せる file access rule の文言や利用者向け指示そのものを確認したいだけの場合は、prompt builder 側の仕様・実装を読む。
- cmoc の path token、work root、run root、schema store directory などの基本 path 定義を調べたいだけの場合は、path model や runtime path の実装を読む。
- Codex model 名や reasoning effort の設定値そのもの、設定ファイルの読み込み規則を変更したい場合は、設定定義側を読む。
- hash 付きファイルを書き出す低レベル処理や内容 hash の命名規則だけを調べたい場合は、runtime content 側を読む。
- CLI サブコマンドの画面仕様、apply、session join、tui などの利用者向け挙動を確認したい場合は、該当サブコマンド仕様または呼び出し側を読む。

## hash
- fe3bad7d4ed7b3a2bf07b30d6ac46fc7dd0eae27b4fa85e5ef6686624841bdfc

# `runtime_codex_tui.py`

## Summary
- Codex TUI 起動用の実行経路を担い、設定読み込み、call log 作成、Codex profile 準備、Codex subprocess 呼び出し、失敗時の cmoc エラー化までをまとめる。
- Agent 呼び出しパラメータから Codex の作業ディレクトリ、CODEX_HOME、profile、起動 argv を組み立て、TUI 呼び出し結果をコマンド結果として返す境界に位置する。
- Codex 呼び出しのコンソール通知とサブコマンドイベントログへ、実行時間、戻り値、call log、profile 情報を残す処理も含む。

## Read this when
- Codex TUI を起動するサブコマンドの挙動、引数組み立て、profile 選択、CODEX_HOME 解決、作業ディレクトリ決定を確認・変更したいとき。
- TUI 呼び出しの call log に記録される内容、保存先、purpose、model class、reasoning effort、file access mode などの記録内容を確認したいとき。
- Codex subprocess の失敗時に、どの例外へ変換され、利用者へどの確認指示と詳細情報が出るかを調べるとき。
- TUI 起動時の追加 read path、linked worktree、Codex profile 配置、writable root まわりの制御を追う必要があるとき。

## Do not read this when
- Codex CLI 呼び出しに共通する profile 生成、CODEX_HOME 検証、subprocess 実行 helper の内部実装だけを調べたいときは、共通 profile・実行補助側を読む。
- 設定ファイルの読み込み規則そのもの、runtime path の定義、timestamp や log directory の算出規則だけを確認したいときは、それぞれの共通 runtime module を読む。
- 非 TUI の Codex 実行経路や、Codex 呼び出し以外のサブコマンド結果処理を調べたいときは、該当する呼び出し元または結果処理の module を読む。

## hash
- 282709994a710f28c42883f934e94c9c2d1ae4a36a91fefc1f755598a316f5e9

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
- git subprocess 実行を cmoc の共通結果型と利用者向けエラーへそろえる境界を担う。branch・HEAD・worktree 清潔性・branch 存在確認など、git repository の現在状態を調べる helper をまとめる。
- cmoc が管理する branch namespace と linked worktree の作成・削除・branch 削除を扱い、管理外 worktree を削除しないための path 検証もここに集約する。
- `.cmoc` を git 追跡対象外に保つための `.gitignore`、git exclude、index、ignore 判定の処理を扱う。

## Read this when
- git command の実行失敗を `CmocError` と `CommandResult` にどう変換するかを確認・変更したいとき。
- detached HEAD、未コミット差分、現在 branch、HEAD commit、branch 存在確認など、git repository 前提条件の検査を扱うとき。
- cmoc が作る run/apply/session 系 branch の判定や、run/apply 用 linked worktree の作成・削除・prune・branch 削除に関わる挙動を確認・変更したいとき。
- `.cmoc` を `.gitignore` または git exclude で ignore させる処理、追跡済み `.cmoc` の index からの除外、ignore 状態の検査を扱うとき。
- 任意 path が git ignore されるかを work root 基準で判定する処理を確認・変更したいとき。

## Do not read this when
- git 以外の外部コマンド実行境界や subprocess 全般の方針を探しているだけのとき。
- cmoc の path model 定義そのもの、`<cmoc-root>` や `<work-root>` の概念仕様を確認したいとき。
- session state や report に HEAD commit をどう保存するかなど、git から取得した値の利用先を調べたいとき。
- CLI サブコマンドの利用者向け引数、出力 schema、操作フローそのものを確認したいとき。
- `.gitignore` や git exclude 以外の設定ファイル、永続状態ファイル、実行ログの読み書きを扱うとき。

## hash
- b2713ceeac3ccc9f67934f3ec38cf0713513c5498cd16b1d499c2e3e909f865e

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
- 実行時に必要なルート解決、時刻文字列、実行状態を置くディレクトリや設定ファイルのパス、memo 配下判定、作業ディレクトリ一時変更をまとめる共通 helper。
- repository/worktree の位置特定失敗を CmocError に変換し、CLI 実行場所に依存する処理が共通の失敗時挙動を使うための入口になる。

## Read this when
- 実行時の repository root、worktree root、cmoc root の解決方法や、解決失敗時のエラーメッセージを確認・変更したいとき。
- sessions、reports、logs、worktrees、codex log、schema store、config など、`.cmoc` 配下の保存先パスを作る処理を確認・変更したいとき。
- timestamp や console 表示用 timestamp、経過時間表示の形式を確認・変更したいとき。
- memo 自体またはその配下を判定する処理や、処理中だけ cwd を切り替えて必ず戻す文脈管理を使う・修正するとき。

## Do not read this when
- path placeholder の種類、抽象的な path model、実パス解決の正本仕様を確認したいだけなら、path model 側の仕様・実装を読む。
- 個別サブコマンドがどの保存先をいつ作成・更新・削除するかを知りたいときは、そのサブコマンド側の実装を読む。
- CmocError の構造、表示形式、例外の共通扱いを変更したいときは、runtime error 定義側を読む。
- ファイルシステム操作全般、Git 操作、設定 JSON の読み書き内容を確認したいだけなら、それぞれの責務を持つ別の実装を読む。

## hash
- 7415276735049b6804964a29f6671212540142e6dec612218466b2617747e2fc

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
