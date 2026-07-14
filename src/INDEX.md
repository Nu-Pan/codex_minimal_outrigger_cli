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
- `commons` 配下の実行時共通基盤をまとめる領域。ここは個別サブコマンドの業務処理ではなく、複数モジュールから共有される runtime helper 群への入口として読む。
- `cmoc_runtime.py` は、Codex 実行前後の共通処理を束ねる入口。実行ライフサイクル、preflight、ログ、設定・状態・パス・Git・エラー処理・結果型を横断して追うときにここを起点にする。
- `indexing.py` は、Codex 実行前に INDEX 更新 preflight を走らせ、必要なら commit まで行う経路の入口。既存 entry の再利用、欠落 entry の生成、検証、失敗時挙動を確認したいときに読む。
- `runtime_apply.py` は `cmoc apply abandon` の cleanup と、worktree 解決・PID 追跡・process group 停止を扱う実装。apply 実行中 process の記録や停止判定を追うときに読む。
- `runtime_cli.py` は CLI サブコマンド共通の実行ライフサイクルをまとめる。work root 検査、doctor preprocess、ログ初期化、step 通知、完了サマリー、例外の終了コード化を確認したいときに読む。
- `runtime_codex.py` は Codex 実行系の公開入口を再エクスポートする薄い境界。exec 実行と TUI 実行の起点だけを確認したいときに読む。
- `runtime_codex_exec.py` は Codex exec の単一試行ループと再試行制御の入口。Structured Output 検証、quota 待機、resume token 継続、call log と event 記録を追うときに読む。
- `runtime_codex_logging.py` は Codex CLI 呼び出し通知と起動失敗時の文面整形を共通化する補助。console 表示の見え方や失敗理由の短い整形を確認したいときに読む。
- `runtime_codex_preflight.py` は Codex exec/TUI 実行直前に indexing preflight を差し込む薄い委譲層。preflight の登録、解除、再入抑止、直列化を追うときに読む。
- `runtime_codex_profile.py` は Codex CLI 起動前後の境界処理を扱う。permission profile、`CODEX_HOME`、schema 配置、子プロセス追跡、JSONL error 判定を確認したいときに読む。
- `runtime_codex_tui.py` は Codex TUI 起動の共通処理。argv と `CODEX_HOME`、call log、サブコマンドログ、失敗時の扱いを揃えたいときに読む。
- `runtime_config.py` は設定の正本型と永続化 JSON の変換、読み込み、検証、既定値補完、書き戻しを担う。設定ファイルの形式や利用者向けエラーを確認したいときに読む。
- `runtime_content.py` は内容 hash と内容アドレス型ファイルの補助をまとめる。digest 計算、重複書き込み回避、簡易 binary 判定を確認したいときに読む。
- `runtime_doctor.py` は doctor 用の Git ロック、一時 index、`.gitignore` 修復、`.agents/.gitkeep` 補完、修復 commit 生成を扱う。doctor 実行時の Git state 復元や並行実行の競合回避を確認したいときに読む。
- `runtime_errors.py` は cmoc の実行時例外を利用者向け Markdown エラーレポートへ変換する共通処理。概要、復旧案、詳細、呼び出しスタックの出力を確認したいときに読む。
- `runtime_git.py` は Git 依存の基盤処理をまとめる境界。branch/HEAD/worktree 判定、`.cmoc/local` の ignore 管理、Git 由来のエラー整形、oracle/realization 判定に使う path 判定を扱う。
- `runtime_logging.py` はサブコマンドごとの JSON Lines ログと経過時間をまとめる共有 logger。イベント記録、step timing、quota 待機時間、現在 logger の受け渡しを追うときに読む。
- `runtime_ollama.py` は cmoc が管理する Ollama の導入と serve 可否確認を担う preflight の入口。対象 model の決定、service 同期、listener 確認、load、GPU 推論確認を追うときに読む。
- `runtime_paths.py` は `<repo-root>` / `<work-root>` の解決、timestamp 生成、各種保存先 path 決定を扱う。root 解決や保存先ルール、cwd 切替の前提を確認したいときに読む。
- `runtime_preprocess_command.py` は `cmoc` の前処理コマンド群の入口。実行開始ラッパー、設定同期、差分 commit までの流れを追いたいときに読む。
- `runtime_results.py` は外部コマンド実行結果と Codex exec 実行結果を保持する不変 dataclass 群。結果コンテナの項目や quota 計測値の保持先を確認したいときに読む。
- `runtime_state.py` は session/apply 用 state file の読み書き基盤。branch 名から session_id を復元し、JSON state を検証付きで扱い、fork 排他 lock も担う。

## Read this when
- `commons` 配下の共有 runtime helper 群へ進むべきか判断したいとき。
- Codex 実行の前処理・後処理・共通基盤の流れを追いたいとき。
- 複数モジュールから共有される補助処理の入口だけを確認したいとき。
- CLI サブコマンド固有の業務処理ではなく、共通実行基盤や周辺 helper の責務境界を知りたいとき。

## Do not read this when
- 個別 helper の実装、入出力、失敗時挙動を確認したいとき。
- CLI コマンド固有の業務ロジックやテスト固有の処理を調べたいとき。
- 共有 runtime helper ではなく、より直接その責務を持つ対象があるとき。
- この領域の入口だけではなく、下位要素の本文を直接読むべきとき。

## hash
- ed0aa8a34ffd7be01efba15d789d603249e76797fd81af48e6033460fb467714

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
- `cmoc` の各サブコマンド実装を束ねる入口で、個別コマンドの実行本体へ進む前のルーティング起点になる。
- `apply` `review` `session` `tui` のように、目的のサブコマンドが分かっているときはここから該当実装へ進む。
- この階層では共通の CLI runtime や基盤処理を追うより、各サブコマンドの責務境界を選び分けるために読む。

## Read this when
- `cmoc` のどのサブコマンドがどの実行本体に対応するかを切り分けたいとき。
- サブコマンドごとの実行フローや入出力の責務境界を確認したいとき。
- 個別コマンドの入口を見つけて、さらに下位の実装へ進みたいとき。

## Do not read this when
- 共通の CLI runtime や session/state などの基盤だけを確認したいときは、より下位の共通実装へ直接進む。
- すでに対象のサブコマンド名が分かっていて、その個別実装へ直接進めるとき。
- サブコマンド全体の定義や一覧ではなく、特定機能の内部処理だけを見たいとき。

## hash
- 81d540ec7a4d3cc96764e277f9dea4b5c2a0b360b473ed52f0ca550521c62be2
