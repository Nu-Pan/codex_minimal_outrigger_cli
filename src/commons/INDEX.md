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
- runtime 系 commons の主要 API を 1 か所から参照できるように集約する入口。Codex 実行・profile・config・content・CLI・error・git・logging・paths・results・state にまたがる既存 runtime 部品を再公開する役割を持つ。
- 実処理の実装本体ではなく、周辺モジュールに分散した runtime 機能への import 境界をまとめるための薄い集約層として読む。

## Read this when
- 複数の runtime commons 機能をまとめて利用している呼び出し側の import 元を確認したいとき。
- runtime 系 API の公開入口にどの関数・クラス・定数が含まれているかを確認したいとき。
- runtime commons の分割済みモジュールへ進む前に、Codex 実行、git、path、state、config などの横断的な参照関係を把握したいとき。

## Do not read this when
- 個別機能の挙動や副作用を調べたいとき。その場合は、対応する runtime commons の実装本体を直接読む。
- 新しい runtime 処理を実装・修正したいとき。この集約層ではなく、責務を持つ下位モジュールを読む。
- CLI サブコマンドの利用者向け挙動や出力仕様を確認したいとき。より直接の command 実装またはテストを読む。

## hash
- 8966f0d5a850e449686651c59834522e9dbbe9937161b01765fe8e2215085580

# `indexing.py`

## Summary
- Codex 呼び出し前の INDEX 更新 preflight、排他制御、差分 commit、ディレクトリ走査、既存エントリー再利用、エントリー生成、hash 鮮度判定、Structured Output 検証と Markdown 描画をまとめて担う実装。
- INDEX.md の自動最新化を、git 管理領域の lock、git ignore・memo・binary・symlink 除外、深い階層からの更新、直列の entry 生成という制御で成立させる。
- エントリー本文の形式検証、対象内容の取り出し、対象 hash の再帰計算、Codex 実行関数への entry 生成依頼までを一連の indexing 実行経路として読む入口になる。

## Read this when
- Codex 実行前に INDEX.md を自動更新する preflight の登録・実行順序・commit 作成条件を確認または変更したいとき。
- INDEX.md 作成対象に含めるファイルやディレクトリ、除外する memo・git ignored・binary・symlink・隠し要素の判定を調べたいとき。
- 既存 INDEX.md エントリーの再利用条件、hash の抽出・検証、対象内容の hash 計算、再生成が必要になる条件を追いたいとき。
- Codex へ単一エントリー生成を依頼する引数、実行 root・cwd・config・purpose の扱い、生成結果の schema 検証と Markdown 変換を確認したいとき。
- INDEX.md 更新処理の直列実行、子孫を先に完了させる更新順序、排他 lock の配置や保持範囲を変更する必要があるとき。

## Do not read this when
- INDEX.md エントリーのプロンプト文面や標準文言そのものを変更したいだけなら、プロンプト構築側または正本仕様側を先に読む。
- git コマンド実行、設定読み込み、repo root 解決、hash 計算、binary 判定、git ignore 判定などの低レベル runtime helper の内部挙動を調べたいだけなら、それぞれの runtime 実装を直接読む。
- 個別 CLI コマンドの利用者向け挙動や通常のサブコマンド処理を調べたいだけなら、CLI command 実装側を読む。
- INDEX.md の仕様意図や oracle 上の正本要求を確認したいだけなら、対応する oracle doc を読む。

## hash
- e496278788e2a80a68e74baab4b84fa7282d2799b80502f9f51380678670c648

# `runtime_apply.py`

## Summary
- apply 実行中 process の識別・追跡・停止を扱う runtime 補助実装。session branch から worktree を引く処理、apply branch 名から managed worktree を復元する処理、apply process pid file の読み書きと削除、Codex subprocess group を含む停止制御を担う。
- pid reuse を避けるため pidfd と process start time を使い、壊れた pid file は停止対象にせず、停止失敗や権限不足は CmocError として利用者向けの対処文付きで返す。

## Read this when
- apply abandon、apply cleanup、apply 実行中断、または session ごとの apply process tracking の挙動を変更・調査する。
- apply process pid file の形式、保存場所、lock、stale 判定、削除タイミングを確認する。
- Codex subprocess を process group 単位で停止する処理、pidfd 利用、SIGTERM/SIGKILL の順序、zombie を含む group 終了判定を確認する。
- session branch または apply branch から対応 worktree を特定する runtime 処理を確認する。

## Do not read this when
- 通常の git command 実行 wrapper、worktree root の一般的な path 定義、CmocError 本体など runtime 共通部品そのものを調べたい場合は、それらを定義する runtime 側を読む。
- apply サブコマンドの CLI 引数、状態遷移、利用者向け出力の仕様を確認したい場合は、該当する app spec または command 実装を読む。
- process 停止と関係しない session state の読み書き、agent 呼び出し、merge や commit の処理を調べたい場合は、このファイルではなく該当責務の実装へ進む。

