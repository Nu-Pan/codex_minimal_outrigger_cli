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
- 複数の `commons.runtime_*` モジュールから、CLI 実行・Codex 起動・設定・Git・パス・状態管理などの共通 API を集約して再公開する互換用ランタイム窓口。個別ランタイム機能の実装を確認する入口ではなく、複数機能を横断する公開シンボルの利用箇所や import 構成を調べる場合に読む。

## Read this when
- 共通ランタイム API の公開名、再公開元、利用可能な例外・型・関数を確認したいとき
- `commons.cmoc_runtime` 経由の import や公開 API の変更影響を調べるとき

## Do not read this when
- 特定のランタイム機能の実装詳細を調べるときは、対応する `commons.runtime_*` モジュールを直接読む
- CLI サブコマンドの処理フローを調べるときは、サブコマンド実装や `runtime_cli` を直接読む

## hash
- b40ef70d07f2c05922acdeceb300a23e1ee94554c2931305aee9a25c4534bc50

# `indexing.py`

## Summary
- INDEX.md の事前更新処理を担うモジュール。リポジトリ内の対象を走査し、Codex によるエントリー生成、内容検証、更新差分の commit までを実行する。
- 排他 lock、対象ディレクトリの深さ優先処理、既存エントリーの hash による再利用、Git 管理・除外対象の判定を扱う。

## Read this when
- INDEX.md の自動生成・更新、indexing preflight、生成結果の検証や commit 処理を変更するとき
- 対象ファイル・ディレクトリの走査条件、hash による鮮度判定、Codex 呼び出しの並列化を確認するとき
- INDEX.md エントリーの Markdown 形式や Structured Output の検証エラーを調査するとき

## Do not read this when
- INDEX.md の文章内容やルーティング方針そのものを変更・確認するときは、対応する oracle 文書やプロンプト生成側を読む
- indexing と無関係な CLI 機能、Git 操作、Codex 実行基盤の一般的な挙動を調査するとき

## hash
- f936050564a8cb139b62d580bbec9450c9c4a1cb8a476ec74ab135bd62297a3e

# `runtime_apply.py`

## Summary
- apply 実行の process identity と PID file を管理し、abandon 時の安全な停止・cleanup を担う共通ランタイムモジュール。linked worktree の解決、apply 実行の直列化、Codex child process group の追跡、PID 再利用を避けた停止処理を扱う。apply の実行中プロセス管理や abandon の停止挙動を変更・調査するときの入口。

## Read this when
- cmoc apply の process tracking、PID file、run lock、abandon による停止処理を変更・調査するとき
- apply process や Codex child process group の同一性確認、停止、stale PID cleanup の挙動を確認するとき
- apply branch に対応する worktree の解決処理を確認するとき

## Do not read this when
- apply の CLI 引数や利用者向け仕様だけを確認する場合
- apply の本体処理や abandon コマンドの上位フローを直接調査する場合は、それらの実装・仕様ファイルを先に読む
- 一般的な git worktree 操作や、apply と無関係な process 管理を調査する場合

## hash
- 47e70c8b3b1671ada93553b3231bbae38f8f14329c3ac9a2eccaf65431dd509a

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを提供する実装モジュール。work root 検査、doctor preprocess、サブコマンドログ、step 通知、完了サマリー、終了コード化、例外表示を一元管理する。
- サブコマンド固有の実装を run_cli_subcommand に渡して実行するための入口であり、ログ記録や標準出力・標準エラーの扱いを確認する際の基点となる。

## Read this when
- CLI サブコマンドの実行前処理・終了処理・例外処理を変更または調査するとき
- サブコマンドログ、step 通知、完了サマリー、終了コードの挙動を確認するとき
- work root 検査や doctor preprocess の共通実行経路を確認するとき

## Do not read this when
- 特定サブコマンドの業務処理や個別の引数定義だけを変更・調査するとき
- ログの保存形式やエラー文面そのものを変更・調査するときは、それぞれの担当モジュールや正本仕様を直接確認するとき

## hash
- 256fd6112f362a6036e13f5ee7d0c78927df7bd1b13d3cb04924fa612ac6d8e4

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
- Codex exec の単一試行ループを実装する中核モジュール。Structured Output の JSON/schema 検証、capacity retry、quota availability probe と待機、resume 継続、subprocess の入出力・call log・subcommand event 記録を一つの状態機械として扱う。変更時は exec 実行制御、再試行、quota、ログ記録、worktree 変更 path 検出の挙動を確認する入口になる。

