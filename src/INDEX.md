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
- cmoc の共通ランタイム機能をまとめた commons パッケージ。設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果型、INDEX 管理など、複数の CLI 機能から利用される基盤処理を扱う。
- 個別の責務ごとに実装が分かれており、共通 API の再公開入口と、各ランタイム機能の具体的な実装を確認するための起点となる。

## Read this when
- 複数の CLI 機能にまたがるランタイム共通処理を調査・変更するとき
- 設定、Git、Codex subprocess、INDEX lifecycle、ログ、パス、状態、run lifecycle などの担当実装を特定するとき
- commons パッケージの公開 API や、共通 helper の責務分担を確認するとき

## Do not read this when
- 特定サブコマンド固有の業務ロジックや CLI 引数だけを調査するとき
- 利用者向け仕様や正本となる oracle 文書だけを確認したいとき
- commons 内の特定機能が明らかな場合は、このディレクトリ全体ではなく対応する個別実装へ直接進むとき

## hash
- 46f2763ed535cff70604a99d3ca8c822158e1e0c5022c3836d75404aaab42cd4

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
- 各サブコマンドの CLI 実装パッケージをまとめるディレクトリ。apply・review は現在実装がなく、doctor・indexing・oracle・realization・run・session・tui の実装入口と下位処理へのルーティングを提供する。

## Read this when
- サブコマンドの実装配置や、複数サブコマンドにまたがる CLI 入口の構成を確認するとき。
- doctor、indexing、oracle、realization、run、session、tui の実行フローや責務分担を調査・変更するとき。
- apply または review の実装追加先を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細処理を調査するときは、対象の実装ファイルまたは下位パッケージを直接読む。
- 共通 runtime、git・state・report・indexing helper、TUI builder、prompt editor、conflict resolution などの共通実装や仕様だけを調査するとき。
- サブコマンド以外の CLI 実装を扱うとき。

## hash
- 5a5f1573cd27ba4eab0d9195807e7a0d9b0bf1934f8cf62e287533118091d8bf
