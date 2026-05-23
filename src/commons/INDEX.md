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

- `src/commons/codex.py` は、cmoc から Codex CLI の `codex exec` を呼び出すための共通ラッパーです。
- `run_codex_exec` を中心に、`model` と `reasoning effort` の組み立て、`read-only` / `workspace-write` の sandbox 指定、Structured Output の schema 連携、`--output-last-message` の回収を扱います。
- Codex 実行前の INDEX.md 保守、`.cmoc/logs/codex_exec` へのフルログ保存、schema ファイルの保存もこのモジュールの責務です。
- JSON 解析、JSON Schema subset の再検証、text / json の意味検証、最大 3 回のリトライ処理をまとめています。
- quota 枯渇時の session id 抽出、`--resume` 付き再実行、復旧確認用の低コスト疎通チェックもここで扱います。

## Read this when

- cmoc から Codex CLI をどのように起動しているか確認したいとき。
- `run_codex_exec` の引数、`read_only`、`expect_json`、`output_schema`、`json_validator`、`text_validator` の使い方を調べたいとき。
- Structured Output の schema ファイルがどこに保存され、どのように `codex exec` に渡されるか確認したいとき。
- Codex 実行ログ、last message ファイル、stdout / stderr の診断情報、リトライ条件を確認したいとき。
- quota 枯渇時の待機・疎通確認・`--resume` 再実行の流れを確認したいとき。
- JSON 応答の `dict` 変換や、cmoc 側の JSON Schema subset 検証を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを調べたいとき。
- `INDEX.md` の自動生成・更新・再利用ルールそのものを調べたいとき。
- git リポジトリ探索、ブランチ操作、差分収集、`.cmoc` の ignore 保証を調べたいとき。
- `CmocError` の表示形式や共通エラーハンドリング全体を調べたいとき。
- タイムスタンプ生成や時間計測など、別の共通ユーティリティを確認したいとき。
- テストコードや Fake Codex CLI の実装パターンだけを確認したいとき。

## hash

- a6f0c1d47f0475678223aa3fa4457e6102ffd67d5163cf860defc5ac5da309ac

# `command_runner.py`

## Summary

- CLI サブコマンドの Typer 関数から呼び出される共通実行ラッパーを定義するファイルです。
- `run_command(handler)` が `<repo-root>` の解決とカレントディレクトリ移動を `enter_repo_root()` に委ね、解決後の `Path` をサブコマンド本体の `handler` に渡します。
- `handler` が整数を返した場合はその値を終了コードとして `typer.Exit` を送出します。
- `typer.Exit` はそのまま再送出し、それ以外の例外は `format_error_report()` で表示してから、例外の `exit_code` 属性または既定値 `1` を使って `typer.Exit` に変換します。

## Read this when

- サブコマンドの Typer エントリーポイントを薄く保ち、共通の実行制御をどこに委譲しているか確認したいとき。
- 各サブコマンド本体が `<repo-root>` の `Path` をどのように受け取るか調べたいとき。
- 例外発生時の共通エラー表示、終了コード決定、`typer.Exit` への変換処理を確認したいとき。
- `enter_repo_root()` や `format_error_report()` とサブコマンド実行フローの接続箇所を探しているとき。

## Do not read this when

- 個別サブコマンドの具体的な処理内容やオプション定義を調べたいとき。
- `<repo-root>` の探索ロジック自体や `.cmoc` の扱いを詳しく確認したいとき。
- エラーメッセージの整形内容や例外クラスの定義を詳しく確認したいとき。
- Codex CLI 呼び出し、プロンプト生成、oracle 評価、INDEX.md 生成などの実処理を調べたいとき。

## hash

- ef44b0b6b838c51a601783bd80e15d97049be1e17cd4771609ed747e30a45b6d

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
- `maintain_indexes` が `<repo-root>` 配下の配置対象ディレクトリを列挙し、必要な `INDEX.md` を生成・更新して、差分があれば自動コミットします。
- 配置対象ディレクトリの除外条件、`memo`・隠し項目・gitignore 対象・バイナリらしいファイル・`build` / `tmp` / `__pycache__` の扱いを実装しています。
- 既存の `INDEX.md` ブロックを解析して再利用し、子項目のハッシュと固定フォーマットの一致を見て再生成要否を判定します。
- 目次本文の新規生成では Codex CLI を Structured Output schema 付きで呼び出し、JSON 検証後に Markdown へ変換します。

## Read this when

- `INDEX.md` がどのディレクトリへ配置され、どの項目が目次生成対象になるかを確認したいとき。
- `maintain_indexes` の処理順、`INDEX.md` 更新、変更パス限定の自動コミットの流れを調べたいとき。
- 既存の `INDEX.md` がハッシュ一致時に再利用される条件や、固定フォーマット検証の仕様を確認したいとき。
- `memo`、隠しディレクトリ、`build`、`tmp`、`__pycache__`、gitignore 対象、バイナリファイルの除外規則を確認したいとき。
- INDEX 生成用の Codex CLI プロンプト、Structured Output schema、JSON 検証、Markdown 変換処理を変更したいとき.

## Do not read this when

- 個別サブコマンドの CLI 引数、ユーザー向け出力、終了ステータスだけを調べたいとき。
- Codex CLI 呼び出しの汎用ラッパー、JSON パース、モデル定数の詳細だけを調べたいとき。
- git コミット処理や `.gitignore` 更新、repo root 検出など、INDEX 以外の repo 共通処理だけを確認したいとき。
- 特定の `INDEX.md` 目次本文だけを読みたい場合で、生成・更新ロジックを追う必要がないとき。
- cmoc 自体の開発規約、テスト規約、環境ルールなど、実装方針の正本仕様を探しているとき.

## hash

- 7f77914cb9e5294ae06f7b4471912058ed5646aa142dea86879f2bc9a5979b32

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

- サブコマンドのステップ時間計測を提供する共通モジュール。
- `StepTimer` はサブコマンド全体の開始時刻、実行中ステップ、確定済みステップ別 duration を保持し、`start()` で直前ステップを確定して新ステップを開始する。
- `StepTimer.report()` は未確定ステップを確定したうえで、ステップ別経過時間とサブコマンド全体の経過時間を stdout に出力する。
- `StepTimer.finish_current()` は実行中ステップがある場合だけ duration を保存して状態をクリアし、実行中ステップが無い場合は何もしない。
- `format_duration()` は秒数を 0.1 秒単位に切り捨て、負値を 0 として扱い、` 0h  0m  0.0s` 形式の経過時間文字列へ変換する。

## Read this when

- サブコマンド処理のステップ別タイミング表示や総経過時間表示を実装・修正するとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` などから共通の時間計測器を使う方法を確認したいとき。
- ステップ開始時に直前ステップを自動的に確定する挙動、または最後のステップを report 時に確定する挙動を確認したいとき。
- 経過時間の表示フォーマット、0.1 秒単位への切り捨て、負値の扱いを確認したいとき。
- タイミングレポートの stdout 出力行や `command_name` の使われ方を確認したいとき。

## Do not read this when

- タイマーを使う側の各サブコマンド固有の処理順序や業務ロジックを調べたいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、リトライなどの実行時仕様全体を調べたいとき。
- oracle ファイル列挙、repo-root 探索、INDEX.md 生成など、時間計測以外の共通処理を調べたいとき。
- pytest や Fake Codex CLI など、テスト基盤の規約だけを確認したいとき。
- Python の一般的な時間計測 API や `perf_counter` の詳細仕様を調べたいだけのとき。

## hash

- 37186b8a149f9438526632ae6e3619364cfc49e91b6157a8b55db52ff3af8126
