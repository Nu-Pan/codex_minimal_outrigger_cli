# `acp`

## Summary
- `acp` 互換の公開入口を扱い、既存の `acp.*` 参照を正本の `oracle.*` または実体モジュールへ移行するまでの導線を提供する。
- 配下には、`acp.builder.*` として正本 builder を再公開する互換入口、動的 prompt の code fence 保護、feedback・indexing・session・TUI・oracle・realization 関連の builder adapter がある。個別処理の実装へ進む際の起点となる。

## Read this when
- `acp.*` または `acp.builder.*` の互換 import を維持・削除する条件を確認したいとき。
- 正本 builder の再公開、動的 prompt の code fence 保護、または処理別 builder adapter の配置を調査・変更するとき。
- feedback・indexing・session・TUI・oracle・realization の builder adapter へ進む入口を判断するとき.

## Do not read this when
- `oracle.acp_builder` の正本仕様や本体ロジックを確認・変更したいときは、正本側の対象を直接読む。
- 個別 builder の prompt 内容や処理詳細を確認したいときは、対応する下位ファイルを直接読む。
- `acp.*` の利用箇所や利用者向け公開面を調査したいときは、各参照元を直接読む。

## hash
- 29138d8819fb8a5f9c16a4f53d866874979e48b0ecc2d5f957e6269aeb4254b4

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
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 共通 lifecycle、Codex exec/TUI、設定・状態・Git・パス・ログ・エラー、feedback、editing run、INDEX 更新など、複数機能から再利用される実装と公開 API を扱う。各個別 runtime 機能を調査・変更する際の入口となる。

## Read this when
- cmoc の共通 runtime API や、複数の runtime 機能にまたがる実行境界・状態管理・公開シンボルを確認するとき
- CLI lifecycle、Codex 実行、設定、Git、feedback、editing run、INDEX 更新などの共通実装の担当箇所を特定するとき
- 対象機能の個別実装へ進む前に、commons 内の公開入口や関連する共通 helper を確認するとき

## Do not read this when
- 特定の runtime 機能の具体的なアルゴリズムや正本仕様だけを確認したい場合は、対応する個別 runtime モジュールまたは oracle 文書へ直接進むとき
- 個別 CLI サブコマンドの業務ロジックや、feedback の保存形式など単一機能の詳細だけを調査するとき
- commons と無関係な realization 実装やアプリケーション固有の挙動を確認するとき

## hash
- 5a6f6847245829711e0f955e6dca26fc8cf8e824ce521d6f88b9b111213a4d73

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの各コマンド入口と実行ライフサイクルへ進むための起点となる。
- apply は現時点で実装がなく、実装追加後に確認する対象として扱う。oracle と realization は配下の個別実装へ、run は編集 run の共通 lifecycle や互換 shim へ進む入口である。

## Read this when
- CLI サブコマンドの構成や、対象コマンドの実装入口を確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui の実行フローやライフサイクル実装を調査・変更するとき。
- apply サブコマンドの実装が追加され、その内容を確認するとき。

## Do not read this when
- サブコマンド以外の共通実装や正本仕様だけを確認したいときは、対応する commons、builder、schema、oracle file を直接読む。
- 特定サブコマンド配下の個別処理だけを調査するときは、このディレクトリではなく該当する下位実装へ直接進む。
- apply 以外のサブコマンドを扱う際に、未実装の apply 入口を読む必要はない。

## hash
- 9a835cc0fa328c399ff20d8c6628f5d5b0674548de1e8479c7c1234db11ef49f