## hash
- f48a64e4dbb0a9f631872914269d3cd2c10db20a575988980f6af5b7a85740ad

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実装。work root 検査、pre-log 処理、サブコマンドログ作成、開始・実行・完了表示、戻り値の終了コード化、例外時のエラー表示、実行時間や quota 待機時間を含む完了サマリー出力を一箇所に集約する。
- 通常の標準サマリーとは別の stdout 契約を持つサブコマンド向けの結果型と、cmoc が work root で実行されている前提を検査する処理も含む。

## Read this when
- CLI サブコマンドの実行前後に共通して行うログ作成、進捗表示、完了サマリー、終了コード処理、例外表示を変更する。
- サブコマンド実装の戻り値を CLI 終了コードや stdout に変換する挙動を確認する。
- init など、runtime state の配置先や pre-log 検査のタイミングが重要なサブコマンドの実行ライフサイクルを調べる。
- cmoc が work root 以外で実行された場合のエラー内容や検査条件を変更する。

## Do not read this when
- 個別サブコマンドの業務処理そのものを変更したいだけで、共通の実行ライフサイクルや表示契約に触れない。
- サブコマンドログの内部フォーマット、イベント記録の保存方法、現在の logger 管理の詳細だけを調べたい場合は、runtime logging 側を直接読む。
- repo root、work root、時刻表示、経過時間整形の解決方法だけを確認したい場合は、runtime paths 側を直接読む。

## hash
- fa9d69da666a38b9545a60975c7d3cd29db49c818a6e4db315962330424ee39e

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
- Codex exec の実行制御を担う実装。単一試行ループを中心に、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、Codex call log と subcommand event の記録を同じ状態機械として扱う。
- TUI 起動や prompt/profile/schema の個別生成そのものではなく、Codex subprocess 呼び出し結果を起点に再試行・検証・ログを統合して扱う入口。

## Read this when
- Codex exec の呼び出し argv、stdin prompt log、stdout/stderr/output/call log の生成や記録条件を確認・変更したいとき。
- Structured Output の JSON 読み取り、schema validation、semantic retry の成功・失敗時挙動を確認・変更したいとき。
- capacity error や quota error の判定後に、再試行、quota polling、代表 probe、resume token 継続がどう制御されるかを確認・変更したいとき。
- Codex call の console 出力、subcommand log event、quota wait 秒数、生成 log path の扱いを追う必要があるとき。

## Do not read this when
- Codex profile、CODEX_HOME、schema file、subprocess 実行 wrapper、Codex エラー判定などの低レベル helper 自体を変更したいだけなら、それらを定義する runtime Codex profile 周辺を直接読む。
- AgentCallParameter を組み立てる prompt builder や acp builder の仕様・実装を確認したいだけなら、該当 builder を直接読む。
- TUI 起動や exec 以外の UI 実行経路を確認したいだけなら、TUI 側の module を読む。
- git command wrapper や repository path helper の一般挙動を確認したいだけなら、runtime git/path の helper を直接読む。
- file access rule の正本仕様や oracle/realization の概念定義を確認したい場合は、対応する oracle doc または oracle src を読む。

## hash
- f25a5241a698cb2a5c1c159f14c32d3a68461d3b1965c0eb199ef78a4f6cc6bf

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し後に、目的・call log path・経過時間・終了コードを利用者の console へ通知するための小さな出力 helper を提供する。
- console 表示の時刻や経過時間の整形は runtime path 系 helper に委ね、この対象は oracle が定める通知ブロックの組み立てと標準出力への即時 flush に責務を絞る。

## Read this when
- Codex CLI call の console 通知内容や表示順を確認・変更したいとき。
- Codex CLI 呼び出しの目的、call log、経過時間、終了コードを利用者へどう出すかを追うとき。
- console log 仕様に対応する実装箇所を探しているとき。

## Do not read this when
- timestamp や duration の具体的な整形規則を確認したいだけのとき。
- call log file の作成、保存場所、書き込み内容を確認したいとき。
- Codex CLI 呼び出しそのものの実行制御や subprocess 処理を調べたいとき。

## hash
- d6c16807d74cfa4ef374c6062dcd9ce3fd7c9464c0d331fb11bf238d5d5d5f6b

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 呼び出しの直前に、登録済みの indexing preflight を挟むための実行ラッパーを定義する。
- preflight の登録・解除、呼び出し起点 root の決定、再入抑止、直列実行、preflight 対象外 purpose の判定を扱う。

