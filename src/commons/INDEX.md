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

- `codex exec` の共通ラッパーで、コマンド組み立て、実行、`--output-last-message` を含むログ保存、`--resume` 再開、quota 待機をまとめるモジュールです。
- Structured Output の `--output-schema` ファイル生成・キャッシュ、JSON パース、JSON Schema 検証、意味検査を扱います。
- workspace-write 実行時の `oracles` 改変検査と、`INDEX.md` メンテナンス前処理を担います。
- model と reasoning effort の制約、quota ポーリング、ログの Front Matter 書き出し補助も含みます。

## Read this when

- `codex exec` の実行、sandbox 切り替え、`--output-last-message` / `--output-schema` / `--resume` の扱いを確認したいとき。
- Structured Output の JSON Schema 保存・検証、JSON パース、意味検査、リトライの流れを見直したいとき。
- quota 枯渇時のポーリング待機・再開、`oracles` 保護、`INDEX.md` メンテナンス前処理を追いたいとき。
- `codex exec` の呼び出しログ、実行メッセージ、schema ファイル名の決め方を確認したいとき。

## Do not read this when

- `codex exec` と無関係な CLI ルーティングや、サブコマンド本体の業務ロジックだけを確認したいとき。
- 共通エラーレポート、`<repo-root>` 探索、タイムスタンプ生成、経過時間表示など、別の `src/commons` モジュールで足りるとき。
- ファイル操作やテスト実装だけを確認したいとき。
- `oracles` の正本仕様そのものを確認したいときは、このモジュールではなく `oracles` 配下を直接読むべきです。

## hash

- ae009dc7a50796fbe8d663b0e5f6bfd845fa036175bc13976d45908742285ce6

# `command_runner.py`

## Summary

- Typer から呼ばれるサブコマンド共通の実行ラッパーをまとめ、`<repo-root>` 解決、例外変換、終了コード決定、終了時レポート出力を担う。
- 通常のサブコマンド本体は `Path` を受け取って実行され、`subcommand_log` と `timing` と連携して実行結果を集約する。
- `typer.Exit` と通常例外を分けて扱い、必要に応じて `format_error_report()` で利用者向けエラー表示を行う。

## Read this when

- サブコマンドの入口をどこに集約し、共通の実行制御をどう掛けているか確認したいとき。
- 各サブコマンドが `<repo-root>` の `Path` をどう受け取るか確認したいとき。
- 例外時のエラー表示、終了コード、`typer.Exit` への変換規則を見直したいとき。
- 実行ログ、経過時間、待機時間、戻り値の集計出力の流れを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `<repo-root>` 探索の詳細や `.cmoc` の扱いを詳しく追いたいときは、`repo.py` を読むべきです。
- エラーメッセージ本文の整形や例外クラスの定義そのものを確認したいときは、`errors.py` を読むべきです。
- サブコマンドログやタイミング計測の実装だけを調べたいときは、`subcommand_log.py` と `timing.py` を直接読むべきです。
- Codex CLI 呼び出し、Structured Output、`INDEX.md` 生成など別機能を調べたいとき。

## hash

- e296c49aaa9993d182bfe68f1c51f79af75fa6fd4c466b713809cb0c73354b8f

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

- `<repo-root>` 配下を走査して `INDEX.md` の配置対象を列挙し、深い階層から順に更新するメンテナンス処理をまとめるモジュールです。
- .gitignore、`.git/info/exclude`、`memo`、`build` / `tmp`、dotfiles、symlink、バイナリ、`INDEX.md` 自身を除外して、目次に載せる直下項目を決めます。
- 既存の `INDEX.md` ブロックを解析し、ハッシュが一致して固定フォーマットも保たれているものは再利用し、崩れたものは再生成します。
- Codex CLI の Structured Output で `summary`、`read_this_when`、`do_not_read_this_when` を生成し、差分が出た場合は `INDEX.md` の変更だけを自動コミットします。

## Read this when

