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
- Codex exec の実行制御を担い、prompt/stdout/stderr/output/call log の保存、Structured Output 検証、semantic retry、capacity retry、quota 待機と代表 probe、resume 継続、subcommand event 記録を一体の状態機械として扱う。
- Codex profile、CODEX_HOME、実行 cwd、output schema、prompt stdin log、call log に関わる実行条件を組み立て、Codex subprocess の結果を統一した実行結果へ変換する。
- worktree 上の変更 path を git status から取得し、apply 系の再投入判断で使える absolute path と status code を返す補助処理も含む。

## Read this when
- Codex exec 呼び出しの再試行条件、quota 枯渇時の待機・probe・resume、capacity error の backoff、または Structured Output 検証失敗時の扱いを確認・変更したいとき。
- Codex call の prompt/stdout/stderr/output/call log、subcommand event、console 表示、elapsed/quota wait/poll count の記録内容や保存タイミングを確認・変更したいとき。
- Codex subprocess に渡す argv、profile、CODEX_HOME、cwd、output schema、stdin prompt file の組み立てや preflight の流れを追いたいとき。
- agent call 後の worktree 変更 path 取得や、untracked directory を file-level path として扱う git status 取得を確認・変更したいとき。

## Do not read this when
- TUI 起動や exec 以外の Codex 呼び出し分岐を扱う場合は、この対象ではなく該当する起動制御側を読む。
- Codex profile の具体的な生成規則、CODEX_HOME 解決、schema 準備、resume token 抽出、エラー種別判定そのものを変更したい場合は、それらを提供する runtime profile 周辺を直接読む。
- subcommand log の保存形式や logger 実装そのものを変更したい場合は、実行制御ではなく logging 側を読む。
- 一般的な git status wrapper の実装や path model 全体を変更したい場合は、ここではなく git/path の共通 runtime 側を読む。

## hash
- 8d0ce870e4c157636416c27c4dcb33333088c7acf4000d4b65b3cc82bcb9a8bf

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
- Codex CLI の subprocess 境界で使う profile 生成、sandbox/permission profile 変換、CODEX_HOME 検証、apply 中の child process tracking、schema 配置、Codex JSONL 出力からの error/quota/capacity 判定をまとめる実装。
- FileAccessMode を Codex CLI が扱える実行環境へ落とし込む処理と、Codex subprocess 起動前後の失敗を cmoc の実行時エラーや retry 判定へ変換する処理の入口になる。

## Read this when
- Codex CLI 起動用 profile の model、reasoning effort、sandbox、permission profile、writable/read root の組み立てを確認または変更したいとき。
- FileAccessMode ごとの読み取り・書き込み許可境界、oracle/realization/repo write の sandbox 表現、追加 read/write path の検証を扱うとき。
- CODEX_HOME の解決・検証、Codex CLI 不在時のエラー化、Ollama provider 設定、schema store への Structured Output schema 配置を調べるとき。
- apply abandon と連動する Codex child process の pid 記録、lock、pid 再利用対策、tracking path の process-local 切り替えを扱うとき。
- Codex JSONL stdout/stderr から利用者向け error detail、resume token、capacity error、quota error を抽出する挙動を確認したいとき。

## Do not read this when
- cmoc の正本仕様そのものを確認したいとき。対応する oracle file を直接読むべき。
- Codex subprocess 境界ではなく、通常の runtime path 計算、git 判定、hash file 書き込み、設定定義そのものを変更したいとき。それぞれの責務を持つ実装を直接読むべき。
- CLI サブコマンドの利用者向けフローや prompt 本文の構成を調べたいだけのとき。subprocess 起動環境や JSONL error 判定に踏み込む場合だけ読む。

## hash
- 35556536607fb7fdf982e7ef4486552dd08f0250bc91f65c1f67c0bbb6bc1c06

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
- cmoc config の永続化 JSON と runtime config 型の相互変換、既定値補完、型検証、読み書き、未作成時の生成を扱う。
- 人間編集された config JSON の不正値を利用者向け CmocError に変換する境界を担い、model・reasoning_effort・各種 loop/parallel 数の復元規則をまとめている。

## Read this when
- cmoc config JSON の保存形式、読み込み、既定値補完、sync 生成、または不正 config のエラー表示を変更したいとき。
- config 型と JSON object の対応、enum key の文字列表現、Codex model spec の検証、整数設定値の bool/string 拒否を確認したいとき。
- doctor などが生成・更新する config の永続化内容や、<repo-root>/.cmoc/config.json の読み込み失敗時挙動を追うとき。

## Do not read this when
- config 項目そのものの正本定義や既定値だけを確認したいときは、config 型や oracle 側の model spec 定義を読む。
- config ファイルの配置パス計算だけを確認したいときは、runtime path を扱う対象を読む。
- CLI command の引数処理、doctor の実行フロー、または config 以外の runtime error 表示全般を調べたいとき。

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
- cmoc provider の local SLM を、cmoc 管理の Ollama として利用可能にする runtime 実装。設定から対象 model を抽出し、Ollama の取得・配置、systemd user service の同期と起動確認、固定 endpoint の所有 process 検証、model pull までを扱う。

## Read this when
- cmoc provider の model を実行前に local Ollama で serve できる状態へ整える処理を確認・変更したいとき。
- Ollama archive の取得先、管理領域、model store、固定 host/port、systemd user service の扱いを調べたいとき。
- 127.0.0.1:11434 の listener が cmoc 管理 service 由来かを procfs と systemd 情報で検証する制御を確認したいとき。
- Ollama の install、service 起動、HTTP 応答確認、model show/pull の失敗を CmocError に変換する利用者向けエラー処理を変更したいとき。

## Do not read this when
- cmoc 設定 schema や model provider 定義そのものを確認したいだけのときは、設定定義側を読む。
- Ollama 以外の provider 実行、Codex 呼び出し、agent call orchestration の処理を調べたいとき。
- パスモデル一般、worktree/repo root の解決、config file path の定義だけを確認したいときは、runtime path や oracle の path model を読む。

## hash
- c1454428151f7829b3634d2c8d92cdcf8a4a5a876e1b56ab13fac5b71e43333c

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
- session state file の永続化モデルと読み書き処理を扱う。session/apply の state 断片、branch 名からの session_id 抽出、現在 branch に対応する state 読み込み、canonical JSON 書き戻し、home branch に紐づく active session 探索の入口になる。

## Read this when
- session state file の schema、必須 field、許容 state、null/string 制約を確認または変更したいとき。
- cmoc/session、cmoc/apply の branch 名から session_id を特定する処理や、その失敗時エラーを確認または変更したいとき。
- session state file の保存先、読み込み、書き戻し、home branch から active session を探す処理を確認または変更したいとき。

## Do not read this when
- session state file のディレクトリ配置だけを確認したいときは、runtime path を扱う対象を直接読む。
- 個別サブコマンドの操作手順や状態遷移の業務仕様を確認したいときは、対応する app spec やコマンド実装を読む。
- CmocError の表示形式や共通エラー処理だけを確認したいときは、runtime error を扱う対象を読む。

## hash
- 5453ce64ca708e9c80e6e3aa4a0416dbc93461ecafdc6a30864d7db0274f46bf
