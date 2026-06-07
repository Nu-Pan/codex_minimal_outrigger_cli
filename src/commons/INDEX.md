# `__init__.py`

## Summary

- Declares the src.commons package with a short module docstring.
- Contains no imports, exports, runtime logic, constants, or public API definitions.

## Read this when

- You need to confirm that src.commons is a Python package.
- You are documenting or routing the commons package at a package-level overview.

## Do not read this when

- You need implementation details for shared utilities; inspect the concrete modules under src/commons instead.
- You are looking for command behavior, workflow logic, configuration handling, or tests.

## hash

- ff1b23adb7b4c5a75686ac97283d2065d5cacc8861143f25677b559abeb6e2d0

# `codex.py`

## Summary

- `src/commons/codex.py` は、Codex CLI 呼び出しの共通処理をまとめるモジュールで、`codex exec` のコマンド組み立て、実行、再試行、`resume` 再開を扱います。
- Structured Output の JSON Schema 検証、`output-last-message` の読み取り、JSON/text の意味検査、起動失敗の診断整形を含みます。
- quota 待機、capacity の指数バックオフ、呼び出しログ保存、`workspace-write` 実行前の oracle 保護と `INDEX.md` メンテナンス前処理も担います。

## Read this when

- `codex exec` の起動オプション、`read-only` / `workspace-write` の切り替え、`--model` と `reasoning_effort` の制約を確認したいとき。
- Structured Output の JSON Schema 検証、JSON パース、`output-last-message` の読み取り、JSON/text の意味検証を確認したいとき。
- quota 枯渇時の待機と `resume`、capacity 失敗時の指数バックオフ再試行を追いたいとき。
- 実行前の `INDEX.md` メンテナンスや、workspace-write 時の oracle 保護の挙動を確認したいとき。
- Codex CLI 呼び出しの Markdown フルログ、出力スキーマ保存、再試行時の診断情報の扱いを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックだけを確認したいとき。
- `repo.py`、`errors.py`、`timing.py`、`timestamps.py` など他の共通モジュールだけを確認したいとき。
- `INDEX.md` の生成・更新ルールそのものや、`oracles` 全体のルーティング方針だけを確認したいとき。
- `codex exec` 以外の CLI 起動制御や、サブコマンド共通ラッパーだけを見たいとき。

## hash

- ec6bd4936dfcc6f9dd8931210a1c0d846ad3bfa12d5d171ea5132ec363be38c4

# `command_runner.py`

## Summary

- `src/commons/command_runner.py` は、`cmoc` の各サブコマンドを共通実行するラッパーで、repo root 解決、ログ開始、例外変換、終了集計をまとめます。
- `run_command()` はサブコマンド本体に `<repo-root>` の `Path` を渡し、整数戻り値や `typer.Exit` を共通規則で終了コードへ変換します。
- 実行中は `subcommand_log` と `timing` を連携し、完了時にログパス、総経過時間、quota 待機時間、戻り値を stdout と JSONL ログへ出力します。
- 内部ヘルパー `_subcommand_exit_error()` と `_print_completion_report()` が非 0 終了の診断文と完了レポート生成を担います。

## Read this when

- `cmoc init` / `session` / `apply` / `review` などの入口がどの共通処理で包まれているかを確認したいとき。
- サブコマンド本体が `Path` を受け取り、戻り値や例外がどう終了コードに反映されるかを見直したいとき。
- `subcommand_log`、`timing`、`format_error_report()` がどの順序で使われるか追いたいとき。
- 非 0 の `typer.Exit` や通常例外がどう利用者向けのエラー表示になるか確認したいとき。
- 完了サマリーに何が出るか、`subcommand_end` ログがどう書かれるかを見たいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数解析だけを確認したいとき。
- `<repo-root>` の探索や `.cmoc` まわりの詳細だけを追いたいときは、`src/commons/repo.py` を読むべきです。
- エラーメッセージ型や詳細な整形規則だけを見たいときは、`src/commons/errors.py` を読むべきです。
- JSONL ログの保存や時間計測の実装だけを見たいときは、`src/commons/subcommand_log.py` と `src/commons/timing.py` を読むべきです。
- `INDEX.md` 生成ルールや `oracles` 側の仕様だけを確認したいとき。

## hash

- 2183c4c608e64b3411b8fde23b9048fe84f439e849ea5d7561d1cb7548ac929c

# `errors.py`

## Summary

- `src/commons/errors.py` は、cmoc 全体で共通に使う例外型 `CmocError` と、エラーレポート整形関数 `format_error_report()` をまとめるモジュールです。
- `CmocError` は利用者向けメッセージ、複数の次アクション、詳細、終了コードを保持し、次アクションは最低 2 件を必須にします。
- `format_error_report()` は `ERROR` / `Summary` / `Next actions` / `Detail` / `Call stack` 形式で Markdown を生成し、通常例外と `CmocError` を分けて扱います。

## Read this when

