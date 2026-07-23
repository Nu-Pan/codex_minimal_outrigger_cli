# `acp`

## Summary
- `acp` 互換の公開入口を扱い、既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する際の判断材料を提供する。公開名の存廃や互換導線の確認に使い、具体的な実装・移行先の詳細は下位の実体モジュールを参照する。
- ACP builder の互換入口と parameter builder adapter をまとめ、canonical な oracle 実装の再公開および indexing、quota probe、oracle、realization、session、TUI 系の下位要素への入口を提供する。builder の互換 import 経路や parameter 構築を横断的に調査するときに読む。

## Read this when
- `acp` という公開名を残すべきか、削除できるか判断したいとき。
- 既存の利用者向け `acp.*` 参照を壊さず、`oracle` 側の実体へ切り替える導線を確認したいとき。
- `acp.builder` 配下の builder 互換 import 経路や parameter 構築処理の配置を確認したいとき。
- indexing、quota probe、oracle、realization、session、TUI の builder adapter を横断して調査したいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細だけを知りたいときは、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変更したいときは、ここではなく対象の実装を読む。
- canonical な builder の具体的な仕様・実装だけを確認したいときは、対応する oracle 実装を直接読む。
- builder 以外の ACP 実装や、個別 adapter の詳細だけを調査したいときは、対応する下位要素へ直接進む。

## hash
- 57fcfc3cbd0997698c674bb5b6e2868ffb01fa171247abd58731284d30546a14

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。Codex 実行、CLI ライフサイクル、設定、Git、パス、ログ、状態、結果、エラー、INDEX 更新など、複数の CLI サブコマンドで共有する実行時機能を扱う。個別の共通機能や API の実装を確認・変更するときの入口。

## Read this when
- 複数の CLI サブコマンドにまたがる runtime helper の責務や公開 API を確認するとき
- Codex 実行、CLI 共通処理、設定、Git、パス、ログ、状態、結果、エラー、INDEX 更新の実装を調査・変更するとき

## Do not read this when
- 特定サブコマンド固有の業務処理や入出力を確認するとき
- 正本仕様や個別 runtime helper の詳細だけを確認する場合は、対応する oracle 文書または commons 配下の対象モジュールを直接読むとき

## hash
- 6a50ea3b2853d9ab75df44105a1d5ac9576d7e36625374cc0b2c82fb4a4b1fea

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
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの各サブコマンド入口と、review・apply の実装配置先を提供する。

## Read this when
- CLI サブコマンドの実装構成や、対象サブコマンドの実行入口を確認するとき。
- oracle review、realization workload、run lifecycle、session 操作、TUI 起動などのサブコマンド実装へ進む先を特定するとき。

## Do not read this when
- 特定サブコマンドの詳細処理、共通 runtime、共通 indexing、Git 操作、state schema、prompt editor、TUI builder などを直接調査するとき。対応する下位実装または共通実装を直接読む。
- apply や review の実装本文を調べるとき。現在は実装がなく、追加後に対象ファイルを読む。

## hash
- 9f1d4ac471518c5a7ebbf23c261a5cb18dcf854d18d3c9a3a3d7c0156142c115
