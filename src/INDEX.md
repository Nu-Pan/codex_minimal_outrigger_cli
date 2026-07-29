# `acp`

## Summary
- ACP互換の公開入口を扱い、既存の`acp.*`参照を`oracle.*`または実体モジュールへ移行する際の入口となる。
- ACP builder realizationのパッケージ。oracle実装への互換入口、builder共通処理、oracle・realization・session・TUI・indexing向けadapter、quota probeのfallbackをまとめ、各下位要素への入口を提供する。

## Read this when
- `acp`という公開名の存廃や、既存参照をoracle側の実体へ切り替える導線を確認したいとき。
- ACP builder realizationの構成、互換import、oracle実装への委譲、builder共通処理、各builder adapterの入口を確認したいとき。

## Do not read this when
- `acp`配下の具体的な実装内容や移行先の詳細だけを確認したいときは、該当する実体モジュールを直接読む。
- canonicalなoracle builderの仕様・実装、またはTUI・CLI・sessionなど利用側の挙動を確認したいときは、それぞれの対象を直接読む。

## hash
- 37a5cdccd2d3f31d506aaed6cc61ba09b39548bbdba0780b9ea25a7280fc4b09

# `basic`

## Summary
- `basic.*` の互換 import を維持する公開入口群。ACP 型、path model、構造化文書 API を実体定義から再公開し、`basic` 側に実装や正本仕様を複製しない。

## Read this when
- `basic.*` 経由の公開名や互換 import の維持・廃止を判断するとき。
- ACP 型、path model、構造化文書 API の realization 側での再公開関係を確認するとき。

## Do not read this when
- 各 API の正本仕様や実装本体を確認したいときは、対応する oracle 側を直接読む。
- `basic.*` の公開面や互換 import に関係しない処理を調査・変更するとき。

## hash
- 6427f271674f13de9f39976c4fe0d10226ad4c7573c6fa05a58ee5db32f274b7

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
- cmoc 共通 runtime helper を提供する commons パッケージの初期化。commons 配下の共通実行時機能を確認するときの入口。
- cmoc runtime の公開 API を集約し、CLI、Codex、設定、状態、Git、ログ、パス、結果、エラーなどの共通部品を再エクスポートする。
- INDEX.md の検査・生成・既存 entry 再利用・Structured Output 検証・書き込み・commit・排他制御を担う indexing lifecycle。
- エディタから AI Agent 用 prompt を受け取り、入力ファイルの準備、エディタ起動、コメント除去、読み込み、関連する ignore 保証を担う。
- CLI サブコマンド共通の work root 検査、doctor preprocess、ログ、step 通知、完了表示、終了コード化、例外処理を管理する。
- Codex exec と TUI の実行 API を公開する共通入口。
- Codex exec の subprocess 実行、Structured Output 検証、capacity/quota retry、resume 継続、ログ・イベント記録を制御する。
- Codex CLI 呼び出しの console 通知と、起動失敗時の共通エラー整形を担う。
- Codex exec/TUI 起動前の INDEX 更新 preflight、再入抑止、直列化、対象 root 算出、実行本体への委譲を担う。
- Codex CLI subprocess の起動環境、sandbox・cwd・CODEX_HOME・argv・schema、process tracking、停止、JSONL 出力解析、エラー判定を扱う。
- Codex TUI の起動、設定上書き、実行環境、ログ、イベント、成功・失敗時の戻り値と例外処理を扱う。
- 設定値と JSON 永続化形式の変換・検証、既定値補完、不正設定のエラー化、安全な設定ファイル読み書きを担う。
- ファイル内容・文字列の SHA-256、ハッシュ付き一時ファイルの安全な保存、バイナリ判定を提供する。
- doctor preprocess の排他、修復対象同期、Git index の退避・合成・復元、修復 commit、追跡状態検証を担う。
- cmoc の実行時例外を利用者向け Markdown エラーレポートへ変換し、概要、復旧案、詳細、call stack を組み立てる。
- Git コマンド、branch・commit・status、managed worktree、ignore 状態、oracle/realization file の path 分類を扱う共通境界。
- サブコマンド単位の JSONL ログ、step timing、quota 待機時間、現在の logger 管理を担う。
- repository・worktree・cmoc root の解決、標準保存先、timestamp・duration 整形、衝突回避、cwd 切替を提供する。
- oracle/realization file の調査履歴 state の読み書き・検証・同期、対象列挙、未調査対象選択を担う。
- Codex exec の構造化出力、外部コマンド結果、実行に伴うログ・生成物・設定パスを表す結果型を定義する。
- editing run の worktree 解決、process identity の記録・検証、Codex 子プロセス追跡・停止、tracking file cleanup を担う。
- editing run の開始、state 遷移、commit、差分分類、INDEX 更新、cleanup 判定を一体で扱う lifecycle 実装。
- editing run の fork と lifecycle の Markdown レポートを YAML Front Matter 付きで生成・保存し、変更パスなどを安全に整形する。
- session state の JSON 復元・検証・保存、session/run schema、branch からの ID 解決、symlink 防止、fork 排他 lock を担う。