- cmoc 全体で使う共通例外 `CmocError` の構造、制約、利用条件を確認したいとき。
- stdout 向けのエラーレポート `format_error_report()` の出力形式や、通常例外と `CmocError` の分岐を確認したいとき。
- `subprocess.CalledProcessError` の `returncode`、`cmd`、`stderr`、`stdout` を含む診断情報の整形方法を確認したいとき。
- `message`、`actions`、`detail`、`exit_code` の意味や、`actions` が 2 件以上必須である制約を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析、git 操作、`codex exec` 呼び出しなど、エラー整形以外の業務ロジックを追いたいとき。
- `repo.py`、`codex.py`、`indexing.py`、`timing.py`、`timestamps.py` など、他の共通モジュールの実装を確認したいとき。
- CLI エントリーポイントやテストコードを確認したいとき。

## hash

- 8e200a8f193254d60a14f5824ccebbacaece04d8fe6497633d460dcec7ac3d19

# `indexing.py`

## Summary

- `src/commons/indexing.py` は `INDEX.md` の生成・更新をまとめる共通モジュールです。
- 配置対象ディレクトリの列挙、既存 `INDEX.md` の再利用判定、Structured Output による目次生成、書き換え、必要時の自動コミットまでを担います。
- `memo`、隠し要素、`gitignore`、symlink、binary、UTF-8 外など、配置可否と内容検査の境界も集約しています。

## Read this when

- `INDEX.md` を自動生成・再生成・更新する処理を修正したいとき。
- `maintain_indexes()` や `is_maintained_index_path()` / `is_maintained_index_path_at_commit()` の判定条件を確認したいとき。
- 排他 lock、`gitignore`、`memo` 除外、binary / UTF-8 判定、Structured Output の検証を追いたいとき。
- `tests/test_indexing.py` が守っている回帰条件を実装側から整理したいとき。

## Do not read this when

- `cmoc indexing` のコマンド入口や引数処理だけを見たいときは、`src/sub_commands/indexing.py` を読むべきです。
- `INDEX.md` 配置・更新の正本仕様だけを確認したいときは、`oracles/docs/app_specs/indexing.md` を読むべきです。
- repo root 探索や state 管理、`codex exec` 起動など別の共通基盤を追いたいときは、このモジュールではなく関連モジュールを読むべきです。

## hash

- f26068739a977e85f7883fd0f3a303f30dd907ec151af9a9e81f46d1a115b919

# `repo.py`

## Summary

- `src/commons/repo.py` は git リポジトリと cmoc の作業領域を扱う共通基盤モジュールです。
- repo root 探索、ブランチ判定、session/apply の state 管理、process id の保存・読込、`.cmoc` の ignore 保証、git 共通ラッパーをまとめています。
- また、oracle / implementation ファイルの列挙と変更検出も担い、cmoc の各サブコマンドから再利用される基盤機能の入口になっています。

## Read this when

- repo root の検出、現在ブランチ名、HEAD commit、`cmoc` 管理ブランチ判定を確認したいとき。
- session / apply の state JSON、apply process id、active session の整合性チェックを追いたいとき。
- `.cmoc` の ignore 保証、未コミット差分の検査、apply worktree から所有元 repo root を復元する処理を確認したいとき。
- `oracles` ファイルや実装ファイルの列挙・絞り込み、変更済み oracle の収集ロジックを確認したいとき。

## Do not read this when

- `src/commons/repo.py` の個々の関数実装や細かな例外メッセージだけを確認したいとき。
- `INDEX.md` の生成・更新ルールや `oracles` 全体の仕様だけを確認したいとき。
- `CmocError` の整形、`codex exec` の起動、経過時間計測など、別の共通モジュールを追いたいとき。

## hash

- 7fa4087e64ec5173451aa5639429487bc75123a9173de952448ccfbfd05d1b04

# `report_files.py`

## Summary

- タイムスタンプ名の Markdown レポートを排他的に作成して保存する共通ヘルパーです。
- 保存先ディレクトリを事前に作成し、`build_report` で生成した本文を `x` モードで新規作成したファイルへ書き込みます。
- ファイル名衝突時は短い待機を挟んで再試行し、作成途中に失敗した場合は生成済みの一時ファイルを削除してから例外を再送出します。
- 最大 1000 回の再試行でも空きパスを確保できなければ `RuntimeError` を送出します。

## Read this when

- `<repo-root>/.cmoc/reports/...` にタイムスタンプ付きの Markdown レポートを保存する処理を実装・修正したいとき。
- 同じタイムスタンプ名が既に存在する場合に、上書きせず別名で再試行する排他生成の挙動を確認したいとき。
- レポート本文の生成は呼び出し元に任せつつ、保存先ディレクトリ作成とファイル作成だけを共通化したいとき。
- レポート保存に失敗した場合の一時ファイル削除や、最大再試行回数の扱いを確認したいとき。

## Do not read this when

- レポート本文の構成や評価結果の意味づけを確認したいときは、このヘルパーではなく、呼び出し元の `cmoc apply fork` や `cmoc review oracles` の実装を読むべきです。
- `<time-stamp>` の生成規則そのものを確認したいときは、このモジュールではなく `timestamps.py` を読むべきです。
- タイムスタンプ付きファイルの生成ではなく、既存レポートの一覧取得や後処理を確認したいときは、このモジュールの範囲外です。
- `INDEX.md` の生成や維持のルールだけを確認したいときは、このファイルではなく `indexing.py` を読むべきです。