## Read this when
- Codex exec の起動、cwd・CODEX_HOME・schema 設定、prompt/stdout/stderr/output のログ保存を変更または調査するとき
- Structured Output 検証失敗、capacity error、quota error、quota probe、resume token による再試行を変更または調査するとき
- Codex call の console/subcommand event や失敗時の調査情報を変更するとき
- agent call 後の worktree 変更 path 検出を変更するとき

## Do not read this when
- TUI 起動処理そのものを変更または調査するときは、TUI 起動を担当する別 module を先に読む
- Codex subprocess の共通的な環境・エラー分類・schema 準備などの詳細だけを変更または調査するときは、runtime_codex_profile 側を直接読む
- 設定読み込み、git status、path 生成などの共通機能だけを変更または調査するときは、それぞれの runtime 共通 module を直接読む

## hash
- 5ee008af197b9904c749b6fe31e40e38d06fd023c7509290639fe0c3f2df0176

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し時の console 通知と、その失敗理由を console/event で共通化する error text 変換を扱う。

## Read this when
- Codex 呼び出しの開始通知、経過時間、終了コード、起動失敗メッセージの表示を変えたいときに読む。
- Codex 固有の失敗情報を、人間向け console 表示とイベント記録で同じ文面に揃えたいときに読む。

## Do not read this when
- 一般的なログ出力の整形や保存先を変えたいだけなら、汎用の runtime logging 側を読む。
- `codex exec` の引数構成、プロンプト生成、実行制御を変えたいだけなら、呼び出し本体の実装を読む。

## hash
- 6ca8648503df249ad1c39cf3d01e3c95496fd6762ca7d903a9caaa7b39b6f9d6

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行前に indexing preflight を挟む共通ランタイム層。preflight の登録・解除、再入抑止、直列実行、実行対象からの indexing root 決定を扱い、実際の Codex 呼び出しは runtime_codex へ委譲する。

## Read this when
- Codex exec または TUI の実行前 indexing 処理、preflight の設定・解除、再入防止や実行順序を変更・調査するとき。
- Codex 呼び出し設定から preflight の起点 root が決まる仕組みを確認するとき。

## Do not read this when
- Codex の実行本体やコマンド結果の詳細を変更・調査するときは、委譲先の runtime_codex または runtime_results を直接読む。
- リポジトリや作業ディレクトリの root 解決そのものを変更・調査するときは、runtime_paths を直接読む。

## hash
- 050693a5a2472180e927055cc8255f07e16e96627d7f16e6877a50b002eacfd4

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界の実装。起動時の sandbox・cwd・CODEX_HOME・argv/env・provider/schema 配置と、child process の追跡・停止、JSONL 出力の解析、capacity/quota/予期せぬエラー判定を扱う。Codex CLI の実行環境または機械的な実行結果の解釈を変更・調査するときの入口。

## Read this when
- Codex CLI に渡すファイルアクセス権、作業ディレクトリ、設定 override、環境変数を変更・確認するとき。
- Codex subprocess の process group 追跡・停止、pid 再利用対策、apply 中断処理を変更・調査するとき。
- Structured Output schema の配置、Codex JSONL 出力の読み取り、resume token や error/retry 判定を変更・調査するとき。

## Do not read this when
- Codex CLI へ渡すプロンプト本文やその構築規則だけを変更・調査するとき。
- Codex の呼び出し元である subcommand の業務フローや設定定義だけを変更・調査するときは、まず該当する上位モジュールを読む。

## hash
- 66ba885d704679c73e5e029b10c53f1755d69ddc9217a9f1ff8f57cc725875e4

# `runtime_codex_tui.py`

## Summary
- Codex TUI を起動する共通ランタイム処理。設定上書き引数・作業ディレクトリ・Codex Home・呼び出しログを準備し、サブプロセス実行結果と成功・失敗イベントを返却・記録する。

## Read this when
- Codex TUI の起動方法、作業ディレクトリや Codex Home の解決、設定上書き引数、call log の生成を変更・調査するとき
- Codex CLI/TUI 呼び出しの例外処理、終了コード、コンソール通知、サブコマンド logger へのイベント記録を確認するとき

## Do not read this when
- Codex CLI の設定値や argv の具体的な生成規則だけを調査する場合は、runtime_codex_profile 側を先に読む
- Codex 呼び出し以外の一般的なログ、パス、設定、結果型の仕様だけを調査する場合は、対応する runtime モジュールを直接読む

## hash
- 302076d6f5ec4b3d9d289ca826f3f3dfc5b0e9a469eaefef10404bd93e2ca1ea

# `runtime_config.py`

## Summary
- 永続化された cmoc 設定 JSON とランタイム設定型の相互変換を担当する。設定値の既定値補完・型検証・JSON 保存、設定ファイルの読み込みと未作成時の初期生成を提供する。

