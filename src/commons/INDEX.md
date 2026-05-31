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

- `Codex CLI` 呼び出しの共通処理をまとめるモジュールで、`codex exec` のコマンド組み立て、実行、再試行、`resume` 再開を扱います。
- Structured Output の検証、`output-last-message` の読み取り、JSON/テキストの意味検査、起動失敗の診断整形を含みます。
- quota 待機、capacity の指数バックオフ、呼び出しログ保存、`workspace-write` 実行前の oracle 保護と `INDEX.md` メンテナンスも担います。

## Read this when

- `codex exec` の起動方法、`read-only` / `workspace-write` の切り替え、`--model` と `reasoning_effort` の制約を確認したいとき。
- Structured Output の JSON Schema 検証、JSON パース、`output-last-message` の読み取り、テキスト/JSON の意味検証を確認したいとき。
- quota 枯渇時の待機と `resume`、capacity 失敗時の指数バックオフ再試行を追いたいとき。
- 実行前の `INDEX.md` メンテナンスや、workspace-write 時の oracle 保護の挙動を確認したいとき。
- Codex CLI 呼び出しの Markdown フルログ、出力スキーマ保存、再試行時の診断情報の扱いを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解釈や業務ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールそのものや、`oracles` 全体のルーティング方針だけを確認したいとき。
- `repo.py`、`errors.py`、`timing.py`、`timestamps.py` など、他の共通モジュールだけを追いたいとき。
- `codex exec` 以外の CLI 起動制御や、サブコマンド共通ラッパーだけを見たいとき。

## hash

- ded5c5d8fb3023216871ed323188c68fb129a739ad05ef55d4479e03b825993f

# `command_runner.py`

## Summary

- `codex exec` 以外の各 CLI サブコマンドに共通する実行ラッパーをまとめたモジュールです。
- `<repo-root>` の解決、`subcommand_log` の開始、例外の変換、終了コード決定、完了レポート出力を担当します。
- 通常のサブコマンド本体は `Path` を受け取り、`subcommand_log` と `timing` と連携して実行結果を集約します。
- `typer.Exit` と通常例外を分けて扱い、必要に応じて `CmocError` と `format_error_report()` で利用者向けのエラー表示を行います。

## Read this when

- サブコマンドの入口をどこに集約し、共通の実行制御をどう掛けているか確認したいとき。
- 各サブコマンドが `<repo-root>` の `Path` をどう受け取るか確認したいとき。
- 例外時のエラー表示、終了コード、`typer.Exit` への変換規則を見直したいとき。
- 実行ログ、経過時間、待機時間、戻り値の集計出力の流れを追いたいとき。
- `init`、`session`、`apply`、`review` 系のサブコマンドが共通の実行ラッパーをどう使うか確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `<repo-root>` の探索や `.cmoc` の扱いの詳細だけを追いたいときは、このファイルではなく `src/commons/repo.py` を読むべきです。
- エラーメッセージ本文の整形や共通例外の定義そのものを確認したいときは、このファイルではなく `src/commons/errors.py` を読むべきです。
- サブコマンドログや経過時間計測の実装だけを調べたいときは、このファイルではなく `src/commons/subcommand_log.py` と `src/commons/timing.py` を直接読むべきです。
- Codex 呼び出しや `INDEX.md` 生成など、別機能の仕様だけを確認したいとき。

## hash

- 3d90637d9d530863775254d70d4717df41b0f29b19d6b046d60632ce18e5e22e

# `errors.py`

## Summary

- `src/commons/errors.py` は、cmoc 全体で使う共通例外 `CmocError` と stdout 向けのエラーレポート整形関数 `format_error_report()` をまとめるモジュールです。
- `CmocError` は利用者向けメッセージ、複数の次アクション、詳細、終了コードを保持し、次アクションは最低 2 件を必須にします。
- `format_error_report()` は `ERROR` / `Summary` / `Next actions` / `Detail` / `Call stack` 形式で例外を整形し、`CmocError` と通常例外を分けて扱います。

## Read this when

- cmoc 全体で使う共通例外 `CmocError` と、その利用条件を確認したいとき。
- stdout 向けのエラーレポート整形 `format_error_report()` の出力形式を確認・修正したいとき。
- `message`、`actions`、`detail`、`exit_code` の意味や制約、特に `actions` が 2 件以上必要な点を確認したいとき。
- 通常例外や `subprocess.CalledProcessError` をどう診断情報付きで表示するか確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数解析、git 操作、`codex exec` 呼び出しを確認したいとき。
- `format_error_report()` 以外の共通処理、たとえば `repo.py`・`codex.py`・`indexing.py`・`timing.py`・`timestamps.py` を確認したいとき。
- テストコードや CLI エントリーポイントの実装を追いたいとき。

## hash

- 4e9b2d98720b30ea3d87e385d451e3fa2a63918c22757b629c57c87093b50048

# `indexing.py`

## Summary

- `INDEX.md` のメンテナンス本体を担う共通モジュールです。
- 対象ディレクトリの列挙、既存目次の再利用判定、目次ブロックの生成・更新・置換、自動コミットまでをまとめています。
- `.gitignore`、`memo`、隠し要素、`build` / `tmp` / `__pycache__`、symlink、バイナリを除外して目次対象を決めます。
- Codex CLI の Structured Output で目次項目を生成し、既存 `INDEX.md` の構文検査、更新判定、メンテナンス用 lock、I/O エラー変換も担当します。

