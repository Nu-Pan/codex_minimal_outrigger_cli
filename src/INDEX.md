# `acp`

## Summary
- ACP 互換の realization package。`acp.*` の公開 import 経路を維持しつつ、下位の builder adapter などを通じて canonical な oracle 側実装へ接続する。
- `acp` 公開入口の存廃判断と、builder 用途別の下位要素へ進むための起点となる。

## Read this when
- `acp.*` の互換 import 経路や公開入口全体を確認したいとき。
- ACP builder の用途別 adapter へ進む入口を選びたいとき。

## Do not read this when
- `acp` 公開入口の存廃だけを判断したいなら、入口モジュールを直接読む。
- 特定の builder の実装・canonical 仕様・利用箇所を調べたいなら、該当する下位要素または参照元を直接読む。

## hash
- 19748d31bd6289625fef47d1a672db39bd72ee4039df05de799d7d7caeb3ec5a

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。パッケージ初期化、CLI 実行基盤、Codex 実行、設定・状態・Git・パス・ログ、INDEX 更新、feedback、run lifecycle など、複数機能から共有される実装の入口。
- 個別 runtime 機能の実装だけでなく、Codex 呼び出しや editing run、設定、feedback、doctor など横断的な共通処理を調査・変更する際に、配下の対応モジュールへ進むためのディレクトリ。

## Read this when
- 複数の CLI または runtime 機能にまたがる共通処理の実装箇所を特定するとき
- Codex 実行、INDEX 更新、設定・状態・Git・パス・ログ、feedback、editing run の共通基盤を調査・変更するとき
- commons パッケージの公開入口や、対象機能に対応する個別 runtime module へのルーティングを確認するとき

## Do not read this when
- 特定の runtime helper の具体的なアルゴリズムや仕様だけを確認したいときは、対応する個別モジュールへ直接進む場合
- 特定 CLI サブコマンドの個別処理や利用者向け仕様だけを調査するとき
- 正本仕様や個別機能のデータ形式を確認することが目的で、共通実装の配置確認が不要なとき

## hash
- 1a72c36bf5532260563d3f60e0a5b5578a751934d6aad4d646c25f3c3f9f29cf

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
