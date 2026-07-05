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
- cmoc の runtime 系 API を単一の入口として再公開する集約モジュール。Codex 起動、profile、設定、content hash、CLI 実行、doctor 前処理、error、git、logging、path、result、state に関する共通実行時要素を各 runtime_* モジュールから取り込む。

## Read this when
- 複数の runtime_* モジュールにまたがる共通 API を、呼び出し側でまとめて import している箇所の依存元を確認したいとき。
- runtime 系 helper の公開入口として、どの関数・型・定数がまとめて提供されているかを確認したいとき。
- 個別 runtime_* モジュールの移動・改名・公開範囲変更により、この集約 import の更新が必要か判断するとき。

## Do not read this when
- Codex profile、git 操作、設定読み書き、path 計算、state 保存などの具体的な処理内容を確認したいときは、それぞれの runtime_* モジュールを直接読む。
- CLI サブコマンドの利用者向け挙動や制御フローを調べたいときは、サブコマンド実装側を読む。
- 新しい runtime 処理を実装したいだけで、この集約入口から公開する必要がまだ決まっていないとき。

## hash
- 19c36c9004dc01f39de717d322a30831b8a1b6e0ded9336a719762767ebdda77

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
- apply 実行に紐づく worktree 特定、apply process の pid file 管理、Codex subprocess 追跡、apply abandon 時の停止処理を扱う runtime 補助実装。
- pidfd、process start time、process group、Linux /proc を使って、PID reuse や zombie を考慮しながら停止対象の同一性確認と signal 送信を行う。
- session branch と apply branch から対応 worktree を解決し、apply 実行中だけ subprocess 追跡先を有効化する入口にもなる。

## Read this when
- apply abandon が実行中 apply process や Codex subprocess group をどう特定・停止するかを確認または変更したいとき。
- apply process pid file の保存形式、読み取り時の壊れた内容の扱い、cleanup 時の削除条件を確認したいとき。
- apply branch 名や session branch から linked worktree を解決する処理を調べたいとき。
- Codex subprocess 追跡用の環境変数と process-local な追跡先設定の関係を変更したいとき。
- pidfd、process start time、process group、/proc を使った process 同一性確認や停止待ちの挙動を調整したいとき。

## Do not read this when
- apply abandon の利用者向け仕様や CLI 出力の正本仕様を確認したいだけなら、対応する oracle doc を読む。
- apply command 全体の CLI 引数、session state 更新、または high-level な制御フローを調べたい場合は、該当する command 実装から読む。
- git command 実行 wrapper、runtime 共通 error、path model、worktree root の基本定義を確認したい場合は、runtime 共通実装や oracle 側の path 定義を読む。
- process 停止とは無関係な session 作成、commit、diff、merge などの apply 周辺処理を調べたい場合は、より直接その責務を持つ実装を読む。

## hash
- d140e6a14473bec52d65e02ccd6c504f7a14b08e0b263dd943a21dcdf9b007b8

# `runtime_cli.py`

## Summary
- CLI サブコマンド実装を共通の実行ライフサイクルに載せるための入口。work root 検査、doctor 前処理、pre-log 検査、サブコマンドログ作成、進捗表示、戻り値の終了コード化、例外表示、完了サマリー出力を一箇所で扱う。
- 標準サマリーとは別の stdout 契約を持つサブコマンド向けの結果型と、CLI が work root で実行されていることを検査する処理も含む。

## Read this when
- 新しい CLI サブコマンドを既存の共通実行形式に接続したいとき。
- サブコマンド開始・実行・完了の表示、サブコマンドログ、終了コード、quota 待機時間、ステップ経過時間の出力契約を確認または変更したいとき。
- サブコマンド例外時のエラー表示先、cmoc_stdout の扱い、typer.Exit への変換を確認または変更したいとき。
- doctor 前処理、pre-log 検査、runtime state の基準 root、サブコマンドログの保存 root の順序や責務を確認したいとき。
- CLI 実行場所が work root であることを要求する制御を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックだけを確認したい場合は、そのサブコマンド実装を直接読む。
- ログファイルの具体的な書き込み形式やイベント保持構造を確認したい場合は、サブコマンドロガーの実装を読む。
- repo root、work root、時刻、経過時間の算出方法だけを確認したい場合は、runtime path 系の実装を読む。
- doctor 前処理の修復内容そのものを確認したい場合は、doctor 前処理の実装を読む。
- エラーメッセージの整形規則だけを確認したい場合は、runtime error 系の実装を読む。

