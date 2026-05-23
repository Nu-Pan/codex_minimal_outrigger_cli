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

- `src/commons/codex.py` は、cmoc から `codex exec` を起動するための共通ラッパーです。
- `read-only` / `workspace-write` のサンドボックス、`model`、`reasoning_effort`、`--json`、`--output-last-message`、`--output-schema` の付与をまとめて扱います。
- Structured Output の schema を `logs/codex_exec/output_schemae` に hash 名で保存し、`logs/codex_exec/call` と `logs/codex_exec/output_last_message` に実行ログを残します。
- JSON 応答の解析、cmoc 側の JSON Schema subset 再検証、text validator、最大 3 回のリトライ、quota 枯渇時の待機と `--resume` 再実行までを扱います。
- `parse_json_object` で JSON object 以外を拒否し、呼び出し側が `dict` 前提で扱えることを保証します。

## Read this when

- cmoc から Codex CLI をどのようなオプションで呼び出しているか確認したいとき。
- `run_codex_exec` の引数、`expect_json`、`output_schema`、`json_validator`、`text_validator` の扱いを確認したいとき。
- Structured Output の schema ファイルの保存先と、`codex exec` への渡し方を確認したいとき。
- `codex exec` 前の `INDEX.md` 保守の有無や、`skip_index_maintenance` の意味を確認したいとき。
- quota 枯渇時に session id を抽出して `--resume` する流れを確認したいとき。
- JSON 応答を `dict` 前提で扱う処理や、cmoc 側の JSON Schema subset 検証を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを調べたいとき。
- `INDEX.md` の配置対象や自動メンテナンス全体を調べたいとき。
- git リポジトリ探索、ブランチ操作、差分収集、`.cmoc` の追跡外保証を調べたいとき。
- `CmocError` の表示形式や共通エラーハンドリング全体を調べたいとき。
- タイムスタンプ生成、経過時間表示、サブコマンドログなど別の共通ユーティリティだけを確認したいとき。
- テストコードや Fake Codex CLI の実装例だけを確認したいとき。

## hash

- e37d6171c059764e6fa7e8509f409af6218eddb74cfca7b0638ff3f7930f4f47

# `command_runner.py`

## Summary

- `src/commons/command_runner.py` は、CLI サブコマンドの Typer エントリーポイントから呼ばれる共通実行ラッパーです。
- `run_command(handler)` が `<repo-root>` の解決を `enter_repo_root()` に委ね、解決済みの `Path` を `handler` に渡して実行します。
- `handler` が整数を返した場合は終了コードとして扱い、`typer.Exit` と通常例外を共通方針で終了コード化します。
- 例外発生時は `format_error_report()` で利用者向けレポートを出し、`subcommand_log` と `timing` の集計結果も最後に出力します。

## Read this when

- サブコマンド本体を薄く保ち、共通の実行制御をどこに集約しているか確認したいとき。
- 各サブコマンドが `<repo-root>` の `Path` をどのように受け取るか確認したいとき。
- 例外時の共通エラー表示、終了コードの決定、`typer.Exit` への変換規則を確認したいとき。
- サブコマンド実行時のログ、経過時間、待機時間、戻り値出力の流れを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを調べたいとき。
- `<repo-root>` の探索ロジックや `.cmoc` の扱いを詳しく確認したいとき。
- エラーメッセージの整形内容や例外クラス定義そのものを詳しく確認したいとき。
- Codex CLI 呼び出し、Structured Output、INDEX.md 生成などの別機能を調べたいとき。

## hash

- c7cbbadbd76f6d19446132324442beeb3558377b48e8e28e8a998368a94518a7

# `errors.py`

## Summary

- cmoc 全体で使う共通エラー型とエラーレポート整形処理を定義するモジュール。
- `CmocError` は利用者に提示するメッセージ、複数の次アクション、詳細、終了コードを保持する実行時エラーで、次アクションは最低 2 件を必須にしている。
- `format_error_report` は任意の例外を stdout 向けの共通エラーレポート文字列へ変換し、`ERROR`、`Summary`、`Next actions`、`Detail`、`Call stack` の形式で出力内容を組み立てる。
- `CmocError` の場合は保持済みの利用者向け情報を使い、それ以外の例外では汎用的な確認・再実行アクションと例外クラス名・例外文字列を使う。

