# `__init__.py`

## Summary
- cmoc の実行時に複数箇所から共有される補助機能をまとめる領域の入口。
- 対象そのものは共有 runtime helper 群のパッケージ境界を示すだけで、個別 helper の責務は下位要素の本文で確認する。

## Read this when
- cmoc の実行時処理で、複数モジュールから使う共通 helper の配置場所や入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime helper 用のまとまりであることを確認したいとき。

## Do not read this when
- 特定の helper の実装、入出力、失敗時挙動を確認したいとき。この対象ではなく、該当する下位要素の本文を読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共有 runtime helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- 実行時共通機能を単一の import 入口に集約する再公開モジュール。Codex 実行、プロファイル、設定、内容ハッシュ、CLI 実行、doctor 前処理、エラー、git 操作、ログ、パス、結果型、状態管理にまたがる runtime API をまとめて参照するための窓口。

## Read this when
- 複数の runtime 系モジュールから提供される関数・型・定数を、呼び出し側でまとめて import したい箇所を確認する。
- 既存コードが runtime 共通 API をどの公開入口から参照しているかを調べる。
- runtime 系モジュールの再公開対象を追加・削除する必要があり、集約 import の表面を確認する。

## Do not read this when
- 個々の runtime API の挙動、引数、失敗時処理、永続状態の詳細を確認したい場合は、対応する各 runtime モジュールを直接読む。
- 新しい runtime 機能を実装する場合は、この集約入口ではなく責務に対応する実装モジュールを読む。
- CLI サブコマンド固有の処理やテスト対象の外部挙動を確認したい場合は、該当するサブコマンド実装またはテストを読む。

## hash
- 19c36c9004dc01f39de717d322a30831b8a1b6e0ded9336a719762767ebdda77

# `indexing.py`

## Summary
- Codex 呼び出し前の indexing preflight を登録・実行し、排他制御下で各階層の INDEX.md を再生成して必要な更新 commit を作る実装を扱う。
- indexable な directory・child の列挙、既存 entry の hash 検証と再利用、Codex による不足 entry 生成、Structured Output からの entry Markdown 描画までを担う。

## Read this when
- INDEX.md の自動更新、鮮度判定、hash 形式、entry の再生成条件、または indexing commit の作成挙動を変更したいとき。
- indexing 対象から除外する file・directory、binary・symlink・memo・git ignored の扱い、または directory traversal の条件を確認したいとき。
- Codex に INDEX.md entry 生成を依頼する入力内容、実行時の root・cwd・config・purpose、または生成結果の検証エラーを調べたいとき。
- 既存 INDEX.md entry の parse、必須 section 構造、bullet-only 制約、hash 抽出条件に関する不具合を調査するとき。

## Do not read this when
- INDEX.md entry の自然言語生成プロンプトや Structured Output schema の正本側定義だけを確認したいときは、oracle 側の prompt builder や indexing 仕様を直接読む。
- 通常の CLI コマンド引数、設定ファイル全体、または Codex 実行基盤そのものを調べたいだけなら、それぞれの担当 module を読む。
- 個別の INDEX.md 文面を人間がどう書くべきかの方針を確認したいだけなら、この実装ではなく indexing 標準や entry standard の正本仕様を読む。

## hash
- dacc5d7428ac22757c3c87ba8deac1328124e8779fa43df5a9b81834e19665a1

# `runtime_apply.py`

## Summary
- apply 実行に対応する worktree と apply process 追跡状態を扱う runtime 補助コード。session branch から linked worktree を探す処理、apply branch 名から managed worktree path を復元する処理、apply process の pid file 読み書き、Codex subprocess group を含む停止処理をまとめる。

## Read this when
- apply 実行中 process の記録、追跡、削除、停止、または abandon 時の停止安全性を確認・変更したいとき。
- session branch や apply branch から worktree path を特定する runtime 処理を確認・変更したいとき。
- pid 再利用、pidfd、process start time、process group、zombie child を考慮した process 停止ロジックを確認したいとき。

