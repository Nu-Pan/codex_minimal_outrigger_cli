# `__init__.py`

## Summary

- `src.commons` パッケージを宣言するだけの最小モジュールです。
- 公開 API、定数、再エクスポート、実行ロジックは持ちません。

## Read this when

- `src.commons` が Python パッケージとして宣言されていることを確認したいとき。
- `<work-root>/src/commons` の入口として、最小限の役割だけを把握したいとき。
- 共通モジュール群の詳細に進む前に、パッケージの存在確認だけを行いたいとき。

## Do not read this when

- `src.commons` 配下の実装詳細や共通ユーティリティの振る舞いを確認したいとき。
- `codex exec` 呼び出し、repo/worktree 解決、エラー整形、ログ、インデクシングなどの具体的な処理を追いたいとき。
- パッケージ宣言の確認だけで足り、追加の公開 API や実行ロジックが不要なとき。

## hash

- ff1b23adb7b4c5a75686ac97283d2065d5cacc8861143f25677b559abeb6e2d0

# `codex.py`

## Summary

- Codex CLI 呼び出しの共通基盤で、`codex exec` のコマンド組み立て・実行・再試行・`resume` 再開をまとめる。
- Structured Output の JSON Schema 検証、JSON / text の意味検査、最後のメッセージ読取とログ出力を扱う。
- quota 枯渇時の復旧待機、capacity エラーの指数バックオフ、workspace-write 時の oracle 保護と `INDEX.md` 事前メンテナンスも含む。

## Read this when

- `codex exec` の呼び出し順、再試行条件、`resume` の扱いを追いたいとき。
- Structured Output の schema 検証や、JSON / text のバリデーション結果を確認したいとき。
- quota 待機、capacity リトライ、起動失敗診断、呼び出しログや last message の保存仕様を見たいとき。
- workspace-write 実行前の oracle 保護や `INDEX.md` メンテナンス前処理の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `repo.py`、`errors.py`、`timing.py`、`timestamps.py` など他の共通モジュールだけを確認したいとき。
- `INDEX.md` の生成ルールそのものや、`oracles` 側の正本仕様だけを確認したいとき。
- `codex exec` 以外の CLI 起動経路や補完処理だけを追いたいとき。

## hash

- 5ce6f881df7f005630be813bc8c1ced11f18e1fab293db95d81c98c3d8a282b7

# `command_runner.py`

## Summary

- `<work-root>/src/commons/command_runner.py` は、cmoc の各サブコマンドを共通実行するラッパーで、repo root 解決、ログ開始、例外整形、完了集計をまとめるモジュールです。
- `run_command()` はサブコマンド本体に `<repo-root>` の `Path` を渡し、整数戻り値、`typer.Exit`、通常例外を共通規則で終了コードへ変換します。
- 実行終了時には `subcommand_end` ログを書き、総経過時間、quota 待ち時間、戻り値を stdout の完了レポートとして出力します。

## Read this when

- `cmoc init` / `session` / `apply` / `review` などの入口が、どの共通実行処理で包まれているかを確認したいとき。
- サブコマンド本体が `Path` を受け取り、戻り値や例外が終了コードへどう反映されるかを見直したいとき。
- `enter_repo_root()`、`subcommand_log`、`format_error_report()`、`report_current_timer()` の呼び出し順を追いたいとき。
- 非 0 の `typer.Exit` や通常例外が利用者向けのエラーレポートになる流れを確認したいとき。
- 完了サマリーや `subcommand_end` ログに何が出るかを確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数解析だけを確認したいとき。
- `<repo-root>` の探索や `.cmoc` 管理の詳細だけを追いたいときは、`<work-root>/src/commons/repo.py` を読むべきです。
- エラーメッセージの型や Markdown 形式の整形規則だけを見たいときは、`<work-root>/src/commons/errors.py` を読むべきです。
- JSONL ログの保存や経過時間計測の実装だけを見たいときは、`<work-root>/src/commons/subcommand_log.py` と `<work-root>/src/commons/timing.py` を読むべきです。

