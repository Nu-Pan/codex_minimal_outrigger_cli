# `acp`

## Summary
- `acp` 互換公開層の入口。公開名の存廃や `oracle` 側の正本実装への移行を判断する際に、配下の互換入口と builder adapter 群への導線を確認する。

## Read this when
- `acp` 公開名を維持・削除できるか判断するとき
- 既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する経路を調査するとき
- 互換 builder adapter を通じた feedback、indexing、quota probe、session join、TUI、oracle command、realization workload の接続構成を確認するとき

## Do not read this when
- `oracle` 側の正本実装の仕様、入出力、処理ロジックを確認・変更するとき
- 互換入口の具体的な利用箇所や、個別実体モジュールの内部挙動だけを調査するとき
- `acp` や builder adapter と無関係な CLI 処理、workload 本体、正本仕様、テストを調査するとき

## hash
- ee386a90d331d71cd78aba32d2f9329e1394f7d5dddc317ec50ada7eae6cf3b8

# `basic`

## Summary
- `basic.*` の互換 import を維持するための realization 側公開入口。ACP 型、path model、構造化文書 API を正本実装から再公開し、個別実装や正本仕様は保持しない。各モジュールの公開経路・互換参照を確認するための下位入口である。

## Read this when
- `basic.*` の互換 import を維持・削除する判断をするとき。
- realization 側から ACP 型、path model、構造化文書 API がどの経路で公開されるかを確認するとき。
- 個別モジュールの再公開関係を調査するとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各再公開元の oracle 側を直接読む。
- 個別 API の詳細や参照削除の影響だけを調べるときは、対象モジュールまたは参照箇所へ直接進む。
- `basic.*` と無関係な処理を調査・変更するとき。

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
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 共通ライフサイクル、Codex 実行、設定・状態、Git・パス・ログ・feedback・run lifecycle、INDEX 更新など、複数の runtime 機能から再利用される実装への入口となる。
- 個別の共通 helper の責務と実装を確認する場合は、commons 配下の対応する runtime モジュールへ進む。パッケージ公開 API の構成を確認する場合は初期化・再公開モジュールを入口とする。

## Read this when
- cmoc の複数の runtime 機能にまたがる共通 helper の配置や責務分担を調査するとき
- CLI、Codex 実行、設定、状態、Git、ログ、feedback、run lifecycle、INDEX 更新の実装入口を探すとき
- commons 配下の個別 runtime モジュールを読む前に、共通パッケージ全体の構成を把握するとき

## Do not read this when
- 特定の runtime helper のアルゴリズムや入出力契約だけを確認したいときは、commons 配下の対応する個別モジュールを直接読む
- 利用者向け CLI の個別サブコマンド仕様や正本仕様だけを確認したいときは、該当する CLI 実装または oracle 文書を直接読む
- INDEX.md の文章規則や Structured Output schema だけを確認したいときは、indexing 用の prompt・schema 定義を直接読む

## hash
- 020dabc1869dc82d602e8b54246cc8b1e9e86632efce056d6e62a52c44588bdf

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
- Typer と Click を用いた cmoc CLI の最上位入口。共通の CLI アプリケーション、サブコマンド階層、コマンド引数、補完処理、引数解析エラー変換を定義し、各サブコマンド実装へ処理を委譲する。

## Read this when
- cmoc の CLI 全体のコマンド構成やトップレベル入口を確認・変更するとき
- Typer/Click の引数解析、補完、CLI 例外の cmoc 形式への変換、または互換処理を確認・変更するとき
- doctor、tui、indexing、session、oracle、realization、run、feedback の CLI コマンド登録を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や業務ロジックを確認したいときは、対応する sub_commands 配下の実装を直接読む
- oracle やエラーハンドリングの仕様を確認したいときは、対応する正本仕様を直接読む

## hash
- 266ba84d0a7501d380ff52d891fbb81985a6e3e0817f8677aabe88142f8dbef1

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
- 各 CLI サブコマンドの実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの個別サブコマンド実装へ進むための入口で、サブコマンドの実行フローや責務分担を横断して確認するときに読む。apply と review は現在具体的な実装本文がなく、実装追加後の入口となる。

## Read this when
- CLI サブコマンドの実装構成や、特定サブコマンドの実行入口を調査・変更するとき。
- 複数サブコマンドにまたがる実行フローや、配下の実装へ進む入口を確認するとき。

## Do not read this when
- サブコマンド共通ランタイムや正本仕様だけを確認したいときは、対応する共通実装または仕様書を直接読む。
- 特定サブコマンドの詳細処理だけを確認したいときは、このディレクトリ全体ではなく該当する下位実装を直接読む。
- サブコマンド実装を扱わない作業のとき。

## hash
- 2dfe630006368a2bdf487fad120bffacdee7697ec0f349d2c30965ef858faa22
