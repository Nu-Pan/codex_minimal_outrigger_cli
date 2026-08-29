# `acp`

## Summary
- `src/acp` は ACP 互換の公開入口と builder adapter 群を扱う。`acp.*` 参照の互換性、canonical な oracle 実装への委譲、共通プロンプト整形、feedback・indexing・oracle・realization・session・TUI などの処理別 adapter への入口として機能する。

## Read this when
- `acp` 公開名の存廃や既存利用者向け参照から `oracle` 側の実体へ切り替える導線を確認したいとき
- `acp.builder` の互換接続、共通プロンプト整形、feedback issue の正規化・検証、または処理別 builder adapter の入口を探すとき
- builder adapter の対象領域を特定し、下位対象へ進む入口が必要なとき

## Do not read this when
- `acp` 配下の具体的な実装詳細や移行先の詳細だけを知りたいときは、対応する実体モジュールを直接読む
- canonical な oracle 実装、正本仕様、通常の利用側ロジックを調査・変更するときは、対応する正本実装や参照元を直接読む
- ACP builder と無関係な CLI 処理や実装を調査するとき

## hash
- ae65897090c293e1c2b592328bda33127b088818977bd7d0f8348ed9ca0f626d

# `basic`

## Summary
- `basic.*` の互換 import 公開面をまとめた realization 側の入口。ACP 型、path model、構造化文書 API の旧参照から、各互換モジュールまたは再公開元の正本へ進むための下位要素入口を提供する。

## Read this when
- `basic` 名前空間に残る互換 API の範囲や、旧 import から移行先を確認したいとき。
- ACP、path model、構造化文書の互換入口を横断して、個別モジュールを読むべきか判断するとき。

## Do not read this when
- 個別 API の実装、再公開内容、型定義、描画仕様を確認したいときは、`basic.acp`、`basic.path_model`、`basic.struct_doc`、またはそれぞれの正本実装を直接読む。
- 正本仕様そのものや、`basic` 名前空間と無関係な処理を調べるとき。

## hash
- ea7ec701e546985b90dda735f067c250cdd2609d2464948e58591d98ccf40fd2

# `cmoc_runtime.py`

## Summary
- `commons.cmoc_runtime` の公開名を互換的に再公開する薄い import shim。pyproject が `cmoc_runtime` を公開し、ツリー内の呼び出し元がこのパスを直接 import している間の移行入口。

## Read this when
- `cmoc_runtime` の互換 import path、公開名、または runtime module への移行状況を確認するとき。

## Do not read this when
- runtime の実装や責務別 module の詳細を確認するときは、`commons.cmoc_runtime` または該当する runtime module を直接読む。
- 互換 path の移行完了後は、この shim を読む必要はない。

## hash
- ce0901465f229760c4bd1f4c5ce3f4a035bb53bf6aee04de082b5843cff3ff17

# `commons`

