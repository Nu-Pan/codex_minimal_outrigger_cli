# `acp`

## Summary
- `__init__.py`: `oracle.acp_builder` を既存の `acp.*` 互換 import 面として公開し続ける初期化入口。実体は正本側に置かれ、この対象は移行期間中の公開 import 面を保つ役割に限る。
- `builder`: `acp.builder` 配下の ACP parameter builder 群を束ねる互換ルーティング層。個別 builder へ進む前に、`apply`、`indexing`、`review`、`session`、`tui`、`quota_probe.py` のどこを読むべきかを切り分ける。

## Read this when
- `__init__.py` は、`acp.*` 参照を `oracle.*` または実体 module へ移す作業で、互換入口を残す理由や削除条件を確認したいときに読む。
- `__init__.py` は、realization 側または利用者向け公開面に残る `acp.*` import の扱いを判断したいときに読む。
- `builder` は、`acp.builder` 配下でどのサブ領域に進むべきかを判断したいときに読む。
- `builder` は、旧来の import 互換を残す入口と、正本実装への委譲先を見分けたいときに読む。
- `builder` は、ACP parameter builder 群のうち、共通部品と個別 builder の境界を確認したいときに読む。

## Do not read this when
- `__init__.py` は、acp builder の実装内容や生成処理そのものを調べたいときには読まない。
- `__init__.py` は、新しい acp 機能や API 仕様を追加する場所を探しているときには読まない。
- `builder` は、個別 builder の生成ロジックや仕様本体を知りたいときには読まない。
- `builder` は、`oracle` 側の正本仕様断片そのものを確認したいときには読まない。
- `builder` は、単に別の公開名前空間や上位 CLI の振る舞いを調べたいときには読まない。

## hash
- 806ab6f1f488b9b610653202a2f686350fce8f53d7bdeb4cf584144a9180684e

# `basic`

## Summary
- oracle src 側の基本 API を realization 側の既存公開面から再公開する互換層。ACP 型、path model、構造化文書 API などを複製せず、正本側定義への参照として維持する入口をまとめる。
- 既存の `basic.*` import 経路を残すための領域であり、削除可否は realization 側と利用者向け公開面から対応する互換参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- realization 側で `basic.*` 経由の公開 import 経路や互換維持を確認したいとき。
- oracle src 側の正本定義を複製せず、既存参照へ再公開している箇所を探したいとき。
- ACP 型、path model、構造化文書 API の互換再公開を残す理由、公開名、削除条件を確認したいとき。

## Do not read this when
- ACP 型、path placeholder、構造化文書処理そのものの仕様や実装詳細を確認したいとき。その場合は再公開先の正本側実装を読む。
- `basic.*` 互換参照や公開 import 経路ではなく、一般的な CLI 挙動、テスト挙動、path 変換仕様の検討をしているとき。
- 新しい基本 API や公開面を追加する実装場所を探しているとき。

## hash
- ad0cfb03fb2c682437a55ec2ac464197bd2fc5eb3bb3da22e79f7473d62523e7

# `cmoc_runtime.py`

## Summary
- runtime 実装を別モジュールへ委譲し、既存の import 経路を一時的に維持する互換 shim。公開名と実体の移行期間にだけ意味を持つ。

## Read this when
- runtime module の import 経路、公開 module 名、または互換 alias の残存理由を確認したいとき。
- 呼び出し元を移行した後に、この互換 shim を削除できるか判断するとき。

## Do not read this when
- runtime の具体的な処理内容や責務分割を調べたいとき。この対象は実装本体ではなく委譲だけを扱う。
- 新しい runtime 挙動を追加・変更したいとき。実体側の runtime 実装を読む方が直接的。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- `commons` 配下の実行時共通基盤を束ねる入口。共有 runtime helper 群のパッケージ境界だけを示し、個別 helper の責務は下位要素で確認する。

## Read this when
- cmoc の実行時処理で、複数モジュールから使う共通 helper の配置場所や入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime helper 用のまとまりであることを確認したいとき。

## Do not read this when
- 特定の helper の実装、入出力、失敗時挙動を確認したいとき。この対象ではなく、該当する下位要素の本文を読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共有 runtime helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 6fab388321f2f0adb20f2bb851d97b0cf92e63d89eae13e1f885deaf769640fb

# `config`

## Summary
- oracle src 側の設定実装を正本に保ちながら、realization 側に残る旧来の `config.*` import を受け止める互換入口をまとめるディレクトリ。
- 設定定義や設定ロジック本体は持たず、正本側の定義を複製せず再公開する境界を確認する入口になる。

