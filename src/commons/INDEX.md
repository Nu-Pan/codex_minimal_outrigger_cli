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
- 実行時共通機能を単一の import 入口に集約する再公開モジュール。Codex 実行と引数上書き、設定、内容ハッシュ、CLI 実行、doctor 前処理、エラー、git 操作、ログ、パス、結果型、状態管理にまたがる runtime API をまとめて参照するための窓口。

## Read this when
- 複数の runtime 系モジュールから提供される関数・型・定数を、呼び出し側でまとめて import したい箇所を確認する。
- 既存コードが runtime 共通 API をどの公開入口から参照しているかを調べる。
- runtime 系モジュールの再公開対象を追加・削除する必要があり、集約 import の表面を確認する。

## Do not read this when
- 個々の runtime API の挙動、引数、失敗時処理、永続状態の詳細を確認したい場合は、対応する各 runtime モジュールを直接読む。
- 新しい runtime 機能を実装する場合は、この集約入口ではなく責務に対応する実装モジュールを読む。
- CLI サブコマンド固有の処理やテスト対象の外部挙動を確認したい場合は、該当するサブコマンド実装またはテストを読む。

## hash
- b66820253dd4a2a3a2a93de7a4d9bf8dad5c44d233e01d4da7de593e4e723f86

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
- Codex exec の単一試行ループを読む入口。Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、call/prompt/stdout/stderr/output の各 log 生成を確認したいときに進む。TUI 起動や他サブコマンドの分岐は対象外。
- この module を読むのは、`codex exec` の実行制御と再試行の境界、失敗時にどの log を残すか、quota 共有状態機械の扱いを確認したいとき。変更が log 命名、resume token の扱い、Structured Output の失敗判定に触れるなら優先して読む。

## Read this when
- `codex exec` の実行フロー、再試行、Structured Output 検証、quota 待機の挙動を変えるとき。
- 実行ごとの prompt/stdout/stderr/output/call log の生成や、resume token の継続条件を確認したいとき。
- capacity error と quota error の分岐、代表 probe の開始・共有・復帰条件を追いたいとき。

## Do not read this when
- TUI 起動や UI 側の制御を変えたいときは、別 module を先に読む。
- `git status` ベースの変更 path 収集だけが目的なら、この module 全体ではなく変更 path 取得側を読む。
- Codex exec 以外のサブコマンドの分岐や CLI 定義を調べたいだけなら、この module は後回しでよい。

## hash
- f4d8c2244c0b283e4e9608724fbf67d2d6bce884fab326793d5d35ae044e43b5

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しに関する console 出力と、起動失敗時の error 文面を共通化する補助をまとめた対象。呼び出し通知の表示形式を確認したいときや、失敗理由の整形を他の出力経路と揃えたいときの入口になる。
- console に出す時刻・経過時間・終了コードの組み立てを見たい場合と、`CmocError` を含む例外を利用者向けの短い error text に直したい場合に読む。

## Read this when
- Codex CLI 呼び出しの通知を console に出す処理を追加・修正したい。
- 起動失敗や例外の文面を、console 出力と event で同じ表現に揃えたい。
- 経過時間や時刻表示を含む呼び出しログの見え方を確認したい。

## Do not read this when
- 呼び出しの記録先そのものや永続化の責務を変えたいときは、保存・記録側の対象を先に読む。
- Codex 以外の CLI 表示や一般的な runtime エラー処理を変えたいだけなら、より上位の入出力処理を読む。
- `console_timestamp` や `format_duration` の表示仕様だけを追いたいときは、それらを定義している対象を直接読む。

## hash
- 3aa2c9b4388542920c4557bddf5901e75f441a15c053f019c7c9b9f20c90267d

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
- Codex CLI を起動する前後で、`argv`/sandbox・read/write 許可・`CODEX_HOME`・child process tracking・Structured Output schema 配置・JSONL error 判定を一括で扱う基盤を読む入口。Codex subprocess 境界の不変条件や、実行環境の組み立てと失敗時の解釈を変える作業でここを読む。
- このファイルを読むのは、Codex 呼び出しの権限境界、実行 root の決定、追加 read/write path の妥当性、tracked child process の記録、schema の保存先、CLI 出力のエラー判定を確認・変更したいとき。実装を分割して個別 helper だけを追うより、subprocess 周辺の挙動全体を把握したい場合に向く。

## Read this when
- Codex CLI に渡す sandbox、permission profile、`CODEX_HOME`、`cwd`、追加 path 制御を変えたい
- apply 実行中の child process tracking や pid file ロック、終了時のクリーンアップを調べたい
- Structured Output schema の配置方法や、Codex の stdout/stderr から capacity/quota/unexpected error を判定する条件を確認したい

## Do not read this when
- 単純な設定値や runtime path の個別定義だけを知りたい場合は、まずそれぞれの設定・path 生成側を読む
- Codex CLI の高レベルなサブコマンド仕様や人間向け運用手順だけを知りたい場合は、対応する app_spec 側を先に読む
- この境界をまたがない単独 helper の内部実装だけを追いたい場合は、より局所的な実装ファイルを直接読む

## hash
- d1e5c028706285f3041bf21382e01e795c76084de1f7ad33a4c325d26d774a3b

# `runtime_codex_tui.py`

## Summary
- Codex TUI の起動を 1 か所にまとめた実行補助。呼び出し用 argv の組み立て、call log の保存、起動後のエラー整形と例外変換までを扱う。
- Codex の実行先 cwd と `CODEX_HOME` の解決・検証、設定上書き引数の準備、サブコマンドログへのイベント記録が必要なときに読む。