## Do not read this when
- apply の CLI 引数、出力文言、状態遷移そのものを確認したいだけなら、subcommand 側または対応する app spec を先に読む。
- 汎用的な git 実行、worktree 置き場、process start time 取得、pid file lock の実装を確認したい場合は、それらを定義する runtime 基盤へ進む。
- apply と無関係な session 管理、prompt 構築、通常のファイル操作を調べる場合は読まなくてよい。

## hash
- d140e6a14473bec52d65e02ccd6c504f7a14b08e0b263dd943a21dcdf9b007b8

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実装。work root 検査、サブコマンドログの開始・完了記録、doctor preprocess、標準の進捗・完了サマリー、終了コード変換、例外時のエラー表示とログ記録をまとめて管理する。
- 標準サマリー以外の stdout 契約を持つサブコマンドが、終了コードと追加 stdout を返すための小さな結果型も定義する。

## Read this when
- CLI サブコマンド実装を共通 runner に接続する方法、戻り値から終了コードや stdout が決まる経路、例外時の表示先や終了処理を確認したいとき。
- サブコマンドログ、doctor preprocess、work root 実行前提、開始・実行・完了のコンソール表示、quota 待機時間を含む完了サマリーの挙動を変更または調査するとき。
- サブコマンド固有の事前検査を、ログ作成後かつ本処理前に実行する流れを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務処理そのもの、引数定義、または command ごとの Typer 登録だけを確認したいとき。
- runtime path の検出規則、ログファイルの具体的な保存形式、doctor preprocess の修復内容、エラー文面の構成だけを調べたいときは、それぞれの責務を持つ実装へ直接進む。
- 正本仕様断片の記述内容そのものを確認したいときは、対応する oracle doc を読む。

## hash
- 6349ae3b90ca5082d2f1c9c251aab80cf42f80ff7a6dee3b471494a1bf705a73

# `runtime_codex.py`

## Summary
- Codex 実行系の公開入口をまとめる薄い再エクスポートモジュール。exec 実行と TUI 実行の起動関数を同じ import 元から参照できるようにする。

## Read this when
- Codex 実行ランタイムの利用側で、exec 実行または TUI 実行の起動関数をどこから import するか確認したいとき。
- 実行方式ごとの実装詳細ではなく、runtime_codex 系の公開 API 境界だけを確認したいとき。

## Do not read this when
- exec 実行の具体的な処理、引数処理、プロセス制御を確認したいときは、exec 実行側の実装を直接読む。
- TUI 実行の具体的な処理、端末制御、対話実行の挙動を確認したいときは、TUI 実行側の実装を直接読む。
- 新しい実行ロジックや分岐を追加する場所を探しているときは、この再エクスポートではなく各実行方式の実装へ進む。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex exec の実行制御を担い、prompt/call/stdout/stderr/output log の保存、Structured Output 検証、semantic retry、capacity retry、quota 待機と代表 probe、resume 継続、実行後の file access 差分検査を一体の状態機械として扱う。
- TUI 起動など exec 以外の分岐は別責務に分け、subprocess 結果、call log、subcommand event、retry counter、resume token を共有する exec 実行制御の文脈だけをまとめて読む入口である。

## Read this when
- Codex exec 呼び出しの argv、cwd、profile、CODEX_HOME、schema、stdin prompt log、call log の生成条件や記録内容を確認・変更したいとき。
- Structured Output の読み取り、JSON schema 検証、semantic retry の失敗条件や再試行挙動を確認・変更したいとき。
- capacity error や quota error に対する retry、quota polling、代表 probe、待機中の他スレッド連携、resume token の扱いを確認・変更したいとき。
- Codex call 後に FileAccessMode の禁止差分を検出する事後チェック、変更 path の署名化、許可 path 判定を確認・変更したいとき。
- subcommand log や console へ Codex call の成功・失敗・待機・retry event をどう記録するかを確認・変更したいとき。

## Do not read this when
- Codex profile の具体的な生成規則、sandbox 設定、schema ファイル準備、Codex CLI stdout/stderr からの error 判定そのものを調べたいだけのときは、それらの runtime helper を直接読む。
- AgentCallParameter の構造、prompt の組み立て、quota probe 用 parameter の内容を調べたいときは、それぞれの定義や builder を直接読む。
- TUI 起動、exec 以外のサブコマンド本体、設定ファイルの読み込み仕様、git status helper の内部実装を調べたいだけのときは、該当する別責務の対象を読む。