## Read this when
- commons の共通 runtime 機能やパッケージ入口を確認するとき
- 複数の runtime 領域を横断する公開 API や依存関係を調査するとき
- INDEX.md の生成・検査・更新・commit・preflight を変更するとき
- prompt editor または TUI の入力保存・編集フローを変更するとき
- CLI サブコマンド共通の実行 lifecycle、ログ、終了処理を変更するとき
- Codex exec/TUI の起動、retry、resume、process 管理、出力解析を変更するとき
- 設定、Git、path、content、doctor、error、logging、state、refactor の各 runtime 挙動を変更するとき
- editing run の process cleanup、state lifecycle、差分管理、report 生成を変更するとき

## Do not read this when
- 単一の runtime 機能の詳細だけを調査する場合は、該当する個別モジュールへ直接進む
- 利用者向け正本仕様、prompt template、INDEX entry schema、run/state の仕様を確認する場合は対応する oracle 文書を読む
- 特定の CLI サブコマンド固有の業務フローだけを調査する場合は、その command 実装を読む
- Codex 実行本体、TUI、設定、Git、path などの個別責務を横断して確認する必要がない場合

## hash
- 0c242605393c730b05f2b74d7b6d6f24d9c4592c20798028394c9b86d2bdc380

# `config`

## Summary
- 設定モジュールの互換入口を提供するディレクトリ。`__init__.py` は `config.*` 参照を成立させ、`cmoc_config.py` は oracle 側の設定型を定義せず realization 側から再公開する。設定仕様の確認先ではない。

## Read this when
- 既存利用者の `config` または `config.cmoc_config` 参照を維持・確認するとき。
- 設定型の import 経路や互換入口の有無を調べるとき。

## Do not read this when
- 設定定義の内容や仕様そのものを確認するときは、oracle 側の設定定義を直接読む。
- 設定参照を新規に追加する実装判断では、利用側の参照経路を直接確認する。

## hash
- fbc828970884bf16f7e7e6174e3461888e3c4000d754454ba9794e1d2c99d6f2

# `main.py`

## Summary
- Typer を用いた cmoc CLI の主要エントリーポイント。doctor、tui、indexing と、session・oracle・realization・run の各サブコマンドを登録し、対応する実装関数へ委譲する。CLI 引数解析エラーは cmoc 形式のエラーレポートへ変換し、自動補完時は副作用を抑制する。各サブコマンド実装や CLI 全体の構成を確認する際の入口。

## Read this when
- cmoc の CLI コマンド、サブコマンド、option、Typer/Click の引数解析、エラー変換、自動補完の挙動を変更・調査するとき
- 特定のサブコマンド実装へ進む前に、CLI からの登録名と委譲先を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や永続化・worktree 操作の詳細を確認したいとき。対応する sub_commands 配下の実装を直接読む
- CLI とは無関係な runtime、oracle、realization の内部処理を調査するとき

## hash
- 2fc467906ef010b3f9c4d51a1600ba115332880dd4658767606f556b60c8e8d7

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
- サブコマンド実装をまとめるディレクトリ。apply、doctor、indexing、oracle、realization、review、run、session、tui の各 CLI 入口または実装パッケージへの入口を提供する。

## Read this when
- サブコマンド実装の構成や、対象サブコマンドの実行フロー・ライフサイクル処理・TUI 起動処理の所在を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細処理、共通ランタイム、oracle 文書・実装、index 更新の具体的処理だけを調査する場合は、対応する下位実装や参照先を直接読む。

## hash
- 043f8e96e1f1dd241b4ae90b25c8ff481ec467f97f3ceecb2f3e7791f5f10f91
