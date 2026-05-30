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

- `codex exec` の共通起動基盤をまとめたモジュールです。コマンド組み立て、実行、再試行、`resume` の流れを扱います。
- Structured Output の JSON / schema 検証、`output-last-message` の読み取り、JSON 応答のパースと意味検証を扱います。
- quota 待機、capacity の指数バックオフ、oracle 保護、実行前の `INDEX.md` メンテナンス、呼び出しログ保存まで含みます。

## Read this when

- `codex exec` の起動方法や、`read-only` と `workspace-write` の切り替えを確認したいとき。
- Structured Output の JSON / schema 検証、`output-last-message` の読み取り、JSON 応答の解釈を確認したいとき。
- quota 待機と `resume`、capacity の指数バックオフ、oracle 保護、実行ログの保存や `INDEX.md` メンテナンス連携を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。
- `repo.py`、`errors.py`、`timing.py`、`timestamps.py` など他の共通モジュールの仕様だけを追いたいとき。

## hash

- dcb6d54f9e3426fb1a80deb7f2b0561e0293018d7c652f2709c51c4c210a9800
<!-- cmoc-index-kind: file -->

# `command_runner.py`

## Summary

- Typer から呼ばれるサブコマンド共通の実行ラッパーで、`<repo-root>` の解決、`subcommand_log` の開始、例外の変換、終了コード決定をまとめています。
- 通常のサブコマンド本体は `Path` を受け取り、`subcommand_log` と `timing` と連携して実行結果を集約します。
- `typer.Exit` と通常例外を分けて扱い、必要に応じて `CmocError` と `format_error_report()` で利用者向けのエラー表示を行います。
- 終了時には `log_event()`、`report_current_timer()`、`format_duration()`、`clear_current_timer()` を使って完了レポートを出します。

## Read this when

- サブコマンドの入口をどこに集約し、共通の実行制御をどう掛けているか確認したいとき。
- 各サブコマンドが `<repo-root>` の `Path` をどう受け取るか確認したいとき。
- 例外時のエラー表示、終了コード、`typer.Exit` への変換規則を見直したいとき。
- 実行ログ、経過時間、待機時間、戻り値の集計出力の流れを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `<repo-root>` 探索や `.cmoc` の扱いの詳細を追いたいときは、`repo.py` を読むべきです。
- エラーメッセージ本文の整形や共通例外の定義そのものを確認したいときは、`errors.py` を読むべきです。
- サブコマンドログやタイミング計測の実装だけを調べたいときは、`subcommand_log.py` と `timing.py` を直接読むべきです。
- Codex CLI 呼び出し、Structured Output、`INDEX.md` 生成など別機能を調べたいとき。

## hash

- fb8b525a34d873d1070035cae87b17be49cd73d9f27228024f1dd4718ae888f7
<!-- cmoc-index-kind: file -->

# `errors.py`

## Summary

- `src/commons/errors.py` は、cmoc 全体で使う共通例外 `CmocError` と、stdout 向けのエラーレポート整形関数 `format_error_report` をまとめるモジュールです。
- `CmocError` は利用者向けメッセージ、複数の次アクション、詳細、終了コードを保持し、次アクションは最低 2 件を必須にします。
- `format_error_report` は `ERROR` / `Summary` / `Next actions` / `Detail` / `Call stack` 形式で例外を整形し、`CmocError` と通常例外を分けて扱います。

## Read this when

- cmoc の共通エラーハンドリングや、例外から stdout 向けレポートへ変換する処理を実装・修正したいとき。
- 復旧手順を複数提示する `CmocError` をサブコマンドや共通処理から投げたいとき。
- `message`、`actions`、`detail`、`exit_code` の意味や制約を確認したいとき。
- 通常の Python 例外が cmoc の共通エラーレポートでどう表示されるか確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数解析、git 操作、`codex exec` 呼び出しを確認したいときは、このモジュールではなく該当するサブコマンドや共通処理を読むべきです。
- ログ保存、リトライ、Structured Output、サンドボックス指定など、`format_error_report` とは別の共通機能だけを確認したいときは、このファイルの範囲外です。
- タイムスタンプ生成、経過時間表示、サブコマンドログなど、他の共通ユーティリティを調べたいときは `src/commons/errors.py` ではありません。
- テスト実装の詳細や Fake Codex CLI の使い方だけを確認したいときは、このモジュールを読む必要はありません。

