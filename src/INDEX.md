# `acp`

## Summary
- `acp` 互換公開入口を扱うディレクトリ。`oracle.acp_builder` の canonical builder を再公開・委譲し、既存の `acp.*` import 経路を維持する。quota probe や TUI、oracle review、realization workload などの adapter 群を下位項目へ案内する。

## Read this when
- `acp.*` の互換 import 経路や公開面を確認・変更するとき。
- canonical builder への委譲、互換 fallback、TUI・review・realization adapter の配置を確認するとき。

## Do not read this when
- canonical な仕様や実装の詳細を確認したいときは、対応する `oracle.acp_builder` 側を直接読む。
- 特定 adapter の内部挙動だけを調査するときは、該当する下位モジュールを直接読む。

## hash
- 583ed1b465ccef74aa9be205e0ec9b5a0a7a8813961bce7f603526a269a2dbc0

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
- cmoc の共通 runtime 機能をまとめる commons パッケージ。CLI 実行ライフサイクル、Codex exec/TUI、設定、Git/worktree、パス、ログ、状態、エラー、Ollama、INDEX 更新など、複数サブコマンドで共有する実装への入口。各機能の詳細確認は配下の担当 runtime モジュールへ進む。

## Read this when
- 複数の CLI サブコマンドにまたがる共通 runtime 処理の担当箇所を探すとき
- Codex 実行、設定、Git/worktree、パス、ログ、状態、エラー、Ollama、INDEX 更新の共通実装を調査・変更するとき
- commons 配下の個別 runtime モジュールへ進む前に、共通機能の構成と入口を把握するとき

## Do not read this when
- 特定サブコマンド固有の業務処理や公開 CLI 仕様を調査するとき
- 正本仕様や retry・quota などの要件を確認するときは、対応する oracle 文書を直接読むとき
- 対象が明確な個別 runtime モジュールの実装詳細を確認するときは、そのモジュールを直接読むとき

## hash
- f2b7058bbffc831d5459925c493c535a326f7dd53942c93934c34e41a1db239e

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
- Typer を使った cmoc CLI のルート定義。doctor・tui・indexing と、session／oracle／realization／run 配下のサブコマンドを登録し、各処理を対応する実装関数へ委譲する。CLI 引数解析エラーの cmoc 形式への変換、補完 probe の扱い、oracle review の scope 定義も含む。各サブコマンドの具体的な処理を確認する場合は、登録先の sub_commands 実装を読む。

## Read this when
- cmoc の CLI 入口、サブコマンド構成、Typer のアプリ階層を確認するとき
- CLI 引数解析エラーや自動補完時の起動挙動を変更・調査するとき
- 新しいトップレベルまたは既存階層のサブコマンドを登録するとき

## Do not read this when
- 特定サブコマンドの業務処理や状態変更の実装を調査するとき
- oracle review、session、run など個別機能の仕様・テストを確認するときは、対応する sub_commands 実装や oracle 文書を直接読む

## hash
- e54ca99e6da1e630eed277aea1d7adc7187cc96ba4e8c9071a285090d8a2845a

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
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、indexing、oracle、realization、review、run、session、tui などの各実行入口と、関連する下位パッケージへ進むための案内を含む。apply は実装未配置で、review も現在は実装本文がない。

## Read this when
- CLI サブコマンドの実装構成や実行入口を確認するとき。
- oracle・realization・run などのサブコマンド群の処理箇所を特定するとき。
- 特定サブコマンドの実行フローや、対応する下位パッケージへの入口を探すとき。

## Do not read this when
- 共通 CLI runtime、git、runtime helper、indexing の具体的処理など、より直接の共通実装だけを調査するとき。
- 特定サブコマンドの内部ロジック、prompt、state、report、findings schema だけを確認したいとき。
- oracle や realization の正本仕様を確認するとき。

## hash
- f578241840ab81ea5626241c0cfe0b87ebf87e4e20a655dd07dad337eb229ec5
