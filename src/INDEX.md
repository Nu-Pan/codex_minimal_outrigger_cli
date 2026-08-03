# `acp`

## Summary
- `acp` 互換名前空間を提供する realization パッケージ。canonical な `oracle` 実装への互換 import、quota probe の fallback、動的 prompt の code fence 補正、indexing・TUI builder の再公開を扱う。互換入口全体の存廃や `acp` 参照の移行を検討する際の上位入口であり、個別の生成ロジックは下位要素へ進む。

## Read this when
- 既存の `acp.*` import 経路を維持・削除・canonical 実装へ移行する判断をするとき。
- quota availability probe、prompt fence 補正、indexing builder、TUI builder の互換接続先を特定するとき。
- builder 配下の oracle・realization・session・indexing・TUI の構成を把握し、該当する下位要素へ進む必要があるとき。

## Do not read this when
- canonical な実装や正本仕様の内容を確認したいときは、対応する `oracle` 側の実体を直接読む。
- 個別 builder の詳細な生成ロジックや prompt の変換規則だけを調査するときは、該当する下位モジュールを直接読む。
- `acp` 互換層と無関係な CLI、TUI、共通処理の挙動を調査するとき。

## hash
- c6a3101eda3c4767814e5e2db6ed0ae2fe3d78b7022a6c71837f778e04b0f8a8

# `basic`

## Summary
- `basic` 配下の互換 import 入口をまとめるディレクトリ。ACP 型、path model、構造化文書 API などを正本や oracle 側から再公開し、既存の `basic.*` 公開面を維持する。個別実装や正本定義を確認する場合は各再公開元へ進む。

## Read this when
- `basic.*` の互換 import を維持・廃止する判断をするとき。
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の公開経路や再公開元を確認するとき。
- 利用者向け公開面の移行先や互換層の維持条件を調べるとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各 oracle 側の定義を直接読む。
- 個別モジュールと無関係な処理を調査・変更するとき。

## hash
- 292bc262556c427d8a4a7636a2c7e14127adfdea1c7d57f167e9bfa04d4ce5ea

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
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 実行 lifecycle、Codex exec/TUI、設定・状態・Git・パス・ログ・エラー、editing run、INDEX 更新、prompt editor など、上位機能が横断利用する実行時基盤を提供する。個別機能の調査・変更では、ここから対応する runtime モジュールへ進む。

## Read this when
- 複数の runtime 領域にまたがる共通 API や依存関係を確認するとき
- CLI、Codex、editing run、INDEX 更新などの共通実行基盤を調査・変更するとき
- commons 配下の個別実装への入口を選ぶ必要があるとき

## Do not read this when
- 特定の runtime helper の実装詳細だけを調査・変更するときは、対応する個別モジュールを直接読む
- 正本仕様や個別コマンドの利用者向け挙動だけを確認するときは、対応する oracle 文書や command 実装を直接読む
- commons と無関係な機能を調査・変更するとき

## hash
- cfc853080f70f0dbffbc07b4d2ab537304a5254ecb67b5c4871ee8e6be45a026

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
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、indexing、tui、session、run、oracle、realization などの実行入口・パッケージへ進むための上位ルーティングで、apply と review は現時点で実装本文がない。

## Read this when
- CLI サブコマンドの実装構成や、特定サブコマンドの実行入口を確認・変更するとき。
- doctor、indexing、tui、session、run、oracle、realization の実行フローや下位実装への入口を探すとき。

## Do not read this when
- サブコマンド共通の CLI ランタイムや設定の詳細だけを調査するとき。
- 特定サブコマンドの処理詳細を確認する場合は、このディレクトリ全体ではなく該当する下位実装を直接読むとき。
- oracle や realization の正本仕様、共通実装、個別処理の詳細だけを確認するとき。

## hash
- 69fac896d4ee6e6a00a3883a4b2c015247b52df888abe2c06b2dedfba7446b54
