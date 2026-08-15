# `acp`

## Summary
- `acp` 互換公開入口と ACP builder 群をまとめるディレクトリ。`acp.*` 参照の互換性や builder の構成を確認し、詳細調査では下位要素へ進むための入口である。

## Read this when
- `acp` 公開入口の存廃と既存参照への影響を確認するとき
- ACP builder の互換入口、共通処理、workload 別 adapter の配置を把握するとき
- 対象ディレクトリ直下から、調査対象となる下位要素への入口を判断するとき

## Do not read this when
- 特定の builder の具体的な入出力や内部実装を調査するとき
- `oracle` 側の実体モジュールや個別 adapter の詳細を直接確認したいとき
- ACP builder と無関係な処理を調査するとき

## hash
- 68f89078a07fdab2bacbbc2570af487c3d91acbcae895c95dfd7df05112e985f

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
- cmoc の実行時共通機能を集約する commons パッケージ。CLI の実行境界、Codex subprocess、設定・ログ・Git worktree・パス・状態管理、feedback、report、run lifecycle など、複数の処理経路から利用される runtime API とその下位実装への入口を提供する。
- INDEX.md の検査・生成 lifecycle、prompt editor、doctor、refactor state、実行結果・エラー・通知など、個別の共通 runtime 責務を確認・変更する際の入口となる。下位の機能別モジュールへ進むためのディレクトリ単位のルーティング対象。

## Read this when
- CLI や Codex の実行基盤、設定、ログ、Git worktree、パス、状態、feedback、report、run lifecycle など、複数機能で共有される runtime 処理の入口を探すとき
- commons 配下の共通 API または個別 runtime helper の責務を確認・変更するとき
- INDEX.md 更新、prompt editor、doctor、refactor state、実行結果・エラー・通知などの共通実装を調査するとき

## Do not read this when
- 特定のサブコマンド固有の業務処理や利用者向け仕様だけを調べるとき
- 特定の runtime helper の内部実装、公開シンボル、状態遷移、保存形式を直接確認したいときは、commons 配下の対応する個別モジュールへ進む場合
- 正本仕様や prompt の生成規則など、commons の実装責務ではなく対応する仕様・定義ファイルが直接の確認対象である場合

## hash
- b053631c0c6f101058e4e3449e9dc458952234d516fd9f342a96df0f1e454449

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
- cmoc のサブコマンド実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui の CLI 入口やライフサイクル処理への入口を提供し、各サブコマンドの下位実装へ進む起点となる。apply と realization review は現在実装本文がない。

## Read this when
- cmoc のサブコマンド構成や、対象サブコマンドの実装入口を確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui の実行フローや責務分担を調査・変更するとき。
- サブコマンドの下位実装へ進む前に、どのパッケージ境界を読むべきか判断するとき。

## Do not read this when
- 特定サブコマンドの詳細実装、共通 CLI ランタイム、正本仕様を直接確認する場合は、それぞれの対象を読むとき。
- サブコマンドに関係しない処理を調査するとき。
- apply または realization review の具体的な実装内容を確認するとき。

## hash
- 299455882f7842539dadff06c26478038903610c5f5afc8cde2b0b9dbaf7ea8b