## hash
- ebd7a01ea3d2ee87c492789bd3416cfc94cc2588ff3d969b7f424bb6ba90c267

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
- Codex exec の単一試行ループを中心に、Structured Output 検証、semantic retry、capacity retry、quota 待機と代表 probe、resume 継続、call log/subcommand event 記録を一体で制御する実行制御モジュール。
- Codex CLI 呼び出しに使う profile、schema、cwd、prompt/stdout/stderr/output/call log の生成と、失敗種別ごとの再試行・エラー化を扱う。
- worktree 上の変更 path を git status から absolute path として取得する補助処理も持つ。

## Read this when
- Codex exec 呼び出しの argv、cwd、profile、CODEX_HOME、schema、prompt stdin、実行 log の扱いを確認・変更したいとき。
- Structured Output の必須 JSON 読み取り、schema 検証、semantic retry、capacity retry、quota 待機、quota availability probe、resume token 継続の制御を確認・変更したいとき。
- Codex call の console 出力、subcommand log event、call log JSON、prompt/stdout/stderr/output log の内容や生成タイミングを確認・変更したいとき。
- agent call 後に worktree の変更 path を取得する処理や、untracked directory を file-level path として扱う必要がある箇所を確認したいとき。

## Do not read this when
- TUI 起動や exec 以外の Codex サブコマンド分岐を確認したいとき。
- Codex profile の詳細な生成規則、CODEX_HOME 解決、quota/capacity error 判定、resume token 抽出、output JSON 読み取りの低レベル実装だけを確認したいときは、それらの runtime Codex profile 系の実装を直接読む。
- subcommand logger や runtime path の一般的な定義だけを確認したいときは、それぞれの共通 runtime 実装を直接読む。
- apply fork の仕様全体や requeue の上位制御を確認したいときは、この変更 path 補助だけでなく apply fork 側の実装・仕様を読む。

## hash
- 4254bd141118194fa89f19a067d69c6c1e7ee61d2905e90d11cbe54a5dec7504

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
- Codex CLI を起動するための profile、sandbox、cwd、CODEX_HOME、schema 配置、subprocess 実行、apply child process tracking、Codex JSONL の error 判定をまとめる実行境界。
- cmoc の FileAccessMode と Codex CLI が受け取る実行環境の差分を吸収し、追加 read/write path の許可検査、hashed profile 生成、Codex home 検証、Codex subprocess の失敗を cmoc の利用者向け error へ変換する。
- Codex CLI から返る機械的結果のうち、output JSON 読み取り、stderr と JSONL message の集約、resume token 抽出、capacity/quota error 判定を扱う。

## Read this when
- Codex CLI 起動時の sandbox/profile/cwd/CODEX_HOME/model provider 設定を変更・調査する場合。
- FileAccessMode ごとの追加 read path または writable root の許可境界、oracle conflict 解消時の例外的 write 許可、TUI prompt 読み取り例外を確認する場合。
- apply abandon と連動する Codex child process の pid 記録、lock、終了時削除、pid 再利用対策を扱う場合。
- Structured Output schema の配置、Codex output JSON の読み取り、Codex JSONL からの error text、resume token、capacity/quota 判定を変更・調査する場合。
- Codex CLI 不在、profile 生成失敗、Codex home/auth 不備、追加許可 path 不正を cmoc error としてどう表現するか確認する場合。

## Do not read this when
- Codex に渡す prompt 本文や file access rule の自然言語説明を確認したいだけの場合は、prompt builder 側を読む。
- cmoc config の model や reasoning effort の定義そのものを変更する場合は、config 定義側を読む。
- runtime log directory や schema store directory の path model を確認する場合は、runtime path 管理側を読む。
- oracle file 判定の仕様や git ignore 判定そのものを変更する場合は、runtime git 側を読む。
- Codex CLI 以外の外部コマンド実行や一般的な subprocess wrapper を探しているだけの場合は、この境界ではない。

## hash
- 86a67673b164efa60d67859580415f734e0847f8472159cc3054826b8cde7ac7

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
- cmoc の永続化 config JSON と runtime config 型の変換、読み込み、書き込み、初期同期を扱う。
- 正本 config 型の既定値を基準に不足項目を補完しつつ、人間が編集した JSON の型不正や未定義値を利用者向け CmocError に変換する境界を担う。

## Read this when
- <repo-root>/.cmoc/config.json の読み込み、生成、再書き込み、または不正時エラーを変更する。
- CmocConfig と JSON object の相互変換、既定値補完、enum key や Codex model 設定の復元挙動を確認する。
- cmoc init や設定同期処理から config ファイルがどの形式で保存されるかを追う。

## Do not read this when
- 正本 config 型そのものの field 定義や既定値を確認したい場合は、config 型定義または oracle 側の config 断片を読む。
- config ファイルのパス解決だけを確認したい場合は、runtime path を扱う対象を読む。
- ACP の model class や reasoning effort の概念定義を確認したいだけの場合は、その型を定義する対象を読む。

