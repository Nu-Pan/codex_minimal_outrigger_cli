# `acp`

## Summary
- `acp` 互換 import 入口と、canonical な `oracle.acp_builder` へ接続する builder adapter 群を扱う。index、session、TUI、quota probe、oracle command、realization workload の parameter builder と、動的 Markdown code fence 補正を下位要素から確認できる。

## Read this when
- `acp.*` または `acp.builder.*` の互換 import 経路を調査・変更するとき。
- canonical builder の parameter を再公開する adapter、prompt 補正、TUI・session・oracle・realization builder の接続を確認するとき。

## Do not read this when
- canonical な `oracle.acp_builder` の仕様や実装そのものを確認したいとき。
- 個別 builder の利用箇所や、TUI・workload の処理本体だけを調査したいとき。

## hash
- 4b33cdb4725ec1c3fd9d1e24a4c9bf5766a4a857c351e9f67947774cc9f8b757

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
- cmoc の共通 runtime 機能をまとめる commons パッケージ。設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果、INDEX 更新など、CLI 実装が横断利用する処理への入口。
- 各 runtime モジュールは責務ごとの実装を持ち、再エクスポート用モジュール、Codex 実行系、設定・Git・状態管理、ログ・パス・エラー処理などに分かれる。

## Read this when
- 複数の CLI サブコマンドで利用される runtime 共通機能の実装箇所を探すとき
- Codex exec/TUI の起動、ログ、retry、preflight、結果処理を調査するとき
- 設定、Git、worktree、path、session state、run lifecycle、INDEX 更新などの共通処理を変更・検証するとき
- 特定機能の担当 runtime モジュールを特定し、その実装へ進む必要があるとき

## Do not read this when
- 特定の runtime 機能の詳細だけを調査する場合は、commons 配下の担当モジュールへ直接進む
- CLI コマンド固有の処理や引数定義だけを確認する場合は、該当するコマンド実装を直接読む
- 利用者向けの正本仕様や出力契約そのものを確認する場合は、対応する oracle 文書を先に読む

## hash
- 3f90ce8b91c6bc1ff4fb352f08fbd1d65f842e56bfe3262e79ba16894657b960

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
- CLI の各サブコマンド実装をまとめるディレクトリ。apply、doctor、indexing、oracle、realization、review、run、session、tui の実装入口を提供し、個別サブコマンドや関連パッケージの詳細確認へルーティングする。

## Read this when
- CLI サブコマンドの実装構成や、対象サブコマンドの実行入口を確認するとき。
- 特定のサブコマンドの動作を調査・変更する際に、配下の実装ファイルまたはパッケージを読むべきか判断するとき。

## Do not read this when
- サブコマンドに共通する runtime、state、report、git、process などの実装詳細だけを調査するとき。
- 個別サブコマンドの詳細な処理、仕様、prompt 構築、Structured Output 生成を確認するときは、配下または対応する専用実装を直接読む。

## hash
- 396ed619782e7a3769668d4f1d4046a5c4061849f331120649b3d54e65cf4101
