# `acp`

## Summary
- ACP互換の公開入口を扱い、既存の`acp.*`参照を`oracle.*`または実体モジュールへ移行する際の入口となる。
- ACP builder realizationのパッケージ。oracle実装への互換入口、builder共通処理、oracle・realization・session・TUI・indexing向けadapter、quota probeのfallbackをまとめ、各下位要素への入口を提供する。

## Read this when
- `acp`という公開名の存廃や、既存参照をoracle側の実体へ切り替える導線を確認したいとき。
- ACP builder realizationの構成、互換import、oracle実装への委譲、builder共通処理、各builder adapterの入口を確認したいとき。

## Do not read this when
- `acp`配下の具体的な実装内容や移行先の詳細だけを確認したいときは、該当する実体モジュールを直接読む。
- canonicalなoracle builderの仕様・実装、またはTUI・CLI・sessionなど利用側の挙動を確認したいときは、それぞれの対象を直接読む。

## hash
- 37a5cdccd2d3f31d506aaed6cc61ba09b39548bbdba0780b9ea25a7280fc4b09

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
- cmoc 共通 runtime helper を提供する commons パッケージ。CLI 実行、Codex 呼び出し、設定・状態・パス、Git、ログ、エラー、run lifecycle、INDEX 管理などの横断的な実行時機能への入口を含む。
- 個別ファイルの entry は、それぞれの runtime 責務を確認・変更する際の直接の入口として機能する。

## Read this when
- commons 配下の共通 runtime 機能の入口や、複数の runtime 領域にまたがる依存関係を確認するとき
- CLI、Codex、設定、状態、Git、ログ、パス、run lifecycle、INDEX 管理の共通実装を変更・調査するとき
- 特定の runtime helper の責務に対応する実装ファイルを選ぶ必要があるとき

## Do not read this when
- 特定の runtime helper の実装詳細だけを確認したい場合は、対応する個別モジュールを直接読む
- 利用者向け仕様や正本テンプレートを確認したい場合は、対応する oracle file を読む
- commons と無関係な CLI サブコマンド固有処理や、単一領域の仕様だけを調査する場合

## hash
- 0f4fdb0812c0da48850db68d45cbe82384da26f1f422c88f19eb961882eeadb6

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
- `src/sub_commands` は各 cmoc サブコマンドの CLI 実行入口をまとめるディレクトリ。doctor・indexing・oracle・realization・run・session・tui などの実装と、未実装サブコマンドの配置先を案内する。個別処理の詳細は配下の担当ファイルや commons 実装へ進むための入口として使う。

## Read this when
- cmoc サブコマンドの実装配置や一覧を確認するとき。
- 特定サブコマンドの CLI 実行入口を調査・変更するとき。
- サブコマンドから下位実装または共通実装へ進む先を判断するとき。

## Do not read this when
- 特定サブコマンドの詳細処理だけを調査する場合は、配下の該当実装ファイルを直接読む。
- 共通 lifecycle、indexing、report などの canonical 実装だけを確認する場合は、対応する commons 実装を直接読む。
- oracle の正本仕様や preprocess など、実装入口以外の内容を確認する場合は、参照先の oracle 文書を直接読む。

## hash
- 6b39dbc3ec2ddcfba1d4f4fb6f717373c5c1cd1ab7c875dfce1fd6d309502ff3