## hash
- ddb16c816697e2d48624800a0301d7991228d8fc9ef0f896f66edb9b3a7fa938

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しの完了情報を利用者向け console に出力する小さな実装。目的、呼び出しログの場所、経過時間、終了コードを、既存の時刻・期間フォーマットを使って整形して表示する。

## Read this when
- Codex CLI 呼び出し後に console へ表示する通知内容や表示順を確認・変更したいとき。
- Codex CLI 呼び出し通知で、目的、呼び出しログ、経過時間、終了コードをどのように利用者へ見せているか確認したいとき。
- console 通知の時刻や経過時間が、共通の実行時フォーマット処理とどう接続しているか確認したいとき。

## Do not read this when
- Codex CLI 呼び出しそのものの実行制御、引数構築、プロセス管理を調べたいとき。
- 呼び出しログファイルの生成・保存・更新の実装を調べたいとき。
- 時刻文字列や経過時間文字列の共通フォーマット規則そのものを変更したいとき。

## hash
- d6c16807d74cfa4ef374c6062dcd9ce3fd7c9464c0d331fb11bf238d5d5d5f6b

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行の直前に登録済みの INDEX 更新 preflight を挟むための薄い委譲層。preflight の登録・解除、実行起点 root の決定、再入抑止と直列化を扱い、実際の Codex 実行は runtime 側へ渡す。

## Read this when
- Codex exec/TUI 呼び出し前に indexing preflight が実行される条件や順序を確認したいとき。
- run_indexing_preflight、cwd、root、parameter.cwd から preflight の起点 root がどう決まるかを調べたいとき。
- indexing preflight の登録解除、再入防止、ロックによる直列実行の挙動を変更したいとき。

## Do not read this when
- Codex exec/TUI の実行本体、サブプロセス実行、戻り値の組み立てを調べたいときは runtime 実行側を読む。
- repo root や work root の判定規則そのものを調べたいときは path 解決を担う runtime path 側を読む。
- AgentCallParameter の項目定義や run_indexing_preflight の意味を確認したいときは basic 側の parameter 定義を読む。

## hash
- 21640496726fe5b154993e3215648edd155e6984b8fcb368ada7a22845c04670

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界で使う profile 生成、sandbox/permission profile の読み書き許可 root 計算、CODEX_HOME 検証、schema 配置、child process tracking、JSONL error 判定をまとめる実装。
- FileAccessMode を Codex CLI 起動設定と実行後検証用の書き込み許可判定へ変換し、追加 read/write path が cmoc の許可境界を広げないよう検査する。
- Codex CLI の実行環境準備と実行結果解釈に閉じた責務を持ち、apply abandon 用の child process pid 記録や capacity/quota retry 判定もこの subprocess 境界の一部として扱う。

## Read this when
- Codex CLI に渡す profile、sandbox mode、permission profile、writable/readable root の決まり方を確認または変更するとき。
- FileAccessMode ごとの読み取り・書き込み許可境界、追加 read/write path の検証、oracle conflict 解消時の例外的な書き込み許可を調べるとき。
- CODEX_HOME の解決・検証、hashed profile の生成、cmoc 管理 Ollama provider 設定、schema store への Structured Output schema 配置を扱うとき。
- Codex subprocess の起動失敗、apply 実行中の child process tracking、pid file lock、pid 再利用検出、abandon との同期を確認するとき。
- Codex JSONL stdout/stderr から利用者向け error detail、resume token、capacity error、quota error を抽出する挙動を変更するとき。

## Do not read this when
- CLI subcommand の利用者向け仕様、prompt 本文、または FileAccessMode の自然言語ルールそのものを確認したいだけの場合は、対応する oracle 側の仕様断片を読む。
- Codex subprocess 境界ではなく、実行後の git 差分検証、path model、runtime log 保存、または config 定義を調べる場合は、それぞれの責務を持つ別実装へ進む。
- 個別コマンドの制御フローや agent call 全体の orchestration を追う場合は、この実装ではなく呼び出し元の command/session/apply 系の実装を読む。
- Structured Output schema の内容や JSON schema 自体を確認したい場合は、この実装ではなく schema の生成元または呼び出し側を読む。

