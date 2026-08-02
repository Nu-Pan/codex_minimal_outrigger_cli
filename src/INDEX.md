# `acp`

## Summary
- `src/acp` は ACP 互換層の realization 実装をまとめる領域で、公開入口と builder 系の互換経路を扱う。下位項目では、利用者向け入口の互換処理や builder の adapter・prompt 生成処理など、責務ごとの具体的な実装へ進める。

## Read this when
- ACP 互換層全体の責務や、`src/acp` 配下で調査すべき実装領域を選びたいとき。
- `acp` 公開入口から canonical な `oracle` 実体や各 builder adapter へつながる realization 側の経路を確認したいとき。

## Do not read this when
- canonical な仕様・実装そのものを確認または変更したいときは、対応する `oracle` 側を直接読む。
- `acp` 配下の特定モジュールの内部挙動だけを調べたいときは、この階層ではなく該当する下位項目を直接読む。

## hash
- 913909fbc65b15ee293901dfef8b670588f2300173ed68f7dcb47173a87b3ad0

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
- cmoc 共通 runtime helper を集約する commons パッケージ。CLI 実行、Codex 呼び出し、設定・状態・パス管理、Git 操作、ログ、エラー処理、INDEX 更新など、複数の上位機能から利用される共通実装への入口。

## Read this when
- cmoc の共通 runtime 機能を調査・変更するとき
- CLI、Codex、設定、状態、Git、ログ、INDEX 更新などの横断的な基盤処理の入口を確認するとき
- 対象となる個別 runtime helper や公開 API の配置を特定するとき

## Do not read this when
- 特定の runtime helper の実装詳細だけを確認したいとき
- 特定の CLI サブコマンドや利用者向け仕様だけを調査するときは、対応する個別実装または oracle 文書を直接読む

## hash
- 1c42a6851f8e63adadadf350a3bd99ae7bcfd9b8624f8c8e1b998c1594a7fceb

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
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、indexing、tui、session、run、oracle、realization などの実行入口・パッケージへ進むための上位ルーティングで、apply と review は現時点で実装本文がない。

## Read this when
- CLI サブコマンドの実装構成や、特定サブコマンドの実行入口を確認・変更するとき。
- doctor、indexing、tui、session、run、oracle、realization の実行フローや下位実装への入口を探すとき。

## Do not read this when
- サブコマンド共通の CLI ランタイムや設定の詳細だけを調査するとき。
- 特定サブコマンドの処理詳細を確認する場合は、このディレクトリ全体ではなく該当する下位実装を直接読むとき。
- oracle や realization の正本仕様、共通実装、個別処理の詳細だけを確認するとき。

## hash
- 69fac896d4ee6e6a00a3883a4b2c015247b52df888abe2c06b2dedfba7446b54
