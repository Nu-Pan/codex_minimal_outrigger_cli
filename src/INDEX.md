# `acp`

## Summary
- acp 互換名前空間の公開入口と、oracle 実装へ委譲する builder adapter 群への上位入口を提供する。公開 import 経路や処理別 adapter の配置関係を確認する際の起点。

## Read this when
- acp という公開入口の存廃や既存参照から oracle 側実体への移行経路を判断するとき
- acp.builder 配下の互換 import 経路、共通 builder 処理、処理別 adapter の構成を確認するとき

## Do not read this when
- acp 配下の具体的な実装、仕様、入出力、利用箇所を調べるときは、対応する oracle 実装や参照元を直接読む
- 個別 builder adapter の詳細実装や、acp と無関係な CLI 処理だけを調べるとき

## hash
- 9086a870ac2e3d3c32195eba2c4441af8578b4de9f66aee07082e825f57eaf2b

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
- commons パッケージの共通 runtime API と、配下の個別 runtime 実装への入口を提供する。
- CLI、Codex subprocess、設定、Git、状態、ログ、feedback、report、run lifecycle など、複数の実行経路で共有される処理を扱う。

## Read this when
- commons 配下の共通 runtime 機能の責務や公開入口を確認するとき
- 複数の CLI・Codex 実行経路にまたがる runtime 処理の実装箇所を探すとき
- 対象機能に対応する commons 配下の個別 runtime モジュールへ進む前に、パッケージ全体の構成を把握するとき

## Do not read this when
- 特定の runtime 機能の実装詳細だけを確認したいとき
- 個別の CLI サブコマンド、正本仕様、または下位プロトコルの詳細を直接確認すれば足りるとき

## hash
- 1d88a39b97a69d3ab633efed7583550b5b6408a9b46c242623515b107959e67c

# `config`

## Summary
- config.* 参照を維持するための互換入口。
- oracle 側の cmoc 設定型を realization 側の config.cmoc_config から再公開する経路への入口。

## Read this when
- config からの import 互換性を確認するとき。
- realization 側の config.cmoc_config における設定型の再公開経路を確認するとき。

## Do not read this when
- 設定型の定義や設定値の仕様そのものを確認したいとき。
- config.cmoc_config の参照経路を新規追加・変更する実装判断を行うとき。

## hash
- 8571722dab57a84f72fd99845c9e5c092cb64b05d9f5ac72e976209acca14524

# `main.py`

## Summary
- Typer を用いた cmoc CLI のルート入口を定義し、共通検証、TUI、セッション・oracle・realization・run・feedback 操作、INDEX 更新の各サブコマンドへ接続する。
- Click/Typer の互換処理と CLI 引数解析エラーの cmoc 形式への変換を集約する、CLI 起動時の境界層である。

## Read this when
- cmoc の CLI ルート構成、サブコマンドの登録、console script からの起動経路を確認するとき。
- Typer と Click の互換処理、補完 probe の扱い、CLI 引数解析エラーの報告形式を変更または調査するとき。
- サブコマンド実装へ進む前に、どの CLI 操作がどの実装入口へ委譲されるかを確認するとき。

## Do not read this when
- 個別サブコマンドの処理内容、業務ロジック、oracle・realization・session・run の内部動作だけを確認したいとき。
- CLI の起動や引数解析に関係しない共通ランタイム、TUI、feedback、indexing の内部実装を直接調査するとき。

## hash
- ebbe5d4f9679a37c97d022394881ba83a1f198ead6fa3bca88743fadeec0a447

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
- CLI サブコマンド実装のパッケージ入口。doctor、feedback、indexing、oracle、realization、run、session、tui など、各サブコマンド固有の実行フローへ進むための上位ルーティング対象。
- サブコマンドごとの CLI 入口、実行制御、状態管理、agent call、worktree 操作、report 処理などを確認・変更するときに、該当する下位実装へ進む起点となる。
- apply と review は現時点で実装本文がなく、将来実装が追加された場合にのみ個別の下位入口となる。

## Read this when
- CLI サブコマンドの実装構成や、どのサブコマンド固有実装を読むべきか確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui などのサブコマンド実行フローを調査・変更するとき。
- 対象サブコマンドの責務が複数の下位実装に分かれており、個別ファイルへ進む前の package 境界を確認したいとき。
- apply または review の実装が追加され、その実装入口を確認するとき。

## Do not read this when
- サブコマンド共通ランタイム、共通 prompt editor、report writer、Git 操作、state 永続化などの具体的な挙動だけを確認したいときは、対応する共通実装を直接読む。
- サブコマンドの正本仕様や lifecycle 仕様だけを確認したいときは、対応する仕様書を直接読む。
- 特定サブコマンドの実装本文をすでに特定しており、上位の package 構成や入口を確認する必要がないとき。
- apply または review に実装がまだ存在しない状態で、その具体的な処理内容を確認しようとするとき。

## hash
- 3b788be6586c73b5da0a93fa33952b37d59ef270878fdc6b10dac5bb6162b18e