## hash
- 4ceaff6f5335f351684de1ffff98b1c62d8e7b6ec9a04d48342296c1e31afc30

# `runtime_codex_tui.py`

## Summary
- Codex TUI 起動用に、対象 cwd の補正、Codex home/profile 準備、call log 記録、subprocess 実行、実行結果の console/logger 通知、失敗時の cmoc 向け例外化をまとめる。

## Read this when
- Codex TUI を起動する処理、profile 作成、Codex home 検証、call log の内容、実行 cwd の決定、TUI 呼び出し失敗時の扱いを確認・変更したいとき。
- AgentCallParameter の cwd が対象 work root 外を指す場合の補正挙動や、linked worktree 実行時の root/work root の使い分けを確認したいとき。
- Codex 呼び出しの elapsed time、returncode、profile 情報を console 出力または subcommand logger event に渡す流れを追いたいとき。

## Do not read this when
- Codex subprocess 実行、profile 名解決、Codex home 解決、環境変数構築そのものの詳細を確認したいだけなら、それらを提供する runtime Codex profile 側を読む。
- runtime path の定義、timestamp、repo root、work root、log directory の算出規則を確認したいだけなら、path utility 側を読む。
- TUI 以外のサブコマンド仕様、設定ファイルの読み込み規則、AgentCallParameter の構造を確認したいだけなら、それぞれの定義元を読む。

## hash
- 66eca5f1c8be9fea27b0322e9f2cda67c3731f9f1b845cf8977ea7f41894371d

# `runtime_config.py`

## Summary
- cmoc の永続化 config JSON と runtime の正本 config 型を相互変換し、config ファイルの読み込み・生成・現在形への書き戻しを行う。
- JSON の section・enum key map・model spec・int 値を検証し、不正な利用者編集を CmocError の利用者向けメッセージへ変換する。
- config 保存先は runtime path helper から得て、未作成時は既定 config を生成し、既存時は不足値を補完した安定 JSON 表現で保存し直す。

## Read this when
- cmoc config JSON の読み込み、初期生成、同期、保存形式、既定値補完の挙動を確認または変更したいとき。
- CmocConfig、CmocConfigCodex、apply_fork、review_oracle、Codex model spec、reasoning effort の永続化 JSON 表現を扱うとき。
- 不正な config JSON、欠落 section、型違い、空文字、未知 enum key、JSON 構文 error に対する CmocError 境界を確認したいとき。

## Do not read this when
- config 値そのものの正本定義、既定値、model class、reasoning effort、Codex model spec の意味を確認したいだけなら、正本 config 型や oracle 側の定義を読む。
- config ファイルのパス規則だけを確認したいなら、runtime path helper を読む。
- CLI command の引数処理、doctor 実行フロー、agent orchestration 側で config 値をどう使うかを調べたい場合は、それぞれの呼び出し元を読む。

## hash
- 1120d55ea7a5a55ce14b73f76f472319f67fe3da04ee9717c70ebf73e14deeda

# `runtime_content.py`

## Summary
- ファイル内容または文字列内容から SHA-256 digest を計算し、digest をファイル名に含めた内容アドレス型ファイルを書き出す小さな runtime content helper 群。
- 出力先 directory の作成有無が異なる 2 種類の書き出し関数と、先頭 chunk の NUL byte と読み取り可否による簡易 binary 判定を扱う。

## Read this when
- 内容 hash を使った成果物ファイル名の生成、重複書き込み回避、または内容アドレス型の一時・補助ファイル保存を確認・変更するとき。
- ファイル内容や文字列内容の SHA-256 digest 計算処理を使う箇所を探すとき。
- テキスト対象と binary 対象を粗く分けるための簡易判定ロジックを確認・変更するとき。

## Do not read this when
- path model、run/work/root の意味、またはパス表記そのものの仕様を確認したいとき。
- CLI 引数、サブコマンド、標準出力、終了コードなど利用者向けの公開面を確認したいとき。
- hash 値を使わない通常のファイル読み書き、設定読み込み、永続状態管理の実装を探しているとき。

