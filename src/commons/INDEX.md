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
- CLI サブコマンドを実行する共通ライフサイクルを扱う実装。work root 検査、doctor preprocess、pre-log 検査、サブコマンドログ作成、進捗表示、戻り値の終了コード化、標準完了サマリー、例外時のエラー表示とログ記録を一箇所で管理する。
- 標準サマリー以外の stdout 契約を持つサブコマンド向けの結果型と、サブコマンド完了時に出力する標準サマリーの整形処理も含む。

## Read this when
- CLI サブコマンドの共通実行順序、ログ作成タイミング、進捗表示、終了コード処理、例外処理を確認または変更したいとき。
- doctor preprocess、pre-log check、runtime state の基準 root、サブコマンドログの保存先の関係を確認したいとき。
- サブコマンド実装が標準サマリーとは別に stdout を返す必要があり、その戻り値契約を確認したいとき。
- cmoc が work root で実行されていることを検査する処理や、その失敗時メッセージを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックだけを確認したいときは、そのサブコマンド実装を読む。
- サブコマンドログの内部データ構造、イベント保存形式、経過時間計測そのものを確認したいときは、runtime logging 側の実装を読む。
- work root や repo root の解決規則そのものを確認したいときは、runtime paths 側の実装を読む。
- doctor preprocess の修復内容そのものを確認したいときは、runtime doctor 側の実装を読む。

## hash
- a770e8482900c16431f7c36346e13329bf19b7d2cbeb885875c82f6b96e51dc8

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
- Codex exec の単一試行ループを実行制御する実装。Structured Output 検証、semantic retry、capacity retry、quota 待機と代表 probe、resume 継続、Codex call のログ保存と subcommand event 記録を同じ状態機械として扱う。
- Codex 実行時の cwd/profile/CODEX_HOME/schema/prompt/stdout/stderr/output/call log の組み立てと保存、quota wait の共有制御、実行結果の CodexExecResult 化、変更 worktree path の取得を担う。

## Read this when
- Codex exec 呼び出しの再試行条件、Structured Output 検証失敗時の扱い、capacity/quota エラー時の挙動、resume token の扱いを確認または変更したいとき。
- Codex call log、prompt log、stdout/stderr/output log、subcommand event、quota wait 時間や poll 数の記録内容を確認または変更したいとき。
- Codex 実行に使う cwd、CODEX_HOME、profile、output schema、subprocess argv/env の組み立てを確認または変更したいとき。
- agent call 後の worktree 変更 path 取得や apply requeue 向けの git status path 取得を確認したいとき。

## Do not read this when
- TUI 起動や exec 以外の Codex 起動分岐を調べるとき。
- Codex profile の具体的な生成内容、CODEX_HOME 解決、schema 準備、Codex stdout 解析などの低レベル共通処理だけを調べるとき。
- CLI サブコマンド定義、設定ファイルの読み込み仕様、または AgentCallParameter の構築ロジックだけを調べるとき。

## hash
- 4254bd141118194fa89f19a067d69c6c1e7ee61d2905e90d11cbe54a5dec7504

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
- Codex exec/TUI 呼び出しの直前に、登録済みの INDEX 更新 preflight を必要に応じて実行してから実行本体へ委譲する薄いラッパーを扱う。preflight の登録・解除、実行起点 root の決定、ロックと ContextVar による直列化・再入抑止を担う。

## Read this when
- Codex 呼び出し前に INDEX 更新 preflight が実行される条件や順序を確認・変更したいとき。
- preflight の登録・解除 API、テスト時の無効化、再入抑止、並行実行時のロック挙動を調べたいとき。
- Codex 呼び出しに渡された cwd/root と agent parameter の cwd から、indexing 対象 root がどう決まるかを確認したいとき。

