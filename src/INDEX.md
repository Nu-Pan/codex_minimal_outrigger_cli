# `acp`

## Summary
- `acp` の互換公開入口と、ACP builder realization 層への導線を扱う。`acp.*` 参照の存続判断や builder 下位要素へのルーティングが必要な場合に使う。

## Read this when
- `acp` 互換公開名の存廃や、`oracle` 側実体への移行導線を確認するとき。
- ACP builder の互換 import、canonical/oracle builder への委譲、または下位 builder package の入口を確認するとき。

## Do not read this when
- `acp` 配下の具体的な実装や移行先の詳細を確認したいときは、該当する実体モジュールを直接読む。
- TUI の挙動、apply fork のループ制御、session の状態遷移など、builder 入口以外の詳細を調べたいときは対応する実装箇所へ進む。

## hash
- 575819effad444213cb4b79b85e77091992dbbb71ff8f15ad2625f7069aec538

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
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 実行、Codex、設定、Git、パス、ログ、状態、Ollama、INDEX.md 更新などの実装入口を提供する。

## Read this when
- commons 配下の共通 runtime 機能の構成や、対象となる個別 helper の入口を確認するとき
- 複数の runtime 機能にまたがる公開 API、実行ライフサイクル、共通状態管理の実装を調査するとき

## Do not read this when
- 特定機能の詳細を調べる場合は、commons 配下の対応する個別 runtime モジュールを直接読むとき
- CLI サブコマンド固有の業務処理や利用者向け仕様だけを調べるとき

## hash
- 9289ee2311354fc904692590199976cdf4622b42111263f57e1c04634d00d60d

# `config`

## Summary
- `config.*` 参照を既存利用者向けに維持するための互換入口群。ここでは設定の実体を持たず、正本の oracle src を再公開する経路だけを確認する。
- `config.cmoc_config` から Cmoc 設定型を再公開する入口。設定定義そのものではなく、既存の公開参照を壊さないための接続点として読む。

## Read this when
- `config` からの import 経路を維持・確認したいとき。
- `config.cmoc_config` 経由で Cmoc 系の設定型を参照したいとき。
- 設定の正本を変更せず、互換入口の有無だけを確認したいとき。

## Do not read this when
- 設定仕様そのものを確認したいときは、正本側の oracle src を読む。
- `config.*` 以外の公開面や新規設定追加を扱いたいとき。
- 設定定義の項目意味や保存仕様を調べたいとき。

## hash
- c121a67917bdcc7850097d1a5fc153afb19f375da55ada79794c9c5739b22514

# `main.py`

## Summary
- Typer ベースの cmoc CLI のルート定義。共通エラー変換、トップレベルコマンド、session/apply/review のサブコマンド、console script の起動入口を扱う。CLI コマンドの追加・変更、引数や option の定義、コマンド実装への接続を調べる際の入口。

## Read this when
- cmoc の CLI コマンド一覧、サブコマンド階層、option の既定値や列挙値を確認するとき
- Typer・Click の引数解析エラー処理や CLI 起動方法を変更するとき
- CLI 入口から各サブコマンド実装への接続を追うとき

## Do not read this when
- 特定サブコマンドの処理内容や業務ロジックだけを調べるときは、対応する sub_commands 配下の実装を直接読む
- oracle のエラー処理・usage・サブコマンド仕様そのものを確認するときは、参照コメントに示された oracle file を読む

## hash
- 81225c8de9d313ba42585b37881ac6abea55daa56d41186a024931538e368802

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
- 複数の CLI サブコマンド実装と review 系処理を収める `src/sub_commands` の入口。apply、doctor、indexing、review、session、tui の各サブコマンドについて、実行制御やライフサイクル処理を確認する際に進む対象を示す。

## Read this when
- apply、doctor、indexing、review、session、tui のサブコマンド実装を確認または変更するとき。
- サブコマンドごとの実行フローや、review の対象列挙・finding 処理・レポート生成・INDEX 統合を調査するとき。

## Do not read this when
- サブコマンド共通の runtime、設定、lock、process、session state、Git 操作の一般実装だけを調査するときは、対応する共通モジュールへ直接進む。
- 特定サブコマンドの詳細処理だけを調査するときは、この階層全体ではなく該当する実装ファイルまたは下位 package へ直接進む。

## hash
- de7fc4ec0d6cb1e16afdae354b831d945084676d2c67aea364dc51066adba52e