## hash
- 327f8182b1ab2047a3f5f70e49d2feb4fba2029da38769d649f9ed82f4175106

# `runtime_doctor.py`

## Summary
- 共通実行前の doctor preprocess を担当し、cmoc ignore、.agents の追跡確保、Ollama ローカル SLM 確認を行ったうえで、doctor 修復差分だけを専用の一時 git index で commit する処理をまとめる。
- user の staged hunks や通常 index を壊さないよう、現在 index の復元用 tree と HEAD 起点の repair commit 用 index を分けて扱い、.gitignore、.agents/.gitkeep、.cmoc/local の追跡解除を doctor 修復として合成する。

## Read this when
- cmoc コマンド実行前に行う自動修復、doctor preprocess、または repair commit の挙動を確認・変更したいとき。
- user の staged 変更を保持したまま .gitignore や .agents の修復だけを commit する制御を調べたいとき。
- .cmoc/local を git index から外す処理、GIT_INDEX_FILE を使った一時 index 操作、または git 失敗時の CmocError 化を確認したいとき。

## Do not read this when
- cmoc ignore パターンそのものの文字列生成や git コマンド wrapper の基本挙動だけを調べたい場合は、対応する runtime git 側を直接読む。
- Ollama がローカル SLM を提供しているかの判定・起動確認だけを調べたい場合は、Ollama runtime 側を直接読む。
- CLI 引数、サブコマンド構成、または doctor 以外の通常実行フローを調べたい場合は、それらを担当する上位 CLI 実装から読む。

## hash
- 1b7e438f300d8227644fcf78a79203dc3cb53fd1c8409d0dca19d84deead08c3

# `runtime_errors.py`

## Summary
- cmoc の実行時例外と、任意の例外を利用者向け Markdown エラーレポートへ変換する共通処理を定義する。エラー概要、復旧案、詳細、呼び出しスタックを一貫した形式で出力するための入口となる。

## Read this when
- 利用者に表示する cmoc 共通エラーレポートの構成や文面を確認・変更したいとき。
- 実装内で発生させる利用者向け例外に、概要・復旧案・詳細を持たせる方法を確認したいとき。
- 例外ごとの復旧案が少ない場合に既定の Next actions がどう補われるかを確認したいとき。

## Do not read this when
- 個別コマンド固有のエラー判定条件や入力検証ロジックを調べたいとき。
- エラーレポートを出力する CLI エントリーポイント側の制御を調べたいとき。
- Markdown エラーレポート以外の通常出力や成功時出力の形式を調べたいとき。

## hash
- 51eb58dfc241cb76b6debfce4a06a3169cb6a2a29d0a6f123f7c5b6c0bd03e95

# `runtime_git.py`

## Summary
- git subprocess 実行を利用者向けエラーへ変換する境界と、branch・HEAD・status・worktree・ignore 判定を扱う runtime helper 群。
- cmoc 管理 branch namespace、run/apply 用 linked worktree の作成・削除安全確認、`.cmoc/local` の git ignore 初期化・検査、oracle file 判定を担う。

## Read this when
- git コマンド呼び出しの失敗時挙動、戻り値、利用者向けエラー化を確認・変更したいとき。
- 未コミット差分の検査、porcelain status の path 取得、rename/copy path の扱いを確認したいとき。
- cmoc が管理する branch 名、run/apply 用 worktree path の対応、worktree 作成・削除の安全条件を確認したいとき。
- `.cmoc/local` を `.gitignore` または git exclude で追跡対象外にする処理や、その初期化済み検査を確認したいとき。
- git ignore 判定、tracked file と ignore pattern の関係、oracle file path 判定を扱う実装を確認したいとき。

## Do not read this when
- path keyword の概念定義そのものを確認したいだけなら、oracle 側の path model を読む。
- CLI サブコマンドの入出力仕様や利用者向け workflow を確認したいだけなら、該当する app spec を読む。
- runtime path のディレクトリ構成や `.cmoc/local` 配下の具体的な path 組み立てだけを確認したいなら、runtime paths 側を読む。
- CommandResult や CmocError の型・表示形式だけを確認したいなら、それぞれの runtime result/error 定義を読む。

