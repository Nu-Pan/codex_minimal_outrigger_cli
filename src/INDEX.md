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
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 実行、Codex 呼び出し、設定・状態管理、Git/worktree 操作、パス・ログ・エラー、feedback、INDEX 更新、editing run lifecycle など、複数機能から再利用される実装への入口。
- 個別 runtime module の実装だけでなく、共通 API、結果型、状態型、パッケージ全体の責務分担を横断して確認するためのディレクトリ。

## Read this when
- 複数の cmoc runtime 機能にまたがる共通処理や公開 API の配置を確認するとき
- CLI、Codex、Git、設定、状態、feedback、INDEX、editing run の共通実装を変更・調査するとき
- 対象となる個別 helper や lifecycle module を特定するために commons 配下の構成を確認するとき

## Do not read this when
- 特定の helper、サブコマンド、仕様、またはデータ形式の詳細だけを調査するときは、対応する個別実装や oracle 文書を直接読む
- 共通 runtime を利用する上位 CLI の利用者向け挙動だけを確認するとき
- commons 配下に対象となる個別実装が明確にある場合に、ディレクトリ全体を読む必要があるとき

## hash
- 6ed9ce9ea39ee9e09c591dce6bc76180b017a5bdbaaa1bbe320b1a13ac842d45

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
- Typer と Click を用いた cmoc CLI の最上位入口。共通の CLI アプリケーション、サブコマンド階層、コマンド引数、補完処理、引数解析エラー変換を定義し、各サブコマンド実装へ処理を委譲する。

## Read this when
- cmoc の CLI 全体のコマンド構成やトップレベル入口を確認・変更するとき
- Typer/Click の引数解析、補完、CLI 例外の cmoc 形式への変換、または互換処理を確認・変更するとき
- doctor、tui、indexing、session、oracle、realization、run、feedback の CLI コマンド登録を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や業務ロジックを確認したいときは、対応する sub_commands 配下の実装を直接読む
- oracle やエラーハンドリングの仕様を確認したいときは、対応する正本仕様を直接読む

## hash
- 266ba84d0a7501d380ff52d891fbb81985a6e3e0817f8677aabe88142f8dbef1

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
- サブコマンド実装を集約するディレクトリ。doctor、feedback、indexing、oracle、realization、review、run、session、tui の各実装領域へ進むための入口であり、apply は現時点で実装がない。

## Read this when
- サブコマンド実装の構成や、対象のサブコマンドに対応する実装領域を特定するとき。
- 特定のサブコマンドの実行入口やライフサイクル処理を調査・変更するとき。
- oracle や realization など、配下に複数の実装領域を持つサブコマンド群の入口を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細処理を確認する場合は、このディレクトリではなく該当する実装ファイルや下位パッケージを直接読む。
- CLI ランタイム、共通 state/store、agent prompt、Structured Output schema、正本仕様の内容だけを確認したいとき。
- apply サブコマンドを扱うが、実装が追加されていない状態のとき。

## hash
- 45b673cb90fe1db4dd0cf83a07956de76c3dd1192eed75e35705eabe5a15693d