## Read this when
- 旧来の `config.*` import が realization 側でどこに受け止められているか確認したいとき。
- 正本側の設定実装を複製せず参照・再公開する互換方針に関わる変更を行うとき。
- 既存の公開参照や互換 import を削除・置換できる条件を判断したいとき。

## Do not read this when
- 設定値の定義、意味、読み込み、検証などの本体挙動を確認したいとき。
- oracle src 側の正本となる設定実装そのものを確認したいとき。
- 互換 import の維持や再公開経路に関係しない設定項目追加・実装変更を行うとき。

## hash
- 97eb1bfd8f73945ab835c22962809b5a59009f2d7e1581a56e7058b6c8c786a4

# `main.py`

## Summary
- Typer ベースの cmoc CLI 入口を定義し、root command と session/apply/review 配下の subcommand を各実装関数へ接続する。
- CLI 引数解析エラーを cmoc のエラーレポート形式に変換する group、補完時の例外処理回避、console script からの起動責務を持つ。
- scope option の公開値や alias command など、利用者が直接触れる command 面の薄い配線を扱う。

## Read this when
- CLI command、subcommand、option、alias、console script 起動の追加・変更・削除を確認したいとき。
- Typer/Click の引数解析エラーが cmoc 形式で表示される経路、または shell completion 時の挙動を確認したいとき。
- CLI 入口からどの sub command 実装へ委譲されるか、scope option が実装へどう渡るかを確認したいとき。

## Do not read this when
- 各 command の実処理、git 操作、worktree 操作、review/apply/session の制御内容を知りたいだけなら、対応する sub command 実装を直接読む。
- cmoc 共通 error 型や error 表示本文の構造を変更したいだけなら、runtime 側の定義を読む。
- oracle や INDEX 更新の仕様本文を確認したいだけなら、仕様文書または該当実装へ進む。

## hash
- e8d8163fd3e7c5f366a20e21707b54b8ee05450bce0e135bf7b3b5493681c4e6

# `oracle.py`

## Summary
- `src` だけを import 対象にした起動時にも、正本側の `oracle` package を解決できるようにする package shim。packaged realization tree の外にある oracle source directory を `__path__` に設定し、見つからない場合は import 失敗として明示する。

## Read this when
- `src` 起点の実行環境で `oracle.*` import を成立させる仕組みを確認したいとき。
- realization code から正本側 oracle module を参照する import 経路や package shim の挙動を調べるとき。
- `oracle package source was not found` という import error の原因を確認するとき。

## Do not read this when
- oracle source の個別 module の仕様や実装内容を確認したいときは、正本側の該当 module を直接読む。
- CLI command、状態管理、入出力処理など cmoc 本体の realization implementation を調べたいときは、それぞれの担当 module を読む。
- oracle file と realization file の定義やパス概念そのものを確認したいときは、対応する正本仕様文書を読む。

## hash
- b6f4097cc1550a057bef77dda6b9e5434b394da2d2831fb96ccbf3d319c4222d

# `sub_commands`

## Summary
- `cmoc` の各サブコマンド実行本体を集めた入口階層。`apply`・`review`・`session`・`tui`・`indexing`・`doctor`・`eval_oracle` のような個別コマンドの実行フローと、その間で共通利用される補助処理への進み先を選ぶために読む。
- ここは CLI 全体の登録や共通ランタイムの説明ではなく、各サブコマンドの責務分担と、どのモジュールがその実行入口かを見分けるための案内として使う。

## Read this when
- どの `cmoc` サブコマンドがどの実装モジュールに対応するかを切り分けたいとき。
- `apply`・`review`・`session`・`tui`・`indexing`・`doctor`・`eval_oracle` の実行フローや責務境界を追い始めたいとき。
- 個別サブコマンドの入口を起点に、そこから先の専用実装へ進む前のルートを確認したいとき。

## Do not read this when
- 共通の CLI runtime、git 操作、session/state、path 変換などの基盤だけを見たいときは、より下位の共通実装へ直接進む。
- 対象サブコマンドがすでに分かっていて、その個別入口や内部実装へ直接進めるとき。
- サブコマンド以外のトップレベル設定や正本仕様そのものを確認したいとき。

## hash
- 65f6b04b668e54888bba2341c90c55757f6a21bdc06f80a774c9e6f98b9fbce3
