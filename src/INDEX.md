# `acp`

## Summary
- `acp` 互換公開入口と `acp.builder` 配下の builder 群を扱う realization package。canonical な `oracle` 側実体への委譲や、apply・indexing・oracle・session・TUI・quota probe の互換入口を確認するための上位入口。

## Read this when
- `acp.*` の公開参照を維持・削除・移行する判断が必要なとき。
- `acp.builder` の互換 import 経路や、対応する canonical な oracle builder への委譲を変更するとき。

## Do not read this when
- canonical な builder の正本仕様や具体的な実装詳細だけを確認したいとき。
- CLI 実装、TUI 本体、ループ制御、state 遷移など `acp` の互換入口以外を調査するとき。

## hash
- fc91b6e1cc36b84a70e7c178883dc7d02615f92e913b2fe01900e1917b2119c7

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行ライフサイクル、Codex exec/TUI 起動、設定・Git・パス・ログ・状態・エラー・Ollama 管理、INDEX.md 生成など、複数のサブコマンドから利用される横断機能を提供する。
- 各 runtime_* モジュールが個別責務の実装を担い、cmoc_runtime.py と runtime_codex.py は共通 API の再公開入口として機能する。

## Read this when
- 複数の CLI サブコマンドにまたがる runtime 共通処理を調査・変更するとき
- Codex 実行、設定永続化、Git/worktree、runtime path、ログ、state、エラー処理、Ollama preflight などの担当モジュールを特定するとき
- commons パッケージの公開 API や runtime helper の構成を確認するとき

## Do not read this when
- 特定のサブコマンド固有の業務処理や CLI 引数仕様だけを調査するとき
- 利用者向けの正本仕様や出力契約だけを確認するときは、対応する oracle 文書を直接読む
- 特定機能の実装詳細が明確な場合は、このディレクトリ全体ではなく対応する runtime モジュールを直接読む

## hash
- c85be745a40dda3b6d782fb13fa49f03f088e198776efa1c3153a4309aae4818

# `config`

## Summary
- 設定定義を直接実装せず、oracle 側の設定型を `config.*` として再公開する互換入口。既存利用者向けの import 面を確認するためのディレクトリ。

## Read this when
- `config` または `config.cmoc_config` の import・公開 API を維持、変更、確認するとき。
- oracle 側の設定定義と realization 側の互換ブリッジの関係を確認するとき。

## Do not read this when
- 設定仕様や設定定義そのものを確認するときは、oracle 側の設定定義を直接読む。
- 設定を利用する個別機能だけを変更するときは、該当する利用側コードを直接読む。

## hash
- daa5ed72b11813f850abdb829e763dbf883b1abeace1419ea40a5fd5a555af2f

# `main.py`

## Summary
- Typer/Click を用いた cmoc CLI のルートアプリケーション定義。共通の CLI 引数解析エラーを cmoc 形式へ変換し、doctor、tui、session/apply/oracle の各サブコマンド、eval-oracle、indexing の公開入口を下位実装へ接続する。

## Read this when
- cmoc の CLI コマンド、サブコマンド、option、列挙型、Typer/Click のエラー処理を変更または確認するとき。
- CLI 入口から各サブコマンド実装への接続関係を確認するとき。
- `cmoc` の console script 起動や補完時の Click 例外処理を確認するとき。

## Do not read this when
- 特定サブコマンドの処理本体、ブランチ操作、oracle 編集、TUI 起動、INDEX 更新の詳細を確認したいときは、対応する `sub_commands` 配下の実装を直接読む。
- oracle の仕様やエラー処理の正本を確認したいときは、参照コメントに示された `oracle/doc` の文書を読む。

## hash
- a9f1d5f48b7a59503d89c92100778c38f406dfbc3bb67168ac4890185ba3f1e7

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
- サブコマンド実装を集約するディレクトリ。apply、doctor、eval_oracle、indexing、oracle、review、session、tui の各実装入口を含み、個別サブコマンドの実行フローや下位実装への導線を確認する起点となる。

## Read this when
- サブコマンドの実装入口、CLI 実行フロー、または package 構成を確認・変更するとき。
- apply、oracle、session、tui など、配下の特定サブコマンドの責務や関連する下位実装を特定するとき。

## Do not read this when
- 共通 runtime、Git、worktree、Codex 実行基盤など、サブコマンド固有ではない処理だけを確認・変更するとき。
- 特定サブコマンドの下位処理や仕様文書を直接確認すべき場合。

## hash
- 8589adf440b36eb38bb02e012dcea45ce790ed97b206b749826294a63dcb7fb3