## Summary
- cmoc 共通 runtime helper を提供する commons パッケージの初期化ファイル。commons 配下の共通実行時補助機能を確認・変更するときの入口。
- cmoc の実行時共通 API を集約する公開モジュール。CLI、Codex subprocess、設定、ログ、パス、Git worktree、状態管理などの共有機能への入口。
- INDEX.md の検査・生成・更新 lifecycle を担う共通実装。directory traversal、entry 更新、hash 鮮度判定、snapshot 復元、lock、commit を扱う。
- エディタを使った AI Agent prompt 入力の共通境界。作業ファイル予約、初期入力、エディタ起動、編集結果の抽出・保存・cleanup を扱う。
- 最外側 CLI サブコマンドの実行 lifecycle を統括する。doctor、進行通知、feedback、診断ログ、primary report、terminal result、終了コードを連携する。
- Codex exec と TUI の外部利用向け公開入口。各実行経路の具体的な処理は下位モジュールへ委譲する。
- 1 回の Codex agent call における exec 制御の中心。Structured Output 検証、retry、quota 回復待ち、resume、ログ・event 記録を統合する。
- Codex 起動失敗時の例外を console と event 用の共通エラーテキストへ変換する。
- Codex exec/TUI 前の INDEX 更新 preflight 境界。登録・解除、再入抑止、直列化、実行 root 決定、Codex への委譲を扱う。
- Codex CLI subprocess の実行境界。sandbox、argv、環境、CODEX_HOME、schema、process tracking、JSONL 出力と error 判定を扱う。
- Codex TUI の起動経路。実行環境・argv、callback、call log、feedback、終了結果、起動失敗の処理を扱う。
- 設定オブジェクトの JSON 永続化・復元と検証を担う runtime 設定境界。Codex provider、agent call、oracle review の値とファイル安全性を扱う。
- ファイル・文字列の SHA-256 ハッシュ、内容ハッシュ付き安全な保存、バイナリの粗い判定を提供する。
- doctor preprocess の修復 lifecycle と排他実行を扱う。config、refactor state、.gitignore、.agents の同期、temporary index、修復 commit を担う。
- cmoc の実行時エラーを利用者向けレポートへ変換する。CmocError の保持情報と handled failure の描画規則を提供する。
- invocation 単位の feedback collector と Codex call capability lifecycle を統合する。Unix socket 受付、protocol 検証、drain、degraded 処理、stable event 検出を扱う。
- Codex 起動時の call-scoped stdio MCP feedback reporter。collector 通信、capability payload、JSON-RPC の MCP lifecycle、submit_observation を扱う。
- feedback の repository-local state を管理する中心実装。report cut、generation、current pointer、aggregate、checkpoint、publication、cleanup、recovery、writer lock を扱う。
- agent および machine rule の raw feedback observation を検査・mask・正規化し、fingerprint と content hash に基づき immutable store へ保存する。
- Git subprocess、branch、linked worktree、path 安全性、Git ignore、oracle/realization file の列挙・分類を担う共通境界。
- サブコマンド実行中の JSONL logger。event、warning、step・quota timing、Codex call 集計、ContextVar、feedback detector 連携を扱う。
- repository/worktree/cmoc root、runtime 保存先、timestamp・duration 表示、process-wide cwd 制御を提供する共通 path utility。
- 非対話サブコマンドの primary report 保存を保証する。既存 report 検証、fallback 生成、項目収集、保存失敗処理を担う。
- runtime 情報から fallback primary report を構築する描画入口。template、front matter、terminal 状態、oracle review、feedback publication 状態を report に反映する。
- 非対話末端サブコマンドの fallback primary report 定義を集約する。コマンド別の保存先、タイトル、必須項目、template を提供する。
- realization refactor の state 管理実装。state の読み書き・検証・同期、調査対象選択、再調査要求、安全な path 検査を扱う。
- CLI 実行結果の共有モデルを定義する。terminal result、外部コマンド結果、Codex Structured Output 検証問題、生成物・ログの契約を扱う。
- editing run の worktree 解決と process cleanup の共通境界。run state lock、tracking、worktree identity、join/abandon 復旧を扱う。
- editing run lifecycle の共通実装。session 条件、branch/worktree、state 遷移、process tracking、rollback/commit、INDEX 更新、差分許可判定を扱う。
- editing run の fork、join、abandon report を保存する共通処理。YAML Front Matter、Markdown、実行段階、結果、変更 path の安全な描画を扱う。
- session state の dataclass schema、状態値、永続化・復元・検証を担う。session/run branch 対応、lock、active session 検索、path 安全性を扱う。
- Windows toast 通知と Codex TUI callback の非致命的 transport 境界。通知生成・送信、callback の invocation-local 状態、turn 重複排除、cleanup を扱う。

