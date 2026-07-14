# `acp`

## Summary
- `acp` 名前空間の互換入口と、その配下の builder 互換層を束ねる上位ルート。`oracle` 側の正本実装へ既存 `acp.*` 参照をつなぐための案内役であり、実装本体ではなく公開 import 面の維持が主目的である。
- この階層では、`acp` 直下の互換入口と、builder 系の各公開経路をどこまで残すかを判断する。個別の実装ロジックを追うより、どの名前空間を互換として維持し、どれを正本側へ委譲するかを確認するために読む。

## Read this when
- `acp.*` 参照を壊さずに正本実装へ移行する作業で、互換入口の残し方や削除条件を確認したいとき。
- builder 系の公開 import がどの階層で維持されているかを確認し、利用側への影響を見積もりたいとき。
- 互換 namespace を残す必要があるか、それとも正本側の実体だけに寄せられるかを判断したいとき。

## Do not read this when
- acp の具体的な生成ロジック、CLI 挙動、入出力仕様を調べたいとき。そうした内容はこの階層ではなく、対応する正本実装側を読む。
- 新しい機能や API を追加する場所を探しているとき。この階層は互換維持が役割で、機能追加の入口ではない。
- `acp.*` の公開面がすでに消えており、互換入口の維持可否だけを確認済みで詳細が不要なとき。

## hash
- ee6fb5b7ad51e758b3da983803fc1e5e8256ffd5ccefdb517fb014eada116186

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
- `commons` 配下の runtime helper 群を束ねるパッケージ境界。個別 helper の実装ではなく、共有 runtime 機能の入口だけを確認したいときに読む。

## Read this when
- `commons` から共有 runtime helper を参照する側で、どの統合入口を使うか確認したいとき。
- 共有 runtime helper 群の下位要素へ進む前に、この領域が共通 runtime 用のまとまりであることを確認したいとき。

## Do not read this when
- 特定の helper の入出力や失敗時挙動を確認したいときは、該当する下位要素を直接読む。
- CLI サブコマンド固有の処理やテスト固有の処理を調べたいときは、共有 runtime helper ではなくその責務を持つ対象へ進む。

## hash
- 1347e9b9fc0b3440dc7dc7977f5ffa63374406e67ba2e3877603c21f57eb2d55

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
