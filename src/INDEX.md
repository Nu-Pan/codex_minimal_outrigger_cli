# `acp`

## Summary
- `acp` 互換入口と `acp.builder` 配下の互換入口群を扱う。旧来の import 経路を維持しつつ、`oracle` 側の正本実装や各機能の実体へ到達するための境界を提供する。

## Read this when
- `acp` または `acp.builder` の公開名・互換 import 経路・委譲先を確認したいとき。
- 互換入口の維持、整理、削除可否を判断するとき。
- apply、indexing、review、session、TUI、quota probe などの入口から対応する実体へ進みたいとき。

## Do not read this when
- 特定機能の正本仕様や本体実装だけを確認したいときは、対応する `oracle.acp_builder` 側または委譲先の実体を直接読む。
- `acp.*` の内部挙動そのものを変更したいときは、対象の実体モジュールを直接読む。

## hash
- 42d30cc28f71c611205d0e05abb41a5cf21bca2db9041834b4f593295855d276

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
- cmoc の実行時に共有される runtime helper 群をまとめる領域。CLI 実行、Codex 起動、設定、Git、パス、ログ、状態管理などの共通機能と、それらを束ねる公開窓口を扱う。個別機能の実装・挙動を確認する際は、対応する下位モジュールが入口になる。

## Read this when
- 複数モジュールから利用される cmoc runtime helper の配置や責務を確認したいとき。
- CLI 実行基盤、Codex 実行、設定、Git、パス、ログ、状態管理などの共通処理を変更・調査するとき。
- 共有 runtime API の再公開構成や、下位モジュールへの入口を確認したいとき。

## Do not read this when
- 特定の helper の詳細な入出力、失敗時挙動、内部処理を確認したいときは、該当する下位モジュールを直接読む。
- 特定 CLI サブコマンドの業務処理や、oracle に定義された仕様そのものを確認したいときは、より直接の実装・仕様対象へ進む。

## hash
- f4f8747383201491de5695a622f924fee199130a582b6797c68b13aadef09587

# `config`

## Summary
- `config.*` 参照を既存利用者向けに維持するための互換入口群。ここでは設定の実体を持たず、正本の oracle src を再公開する経路だけを確認する。
- `config.cmoc_config` から Cmoc 設定型を再公開する入口。設定定義そのものではなく、既存の公開参照を壊さないための接続点として読む。

## Read this when
- `config` からの import 経路を維持・確認したいとき。
- `config.cmoc_config` 経由で Cmoc 系の設定型を参照したいとき。
- 設定の正本を変更せず、互換入口の有無だけを確認したいとき。

## Do not read this when
- 設定仕様そのものを確認したいときは、正本側の oracle src を読む。
- `config.*` 以外の公開面や新規設定追加を扱いたいとき。
- 設定定義の項目意味や保存仕様を調べたいとき。

## hash
- c121a67917bdcc7850097d1a5fc153afb19f375da55ada79794c9c5739b22514

# `main.py`

## Summary
- Typer/Click による cmoc CLI の最上位エントリー。doctor、tui、indexing、eval-oracle と session/apply/review 配下の各サブコマンドを登録し、対応する実装へ委譲する。CLI 引数解析エラーの cmoc 形式への変換と scope option の定義も扱う。サブコマンドの具体的な処理を調べる際の入口。

## Read this when
- cmoc のトップレベルコマンド、サブコマンド名、option、scope の既定値や選択肢を確認するとき
- CLI 引数解析エラーの表示・終了処理を変更または調査するとき
- 新しいサブコマンドの登録先や console script の起動経路を確認するとき

## Do not read this when
- 特定サブコマンドの業務処理や分岐を調査するときは、対応する sub_commands 配下の実装を直接読む
- oracle の詳細仕様や利用手順を確認するときは、コメントに示された oracle 文書を直接読む
- CLI とは無関係な内部処理や共通ランタイムの実装を調査するとき

## hash
- 69fb1bf5b1b12340db48a63f99de040ba4942cc13103ba131f4d2123f8f1cdb0

# `oracle.py`

## Summary
- `src` から `oracle.*` を import したときに、正本側の実装群へ解決させるための境界を見る入口。`oracle` 名前空間の参照先を切り替える仕組みだけを扱い、個別の oracle 実装内容を追う前段として読む。

## Read this when
- `src` 経由の import で正本側 `oracle.*` が見つからない、または参照先の切り替え方法を確認したいとき。
- `oracle` 名前空間を packaged realization ではなく正本ソースへ向ける必要があるかを判断したいとき。

## Do not read this when
- `oracle.*` 配下の個別機能や実装内容を知りたいときは、ここではなく正本側の該当モジュールを読む。
- 通常のアプリ機能や CLI の挙動を追いたいだけなら、この import 解決の仕組みは読まなくてよい。

## hash
- 7ef36bb425d49e4907bce740821b18302da678a21b33bf887d9fd94c111929a5

# `sub_commands`

## Summary
- `cmoc` のサブコマンド実装を収めるディレクトリ。apply、doctor、eval_oracle、indexing、review、session、tui などの CLI 入口と、review の対象選定・ループ・パス処理・レポート生成・INDEX 統合を扱う下位要素への入口となる。

## Read this when
- サブコマンドの構成や、特定の CLI サブコマンドの実行入口を調査・変更するとき。
- apply、review、session、tui などのサブコマンド固有のライフサイクルや処理範囲を確認するとき。
- review oracle の対象列挙、評価ループ、パス解決、レポート生成、INDEX 統合の担当モジュールを探すとき。

## Do not read this when
- 共通 runtime、Git 操作、session state、process lock など、サブコマンド固有でない実装だけを調査するとき。
- 特定サブコマンドの詳細が明らかな場合は、このディレクトリ全体ではなく対応する下位実装を直接読むとき。
- oracle 内容、対象ファイル単位の review/fix パラメータ、finding schema など、別の担当領域だけを確認したいとき。

## hash
- 7f5b4b7c72a383dc55037a82a9f313d4ae3f205a70da24e52bd8c4518c1aa9dd