## Read this when
- cmoc 設定 JSON の読み書き、設定値の復元・検証、既定設定との同期、設定エラーの挙動を変更または調査するとき。

## Do not read this when
- 設定型そのものの定義や既定値を確認したいときは、設定型を定義する対象を直接読む。
- 設定ファイルのパス定義だけを確認したいときは、ランタイムパス定義を直接読む。

## hash
- 14db36478944f71011c1654ad666f4e63610b6219e41f56788070e17b826d13b

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
- doctor 前処理として、Git common directory 単位の排他ロック下で設定同期・ignore 修復・`.agents/.gitkeep` の追跡・ローカル Ollama の稼働確認を行い、修復差分だけを commit する実装。通常の staged 差分を保護しながら一時 index で修復を合成・復元する処理も含む。doctor 前処理、Git index の保全、修復 commit、設定追跡検証を確認する入口。

## Read this when
- doctor 前処理の挙動、ロック、worktree と main worktree の修復対象を変更・調査するとき
- 修復差分だけの commit、一時 index の利用、既存 staged 差分や index の復元を確認するとき
- `.gitignore`、`.agents/.gitkeep`、cmoc 設定、`.cmoc/gu` の Git 追跡状態に関する処理を変更するとき
- doctor 実行時の Ollama 確認や Git エラー処理を調査するとき

## Do not read this when
- doctor 前処理や修復 commit の仕組みを扱わず、他の CLI 処理・設定定義・Ollama 実装だけを直接調査するとき
- 一般的な Git 操作や別モジュールの runtime helper の仕様を確認することが目的のとき

## hash
- 260121e3ae5d397c799008a9aa9d44e8af6c186600f407c17321eebe7825c4e0

# `runtime_errors.py`

## Summary
- cmoc の実行時例外と利用者向け Markdown エラーレポート生成を担当する。CmocError が概要・次の行動・詳細を保持し、render_error が未知の例外も含めて Summary、Next actions、Detail、Call stack の共通形式へ変換する。

## Read this when
- 実行時エラーの構造、利用者向けエラーレポートの出力形式、復旧案の補完、コールスタックの扱いを変更・調査するとき。

## Do not read this when
- 特定の CLI コマンドの入力検証や業務処理だけを変更・調査するとき。
- エラーレポートの表示先や呼び出し側の制御を確認したいときは、まずその呼び出し側を直接読む。

## hash
- 152fcb4b8030f5fb2be82569787d2862effba44076d46afbc39bdb088b736e9a

# `runtime_git.py`

## Summary
- Git 操作、branch・linked worktree 管理、`.cmoc` の ignore 状態確認、oracle file 判定を担う共通 runtime helper。各種 cmoc 操作で必要な Git 状態検査・安全な worktree 操作・パス分類の入口となる。

## Read this when
- Git command の実行結果を cmoc のエラーへ変換する処理を確認するとき
- branch、HEAD、worktree の作成・削除・管理対象判定を変更するとき
- `.cmoc/gu` の ignore 設定や Git exclude の更新・検査を変更するとき
- oracle file または Git ignore に基づくパス分類を変更するとき

## Do not read this when
- CLI の個別サブコマンドの業務フローだけを確認するとき
- Git や worktree と無関係な runtime helper を変更するとき
- oracle file の仕様そのものを確認するときは、対応する `oracle` 配下の正本を直接読む

## hash
- a0090ae952b5554b67e283d37a7d7c9bd84108a66d479c419f8a998b580abb2c

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines ログ記録と step timing・quota 待機時間の集約を担う runtime logging モジュール。logger の context 間共有機能も提供する。

## Read this when
- サブコマンドのイベントログ形式、ログファイル生成、step の開始・完了計測、経過時間や quota 待機時間の集計を変更・調査するとき
- 深い runtime helper から現在のサブコマンド logger を参照・差し替え・復元する処理を変更するとき

## Do not read this when
- ログ仕様そのものや console 表示との互換性を確認したい場合は、先に対応する oracle 文書を読むとき
- ログディレクトリや timestamp 付きパス予約の共通処理だけを調査する場合は、runtime paths の実装を直接読むとき

## hash
- 01fababfe41483ba8194c1aec614beda27fe55ad5010a54e0b61e8a190f71a09

# `runtime_ollama.py`

## Summary
- cmoc provider の local SLM を managed Ollama で利用可能にする単一の preflight 実装。Ollama の archive install、user systemd service の同期・起動、procfs による listener と executable の所有者確認、model の取得・load、GPU 使用確認までを一連の処理として扱う。

