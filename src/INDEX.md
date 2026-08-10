# `acp`

## Summary
- `acp` 互換パッケージを提供する realization 領域。canonical な `oracle` 実装への互換 import、prompt 補正、builder・feedback・session・TUI 関連の adapter を扱う。
- 下位要素では、builder の共通処理、個別 adapter、oracle 互換入口、realization 操作用の adapter へ分岐する。

## Read this when
- 既存の `acp.*` または `acp.builder.*` 参照を維持しつつ canonical な `oracle` 実装へ委譲する経路を調査するとき。
- builder の prompt 生成補正、quota probe、indexing、feedback、session join、TUI、realization 操作の adapter の所属領域を判断するとき。
- `acp` 互換パッケージ全体から、該当する下位 adapter や共通処理へ読み進めるとき。

## Do not read this when
- canonical な oracle 実装の仕様や挙動そのものを確認・変更するときは、対応する oracle 側を直接読む。
- CLI の実行処理、利用者向け公開面、`acp` の利用箇所を調査するときは、各参照元や実行処理を直接読む。
- 特定 adapter の内部挙動だけを確認したいときは、このディレクトリ全体ではなく該当する下位要素を直接読む。

## hash
- 6b525d9f04227e7a452c5ac6039b5d6e902f6523be7ad95dfc4efc1bcfcaeee8

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行、Codex、設定、Git、パス、ログ、状態、feedback、エラー処理など、複数の機能から再利用される runtime API と lifecycle 実装を扱う。各個別 helper やサブシステムの実装へ進むための入口。

## Read this when
- commons 配下の共通 runtime API、公開シンボル、パッケージ構成を確認するとき
- CLI、Codex、設定、Git、パス、ログ、状態、feedback など複数の runtime 機能を横断して実装入口を探すとき
- INDEX.md の生成、Codex 実行、editing run、doctor、feedback、設定永続化などの共通 lifecycle を調査するとき

## Do not read this when
- 特定の runtime helper のアルゴリズムや挙動を確認したいとき
- 特定の CLI サブコマンドや個別機能の利用者向け仕様だけを確認したいとき
- commons の個別実装ファイルが対象として明確な場合

## hash
- 43a4f9df32f4bbc0468f13f2774cba88e948c507a0c43656ea07d83b4b3d4b87

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
- CLI 全体の Typer アプリケーションを構成し、各トップレベルおよびサブコマンドを公開する実行入口。引数解析エラーを cmoc 形式へ変換し、処理本体は対応するサブコマンド実装へ委譲する。CLI 構成、引数解析、補完、起動経路を確認するときの入口となる。

## Read this when
- CLI のコマンド登録やサブコマンド階層を確認・変更するとき
- Typer/Click の引数解析エラー、補完、終了処理を確認するとき
- console script から CLI が起動される経路を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容を調査・変更するときは、対応する sub_commands 配下を直接読む
- エラー表現や自動補完の正本仕様を確認するときは、参照されている oracle 文書を読む

## hash
- 9b8448815b84ea98040776fdaccc0058c63c9a1828c6ebbbb2c8a13c61b38d09

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの実行入口と、それぞれの処理フローへの入口を提供する。apply と review は現時点で実装本文がない。

## Read this when
- CLI サブコマンドの構成や、目的のサブコマンド実装への入口を確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui の実行フローや責務分担を調査・変更するとき。

## Do not read this when
- 特定サブコマンドの内部処理、共通実装、正本仕様、プロンプトや起動パラメータの詳細だけを確認したいとき。
- apply または review の具体的な実装を確認したいとき。現時点ではこのディレクトリに実装本文がない。

## hash
- e4b2db3cc5b0965c1474fac01983e3e5d67d57106af9e287ce9be570ca18032a
