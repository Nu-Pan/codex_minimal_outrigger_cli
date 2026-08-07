# `acp`

## Summary
- ACP 互換の realization package。`acp.*` の公開 import 経路を維持しつつ、下位の builder adapter などを通じて canonical な oracle 側実装へ接続する。
- `acp` 公開入口の存廃判断と、builder 用途別の下位要素へ進むための起点となる。

## Read this when
- `acp.*` の互換 import 経路や公開入口全体を確認したいとき。
- ACP builder の用途別 adapter へ進む入口を選びたいとき。

## Do not read this when
- `acp` 公開入口の存廃だけを判断したいなら、入口モジュールを直接読む。
- 特定の builder の実装・canonical 仕様・利用箇所を調べたいなら、該当する下位要素または参照元を直接読む。

## hash
- 19748d31bd6289625fef47d1a672db39bd72ee4039df05de799d7d7caeb3ec5a

# `basic`

## Summary
- `basic` 配下の互換 import 入口をまとめるディレクトリ。ACP 型、path model、構造化文書 API などを正本や oracle 側から再公開し、既存の `basic.*` 公開面を維持する。個別実装や正本定義を確認する場合は各再公開元へ進む。

## Read this when
- `basic.*` の互換 import を維持・廃止する判断をするとき。
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の公開経路や再公開元を確認するとき。
- 利用者向け公開面の移行先や互換層の維持条件を調べるとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各 oracle 側の定義を直接読む。
- 個別モジュールと無関係な処理を調査・変更するとき。

## hash
- 292bc262556c427d8a4a7636a2c7e14127adfdea1c7d57f167e9bfa04d4ce5ea

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行、Codex 呼び出し、設定・状態・パス、Git、ログ、feedback、エラー、INDEX 更新など、複数の上位機能から利用される横断的な実行時基盤を扱う。
- 共通 runtime API の入口と、各領域に分かれた個別 helper の実装を含むため、commons 配下の runtime 機能を横断して確認する際の起点になる。

## Read this when
- 複数の cmoc 機能にまたがる runtime helper の責務や公開 API を調査するとき
- Codex 実行、CLI lifecycle、設定・状態・Git・パス・ログ・feedback・エラー・INDEX 更新の共通処理を変更または調査するとき
- commons 配下で対象となる個別 runtime helper を特定し、適切な実装へ進む必要があるとき

## Do not read this when
- 特定の runtime 領域の実装詳細だけを調査する場合は、その領域の個別実装へ直接進むとき
- CLI サブコマンド固有の業務処理や利用者向け仕様だけを確認する場合
- 正本仕様や Structured Output の要件だけを確認する場合は、対応する oracle 文書を直接読むとき

## hash
- 10339517f4414c4e4753f7d65fec6bd4e005726fd829cdf90908f8c4e7d8c6c8

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
- cmoc の Typer/Click CLI のルートエントリーポイント。補完 probe、引数解析エラーの cmoc 形式への変換、session・oracle・realization・run・feedback のサブコマンド登録、doctor・tui・indexing・console script 起動を扱う。各サブコマンドの具体的な処理は import 先の実装への入口として委譲する。

## Read this when
- CLI のトップレベルコマンド、サブコマンド階層、option、補完処理、引数解析エラー処理、または console script の起動方法を変更・確認するとき。

## Do not read this when
- 特定サブコマンドの業務処理や run/session/oracle/realization の内部実装を変更するときは、対応する import 先の実装を直接読む。CLI のテストのみを調べるときは、対応する realization test を読む。

## hash
- 7726923dd657d38c034f473eb30b402793bb9849767e56eb218d4d4ddedaa8fa

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
- CLI サブコマンドの realization 実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui など各サブコマンドの実行入口と、関連する処理構成への入口を提供する。apply と review は現在実装がない。

## Read this when
- CLI サブコマンドの実装構成や、特定サブコマンドの実行入口を確認・変更するとき。
- サブコマンドの処理範囲を把握し、配下の個別実装へ進む入口を選ぶとき。

## Do not read this when
- 特定サブコマンドの詳細な処理を確認する場合は、配下の該当実装を直接読むとき。
- 共通 CLI runtime、git 操作、report、oracle 仕様など、サブコマンド固有でない処理を確認するとき。
- 未実装の apply または review の具体的な挙動を調べるとき。

## hash
- 60376c23e6704a0172a2a0c11970a86915a4a31567036525a1ecac84a85e2ed7
