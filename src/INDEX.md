# `acp`

## Summary
- oracle 側の acp builder 実装を正本に保ちつつ、旧来の `acp.*` / `acp.builder.*` import 経路を成立させる realization 側互換入口を扱う階層。
- 既存公開名の再公開、canonical oracle 実装への中継、薄い wrapper、移行期間中の削除条件を確認するための入口になる。
- apply、review、session、tui、indexing 系 builder の互換経路に加え、quota 回復確認用の低コスト probe builder も含む。

## Read this when
- `acp.*` または `acp.builder.*` の旧 import 互換性を確認・維持・削除判断したいとき。
- realization 側や利用者向け公開面に残る acp 系 import を oracle 側実装へどう接続しているか調べたいとき。
- oracle 側 builder の結果を既存の公開型や公開名へ適合させる wrapper、再公開、中継処理を確認したいとき。
- quota wait 中の回復確認で使う最小 agent call parameter builder の内容を確認・変更したいとき。

## Do not read this when
- acp builder の正本仕様、prompt、生成内容、人間意図を確認したいときは、対応する oracle 側 builder を読む。
- apply fork、review、session、TUI などの機能全体の実行フローや CLI 制御を調べたいときは、それぞれの上位実装や呼び出し元を読む。
- ACP parameter の公開型、path model、git helper、index entry 生成仕様など、builder 互換入口以外の共通実装を調べたいときは該当対象を読む。
- 新規 acp 機能や API 仕様の追加場所を探しているだけで、既存 import 互換や quota probe に関係しないとき。

## hash
- c35c16dceec30fb4f9b69e36cbbab9e4f340620e069b481f5450635346d5d7e8

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
- cmoc の実行時に複数領域から共有される runtime helper 群をまとめる領域。
- Codex 実行、CLI 共通 runner、config、content hash、doctor preprocess、error、git、logging、Ollama、path、result、state、apply process、INDEX 更新 preflight などの runtime 共通処理への入口になる。
- この領域自体は共有 runtime 実装群のまとまりであり、個別 API の挙動や責務境界は下位要素の本文で確認する。

## Read this when
- cmoc の runtime 共通機能の配置を調べ、どの helper や再公開入口へ進むべきか判断したいとき。
- Codex exec/TUI 実行、profile、preflight、call log、quota retry、Structured Output 検証など Codex 実行基盤に関わる実装を探したいとき。
- CLI サブコマンド共通 runner、doctor preprocess、config 同期、subcommand logging、利用者向け error report など、複数コマンドから共有される実行制御を確認したいとき。
- git 操作、root/path 解決、content hash、session state、apply process 追跡、Ollama 管理、外部コマンド結果型などの runtime 補助処理を確認・変更したいとき。
- INDEX.md 自動更新 preflight、entry hash 検証、Codex による entry 生成、indexing commit 作成の実装を確認・変更したいとき。

## Do not read this when
- 個別 CLI サブコマンドの業務処理、引数定義、Typer 登録、利用者向け workflow を調べたいときは、該当するサブコマンド実装や app spec を読む。
- 正本仕様断片、prompt、Structured Output schema、path model、config 定義、FileAccessMode の自然言語ルールを確認したいだけなら、対応する oracle 側の文書や定義を読む。
- テスト固有の fixture、期待値、外部挙動検証を調べたいときは、test 側の対象を読む。
- 特定の runtime API の詳細が既に分かっている場合は、この領域全体ではなく、該当する下位要素を直接読む。

## hash
- 2066f4f53d71acc44dc6cc3bf52d0638fb28b39cebf488231083c84b224b7174

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
- CLI サブコマンド実装の入口を集める領域で、session、apply、review、indexing、doctor、TUI、oracle 評価などの利用者向け操作から、各 workflow の制御ロジックへ進むためのルーティング境界を担う。
- 各サブコマンドの薄い委譲入口から、状態遷移、branch/worktree 管理、Codex 呼び出し、merge、cleanup、report 生成、runtime preprocess 連携まで、操作種別ごとの主要処理へ下位対象を振り分ける。

## Read this when
- CLI サブコマンドの実装入口を探し、どの下位対象へ進むべきかを判断したいとき。
- session、apply、review、indexing、doctor、TUI、oracle 評価のいずれかに関する実行フロー、事前条件、委譲先、状態更新、branch/worktree 操作、report 出力の担当箇所を探したいとき。
- 複数のサブコマンド間で、runtime への接続、workflow orchestration、失敗時処理、cleanup、利用者向け出力の責務境界を確認したいとき。

## Do not read this when
- CLI 全体のサブコマンド登録、共通 runtime、共通 git/worktree helper、状態ファイル形式、path model の定義そのものを調べたいとき。
- oracle file や realization file の定義、INDEX.md エントリー作成規則、正本仕様文書そのものを確認したいとき。
- 具体的に読むべきサブコマンド実装や共通 helper が既に決まっており、その対象へ直接進めるとき。

## hash
- 4c210d36a5c9cb163a471286ee12499ce103325bf1130c39dd74f1e81ad9a346