## hash

- a72dbd1205ce53b398ceacaaf86e966b9aba8f03be9634806f0d94a73e4717ea

# `indexing.py`

## Summary

- `INDEX.md` のメンテナンス本体を担う共通モジュールで、対象ディレクトリの列挙、既存目次の再利用判定、再生成、置換、自動コミットまでをまとめています。
- `gitignore`、`memo`、隠しディレクトリ、`build` / `tmp` / `__pycache__`、symlink、バイナリ、通常ファイルでない項目を除外して、目次作成対象を決めます。
- Codex CLI の Structured Output で `summary` / `read_this_when` / `do_not_read_this_when` を生成し、Markdown の `INDEX.md` ブロックへ整形します。
- 既存 `INDEX.md` の構文検査、内容ハッシュによる更新判定、メンテナンス用 lock、失敗時の `CmocError` 変換も担当します。

## Read this when

- `INDEX.md` の自動生成・再生成・更新・自動コミットの実装や挙動を確認したいとき。
- ディレクトリ列挙、`gitignore` 判定、`memo` 除外、隠しディレクトリや `build` / `tmp` / `__pycache__` の除外、symlink とバイナリの排除条件を追いたいとき。
- 既存 `INDEX.md` の再利用条件、内容ハッシュによる更新判定、Structured Output から Markdown への変換を確認したいとき。
- INDEX メンテナンス用の lock による直列化や、I/O 失敗をユーザー向けの `CmocError` に変換する処理を確認したいとき。

## Do not read this when

- `INDEX.md` の配置ルールや見出し構成の概要だけを知りたいとき。
- `codex.py`、`repo.py`、`errors.py` など他の共通モジュールの仕様だけを追いたいとき。
- cmoc の個別サブコマンドの引数や実行フローだけを確認したいとき。

## hash

- b789244f2b8c7ce8728c0d2dc536904e51896bf686df133e76c4a41c22d1f98e
<!-- cmoc-index-kind: file -->

# `repo.py`

## Summary

- Git リポジトリ root の探索と、`cmoc` 実行時に cwd を repo root に固定する共通モジュールです。
- `cmoc/session/*` と `cmoc/apply/*` の branch 判定、session id 抽出、apply worktree path の復元、worktree 参照を扱います。
- `.cmoc` を ignore 対象にする保証、session state JSON / apply process id の読み書きと schema 検証、active session の整合性確認を含みます。
- `git status` / `git diff` / `git check-ignore` / pathspec を使った未コミット差分、削除検出、oracle / implementation ファイル列挙と変更抽出、内部 commit の復元処理をまとめます。

## Read this when

- repo root を見つけて `cmoc` の実行基準ディレクトリを揃えたいとき。
- `session` / `apply` の branch ルール、session id の復元、worktree の場所特定を確認したいとき。
- `.cmoc` の ignore 保証、session state / apply pid の永続化、スキーマ検証、active session の整合性を実装・修正したいとき。
- `oracles` / 実装ファイルの列挙、変更抽出、削除検出、未コミット差分や pathspec commit の扱いを確認したいとき。

## Do not read this when

- `cmoc init` / `session` / `apply` の操作手順や CLI 引数だけを確認したいとき。
- `INDEX.md` の生成ルールや Structured Output の仕様だけを確認したいとき。
- エラーレポート整形や共通例外の仕様だけを確認したいとき。
- タイムスタンプ、ログ保存、計時など他の共通モジュールだけを確認したいとき。

## hash

- 86730c21c41a8fbded798935298ff558ae6885ec3e3609ed7777b5ac5697ecda
<!-- cmoc-index-kind: file -->

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

- サブコマンド呼び出し単位の JSON Lines ログを管理する共通処理への入口です。
- ログ状態の保持、イベント追記、quota 待ち時間の加算、現在のログコンテキスト取得をまとめます。
- ログファイルの作成先を `repo root` 側に寄せつつ、worktree 配下に出力しないための判定と `git info/exclude` 更新も扱います。

## Read this when