## Do not read this when
- Codex exec/TUI の実際のプロセス起動、標準入出力、戻り値変換を調べたいだけのときは、実行本体を扱う runtime 側へ進む。
- AgentCallParameter のフィールド定義や run_indexing_preflight の意味そのものを確認したいときは、agent 呼び出しパラメータの定義へ進む。
- repo root や work root の解決規則を詳しく確認したいときは、runtime path 解決を扱う対象へ進む。

## hash
- 89a645a3eedc934ea16a6574c988bd0653ef220cfb48d418483de39768176610

# `runtime_codex_profile.py`

## Summary
- Codex CLI 起動時に渡す profile、sandbox、cwd、CODEX_HOME、追加 read/write path、schema 配置を組み立て、起動前検証と subprocess 実行の境界を扱う。
- apply 実行中の Codex child process tracking、pid file lock、終了後の記録削除、Codex JSONL stdout/stderr からの error・quota・capacity・resume token 判定をまとめる。
- 16,000 文字を超えるが、Codex subprocess 境界で共有される不変条件と失敗時文脈を一箇所に保つ責務を持つ。

## Read this when
- Codex CLI に渡す profile 本文、sandbox_mode、writable_roots、model provider、reasoning effort、CODEX_HOME の解決や検証を確認・変更したいとき。
- FileAccessMode ごとの追加 read/write path 許可境界、oracle・realization・repo write の sandbox 表現、TUI complete prompt や conflict 解消時の例外扱いを確認したいとき。
- Codex subprocess の起動失敗、apply abandon 用の child process tracking、pid file lock、process start time による pid 同一性確認を扱うとき。
- Structured Output schema の hash store 配置、Codex output JSON の読み取り、JSONL event からの error detail、quota/capacity retry 判定、resume token 抽出を扱うとき。

## Do not read this when
- prompt 本文や file access rule の正本仕様断片そのものを確認したいだけなら、対応する oracle 側の文書または prompt builder parts を読む。
- cmoc 設定値の定義や model/reasoning effort の設定構造を確認したいだけなら、設定を担う対象を読む。
- runtime log や schema store のディレクトリ構造だけを確認したいなら、runtime path を担う対象を読む。
- Codex CLI 以外の外部コマンド実行一般、または subprocess 境界に関係しないアプリケーションロジックを扱う場合は読まなくてよい。

## hash
- 86a67673b164efa60d67859580415f734e0847f8472159cc3054826b8cde7ac7

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
- cmoc の設定を正本 config 型と永続化 JSON object の間で相互変換し、設定ファイルの読み込み・検証・安定形式での書き込み・未作成時の初期生成を担う。
- 人間編集された config JSON の型不正や構文不正を、利用者向けの CmocError 境界へ変換する。

## Read this when
- CmocConfig と設定 JSON の変換規則、不足項目の既定値補完、enum key や model spec の復元処理を確認したいとき。
- 設定ファイルの存在確認、読み込み失敗、top-level 型不正、値の型不正に対する利用者向けエラーを変更したいとき。
- 設定ファイルを初期生成または現在の安定した JSON 表現へ同期する処理を確認したいとき。

## Do not read this when
- 正本 config 型そのものの field 定義や既定値を確認したいだけのときは、正本 config 定義を読む。
- 設定ファイルのパス決定規則だけを確認したいときは、runtime path を扱う対象を読む。
- Codex model 名や reasoning effort 名の正本対応を確認したいときは、oracle 側の config 定義を読む。

## hash
- ed2bb2ee956c57cf960d668d8d9aea8eea6a1b843c5035aafa0f9d07b37d8230

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
- 共通実行前の doctor preprocess を担う実装。cmoc ignore 設定、`.agents` の追跡可能化、cmoc 管理 Ollama の導入・user service 起動確認・model 取得を行い、修復差分だけを一時 index 経由で commit し、既存 staged 差分を復元する。
- git index を直接汚さずに HEAD 起点の一時 index で修復 commit を作る処理、systemd user service と `/proc` を使った Ollama listener 検証、cmoc provider model の重複排除と取得確認への入口になる。

