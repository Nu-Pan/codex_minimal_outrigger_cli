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
- `src/commons` は cmoc の実行時共通基盤を集める領域で、サブコマンド実行、設定、状態、Git、パス、ログ、エラー、Codex 呼び出し周辺の共有処理へ進むための入口になる。個別機能は下位モジュールで読む。
- `__init__.py` は共有 runtime helper 群のパッケージ境界だけを示す。共有 helper の入口を確認するときだけ読む。
- `cmoc_runtime.py` は実行ライフサイクル全体の横断入口で、Codex 実行前後の準備、設定・状態・ログ・パス・Git・エラー・結果型をまとめて扱う。
- `indexing.py` は Codex 実行前の INDEX 更新 preflight と、その commit 判定や生成結果の検証を扱う。
- `runtime_apply.py` は `cmoc apply abandon` の cleanup と、対象 worktree や実行中 process の追跡・停止確認を扱う。
- `runtime_cli.py` はサブコマンド共通の実行順序、work root 検査、doctor preprocess、step 通知、完了サマリー、例外の終了コード化を扱う。
- `runtime_codex.py` は Codex 実行系の公開入口で、exec 実行と TUI 実行の起動関数を同じ import 元から参照できるようにする。
- `runtime_codex_exec.py` は Codex exec の単一試行と再試行制御、Structured Output 検証、quota 待機、resume token、実行ログ記録を扱う。
- `runtime_codex_logging.py` は Codex CLI 呼び出しの console 表示と起動失敗時の error 文面整形を共通化する。
- `runtime_codex_preflight.py` は Codex exec/TUI の直前に indexing preflight を挟む薄い委譲層で、登録、起点 root 決定、再入抑止を扱う。
- `runtime_codex_profile.py` は Codex CLI の起動条件、sandbox、`CODEX_HOME`、schema 配置、子プロセス追跡、JSONL エラー判定の境界を扱う。
- `runtime_codex_tui.py` は Codex TUI 起動の共通処理で、argv と `CODEX_HOME` の準備、call log、実行結果の返却を扱う。
- `runtime_config.py` は cmoc config の読み込み、検証、既定値補完、永続 JSON との変換を扱う。
- `runtime_content.py` は SHA-256 digest に基づく内容アドレス型ファイルの書き出しと簡易 binary 判定を扱う。
- `runtime_doctor.py` は doctor 用の Git ロック、一時 index、ignore 修復、placeholder 補完、修復 commit 生成を扱う。
- `runtime_errors.py` は cmoc の実行時例外と利用者向け Markdown エラーレポート生成を扱う。
- `runtime_git.py` は Git 依存の基盤処理で、branch/HEAD/worktree 判定、ignore 管理、Git 由来エラー整形、oracle/file path 判定を扱う。
- `runtime_logging.py` はサブコマンドごとの JSON Lines ログと経過時間の共有 logger を扱う。
- `runtime_ollama.py` は cmoc が管理する Ollama の導入、service 同期、提供確認、model 取得と検証を一連で扱う。
- `runtime_paths.py` は `<repo-root>` と `<work-root>` の解決、timestamp、保存先 path の決定を扱う。
- `runtime_preprocess_command.py` は `cmoc` の前処理コマンド群の実行順、設定同期、設定 commit を扱う。
- `runtime_results.py` は外部コマンド実行結果と Codex exec 実行結果を保持する不変 dataclass を扱う。
- `runtime_state.py` は session/apply 用 state file の読み書き、branch からの session_id 復元、active session 探索、fork lock を扱う。

## Read this when
- cmoc 実行時の共通基盤の入口を探したいとき。
- 共有 runtime helper 群のパッケージ境界だけを確認したいとき。
- Codex 実行の前後をまたぐ共通処理をまとめて追いたいとき。
- Codex 実行前の indexing preflight を確認したいとき。
- `cmoc apply abandon` の cleanup と停止対象の追跡を確認したいとき。
- サブコマンド共通の実行順序や失敗時の見せ方を確認したいとき。
- Codex 実行系の公開 API 境界だけを確認したいとき。
- Codex exec の再試行、quota 待機、Structured Output 検証、resume token を確認したいとき。
- Codex CLI 呼び出しの console 表示や失敗文面を確認したいとき。
- Codex 実行前に indexing preflight を差し込む条件や順序を確認したいとき。
- Codex CLI の起動条件、sandbox、`CODEX_HOME`、schema、JSONL エラー判定を確認したいとき。
- Codex TUI 起動時の argv、`CODEX_HOME`、call log、失敗時の扱いを確認したいとき。
- 設定ファイルの保存形式、検証、既定値補完、書き戻しを確認したいとき。
- 内容 hash による成果物名生成や binary 判定を確認したいとき。
- doctor の Git 修復や ignore 保障の流れを確認したいとき。
- cmoc の共通エラーレポート構成や文面を確認したいとき。
- Git 依存の基盤処理や oracle/file path 判定を確認したいとき。
- サブコマンドごとの JSON Lines ログや step 経過時間を確認したいとき。
- Ollama の導入と local SLM 提供の preflight を確認したいとき。
- `<repo-root>` と `<work-root>` の解決や保存先 path を確認したいとき。
- 前処理コマンドの順序や設定同期、設定 commit を確認したいとき。
- 外部コマンドや Codex exec の結果コンテナを確認したいとき。
- session/apply state の読み書きや branch からの session_id 復元を確認したいとき。

## Do not read this when
- 個別 helper の実装や入出力、失敗時挙動だけを確認したいとき。
- CLI 固有の業務ロジックやテスト固有の処理を追いたいとき。
- 単一サブコマンドだけの詳細を知りたいときは、その責務を持つ下位モジュールを直接読むべきとき。
- INDEX の表示テンプレートや項目仕様だけを知りたいとき。
- session state の読み書きや branch 遷移だけを追いたいとき。
- サブコマンドの個別ビジネスロジックだけを変更したいとき。
- exec 実行の具体的処理、引数処理、プロセス制御を確認したいとき。
- TUI 起動、端末制御、対話実行の具体的挙動を確認したいとき。
- 記録先そのものや永続化の責務を変えたいとき。
- Codex 実行本体や構造化出力の判定を調べたいとき。
- 単純な path 操作や局所 helper だけを確認したいとき。
- 実行結果コンテナではなくログ保存先だけを知りたいとき。
- route の選定ではなく state schema の人間向け正本仕様を見たいとき。

## hash
- 89fa7e9a5b55749343e2d2be2b615e29f9308a5b57aca596b82c9d96b95c9015

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
