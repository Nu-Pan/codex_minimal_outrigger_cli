# `acp`

## Summary
- ACP互換層の公開入口とbuilder関連の互換実装をまとめるディレクトリ。既存の`acp.*`参照をcanonicalな`oracle`実装または実体モジュールへ移行・整理する際の入口となる。
- 直下の公開入口は`acp`名の存廃や利用者向け参照の切り替えを扱い、builder配下はoracle委譲、prompt補正、quota probe、oracle・realization・TUI・session・indexing関連のbuilder adapterを扱う。

## Read this when
- `acp`互換層全体の構成や、公開入口からbuilder関連の下位要素へ進む経路を確認したいとき。
- 既存の`acp.*` import経路を維持・整理し、canonicalなoracle実装へ移行する範囲を判断したいとき。
- builder共通のprompt境界補正やquota probe、各種builder adapterの入口を横断して調査したいとき。

## Do not read this when
- 個別builderの生成ロジックや挙動だけを調査・変更したいときは、対応する下位パッケージまたはモジュールを直接読む。
- canonicalなoracle実装や正本prompt仕様を確認したいときは、oracle側の対象を直接読む。
- `acp.*`を利用するCLI・TUIなど呼び出し元の公開面を調査したいときは、各利用箇所を直接読む。

## hash
- 3ef630ce42db9e98bafb4ce93d41d3013ba3b5847dec653013c34243b3df4431

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
- cmoc の共通 runtime helper を集約する commons パッケージ。Codex 実行、CLI lifecycle、設定、Git、パス、ログ、状態、結果、エラー、INDEX 更新など、複数の CLI サブコマンドで共有される実行基盤の入口。
- runtime_codex や runtime_codex_exec/runtime_codex_tui、runtime_cli、runtime_config、runtime_git、runtime_paths、runtime_state など、目的別モジュールへ進むためのディレクトリ。

## Read this when
- 複数の CLI サブコマンドにまたがる共通 runtime API、実行 lifecycle、設定・Git・path・logging・state の処理を調査または変更するとき
- Codex exec/TUI の起動、retry、process 制御、Structured Output、ログ、INDEX preflight の連携を確認するとき
- editing run や session の lifecycle、worktree、state、report、変更 path 検査を確認するとき

## Do not read this when
- 特定の runtime helper の詳細だけを確認する場合は、対応する個別 runtime_* モジュールへ直接進む
- CLI サブコマンド固有の業務処理、引数、入出力仕様を調査する場合は、該当する上位実装や oracle 文書へ進む
- 設定・ログ・エラー・INDEX の正本仕様そのものを確認する場合は、対応する oracle 文書を直接読む

## hash
- 5506d73d9a6e6c01f40df2795f02426db3c6a3dbe155eff32336b1bbbea6a271

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
- 複数の CLI サブコマンド実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tui などの実行入口と、配下パッケージへのルーティングを提供する。apply と review は現在実装本文がない。

## Read this when
- サブコマンドの実装構成や、複数サブコマンドにまたがる実行入口を確認・変更するとき。
- doctor、indexing、oracle、realization、run、session、tui のいずれかのサブコマンド実装を扱うとき。

## Do not read this when
- apply または review の具体的な実装を確認したいとき。現在は実装本文がないため、実装追加前の配置確認以外では読む必要がない。
- 共通 runtime、共通 indexing、oracle review の仕様、TUI builder、prompt editor、Git 操作、state schema などの具体的な処理だけを調査するときは、対応する直接の実装または仕様文書を読む。

## hash
- 7dd987daa0c51f651fb1bdf9caa2e92886e62457e0be417eea7515c7b9ad0a8b
