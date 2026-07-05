# `acp`

## Summary
- ACP 互換領域の入口。oracle src 側の acp builder 実装を複製せず、既存の ACP import 経路を canonical oracle 実装または実体 module へ接続するための薄い公開面を扱う。
- 移行期間中の公開 import 互換、builder 系 package へのルーティング、oracle 側 builder を正本に保つための再公開・委譲・最小補正の境界を確認する起点になる。

## Read this when
- 旧 ACP import 経路を oracle 側または実体 module へ移行する作業で、互換入口を残す理由や削除条件を確認したいとき。
- ACP builder 配下の互換 package、module alias、公開型への適合、既存 caller 向け再公開の扱いを広く確認したいとき。
- apply fork、review、session、tui、indexing、quota probe などの builder 領域のどこへ進むべきか判断したいとき。
- oracle src 由来の acp builder 互換 import が realization 側または利用者向け公開面でどこに維持されているかを確認したいとき。

## Do not read this when
- ACP builder の生成処理本体、prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいときは、対応する oracle 側 builder または oracle document を直接読む。
- agent call parameter の型定義、path model、file access mode、git helper など builder 以外の共通基盤を調べたいときは、それぞれの定義元を読む。
- apply、review、session、tui など各機能本体の実行フロー、CLI 引数処理、状態操作、画面構成を調べたいときは、対象機能の実装へ進む。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持と builder 入口の接続が中心であり、機能追加の正本入口ではない。
- ACP import 経路がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口や builder ルーティングの詳細を読む必要がないとき。

## hash
- c998cd7e54fda57cb94b9bc6b62012bfde7472cbaecc8db84b5a3449cb3bce3b

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
- cmoc の実行時に複数箇所から共有される runtime helper 群をまとめる領域。
- Codex 実行、設定、git、path、logging、state、error、content hash、doctor preprocess、INDEX 更新 preflight など、サブコマンド横断の実行基盤へ進む入口になる。

## Read this when
- CLI サブコマンドや runtime 処理から共有される helper の配置先を探したいとき。
- Codex exec/TUI 起動、profile、preflight、call log、quota/capacity retry、Structured Output schema、Codex 実行結果の扱いを確認したいとき。
- config、git、path、logging、state、error、content hash、doctor preprocess など、複数機能から使われる runtime 基盤の責務先を選びたいとき。
- INDEX.md 自動更新や entry hash 検証、Codex による entry 生成、indexing commit の実装へ進みたいとき。

## Do not read this when
- 個別 CLI サブコマンドの引数、業務処理、利用者向け workflow を確認したいときは、該当するサブコマンド実装へ進む。
- oracle file にある正本仕様断片、prompt、path model、config 定義そのものを確認したいときは、oracle 側の対象へ進む。
- 特定の runtime API の詳細がすでに分かっているときは、この領域全体ではなく該当する下位要素を直接読む。
- テスト固有の期待値や外部挙動を確認したいときは、対応する test 側を読む。

## hash
- bb3c20688e22920171dcc70604ba1d28a5e08545c6ad1d2d48a71a0f4c107160

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
- Typer による cmoc の最上位 CLI 定義を担い、session/apply/review 配下を含むサブコマンドを各実装関数へ接続する入口。
- 補完時以外の Click 引数解析エラーを cmoc 共通エラー形式へ変換し、console script から実行される main を提供する。

## Read this when
- cmoc の CLI コマンド構成、サブコマンド名、option 値、既定値、または実装関数へのディスパッチを確認・変更したいとき。
- Typer/Click の引数解析エラーを cmoc 形式で表示する入口処理を確認・変更したいとき。
- console script から起動されるアプリケーション入口や prog_name の扱いを確認したいとき。

## Do not read this when
- 個々のサブコマンドの業務処理、git 操作、worktree 操作、review/apply/session の内部制御を確認したいだけのときは、対応するサブコマンド実装を直接読む。
- cmoc 共通エラー型やエラー表示の詳細を確認したいだけのときは、共通 runtime 側を読む。
- INDEX.md 更新処理そのもののアルゴリズムや生成内容を確認したいだけのときは、indexing 実装を読む。

## hash
- cb7ee361b9445d7c2a928441e07765ae4eaed3d2e06d35acd79015f249e66dde

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
- CLI サブコマンドの実行本体をまとめる領域。初期化・修復、index maintenance、TUI、session 操作、apply workflow、review workflow など、利用者向け command を runtime や下位 helper へ接続する入口になる。
- 各 command 固有の preflight、branch/worktree/state/report 制御、cleanup、CLI 表示、共通処理への orchestration を確認するための上位ルーティング対象。

## Read this when
- 特定の CLI サブコマンドの実行本体がどの下位領域または module にあるかを選びたいとき。
- 利用者向け command が runtime、git 操作、state、report、Codex 呼び出し、INDEX maintenance などの共通処理へどう接続されるかを追いたいとき。
- session、apply、review、初期化・修復、indexing、TUI のいずれかに固有の実行条件、状態遷移、cleanup、出力、失敗時挙動を調べる入口を探しているとき。

## Do not read this when
- CLI runtime、git wrapper、path model、state schema、report directory、Codex 実行 wrapper などの共通基盤だけを直接確認したいとき。
- oracle file、realization file、INDEX.md 生成規則、path model などの正本仕様そのものを確認したいとき。
- prompt 文面、Structured Output schema、低レベルの state 読み書き、worktree 操作、INDEX.md 本文生成など、下位の専用 helper が直接担う詳細だけを調べたいとき。

## hash
- e92060d92738616a54c1692f13b07d67629d831b65f0cde1f7e843f8b560c05b