## hash

- 2183c4c608e64b3411b8fde23b9048fe84f439e849ea5d7561d1cb7548ac929c

# `errors.py`

## Summary

- `<work-root>/src/commons/errors.py` は、cmoc 全体で共通に使う例外型 `CmocError` と、エラーレポート整形関数 `format_error_report()` をまとめるモジュールです。
- `CmocError` は利用者向けメッセージ、複数の次アクション、詳細、終了コードを保持し、次アクションは最低 2 件を必須にします。
- `format_error_report()` は `ERROR` / `Summary` / `Next actions` / `Detail` / `Call stack` 形式で Markdown を生成し、通常例外と `CmocError` を分けて扱います。

## Read this when

- cmoc 全体で使う共通例外 `CmocError` の構造、制約、利用条件を確認したいとき。
- 標準例外と `CmocError` を含むエラーレポートの Markdown 形式や、`subprocess.CalledProcessError` の診断情報の整形方法を確認したいとき。
- `message`、`actions`、`detail`、`exit_code` の意味や、`actions` が 2 件以上必須である制約を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析、git 操作、`codex exec` 呼び出しなど、エラー整形以外の業務ロジックを追いたいとき。
- `repo.py`、`codex.py`、`indexing.py`、`timing.py`、`timestamps.py` など、他の共通モジュールの実装を確認したいとき。
- CLI の入口実装やテストコードを確認したいとき。

## hash

- 8e200a8f193254d60a14f5824ccebbacaece04d8fe6497633d460dcec7ac3d19

# `indexing.py`

## Summary

- `<work-root>/src/commons/indexing.py` は `INDEX.md` の生成、再生成、整合性検査をまとめる共通モジュールです。
- .gitignore、`memo`、隠し要素、symlink、バイナリを除外し、既存 `INDEX.md` は再利用可否を判定して差分がなければ書き換えません。
- Structured Output の JSON schema 検証、排他ロック、原子的な置換、自動コミット、不整合チェックまで扱います。
- `is_maintained_index_path*` と `find_index_inconsistencies` で、どの `INDEX.md` が管理対象かを判定できます。

## Read this when

- `INDEX.md` の生成・更新・再生成ルールを変更したいとき。
- 配置対象や目次対象の除外条件、`.gitignore` 判定、バイナリ判定、symlink の扱いを確認したいとき。
- 既存 `INDEX.md` の再利用条件、Structured Output 検証、排他ロック、原子的な置換、自動コミットの流れを追いたいとき。
- 特定の相対 path が cmoc の管理対象 `INDEX.md` かどうか、または不整合があるかを判定したいとき。

## Do not read this when

- `cmoc indexing` の CLI 引数やコマンド入口だけを確認したいときは、`<work-root>/src/sub_commands/indexing.py` を読むべきです。
- `INDEX.md` の正本仕様や利用手順だけを確認したいときは、`<work-root>/oracles/docs/app_specs/indexing.md` を読むべきです。
- `INDEX.md` 生成の回帰条件だけを追いたいときは、`<work-root>/tests/test_indexing.py` を読むべきです。
- `<work-root>/src/commons` の他の共通処理だけを確認したいときは、このファイルではなく該当モジュールを読むべきです。

## hash

- 8a6f09771b557e5258e70c68604bbca5885b9ef8697ea167a66f1de334f5fb65

# `repo.py`

## Summary

- `<work-root>/src/commons/repo.py` は git リポジトリと cmoc 作業領域を扱う共通基盤モジュールです。
- repo root 探索、ブランチ判定、session / apply state 管理、apply process id の保存・読込、`.cmoc` 追跡外保証をまとめています。
- `oracles` と実装ファイルの列挙や変更検出、`.gitignore` の評価・復元補助、`git` 呼び出しの共通ラッパーも含みます。

## Read this when

