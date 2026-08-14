# `acp`

## Summary
- `acp` 互換公開層の入口。公開名の存廃や `oracle` 側の正本実装への移行を判断する際に、配下の互換入口と builder adapter 群への導線を確認する。

## Read this when
- `acp` 公開名を維持・削除できるか判断するとき
- 既存の `acp.*` 参照を `oracle.*` または実体モジュールへ移行する経路を調査するとき
- 互換 builder adapter を通じた feedback、indexing、quota probe、session join、TUI、oracle command、realization workload の接続構成を確認するとき

## Do not read this when
- `oracle` 側の正本実装の仕様、入出力、処理ロジックを確認・変更するとき
- 互換入口の具体的な利用箇所や、個別実体モジュールの内部挙動だけを調査するとき
- `acp` や builder adapter と無関係な CLI 処理、workload 本体、正本仕様、テストを調査するとき

## hash
- ee386a90d331d71cd78aba32d2f9329e1394f7d5dddc317ec50ada7eae6cf3b8

# `basic`

## Summary
- `basic.*` の互換 import を維持するための realization 側公開入口。ACP 型、path model、構造化文書 API を正本実装から再公開し、個別実装や正本仕様は保持しない。各モジュールの公開経路・互換参照を確認するための下位入口である。

## Read this when
- `basic.*` の互換 import を維持・削除する判断をするとき。
- realization 側から ACP 型、path model、構造化文書 API がどの経路で公開されるかを確認するとき。
- 個別モジュールの再公開関係を調査するとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各再公開元の oracle 側を直接読む。
- 個別 API の詳細や参照削除の影響だけを調べるときは、対象モジュールまたは参照箇所へ直接進む。
- `basic.*` と無関係な処理を調査・変更するとき。

## hash
- 292bc262556c427d8a4a7636a2c7e14127adfdea1c7d57f167e9bfa04d4ce5ea

# `cmoc_runtime.py`

## Summary
- `commons.cmoc_runtime` の公開名を互換的に再公開する薄い import shim。pyproject が `cmoc_runtime` を公開し、ツリー内の呼び出し元がこのパスを直接 import している間の移行入口。

## Read this when
- `cmoc_runtime` の互換 import path、公開名、または runtime module への移行状況を確認するとき。

## Do not read this when
- runtime の実装や責務別 module の詳細を確認するときは、`commons.cmoc_runtime` または該当する runtime module を直接読む。
- 互換 path の移行完了後は、この shim を読む必要はない。

## hash
- ce0901465f229760c4bd1f4c5ce3f4a035bb53bf6aee04de082b5843cff3ff17

# `commons`

## Summary
- `commons` は cmoc の共通 runtime 実装を集約するパッケージで、CLI lifecycle、Codex 実行、設定、Git、状態、ログ、feedback、editing run、INDEX 更新などの下位機能へ進むための入口を提供する。
- `cmoc_runtime.py` は複数の runtime module が公開する API・定数・型を再公開する集約入口。個別実装の詳細ではなく、共通公開面や横断依存を確認するときに読む。
- `indexing.py` は INDEX.md の探索、entry の再利用・生成、hash 検証、書き込み、lock、Codex 呼び出し、Git commit までの indexing lifecycle を扱う。
- `prompt_editor_input.py` はエディタ入力の予約・読込、prompt skeleton の placeholder 検証、コメント除去、完全 prompt の確定、`.cmoc` ignore 保証を扱う。
- `runtime_cli.py` は CLI サブコマンド共通の work-root 検査、doctor・feedback・logger lifecycle、step 通知、割り込み・失敗・完了時の終了処理を扱う。
- `runtime_codex.py` は Codex exec と TUI の公開実行 API を再公開する薄い入口。具体的な exec/TUI 挙動を調べる場合は下位 module を読む。
- `runtime_codex_exec.py` は Codex exec の subprocess 実行、ログ、capacity/quota retry、session resume、Structured Output 検証・補正、成果物保護を一体で扱う。
- `runtime_codex_logging.py` は Codex 呼び出しの console 通知と起動失敗エラーの共通整形を扱う。
- `runtime_codex_preflight.py` は Codex exec/TUI 起動前の INDEX 更新 preflight の登録・解除、再入防止、直列化、work-root 導出を扱う。
- `runtime_codex_profile.py` は Codex CLI subprocess 境界として argv・環境・sandbox・CODEX_HOME・schema、process tracking、停止、JSONL 結果と retry 対象の判定を扱う。
- `runtime_codex_tui.py` は Codex TUI の起動、設定上書き、作業ディレクトリ・ログ・通知 callback の準備、call log と終了結果の連携を扱う。
- `runtime_config.py` は cmoc 設定の JSON 永続化、型・値・循環参照の検証、既定値補完、安全な読み書きを扱う。
- `runtime_content.py` はファイル・文字列の SHA-256、hash 付きファイル保存、NUL バイト等による粗い binary 判定を提供する共通処理。
- `runtime_doctor.py` は doctor preprocess の排他、修復対象の同期、一時 Git index の退避・復元、修復差分のみの commit lifecycle を扱う。
- `runtime_errors.py` は CmocError と通常例外を利用者向け Markdown エラーレポートへ変換し、Summary、Next actions、Detail、Call stack を組み立てる。
- `runtime_feedback.py` は invocation 単位の feedback collector lifecycle、capability、IPC 受付・検証・保存、call 終了時 drain、degraded event を扱う。
- `runtime_feedback_reporter.py` は Codex call-scoped stdio MCP reporter として collector との通信、capability payload、JSON-RPC、`submit_observation` を扱う。
- `runtime_feedback_state.py` は feedback の active generation、current pointer、report cut、checkpoint、publication、incomplete 診断、cleanup と相互参照の integrity を扱う。
- `runtime_feedback_store.py` は raw observation の schema 検査、secret masking、evidence path 正規化、fingerprint・hash、重複排除、atomic durable 保存を扱う。
- `runtime_git.py` は Git command、branch/worktree、snapshot・復元、ignore、oracle/realization file 分類を担う共通 Git 境界。
- `runtime_logging.py` はサブコマンド単位の JSON Lines event、step timing、Codex quota 待機時間、current logger、並行追記の直列化を扱う。
- `runtime_paths.py` は repository/worktree/cmoc root の解決と、設定・状態・ログ・report・schema・worktree 等の runtime path 導出を扱う。
- `runtime_refactor.py` は refactor state の読み書き・schema 検証、oracle/realization file 集合との同期、調査対象の列挙と選択を扱う。
- `runtime_results.py` は Codex exec、Structured Output 検証、外部コマンド結果、呼び出しログを表す不変データ型と callable protocol を定義する。
- `runtime_run.py` は editing run の worktree 解決、state lock、process tracking、親 run と Codex child process group の安全な停止・cleanup を扱う。
- `runtime_run_lifecycle.py` は editing run の開始・状態遷移、branch/worktree、commit、差分分類、INDEX 更新、cleanup・recovery を一体で扱う。
- `runtime_run_report.py` は editing run の fork/lifecycle report を Markdown + YAML Front Matter 形式で保存し、path・YAML・Markdown のエスケープを扱う。
- `runtime_state.py` は session/run state の dataclass schema、状態遷移、永続化・復元・検証、branch 対応、lock、active session 検索を扱う。
- `runtime_windows_toast.py` は Windows toast と Codex TUI callback の非致命的 transport 境界で、通知内容、有限時間送信、turn 重複排除、callback state cleanup を扱う。

