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

- Codex CLI 呼び出しの共通ラッパー。
- Structured Output 検証、quota 待機再開、実行ログ保存をまとめて扱う。
- `codex exec` のコマンド組み立てと補助関数群を収録する。

## Read this when

- `codex exec` を起動する共通処理を実装・修正するとき
- Structured Output の JSON Schema 保存・検証・再試行の流れを確認したいとき
- quota 枯渇時の待機・再開、`--resume`、`--output-last-message`、ログ保存の挙動を追いたいとき
- model / reasoning effort の制約や `codex exec` の実行オプションを確認したいとき

## Do not read this when

- Codex CLI の呼び出しや出力検証とは無関係な機能を変更するとき
- `codex.py` 以外の共通処理や別サブコマンドの実装だけを確認したいとき
- INDEX.md の維持や他ディレクトリのルーティングだけを更新したいとき

## hash

- 9e13bc369f3a0e79e1528a69323ee133fb15824e98be327f2232104278ec1c29

# `command_runner.py`

## Summary

- Typer から呼ばれるサブコマンド共通の実行ラッパーをまとめるモジュールです。
- `enter_repo_root()` で `<repo-root>` を解決し、その `Path` を各サブコマンド本体に渡して実行します。
- `typer.Exit` と通常例外を共通方針で終了コード化し、必要に応じて `format_error_report()` で利用者向けレポートを出します。
- `subcommand_log` と `timing` と連携して、サブコマンド全体の経過時間、待機時間、戻り値を最後に出力します。
- サブコマンド本体を薄く保ち、実行制御・エラー処理・集計出力を `commons` 側へ集約する役割を持ちます。

## Read this when

- サブコマンドの入口をどこに集約しているか、共通の実行制御を確認したいとき。
- 各サブコマンドが `<repo-root>` の `Path` をどのように受け取るか確認したいとき。
- 例外時の共通エラー表示、終了コードの決定、`typer.Exit` への変換規則を確認したいとき。
- サブコマンド実行時のログ、経過時間、待機時間、戻り値出力の流れを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを調べたいとき。
- `<repo-root>` の探索ロジックや `.cmoc` の扱いを詳しく確認したいとき。
- エラーメッセージの整形内容や例外クラス定義そのものを詳しく確認したいとき。
- Codex CLI 呼び出し、Structured Output、INDEX.md 生成などの別機能を調べたいとき。

## hash

- d6133db4b6e0d0dfd6673433b4c89b471d97c333023549da4d5087119edd4801

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

- 個別サブコマンドの業務ロジック、引数解析、git 操作、`codex exec` 呼び出しを調べたいとき。
- ログ保存、リトライ、Structured Output、サンドボックス指定など、別の共通機能だけを調べたいとき。
- タイムスタンプ生成、経過時間表示、サブコマンドログなど、他の共通ユーティリティを調べたいとき。
- テスト実装の詳細や Fake Codex CLI の使い方だけを確認したいとき。

## hash

- d4b9943ebba58c28cfcb04b0c1a4971b63391ac36f12740d38c1381392381b97

# `indexing.py`

## Summary

- `src/commons/indexing.py` は `<repo-root>` 配下の `INDEX.md` を列挙・再生成・更新し、必要なら自動コミットするための共通モジュールです。
- 配置対象ディレクトリと直下項目を、`memo`、隠し項目、`build` / `tmp` / `__pycache__`、`gitignore` 対象、バイナリらしいファイルを除外しながら判定します。
- 既存の `INDEX.md` から再利用可能な目次ブロックを解析し、ハッシュ一致かつ形式が妥当なら再生成を避けます。
- 新規生成時は Codex CLI を Structured Output 付きで呼び出し、JSON を検証して Markdown の目次ブロックへ変換します。

## Read this when

- `INDEX.md` をどのディレクトリに配置し、どの項目を目次生成対象にするか確認したいとき。
- `maintain_indexes` の処理順、既存 `INDEX.md` の再利用条件、自動コミットの流れを確認したいとき。
- `memo`、隠しディレクトリ、`build`、`tmp`、`__pycache__`、`gitignore` 対象、バイナリファイルの除外規則を確認したいとき。
- INDEX 生成用の Codex CLI プロンプト、Structured Output schema、JSON 検証、Markdown 変換処理を変更したいとき。