## Read this when
- 実行前修復、doctor preprocess、`.gitignore` 修復、`.agents` の tracked placeholder、`.cmoc/local` の追跡解除、修復 commit、既存 staged hunks の保護に関する挙動を確認または変更したいとき。
- cmoc 管理 Ollama のインストール先、archive 取得、user service file 生成、`127.0.0.1:11434` の service 所有確認、HTTP 到達確認、model pull/show の制御を調べたいとき。
- config の cmoc provider model からローカル SLM を準備する流れや、設定読み込み失敗時の fallback を確認したいとき。
- git command、systemctl、tar、urllib、`/proc` 参照の失敗を `CmocError` として利用者向けに返す境界を調べたいとき。

## Do not read this when
- 個別 CLI command の引数定義や dispatch だけを調べたい場合は、CLI 層の実装を先に読む。
- 設定ファイルの schema、読み込み規則、model provider 定義そのものを調べたい場合は、config と runtime config の実装を読む。
- 汎用 git wrapper や cmoc ignore pattern の基本仕様だけを調べたい場合は、runtime git 側を読む。
- Ollama 以外の provider 実行、LLM 呼び出し、agent 実行制御を調べたい場合は、それぞれの実行系の実装を読む。

## hash
- d89d26693fb7a29e7b0464ae5fe384c018e30b709d507514ac4774ace363bdcd

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

# `runtime_paths.py`

## Summary
- 実行時の root 解決、時刻文字列、duration 表示、cmoc のローカル状態保存先、作業 directory 一時変更をまとめる runtime 用 path/time helper。
- oracle 側の path resolver を CLI 実行時の runtime error に変換し、session・report・log・worktree・schema・config など `.cmoc/local` 周辺の保存先を一貫して組み立てる入口。

## Read this when
- runtime code から `<repo-root>`, `<work-root>`, `<cmoc-root>` を解決する処理や、解決失敗時の利用者向け error を確認・変更したいとき。
- session state、report、sub command log、Codex call log、managed worktree、schema store、config JSON の保存先 path を確認・変更したいとき。
- 実行時刻の file name 用表記、console 表示用時刻、duration 表示の形式を確認・変更したいとき。
- `<work-root>/memo` 判定や、cwd 前提の外部 API 呼び出し区間だけ作業 directory を切り替える処理を扱うとき。

## Do not read this when
- path placeholder の正本定義や root resolver の仕様そのものを確認したい場合は、oracle 側の path model を読む。
- CLI command の実行フロー、永続状態の内容、report や log の中身を扱う場合は、それぞれの command・state・report・logging 実装を直接読む。
- 一般的な runtime error 型や表示形式を変更したい場合は、error 定義側を読む。

## hash
- 48f612d340a45bf5d137635a4caadb23384a661da842f554fe82e50c97e40931

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
- cmoc 管理 branch と session state file の対応を扱う永続化モデル。session/apply の state 断片、JSON schema 検証、canonical JSON 書き戻し、branch 名からの session_id 抽出、home branch に紐づく active session 探索を担う。

## Read this when
- session state file の構造、必須 field、許可される state 値、欠落 field の扱いを確認・変更したいとき。
- cmoc 管理 branch 名から session_id を特定する処理や、session/apply branch 判定のエラー挙動を確認・変更したいとき。
- session state file の読み込み、保存先決定、canonical JSON 書き戻し、active session 探索に関わる処理を追うとき。

## Do not read this when
- CLI サブコマンドの引数定義や利用者向け出力だけを確認したいとき。
- git 操作そのものの実行処理や branch 作成・削除の手順を確認したいとき。
- runtime path のディレクトリ定義だけを確認したいとき。

## hash
- d608145646343b8c53fb1f215b685f21693e0ada024aee1bbbd2f2b2abe8961e
