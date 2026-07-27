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
- cmoc の共通 runtime helper を集約する commons パッケージ。設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果、INDEX lifecycle など、CLI 実装が横断利用する共通機能への入口。

## Read this when
- 複数の CLI 機能にまたがる runtime helper の責務や公開 API を確認・変更するとき
- 設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果、INDEX 更新の共通処理を調査するとき
- 特定機能の実装先となる commons 配下の個別モジュールを選ぶとき

## Do not read this when
- 特定の runtime helper の実装詳細だけを確認したいときは、対応する個別モジュールを直接読む
- 特定サブコマンド固有の処理、引数定義、業務ロジックだけを調査するとき
- oracle 文書に定義された利用者向け仕様や Codex 実行仕様だけを確認するとき

## hash
- 189bd31b85f8b4aaea530d03def1347db420fd0d0f630dd2d36f8ebe87c11120

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
- サブコマンドごとの CLI 実行入口を配置するディレクトリ。apply・review は現在実装本文がなく、doctor・indexing・oracle・realization・run・session・tui の実装入口を提供する。各サブコマンドの詳細は配下の対応ファイルまたはパッケージを入口として確認する。

## Read this when
- 複数の cmoc サブコマンドの実装配置や入口を横断して確認するとき。
- 特定サブコマンドの CLI 実行フロー、パッケージ構成、または実装追加場所を判断するとき。

## Do not read this when
- 単一サブコマンドの詳細実装を確認したいときは、対応する配下の実装ファイルを直接読む。
- 共通 runtime、git・state・process・report helper、workload 共通処理などの下位実装詳細を確認したいときは、それぞれの実装を直接読む。
- サブコマンドの利用者向け仕様や oracle 仕様を確認したいときは、対応する oracle 文書を先に読む。

## hash
- 7b61d4c338ff4c0e57a8276d05e6d707246aca86fc3d8fe1b0216ed43533c3f5