## Read this when
- commons 配下の共通 runtime API や責務分担を確認するとき
- CLI、Codex、設定、Git、state、feedback、editing run、INDEX 更新の実装入口を探すとき
- 対象機能がどの runtime module に実装されているかを切り分けるとき

## Do not read this when
- 特定 module の内部アルゴリズムや正本仕様を直接確認したいとき
- commons 配下の個別機能と無関係なアプリケーション固有処理だけを調査するとき
- 単に INDEX.md の既存 entry や hash を確認したいとき

## hash
- 1bb88b2fa943b07b656267491b13a06439ee80afef421f57bd5d9f44f463fe43

# `config`

## Summary
- 設定モジュールの互換入口を提供するディレクトリ。`__init__.py` は `config.*` 参照を成立させ、`cmoc_config.py` は oracle 側の設定型を定義せず realization 側から再公開する。設定仕様の確認先ではない。

## Read this when
- 既存利用者の `config` または `config.cmoc_config` 参照を維持・確認するとき。
- 設定型の import 経路や互換入口の有無を調べるとき。

## Do not read this when
- 設定定義の内容や仕様そのものを確認するときは、oracle 側の設定定義を直接読む。
- 設定参照を新規に追加する実装判断では、利用側の参照経路を直接確認する。

## hash
- fbc828970884bf16f7e7e6174e3461888e3c4000d754454ba9794e1d2c99d6f2

# `main.py`

## Summary
- Typer と Click を用いた cmoc CLI の最上位入口。共通の CLI アプリケーション、サブコマンド階層、コマンド引数、補完処理、引数解析エラー変換を定義し、各サブコマンド実装へ処理を委譲する。

## Read this when
- cmoc の CLI 全体のコマンド構成やトップレベル入口を確認・変更するとき
- Typer/Click の引数解析、補完、CLI 例外の cmoc 形式への変換、または互換処理を確認・変更するとき
- doctor、tui、indexing、session、oracle、realization、run、feedback の CLI コマンド登録を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や業務ロジックを確認したいときは、対応する sub_commands 配下の実装を直接読む
- oracle やエラーハンドリングの仕様を確認したいときは、対応する正本仕様を直接読む

## hash
- 266ba84d0a7501d380ff52d891fbb81985a6e3e0817f8677aabe88142f8dbef1

# `oracle.py`

## Summary
- `src` 起動時に正本側 `oracle.*` パッケージを解決するための互換用 package shim。`oracle/src/oracle` をパッケージパスとして再公開し、正本ソースが存在しない場合は `ModuleNotFoundError` を送出する。

## Read this when
- `src` だけを起動した際の `oracle.*` パッケージ解決や互換 import の挙動を確認するとき。

## Do not read this when
- 正本側 `oracle.*` の実装内容を確認するときは、直接 `oracle/src/oracle` 配下を読む。
- `src` の通常の CLI 実装や、package shim と無関係な import 経路を調査するとき。

## hash
- e476648f073484004b64741d40d6d373fab223e001be01ac8051f9c5ab15e095

# `sub_commands`

## Summary
- CLI サブコマンドの実装をまとめるディレクトリ。各サブコマンドの実行入口や実装構成を確認する際の起点であり、対象のサブコマンドに対応する下位要素へ進むために読む。現在は apply と review の実装本文がなく、doctor、feedback、indexing、oracle、realization、run、session、tui などの実装入口が配置されている。

## Read this when
- cmoc の特定サブコマンドの実装入口や実行フローを調査・変更するとき。
- サブコマンドごとの処理領域を特定し、対応する下位実装へ進む起点を確認するとき。

## Do not read this when
- サブコマンドに共通する CLI ランタイム、Git・パス処理、state 管理などの詳細だけを確認するとき。
- サブコマンドの正本仕様や、特定サブコマンド配下の具体的な処理を直接確認すべきとき。

## hash
- 1c6d040a622b3d194446880ca56536a02e99a0bc3e4fed09898b13b7fe54fbba