## hash
- ed2bb2ee956c57cf960d668d8d9aea8eea6a1b843c5035aafa0f9d07b37d8230

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

# `runtime_doctor.py`

## Summary
- 共通実行前の doctor preprocess を担う実装。cmoc 管理領域の ignore 設定、.agents の追跡可能化、cmoc provider 向け local SLM の Ollama 準備、修復差分だけの commit と既存 staged 差分の復元を扱う。
- Git の一時 index を使って doctor 修復差分を user staged hunks から分離し、Ollama は user systemd service、固定 host、model store、/proc による listener 照合で cmoc 管理プロセスとして確認する。

## Read this when
- 実行前修復、doctor preprocess、cmoc 管理ファイルの ignore、.agents の git 追跡、または修復 commit の作成・復元挙動を確認・変更したいとき。
- cmoc provider の model を使う前に Ollama を自動インストール・起動・検証・pull する処理、systemd user service、固定ポートの衝突検出、model store 環境変数を調べたいとき。
- Git index、staged 差分、.cmoc 追跡解除、.gitignore 修復など、ユーザーの既存 staging 状態を壊さずに自動修復を commit する制御を調べたいとき。

## Do not read this when
- 通常の git コマンド wrapper、runtime config の読み込み、CmocError の定義そのものを確認したいだけのときは、それぞれの共通 runtime 実装を直接読む。
- CLI 引数やサブコマンドの定義、doctor コマンドの呼び出し口、ユーザー向け出力形式を調べたいときは、CLI 層または command 層を先に読む。
- Ollama 以外の model provider、LLM 呼び出し本体、prompt 構築、agent 実行制御を調べたいときは、それらの provider・agent 実行系を読む。

## hash
- 86e37269c6ae612c184ea8a95e0549ceb2e19eb2aa6e938b40a042607f54453a

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
- git コマンド実行を cmoc のエラー形式へ変換し、branch・HEAD・status・worktree・branch 削除などの git 操作を共通化する runtime helper。
- .cmoc/local の git ignore 状態を検査・更新し、oracle file 判定や git ignore 判定など、git の追跡・ignore 状態に依存するファイル分類を扱う。
- cmoc 管理 branch namespace と linked worktree の対応を検証し、管理外 worktree の削除を防ぐ安全境界を担う。

## Read this when
- git subprocess の呼び出し、失敗時の CmocError 化、または git コマンド結果の扱いを確認・変更したいとき。
- cmoc の session/run/apply 用 branch や linked worktree の作成・削除・管理領域判定に関わる挙動を確認・変更したいとき。
- .cmoc/local を git 追跡対象外にする処理、.gitignore や git exclude への ignore pattern 追加、初期化済み repository の ignore 検査を扱うとき。
- git status の porcelain 出力から path と status を取得する処理、rename/copy source の扱い、未追跡ファイルの列挙条件を確認・変更したいとき。
- oracle file 判定、git ignored 判定、tracked file と ignore pattern の関係に基づくファイル分類を扱うとき。

## Do not read this when
- cmoc の path keyword や work-root/run-root の概念定義だけを確認したいときは、path model 側を読む。
- CLI subcommand の引数定義、表示文言、上位の実行フローを確認したいだけなら、各 subcommand 実装を直接読む。
- CmocError や CommandResult のデータ構造そのものを確認したいときは、それぞれの runtime error/result 定義を読む。
- oracle file や realization file の正本仕様を確認したいときは、この helper ではなく対応する oracle 文書を読む。

## hash
- 73c3866df657cea05215893e182b3d869328aff8d031cb776f886880a2174d99

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
- session state file の永続化構造と読み書き、cmoc 管理 branch 名からの session_id 抽出、home branch に紐づく active session 探索を扱う。session/apply の state 断片を dataclass で表し、JSON schema 相当の必須 field と許可 state を読み込み時に検証する。

## Read this when
- session state file の JSON 構造、canonical な保存形式、欠落 field や不正 state の扱いを確認したいとき。
- cmoc session branch または cmoc apply branch から session_id を特定する処理や、その失敗時エラーを変更したいとき。
- 現在 branch に対応する session state file の読み込み、書き戻し、または home branch から active session を探す処理を調べたいとき。

## Do not read this when
- runtime 上のディレクトリ配置や sessions directory の場所だけを確認したいときは、runtime paths を扱う対象を読む。
- CmocError の表示形式やエラー出力全体の方針を確認したいときは、runtime errors を扱う対象を読む。
- session/apply 各サブコマンドの CLI 制御フローそのものを変更したいときは、該当する command 実装を読む。

## hash
- d608145646343b8c53fb1f215b685f21693e0ada024aee1bbbd2f2b2abe8961e