## Read this when
- Codex TUI を起動する処理を追加・変更するとき。
- 呼び出し前に `CODEX_HOME` の解決や検証、`--cd` の決定方法、追加 read path の扱いを確認したいとき。
- call log の保存内容、起動失敗時の `CmocError` 変換、サブコマンドログへの記録を追いたいとき。

## Do not read this when
- Codex の通常 CLI 実行や別サブコマンドの起動経路を見たいときは、各サブコマンド側の実行補助を読む。
- 設定値の読み込みや Codex プロファイルの詳細だけを確認したいときは、このファイルではなく各責務の元のモジュールを読む。
- TUI 以外の call log 形式や保存先の全体方針だけを知りたいときは、より上位のログ・パス管理側を読む。

## hash
- 1ac3e6cc3de04dbe252fbf40360285086b7736e54c580b62da3b7920189e47de

# `runtime_config.py`

## Summary
- cmoc の設定を正本 config 型と永続化 JSON の間で変換し、設定ファイルの読み込み、検証、既定値補完、書き戻しを担う。
- 利用者が編集する config JSON の型不正や構文不正を、利用者向けの CmocError 境界へ変換する。

## Read this when
- 設定ファイルの保存形式、既定値補完、読み込み時の検証、または sync 時の生成・正規化挙動を確認・変更したいとき。
- config の enum key map、Codex model spec、int 値、optional section の JSON 復元ルールを調べたいとき。
- 設定ファイル不在、JSON 構文不正、top-level 不正、値型不正に対する利用者向けエラーを確認したいとき。

## Do not read this when
- config 型そのものの項目定義や既定値を確認したいだけなら、config 定義側を読む。
- Codex model 名や reasoning effort 名の正本定義を確認したいだけなら、oracle 側の model config 定義を読む。
- 設定ファイルのパス解決だけを確認したいなら、runtime path 側を読む。

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
- d121b59cd941f68e101d0bf9b1eb0f0fdd2fe8c928d89dd6447b3079581fb905

# `runtime_doctor.py`

## Summary
- `cmoc doctor preprocess` の共通修復処理をまとめる。Git の作業ツリー修復、`.agents` の追跡補助、ローカル SLM 起動確認、修復差分の commit までを一連で扱う入口。
- 通常の Git 操作や Ollama 制御の個別処理を読む場所ではなく、doctor 実行時に「何を修復し、どこまで commit するか」を確認したいときに読む。

## Read this when
- doctor 実行前に入る共通修復の範囲を確認したい。
- 修復対象に `.gitignore`、`.agents`、`.cmoc/local` が含まれる理由や、修復差分だけを commit する流れを追いたい。
- 一時 index を使って user の staged 変更と doctor の修復 commit を分離する意図を確認したい。

## Do not read this when
- 通常の Git 操作や汎用的な error handling の実装だけを追いたい。
- Ollama 起動確認の詳細だけを知りたいなら、より直接の実装を読むべきである。
- doctor 前処理以外のサブコマンドや一般的な CLI 初期化の入口を探している。

## hash
- 582b46929933fcfe8334d576eb38a2c65afd86f14cdc7bf803ae6ea97cd0c900

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
- cmoc が管理する Ollama の導入、user service の同期、`/proc` による稼働主体の確認、モデルの取得・load・GPU 推論確認までを一連で扱う入口。」「単一の `ensure_ollama_serves_local_slm` を起点に読むと、修復と検証の順序、失敗時の停止条件、どこまでがこの module の責務かを把握しやすい。」「Ollama の設定値や共通 config 取得の詳細を追いたいときは、この module より先に `runtime_config` や `runtime_paths` を読む。

## Read this when
- cmoc provider の local SLM を Ollama で自動的に使える状態へ整える処理を変更・確認したいとき。
- Ollama の install、systemd user service、model load、GPU 利用確認のいずれかを、同じ起動経路の一部として扱う必要があるとき。
- サービスが本当に cmoc 管理の Ollama か、`/proc` と `systemctl --user` でどう判定しているかを確認したいとき。

## Do not read this when
- Ollama のモデル名や provider 設定の値そのものを決めたいだけなら、先に `runtime_config` 側を読む。
- Ollama 以外の provider の起動や検証を扱いたいときは、この module ではなくその provider 専用の実装を読む。
- CLI の引数解釈やコマンド分岐だけを追いたいときは、この module ではなく呼び出し元の subcommand 実装を読む。

## hash
- 092a1e1e44d6512fb4b3f39644107c066450eda14370e09ab0cb0e27c1b65ed1

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
- コマンド終了コード、標準出力・標準エラー、生成物パス、Codex home、schema、実行時間、quota 待機情報など、runtime 実行後に他処理へ渡す結果コンテナを扱う。

## Read this when
- 外部コマンドや Codex exec の実行結果を受け渡す型のフィールドを確認・変更したいとき。
- call log、prompt log、stdout/stderr log、output、schema などの実行成果物パスを保持する結果オブジェクトを扱うコードを読むとき。
- quota 待機時間や poll 回数など、Codex exec 実行結果に付随する計測値の保持場所を確認したいとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する処理、ログファイルを書き出す処理、quota 待機制御の実装を探しているとき。
- CLI 引数、設定読み込み、argv 上書き生成、schema 生成など、実行結果コンテナへ渡される値の作成元を調べたいとき。
- runtime 結果型ではなく、ユーザー向け出力形式やテスト期待値の仕様を確認したいとき。

## hash
- c9bf5b582e21beadd3ab372c424bc794a332ddbfd657f47369776b0109590f13

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
