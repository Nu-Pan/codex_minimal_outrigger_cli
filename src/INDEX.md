# `acp`

## Summary
- ACP互換層の公開入口と、`acp.builder.*` の互換入口・realization adapter をまとめるディレクトリ。canonical な oracle 実装への接続や、各種 builder adapter の下位要素へ進む起点となる。

## Read this when
- `acp` 公開名の互換維持・削除や、既存の `acp.*` 参照を実体モジュールへ移行する導線を確認するとき。
- ACP builder 全体の互換構成、canonical 実装との接続、prompt のコードフェンス補正、workload・command・TUI・session 向け adapter を調査するとき。

## Do not read this when
- `acp.builder.*` の具体的な処理や、TUI・session・oracle・realization など個別実装の詳細だけを確認したいとき。対応する下位実体を直接読む。
- 利用側の参照や利用者向け公開面だけを調査したいとき。各参照元を直接読む。

## hash
- 6ed43809a28b509b9bce95d5c7127323b0c9d6d4a329e8ec8423216892f79ace

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
- cmoc の commons パッケージ。共通 runtime API と、Codex 実行、CLI lifecycle、設定、Git、パス、ログ、状態、エラー、INDEX 更新などの横断的な補助機能を提供する。
- パッケージ入口と共有 API は __init__.py・cmoc_runtime.py から確認でき、各領域の具体的な実装は対応する runtime_* モジュールへ進む。

## Read this when
- commons の共通 runtime helper、公開 API、パッケージ入口を確認・変更するとき
- Codex 実行、CLI lifecycle、INDEX 更新、設定、Git、パス、ログ、状態、エラーなどの共通処理を調査するとき
- 特定の runtime_* モジュールの責務や実装詳細を確認するとき

## Do not read this when
- 特定サブコマンド固有の業務処理や入出力だけを調査するとき
- 利用者向け仕様や出力形式などの正本を確認するときは、対応する oracle 文書を直接読む
- 単一の runtime 領域の詳細が明確な場合は、commons 全体ではなく対応する runtime_* モジュールを直接読む

## hash
- be86d4d1df068c9ed1824d433b46d8e1f779248584de9fcda2e220ad2bd420c9

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの各サブコマンド実装への入口を提供する。apply と review は現時点で実装本文がない。
- realization、run、session には、各 workload・lifecycle・状態管理・差分処理などの関連実装が集約されている。

## Read this when
- CLI サブコマンドの実装構成や、対象サブコマンドの実行フローを確認・変更するとき。
- doctor、indexing、oracle、realization、run、session、tui のいずれかを調査するとき。

## Do not read this when
- 特定サブコマンドのより限定された共通処理や詳細実装だけを確認するときは、該当する下位実装を直接読む。
- apply または review の具体的な実装を確認したいときは、実装追加後に該当箇所を読む。
- このディレクトリに属さない共通 runtime、builder、oracle 文書の仕様だけを確認するとき。

## hash
- 3216ea22f49e286b31f8e35552db99b7788acfba601720f36b821593a139d986
