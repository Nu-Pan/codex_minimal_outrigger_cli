# `__init__.py`

## Summary
- cmoc の共有ランタイム helper 群に属するパッケージ入口であることを示すだけの、ごく小さい初期化本文。現時点では公開 import や初期化処理を持たない。

## Read this when
- 共有ランタイム helper 群のパッケージ境界や、この階層が cmoc の共通実行時支援を扱う領域かを確認したいとき。

## Do not read this when
- 個別の helper 関数、クラス、定数、具体的な runtime 挙動を調べたいとき。その場合は同階層の責務別 runtime 実装本文へ進む。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- 旧来の `commons.cmoc_runtime` import 経路を保つための薄い再公開モジュール。エラー、結果型、path、git、state、config、logging、Codex、hash/binary helper を責務別 runtime module から import して公開する。
- この file 自体は実装ロジックを持たず、既存呼び出し元の互換性と公開名一覧の確認に使う。

## Read this when
- 旧来 import で公開されている名前、または責務別 runtime module への対応を確認したいとき。
- `cmoc_runtime.subprocess` や `cmoc_runtime.time` のようなテスト用互換公開を確認したいとき。

## Do not read this when
- ランタイムの具体的な挙動を変更したいとき。その場合は下記の責務別 module を読む。

## hash
- 9ed7d44e36c16b4b5c954de65c8f1652ab899285d79ee3be5af2bd2c5b8ff1a2

# `runtime_errors.py`

## Summary
- 共通エラー型 `CmocError` と、CLI 表示用の構造化エラー本文生成を扱う。

## Read this when
- cmoc 共通エラーの保持項目、next action、例外の表示整形、call stack 付き error report を変更したいとき。

## Do not read this when
- git、config、Codex など個別操作の失敗条件そのものを調べたいとき。各責務 module を読む。

## hash
- feeb51cfbe1a571af40311c8b7dfc6d02d73e4e4c273cd11cb89e99f1843134b

# `runtime_results.py`

## Summary
- 外部コマンド結果 `CommandResult` と Codex exec 結果 `CodexExecResult` の共有データ型を定義する。

## Read this when
- subprocess や Codex 呼び出し wrapper の戻り値として共有されるフィールドを確認・変更したいとき。

## Do not read this when
- 実際の git/Codex 実行処理、ログ保存、retry 制御を変更したいとき。

## hash
- bc07588fcd418f58345aaaf5fa48ed9b3883bbf1e0d628d07ed74c959c60c719

# `runtime_paths.py`

## Summary
- repo/work root 解決、timestamp、duration 表示、`.cmoc` 配下の標準ディレクトリ・ファイルパス、作業ディレクトリ切替、cmoc root 探索を扱う。

## Read this when
- repository root、work root、session/report/log/worktree/schema/config など、実行時に使う保存場所やパス生成規則を確認・変更したいとき。
- timestamp 表示、duration 表示、`pushd`、`cmoc_root` の挙動を扱うとき。

## Do not read this when
- path に保存される状態 JSON、config JSON、Codex call log の内容やライフサイクルを調べたいとき。

## hash
- 9eaef775dec895fcf6af052fc7741e21fee7ffb91b90c00b12b19394c69558b9

# `runtime_git.py`

## Summary
- git subprocess wrapper、管理 branch 判定、branch/head/clean 状態確認、run worktree 作成・削除、branch 削除、`.cmoc` ignore 確保、git ignore 判定を扱う。

## Read this when
- git command 実行、worktree 操作、branch 存在確認、clean worktree 要求、`.cmoc` の追跡除外、ignore 判定を変更したいとき。

## Do not read this when
- session/apply 状態ファイルの構造、active session 探索、設定読み書き、Codex 呼び出しを調べたいとき。

## hash
- 04f69ea26437f7e11efa1bd9933fd22921e0b3124090e8cfa2ecca04c0d5e18e

# `runtime_state.py`

## Summary
- session/apply state dataclass、state file path、branch 名からの session id 抽出、branch 対応 state 読み書き、home branch の active session 探索を扱う。

## Read this when
- session state JSON、apply state JSON、cmoc session/apply branch と state file の対応、active session 探索を変更したいとき。

## Do not read this when
- git worktree/branch の実操作、設定 JSON、Codex 実行ログを調べたいとき。

## hash
- 0b2442ec7f0f2d5c61d738e22859f62c19db77e2be19fc6607060816ec596f69

# `runtime_config.py`

## Summary
- `CmocConfig` の dict 変換、config JSON の読み込み・書き込み・同期、既定値補完、設定値の型変換エラーを扱う。

## Read this when
- `<repo-root>/.cmoc/config.json` の永続化形式、読み込み時の補完、書き戻し、設定不正時のエラーを変更したいとき。

## Do not read this when
- 設定 dataclass の項目定義や既定値そのものを確認したいだけなら、`src/config` を読む。

## hash
- 3fcf385d58835fbc52bb232c03f8d4634678aba9fe13bf65da3728c24552d4ed

# `runtime_logging.py`

## Summary
- subcommand 単位の JSONL logger、現在の logger を保持する context var、経過時間と quota wait 累積を扱う。

## Read this when
- subcommand log の event 形式、保存先、現在 logger の設定・取得・リセット、quota wait 加算を変更したいとき。

## Do not read this when
- Codex call log、stdout/stderr/output log、CLI 表示そのものを変更したいとき。

## hash
- 11d652749b9cb4df02aa6682b709b3e3053003bf47a98ac8479e06803ca9dc0b

# `runtime_codex_profile.py`

## Summary
- Codex profile 生成、sandbox mode 変換、Codex home 解決・検証、Codex subprocess 環境、schema 保存、Codex JSONL/stdout/stderr の error/resume/quota/capacity 判定 helper を扱う。

## Read this when
- AgentCallParameter から Codex profile を作る処理、CODEX_HOME の扱い、Structured Output schema の保存、Codex 出力のエラー判定や resume token 抽出を変更したいとき。

## Do not read this when
- Codex CLI/TUI subprocess の起動順序、retry loop、call log、subcommand logger 連携を変更したいとき。

## hash
- c9e43969363b335a869c1a2162a6fa823ce07dc4b88a17a3c521a776f2a28fae

# `runtime_codex.py`

## Summary
- Codex CLI exec/TUI subprocess の実行制御を扱う。exec では call/stdout/stderr/output log、Structured Output 検証、semantic retry、capacity retry、quota polling/resume、subcommand logger 連携を実装する。

## Read this when
- Codex CLI/TUI 呼び出し、JSONL/stdout/stderr/output/call log、schema validation retry、capacity retry、quota polling/resume、Codex call event 出力を変更したいとき。

## Do not read this when
- Codex profile 文字列、CODEX_HOME 検証、sandbox mode 変換、schema file 保存、エラーテキスト抽出だけを変更したいとき。

## hash
- b9f190cc5692b7c271a433ae780a8db55d4fde222bc9b6f79eb58914905f8845

# `runtime_content.py`

## Summary
- file/text sha256、内容 hash 付きファイル生成、binary 判定を扱う。

## Read this when
- hash に基づく生成ファイル名、ファイル内容更新判定、binary 判定の共通処理を変更したいとき。

## Do not read this when
- git ignore 判定や INDEX.md の hash 更新ロジックを調べたいとき。

## hash
- a914c083a867428af66f067f4a90c2f94123f6c97d0af270e8802bfbef05b28f
