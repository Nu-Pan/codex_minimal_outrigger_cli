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
- 正本 config 型と永続化 JSON の相互変換、読み込み、保存、未作成時の生成を扱う実行時 config 境界。既定値補完、enum key map の復元、型不正や JSON 不正を利用者向け error に変換する責務を持つ。

## Read this when
- cmoc config の JSON 保存形式、読み込み時の既定値補完、型検証、error message を変更したいとき。
- config の永続化 path から正本 config 型を復元する処理、または既定 config を生成して書き戻す処理を確認したいとき。
- model provider、reasoning effort、apply fork、review oracle などの config section が runtime でどう組み立てられるかを調べるとき。

## Do not read this when
- config 型そのものの項目定義や既定値だけを確認したいとき。正本 config 定義を直接読む。
- config file の配置場所や path keyword の意味だけを確認したいとき。path 解決を担う対象を読む。
- CLI command の引数処理や doctor command 全体の制御を調べたいとき。command 実装を直接読む。

## hash
- 55bd6094b87b350e3efdb837af5e94d484818c2788259f3ba9845c0aec4c8fa1

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
- 共通実行前修復をまとめる実行時処理。ignore 設定、agent 作業領域の追跡可能化、設定同期、cmoc 管理の local SLM 用 ollama 準備、修復差分の commit を扱う。
- cmoc provider を使う model が設定されている場合にだけ、user service として ollama を導入・起動確認し、必要な model を取得可能な状態にする。

## Read this when
- doctor preprocess の実行順序、修復対象、commit 対象、失敗時のエラー内容を確認または変更したいとき。
- cmoc 管理の ollama の導入先、lock、systemd user service、HTTP 起動確認、model pull の挙動を確認または変更したいとき。
- 設定内の cmoc provider model から local SLM の準備対象を決める処理を確認したいとき。

## Do not read this when
- CLI 引数やサブコマンドの定義だけを確認したいとき。
- 設定ファイルの schema、読み書き形式、同期内容そのものを確認したいとき。
- git コマンド実行 wrapper や共通エラー型の基本挙動だけを確認したいとき。

## hash
- f8f2bcf6fb2b439b6adeb2173528b833570d92fb069397befd405c4badd6d4c2

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
- git コマンド実行、branch/HEAD 取得、clean worktree 検査、cmoc 管理 branch/worktree の作成・削除、.cmoc/local の ignore 保証、git ignore 判定、oracle file path 判定を担う runtime helper 群。
- subprocess の git 失敗を利用者向け CmocError または CommandResult にそろえ、cmoc が操作してよい branch namespace と worktree 管理領域を検証する境界として機能する。

## Read this when
- git subprocess 呼び出し、git エラーの CmocError 化、CommandResult の扱いを確認・変更したいとき。
- detached HEAD、現在 branch、HEAD commit、未コミット差分検査、.cmoc/config.json を除外した status 判定に関わる挙動を確認したいとき。
- cmoc が作成する apply/run 用 linked worktree の path 検証、作成、削除、prune、管理外 worktree 削除防止を扱うとき。
- cmoc 管理 branch の namespace 判定、branch 存在確認、branch 削除の失敗を caller 側で warning 化する流れを確認したいとき。
- .cmoc/local を .gitignore または git exclude で追跡対象外にする処理、初期化済み repository の ignore 状態検査、git index からの除外処理を扱うとき。
- git ignore 判定、追跡済みファイルを対象に残すための check-ignore 判定差、oracle file path 判定に関わる runtime 側の共通処理を確認したいとき。

## Do not read this when
- cmoc の path keyword や work-root/run-root/work-root の概念定義そのものを確認したいだけなら、正本仕様側の path model を読む。
- CLI サブコマンドの利用者向け仕様、出力 schema、セッションや apply の業務フローを確認したいだけなら、対応する仕様文書または command 実装を読む。
- git 以外の runtime path、runtime error、runtime result の型定義や責務を確認したいだけなら、それぞれの専用 helper を読む。
- oracle file と realization file の正本定義そのものを確認したい場合は、正本仕様側の oracle/realization 定義を読む。

## hash
- 899a40cfbc8cf5c12fe0f2f55afc203ec87eb1262f30f35a0103fb9b58fcd002

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
