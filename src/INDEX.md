# `acp`

## Summary
- ACP 互換の公開入口を担い、既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する際の判断材料を提供する。互換入口の存廃を検討する場合の入口であり、具体的な実装や移行先の詳細は対応する実体モジュールを直接読む。
- ACP builder の互換入口と adapter をまとめ、canonical な oracle builder への接続を維持する。quota probe、session、TUI、realization、review、feedback、および動的 Markdown section の code fence 保護に関する下位実装へ進む必要がある場合に読む。canonical 実装の仕様や個別 builder の具体的な処理を確認する場合は、対応する oracle 側または下位実装を直接読む。

## Read this when
- `acp` という公開名の存続・削除や、既存参照を壊さず oracle 側の実体へ切り替える導線を判断するとき。
- ACP builder の互換 import 経路、oracle 実装への委譲、adapter 構成を調査・変更するとき。
- quota probe、session join、TUI 起動、realization apply/refactor、review finding、feedback issue、または動的 prompt section の code fence 保護に関係する builder の入口を探すとき。

## Do not read this when
- 互換入口ではなく `acp.*` の具体的な内部挙動を変更したいときは、該当する実体モジュールを直接読む。
- canonical な oracle builder の仕様・prompt 内容・本体ロジックを確認したいときは、対応する oracle 側の対象を直接読む。
- 個別 builder の具体的な処理や利用箇所を調査したいときは、該当する下位実装または参照元を直接読む。
- INDEX エントリーの routing 規則や生成内容だけを確認したいときは、builder 実装へ進まない。

## hash
- 17bf164f4503c60243123704d3d04ea58f664e5a68193b815e206ad98d470ab2

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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行 lifecycle、Codex 呼び出し、設定・状態・Git・パス・ログ、INDEX 更新、feedback、editing run など、複数の runtime 機能から共有される実装と公開 API を扱う。個別 helper や runtime lifecycle の実装を調査・変更するときの入口となる。

## Read this when
- 複数の runtime 機能にまたがる共通 helper、公開 API、状態型、エラー型、結果型の配置を確認するとき
- Codex 実行、INDEX 更新、設定・状態管理、Git、ログ、feedback、editing run などの共通 runtime 境界を調査するとき
- commons 配下の個別実装へ進む前に、対象機能を担うモジュールの入口を絞り込むとき

## Do not read this when
- 特定の runtime helper のアルゴリズムや個別サブコマンドの挙動だけを確認したいときは、対応する下位モジュールを直接読む
- 利用者向けの正本仕様や設計根拠だけを確認したいときは、対応する oracle 文書を直接読む
- commons と無関係な CLI 固有処理やアプリケーション仕様を調査するとき

## hash
- bef348ee46466fc5f79b9d0a0d10af2f3e7ea24a98ac0c87950fe72b660a6e9d

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
- CLI サブコマンド実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの各コマンド入口と関連処理へ進むためのルーティング起点で、apply と review は現在実装がない。
- サブコマンド全体の構成や、個別コマンドの実行入口・責務分担を確認したうえで、必要な下位実装へ進むために使用する。

## Read this when
- CLI サブコマンドの構成、実装入口、またはコマンド間の責務分担を確認するとき。
- 特定のサブコマンドの実行フローや関連する下位処理の調査・変更対象を特定するとき。

## Do not read this when
- 特定サブコマンドの詳細実装、共通 runtime、正本仕様、または下位 helper の内容だけを確認する場合は、対応する下位実装や仕様を直接読む。
- apply または review の具体的な処理を確認する場合。現在これらのディレクトリには実装がない。

## hash
- 96c7e67177a6fb1c002c5644d2ddb940df3adae286ea71186da11c433cbfb132