## Read this when

- cmoc の共通エラーハンドリング、エラー表示、例外から stdout レポートへの変換を実装または修正するとき。
- サブコマンドや共通処理から利用者向けの復旧アクション付きエラーを投げたいとき。
- `CmocError` に渡す `message`、`actions`、`detail`、`exit_code` の意味や制約を確認したいとき。
- 仕様で要求される `ERROR` レポートの見出し構成、次アクション一覧、詳細、コールスタック出力の組み立て方を確認したいとき。
- 通常の Python 例外が cmoc の共通エラーレポート上でどのように扱われるか確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数解析、git 操作、Codex CLI 呼び出し処理を調べたいとき。
- エラー表示ではなく、ログ保存、リトライ、Structured Output、サンドボックス指定などの Codex 連携仕様を調べたいとき。
- テスト用ヘルパー、Fake Codex CLI、pytest 設定など、テスト実装の詳細だけを確認したいとき。
- cmoc のユーザー向けワークフローや `<repo-root>` 側に配置される `INDEX.md` の生成仕様を調べたいとき。
- 例外クラスやエラーレポート形式ではなく、ファイルシステム探索、oracle 読み込み、タイムスタンプ生成などの補助処理を探しているとき。

## hash

- 08942dd418269062be5b2ed6bad95b8f070d9a37fbc0c65ea870a33fd66a06f4

# `indexing.py`

## Summary

- `src/commons/indexing.py` は、`INDEX.md` の自動メンテナンス処理をまとめた共通モジュールです。
- `<repo-root>` 配下の配置対象ディレクトリを列挙し、必要な `INDEX.md` を生成・更新して、差分があれば自動コミットします。
- `memo`、隠し項目、`gitignore` 対象、`build` / `tmp` / `__pycache__`、バイナリらしいファイルを除外する判定を実装しています。
- 既存の `INDEX.md` ブロックを解析して再利用し、子項目のハッシュと固定フォーマットの一致で再生成要否を判定します。
- 目次本文の新規生成では Codex CLI を Structured Output schema 付きで呼び出し、JSON 検証後に Markdown へ変換します。

## Read this when

- `INDEX.md` がどのディレクトリへ配置され、どの項目が目次生成対象になるかを確認したいとき。
- `maintain_indexes` の処理順、`INDEX.md` 更新、変更パス限定の自動コミットの流れを調べたいとき。
- 既存の `INDEX.md` がハッシュ一致時に再利用される条件や、固定フォーマット検証の仕様を確認したいとき。
- `memo`、隠しディレクトリ、`build`、`tmp`、`__pycache__`、`gitignore` 対象、バイナリファイルの除外規則を確認したいとき。
- INDEX 生成用の Codex CLI プロンプト、Structured Output schema、JSON 検証、Markdown 変換処理を変更したいとき。

## Do not read this when

- 個別サブコマンドの CLI 引数、ユーザー向け出力、終了ステータスだけを調べたいとき。
- Codex CLI 呼び出しの汎用ラッパー、JSON パース、モデル定数の詳細だけを調べたいとき。
- git コミット処理や `.gitignore` 更新、repo root 検出など、INDEX 以外の repo 共通処理だけを確認したいとき。
- 特定の `INDEX.md` 目次本文だけを読みたい場合で、生成・更新ロジックを追う必要がないとき。
- cmoc 自体の開発規約、テスト規約、環境ルールなど、実装方針の正本仕様を探しているとき。

## hash

- 6d05df0e2ee40acbac84fbb0549101830c1a9a8fe7f3cdef13cba8aef7aaf83b

# `repo.py`

## Summary

