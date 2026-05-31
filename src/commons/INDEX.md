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

- `Codex CLI` 呼び出しの共通起動基盤で、`codex exec` のコマンド組み立て、実行、再試行、`resume` 再開をまとめるモジュールです。
- Structured Output の schema 検証、JSON パース、`output-last-message` の読み取り、テキスト/JSON の意味検証を扱います。
- quota 待機、capacity の指数バックオフ、呼び出しログ保存、`workspace-write` 時の oracle 保護と実行前の `INDEX.md` メンテナンスも含みます。

## Read this when

- `codex exec` の起動方法、`read-only` / `workspace-write` の切り替え、`--model` や `reasoning_effort` の制約を確認したいとき。
- Structured Output の JSON Schema 検証、`output-last-message` の保存と読み取り、JSON 応答の意味検証を確認したいとき。
- quota 枯渇時の待機と `resume`、capacity 失敗時の指数バックオフ再試行を追いたいとき。
- 実行前の `INDEX.md` メンテナンスや、workspace-write 時の oracle 保護の挙動を確認したいとき。
- Codex CLI 呼び出しの Markdown フルログと output schema の保存規則を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールそのものや、`oracles` 全体のルーティング方針だけを確認したいとき。
- `repo.py`、`errors.py`、`timing.py`、`timestamps.py` など他の共通モジュールだけを追いたいとき。
- `codex exec` 以外の CLI 起動制御や、サブコマンド共通ラッパーだけを見たいとき。

## hash

- 0254deddb70cd770630f08d6f57e931eab0f7cc3024291a40816a52ef8dc49ce

# `command_runner.py`

## Summary

- Typer サブコマンドの共通実行ラッパーで、`<repo-root>` の解決、`subcommand_log` の開始、例外変換、終了コード確定をまとめる。
- 通常のサブコマンド本体を `Path` 受け取りに統一し、`typer.Exit`、通常例外、`CmocError` を分けて stdout のエラーレポートと終了集計を出す。
- 実行完了時に `log_event()`、`report_current_timer()`、`format_duration()`、`clear_current_timer()` を使ってログと経過時間を集約する。

## Read this when

- サブコマンドの共通入口がどこで `repo root` を解決し、どう本体へ渡すか確認したいとき。
- `typer.Exit`、通常例外、`CmocError` の扱いと、非 0 終了時のレポート出力規則を確認したいとき。
- 実行ログ、`quota` 待ち時間、経過時間、終了コードの最終集計を追いたいとき。
- `run_command()` を使うサブコマンドを実装・修正するとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `<repo-root>` 探索や `.cmoc` の状態管理の詳細を追いたいときは `repo.py` を読むべきです。
- エラーメッセージの整形仕様そのものを確認したいときは `errors.py` を読むべきです。
- サブコマンドログや時間計測の実装だけを確認したいときは `subcommand_log.py` と `timing.py` を読むべきです。

## hash

- a21c1222e282f147389a35cb8a6bedab12da3431dc4c134af4bd2ed09b37a35a

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
- ディレクトリ列挙、`gitignore` 判定、`memo` 除外、隠しディレクトリや `build` / `tmp` / `__pycache__` の除外条件を追いたいとき。
- 既存 `INDEX.md` の再利用条件、内容ハッシュによる更新判定、Structured Output から Markdown への変換を確認したいとき。
- INDEX メンテナンス用の lock や、I/O 失敗を `CmocError` に変換する処理を確認したいとき。

## Do not read this when

- `INDEX.md` の配置ルールの概要だけを確認したいとき。
- `codex.py`、`repo.py`、`errors.py` など他の共通モジュールの仕様を確認したいとき。
- 個別サブコマンドの引数や実行フローだけを確認したいとき。

## hash

- f932aa99e0d198d42cbbfd440816bc39cb455a23b0eb7414f3a069e1eea93c6b

# `repo.py`

## Summary

- `src/commons/repo.py` は、git リポジトリと cmoc 作業領域を扱う共通基盤モジュールです。
- repo root 検出、branch / commit 取得、`cmoc/session/*` と `cmoc/apply/*` の判定、session/apply state のパスと読み書き・検証をまとめています。
- `.cmoc` の ignore 保証、active session の整合性確認、oracle / implementation ファイルの列挙、差分収集、内部 commit の補助処理まで担います。

## Read this when

- repo root の探索、`cwd` の固定、現在の branch 名や `HEAD` commit を取得したいとき。
- `cmoc/session/*` と `cmoc/apply/*` の branch 判定、session id 復元、apply worktree 配置の復元を確認したいとき。
- session/apply state JSON の保存・読込・検証、active session の一意性確認、process id の runtime 保存を確認したいとき。
- `.cmoc` の ignore 保証、未コミット差分の検査、oracle / 実装ファイルの列挙や差分抽出、内部 commit の補助処理を追いたいとき。

## Do not read this when

- 個別サブコマンドの引数解釈や処理順だけを確認したいときは、このファイルではなく `src/sub_commands/...` 側を読むべきです。
- `codex exec` の起動、ログ、計測、エラー整形、`INDEX.md` 生成などの共通処理を確認したいときは別の `commons` モジュールを読むべきです。
- `session` や `apply` の利用手順、状態遷移の仕様断片だけを見たいときは、`oracles/docs/app_specs/sub_commands/` 側を参照すべきです。

## hash

- 2e82d1dde7ade3054d31fcd1eb087af29379048b221d691da1d527603e7fcf89

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

- `src/commons/subcommand_log.py` は、サブコマンド呼び出しごとの JSON Lines ログを管理する共通処理の入口です。
- `SubcommandLogContext` で現在のログ状態を保持し、`log_event()` と `add_quota_wait()` でイベント追記と quota 待ち時間の加算を行います。
- ログファイルは repo root 側の `.cmoc/logs/sub_commands/` に作成され、worktree 配下に出力しないための判定と `git info/exclude` 更新もこのモジュールが担います。
- `subcommand_log()` はログ開始時にコンテキストを設定し、開始イベントとコンソール表示を出したうえで呼び出し本体へ制御を渡します。

## Read this when

- サブコマンド呼び出し単位の JSON Lines ログをどこに、どう作るか確認したいとき
- 現在実行中のサブコマンドログ状態を `ContextVar` で保持し、イベントを追記する実装を確認したいとき
- `.cmoc/logs/sub_commands/<time-stamp>.jsonl` の作成、排他生成、即時 flush の流れを実装・修正・レビューしたいとき
- `.cmoc/logs/` を git の未コミット差分にしないための `info/exclude` 更新や、worktree での保存先切り替えを確認したいとき
- quota 待ち時間の加算と、その記録がサブコマンドログへどう反映されるかを確認したいとき

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを追いたいとき
- コンソール表示やエラーレポートの整形だけを確認したいとき
- `codex exec` の呼び出し方や Structured Output の仕様だけを確認したいとき
- `INDEX.md` の生成ルールや他の共通仕様だけを確認したいとき

## hash

- e7d00e3d3c4701e80a0c2dcdfa842b3571d02d7b8e29fecd2f66baab847c3c6f

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
