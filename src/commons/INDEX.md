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
- Codex 呼び出し前に INDEX.md を深い階層から再生成し、変更があれば専用 commit として保存する indexing preflight の実装を扱う。
- indexing 対象の directory・child の選別、既存 entry の hash による再利用、entry 生成結果の検証と Markdown への描画、repository 単位の排他 lock をまとめる。

## Read this when
- INDEX.md の自動更新、鮮度判定、entry 再生成、indexing commit の作成に関する実装を確認または変更したいとき。
- INDEX.md に含める対象の除外条件、git ignore・memo・binary・symlink の扱い、directory hash の計算方法を確認したいとき。
- Codex CLI に INDEX.md entry 生成を依頼する preflight 連携、実行 root・cwd・config の渡し方、Structured Output の検証を調べたいとき。

## Do not read this when
- INDEX.md entry に書くべき文章上の基準や prompt 部品そのものを確認したいだけなら、oracle 側の indexing 仕様や prompt builder を読む。
- Codex 実行基盤、config 読み込み、git wrapper、hash 計算、ignore 判定などの共通 runtime 実装を変更したいだけなら、それぞれの定義元を読む。
- 生成済み INDEX.md の個別 entry 内容や、特定 directory のルーティング判断を確認したいだけなら、その directory の INDEX.md または対象本文を読む。

## hash
- dacc5d7428ac22757c3c87ba8deac1328124e8779fa43df5a9b81834e19665a1

# `runtime_apply.py`

## Summary
- apply 実行に関わる linked worktree の特定、apply process pid file の保存・読取・削除、Codex subprocess 追跡環境の一時設定、apply abandon 時の停止処理を担う runtime 補助実装。
- pid 再利用を避けるため process start time と pidfd を使って停止対象の同一性を確認し、Codex subprocess は process group 単位で停止する。

## Read this when
- apply branch から managed worktree を復元する処理、または session branch が checkout された linked worktree を探す処理を確認・変更したいとき。
- apply process の pid file の保存形式、破損時の扱い、削除タイミング、process tracking 用環境変数の復元挙動を確認・変更したいとき。
- apply abandon が実行中 apply process や Codex subprocess group をどの順序・条件・signal で停止するかを確認・変更したいとき。
- pidfd、process start time、Linux /proc、process group、zombie process を使った停止対象の安全確認や警告生成を扱うとき。

## Do not read this when
- apply の CLI 引数、session state schema、出力文言全体、または subcommand の高レベル制御だけを確認したいとき。
- git worktree の一般的な作成・削除処理や session 管理の永続状態全体を確認したいとき。
- Codex CLI 呼び出しそのもののコマンドライン構築、プロンプト生成、または LLM 出力処理を確認したいとき。
- process 停止と関係しない runtime 共通関数、git command wrapper、path model の定義を確認したいとき。

## hash
- 560d83c54153af00482520b92b6a5d9fd4bc5289777b59ed22976f848c21f8b0

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
- Codex exec の実行制御を担う。単一試行ループ内で prompt/call/stdout/stderr/output の記録、Structured Output 検証、semantic retry、capacity retry、quota 待機と代表 probe、resume 継続、subcommand event 発行を同じ状態機械として扱う。
- agent call 後の file access 事後検証を行わない互換 API と、git status 由来の worktree 変更 path 取得も含む。

## Read this when
- Codex CLI を `exec` で呼び出す処理、実行時 profile/cwd/CODEX_HOME/schema の扱い、または Codex call log の生成内容を確認・変更したいとき。
- Structured Output の読み取り失敗や schema 検証失敗を semantic retry として扱う条件を確認・変更したいとき。
- capacity error、quota error、quota availability probe、resume token、複数 caller 間の quota polling 共有を扱う挙動を確認・変更したいとき。
- Codex call の console 出力、subcommand log event、quota wait 時間や poll 回数の記録を確認・変更したいとき。
- agent call 後の file access 事後検証を無効化している互換 API、または worktree の変更 path 列挙を確認・変更したいとき。

## Do not read this when
- TUI 起動や exec 以外の Codex 起動経路を確認したいだけのとき。
- Codex profile、schema file、Codex home、resume token 抽出、quota/capacity error 判定などの個別 helper の実装詳細を確認したいときは、それぞれの runtime helper 側を直接読む。
- CLI サブコマンド固有の仕様や prompt 構築内容を確認したいときは、対象サブコマンドや prompt builder 側を読む。
- git の低レベル実行 wrapper そのものや path model の定義を確認したいだけのとき。

## hash
- ab354246a8c6a03dc23464d07229185c1fa3c4c7737ee0733f9e23b5769eaf0e

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
- Codex exec/TUI 呼び出しの直前に、登録済みの indexing preflight を必要時だけ実行してから実行本体へ委譲する薄い境界層。
- preflight の登録・解除、再入抑止、直列化、Codex 呼び出し設定から indexing 起点 root を決める処理を扱う。

## Read this when
- Codex exec/TUI 実行前に INDEX 更新などの preflight を挟む条件や順序を確認・変更したいとき。
- preflight の登録解除 API、テスト向け無効化、再入防止、ロックによる直列実行の挙動を確認したいとき。
- Codex 呼び出し時の cwd/root と parameter cwd から、どの work root を indexing 対象にするかを確認・変更したいとき。

