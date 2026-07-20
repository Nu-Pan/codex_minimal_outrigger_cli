# `acp`

## Summary
- `acp` 互換公開入口をまとめるパッケージ。`acp.*` の既存参照を維持しつつ、`oracle.*` または canonical 実体へ委譲する導線を提供する。
- `acp.builder` 配下には、TUI、session、indexing、realization、oracle、quota probe などのビルダー関連互換入口が含まれる。

## Read this when
- `acp` 公開名や互換入口の存廃を判断するとき。
- 既存の `acp.*` または `acp.builder.*` import 経路を維持・変更するとき。
- ビルダー関連サブパッケージの canonical 実装への委譲経路を辿るとき。

## Do not read this when
- 具体的な TUI、session、apply、refactor などの内部実装を直接調査・変更したいとき。
- canonical な正本仕様や実体モジュールそのものを確認したいとき。

## hash
- 64311522fa0e3a0c66afe888a9acff7a45f737437301fe6908a1b9b1c87016ff

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
- cmoc の共通 runtime helper を集約する commons パッケージ。Codex 実行、CLI lifecycle、設定、Git、パス、状態、ログ、エラー、結果、INDEX 更新など、複数の CLI サブコマンドで共有する基盤機能への入口。
- 個別の責務は配下の runtime_* モジュールに分かれているため、具体的な挙動の変更・調査では該当モジュールへ進む。

## Read this when
- 複数の CLI サブコマンドで共有される runtime helper の配置や責務を確認するとき
- Codex 実行、設定、Git、パス、状態、ログ、エラー、結果、INDEX 更新の共通実装を探すとき
- commons 配下の個別モジュールを利用・変更する前に、共通 runtime API の構成を把握するとき

## Do not read this when
- 特定の runtime helper の実装詳細を直接確認したいときは、対応する runtime_* モジュールへ進む
- CLI サブコマンド固有の業務処理や入出力を調査するとき
- oracle に定義された仕様や Codex 実行方式固有の詳細を確認するときは、対応する oracle 文書または専用実装を直接読む

## hash
- 5b9f8e2f104746fac23f16603214de57c84c1ff56cc8d60a7f43cd60bbb9bb9f

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
- Typer を使った cmoc CLI のルート定義。doctor・tui・indexing と、session／oracle／realization／run 配下のサブコマンドを登録し、各処理を対応する実装関数へ委譲する。CLI 引数解析エラーの cmoc 形式への変換、補完 probe の扱い、oracle review の scope 定義も含む。各サブコマンドの具体的な処理を確認する場合は、登録先の sub_commands 実装を読む。

## Read this when
- cmoc の CLI 入口、サブコマンド構成、Typer のアプリ階層を確認するとき
- CLI 引数解析エラーや自動補完時の起動挙動を変更・調査するとき
- 新しいトップレベルまたは既存階層のサブコマンドを登録するとき

## Do not read this when
- 特定サブコマンドの業務処理や状態変更の実装を調査するとき
- oracle review、session、run など個別機能の仕様・テストを確認するときは、対応する sub_commands 実装や oracle 文書を直接読む

## hash
- e54ca99e6da1e630eed277aea1d7adc7187cc96ba4e8c9071a285090d8a2845a

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor・indexing・oracle・realization・run・session・tui などの実行入口と、各サブコマンド実装へ進むためのルーティング対象。apply・review は現時点で実装本文がない。

## Read this when
- CLI サブコマンドの構成や実行入口を確認するとき。
- 特定サブコマンドの実行フロー、worktree 条件、ライフサイクル、TUI 起動、oracle／realization 処理を調査・変更するとき。

## Do not read this when
- 共通 runtime、git 操作、INDEX 更新、prompt、state、report などの内部処理だけを確認したいときは、対応する共通モジュールや下位実装を直接読む。
- サブコマンド実装の追加先だけを確認する場合は、該当する下位ディレクトリを直接読む。

## hash
- 92eaa66dfc9816a329e70e18681bc7f99c647a6c616b598b26bf78a26e3e4922
