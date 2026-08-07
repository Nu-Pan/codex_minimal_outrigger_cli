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
- cmoc の共通 runtime helper を提供する commons パッケージ。CLI 実行 lifecycle、Codex exec/TUI、設定・状態・パス、Git、ログ、feedback、エラー、INDEX 更新など、複数の上位機能から利用される横断的な実行時処理を扱う。
- パッケージ初期化と共通 API の集約を入口に、個別の runtime_* モジュールへ進んで各領域の実装詳細を確認するためのディレクトリ。

## Read this when
- 複数の cmoc 機能にまたがる runtime helper の構成や、共通 API の入口を確認するとき
- CLI、Codex、設定、状態、Git、ログ、feedback、INDEX 更新などの共通実行時処理の担当モジュールを選ぶとき

## Do not read this when
- 特定の runtime 機能の実装詳細だけを確認したいときは、対応する runtime_* モジュールを直接読む
- 利用者向けの正本仕様や個別サブコマンドの業務処理だけを確認したいときは、対応する oracle 文書または呼び出し元の実装を直接読む

## hash
- fdd8ad10929086e04c6c1e1f81945bd6728f6b4838824039b21f994ac126b446

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
- CLI サブコマンドの実装をまとめる領域。doctor、feedback、indexing、oracle、realization、run、session、tui の各実行入口と、サブコマンド固有の下位処理への入口を提供する。
- サブコマンド全体の構成や、目的の CLI 実装へ進む先を選ぶための起点として扱う。

## Read this when
- CLI サブコマンドの一覧、実装配置、実行入口を確認するとき。
- 特定サブコマンドの実装を調査・変更する前に、対応する下位パッケージまたは実装ファイルを特定するとき。
- oracle、realization、run、session のサブコマンド群に含まれる下位処理への入口を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細な挙動、状態遷移、処理内容を確認したいときは、対応する下位パッケージまたは実装ファイルを直接読む。
- CLI サブコマンドで共有されるランタイム、Git 操作、report 処理などの共通実装だけを確認したいとき。
- oracle や realization の正本仕様を確認したいときは、対応する oracle 文書を直接読む。

## hash
- d70c36bf435e0ea688e8de9265bb5303602a273ccce3db1ec9d4118e74ac1718
