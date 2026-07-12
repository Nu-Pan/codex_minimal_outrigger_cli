# `acp`

## Summary
- `acp` 系の互換 import 入口と、`acp.builder` 配下の転送層をまとめて見るための案内。旧公開名を維持するだけの薄い層と、正本側実装へつなぐ入口を切り分けて辿るときに使う。
- 配下の各領域は、互換維持か正本側への接続かを判断したいときに読む。`common` は共通ビルダー処理の置き場だが、現時点では本文がないため、この案内から実体は読めない。
- `quota_probe` は quota 回復確認のための最小呼び出しを確認したいときに読む。機能追加や本体仕様の調査ではなく、旧 import path の扱いと接続境界の確認に向いている。

## Read this when
- `acp.builder.*` の旧 import 互換を残すか削るかを判断したいとき。
- 正本側の builder を旧公開名からどう辿るか、またどの互換入口が残っているかを確認したいとき。
- 各サブ領域の互換 wrapper と、正本側実装への接続境界を確認したいとき。
- quota 回復確認のための最小呼び出し内容を確認したいとき。

## Do not read this when
- 正本側の具体的な実装内容や仕様本体を確認したいとき。
- 互換入口ではなく個別機能の中身を確認したいとき。
- `common` の実装詳細を探しているとき。
- `acp.builder` 以外の公開面や、互換以外の新規 API を探しているとき。

## hash
- eb41ce1e871c19639fa976bd0c383f502b49f242ff49174f47120acac27e11cc

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
- `commons` 配下の共通補助群への入口で、複数の runtime 系モジュールから共有される補助機能をまとめて参照するためのパッケージ境界を示す。
- 個別 helper の責務や挙動はここでは定義せず、必要に応じて下位要素の本文へ進むための起点として使う。

## Read this when
- cmoc の実行時処理で、複数モジュールから使う共通 helper の配置場所や入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime helper 用のまとまりであることを確認したいとき。

## Do not read this when
- 特定の helper の実装、入出力、失敗時挙動を確認したいとき。この対象ではなく、該当する下位要素の本文を読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共有 runtime helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 386f2ea624105737cd155bc92af5a8b8ee775efd9608289e31b294d92ce21e02

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
- `sub_commands` 配下の CLI サブコマンド実装を束ねるルーティング層。個別コマンド本体に入る前に、この階層でどのサブコマンド群を扱うかを見分けるための入口になる。
- この階層では `apply`、`review`、`session` などのサブコマンド実装がまとまっており、各コマンドの実行入口や上位からの振り分けを追うときに読む。

## Read this when
- CLI のサブコマンド構成や、この階層にどのコマンド実装が集まっているかを確認したいとき。
- 個別サブコマンドの実行入口を探し、そこから先の実装へ進む前に責務の境界を把握したいとき。
- サブコマンドの追加・移動・整理を行うために、どの実装がこの階層に属するかを確認したいとき。

## Do not read this when
- 個別サブコマンドの処理本体、状態遷移、report 生成、worktree 操作などの詳細を知りたいときは、該当サブコマンド側を読む。
- CLI 全体の起動処理や共通 runtime、設定ロード、共通 helper の挙動を調べたいときは、この階層ではなく共通基盤側を読む。
- oracle file や realization file の定義、INDEX.md 生成規則そのものを確認したいときは、この階層ではなく正本仕様側を読む。

## hash
- 46021410c97a2b1124b17892e1c53d90d6ca030a166b1b81c2e88a6e894e5026