- `src/commons/repo.py` は、git リポジトリ探索、ブランチ・HEAD 情報取得、cmoc 作業用ブランチ判定、`.cmoc` の git 追跡対象外保証、未コミット差分検査、指定パス差分の commit 作成、oracle ファイルと実装ファイルの列挙、変更済みファイルと削除済みファイルの検出を扱う共通処理モジュールです。
- `enter_repo_root`、`find_repo_root`、`current_branch`、`head_commit`、`run_git` など、サブコマンド横断で使う git 実行・リポジトリ状態取得の入口を提供します。
- `ensure_cmoc_ignored`、`gitignore_has_cmoc_rule`、`commit_cmoc_initialization_changes` など、`.cmoc` を root `.gitignore` と git index の両面から追跡対象外に保ち、初期化時の差分だけを安全に commit する処理を含みます。
- `list_oracle_files`、`list_implementation_files`、`changed_oracle_files`、`changed_implementation_files`、`has_deleted_oracle_files`、`has_deleted_implementation_files` など、仕様評価・適用対象ファイルを列挙するための path フィルタリングと git 差分収集を実装しています。
- 一時 index、`commit-tree`、`update-ref`、staged 差分の退避・復元を使い、既存の利用者 staged 差分を混ぜずに cmoc 管理対象だけを commit する補助関数群を持ちます。

## Read this when

- cmoc の各サブコマンドから git コマンドを実行し、repo root、現在ブランチ、HEAD commit、未コミット差分、変更パスを取得する共通処理を確認したいとき。
- `.cmoc` が git に追跡されないことを保証する処理、root `.gitignore` への `/.cmoc/` 追加、tracked `.cmoc` の index 除去、保証検証の実装を調べたいとき。
- `cmoc init` などで、利用者が元から stage していた差分を壊さず、初期化対象の `.gitignore` や `.cmoc` 関連差分だけを commit する仕組みを確認したいとき。
- oracle ファイルや実装ファイルの列挙規則、`INDEX.md`、`oracles`、`.git`、root `.gitignore` 対象ファイルの除外規則を調べたいとき。
- 部分評価や部分適用のために、base commit 以降の committed 差分、working tree 差分、staging area 差分、untracked ファイル、rename/copy 後パスをどのように収集しているか確認したいとき。
- oracle ファイルまたは実装ファイルの削除有無によって full 評価・適用へ切り替える判定ロジックを確認したいとき。
- `.cmoc/branch/<branch>.txt` に保存された cmoc branch 作成元 commit を読む処理や、そのファイルパス規則を調べたいとき。
- gitignore 判定を root `.gitignore` だけで行う一時 git repository 方式や、`git check-ignore` 失敗時の簡易 fallback 判定を確認したいとき。

## Do not read this when

- cmoc の CLI 引数定義、サブコマンドのユーザー向け入出力、進捗表示、Structured Output プロンプト構築だけを調べたいとき。
- oracle の正本仕様そのもの、仕様文書のルーティング、`oracles` 配下の `INDEX.md` 内容を確認したいとき。
- `CmocError` の表示形式や共通エラーハンドリング全体を調べたいだけで、git・ファイル列挙処理の呼び出し箇所に関心がないとき。
- Codex CLI 呼び出し、ログ保存、モデル・reasoning effort、サンドボックス指定など、Codex 連携仕様だけを調べたいとき。
- 自動テストの構成、Fake Codex CLI、pytest fixture、テストデータの作り方だけを調べたいとき。
- README、AGENTS、memo、oracles の編集可否など、リポジトリ運用ルールだけを確認したいとき。

## hash

- fb74e9bfaa0c5c5d27d06f4ca23767d023eb93c7380f80dd7200392ccb31dc2b

# `subcommand_log.py`

## Summary

- `src/commons/subcommand_log.py` は、サブコマンド単位の標準出力・標準エラー出力を `tee` して `<repo-root>/logs/sub_commands` 配下へ保存する共通ログ管理モジュールです。
- `SubcommandLogContext` と `current_subcommand_log()` で現在のログ状態を共有し、`add_quota_wait()` で quota 回復待ち時間を加算できます。
- `subcommand_log()` はログファイルを作成し、コンソール出力とログファイルへの複製を行い、開始時にログの相対パスを表示します。
- `_ensure_logs_excluded()` は `logs/` がサブコマンド自身の未コミット差分にならないよう、`.git/info/exclude` へ除外設定を追加します。

## Read this when