## Read this when
- Codex exec または Codex TUI の実行前に INDEX 更新などの事前処理を走らせる経路を確認・変更したいとき。
- indexing preflight の登録、解除、再入防止、スキップ条件、root 決定ロジックを調べたいとき。

## Do not read this when
- Codex 実行本体や TUI 起動処理そのものを確認したいだけのときは、実行本体を持つ runtime 側を読む。
- 作業 root や repo/work root の定義を確認したいだけのときは、runtime path を扱う対象を読む。
- AgentCallParameter や実行結果型の構造を確認したいだけのときは、それぞれの型定義を扱う対象を読む。

## hash
- 51399f811a8fcad100d5ff2c0c6c7556ba46b469a5865173e457f9ee580d21b3

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界で使う profile 生成、sandbox/cwd/write/read path 検査、CODEX_HOME 検証、apply child process tracking、Structured Output schema 配置、Codex JSONL の error/resume 判定をまとめる実装。
- FileAccessMode を Codex CLI が受け取れる実行環境へ変換し、cmoc 側の実行 root・sandbox profile 境界を担う。

## Read this when
- Codex CLI 起動用 profile の内容、sandbox mode、writable_roots、cwd、追加 read/write path の許可判定を確認または変更したいとき。
- CODEX_HOME の解決・検証、profile ファイル生成、Codex subprocess へ渡す環境変数、Codex CLI 不在時のエラー化を扱うとき。
- apply abandon に関係する Codex child process の pid 記録、lock、process group 起動、pid 再利用検出を調べるとき。
- Structured Output schema の保存先配置、Codex output JSON の読み取り、JSONL stdout/stderr からの error detail、resume token、capacity/quota retry 判定を変更するとき。

## Do not read this when
- FileAccessMode そのものの正本定義や prompt 上のファイルアクセス規則を確認したいだけなら、oracle 側の file access rule を読む。
- Codex profile 境界ではなく、cmoc の CLI サブコマンド仕様、設定 schema、git 差分検査、runtime path 定義を調べたいときは、それぞれの担当ファイルへ進む。
- Codex subprocess の起動結果を使う上位フローや retry 全体の制御を追いたいだけなら、呼び出し側の実装を読む。

## hash
- 0b494aabcb9e7f983cd2510fec15e8e8b6d77695d7e888bada9dfb0329eb1492

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを、実行プロファイル作成、作業ディレクトリ決定、call log 記録、実行結果の console/log event 出力、失敗時の cmoc エラー化まで含めて扱う実行入口。
- agent call parameter と runtime config から Codex CLI/TUI 用の profile、CODEX_HOME、実行 cwd、環境変数を組み立て、TUI サブコマンド相当の外部プロセス起動を担う。
- Codex TUI 実行時の call log に残す metadata、実行時間、returncode、logger event payload の生成責務を持つ。

## Read this when
- Codex TUI を起動する実装、引数、cwd、CODEX_HOME、profile 名、file access mode に応じた実行位置を確認または変更したいとき。
- TUI 呼び出しの call log JSON、console 出力、subcommand logger の event 内容、失敗時のエラーメッセージを調べたいとき。
- linked worktree や追加 read path を含む TUI 実行 profile の準備経路を追いたいとき。

## Do not read this when
- Codex exec や非 TUI の agent call 実行経路を調べたいだけのとき。
- profile 作成、CODEX_HOME 解決、file access mode から cwd を決める詳細実装そのものを確認したいとき。
- cmoc の設定読み込み、runtime path 計算、CommandResult、CmocError の一般的な仕様や実装を確認したいとき。

## hash
- 282709994a710f28c42883f934e94c9c2d1ae4a36a91fefc1f755598a316f5e9

# `runtime_config.py`

## Summary
- cmoc の永続化 config JSON と正本 config 型の変換、読み込み、書き込み、初期同期を扱う。
- config の不足項目補完、型検証、enum key map の復元、利用者向け CmocError への変換を担う。

## Read this when
- <repo-root>/.cmoc/config.json の JSON 形式、既定値補完、保存順序、保存時の整形を確認・変更したいとき。
- config 読み込み失敗時や不正値検出時の利用者向けエラー文言・エラー境界を確認・変更したいとき。
- CmocConfig と永続化 JSON object の対応、ModelClass や ReasoningEffort を key にした map の変換を追うとき。
- cmoc init 相当の config 生成・既存 config の現行形式への書き戻し挙動を確認したいとき。

## Do not read this when
- config の正本型や既定値そのものを確認したいだけなら、正本 config 定義を読む。
- config ファイルの配置パス解決だけを確認したいなら、runtime path の責務を持つ対象を読む。
- CLI 引数や個別サブコマンドが config 値をどう使うかを調べたい場合は、そのコマンド実装を読む。