## hash
- bfcce2aa66615b98cf1af9b07e665542bf19bea772bd5200bddac41b3ad4b98a

# `runtime_logging.py`

## Summary
- サブコマンド単位の実行ログと実測時間を扱う runtime logging 実装。JSON Lines event の追記、step 開始・終了 timing、quota 待機時間の集計、現在の logger を context local に差し替えて参照する仕組みを提供する。

## Read this when
- サブコマンド実行中に記録される JSON Lines log event の生成内容、保存単位、timestamp 付き log file の作成方法を確認したいとき。
- console summary と file log で共有される step timing、elapsed time、quota wait time の集計方法を確認または変更したいとき。
- 深い runtime helper から現在のサブコマンド logger を参照する context variable の設定・復元・取得経路を扱うとき。

## Do not read this when
- log directory のパス規則や timestamp 文字列の生成規則だけを確認したいときは、それらを定義する runtime path 側を読む。
- 個別サブコマンドの処理順序や step の文言そのものを確認したいときは、そのサブコマンド実装を読む。
- oracle 上の console 表示・file log 仕様や coding rule の正本内容を確認したいときは、対応する oracle doc を読む。

## hash
- 435c34b19e2277edd8f95d4456eadef464c857b66fc7bca81fa0646e1a77a4f8

# `runtime_ollama.py`

## Summary
- cmoc provider の model を local SLM として使うため、管理対象 Ollama の導入、systemd user service 起動、固定 endpoint 検証、model pull をまとめて行う runtime 実装。
- config から cmoc managed 対象 model を抽出し、~/.cmoc/ollama 配下の executable・model store・lock と 127.0.0.1:11434 の service 実体を扱う。
- Ollama archive 取得、service file 同期、systemctl 実行、/proc による listener と process 系列の照合、HTTP 疎通確認、ollama command 実行失敗時の CmocError 化を含む。

## Read this when
- cmoc provider の model を実行前に local Ollama で serve 可能にする処理を確認・変更したいとき。
- managed Ollama の install 先、model store、systemd user service、固定 host/port、process lock、model pull の挙動を調べるとき。
- 127.0.0.1:11434 の listener が cmoc managed Ollama 由来かどうかの検証、/proc 読み取り、systemctl や ollama command の失敗時エラーを扱うとき。
- config 内の model provider から cmoc managed 対象 model 名を重複排除して取り出す処理を確認するとき。

## Do not read this when
- runtime 設定ファイルそのものの schema、読み込み、保存場所の定義を調べたいだけなら、設定や path を担当する対象を読む。
- cmoc provider 以外の model provider の選択、Codex 設定全体、agent 呼び出し制御を調べたいだけなら、呼び出し側や設定変換を担当する対象を読む。
- Ollama 自体の一般的な仕様や model の品質、LLM 出力内容を調べたいだけなら、この runtime 実装は入口ではない。

## hash
- 26c5a3a7377c2caffd20dc4b952f1a5d037be22a7a67006ca200a3ac01e0b45e

# `runtime_paths.py`

## Summary
- 実行時に必要な root path 解決、時刻文字列、duration 表示、cmoc 管理ディレクトリや設定ファイルの path 組み立て、cwd 一時変更、memo 配下判定を扱う runtime path helper 群。
- root 解決失敗時は `CmocError` に変換し、利用者が実行場所を直せるメッセージを返す責務を持つ。

## Read this when
- 実行時の `<repo-root>`、`<work-root>`、`<cmoc-root>` 解決や、その失敗時エラー文言を確認・変更したいとき。
- `.cmoc/local` 配下の session、report、log、worktree、schema、config の保存先 path を確認・変更したいとき。
- file name 用 timestamp、console 表示用 timestamp、duration 表示形式を確認・変更したいとき。
- `<work-root>/memo` 自体または配下の判定、または cwd 前提 API を呼ぶ短い区間の作業 directory 切替を扱うとき。