## Read this when
- commons の公開入口やパッケージ初期化を確認するとき。
- 共通 runtime API の公開シンボルや、複数実行経路で共有される runtime 機能の入口を確認するとき。
- INDEX.md の preflight、更新、hash 検証、復元、lock、commit の挙動を調査・変更するとき。
- prompt editor の作業ファイル、エディタ選択、入力抽出、保存、cleanup を調査・変更するとき。
- 最外側 CLI の実行順序、終了処理、例外分類、終了コード、report、feedback、診断ログを調査・変更するとき。
- Codex exec/TUI の公開 API と委譲境界を確認するとき。
- Codex exec の retry、quota、resume、Structured Output 検証、ログ・event 記録を調査・変更するとき。
- Codex 起動失敗のエラーテキスト整形を確認・変更するとき。
- Codex 呼び出し前の indexing preflight、再入防止、lock、root 決定、委譲境界を調査・変更するとき。
- Codex CLI の起動引数、sandbox、環境、schema、process tracking、JSONL protocol/error 解釈を調査・変更するとき。
- Codex TUI の起動、callback、feedback、call log、終了処理を調査・変更するとき。
- config の JSON 保存・復元、既定値補完、Codex/oracle review 設定検証、symlink・特殊 file 安全性を調査・変更するとき。
- 内容ハッシュ、ハッシュ名付き保存、一時ファイル置換、regular file/symlink、バイナリ判定を調査・変更するとき。
- doctor の修復、lock、temporary index、同期対象、修復 commit、既存差分復元を調査・変更するとき。
- CmocError の属性、error rendering、ログ初期化前の handled failure 表示を調査・変更するとき。
- feedback observation の収集、collector lifecycle、capability、degraded 境界、doctor 検査、stable event detector を調査・変更するとき。
- feedback reporter の MCP JSON-RPC、collector 通信、payload 検証、submit_observation を調査・変更するとき。
- feedback report cut、publication、checkpoint、aggregate、cleanup、discard、recovery、active state integrity を調査・変更するとき。
- feedback raw observation の schema、secret masking、evidence path、fingerprint、ID、重複排除、atomic 保存、pending 判定を調査・変更するとき。
- Git command、branch/worktree、path 安全性、ignore、oracle/realization 分類を調査・変更するとき。
- event log、warning、step/quota timing、Codex call 集計、ContextVar logger、feedback detector 接続を調査・変更するとき。
- root 解決、runtime 保存先、timestamp/duration 表示、cwd lock を調査・変更するとき。
- primary report の保存保証、fallback 生成、項目統合、保存失敗時の処理を調査・変更するとき。
- fallback primary report の template、front matter、terminal 状態、oracle review、feedback 状態の描画を調査・変更するとき。
- コマンド別 primary report の保存先、タイトル、必須項目、template 登録を調査・変更するとき。
- realization refactor state の schema、同期、調査対象選択、再調査、安全な保存を調査・変更するとき。
- terminal result、外部コマンド結果、Codex 出力検証、生成物・ログ path の共有契約を調査・変更するとき。
- editing run の join/abandon、worktree lookup、process tracking、process group cleanup を調査・変更するとき。
- editing run の開始、state 遷移、branch/worktree lifecycle、差分検査、INDEX 更新、rollback/commit を調査・変更するとき。
- editing run report の保存先、front matter、Markdown、実行結果、変更 path の描画を調査・変更するとき。
- session state の schema、JSON 永続化、branch 対応、lock、active session、path 検証を調査・変更するとき。
- Windows toast、TUI agent-turn-complete callback、重複排除、通知 transport の非致命性を調査・変更するとき。

## Do not read this when
- 個別の runtime helper の実装詳細だけを調査するとき。
- 特定の runtime 機能、個別 CLI、Codex preflight の具体的挙動だけを調査するとき。
- prompt builder、schema、または個別 runtime module の仕様だけを調査するとき。
- prompt の内容・skeleton 生成だけ、または prompt editor を使わない入力処理を調査するとき。
- 個別サブコマンドの業務処理・引数定義、または専用の report/log/error 実装だけを調査するとき。
- Codex exec/TUI の具体的挙動を調査するとき。
- TUI の起動、または subprocess 環境・schema など exec 補助の個別処理だけを調査するとき。
- 例外クラスや通常のログ処理など、起動失敗テキスト変換以外を調査するとき。
- Codex subprocess 本体、agent call parameter、または indexing アルゴリズム自体を調査するとき。
- agent call の業務ロジック、編集対象内容生成、Codex 境界と無関係な一般 process 管理を調査するとき。
- Codex 設定上書き自体、設定定義、TUI 以外の呼び出し経路、共通 logging/feedback/path 詳細を調査するとき。
- 設定型・既定値そのもの、CLI 実行、agent call、oracle review の個別ロジックを調査するとき。
- hash を使う呼び出し側の同期・列挙規則、出力 schema、CLI 一般規則を調査するとき。
- doctor の正本仕様、個別同期ロジック、Git/path/error/feedback の専用実装を調査するとき。
- TerminalResult や通常成功結果、個別処理の error 生成、通常ログの詳細を調査するとき。
- 観測 payload の永続化仕様、reporter schema、一般 logging・Git context・別 runtime helper を調査するとき。
- observation 保存形式、feedback 仕様全体、feedback と無関係な MCP/CLI/runtime を調査するとき。
- 低レベル observation 保存、report 集約・正規化・検証、CLI 引数、Markdown 内容生成、正本仕様を調査するとき。
- collector/reporter の上位処理、feedback 正本仕様、低レベル JSON/ID utility だけを調査するとき。
- Git/path 分類と無関係な CLI、oracle/realization の仕様内容、session orchestration だけを調査するとき。
- サブコマンド固有処理、ログ正本仕様、feedback 検出・保存そのものを調査するとき。
- primary report の項目定義・描画形式、ログ、path、terminal result 型、個別 app specification を調査するとき。
- report の保存・生成処理、個別 report 内容、TUI 通知だけを調査するとき。
- 個別の report 内容、保存処理、TUI-only の挙動を調査するとき。
- refactor state と無関係な処理、state の具体的 field/JSON 形式だけを調査するとき。
- 特定サブコマンドの結果内容、console/file log、Codex exec 手順や正本ルールを調査するとき。
- Git worktree の低レベル操作、pidfd/process signal の個別 primitive、editing run 外部仕様を調査するとき。
- workload 固有編集、state schema、Git 低レベル実装、INDEX アルゴリズム自体を調査するとき。
- 個別 report 仕様、canonical 配置判断、ログ収集、run state 管理を調査するとき。
- CLI 固有処理、state 正本仕様、state schema の詳細だけを調査するとき。
- 通常の terminal result、最外側 lifecycle、通知本文仕様、通知と無関係な runtime 機能を調査するとき。