## hash
- c9fc925256fc10765fbd3facd26cba96f606c598ea92625519b04918e0caf273

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
- git コマンド実行を cmoc のエラー形式へ変換する境界と、branch・HEAD・worktree・ignore 状態に関する共通操作をまとめた runtime helper。
- cmoc 管理 branch/worktree の作成・削除制約、clean worktree 要求、.cmoc/local の ignore 初期化・検査、oracle file 判定など、git 状態に依存する実装の入口になる。

## Read this when
- git subprocess の呼び出し結果を利用者向けエラーへそろえる処理を確認・変更したいとき。
- 現在 branch、HEAD commit、未コミット差分、branch 存在確認など、repository 状態の取得・検査に関わる実装を扱うとき。
- cmoc 管理 worktree の作成・削除、管理外 worktree 削除防止、管理 branch namespace の判定を確認したいとき。
- .cmoc/local を git ignore 対象にする初期化・検査、または tracked file と ignored file の扱いを変更したいとき。
- oracle file 判定や git ignore 判定を使うアクセス制御・diff 分類の挙動を追うとき。

## Do not read this when
- CLI 引数定義、表示文言の組み立て、コマンドごとの上位制御だけを確認したいとき。
- git を介さない path model の正本仕様や、path 用語そのものの定義を確認したいとき。
- Codex や LLM への prompt 構築ロジックを確認したいとき。ただし oracle file 判定 helper の利用箇所を追う場合は読む。
- 永続 state file の schema や読み書き形式だけを確認したいとき。

## hash
- 6a378bcabcc734fecb03ff64c0b4c2f9a674ae993ffc3a55d18e79cd22c9a33e

# `runtime_logging.py`

## Summary
- サブコマンド実行単位のログファイルを初期化し、JSON Lines event、経過時間、quota 待機時間、step 実測値を集約する runtime logging 実装。
- 現在の制御文脈から任意参照できるサブコマンド logger を ContextVar で保持し、深い runtime helper からログ記録へ接続する入口を提供する。
- console summary と file log の共有 timing 情報、および console 表示名と JSON Lines 用 step 名を分ける制約を扱う。

## Read this when
- サブコマンド単位のログファイル生成、JSON Lines event の出力、ログレコードの共通 payload、timestamp 付与を確認または変更するとき。
- step 開始・終了、経過秒、quota 待機秒、完了サマリー向け timing 集計の挙動を確認または変更するとき。
- runtime helper から現在のサブコマンド logger を参照する仕組み、または logger の一時差し替えと復元を確認または変更するとき。
- console 表示用の step description と log event 用の step description を分ける必要がある処理を扱うとき。

## Do not read this when
- ログ保存先ディレクトリや時刻文字列の生成規則だけを確認したい場合は、それらを定義する runtime path 側を読む。
- CLI サブコマンドの呼び出し構造、ユーザー向け console 出力文面、または個別サブコマンドの業務処理を確認したいだけの場合。
- 生成済みログファイルの内容調査や実行履歴の確認が目的で、logging 実装自体を変更しない場合。

## hash
- 435c34b19e2277edd8f95d4456eadef464c857b66fc7bca81fa0646e1a77a4f8

# `runtime_paths.py`

## Summary
- 実行時に必要な root 解決、時刻・duration 表示、cmoc 管理領域の保存先 path、memo 判定、短時間の cwd 切替をまとめる共通 utility。
- oracle 側の path model で内部扱いの root resolver を、実行時エラーへ変換して runtime から使える形にする入口でもある。

## Read this when
- 実行中の repository root、worktree root、cmoc root を取得する処理を確認・変更したいとき。
- session、report、log、worktree、schema store、config などの cmoc 管理ファイル・ディレクトリの保存先を確認・変更したいとき。
- console や log に出す timestamp、duration 表示の形式を確認・変更したいとき。
- `<work-root>/memo` 判定や、一時的に cwd を変更して外部 API を呼ぶ処理を確認したいとき。

## Do not read this when
- path placeholder の定義や root path 解決仕様そのものを確認したいときは、oracle 側の path model を読む。
- CmocError の構造や表示仕様を確認したいだけのときは、runtime error を扱う定義を読む。
- 各 sub command 固有の report 内容、session state 内容、log 内容を確認したいときは、それぞれの生成・利用箇所を読む。

## hash
- a3ccc3a7b94c195b2287c300c0ae0edef9578ad3f366c51b4a97a5081416e1ad

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
- runtime path の基準ディレクトリ定義や session directory の組み立てだけを調べたいとき。
- CmocError の表示形式や例外クラス自体の責務を調べたいとき。

## hash
- 639a3107fd6c4d1ad5208798d2042e7bdaa8b70ba12f3984bd72b4432b5dab30
