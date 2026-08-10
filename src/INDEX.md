# `acp`

## Summary
- `acp` 互換の公開入口を扱い、既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する際の判断材料を提供する。互換入口の存廃や移行導線を確認するための入口であり、具体的な内部実装は扱わない。
- ACP builder の互換・委譲 adapter 群をまとめるパッケージ。basic、common、feedback、indexing、oracle、quota_probe、realization、session、tui などの下位要素へ進む入口で、正本実装への接続、既存 import 経路の維持、prompt の code fence 保護を扱う。

## Read this when
- `acp` という公開名を維持または削除できるか判断したいとき。
- 既存利用者向けの `acp.*` 参照を壊さず、`oracle` 側の実体へ切り替える導線を確認したいとき。
- ACP builder の構成、正本 builder への委譲経路、既存 import 互換性を調査したいとき。
- 特定の command、session、index、feedback、quota probe、TUI、realization builder の下位実装へ進む入口を選びたいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細だけを知りたいときは、該当する実体モジュールを直接読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変更したいとき。
- canonical な oracle 実装や正本仕様そのものを確認・変更したいとき。
- ACP builder の特定機能の具体的な生成ロジックを調査したいとき。
- builder 以外の CLI 実行処理や利用箇所の公開面を調査したいとき。

## hash
- cbf719e2bc11d45ae4f862c9244d6d8d978a2996a9aa3b3530d5383f42a040dd

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行、Codex、設定・状態、Git、ログ、パス、feedback、INDEX 更新など、複数の runtime 機能から再利用される公開 API と個別実装を扱う。各共通機能の実装や公開入口へ進むためのディレクトリ。

## Read this when
- cmoc の共通 runtime 機能の構成や、対象となる helper の所在を確認するとき
- 複数の runtime 機能にまたがる共通 API・状態・実行制御・永続化処理を調査または変更するとき
- INDEX 更新、Codex 実行、feedback、設定、Git、ログ、パスなどの個別実装へ進む入口を探すとき

## Do not read this when
- 特定の helper や runtime 機能の具体的な挙動だけを調査する場合は、commons 配下の対応する個別実装を直接読む
- 利用者向けの正本仕様や CLI サブコマンド固有の業務ロジックだけを確認する場合は、対応する仕様またはサブコマンド実装へ直接進む

## hash
- 0d38d343cf80d4bafded8d8c0695cc1e9e804d996b49983f3a4e24b90c0ebe93

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
- CLI サブコマンドの実装を集約するディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの実行入口と、各処理領域の下位パッケージへの入口を提供する。apply と review は現在実装ファイルがなく、将来の配置先として扱われる。

## Read this when
- CLI サブコマンドの実装構成や、目的のサブコマンドの実行入口を確認するとき。
- 複数サブコマンドにまたがる実装配置や責務分担の入口を判断するとき。

## Do not read this when
- 特定サブコマンドの詳細な処理、共通ランタイム、正本仕様、または下位パッケージの具体的実装だけを確認したいとき。
- 対象が apply または review で、実装が追加されていない状態の具体的挙動を調査するとき。

## hash
- 3b4fff7acf004cb3e045767141ec3da9be3e848b57cb3d760a9b99d3f716e70c