## Read this when

- `INDEX.md` の自動生成、再生成、更新、自動コミットの挙動を確認したいとき。
- ディレクトリ列挙、`.gitignore` 判定、`memo` 除外、隠し要素や `build` / `tmp` / `__pycache__` の除外条件を追いたいとき。
- 既存 `INDEX.md` の再利用条件、内容ハッシュによる更新判定、Structured Output から Markdown への変換を確認したいとき。
- `INDEX` メンテナンス用の lock や、I/O 失敗を `CmocError` に変換する処理を確認したいとき。

## Do not read this when

- `INDEX.md` の配置ルールの概要だけを確認したいとき。
- `codex.py`、`repo.py`、`errors.py` など他の共通モジュールの仕様を確認したいとき。
- 個別サブコマンドの引数や実行フローだけを確認したいとき。

## hash

- 5b5c30ac20feb3db91d24a5b767e13d1564f3cb8808ebe0fcc08d52a2e33a7fe

# `repo.py`

## Summary

- `src/commons/repo.py` は、git リポジトリと cmoc の作業領域を扱う共通基盤モジュールです。
- repo root の探索、現在ブランチ名と HEAD commit の取得、cmoc 管理ブランチの判定と session id 抽出をまとめています。
- session / apply の状態ファイルと apply process id の保存・読込・検証、active session の整合性確認を担います。
- `.cmoc` の ignore 保証、未コミット差分の検査、`oracles` と実装ファイルの列挙・差分抽出・削除判定、`run_git()` を含む git 共通ラッパーを提供します。

## Read this when

- repo root の検出、現在ブランチ名、HEAD commit の取得方法を確認したいとき。
- `cmoc/session/*` と `cmoc/apply/*` のブランチ命名規則や、session id の抽出処理を追いたいとき。
- session state と apply process id の保存・読込・検証、active session の整合性確認を確認したいとき。
- apply worktree から所有元 repo root を復元する処理や、`.cmoc` の ignore 保証を確認したいとき。
- root `.gitignore` と git index を使った未コミット差分・削除検出、`oracles` と実装ファイルの列挙やフィルタリングを追いたいとき。

## Do not read this when

- `src/commons/repo.py` の個々の関数実装や細部の例外メッセージを確認したいときは、本文を直接読むべきです。
- `INDEX.md` の生成・更新ルールそのものを確認したいときは、`src/commons/indexing.py` を読むべきです。
- `CmocError` の整形や stdout 向けエラーレポートだけを確認したいときは、`src/commons/errors.py` を読むべきです。
- 経過時間計測やサブコマンドログだけを追いたいときは、`timing.py` や `subcommand_log.py` を読むべきです。
- `codex exec` の起動や Structured Output の扱いだけを確認したいときは、この文書の範囲外です。

## hash

- fc5052391ab23aa18cd4e4ef0d5658c02f1afa869173bcbab7a9057af7f384b4

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

- `src/commons/subcommand_log.py` は、サブコマンド呼び出し単位の JSON Lines ログを管理する共通処理の入口です。
- `SubcommandLogContext` で現在状態を保持し、`log_event()` と `add_quota_wait()` でイベント追記と quota 待ち時間の記録を行います。
- ログファイルは `<repo-root>/.cmoc/logs/sub_commands/` 配下に排他的に作成され、apply worktree や linked worktree では保存先の repo root を解決して集約します。
- `subcommand_log()` は開始イベントを書き込み、コンソールに開始メッセージを出したうえで呼び出し本体へ制御を渡します。

## Read this when

- サブコマンド呼び出しごとの JSON Lines ログをどこに、どう作るか確認したいとき。
- 現在のサブコマンドログ状態を `ContextVar` で保持し、イベントを追記する流れを追いたいとき。
- `.cmoc/logs/sub_commands/<time-stamp>.jsonl` の排他的作成、即時 flush、開始イベント出力を確認したいとき。
- `.cmoc/logs/` を git の未コミット差分にしないための `info/exclude` 更新や、apply worktree からの保存先切り替えを確認したいとき。
- quota 待ち時間の加算がログへどう反映されるか確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを追いたいとき。
- `codex exec` の呼び出し方法や Structured Output の仕様だけを確認したいとき。
- エラーレポートの整形や `CmocError` の出力形式だけを確認したいとき。
- `INDEX.md` の生成・更新ルールや、他の共通モジュールの仕様だけを見たいとき。

## hash

- 1ddbe918d0fbc7c65e6ff8d3a935be20d20d0a460f7a8824e35721ba54d00b4f

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
- `current_timer()`、`report_current_timer()`、`clear_current_timer()` などの現在の計測器管理を追いたいとき。
- `format_duration()` の stdout 向け表示や、0.1 秒単位の切り捨て規則を確認したいとき。

## Do not read this when

- サブコマンド本体の引数解析や業務ロジックだけを確認したいとき。
- `codex exec` の起動制御、Structured Output、`INDEX.md` メンテナンスそのものを確認したいとき。
- タイムスタンプ生成やサブコマンドログ保存だけを調べたいときは、`timestamps.py` や `subcommand_log.py` を読むべきです。
- `StepTimer` 以外の共通例外、repo 探索、ファイルレポート保存を確認したいとき。

## hash

- da12b431690040219484b33d51f4d6c45f488289b91d04f383232107820071fd
