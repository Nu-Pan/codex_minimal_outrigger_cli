# `acp`

## Summary
- `acp` 互換公開入口と ACP builder の realization package を扱う。既存の `acp.*` 参照を維持・移行する判断や、用途別 builder adapter の調査を始めるための入口。

## Read this when
- `acp` 公開名の存廃や oracle 側実体への移行導線を確認したいとき。
- ACP builder の互換入口、委譲 adapter、用途別 builder の配置を調査したいとき。

## Do not read this when
- 特定用途の builder の生成ロジックや内部挙動を確認・変更したいときは、対応する下位要素を直接読む。
- canonical builder、CLI 実行処理、利用側の参照を調査したいときは、それぞれの直接の対象を読む。

## hash
- 09db759a0970b3bff75e3a86e811ce069889b3cf001bc092feeb6df89c9bca33

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
- 対象ディレクトリは、cmoc の共通 runtime helper をまとめる commons パッケージ。パッケージ初期化と runtime API の集約に加え、INDEX 更新、prompt editor、Codex 実行、設定、Git、ログ、パス、feedback、session・editing run など、複数の上位機能から共有される実行時境界を扱う。
- commons 配下の共通実装を調査・変更する際に、対象となる個別 runtime モジュールへ進むための入口である。

## Read this when
- commons が提供する共通 runtime 機能の責務範囲を把握するとき
- Codex 実行、INDEX 更新、設定、Git、ログ、feedback、session・editing run などの共有実行基盤から、調査対象の下位モジュールを選ぶとき
- commons パッケージの初期化や runtime API の公開入口を確認するとき

## Do not read this when
- 特定の runtime 機能の実装詳細を確認・変更する場合は、対応する commons 配下の個別モジュールへ直接進むとき
- 利用者向け CLI サブコマンド固有の業務処理や正本仕様だけを確認する場合
- commons と無関係な実装領域を調査する場合

## hash
- 02337535b2b08dfa5e628bf56e9d8deaf72eaf6ffa1a0ebf7671e3e6970a6962

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
- cmoc の Typer CLI アプリケーション本体。トップレベルおよび session、oracle、realization、run、feedback の各サブコマンドを登録し、対応する実装へ処理を委譲する。
- CLI 引数解析エラーを cmoc のエラーレポート形式へ変換し、自動補完時の副作用を抑制する共通実行制御も担う。各サブコマンドの詳細な挙動を確認する場合の CLI 実装入口。

## Read this when
- cmoc の CLI コマンド構成、コマンド登録、サブコマンドの入口、Typer/Click の引数解析エラー処理を調査・変更するとき。
- トップレベル CLI から各サブコマンド実装へ処理がどのように委譲されるかを確認するとき。

## Do not read this when
- 特定サブコマンドの業務ロジックや詳細仕様だけを調査するときは、対応する sub_commands 配下の実装または oracle 仕様を直接読む。
- CLI 以外のランタイムエラー描画、ブランチ操作、oracle/realization 処理の内部実装を調査するとき。

## hash
- ab836c831dc3c506349bd82f4dbd6b61ff24527de8e45ffadd819f423bb670d6

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
- CLI サブコマンドの realization 実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの各サブコマンド入口と、apply・review の実装配置先を下位要素へ案内する。

## Read this when
- CLI サブコマンドの実装構成や、特定サブコマンドの実行入口を確認・変更するとき。
- サブコマンドのライフサイクル、worktree、state、commit、cleanup、report などの処理経路を特定するとき。
- 未実装の apply または review サブコマンドの実装配置先を確認するとき。

## Do not read this when
- サブコマンドに関係しない処理を調査するとき。
- 特定サブコマンドの詳細実装を確認する場合は、このディレクトリ全体ではなく対応する下位要素を直接読む。
- 共通 runtime、lifecycle、git 差分操作、report の canonical 実装や、各サブコマンドの正本仕様を確認する場合は、対応する共通実装・仕様文書を直接読む。

## hash
- c081b07ac8fb196c3cdbd045c046dca96e017761f0c482e04341d05ca8c3eadb
