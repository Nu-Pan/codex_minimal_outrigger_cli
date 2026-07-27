# `acp`

## Summary
- `acp` 互換公開入口を扱い、既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する際の判断材料を提供する。
- ACP builder の互換入口と各種 builder adapter へのルーティング起点。canonical な oracle 実装への接続、Markdown code fence 補正、indexing・session・TUI・realization・oracle・quota probe 関連の builder 経路を扱う。

## Read this when
- `acp` という公開名の維持・削除や、既存参照を oracle 側の実体へ切り替える方法を確認したいとき。
- ACP builder のパッケージ構成、互換 import 経路、または特定の builder 系統への入口を確認したいとき。
- prompt 生成時の code fence 補正や、indexing・session・TUI・realization・oracle・quota probe 関連の下位要素を調査するとき。

## Do not read this when
- `acp` 配下の具体的な実装や移行先の詳細だけを知りたいときは、対象の実体モジュールを直接読む。
- 個別 builder の prompt 構築や処理本体を調査するときは、該当する下位要素を直接読む。
- canonical な oracle builder の仕様・実装、または ACP builder と無関係な CLI・TUI・agent call の利用箇所を調査するとき。

## hash
- 0e62104696408d058db918541ff0e58da0d7e4b842c0d01cfd46050afa7aba94

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
- cmoc の共通 runtime 機能を集約する commons ディレクトリ。設定、Git、Codex 実行、プロセス、パス、状態、ログ、結果型、INDEX 管理など、CLI 複数箇所から利用される実行時補助機能への入口。

## Read this when
- 複数の CLI 実装で共有される runtime helper の責務や公開 API を確認・変更するとき
- 設定、Git、Codex 実行、INDEX lifecycle、プロンプト入力、ログ、パス、状態管理などの共通処理を調査するとき

## Do not read this when
- 特定の CLI サブコマンド固有の業務ロジックだけを調査・変更するとき
- 共通機能の正本仕様や利用者向け挙動を確認したい場合に、対応する oracle 文書や個別実装へ直接進めるとき

## hash
- fc4ec0012c4eaa785d39b596b110e305bb9452f0d4c5b38a399415e9385d1104

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
- cmoc の各サブコマンド実装を配置するディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの CLI 入口と関連パッケージへのルーティング起点であり、apply・review は現在実装本文がない。

## Read this when
- サブコマンドの実装構成や、対象サブコマンドの CLI 実行入口を確認・変更するとき。
- oracle、realization、run、session など、配下のサブコマンドパッケージをどこから調査するか判断するとき。

## Do not read this when
- サブコマンド以外の共通実装や、個別サブコマンドの詳細処理を直接調査する場合。
- 対象サブコマンドが明確な場合は、このディレクトリ全体ではなく該当する実装ファイルまたは下位パッケージを直接読む。

## hash
- 9c46c69238019ecb18895440e6960811a55067491d7d526c1236d627fa27b6d4
