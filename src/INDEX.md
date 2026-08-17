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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行境界、Codex exec/TUI、設定・ログ・パス・Git worktree、状態管理、feedback、report、INDEX 更新など、複数の実行経路から共有される機能の実装入口を提供する。
- 共通 runtime API の公開入口を確認する場合は `cmoc_runtime.py`、Codex 実行や preflight は対応する `runtime_codex*`、設定・Git・状態・feedback などは各専用 `runtime_*.py` へ進む構成になっている。

## Read this when
- cmoc の複数機能で共有される runtime helper の配置や公開入口を確認するとき
- CLI、Codex、設定、ログ、Git worktree、状態、feedback、report、INDEX 更新などの共通実行基盤を調査・変更するとき
- 特定の共通機能の実装へ進む前に、commons 配下の担当モジュールを選ぶとき

## Do not read this when
- 特定の runtime helper の内部挙動だけを確認したいときは、対応する `runtime_*.py` を直接読む
- 個別 CLI サブコマンド、Codex preflight、report、feedback などの固有仕様だけを調査するときは、その機能の専用実装または正本仕様を直接読む
- commons と無関係なアプリケーション固有処理や利用者向け仕様だけを確認するとき

## hash
- 58c03d494243c8cec674c0f299eb26f09d3f10b30ea9a1056f37056fed762724

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
- 日本語のルーティング文書を生成するため、対象ディレクトリの各サブコマンド入口の責務と読む条件を、提示された本文だけを根拠に整理します。

## Read this when
- src/sub_commands 配下のサブコマンド実装の構成や入口を俯瞰したいとき。
- apply、doctor、feedback、indexing、oracle、realization、review、run、session、tui のいずれかについて、まず適切な上位入口へルーティングしたいとき。
- サブコマンドの実行フロー、固有処理、または配下の実装・仕様への進み方を確認したいとき。

## Do not read this when
- 特定サブコマンドの詳細実装、正本仕様、共通ランタイム、prompt 契約、Structured Output schema を直接確認するだけで、上位ディレクトリの構成把握が不要なとき。
- サブコマンド以外の実装や、提示された配下エントリーの責務に該当しない処理を調査するとき。

## hash
- d9132e69da50fb09ec7498a2644d928365cd4f3774678abf20004235ac93321a
