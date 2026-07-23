# `acp`

## Summary
- `acp` 互換公開入口と、旧 `acp.builder.*` import 経路を canonical 実装へ委譲する builder 互換パッケージを扱う。`acp` 公開名や builder 関連の下位実装・公開経路を確認する際の入口。

## Read this when
- `acp` 互換公開名の存廃や oracle 側実体への移行導線を確認したいとき。
- `acp.builder` の互換 import 経路、公開入口、canonical builder 実装への委譲関係を確認・変更したいとき。
- builder に関連する oracle、realization、TUI、session、indexing などの下位パッケージの入口を選びたいとき。

## Do not read this when
- 個別 builder の canonical 実装や正本仕様を確認したいときは、対応する下位実装または oracle 側を直接読む。
- TUI 画面本体、CLI 全体の動作、builder と無関係な処理を調査するとき。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変更したいときは、具体的な実体モジュールを直接読む。

## hash
- 7b02a4bee63eef899d0a6db5d5d80cf5efb922d0c39053b11447f9ed5a7af2bb

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
- cmoc の CLI サブコマンドや Codex 実行系で共有する runtime helper 群を集約する commons パッケージ。設定、Git、パス、状態、ログ、結果、エラー、Codex subprocess、INDEX 更新などの共通処理への入口であり、個別 runtime 領域を変更・調査する際は配下の担当モジュールへ進む。

## Read this when
- CLI サブコマンド間で共有される runtime API や helper の責務を確認するとき
- Codex exec/TUI、設定、Git、パス、状態、ログ、結果、エラー、INDEX 更新などの共通実装を変更・調査するとき
- 共通処理の適切な担当モジュールや公開 API の入口を特定するとき

## Do not read this when
- 特定サブコマンド固有の業務処理や引数定義だけを確認するとき
- 正本仕様や prompt の定義を確認するときは、対応する oracle 文書・oracle source を直接読む
- 特定の runtime helper の実装詳細が明らかな場合は、commons 配下の該当モジュールを直接読む

## hash
- 4bd7c163bd59832d576aefe330e556d3700336b7b9f369a12d9ce4b5bf32fe00

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
- cmoc の各サブコマンド実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの CLI 入口・実行フローを確認するための上位ルーティング地点で、個別処理は各サブディレクトリまたは実装ファイルへ進む。apply と review は現在実装本文がなく、将来の実装追加先として扱う。

## Read this when
- サブコマンドの実装構成や CLI 実行入口を横断的に確認するとき。
- 特定サブコマンドの実装箇所を探し、対応する下位ディレクトリやファイルへ進むとき。

## Do not read this when
- 特定サブコマンドの内部処理、共通 runtime、git 操作、状態管理、TUI builder などの詳細を調査するときは、対応する下位実装を直接読む。
- サブコマンド以外の共通実装や正本仕様だけを確認するとき。

## hash
- 4f8069e3dc2e32be826cde08fe5fd6b6d0b15a0aeee43381f7112ded5c18fea8
