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
- commons パッケージは、cmoc の複数の実行経路で共有される runtime helper を集約する実装層。設定、Git/worktree、パス、ログ、状態、プロセス、Codex 実行、feedback、INDEX 更新、結果・エラー処理などの共通機能を扱い、個別 helper の実装を確認・変更するときの入口になる。

## Read this when
- 複数の CLI や実行経路にまたがる共通 runtime 機能の責務や実装箇所を確認するとき
- commons 配下の個別 helper に進む前に、共有 runtime API と関連モジュールの構成を把握するとき

## Do not read this when
- 特定の runtime helper の内部挙動だけを確認したいときは、該当する個別実装を直接読む
- 個別 CLI の業務ロジックや正本仕様だけを調査し、共通 runtime 実装に触れないとき

## hash
- 50d4438c156b76c67b22d7cd2c49642e302ecbf446a066c01af79707310352f7

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
- Typer を使った cmoc CLI のルート入口。トップレベルおよび session、oracle、realization、run、feedback 配下のサブコマンドを登録し、それぞれの実装関数へ処理を委譲する。
- Click/Typer の互換処理と CLI 引数解析エラーの cmoc 形式への変換を担い、通常実行と `_CMOC_COMPLETE` による自動補完 probe を分離する。
- CLI のコマンド構成、引数解析エラーの扱い、または console script からの起動経路を確認する際の入口であり、個別コマンドの挙動は各 `sub_commands` 実装を直接読む。

## Read this when
- cmoc の利用可能なトップレベル・サブコマンド構成を確認するとき
- Typer と Click の互換処理、CLI 引数解析エラーの表示・終了コード、または自動補完の起動経路を調査するとき
- console script が cmoc CLI をどのように起動するかを確認するとき

## Do not read this when
- 特定サブコマンドの業務処理や worktree 操作の詳細を調査するときは、対応する `sub_commands` の実装を直接読む
- oracle、realization、session などの仕様や外部挙動の正本を確認するときは、対応する oracle/specification を直接読む
- CLI とは無関係な共通ランタイムや個別機能の実装を調査するとき

## hash
- 8a443d75371da9adebc4b8b7dc79b17f5f85b50af38d34a7405727edb10de6e0

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
- CLI サブコマンドの実装をまとめる上位ディレクトリです。doctor、indexing、tui の実装と、feedback・oracle・realization・run・session の各サブコマンドパッケージへの入口を提供します。
- 特定のサブコマンドの処理を調査するときは、まずこのディレクトリで該当する実装またはパッケージを特定し、その下位対象へ進みます。

## Read this when
- CLI サブコマンドの実装構成や、目的のサブコマンドの入口を特定するとき。
- doctor、indexing、tui、feedback、oracle、realization、run、session のいずれかを扱うが、担当する下位実装がまだ特定されていないとき。

## Do not read this when
- 特定のサブコマンドの処理フローや仕様を確認する場合は、該当する下位実装または正本仕様を直接読むとき。
- CLI ランタイム、共通 indexing、prompt editor など、サブコマンドから呼び出される共通実装だけを確認するとき。

## hash
- 482328901cffe9279c0e26b01db2240b2b26b101f5182e96441605cb78d4523a