- サブコマンド呼び出し単位の JSON Lines ログをどこにどう作るか確認したいとき。
- 現在実行中のサブコマンドログ状態を `ContextVar` で保持し、イベントを追記する実装を確認したいとき。
- `.cmoc/logs/sub_commands/<time-stamp>.jsonl` の作成、排他生成、即時 flush、ログ追記の流れを実装・修正・レビューしたいとき。
- `.cmoc/logs/` を git の未コミット差分にしないための `info/exclude` 更新や、worktree での保存先切り替えを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいときは、この共通ログ処理ではなく該当サブコマンドの仕様を読むべきです。
- `cmoc` のコンソール表示フォーマットだけを確認したいときは、`console_and_file_log.md` を先に読むべきです。
- `codex exec` の呼び出し方や quota 待ちの共通規約だけを確認したいときは、`codex_call.md` を読むべきです。
- `.cmoc` の配置や `INDEX.md` の生成ルールそのものを確認したいときは、このファイルではなく `misc_specs.md` や `indexing.md` を読むべきです。

## hash

- c5363a43ba379d9f913aed453f9a6588296f5b5a2f6d9aa207ef4687eb837977

# `timestamps.py`

## Summary

- `cmoc` 仕様で使う `<time-stamp>` 文字列を生成する共通モジュールです。
- `make_timestamp(now: datetime | None = None) -> str` は、指定された `datetime` または現在のローカル時刻からタイムスタンプを作ります。
- aware な `datetime` はローカルタイムゾーンへ変換し、naive な `datetime` はローカル時刻として扱います。
- 出力形式は `YYYY-MM-DD_HH-MM_SS_mmm` で、年月日時分秒はゼロ埋めし、ミリ秒は `microsecond // 1000` を 3 桁で表現します。

## Read this when

- `<time-stamp>` の文字列生成ルールを確認したいとき
- ローカル時刻と aware / naive `datetime` の扱いを確認したいとき
- ログ名やファイル名に使う時刻文字列の生成実装や、そのテストを書きたいとき

## Do not read this when

- cmoc のサブコマンドごとのタイムスタンプ利用箇所や保存先仕様を調べたいとき
- 日時のパース、UTC 固定、その他の日時ユーティリティを探しているとき
- `INDEX.md` の自動生成や内容ハッシュの管理方法だけを調べたいとき
- コンソール出力、Codex CLI 呼び出し、エラー処理など別の共通実行制御を確認したいとき

## hash

- d680614f3f0ce38c972594ac81fb8ef06663be408f36e822d9fcccb56d43cc51

# `timing.py`

## Summary

- サブコマンド実行中のステップ単位の経過時間を管理し、最後に stdout へ集計表示する共通モジュールです。
- `StepTimer` は開始時刻、現在ステップ、確定済みの各ステップ時間を保持し、`start()` と `finish_current()` で計測区間を区切ります。
- `start_step()` は flat / hierarchical なステップ番号を整形して `step_start` ログと stdout の開始通知を出します。
- `current_timer()`、`report_current_timer()`、`clear_current_timer()` は `ContextVar` 上の現在の計測器を取得・出力・解除します。
- `format_duration()` は秒数を 0.1 秒単位で切り捨て、負値を 0 として固定幅の経過時間文字列に整形します。

## Read this when

- サブコマンドのステップ別の経過時間表示や、完了時の総経過時間表示を実装・修正したいとき。
- `StepTimer` の状態遷移や、`start()`、`finish_current()`、`report()` の関係を確認したいとき。
- 階層化されたステップ番号を含む開始通知の表示形式を確認したいとき。
- 現在の計測器を `ContextVar` 経由で参照・出力・解除したいとき。
- 経過時間の表示フォーマットや、0.1 秒単位への切り捨て、負値の扱いを確認したいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや引数解析だけを確認したいとき。
- ログ保存、`subcommand_log`、`repo` 探索など、経過時間計測以外の共通処理を調べたいとき。
- `INDEX.md` の自動生成や内容ハッシュの規則だけを確認したいとき。
- Python の一般的な時間計測 API や `perf_counter` の詳細だけを知りたいとき。

## hash

- 2dc577ed39e2040ba837ec032afb14e81fd0313520c6969249125b3f858884ea