## Do not read this when

- 個別サブコマンドの CLI 引数、ユーザー向け出力、終了ステータスだけを調べたいとき。
- Codex CLI 呼び出しの汎用ラッパー、JSON パース、モデル定数の詳細だけを調べたいとき。
- git コミット処理や `.gitignore` 更新、repo root 検出など、INDEX 以外の共通処理だけを確認したいとき。
- 特定の `INDEX.md` 目次本文だけを読みたい場合で、生成・更新ロジックを追う必要がないとき。

## hash

- 9f2cd7fa5e47f1b14ba861bc76ef7a9a3743ab8dfd6338bc9b0aec3a1fbe75a9

# `repo.py`

## Summary

- git リポジトリのルート探索、`cwd` 固定、`git` 実行の共通ラッパーをまとめたモジュールです。
- 現在ブランチ名、`HEAD` commit、cmoc 管理ブランチ判定、`session state` の読み書きと参照を扱います。
- .cmoc` の追跡除外保証、root `.gitignore` の判定、未コミット差分や pathspec 単位の clean 判定を提供します。
- oracle / 実装ファイルの列挙、変更・削除検出、一時 index を使った commit と index 復元までを担います。

## Read this when

- `cmoc` が使う git リポジトリのルート探索や、`cwd` をルートへ固定する処理を確認・修正したいとき。
- 現在ブランチ名、`HEAD` commit、`cmoc/session/<session-id>` や `cmoc/apply/<session-id>/<apply-run-id>` の判定、session id 抽出を扱いたいとき。
- `.cmoc/sessions` の session state の読み書き、`cmoc session fork` 直後の初期状態、session start commit の参照を確認したいとき。
- `.cmoc` を追跡対象外に保つ保証、root `.gitignore` の判定、未コミット差分の検査や pathspec ごとの clean 判定を実装したいとき。
- oracle ファイルや実装ファイルの列挙、変更・削除検出、untracked も含めた差分収集、`INDEX.md` 自動更新前後の差分管理を追いたいとき。
- `commit_if_changed` や `commit_cmoc_initialization_changes` のように、対象パスだけを一時 index で commit し、その後に既存の staged 差分を復元する挙動を確認したいとき。

## Do not read this when

- `cmoc` の CLI 引数解析や画面出力だけを確認したいときは、この共通処理ではなく各サブコマンド側を読むべきです。
- `commons.errors`、`commons.indexing`、`commons.subcommand_log`、`commons.timing` など、別の共通モジュールだけを追いたいときはこのファイルを読む必要はありません。
- `oracles` 側の正本仕様や `INDEX.md` 生成ルールそのものだけを確認したいときは、`oracles` 配下の該当文書を読むべきです。
- git リポジトリ探索、ブランチ判定、session state、差分列挙、pathspec commit の流れに関心がない場合は、このファイルは不要です。

## hash

- a65e99cc41639d0cf7c96e001e7d2008169e27c79c8523624a356e4f13788c14

# `subcommand_log.py`

## Summary

- `src/commons/subcommand_log.py` は、各サブコマンド実行の標準出力と標準エラー出力をコンソールと `<repo-root>/.cmoc/logs/sub_commands/<time-stamp>.log` の両方へ tee する共通ログ管理モジュールです。
- `SubcommandLogContext` と `current_subcommand_log()` で現在のサブコマンドログ状態を共有し、`add_quota_wait()` で quota 回復待ち時間を累積できます。
- `subcommand_log()` は一意なログファイル作成と開始メッセージ表示を担い、`_ensure_logs_excluded()` は `.git/info/exclude` を更新して `.cmoc/logs/` が未コミット差分にならないようにします。

## Read this when

- サブコマンドの標準出力と標準エラー出力をコンソールとログファイルへ同時保存する仕組みを確認したいとき。
- 現在実行中のサブコマンドのログ状態や、quota 回復待ち時間の加算方法を確認したいとき。
- ログファイルの保存先、ファイル名の払い出し方法、開始時に表示される相対パスのメッセージを確認したいとき。
- `logs/` をサブコマンド自身の差分として扱わないための除外設定の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数解析だけを確認したいとき。
- `INDEX.md` の自動生成や更新ルールだけを確認したいとき。
- タイムスタンプ生成や経過時間表示など、別の共通ユーティリティを調べたいとき。
- エラー整形や共通エラーハンドリング全体だけを調べたいとき。

## hash

- ee836b6e43a710666e30a2c70dbf7817ef3a2ffbcc6da3fd36a3401e5690ed5e

# `timestamps.py`

## Summary

- `cmoc` 仕様で使う `<time-stamp>` 文字列を生成する共通モジュールです。
- `make_timestamp(now: datetime | None = None) -> str` は、指定された `datetime` または現在のローカル時刻からタイムスタンプを作ります。
- aware な `datetime` はローカルタイムゾーンへ変換し、naive な `datetime` はローカル時刻として扱います。
- 出力形式は `YYYY-MM-DD_HH-MM_SS_mmm` で、年月日時分秒はゼロ埋めし、ミリ秒は `microsecond // 1000` を 3 桁で表現します。

