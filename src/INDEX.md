# `acp`

## Summary
- ACP互換の公開入口を担い、既存の`acp.*`参照を`oracle.*`または実体モジュールへ移行する際の判断材料を提供する。互換入口の存廃を確認する場合の入口であり、具体的な実装や移行先の詳細は下位の実体モジュールへ進む。
- ACP builderの互換adapterとcanonicalなoracle builderへの接続をまとめる。prompt内のMarkdown code fence保護、feedback・index・session・quota probe、realization apply/refactor、oracle edit/investigation/reviewのbuilder実装を調査するときの入口であり、canonicalなprompt仕様やACP実行処理そのものは対応する実装へ進む。

## Read this when
- ACP互換入口の責務、存廃、既存参照からoracle側実体への移行導線を確認するとき
- ACP builderのadapter配置、canonical oracle builderへの委譲、prompt埋め込み時のcode fence保護、または関連probe・builder接続の下位実装を探すとき

## Do not read this when
- ACP配下の具体的な実装内容や移行先の詳細だけを確認したいとき
- canonical oracle builderのprompt内容・schema・判定基準、ACP builderの利用箇所、ACP実行処理やrealization本体を直接調査するとき

## hash
- 07d4de284eb6fb0b8ea42fd2342f4f1aba511c62d164ee81bc874d33dcbaf3c7

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
- cmoc の commons パッケージとして、CLI・Codex 実行・設定・状態・Git・ログ・パス・feedback・editing run などで共有される runtime helper をまとめる領域。共通 API の公開入口から、各機能の個別実装や結果型、永続化・ライフサイクル管理へ進むための起点となる。

## Read this when
- 複数の cmoc runtime 機能にまたがる共通 API、実行境界、状態管理、Git 操作、ログ、feedback、パス処理を横断して確認するとき
- commons 配下の共通 helper の責務分担や、公開入口から個別 runtime 実装へ進む経路を把握するとき
- Codex exec/TUI、INDEX preflight、editing run、doctor、feedback などの共通 runtime lifecycle を調査するとき

## Do not read this when
- 特定の runtime helper のアルゴリズムや個別機能の挙動だけを確認したいときは、対応する個別実装を直接読む
- CLI サブコマンド固有の業務ロジックや利用者向け仕様だけを確認したいときは、該当する subcommand または正本仕様を直接読む
- 設定型、feedback の schema、INDEX entry の生成規則など、commons の共通入口ではなく専用仕様が責務を持つ内容を確認するとき

## hash
- f4e4864c1ca96f1debb2f962c4571a582ce59ebc8c85bd0aafc4bd06e72d7f97

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
- cmoc の各サブコマンド実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、review、run、session、tui などの CLI 実行入口と、配下の個別 lifecycle・workload 実装へ進むための起点となる。apply は現在未実装。

## Read this when
- cmoc のサブコマンド実装の構成や、対象サブコマンドの CLI 実行入口を確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui など、複数のサブコマンドから読むべき実装を選ぶとき。
- 特定サブコマンドの詳細実装へ進む前に、該当する入口と下位要素を特定するとき。

## Do not read this when
- サブコマンドに共通する runtime、state、Git、lock などの canonical 実装詳細だけを確認するときは、対応する commons 配下の実装を直接読む。
- サブコマンドの利用者向け仕様や oracle の正本仕様を確認するときは、対応する oracle 文書を直接読む。
- 特定サブコマンドの詳細な lifecycle や workload 処理を確認する場合は、このディレクトリ全体ではなく該当する個別実装へ直接進む。

## hash
- 17ac9c652723807cfbdaac2c74c8302381c4500fe3ffc4b8a63ebdcdd4303626