- サブコマンド実行時の標準出力・標準エラー出力をログファイルへ同時保存する仕組みを確認したいとき。
- 現在実行中のサブコマンドのログ状態や、quota 回復待ち時間の累積方法を確認したいとき。
- ログファイルの保存先、ファイル名の付け方、開始メッセージの表示内容を確認したいとき。
- `logs/` をサブコマンド自身の差分として扱わないための除外設定の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数解析、実装手順だけを調べたいとき。
- `INDEX.md` の自動生成や更新の仕組みを調べたいとき。
- git リポジトリ探索、ブランチ操作、差分収集などの共通 repo 処理を調べたいとき。
- タイムスタンプ生成や経過時間表示など、別の共通ユーティリティを調べたいとき。
- エラー整形や例外処理の共通仕様だけを調べたいとき。

## hash

- 56034b81bd2d66809847c5c1a5d493068d686c1cbd4a943e4e12eaa4f3e3d330

# `timestamps.py`

## Summary

- cmoc 仕様で使う `<time-stamp>` 文字列を生成する共通モジュールです。
- `make_timestamp(now: datetime | None = None) -> str` は、指定された `datetime` または現在のローカル時刻からタイムスタンプを作ります。
- 出力形式は `YYYY-MM-DD_HH-MM_SS_mmm` で、年月日時分秒をゼロ埋めし、ミリ秒は `microsecond // 1000` により 3 桁で表現します。

## Read this when

- cmoc のログ名、ファイル名、ディレクトリ名などに使うタイムスタンプ文字列の生成処理を確認したいとき。
- `<time-stamp>` の実装上のフォーマット、ゼロ埋め、ミリ秒の扱いを確認したいとき。
- テストで固定時刻を渡してタイムスタンプ生成を検証したいとき。
- 現在ローカル時刻を使う場合と、呼び出し側が `datetime` を明示する場合の挙動を確認したいとき。

## Do not read this when

- cmoc のサブコマンド別のタイムスタンプ利用箇所や保存先仕様を調べたいとき。
- タイムゾーン変換、UTC 固定、日時パースなど、タイムスタンプ生成以外の日時処理を探しているとき。
- `INDEX.md` 自動メンテナンスや内容ハッシュ計算の実装を調べたいとき。
- コンソール出力、Codex CLI 呼び出し、エラー処理などの共通実行制御を確認したいとき。

## hash

- 19f63db93ff1ae561f750e9a5b22b1d9869679523ef84672607bdf96fda0491b

# `timing.py`

## Summary

- `src/commons/timing.py` はサブコマンドのステップ単位の経過時間を扱う共通モジュールです。
- `StepTimer` はサブコマンド全体の開始時刻、現在のステップ名、確定済みステップの経過時間を保持し、`start()` で直前ステップを確定して次のステップを開始します。
- `report()` は未確定の最後のステップも含めて、各ステップの経過時間とサブコマンド全体の経過時間を stdout に出力します。
- `current_timer()`、`report_current_timer()`、`clear_current_timer()` は `ContextVar` を使って現在の計測器を参照、出力、解除します。
- `format_duration()` は秒数を 0.1 秒単位で切り捨て、負値を 0 として ` 0h  0m  0.0s` 形式の文字列に整形します。

## Read this when

- 各サブコマンドのステップ別タイミング表示や総経過時間表示を実装・修正したいとき。
- `StepTimer` の `start()`、`report()`、`finish_current()` の状態遷移を確認したいとき。
- サブコマンド実行中の現在の計測器を取得したり、最後にまとめて出力したり、参照を消したりする方法を確認したいとき。
- 経過時間の表示フォーマット、0.1 秒単位への切り捨て、負値の扱いを確認したいとき。
- タイミングレポートの stdout 出力行や `command_name` の使われ方を確認したいとき。

## Do not read this when

- 各サブコマンド固有の業務ロジックだけを追いたいとき。
- Codex CLI 呼び出し、ログ保存、Structured Output、リトライなど `timing.py` 以外の共通処理を調べたいとき。
- `INDEX.md` の自動生成や内容ハッシュの規則を調べたいとき。
- `repo` 探索、oracle 列挙、ブランチ操作など、タイミング以外の共通機能を探したいとき。
- Python の一般的な時間計測 API や `perf_counter` の詳細仕様だけを知りたいとき。

## hash

- 10e161032e4c03d1517c0c89f553acc0c2bd56358372ee48189480672ceb7fe1
