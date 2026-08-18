# `acp`

## Summary
- `src/acp` は ACP 互換の公開入口と builder adapter 群を扱う。`acp.*` 参照の互換性、canonical な oracle 実装への委譲、共通プロンプト整形、feedback・indexing・oracle・realization・session・TUI などの処理別 adapter への入口として機能する。

## Read this when
- `acp` 公開名の存廃や既存利用者向け参照から `oracle` 側の実体へ切り替える導線を確認したいとき
- `acp.builder` の互換接続、共通プロンプト整形、feedback issue の正規化・検証、または処理別 builder adapter の入口を探すとき
- builder adapter の対象領域を特定し、下位対象へ進む入口が必要なとき

## Do not read this when
- `acp` 配下の具体的な実装詳細や移行先の詳細だけを知りたいときは、対応する実体モジュールを直接読む
- canonical な oracle 実装、正本仕様、通常の利用側ロジックを調査・変更するときは、対応する正本実装や参照元を直接読む
- ACP builder と無関係な CLI 処理や実装を調査するとき

## hash
- ae65897090c293e1c2b592328bda33127b088818977bd7d0f8348ed9ca0f626d

# `basic`

## Summary
- `basic.*` の旧来の公開 import 経路を維持する互換層。ACP 型、path model、構造化文書 API を realization 側から再公開し、実装や正本仕様そのものは保持しない。各モジュールの互換インターフェース確認から、対応する正本実装・仕様へ進む入口となる。

## Read this when
- `basic.*` の互換 import を維持・削除・移行する条件を判断するとき
- realization 側の ACP 型、path model、構造化文書 API の公開経路を確認するとき
- 旧 API から canonical な実装・型・仕様への参照関係を調査するとき

## Do not read this when
- ACP 型、path model、構造化文書の正本仕様や実装詳細を確認したいときは、対応する oracle 側または canonical 側を直接読む
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の個別 API や再公開内容だけを確認したいときは、該当モジュールを直接読む
- `basic.*` の互換公開面や参照経路に関係しない処理を調査・変更するとき

## hash
- 64892c955750ada2d0b8daa7c36300b7de9145ab6117ea7e5befdbcd93ec574c

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
- `src/commons` は、cmoc の CLI・Codex 実行・設定・Git・状態・ログ・feedback・レポートなど複数の実行経路から共有される runtime helper 群を集約するパッケージである。共通 runtime API や個別 helper の責務を確認・変更するときの入口として、まずこのディレクトリから対象モジュールへ進む。

## Read this when
- 複数の CLI または Codex 実行経路にまたがる共通 runtime 処理の担当モジュールを探すとき
- 設定、パス、Git、プロセス、状態、ログ、feedback、レポート、indexing などの共通 helper を確認・変更するとき
- commons 配下の実装を利用・変更する前に、該当する個別 runtime module の入口を特定するとき

## Do not read this when
- 特定の runtime helper の内部実装だけを確認する場合は、対応する commons 配下の個別モジュールを直接読む
- CLI サブコマンド固有の業務ロジック、Codex の個別実行仕様、または oracle の正本仕様だけを確認する場合
- commons 配下に対象となる共通 helper がない機能を調べる場合

## hash
- 6d98c069176743f3db2bb4515fe5eed5784f5cba5497d9934a0d5630f2422979

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
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui などの個別サブコマンド入口と、その配下の処理へ進むための上位ルーティング対象。

## Read this when
- CLI サブコマンド全体の実装構成や、特定サブコマンドの実装入口を確認するとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui のいずれかを調査・変更するとき。

## Do not read this when
- CLI サブコマンドに関係しない処理を確認するとき。
- 個別サブコマンドの詳細な処理、共通 runtime、正本仕様、prompt 契約を直接確認したいときは、対応する下位実装または仕様文書へ進む。

## hash
- c172450b955a9cf087e89fdb20689d5f180bd071cec47aa04f870ceee3008867
