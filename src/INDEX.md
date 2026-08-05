# `acp`

## Summary
- `acp` 互換の公開入口と ACP builder adapter 群を扱うディレクトリ。公開名の互換維持や oracle 実体への移行を確認する入口であり、builder の command/package 別処理は下位要素へ案内する。

## Read this when
- `acp` という公開参照を維持・削除できるか判断するとき。
- ACP builder 全体の構成や、command 別 adapter・共通処理の調査先を切り分けるとき。

## Do not read this when
- `acp` 配下の具体的な実装や移行先の詳細だけを確認したいときは、該当する実体モジュールを直接読む。
- ACP と無関係な CLI 実装や利用者向け公開面だけを調査するとき。

## hash
- 0b7c56e5a4cbb8b1fd252f7f4742b58265d952a0a784bd780fcb3732be279d80

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行、Codex 実行、設定・状態・パス管理、Git、ログ、エラー、INDEX 更新、editing run など、上位実装が横断的に利用する runtime API と個別実装への入口を提供する。
- パッケージ全体の公開 API や複数 runtime 領域の連携を確認する場合の入口であり、個別機能の詳細調査では配下の担当モジュールへ進む。

## Read this when
- cmoc の共通 runtime API や commons パッケージの責務範囲を確認するとき
- CLI、Codex、設定、状態、Git、ログ、INDEX 更新、editing run など複数の runtime 領域にまたがる依存関係を調査するとき
- commons 配下で対象となる個別実装を選ぶため、各 runtime module の役割を確認するとき

## Do not read this when
- 単一の runtime 機能の実装詳細だけを調査・変更するときは、対応する runtime module を直接読む
- 特定サブコマンドの固有処理や利用者向け仕様だけを確認するときは、その command 実装または oracle 文書を直接読む
- INDEX.md の正本 schema や生成 prompt、個別の session・report・process 仕様を確認するときは、対応する専用実装または oracle file を直接読む

## hash
- b777aed2e1f18f5a8a14517b9dd0a6ee08e756af1e18583b7a623dfc9264e684

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
- Typer を用いた cmoc CLI の主要エントリーポイント。doctor、tui、indexing と、session・oracle・realization・run の各サブコマンドを登録し、対応する実装関数へ委譲する。CLI 引数解析エラーは cmoc 形式のエラーレポートへ変換し、自動補完時は副作用を抑制する。各サブコマンド実装や CLI 全体の構成を確認する際の入口。

## Read this when
- cmoc の CLI コマンド、サブコマンド、option、Typer/Click の引数解析、エラー変換、自動補完の挙動を変更・調査するとき
- 特定のサブコマンド実装へ進む前に、CLI からの登録名と委譲先を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や永続化・worktree 操作の詳細を確認したいとき。対応する sub_commands 配下の実装を直接読む
- CLI とは無関係な runtime、oracle、realization の内部処理を調査するとき

## hash
- 2fc467906ef010b3f9c4d51a1600ba115332880dd4658767606f556b60c8e8d7

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
- CLI サブコマンドの realization 実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの各サブコマンド入口と、関連する実行フロー実装への階層入口を提供する。
- apply と review は現在実装本文がなく、将来の実装配置先として示されている。

## Read this when
- CLI サブコマンドの実装構成や、特定サブコマンドの実行入口を確認・変更するとき。
- doctor、indexing、oracle、realization、run、session、tui のいずれかの実行フローを調査するとき。

## Do not read this when
- 個別サブコマンドの詳細実装、共通処理、正本仕様を直接確認したいときは、該当する下位実装または oracle 文書を読む。
- apply または review の具体的な処理を確認したいときは、実装が追加された後に該当する下位要素を読む。

## hash
- fdd924c80cfde87014738001294eb9358dc73ea3b6262e624e045818e8883fe5