## Do not read this when
- placeholder 名や実 path 変換の正本定義そのものを確認したいだけなら、path model 側を読む。
- 個別サブコマンドの report、log、session state の中身や schema を確認したいだけなら、それぞれの保存・読み書き処理へ進む。
- CLI 引数解析、コマンド実行制御、利用者向け出力全体の仕様を確認したいだけなら、該当する command 層へ進む。

## hash
- af9e2b9db9e0c790c7f08af804841b073dd6cd5ef99ca122152ad4a3387c78d3

# `runtime_preprocess_command.py`

## Summary
- doctor preprocess、config 同期、config 差分の git commit、見出し出力をまとめて実行する CLI 前処理サブコマンド用の実行入口。
- runtime path 解決、doctor 前処理、config 同期、git add/diff/commit を既存 runtime helper 経由で連結し、通常の CLI サブコマンド実行ラッパーに渡す責務を持つ。

## Read this when
- preprocess 系コマンドが実行時にどの前処理を行うか確認・変更したいとき。
- doctor preprocess と config 同期が CLI 実行前後のどこで呼ばれるかを追いたいとき。
- .cmoc/config.json の同期結果を git commit する条件や commit メッセージを確認・変更したいとき。
- preprocess コマンドの標準出力に含まれる見出しや repo root 表示を確認・変更したいとき。

## Do not read this when
- 個別の doctor preprocess の検査内容を確認したいだけなら、doctor preprocess 側の実装や対応する oracle doc を読む。
- config の正本定義や同期内容そのものを確認したいだけなら、config 定義・同期処理側を読む。
- git コマンド実行 helper の共通挙動を確認したいだけなら、runtime git helper 側を読む。
- repo root や work root の解決規則を確認したいだけなら、runtime path helper 側を読む。

## hash
- 2c59ed090cd67f23df77eceafbf163ec3eb5731d24b159df5ff7cf5717f13411

# `runtime_results.py`

## Summary
- 外部コマンド実行結果と Codex exec 実行結果を保持する不変 dataclass を定義する。
- コマンド終了コード、標準出力・標準エラー、生成物パス、Codex home、profile、schema、実行時間、quota 待機情報など、runtime 実行後に他処理へ渡す結果コンテナを扱う。

## Read this when
- 外部コマンドや Codex exec の実行結果を受け渡す型のフィールドを確認・変更したいとき。
- call log、prompt log、stdout/stderr log、output、profile、schema などの実行成果物パスを保持する結果オブジェクトを扱うコードを読むとき。
- quota 待機時間や poll 回数など、Codex exec 実行結果に付随する計測値の保持場所を確認したいとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する処理、ログファイルを書き出す処理、quota 待機制御の実装を探しているとき。
- CLI 引数、設定読み込み、profile 生成、schema 生成など、実行結果コンテナへ渡される値の作成元を調べたいとき。
- runtime 結果型ではなく、ユーザー向け出力形式やテスト期待値の仕様を確認したいとき。

## hash
- 149af60f60abfd4347d39a62b9b27d873af9cb1148cba531f191e860be3a9e8b

# `runtime_state.py`

## Summary
- session state file の永続化モデルと読み書き処理を担う。session/apply の state 断片、branch 名からの session_id 抽出、現在 branch に対応する state 読み込み、canonical JSON 書き戻し、home branch に紐づく active session 探索を扱う。

## Read this when
- session state file の JSON schema、欠落 field、不正 state、保存形式に関わる挙動を確認・変更したいとき。
- cmoc 管理 branch 名から session_id を特定する処理、または session/apply branch 上で state file を読み込む処理を確認・変更したいとき。
- home branch に対応する active session の探索条件を確認・変更したいとき。

## Do not read this when
- session state file の保存ディレクトリなど runtime path の組み立てだけを確認したいときは、runtime path を扱う対象を読む。
- CmocError の表示形式や例外クラス自体を確認したいときは、runtime error を扱う対象を読む。
- session/apply/abandon など各サブコマンドの利用者向け制御フローを確認したいときは、該当コマンド実装を読む。

## hash
- a9b62b64b304d58d929898813350f1f806a919e435b8ba036a23c109c1509fde