## Read this when
- cmoc provider の model を Ollama で serve・load する処理を変更または調査するとき
- Ollama の archive install、systemd user service、127.0.0.1:11434 の検証、procfs による process/socket 確認を扱うとき
- Ollama model の pull、API 応答、VRAM 使用確認や、それらの失敗時エラーを扱うとき

## Do not read this when
- cmoc provider の model を使用しない処理を扱うとき
- Ollama 以外の provider、一般的な runtime config、runtime path、runtime error の実装だけを扱うとき
- 既存の managed Ollama preflight の内部順序・検証・失敗条件を確認する必要がなく、別の上位処理を直接調べるとき

## hash
- de8547c0be605cfb5d80c3dce084e41a92885ad5d7ccce48e162927b3e692d30

# `runtime_paths.py`

## Summary
- cmoc の実行時パスと時刻・所要時間を扱う共通ユーティリティ。repository/worktree/cmoc root の解決、runtime ディレクトリ・設定・ログ・report・schema・worktree の保存先取得、cwd の一時変更、timestamp 予約、表示形式の整形を提供する。パス解決や runtime 状態の保存先を扱う実装・テストの入口。

## Read this when
- repository root、worktree root、cmoc root、runtime ディレクトリ、設定・ログ・report・schema・session の保存先を確認または変更するとき
- timestamp、console timestamp、duration 表示、timestamp 付き path の排他的予約を確認または変更するとき
- cwd を切り替える処理や、root 解決時の runtime error、memo 判定を確認するとき

## Do not read this when
- CLI サブコマンド固有の処理や出力形式だけを調べるとき
- root placeholder の定義や実パス解決そのものを変更するときは、まず path model の実装を読むとき
- 設定 JSON の内容や prompt の構築規則だけを調べるとき

## hash
- c238d9bab51ff7e5482f5521f8e16824df565c5437077d44667b12e34ddec88f

# `runtime_preprocess_command.py`

## Summary
- `cmoc` の preprocess 系サブコマンド実行をまとめる薄いラッパー。コマンド開始時の共通処理と、事前診断(preprocess)の呼び出し、最後の最小出力をつなぐ役割が中心で、個別サブコマンド本体よりも起動経路の整理を読むときに参照する。

## Read this when
- `cmoc` の各サブコマンドを実行前に共通の前処理へ通す流れを確認したいとき。
- コマンド実行時に work root や repo root をどう取得し、どのタイミングで診断処理を走らせるかを見たいとき。
- サブコマンド開始ステップの表示と、その後の最小限のヘッダ出力の責務を確認したいとき。

## Do not read this when
- 事前診断(preprocess)そのものの内容や判定基準を知りたいときは、直接その診断実装側を読む。
- CLI の引数定義やサブコマンド列挙を追いたいときは、個別コマンド定義側を読む。
- 共通のパス解決や CLI 実行基盤の詳細を知りたいときは、runtime_paths や runtime_cli 側を読む。

## hash
- c9a2178b1f21f1239059f2b05992c5ba13756483053e288203185c99e9d55320

# `runtime_results.py`

## Summary
- Codex exec の構造化出力契約、外部コマンド結果、および exec 実行に伴う生成物・ログ・設定パスを表す型を定義する。runtime 結果の型や呼び出し側契約を確認する必要がある場合の入口となる。

## Read this when
- Codex exec の戻り値契約や構造化出力へのアクセス方法を変更・確認するとき
- 外部コマンドの終了コード、標準入出力、実行ログや生成物のパスを保持する結果型を利用するとき

## Do not read this when
- Codex exec の実行処理そのものを変更・確認するとき
- CLI 入出力やログ保存処理の具体的な挙動だけを調べるとき

## hash
- 9f6e365d5335be51796785b3abc187d63c1d32111ecb9b0ad30308780df063e4

# `runtime_state.py`

## Summary
- session state の永続化モデルと JSON 変換・検証を担う。session/apply の状態断片、state file の保存先、branch から session ID を特定する処理、home branch に紐づく active session の検索を提供する。session fork 用の repository 共通排他 lock も扱う。

## Read this when
- session/apply の state schema、state file の読み書き、JSON field 検証を変更・調査するとき
- cmoc 管理 branch から session ID を解決する処理や session fork の排他制御を変更するとき
- active session と home branch の関連付けを確認するとき

## Do not read this when
- CLI の session/apply 操作そのものや branch 操作の手順を確認したいときは、対応する sub-command 実装・仕様を直接読む
- runtime path の定義だけを確認したいときは runtime_paths を直接読む
- git 共通ディレクトリの取得だけを確認したいときは runtime_git を直接読む

## hash
- 0dd8e9d30a216467abff8714452d83ecc78ceb9824fe48186bb818f0e5089aaa