- repo root の探索、現在ブランチ名、HEAD commit、cmoc 予約ブランチ判定を確認したいとき。
- session / apply state の保存・読込・検証や、session home branch の復元ロジックを確認したいとき。
- apply process id の runtime file、worktree path の復元、`.cmoc` の追跡外保証、未コミット差分の検査を確認したいとき。
- `oracles` と実装ファイルの列挙・絞り込み、変更済みファイルの収集、`git` 呼び出しの共通ラッパーを確認したいとき。

## Do not read this when

- `CmocError` の整形や `codex exec` など、repo 以外の共通基盤だけを確認したいとき。
- サブコマンド固有の引数解析や業務ロジックだけを追いたいとき。
- `INDEX.md` の生成ルールや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 179f21ed46d437277bb38c080784a7b78b84e339cc34ef993081027bcb53d92a

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

- `<work-root>/src/commons/subcommand_log.py` は、cmoc のサブコマンド呼び出しごとの JSON Lines ログを作成・追記する共通モジュールへの入口です。
- `SubcommandLogContext` と `ContextVar` による現在のログ状態管理、イベント記録、quota 待ち時間の集計、標準出力との同時書き込み制御を扱います。
- ログ保存先の repo root 解決、`<repo-root>/.cmoc/logs/sub_commands/` への一意なタイムスタンプ保存、`<work-root>/.cmoc/logs/` の git 除外設定まで含みます。

## Read this when

- サブコマンド呼び出し単位の JSON Lines ログの保存先、作成順序、追記方法を確認したいとき。
- `ContextVar` を使ったログ状態管理、イベント記録、quota 待ち時間の集計の流れを追いたいとき。
- apply worktree や linked worktree から実行したときの保存先 repo root の解決方法を知りたいとき。
- 起動時の開始イベント、コンソール見出し、ログファイルパス表示、並行出力時のロック処理を確認したいとき。
- <work-root>/.cmoc/logs/` を git の追跡対象外にする挙動を確認したいとき。

## Do not read this when

- `<work-root>/src/commons` 全体の役割分担や、他の共通モジュールの入口だけを確認したいとき。
- `command_runner.py` や `timing.py` など、サブコマンド実行の共通処理本体を追いたいとき。
- `repo.py` の repo root 探索や `.cmoc` 管理、`timestamps.py` のタイムスタンプ生成だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 473dc7e0137054f0fabef4eea13883542cfe3c68beabb5cf007eb5f38e22dc8f

# `timestamps.py`

## Summary

- `<work-root>/src/commons/timestamps.py` は cmoc 仕様の `<time-stamp>` 文字列生成と判定をまとめた共通モジュールです。
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

- `StepTimer` がサブコマンド全体と各ステップの開始・終了時刻を記録し、親子関係を保ったまま完了サマリーを出力します。
- `start_step()` が step 番号を `i/N` または階層化表記に整形し、`subcommand_log` へ `step_start` を記録して stdout に見出しを出します。
- `current_timer()` / `report_current_timer()` / `clear_current_timer()` で `ContextVar` ベースの現在の計測器を管理します。
- `format_duration()` が経過秒を 0.1 秒単位で切り捨てた固定幅の `h/m/s` 形式に整形します。

## Read this when

- サブコマンドのステップ時間表示や、完了サマリーの出力順を確認したいとき。
- 階層化された step index の扱いと、親ステップをどのタイミングで終了するかを追いたいとき。
- `step_start` ログや stdout の見出しがどう組み立てられるか確認したいとき。
- 時間の表示幅・切り捨て規則を確認したいとき。
- 現在の計測器の取得・破棄・自動出力の流れを確認したいとき。

## Do not read this when

- サブコマンド実行の共通入口、終了コード変換、例外整形を確認したいときは `command_runner.py` や `errors.py` を読むべきです。
- タイムスタンプ文字列そのものの生成や検証を確認したいときは `timestamps.py` を読むべきです。
- サブコマンドログの保存先や JSONL 記録仕様を確認したいときは `subcommand_log.py` を読むべきです。
- repo/worktree 解決や `.cmoc` 管理を確認したいときは `repo.py` を読むべきです。

## hash

- 822869d260c24c976ead0ecc66a80a76f2267fe39cbad09b80b426f42b996474