- `INDEX.md` の自動配置・更新ルールや、対象ディレクトリの列挙方法を実装・修正したいとき。
- `.gitignore`、`.git/info/exclude`、`memo`、`build` / `tmp`、dotfiles、symlink、バイナリなどの除外条件を確認したいとき。
- 既存の `INDEX.md` の再利用、再生成、ハッシュ一致判定、空ディレクトリの扱いを見直したいとき。
- Structured Output の schema 検証、目次生成用プロンプトの組み立て、Codex 呼び出し、自動コミットの流れを追いたいとき。
- 親子の `INDEX.md` がどの順序で更新されるかや、最新判定の条件を確認したいとき。

## Do not read this when

- 正本仕様だけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `codex exec` の一般的な呼び出し方だけを知りたいときは、`commons/codex.py` を読むべきです。
- `git` リポジトリ探索や `.cmoc`、session state の処理を確認したいときは、別のモジュールを読むべきです。
- `INDEX.md` メンテナンス以外の共通エラー処理やログ制御を調べたいときは、このモジュールの範囲外です。

## hash

- f877795e28b7fb6c6bc4fee92a674b581591825e7577a18ad9c6d29634eabdb1

# `repo.py`

## Summary

- git リポジトリのルート探索、`cwd` 固定、`git` 実行ラッパーをまとめる共通モジュールです。
- `cmoc/session/<session-id>` と `cmoc/apply/<session-id>/<apply-run-id>` のブランチ判定、session id 抽出、apply worktree path 復元を扱います。
- .cmoc/sessions/<session-id>.json` の読み書き、固定スキーマ検証、active session 一覧、session start commit 参照を扱います。
- `.cmoc` の追跡対象外保証、未コミット差分の検出、oracle / 実装ファイルの列挙、削除検出、差分 commit 後の index 復元を行います。

## Read this when

- リポジトリルート探索や `cwd` の固定、`git` コマンド共通実行の挙動を確認・修正したいとき。
- `cmoc/session/...` と `cmoc/apply/...` のブランチ判定や、branch 名から session id を取り出す処理を確認したいとき。
- .cmoc/sessions/<session-id>.json` の state JSON を読み書きする処理や、検証ルールを確認したいとき。
- `oracles` と実装ファイルの列挙、削除検出、差分 commit 後の staged 差分復元を追いたいとき。

## Do not read this when

- CLI の引数定義やサブコマンド本体の業務ロジックだけを確認したいときは、別モジュールを読むべきです。
- `commons.errors` や `commons.indexing` など、別の共通モジュールだけで足りるときはこのファイルを読む必要はありません。
- cmoc の仕様断片やユーザー向け手順だけを追いたいときは、`oracles` 側を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、このモジュールではなく `src/commons/indexing.py` を読むべきです。

## hash

- 62005af6bd7913754183b34aaffde72148702dd2fc7342dcbcde710698bf8ce6

# `subcommand_log.py`

## Summary

- `src/commons/subcommand_log.py` は、各サブコマンド実行の標準出力と標準エラー出力をコンソールと `<repo-root>/.cmoc/logs/sub_commands/<time-stamp>.log` の両方へ tee する共通ログ管理モジュールです。
- `SubcommandLogContext` と `current_subcommand_log()` で現在のサブコマンドログ状態を共有し、`add_quota_wait()` で quota 回復待ち時間を累積できます。
- `subcommand_log()` は一意なログファイル作成と開始メッセージ表示を担い、`_ensure_logs_excluded()` は `.git/info/exclude` を更新して `.cmoc/logs/` が未コミット差分にならないようにします。

## Read this when

- サブコマンドの標準出力と標準エラー出力をコンソールとログファイルへ同時保存する仕組みを確認したいとき。
- 現在実行中のサブコマンドのログ状態や、quota 回復待ち時間の加算方法を確認したいとき。
- ログファイルの保存先、ファイル名の払い出し方法、開始時に表示される相対パスのメッセージを確認したいとき。
- `.cmoc/logs/` をサブコマンド自身の差分として扱わないための除外設定の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数解析だけを確認したいとき。
- `INDEX.md` の自動生成や更新ルールだけを確認したいとき。
- タイムスタンプ生成や経過時間表示など、別の共通ユーティリティを調べたいとき。
- エラー整形や共通エラーハンドリング全体だけを調べたいとき。

## hash

- 7f18681c89832887103f064328d088ebf01496a44ded901bc19821c642c01eb3

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
