# `acp`

## Summary
- `acp` 互換公開入口を扱う realization package。既存の `acp.*` import 経路を維持しつつ、canonical な `oracle` 側の builder や実体モジュールへ委譲・適合する。
- 下位には、builder の共通 Markdown fence 補正、indexing・feedback・session・TUI・quota probe、oracle command、realization apply/refactor、review adapter がある。

## Read this when
- 既存利用者や realization code の `acp.*` 参照を維持・移行・削除する条件を確認するとき。
- canonical builder への委譲に加え、動的 prompt 本文・差分・review finding の埋め込み補正が必要な互換 adapter の入口を探すとき。
- builder 配下の command 別 adapter や共通 prompt fence 処理へ進む前に、互換層全体の責務を把握したいとき。

## Do not read this when
- canonical な `oracle` 側の builder の仕様や prompt 本文を調べたいとき。
- 個別 builder の内部挙動、具体的な command 処理、または利用者向けの参照元を直接調べたいときは、該当する下位要素や参照元へ進む。
- `acp.*` 互換入口の存廃ではなく、実体モジュールそのものを変更・検証したいとき。

## hash
- 0546b07587dfb4189aba0072416e559620856925b9234f872060bf4691cb6a8f

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行基盤、Codex exec/TUI、設定・状態・Git・パス・ログ・エラー・feedback、INDEX lifecycle など、複数機能から共有される実装への入口。

## Read this when
- cmoc の共通 runtime helper の責務や公開入口を確認するとき
- CLI、Codex、設定、状態、Git、feedback、INDEX 更新など複数の runtime 機能を横断して依存関係を調査するとき
- commons 配下の個別実装を変更する前に、対象となる共通機能の入口を選ぶとき

## Do not read this when
- 特定の runtime helper のアルゴリズムや詳細仕様だけを調査するときは、対応する個別モジュールを直接読む
- 特定サブコマンドの引数定義や固有ビジネスロジックだけを確認するとき
- 正本仕様や利用者向け挙動を確認することが目的の場合は、対応する oracle 文書を直接読む

## hash
- c708a91f49f3bf2a42be2939378ecd37ea3dbcc7da62b29a12a2ed37328a6d63

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
- Typer で構成された cmoc の CLI ルートエントリ。トップレベル command と session/oracle/realization/run/feedback のサブコマンドを登録し、引数解析エラーを cmoc 形式へ変換して各実装へ委譲する。CLI の公開入口とサブコマンド構成を確認するための起点。

## Read this when
- トップレベル command、サブコマンドの登録、CLI option、終了コード、引数解析エラー、補完処理を変更または調査するとき。
- cmoc の console script 起動経路や CLI 全体の command tree を確認するとき。

## Do not read this when
- 特定サブコマンドの業務ロジックや実行処理を調査するときは、各サブコマンド実装を直接読む。
- oracle の仕様、テスト内容、エラー描画の詳細だけを確認する場合。

## hash
- 7726923dd657d38c034f473eb30b402793bb9849767e56eb218d4d4ddedaa8fa

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
- CLI サブコマンドの realization 実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui など各サブコマンドの実行入口・処理フローへの入口を提供する。apply と review は現在実装本文がなく、追加後の参照先となる。

## Read this when
- CLI サブコマンドの構成や、対象サブコマンドの実行入口を確認・変更するとき。
- feedback、oracle、realization、run、session などのサブコマンドにおける実行フロー、状態管理、report、cleanup、commit・merge 処理への入口を調査するとき。
- doctor、indexing、tui の起動条件や preflight、入力処理、INDEX 更新・commit、Codex TUI 起動の連携を確認するとき。
- apply または review の realization 実装を追加する場所や、追加後の入口を確認するとき。

## Do not read this when
- 特定サブコマンドの内部処理、共通 helper、prompt、runtime、Git 処理、または正本仕様の詳細だけを調べるときは、該当する下位実装・共通実装・oracle 文書を直接読む。
- 対象サブコマンド以外の CLI 実行フローを調査するとき。

## hash
- be15c374eae6ecdfc82f0016ee4b2d8f5b3e983b3c26d172bbc4c4bc928c0828
