# `acp`

## Summary
- acp 互換の公開入口と builder adapter 群を扱うディレクトリ。既存の acp.* import 経路を oracle 側の canonical 実装へ移行・維持・削除する判断や、builder 配下の oracle／realization／feedback／indexing／session／TUI／quota probe への入口を確認する際の起点となる。

## Read this when
- 既存の acp.* または acp.builder.* import 経路の互換性、移行、削除条件を調査するとき
- acp.builder 配下の adapter 構成と、canonical 実装への委譲関係を確認するとき
- oracle edit／investigation の realization adapter や各領域の builder へ進む入口を探すとき

## Do not read this when
- oracle 側の canonical 実装の仕様や詳細を調査・変更するときは、対応する oracle の実体を直接読む
- acp 配下の具体的な内部挙動や共通処理の実装を調査・変更するときは、該当する実体モジュールを直接読む
- builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む

## hash
- 5c8ad5573a628c2248ae9b55dd4fc109c2009349bff27ba13d1db76cabef02b0

# `basic`

## Summary
- `basic.*` の互換 import を維持するための realization 側公開入口。ACP 型、path model、構造化文書 API を正本実装から再公開し、個別実装や正本仕様は保持しない。各モジュールの公開経路・互換参照を確認するための下位入口である。

## Read this when
- `basic.*` の互換 import を維持・削除する判断をするとき。
- realization 側から ACP 型、path model、構造化文書 API がどの経路で公開されるかを確認するとき。
- 個別モジュールの再公開関係を調査するとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各再公開元の oracle 側を直接読む。
- 個別 API の詳細や参照削除の影響だけを調べるときは、対象モジュールまたは参照箇所へ直接進む。
- `basic.*` と無関係な処理を調査・変更するとき。

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
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 実行、Codex exec/TUI、設定・ログ・パス、Git/worktree、状態管理、feedback、INDEX 更新など、複数の実行経路で共有される機能の実装入口を提供する。
- 共通 runtime API の公開入口から個別 lifecycle・設定・プロセス・状態・feedback・indexing 機能へ進むためのディレクトリであり、特定機能の内部挙動を調べる場合は対応する個別モジュールを直接読む。

## Read this when
- cmoc の複数の CLI・Codex 実行経路で共有される runtime 機能の配置や責務の全体像を確認するとき
- 共通 runtime API、INDEX 更新 lifecycle、Codex 実行境界、設定・Git・状態・feedback・run lifecycle などの実装入口を選ぶとき
- commons 配下の個別 helper を利用・変更する前に、関連する共通機能の構成を把握するとき

## Do not read this when
- 特定の runtime helper の内部実装や個別の公開シンボルだけを調べる場合は、対応する個別モジュールを直接読むとき
- CLI サブコマンド固有の業務ロジック、Codex の正本仕様、feedback の保存仕様、INDEX entry の生成 prompt・schema だけを確認する場合は、それぞれの専用実装または仕様へ直接進むとき

## hash
- 1814f6d78c46f81b14b87ca82b75f43a4fe4ac1e0636bd0ac4f76e138dbe438f

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
- Typer で構成された cmoc CLI の最上位入口。doctor、tui、indexing、feedback と、session・oracle・realization・run のサブコマンド群を登録し、各処理実装へ振り分ける。
- Click/Typer の互換処理と CLI 引数解析エラーの cmoc 形式への変換を閉じ込め、console script から `cmoc` としてアプリケーションを起動する。

## Read this when
- cmoc の CLI コマンド構成、サブコマンド登録、起動入口を変更または調査するとき
- Typer と Click のバージョン互換、補完 probe、または CLI 引数解析エラーの報告形式を確認するとき
- 新しい最上位コマンドやサブコマンドを追加し、対応する実装への接続箇所を確認するとき

## Do not read this when
- 特定サブコマンドの処理内容や業務ロジックを調査するときは、対応する `sub_commands` 配下の実装を直接読む
- `CmocError` やエラー描画の共通仕様そのものを調査するときは、`cmoc_runtime` と該当する app specification を読む
- oracle、realization、session、run の内部処理を変更するときは、この CLI 登録層ではなく各サブコマンド実装と対応仕様を読む

## hash
- 36ab2a93a49ac1ed50f74e548bdf0eed0219fade8a647b8bd930a8bde81c3004

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
- CLI サブコマンド実装を集約するディレクトリ。apply、doctor、feedback、indexing、oracle、realization、review、run、session、tui など、各サブコマンドの入口または上位ルーティング対象を確認する際の起点となる。
- サブコマンド全体の実行フローや構成を把握する場合はここから該当するサブコマンドへ進み、個別の正本仕様・共通 runtime・下位実装の詳細が目的なら、それぞれの直接の参照対象へ進む。

## Read this when
- CLI サブコマンドの実装構成や、対象サブコマンドの入口を特定するとき
- 複数のサブコマンドにまたがる実装配置や、該当する下位 package・module への進み方を確認するとき

## Do not read this when
- 利用者向けサブコマンドの正本仕様や外部契約だけを確認するとき
- 共通 CLI runtime、Git 操作、state、publication などの実装詳細を直接調べるとき
- 対象サブコマンドが明確で、その配下の実装や仕様を直接読む方が適切なとき

## hash
- 32f4929e7b54f4a13c471e2964cc97c37bf7f59158c9d43eab0bc81531a5a2aa
