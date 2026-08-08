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
- `basic.*` の互換 import を提供する realization 側の公開入口。ACP 型、path model、構造化文書 API を再公開し、既存利用者向けの参照経路を維持する。個別モジュールの実装や正本仕様へ進むためのルーティング対象。

## Read this when
- `basic.*` の互換 import を維持・廃止する条件を判断するとき。
- ACP 型、path model、構造化文書 API の realization 側公開面や参照経路を確認するとき。
- 文字列 child を含む構造化文書の Markdown 描画補正を調査するとき。

## Do not read this when
- 個別モジュールの詳細実装や再公開内容だけを確認したいときは、該当モジュールを直接読む。
- ACP 型、path model、構造化文書 API の正本仕様・定義を確認したいときは、oracle 側の正本を直接読む。
- 互換 import や `basic` の公開面に関係しない CLI、プロンプト、別機能を調査するとき。

## hash
- e143d1e333f9149e479c07ad78ab62cc47a489a1c38b3a192eba4e554842873f

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行 lifecycle、Codex 実行、設定・状態管理、Git・パス・ログ・エラー・feedback、INDEX 更新など、複数機能から再利用される runtime 実装への入口。
- 個別 helper の実装だけでなく、共通公開 API、Codex 実行制御、feedback 永続化、editing run lifecycle など、commons 配下の責務別モジュールへ進むためのルーティング単位。

## Read this when
- cmoc の共通 runtime 機能を横断して調査・変更するとき
- CLI、Codex、設定、状態、Git、ログ、feedback、パス、INDEX 更新などの共通実装の入口を選ぶとき
- 特定の runtime helper の責務に対応する下位モジュールを特定するとき

## Do not read this when
- 単一の runtime helper の具体的なアルゴリズムや挙動だけを調査・変更するとき
- 個別 CLI サブコマンドの業務ロジックや引数定義だけを確認するとき
- 正本仕様や、commons が再公開・委譲する機能の詳細仕様を確認するとき

## hash
- 68786a4685f6e7bd04c07ae954131b6129793461669d0e42c4f8e75a822ca6e7

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
- Typer で構成された cmoc の CLI ルートエントリ。トップレベル command と session/oracle/realization/run/feedback のサブコマンドを登録し、引数解析エラーを cmoc 形式へ変換して各実装へ委譲する。CLI の公開入口とサブコマンド構成を確認するための起点。

## Read this when
- トップレベル command、サブコマンドの登録、CLI option、終了コード、引数解析エラー、補完処理を変更または調査するとき。
- cmoc の console script 起動経路や CLI 全体の command tree を確認するとき。

## Do not read this when
- 特定サブコマンドの業務ロジックや実行処理を調査するときは、各サブコマンド実装を直接読む。
- oracle の仕様、テスト内容、エラー描画の詳細だけを確認する場合。

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
- CLI サブコマンドの realization 実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui など各サブコマンドの実行入口とオーケストレーションを扱い、個別サブコマンド実装へ進むための起点となる。apply と review には現在実装がない。

## Read this when
- CLI サブコマンドの構成や、目的のサブコマンド実装への入口を確認・変更するとき。
- 複数サブコマンドにまたがる実行フローや、サブコマンド固有ディレクトリへの進み先を判断するとき。

## Do not read this when
- 特定サブコマンドの内部処理、共通 runtime、パラメータ構築、正本仕様を直接確認したいときは、該当する下位実装または oracle 文書を直接読む。
- このディレクトリに実装がない apply や review の具体的処理を調べるとき。

## hash
- fcb35dd401f5cc9d3d60eb767d600f493e5b708a8734cd3dcac2c0c426391fb5
