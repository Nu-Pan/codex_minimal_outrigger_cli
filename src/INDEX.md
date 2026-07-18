# `acp`

## Summary
- ACP 互換の公開入口と、ACP parameter builder の realization 側入口をまとめるパッケージ。canonical builder への委譲や既存 import の互換維持、機能別 builder への導線を扱う。

## Read this when
- `acp` 公開入口の存廃や既存参照の互換維持を判断するとき。
- ACP parameter builder の realization 側入口、canonical builder への委譲、または機能別 builder を調査・変更するとき。

## Do not read this when
- canonical な builder の仕様・実装内容だけを確認したいとき。対応する `oracle.acp_builder` 側を読む。
- CLI のループ制御、state 遷移、TUI 起動後の処理など、ACP の公開入口や parameter builder 以外の挙動を調査するとき。対応する上位実装または実体モジュールを直接読む。

## hash
- ad852e72b72fda5b0728c292e6c863f8024e25a526244d93299652f0269328ee

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
- cmoc 共通 runtime helper を集約する commons パッケージ。CLI 実行ライフサイクル、Codex exec/TUI、設定、Git、パス、ログ、状態、エラー、doctor、Ollama、INDEX 更新などの共通機能を扱い、commons 配下の個別 runtime 実装を確認・変更する際の入口となる。

## Read this when
- 複数のサブコマンドや実行方式にまたがる共通 runtime 機能の責務や公開 API を確認するとき
- CLI 実行、Codex 呼び出し、設定・Git・パス・ログ・状態管理などの共通処理の実装箇所を選ぶとき
- commons 配下の個別 runtime helper を利用・変更する前に、関連する共通境界を確認するとき

## Do not read this when
- 特定の runtime helper の実装詳細だけを確認したいときは、対応する個別 runtime モジュールを直接読む
- 特定サブコマンドの業務処理や利用者向け仕様だけを調査するときは、該当する command 実装または oracle 文書を直接読む
- INDEX.md のエントリー内容や正本仕様だけを確認したいときは、indexing の oracle 文書を読む

## hash
- 36ba5e3b8613a16d7c1980911d2d096735819099b052147b55d8a0cec7b6c7f2

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
- cmoc の Typer CLI アプリケーション定義。トップレベルおよび session、apply、oracle 配下のサブコマンドを登録し、各実装モジュールへ委譲する実行入口。CLI 引数解析エラーの共通変換、補完時の副作用抑制、scope option と console script 起動も扱う。

## Read this when
- cmoc の CLI コマンド、サブコマンド、option、scope 値、引数解析エラー処理、補完動作、または console script の起動経路を変更・調査するとき。

## Do not read this when
- 特定サブコマンドの業務処理や branch・worktree 操作の詳細を調査するときは、対応する sub_commands 配下の実装を直接読む。
- oracle review、oracle edit、apply fork などの仕様詳細だけを確認するときは、参照されている oracle 文書を直接読む。

## hash
- ccb042da55c6aa724f6c6810135c48c7ecaee2dfc4da1ead01512324a4c4387f

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
- サブコマンド実装を配置するパッケージ。apply、doctor、oracle、review、session、indexing、tui などの CLI 実行入口と、各処理の下位実装への導線を扱う。

## Read this when
- サブコマンドの実装構成や CLI 実行入口を確認・変更するとき。
- apply、oracle、session、tui など特定サブコマンドの lifecycle、state、worktree、report、起動処理の入口を調査するとき。

## Do not read this when
- 共通 runtime、Git、worktree、Codex 実行基盤、indexing の具体的更新処理など、下位または共通実装そのものを直接調査するとき。
- 特定サブコマンドの下位責務だけを扱うときは、対応する下位実装を直接読む。

## hash
- 57fe313fa0ed4e183ebdb529bac3a9798e04558b95faff7cd33f5200069c2390
