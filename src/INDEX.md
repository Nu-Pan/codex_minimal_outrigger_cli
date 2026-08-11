# `acp`

## Summary
- ACP互換の公開入口と、`acp.builder` 配下の互換・委譲層を扱う。既存の`acp` import経路の存廃、canonical実装への接続、builder adapter群への入口を確認するための階層。

## Read this when
- `acp`公開名を維持・削除する判断や、`oracle`側の実体への移行導線を確認するとき。
- ACP builderのadapter構成、互換import経路、canonical実装への委譲先を調査するとき。

## Do not read this when
- 具体的なACP実装や`acp.builder`配下の個別builderの処理内容を確認・変更するときは、対応する実体モジュールまたは下位対象を直接読む。
- ACPやbuilderと無関係なCLI、公開API、利用箇所を調査するときは、それぞれの対象を直接読む。

## hash
- 249b7858f7985680d719613ddacaa06b29d615d32551ee4b5c40fce604a8534c

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
- cmoc の各機能から共有される runtime helper をまとめる commons パッケージ。CLI 実行、Codex 呼び出し、設定・状態・Git・パス・ログ・feedback・run lifecycle など、複数の runtime 機能にまたがる共通処理を確認する際の入口。配下の個別モジュールへ進むためのディレクトリ単位のルーティング対象。

## Read this when
- 複数の runtime 機能に共通する helper や公開 API の配置を確認するとき
- commons 配下のどの runtime モジュールを読むべきか判断するとき
- CLI、Codex、設定、状態、Git、ログ、feedback、run lifecycle などを横断して共通処理の依存関係を調査するとき

## Do not read this when
- 特定の runtime helper のアルゴリズムや入出力契約を確認したい場合は、対応する commons 配下の個別モジュールを直接読むとき
- 利用者向けコマンドの業務ロジックだけを調査する場合
- 正本仕様や個別機能の詳細な挙動を確認する場合は、対応する oracle 文書または専用実装へ直接進むとき

## hash
- 71357f295cf1ed7617d11b27663a36a0f87443ea04c6b16eb92ae7f48aa5fe8e

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
- CLI 全体の Typer アプリケーションを構成し、各トップレベルおよびサブコマンドを公開する実行入口。引数解析エラーを cmoc 形式へ変換し、処理本体は対応するサブコマンド実装へ委譲する。CLI 構成、引数解析、補完、起動経路を確認するときの入口となる。

## Read this when
- CLI のコマンド登録やサブコマンド階層を確認・変更するとき
- Typer/Click の引数解析エラー、補完、終了処理を確認するとき
- console script から CLI が起動される経路を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容を調査・変更するときは、対応する sub_commands 配下を直接読む
- エラー表現や自動補完の正本仕様を確認するときは、参照されている oracle 文書を読む

## hash
- 9b8448815b84ea98040776fdaccc0058c63c9a1828c6ebbbb2c8a13c61b38d09

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
- cmoc の各サブコマンド実装をまとめる領域。doctor、feedback、indexing、oracle、realization、run、session、tui などの CLI 入口と、関連する下位実装へのルーティングを担う。
- サブコマンドごとの実行フローや状態管理、レビュー・編集・レポート生成などの詳細を確認する際の起点となる。apply と realization review は現在具体的な実装を持たない。

## Read this when
- サブコマンドの実装構成や、目的の CLI 実行入口を特定するとき。
- 複数のサブコマンドにまたがる実装領域の責務分担や、下位要素への入口を確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui の実装を調査・変更するとき。

## Do not read this when
- 特定サブコマンドの詳細な処理、共通 runtime、builder、store、schema、正本仕様を直接確認する場合。
- apply または realization review の具体的な実装内容を確認する場合。
- 対象サブコマンド以外の処理だけを調査する場合。

## hash
- 1ede40fe72dd82908678304ee07d5ccfbd06b92fdb3a89132a177901a35f0f3b
