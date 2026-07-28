# `acp`

## Summary
- ACP builder 関連の realization 実装をまとめた入口。互換公開、builder adapter、indexing、session、TUI などの下位領域へ進むための案内を提供する。

## Read this when
- ACP builder の実装領域や下位モジュールの入口を確認するとき。
- 互換 import、builder adapter、prompt の code fence 保護、session・TUI・indexing 向け builder を調査するとき。

## Do not read this when
- canonical な oracle 仕様や実装を確認するときは、対応する oracle 側を直接読む。
- builder 以外の CLI、TUI、apply、refactor などの処理本体を調査するとき。
- review builder の具体的な finding 処理を変更するとき。

## hash
- 674476fe6219ebcaa2ba07598f84807d45cb198669bd477faa0a858e9cc96fab

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
- cmoc の共通 runtime helper を集約する commons パッケージ。設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果型、INDEX 管理など、CLI 全体で共有される実行時機能を扱う。各機能の個別実装や公開 API を確認するための入口。

## Read this when
- 複数の CLI 機能にまたがる共通 runtime helper の実装・公開 API・利用箇所を調査または変更するとき
- 設定、Git、Codex 実行、INDEX 管理、ログ、パス、状態、エラー、run lifecycle などの共通処理の担当箇所を探すとき

## Do not read this when
- 特定の CLI サブコマンド固有の業務ロジックやテストだけを確認するとき
- 共通機能の正本仕様を確認したいとき。対応する oracle 文書を直接読む
- 対象となる個別 runtime module が明確なとき。その module を直接読む

## hash
- f5ab78f20fec8bb96c7854750e2b2cca9defcf93b4ef3ef25cf953f77ce295a2

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor・indexing・oracle・realization・run・session・tui などの実行入口と関連パッケージへの下位要素を提供する。apply と review は現時点で実装本文がない。

## Read this when
- サブコマンドの実装構成や、各サブコマンドの実行入口を確認・変更するとき。
- doctor、indexing、oracle、realization、run、session、tui の処理フローや責務分担を調査するとき。

## Do not read this when
- 個別サブコマンドの詳細処理だけを確認する場合は、該当する実装ファイルや下位パッケージを直接読む。
- サブコマンド共通処理、参照される oracle 仕様、または専用の補助処理だけを確認する場合は、それぞれの直接の実装・仕様文書を読む。

## hash
- 6831225262057e5a5cddc9ed9b75c93c031f5d0b5f08ce97137e6484dded7690
