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
- cmoc の共通 runtime パッケージ。CLI 実行、Codex 呼び出し、設定・状態・パス管理、Git 操作、ログ、エラー、INDEX 更新、run lifecycle など、複数の上位機能から利用される横断的な実行時補助機能をまとめる。
- パッケージ初期化では、各 runtime モジュールの主要 API を共通入口として再公開している。個別機能の実装や挙動を調査する場合は、対応する下位モジュールへ進む。

## Read this when
- cmoc の共通 runtime API の構成や、複数領域にまたがる実行時依存を把握するとき
- CLI、Codex、設定、Git、状態、INDEX 更新、run lifecycle などの共通実装の入口を選ぶとき
- 個別 runtime モジュール間の責務分担や公開 API の再エクスポートを確認するとき

## Do not read this when
- 単一の runtime 機能の具体的な挙動だけを調査・変更するときは、対応する個別実装を直接読む
- 利用者向け仕様や正本仕様を確認するときは、対応する oracle 文書を直接読む
- 特定の CLI サブコマンド固有の処理を調査するときは、そのサブコマンド実装へ直接進む

## hash
- c3a278cd8619ddb60cb032b8c91312c0567e76a14145637f960e0eca059dd43c

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor、indexing、oracle、realization、review、run、session、tui の各実行入口を下位要素として案内する。
- 特定のサブコマンドの実行フローや lifecycle、状態遷移、差分・commit・report 処理を調査・変更する際の入口となる。

## Read this when
- CLI サブコマンドの実装構成や、対象サブコマンドの実行入口を確認するとき。
- doctor、indexing、oracle、realization、review、run、session、tui のいずれかの実装を調査・変更するとき。

## Do not read this when
- サブコマンドに依存する共通処理の詳細を確認するときは、対応する commons 側の実装を直接読む。
- 特定サブコマンドの詳細仕様や下位処理を確認するときは、このディレクトリの入口ではなく該当する実装ファイルまたは oracle 文書を直接読む。
- apply サブコマンドの実装を確認するときは、実装ファイルが追加されるまで読むべき下位要素はない。

## hash
- ef0520b7f48b4da77a5f53e7442d61beae611e4766c3edb92e5d5d5f3096258c