## Read this when

- `<time-stamp>` の文字列生成ルールを確認したいとき。
- ローカル時刻と aware / naive `datetime` の扱いを確認したいとき。
- ログ名やファイル名に使う時刻文字列の生成実装や、そのテストを書きたいとき。

## Do not read this when

- cmoc のサブコマンドごとのタイムスタンプ利用箇所や保存先仕様を調べたいとき。
- 日時のパース、UTC 固定、その他の日時ユーティリティを探しているとき。
- `INDEX.md` の自動生成や内容ハッシュの管理方法だけを調べたいとき。
- コンソール出力、Codex CLI 呼び出し、エラー処理など別の共通実行制御を確認したいとき。

## hash

- bf17be3874ec3ab0c88d7652c9869ca7c9b7b5554037dbc60f26117a2287a391

# `timing.py`

## Summary

- `src/commons/timing.py` は、サブコマンドのステップ単位の経過時間を記録・表示する共通モジュールです。
- `StepTimer` はサブコマンド全体の開始時刻、現在のステップ名、確定済みステップの経過時間を保持し、`start()` で直前ステップを確定して次のステップを開始します。
- `report()` は未確定の最後のステップも含めて、各ステップの経過時間と全体の経過時間を stdout に出力します。
- `current_timer()`、`report_current_timer()`、`clear_current_timer()` は `ContextVar` を使って現在の計測器を参照・出力・解除します。
- `format_duration()` は秒数を 0.1 秒単位で切り捨て、負値を 0 として ` 0h  0m  0.0s` 形式に整形します。

## Read this when

- 各サブコマンドのステップ別タイミング表示や総経過時間表示を実装・修正したいとき。
- `StepTimer` の状態遷移や、`start()`・`report()`・`finish_current()` の関係を確認したいとき。
- 実行中の現在の計測器を取得したい、最後にまとめて出力したい、参照を消したいとき。
- 経過時間の表示フォーマット、0.1 秒単位への切り捨て、負値の扱いを確認したいとき。
- タイミングレポートの stdout 出力形式や `command_name` の使われ方を確認したいとき。

## Do not read this when

- 各サブコマンド固有の業務ロジックだけを追いたいとき。
- Codex CLI 呼び出し、ログ保存、Structured Output、リトライなど `timing.py` 以外の共通処理を調べたいとき。
- `INDEX.md` の自動生成や内容ハッシュの規則を調べたいとき。
- `repo` 探索、oracle 列挙、ブランチ操作など、タイミング以外の共通機能を探したいとき。
- Python の一般的な時間計測 API や `perf_counter` の詳細仕様だけを知りたいとき。

## hash

- 9c0e3bd7f64b020379aadcc0e747d1b0c90c0678b2bd2a27efd4db0f4ff58175
