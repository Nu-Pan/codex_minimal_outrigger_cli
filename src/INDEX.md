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
- cmoc 共通 runtime helper を提供する commons パッケージ。CLI 実行、Codex 実行、設定・状態・パス管理、Git、ログ、エラー、INDEX 更新、editing run lifecycle などの runtime 実装への入口。

## Read this when
- 複数の runtime 機能にまたがる共通 API や依存関係を確認するとき
- 特定の runtime helper、Codex 実行、設定・状態・Git、INDEX 更新、editing run lifecycle の実装を調査・変更するとき
- commons パッケージの初期化や共通 runtime 公開入口を確認するとき

## Do not read this when
- 単一の runtime 機能の詳細だけを調査する場合は、対応する個別モジュールを直接読む
- 利用者向け正本仕様や INDEX entry の文章を確認する場合は、対応する oracle file または対象本文を直接読む
- commons 配下を利用するだけで、共通実装の責務や依存関係を変更しない場合

## hash
- d9d43d36c42a8d172a26c7ec523dd7974582e7e0b492ef5d010e984fb15fdc7c

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
- cmoc の各サブコマンド実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの個別実装への入口を提供し、未実装の apply・review も配置予定場所として示す。

## Read this when
- 特定のサブコマンド実装の配置や、実行フロー・ライフサイクル処理・TUI 起動処理の入口を確認するとき。
- 複数のサブコマンドにまたがる実装パッケージの構成や、対象サブコマンドの下位実装を探すとき。

## Do not read this when
- サブコマンド共通の runtime、builder、report、lifecycle などの実装詳細だけを調査するとき。
- 特定サブコマンドの詳細を確認する場合は、このディレクトリ全体ではなく対応する個別実装や下位パッケージを直接読むとき。
- oracle 文書や preprocess など、サブコマンドから参照される仕様・処理自体を確認するとき。

## hash
- b7f57b5a05dd794c9849dd81230dd25e0a9a714050cf1efac15460d801fcbb78
