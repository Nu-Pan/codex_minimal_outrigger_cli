# `acp`

## Summary
- `acp` 互換の公開入口を扱い、既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する際の判断材料を提供する。
- ACP builder の互換入口と共通処理、oracle command builder、realization workload builder adapter、TUI/session 関連 adapter をまとめる。各機能の詳細は対応する下位実装または canonical 実装への入口として利用する。

## Read this when
- `acp` という公開名を維持または削除できるか判断するとき。
- 既存利用者向け参照を壊さず oracle 側の実体へ切り替える導線を確認するとき。
- `acp.builder` 配下の互換公開経路、builder adapter の構成、共通 prompt 処理の入口を確認するとき。
- oracle command、realization workload、TUI、session、indexing などの builder adapter の下位実装へ進む対象を判断するとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細だけを確認したいとき。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変更したいとき。
- canonical な oracle builder の具体的な prompt 生成仕様や実装挙動を確認したいとき。
- TUI、session、realization apply/refactor、indexing など特定機能の詳細だけを調査・変更するとき。
- `acp.builder` と無関係な CLI、TUI 本体、一般的な ACP parameter 処理を調査するとき。

## hash
- e276fc7c7e66fe5bdf0ce35c75500610890136639963a98a4c10ac3af077c27a

# `basic`

## Summary
- `basic.*` の互換 import を維持する公開入口群。ACP 型、path model、構造化文書 API を実体定義から再公開し、`basic` 側に実装や正本仕様を複製しない。

## Read this when
- `basic.*` 経由の公開名や互換 import の維持・廃止を判断するとき。
- ACP 型、path model、構造化文書 API の realization 側での再公開関係を確認するとき。

## Do not read this when
- 各 API の正本仕様や実装本体を確認したいときは、対応する oracle 側を直接読む。
- `basic.*` の公開面や互換 import に関係しない処理を調査・変更するとき。

## hash
- 6427f271674f13de9f39976c4fe0d10226ad4c7573c6fa05a58ee5db32f274b7

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
- cmoc の共通 runtime helper を集約する commons パッケージ。Codex 実行、CLI ライフサイクル、設定、Git、パス、状態、ログ、結果、エラー、INDEX 更新など、複数機能で共有される実装への入口。
- パッケージ初期化と共有 API の再公開に加え、各 runtime_* モジュールで責務ごとの具体的な処理を提供する。

## Read this when
- 複数の CLI サブコマンドや runtime 機能にまたがる共通処理を変更・調査するとき
- Codex 実行、設定、Git、path、state、logging、report、INDEX 更新の担当モジュールを特定するとき
- commons パッケージの公開入口や runtime API の構成を確認するとき

## Do not read this when
- 特定サブコマンド固有の業務処理や入出力だけを調査するとき
- 正本仕様や個別 runtime helper の詳細が目的で、対象モジュールまたは oracle 文書が直接特定できるとき

## hash
- c3a6b20a0baed046fe06f98ed327a4cc3d18659967c358c3e5a7da4827830e8c

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
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの個別入口と、apply・review の実装配置先を提供する。各サブコマンドの構成や実行フローを調査・変更する際のルーティング起点となる。

## Read this when
- CLI サブコマンドの実装構成を確認・変更するとき。
- 特定のサブコマンドの実装入口や、配下の詳細実装を探すとき。

## Do not read this when
- サブコマンドに属さない共通 runtime、共通 lifecycle、INDEX 更新、Git 操作、状態 schema などの詳細だけを調査するとき。
- 特定の処理の詳細を直接確認したい場合は、このディレクトリの概観ではなく該当する下位実装を読むとき。

## hash
- 9a84e87fb14333de650f544252d2652bf2519765008a4367f62108f802174822