## hash

- 47b3281358f54f5ff35ccac45b8eb36ae75cf291db1e91047da1b10c2e8fde8e

# `subcommand_log.py`

## Summary

- `src/commons/subcommand_log.py` はサブコマンド呼び出しごとの JSON Lines ログを生成・追記する共通モジュールです。
- `SubcommandLogContext` と `ContextVar` で現在のログ状態を保持し、`log_event()` と `add_quota_wait()` がイベント記録を担います。
- ログは `<repo-root>/.cmoc/logs/sub_commands/` に排他的に作成され、apply worktree や linked worktree では保存先 repo root を解決して集約します。
- 起動時には `subcommand_log()` が開始イベントとコンソール通知を出し、`info/exclude` 更新で `.cmoc/logs/` を未追跡に保ちます。

## Read this when

- サブコマンド呼び出し単位の JSON Lines ログの保存先、作成手順、追記方法を確認したいとき。
- 現在のログ状態を `ContextVar` で管理し、イベントや quota 待ち時間をどう残すか追いたいとき。
- apply worktree や linked worktree から呼んだときの保存先解決や、`.cmoc/logs/` の除外設定を確認したいとき。
- 開始メッセージやログファイルパスのコンソール出力仕様を確認したいとき。
- `tests/test_codex.py` や `tests/test_subcommands.py` でサブコマンドログの回帰を追いたいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `codex exec` の起動制御や Structured Output の扱いだけを確認したいときは、`src/commons/codex.py` を読むべきです。
- ステップ計測や経過時間表示だけを確認したいときは、`src/commons/timing.py` を読むべきです。
- repo root 探索やブランチ・worktree・state 管理だけを確認したいときは、`src/commons/repo.py` を読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`src/commons/indexing.py` や `oracles/docs/app_specs/indexing.md` を読むべきです。

## hash

- 741d58a56edc70209f48a158103f3b0bf30a8d64f5dae9c502bdf4f6ecd9d326

# `timestamps.py`

## Summary

- `src/commons/timestamps.py` は cmoc 仕様の `<time-stamp>` 文字列生成と判定をまとめた共通モジュールです。
- `make_timestamp()` はローカル時刻基準で `YYYY-MM-DD_HH-MM_SS_mmm` 形式の文字列を返します。
- `is_timestamp()` は正規表現と日時の妥当性確認で、その形式かどうかを判定します。
- `console_timestamp()` はコンソール表示向けの日時文字列を返します。

## Read this when

- `make_timestamp()` がどのような `<time-stamp>` 文字列を返すか確認したいとき。
- aware / naive の `datetime` をどのように扱うか確認したいとき。
- `is_timestamp()` と `TIMESTAMP_PATTERN` による形式検証を確認したいとき。
- コンソールログ用の日時文字列 `console_timestamp()` の形式を確認したいとき。

## Do not read this when

- `report_files.py` など、タイムスタンプ文字列を使う保存処理の詳細を確認したいとき。
- `timing.py` や `format_duration()` など、経過時間の整形ロジックを確認したいとき。
- CLI のサブコマンド仕様や `INDEX.md` 生成ルールそのものを確認したいとき。

## hash

- ddd77781ba95fc018f1bbd129860524b7b44d6623222945445aabdbc77e18bc8

# `timing.py`

## Summary

- `src/commons/timing.py` は、サブコマンド実行中のステップ計測と経過時間表示をまとめるモジュールです。
- `StepTimer` で全体時間と各ステップ時間を保持し、`start_step()` で開始通知とログイベントを出します。
- `_format_step_index()` は単一階層と階層化の両方のステップ番号を表示用文字列へ整形します。
- `format_duration()` は oracle 指定の stdout 形式へ経過時間を変換し、`current_timer()` 系で現在の計測器を管理します。

## Read this when

- サブコマンド全体と各ステップの経過時間の計測方法を確認したいとき。
- ステップ開始通知の表示形式や、`step_index` の flat / hierarchical 表現を確認したいとき。
- `current_timer()`、`report_current_timer()`、`clear_current_timer()` など現在の計測器管理を追いたいとき。
- `format_duration()` の stdout 向け表示や、0.1 秒単位の切り捨て規則を確認したいとき。
- ネストしたステップで、どのステップがいつ終了扱いになるかを確認したいとき。

## Do not read this when

- サブコマンド本体の引数解析や業務ロジックだけを確認したいとき。
- `codex exec` の起動制御、Structured Output、`INDEX.md` メンテナンスそのものを確認したいとき。
- タイムスタンプ生成やサブコマンドログ保存だけを調べたいとき。
- `StepTimer` 以外の共通例外、repo 探索、ファイルレポート保存を確認したいとき。

## hash

- 822869d260c24c976ead0ecc66a80a76f2267fe39cbad09b80b426f42b996474
