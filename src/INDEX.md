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
- commons パッケージの初期化と、cmoc の共通 runtime API・実行制御・設定・Git・状態・ログ・レポート・feedback・editor handoff などを担う下位モジュールへの入口を提供する。
- INDEX.md の検査・生成・更新 lifecycle、Codex exec/TUI の起動境界、runtime 設定・パス・結果・エラー、feedback や editing run の状態管理など、複数の CLI 実行経路で共有される実装を対象とする。
- 特定の機能を調査する場合は、commons 内でその責務を直接担う runtime モジュールへ進むための上位ルーティング対象である。

## Read this when
- commons の初期化や共通 runtime API の公開範囲を確認するとき
- CLI 実行、Codex subprocess、設定、ログ、Git worktree、状態管理、レポート、feedback、editor input handoff など、複数機能にまたがる共通 runtime の入口を探すとき
- INDEX 更新 lifecycle や editing run lifecycle の共通実装へ進むべきか判断するとき

## Do not read this when
- 特定の runtime helper、CLI サブコマンド、Codex exec/TUI、feedback、report、state などの内部実装だけを確認したいとき
- 正本仕様、Structured Output schema、個別の protocol やデータ型の定義を直接確認すれば足りるとき
- commons の共通処理を利用せず、対象機能固有の実装や仕様だけを調査するとき

## hash
- 8611d119813d2ed29b22d2d9c0c3ca2212dd642a786f10ed58590b0c47092c5a

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
