# `acp`

## Summary
- `acp` 互換公開入口と、その配下にある builder 互換入口・adapter 群を扱う。既存の `acp.*` 参照を canonical な oracle／実体モジュールへ移行する際の入口となる。
- `builder` は `acp.builder.*` の互換 import 経路を維持し、各 workload、quota probe、session、TUI、indexing 関連の builder 入口を公開・委譲する。

## Read this when
- `acp` 公開名の存廃や、既存参照を oracle 側の実体へ切り替える導線を確認したいとき。
- `acp.builder` 配下の互換 import、canonical builder への委譲先、または builder adapter の配置を確認・変更したいとき。

## Do not read this when
- canonical builder の仕様・実装本体を確認したいときは、oracle 側の対応モジュールを直接読む。
- 具体的な workload 処理、ACP runtime、CLI、TUI 本体、または `acp.builder` 内部の個別挙動を調査したいときは、該当する実体モジュールを直接読む。

## hash
- b92851f6133acc8c8c2e709ba057b123512f1442d8eeaef3ab49a0146ddb9703

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
- cmoc の共通 runtime 機能をまとめる commons パッケージ。Codex 実行、CLI ライフサイクル、設定、Git、パス、ログ、状態、エラー、Ollama、INDEX 更新など、複数のサブコマンドで共有する実装への入口。
- Codex 実行系、設定・状態管理、Git/worktree 操作、ログ・エラー処理、path/content helper、doctor・preprocess・indexing などの個別 runtime モジュールへ進むためのディレクトリ。

## Read this when
- 複数の CLI サブコマンドで共有される runtime helper の実装箇所を探すとき
- Codex 実行、設定、Git/worktree、path、ログ、状態、エラー、Ollama、doctor、INDEX 更新の共通処理を確認・変更するとき
- commons 配下の個別 runtime モジュールの責務や、公開 API の入口を確認するとき

## Do not read this when
- 特定サブコマンド固有の業務処理や CLI 引数定義だけを変更・調査するとき
- 利用者向けの正本仕様や retry・quota・出力形式などの要件だけを確認したいとき
- 対象が commons 配下の特定モジュールに明確に対応している場合は、その個別モジュールを直接読むとき

## hash
- 5d1ff907c0cd22f146120515ecec20fd47489698c2c53fd466e76414dd4e6ea0

# `config`

## Summary
- 設定の正本を保持せず、oracle 側の cmoc 設定クラスを realization 側から再公開する互換入口。`config.*` および `config.cmoc_config` の既存参照を維持するためのディレクトリ。

## Read this when
- `config` からの import 互換性や、cmoc 設定クラスの realization 側での公開入口を確認するとき。
- 互換モジュールの整理可否や `config.cmoc_config` 参照の削除影響を検討するとき。

## Do not read this when
- 設定項目の具体的な定義・仕様を確認したいときは、oracle 側の設定定義を直接読む。
- 設定を利用する機能の挙動を確認したいときは、各利用側の実装やテストを直接読む。

## hash
- c44790bfc0570bbed52fd98756b3c67ec1812034c8255ae3564f84b88719020a

# `main.py`

## Summary
- Typer を使った cmoc CLI の最上位エントリー。共通の引数解析エラー変換、補完 probe の扱い、主要な command・subcommand の登録、console script の起動を担う。各 command の実処理は対応する sub_commands モジュールへ委譲される。

## Read this when
- CLI の command・subcommand の構成や登録先を確認するとき
- Typer／Click の引数解析エラー処理や補完時の挙動を確認するとき
- cmoc の CLI 起動経路や最上位エントリーを変更・調査するとき

## Do not read this when
- 特定 command の実処理、状態変更、worktree 操作の詳細を確認するとき
- oracle review、session、run、realization など個別機能の実装を確認するときは、対応する sub_commands 配下を直接読む場合
- INDEX.md 更新処理そのものの詳細を確認するときは、indexing 実装を直接読む場合

## hash
- fce4d60b1b6cfd0f6921c6ad6d4b81715d2d369a03738c94136b4461ca29c29b

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
- CLI サブコマンドの実装群をまとめるディレクトリ。apply、doctor、indexing、oracle、realization、review、run、session、tui の各サブコマンド実装と、関連する下位パッケージへの入口を提供する。

## Read this when
- CLI サブコマンドの実装構成や、対象サブコマンドの実行フローを確認・変更するとき。
- 複数のサブコマンドにまたがる CLI 実装の配置や責務を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細処理だけを調査したいときは、該当する下位ファイルやパッケージを直接読む。
- 共通 runtime、indexing 処理、TUI builder、oracle doc などの共通・具体的実装だけを確認するときは、対応する直接の実装を読む。

## hash
- 3807c8676599b9468c96e2d3999b835c9074866cdc6a02e51487a56e7d453a1f
