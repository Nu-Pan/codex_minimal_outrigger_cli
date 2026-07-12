# `acp`

## Summary
- `acp` 配下の公開入口を束ねる上位ディレクトリ。個別の実装へ進む前に、互換入口と下位パッケージへのルーティングを確認するための場所として読む。
- 互換 import 面の維持方針や、`acp.*` 参照を実体 module へ移す判断を確認したいときに読む。実処理の詳細や新機能の追加先を探す用途には向かない。

## Read this when
- `acp.*` の公開面をどの下位実装へ進めるか判断したいとき。
- 互換入口を残す理由や削除条件を確認したいとき。
- 上位の公開面と下位の個別実装の境界を見たいとき。

## Do not read this when
- 個別の builder 実装、変換処理、実行ロジックを知りたいとき。
- 新しい `acp` 機能や API 仕様の追加先を探しているとき。
- 互換入口の有無だけを確認済みで、詳細が不要なとき。

## hash
- 8e127ad9b7631b93da147e4098f3804ab51044025d7614f9ede0642dea24d4d0

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
- cmoc の実行時に複数の runtime helper を束ねる共通領域の入口。ここでは個別機能の実装ではなく、この配下が runtime 共通処理のまとまりであることを示す。
- 共有 helper 群へ進む前のルーティング点として使い、実装詳細は下位の対象へ委ねる。

## Read this when
- cmoc 実行時に、複数モジュールで共有する helper の置き場や入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime 共通処理のまとまりであることを確認したいとき。

## Do not read this when
- 特定 helper の入出力や失敗時挙動を知りたいとき。この対象ではなく、該当する下位要素を読む。
- CLI 固有の処理やテスト固有の処理を調べたいとき。共有 helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 0ec38a32d924690b6bfec833b61b47ee4fc3408217420c2dd7d9c25008715f56

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
- `src/sub_commands` は `cmoc` の各サブコマンド実装を束ねる入口で、ここでは個別処理そのものではなく、どの機能をどの下位実装へ案内するかを読む。
- 共通 CLI ルーティング、個別サブコマンドの責務分担、または `apply` / `review` / `session` / `tui` のどれを読むべきかを切り分けたいときの起点にする。

## Read this when
- サブコマンド群の全体構成や、目的の処理がどの下位実装にあるかを判断したいとき。
- `apply`、`review`、`session`、`tui`、`doctor`、`eval_oracle` のどれを読むべきかを先に絞りたいとき。
- CLI の入口から各サブコマンド実装へどう分岐するかを確認したいとき。

## Do not read this when
- 個別サブコマンドの実行フローや詳細な処理内容を追いたいときは、この階層ではなく各サブコマンド本文を直接読む。
- 引数定義や実行時の共通基盤だけを確認したいときは、サブコマンド群ではなく CLI runtime 側を読む。
- 正本仕様そのものを確認したいときは、実装ではなく対応する oracle doc を読む。

## hash
- 56adbf905ea6873a5abd57c62deeb29a8f1c6a216a94f5a6a0e92973ee64b6cf