## Do not read this when
- Codex exec/TUI の実行本体、外部コマンド起動、結果オブジェクトの詳細を確認したいとき。
- agent call parameter の定義や run_indexing_preflight フラグ自体の仕様を確認したいとき。
- work root や repo root の一般的なパス解決規則を確認したいとき。

## hash
- 89a645a3eedc934ea16a6574c988bd0653ef220cfb48d418483de39768176610

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界で必要になる profile 生成、sandbox writable/read path 検証、CODEX_HOME 解決と事前検査、hashed profile/schema 配置、Codex child process tracking、JSON/JSONL 出力からの error・quota・capacity・resume token 判定をまとめる。
- FileAccessMode を Codex CLI が受け取れる sandbox/profile 設定へ変換し、cmoc の禁止領域や oracle/realization 書き込み境界を subprocess 起動前に反映する責務を持つ。
- apply abandon 用の child process pid file ロック・記録・削除も扱い、Codex CLI 起動から戻り値解釈までの機械的な実行境界を一箇所で読む入口になる。

## Read this when
- Codex CLI に渡す profile 本文、profile 名、sandbox_mode、writable_roots、追加 read/write path の許可判定を確認・変更したいとき。
- FileAccessMode と Codex CLI sandbox の対応、oracle file や AGENTS.md/INDEX.md/memo/.git/.agents/.codex などの書き込み禁止境界を実装上で追いたいとき。
- CODEX_HOME の解決、auth.json を含む Codex home 事前検査、Codex subprocess に渡す環境変数の扱いを確認したいとき。
- Codex CLI 不在時の CmocError 化、subprocess.run/Popen の呼び出し境界、apply 実行中の child process tracking と abandon 連携を調べたいとき。
- Structured Output schema の hash store 配置、schema なし output JSON の読み取り、Codex JSONL stdout/stderr から error detail・capacity retry・quota retry・resume token を判定する処理を変更したいとき。

## Do not read this when
- AgentCallParameter や FileAccessMode 自体の定義、利用者向け file access rule 文面、prompt 構築部品の正本断片を調べたいだけなら、それぞれの定義・oracle 側を読む。
- logs directory や schema store directory など runtime path の場所決定だけを確認したい場合は、path helper を直接読む。
- Codex CLI へ渡す prompt 本文、会話制御、agent call 全体の orchestration、サブコマンド固有の流れを調べたい場合は、その呼び出し元や対象サブコマンドの実装を読む。
- CmocError の表示形式や runtime error 共通処理を確認したいだけなら、error helper を読む。

## hash
- 5167e215e6485bd2fa8090eda48b80586c389a666011a34a678ab8f803a3f28d

# `runtime_codex_tui.py`

## Summary
- Codex TUI 起動用の runtime 処理を扱う。agent call parameter、設定、profile、CODEX_HOME、call log を組み合わせて Codex CLI/TUI を実行し、実行結果の console 表示・subcommand logger へのイベント記録・失敗時の CmocError 化までを担当する。

## Read this when
- Codex TUI 呼び出し時の作業ディレクトリ決定、profile 作成、CODEX_HOME 解決・検証、call log 出力、実行後ログ通知、失敗時エラー化の挙動を確認または変更したいとき。
- AgentCallParameter.cwd が対象 work root 外を指す場合の補正、linked worktree 実行時の root と work root の使い分け、extra read paths を TUI profile に渡す流れを追いたいとき。
- Codex subprocess の argv、cwd、env、check 指定、戻り値や CalledProcessError の扱いを TUI 経路で確認したいとき。

## Do not read this when
- Codex TUI ではなく exec や他の subcommand の仕様・実装を調べたいとき。
- profile 名生成、profile ファイル作成、CODEX_HOME 解決、subprocess 実行そのものの低レベル実装だけを調べたいときは、それらを提供する runtime codex profile 側を読む。
- repo root、work root、log directory、timestamp などの path 解決 helper 自体を調べたいときは、runtime paths 側を読む。

## hash
- 66eca5f1c8be9fea27b0322e9f2cda67c3731f9f1b845cf8977ea7f41894371d

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
- 実行時に必要な root path 解決、時刻文字列、duration 表示、cmoc の local state/config/log/report/schema/worktree 保存先 path、memo 判定、短時間の cwd 変更をまとめる runtime 用 path utility。
- 正本側の path resolver を runtime error に変換して扱い、CLI 実行前提に合わない cwd や cmoc root 解決失敗を利用者向けの CmocError として返す入口になる。

## Read this when
- 実行中の repository root、worktree root、cmoc root を解決する処理を確認・変更するとき。
- session、report、sub_command log、Codex call log、worktree、schema store、config JSON など、.cmoc local 配下の保存先 path を確認・変更するとき。
- 利用者向け時刻表示、file name 用 timestamp、duration 表示の形式を確認・変更するとき。
- memo 配下判定や、一時的に cwd を差し替える処理の挙動を確認・変更するとき。

## Do not read this when
- path placeholder の定義や root resolver の正本仕様を確認したいだけなら、oracle 側の path model を直接読む。
- 個別サブコマンドの実行手順、出力 schema、report 内容、session state の中身を調べたい場合は、それぞれの command 実装や state 管理の対象へ進む。
- CmocError の構造や表示形式そのものを変更したい場合は、runtime error 定義を直接読む。

## hash
- 48f612d340a45bf5d137635a4caadb23384a661da842f554fe82e50c97e40931

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
