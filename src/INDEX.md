# `acp`

## Summary
- ACP互換の公開入口と、ACP builder群の互換・realization adapterを扱う領域。oracle側のcanonical実装を既存のacp参照経路から利用するための入口であり、builder配下にはfeedback、indexing、oracle command、realization、session、TUI、quota probe、共通builder関連の導線が集約されている。

## Read this when
- acp互換公開名の存廃や、既存参照をoracle側の実体へ移行する導線を判断するとき。
- ACP builder全体のadapter構成や、canonical oracle実装への委譲関係を確認するとき。
- feedback issue、index entry、quota probe、session join、TUI起動、oracle command、realization apply/refactorに関するbuilder入口を特定するとき。

## Do not read this when
- 特定builderのprompt、入力検証、出力仕様、処理ロジックを確認したいだけなら、対応するcanonical実装または下位対象を直接読む。
- acp配下の具体的な内部挙動を変更・調査したいだけなら、対象の実体モジュールを直接読む。
- CLI commandの業務ロジックや利用者向け公開面、特定領域の詳細を調べる場合は、この領域を入口に総当たりせず、該当する参照元または下位対象へ進む。

## hash
- eb375d96ed92dd7ecf4cfb6611e7f2b3cf0104bafae1c5736c2d5a7fe4b9c556

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行ライフサイクル、Codex 呼び出し、設定・状態・Git・パス・ログ・エラー、INDEX 更新、feedback など、複数の runtime 機能から再利用される共通 API と実装を扱う。各個別 helper や公開 API の調査へ進むための入口。

## Read this when
- cmoc の runtime 共通機能の構成や、複数の runtime 機能にまたがる依存関係を確認するとき
- CLI、Codex、設定、状態、Git、パス、ログ、feedback、INDEX 更新などの共通実装を変更・調査するとき
- 対象となる個別 runtime helper や公開 API の所在を判断するとき

## Do not read this when
- 特定の runtime helper の内部実装やアルゴリズムだけを確認したいときは、対応する個別ファイルへ直接進む
- 特定の CLI サブコマンド、正本仕様、Structured Output schema の詳細だけを確認したいときは、それぞれの担当対象を直接読む

## hash
- ce5cceaf4db762c7f096a551c19789615a5a92665db8e5c29f35add03afee0a2

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui など、各サブコマンドの実行入口やライフサイクル処理へ進むための上位ルーティングを担う。
- サブコマンド横断の構成や、目的の CLI 操作に対応する実装の所在を確認する際の入口となる。

## Read this when
- CLI サブコマンドの実装構成を確認するとき
- 特定のサブコマンドの実行入口、ライフサイクル、または配下の個別実装へ進む場所を判断するとき
- doctor、feedback、indexing、oracle、realization、run、session、tui のいずれかを調査・変更するとき

## Do not read this when
- CLI 共通ランタイム、Git・パス処理、state 管理など、サブコマンド個別実装ではない共通処理だけを調査するとき
- サブコマンドの正本仕様や oracle 文書の契約だけを確認するときは、対応する仕様文書を直接読む
- 特定サブコマンドの詳細な挙動を確認する場合は、このディレクトリ全体ではなく該当する個別実装へ直接進む

## hash
- 34b787f0298c7bce6da24357662542a9d53412c7e4bf5af7a44cb794380f6525
