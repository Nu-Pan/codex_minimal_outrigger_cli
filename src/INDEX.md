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
- cmoc の実行時に複数箇所から共有される runtime helper 群をまとめる領域。
- Codex 実行、CLI 共通 runner、config、content hash、doctor preprocess、error、git、logging、Ollama、path、result 型、state、apply process、INDEX 更新 preflight など、サブコマンド横断の実行基盤へ進む入口になる。

## Read this when
- cmoc の複数サブコマンドや複数 runtime モジュールから使われる共通処理の配置先を探したいとき。
- Codex exec/TUI の起動、profile/env/sandbox/schema、quota/capacity/resume、call log、preflight など Codex 呼び出し基盤を確認したいとき。
- CLI 共通実行ライフサイクル、doctor preprocess、config 永続化、git 操作、runtime path、logging、error report、state file、apply process 追跡など、サブコマンド横断の挙動を確認・変更したいとき。
- INDEX.md 自動更新の traversal、entry parse、hash 検証、Codex による entry 生成、更新 commit の作成挙動を調べたいとき。

## Do not read this when
- 個別サブコマンド固有の業務処理、引数定義、画面表示、状態遷移を確認したいときは、そのサブコマンド実装や対応する正本仕様へ進む。
- 正本仕様断片そのもの、prompt 文面、Structured Output schema、path model、config 項目定義などを確認したいときは、oracle 側の該当対象を読む。
- 特定 helper の詳細な入出力や失敗時挙動だけを確認したいときは、この領域全体ではなく、責務が一致する下位要素を直接読む。

## hash
- 8069d34f2e57086bd4cded0490bbd3127f65aa5370bdf56444dcec7902c34d54

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
- CLI サブコマンドの実行本体をまとめる実装領域。apply、session、review oracle、indexing、tui、doctor、eval oracle などの外部挙動を、CLI runtime、git 操作、worktree・branch・state 管理、Codex 呼び出し、report 生成へ接続する。
- 各サブコマンドの詳細実装へ進む入口であり、サブコマンドごとの開始条件、状態遷移、cleanup、失敗時挙動、利用者向け出力、下位 helper への委譲関係を切り分けて確認するために読む。

## Read this when
- CLI サブコマンド単位の実行フロー、事前条件、状態更新、git/worktree/branch/process 操作、cleanup、警告やエラー出力を確認または変更したいとき。
- apply workflow の開始、fork、join、abandon、report、conflict 処理、process 停止、apply state 更新など、apply 系サブコマンドの制御へ進みたいとき。
- session lifecycle の開始、完了、破棄、home branch と session branch の merge、session state 更新、conflict 解消、rollback 条件を調べたいとき。
- review oracle の対象列挙、review loop、finding 操作、INDEX 変更の commit/merge、report 出力、isolated worktree cleanup のどこを読むべきか判断したいとき。
- indexing、tui、doctor、eval oracle などの薄いサブコマンド入口が、runtime 共通処理や既存実装へどのように委譲しているかを確認したいとき。

## Do not read this when
- トップレベル CLI へのサブコマンド登録、Typer app 構成、外側の command routing だけを確認したいとき。
- git wrapper、CLI runtime、work root 解決、状態ファイル読み書き、path model、oracle file 判定、cmoc ignore 判定などの共通 runtime API 自体を変更したいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder、finding 生成・適用・変更要約 builder の本文や定義だけを確認したいとき。
- oracle file や realization file の定義、INDEX.md 生成規則、path model、各サブコマンドの正本仕様を確認したいとき。
- 各サブコマンドの具体的な workflow 制御ではなく、パッケージ初期化、import 時副作用の有無、または共通 helper の詳細だけを確認したいとき。

## hash
- 354ec78a37f5cc041dfd7f52b647b414482a19649d1ba0417f9169c74b6cd921
