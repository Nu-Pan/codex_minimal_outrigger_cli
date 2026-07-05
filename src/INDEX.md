# `acp`

## Summary
- oracle src 側の acp builder 実装を複製せず、旧来の acp import 経路を維持するための互換入口をまとめる領域。実体は canonical 実装や個別 module 側に置き、この対象は import 互換、oracle builder 委譲、realization 側公開型への最小変換への入口として機能する。
- 配下には acp builder の互換入口と apply fork、indexing、quota probe、review、session、TUI などの個別 builder 領域があり、旧参照をどこへ接続しているか、どの互換層を残すべきか、削除条件を確認するための起点になる。

## Read this when
- acp.* または acp.builder.* の旧 import 経路が、oracle 側 canonical 実装や realization 側 wrapper へどう接続されるかを調べたいとき。
- oracle 側 builder を正本に保ちつつ、realization 側で AgentCallParameter への変換、module alias、package path 追加、既知 typo 補正などを扱う場所を確認したいとき。
- apply fork、quota probe、review、session、TUI、indexing などの builder 互換入口や削除条件を確認し、個別領域へ進む入口を選びたいとき。
- 旧 acp 参照を canonical import path へ移行する作業で、残すべき互換層、公開面に残る import、削除できる条件を判断したいとき。

## Do not read this when
- acp builder の正本仕様、prompt 本文、parameter 生成内容そのものを確認したいときは、対応する oracle 側実装を直接読む。
- apply、review、session、TUI など各機能の実行フロー、画面挙動、branch 操作、finding 処理など builder 以外の実装詳細を調べたいときは、該当機能の実装へ進む。
- AgentCallParameter の基本型、file access mode、path model、Structured Output schema などの共通基礎仕様だけを確認したいときは、それぞれの共通定義を読む。
- 新しい acp 機能、公開 API、新規 import 経路を設計したいときは、この互換維持領域ではなく正本仕様または新規機能の入口を確認する。
- acp.* 参照がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- 1c5e2b3dac5ab40713d93f624d513992ff330b37eee6cb378d8ccfd94f37125e

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
- cmoc の実行時に複数モジュールから共有される runtime helper 群を収める領域。
- Codex 実行、設定、path、git、logging、state、doctor、INDEX 更新、apply process 管理など、サブコマンド横断の共通処理への入口になる。
- 個別 helper の詳細ではなく、runtime 共通機能のまとまりと下位要素へ進むための判断材料を扱う。

## Read this when
- CLI サブコマンド横断で使われる共通 runtime 処理の配置先を探したいとき。
- Codex 実行、config、path、git、logging、state、doctor、INDEX 更新、apply process 管理などの runtime 基盤のどの下位要素へ進むべきか判断したいとき。
- 複数の runtime API をまとめて参照する公開入口や、runtime helper 群の責務境界を確認したいとき。

## Do not read this when
- 個別サブコマンド固有の業務ロジック、CLI 引数、利用者向け workflow を調べたいときは、そのサブコマンド実装を読む。
- 正本仕様断片、prompt、Structured Output schema、path model など oracle 側の定義を確認したいときは、対応する oracle file を読む。
- テスト固有の期待値や外部挙動を確認したいときは、該当する test 側の対象を読む。

## hash
- ae88b6c890bc5c003c8c2739e99797def34b5e4f5717a5e54d94807a9fd6fe0b

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
- CLI サブコマンド実装を集約する階層。session、apply、review、doctor、indexing、tui など、利用者向け command の実行入口から runtime 共通処理や下位 helper へ処理を接続する。
- 各サブコマンド固有の事前条件、状態遷移、branch/worktree 操作、Codex 呼び出し、report 生成、commit や cleanup への入口を選ぶためのルーティング単位になる。

## Read this when
- 利用者向けサブコマンドの実行フロー、責務分担、どの実装へ進むべきかを切り分けたいとき。
- session、apply、review、doctor、indexing、tui の各操作について、CLI runtime から個別処理や共通 helper へどう接続されるかを確認したいとき。
- サブコマンド固有の実行条件、失敗条件、状態更新、branch/worktree 操作、commit、cleanup、report 出力、Codex 呼び出しの入口を探したいとき。

## Do not read this when
- CLI runtime、git wrapper、worktree 操作、state 入出力、path model など、複数サブコマンドで共有される基盤処理だけを調べたいとき。
- oracle file、realization file、path model などの一般定義や正本仕様断片そのものを確認したいとき。
- Codex に渡す prompt、parameter、Structured Output schema、INDEX.md 生成ロジックなど、サブコマンド入口ではなく専用 builder や共通処理が担う内容だけを確認したいとき。

## hash
- 6ea670b775708ceff5017af5f6721dd051f0664bc88c995b16313c4057ccf752