## hash
- 4092c9567c064cc20f31d1c0f03a418e9dfea39446a2e827af28bc5cdca02347

# `config`

## Summary
- 設定の正本を複製せず、oracle 側で定義された cmoc 設定型を realization 側で再公開する互換入口。既存の config 参照経路を維持するための階層。

## Read this when
- 既存利用者や realization 側で config 経由の設定型参照を維持・確認するとき。
- 互換入口の有無や、設定型の定義元を oracle 側へ統一する必要があるとき。

## Do not read this when
- 設定型の構造・値・仕様そのものを確認または変更するときは、oracle 側の定義元を直接読む。
- config 経由の参照を新規実装する判断だけが必要なときは、利用側の参照経路を直接確認する。

## hash
- 210d91011e2bae467ef89956c606fa11dd52f78e193037b7f4f30993c3d2b11b

# `main.py`

## Summary
- Typer で構成された cmoc CLI の最上位入口。doctor、tui、indexing、feedback と、session・oracle・realization・run のサブコマンド群を登録し、各処理実装へ振り分ける。
- Click/Typer の互換処理と CLI 引数解析エラーの cmoc 形式への変換を閉じ込め、console script から `cmoc` としてアプリケーションを起動する。

## Read this when
- cmoc の CLI コマンド構成、サブコマンド登録、起動入口を変更または調査するとき
- Typer と Click のバージョン互換、補完 probe、または CLI 引数解析エラーの報告形式を確認するとき
- 新しい最上位コマンドやサブコマンドを追加し、対応する実装への接続箇所を確認するとき

## Do not read this when
- 特定サブコマンドの処理内容や業務ロジックを調査するときは、対応する `sub_commands` 配下の実装を直接読む
- `CmocError` やエラー描画の共通仕様そのものを調査するときは、`cmoc_runtime` と該当する app specification を読む
- oracle、realization、session、run の内部処理を変更するときは、この CLI 登録層ではなく各サブコマンド実装と対応仕様を読む

## hash
- 36ab2a93a49ac1ed50f74e548bdf0eed0219fade8a647b8bd930a8bde81c3004

# `oracle.py`

## Summary
- `src` 起動時に正本側 `oracle.*` パッケージを解決するための互換用 package shim。`oracle/src/oracle` をパッケージパスとして再公開し、正本ソースが存在しない場合は `ModuleNotFoundError` を送出する。

## Read this when
- `src` だけを起動した際の `oracle.*` パッケージ解決や互換 import の挙動を確認するとき。

## Do not read this when
- 正本側 `oracle.*` の実装内容を確認するときは、直接 `oracle/src/oracle` 配下を読む。
- `src` の通常の CLI 実装や、package shim と無関係な import 経路を調査するとき。

## hash
- e476648f073484004b64741d40d6d373fab223e001be01ac8051f9c5ab15e095

# `sub_commands`

## Summary
- サブコマンド実装をまとめるディレクトリ。apply、doctor、feedback、indexing、oracle、realization、review、run、session、tui の各 CLI 入口または実装パッケージへ進むためのルーティング起点となる。

## Read this when
- cmoc のサブコマンド実装の配置や、対象サブコマンドの CLI 入口を特定するとき。
- 複数のサブコマンドにまたがる実装構成を確認し、個別の下位対象へ進む必要があるとき。

## Do not read this when
- 特定サブコマンドの実行フローや処理内容を直接確認できる場合は、対応する下位ファイルまたはパッケージを直接読むとき。
- サブコマンド共通ランタイム、正本仕様、agent prompt、Structured Output schema など、別の対象が直接定義する内容だけを確認するとき。

## hash
- e9e67512829b6205e387bd76d8a036c9bcbb3ed84b729f79fe5a1028010ace67
