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

- `codex exec` 呼び出しの共通処理を定義するファイルです。
- 実行前の `INDEX.md` 保守、サンドボックス指定、Structured Output 用 schema ファイル生成、`.cmoc/logs/codex_exec` へのフルログ保存、stdout 進捗表示、JSON 応答のリトライと検証をまとめています。
- `run_codex_exec` は Codex CLI 実行の入口で、通常出力または schema 検証済み JSON 文字列を返し、Codex CLI 失敗や JSON 検証失敗時は `CmocError` を送出します。
- `parse_json_object` は Codex CLI の JSON 応答が object であることを保証して辞書として返します。
- 内部 helper として、Codex 実行ログ追記、Structured Output schema 保存、cmoc が使う JSON Schema subset の再帰検証、JSON Schema type 判定、prompt/stdout の先頭 80 文字切り詰めを実装しています。

## Read this when

- cmoc から `codex exec` を呼び出す処理、引数構築、作業ディレクトリ、サンドボックス指定を確認したいとき。
- Codex CLI 呼び出し前に `INDEX.md` 保守がいつ実行され、どの条件でスキップされるかを調べたいとき。
- Structured Output を使う呼び出しで、schema ファイルの保存場所、`--output-schema` 指定、最大 3 回の JSON リトライ、検証順序を確認したいとき。
- Codex CLI の stdout 進捗表示と `.cmoc/logs/codex_exec` 配下のフルログ保存内容を実装または確認したいとき。
- Codex CLI の失敗、JSON parse 失敗、schema 不一致、意味検査失敗がどのように `CmocError` や `ValueError` へ変換されるかを確認したいとき。
- cmoc 内部で対応している JSON Schema subset、`required`、`properties`、`additionalProperties`、`items`、`type` の検証挙動を確認したいとき。
- Codex CLI の JSON 応答を dict として扱う前に `parse_json_object` の保証内容を確認したいとき。

## Do not read this when

- 個別サブコマンドの CLI 仕様、引数、利用者向けワークフローだけを調べたいとき。
- `INDEX.md` の目次生成対象、除外規則、フォーマット、処理順序など、インデックス保守そのものの詳細を調べたいとき。
- タイムスタンプ生成の形式や実装だけを確認したいとき。
- cmoc の共通エラー型やエラーメッセージ表示の実装だけを確認したいとき。
- Codex CLI を使わない処理、git 操作、ファイルコピー、oracle 評価、merge conflict 解消などの実装を調べたいとき。
- 外部の JSON Schema ライブラリ互換性や JSON Schema 全仕様への対応状況を調べたいとき。

## hash

- ffba4a682429b2c6954b1dd42078c883c976fbbee26479e204bfee8e508e5650

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

- `INDEX.md` の自動メンテナンス処理を実装するモジュールです。
- 配置対象ディレクトリの列挙、既存目次ブロックの再利用、直下項目のハッシュ計算、Codex CLI Structured Output による目次情報生成、Markdown 形式への変換を扱います。
- `.cmoc` の ignore 保証、gitignore 対象や `memo`・隠し項目・バイナリらしきファイルの除外、深い階層から親へ向かう更新順序、自動コミット対象の限定を担います。
- INDEX 生成用 JSON schema と payload 検証、既存 `INDEX.md` ブロックの hash・固定フォーマット検証、箇条書き出力などの補助関数を含みます。

## Read this when

- `maintain_indexes` による `INDEX.md` 自動生成・更新の全体フローを確認したいとき。
- どのディレクトリやファイルが `INDEX.md` 配置対象・目次対象から除外されるかを調べたいとき。
- `memo`、隠しファイル、`build`、`tmp`、`__pycache__`、gitignore 対象、バイナリらしきファイルの扱いを確認したいとき。
- INDEX 生成時に Codex CLI へ渡すプロンプト、Structured Output schema、JSON 検証、hash を返させない方針を調べたいとき。
- 既存 `INDEX.md` の目次ブロックをいつ再利用し、いつ再生成するかの判定条件を確認したいとき。
- 直下項目の hash 計算、ディレクトリ hash の子 hash 連結、親目次へ最新の子目次状態を反映する更新順序を理解したいとき。
- INDEX メンテナンス結果を `.gitignore` や `.cmoc` とともに自動コミットする条件を確認したいとき。

## Do not read this when

- cmoc の個別サブコマンドのユーザー向け仕様や実行ワークフローだけを調べたいとき。
- Codex CLI 呼び出しの低レベル実装、JSON 抽出、コマンド実行共通処理そのものを調べたいとき。
- リポジトリ探索、`.cmoc` ignore 保証、コミット処理の詳細実装だけを確認したいとき。
- `INDEX.md` の出力内容を編集したいが、自動メンテナンスの実装ロジックには関心がないとき。
- Python の一般的なファイル I/O、正規表現、hashlib、subprocess の使い方だけを知りたいとき。
- テストコードの構成や Fake Codex CLI の実装方針を調べたいとき。

## hash

- 2ec828f5a583d8de4a4e1224328cd97ce28b558cc5e86cb32cb234ed2c1e2554

# `repo.py`

## Summary

- git リポジトリ検出、cwd の repo root への移動、現在ブランチ名や HEAD commit の取得、cmoc ブランチ名判定など、リポジトリ操作の共通処理を提供する。
- `.cmoc` を git 追跡対象外に保つため、root `.gitignore` への `/.cmoc/` 追加、tracked `.cmoc` の index 解除、保証状態の検証を行う。
- 未コミット差分の有無確認、指定 pathspec の clean 検査、oracles 配下のみの差分制約、変更パス一覧取得など、サブコマンド前提条件の git 状態検査を扱う。
- `cmoc init` 用に、初期化対象差分の検査、init が発生させた `.gitignore`・`.cmoc` 差分だけの commit、任意 pathspec の差分 commit を行う。
- oracle ファイルの全列挙、base commit 以降に変更された oracle ファイル列挙、削除済み oracle ファイル有無判定を行い、`INDEX.md` と root `.gitignore` 対象を除外する。
- cmoc branch の base commit 記録ファイルパス生成と読み取り、git コマンド実行ラッパー、root `.gitignore` の Git wildmatch 評価補助を含む。

## Read this when

- cmoc の任意サブコマンドで、実行対象の git リポジトリルートを見つけて cwd を固定する処理を確認・修正したいとき。
- 現在ブランチ名、HEAD commit、cmoc ブランチ名形式、cmoc branch の base commit 記録ファイルを扱う処理を調べたいとき。
- `.cmoc` ディレクトリを git 追跡対象外にする保証、`.gitignore` への `/.cmoc/` 追加、tracked `.cmoc` の追跡解除に関する実装を確認したいとき。
- 未コミット差分の検査、clean working tree の要求、oracles 配下だけの差分許可、指定パスの clean 検査など、git 状態によるエラー条件を実装・確認したいとき。
- `cmoc init` が自動 commit する初期化差分の範囲や、既存 `.gitignore` 差分を巻き込まない stage 方法を調べたいとき。
- oracle ファイルの列挙、変更済み oracle ファイルの部分評価対象判定、削除済み oracle による full 評価切替条件を確認したいとき。
- root `.gitignore` だけを使った oracle 除外判定や、git check-ignore を使う補助処理の挙動を調べたいとき。
- repo root 起点で git コマンドを実行する共通ラッパーの使い方や戻り値処理を確認したいとき。

## Do not read this when

- CLI 引数定義、サブコマンドの dispatch、ユーザー向け stdout 表示など、git 共通処理以外の CLI 層だけを調べたいとき。
- Codex CLI 呼び出し、プロンプト構成、Structured Output、ログ保存、リトライなど、LLM 連携仕様や実装だけを確認したいとき。
- oracle ファイルの内容評価ロジックや評価レポート生成の詳細を調べたいが、oracle ファイルの列挙条件は不要なとき。
- `INDEX.md` の本文生成、ハッシュ計算、目次ファイルの書き込み規則など、ルーティング文書生成そのものの処理だけを調べたいとき。
- cmoc のエラー表示フォーマットや `CmocError` クラス自体の実装を確認したいとき。
- テストヘルパー、Fake Codex CLI、pytest の fixture など、テスト側の仕組みだけを調べたいとき。
- git の一般的な使い方や GitHub 操作を調べており、cmoc 固有のリポジトリ状態管理が不要なとき。

## hash

- a8775664665f820b782474005af6d5fbb280e4ea4ce41ff4439d3db7ff63757a

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

- サブコマンド実行中の経過時間を計測し、oracle 指定の表示形式で stdout に出力するための共通ユーティリティです。
- `format_duration(duration_seconds)` は秒数を 0.1 秒単位へ切り捨て、負値は 0 に丸めたうえで ` 0h  0m  0.0s` 形式の文字列に変換します。
- `StepTimer` はサブコマンド全体の開始時刻、現在実行中ステップ、確定済みステップ別所要時間を保持します。
- `StepTimer.start(step_name)` は直前ステップを確定してから新しいステップ計測を開始し、`finish_current()` は実行中ステップがある場合だけ所要時間を記録する冪等な処理です。
- `StepTimer.report()` は未確定ステップを確定したうえで、ステップ別タイミングとサブコマンド全体の経過時間を標準出力へ表示します。

## Read this when

- サブコマンドのステップ別経過時間表示や合計経過時間表示を実装・修正したいとき。
- 経過時間の文字列表現、0.1 秒単位への切り捨て、負値の丸め、時分秒フォーマットを確認したいとき。
- `StepTimer` を使って処理ステップの開始、直前ステップの自動終了、最後のステップ確定、レポート出力を行う箇所を理解したいとき。
- stdout に出る `step timings` や `total elapsed` の出力内容に関するテストを追加・修正したいとき。
- サブコマンド共通の進捗・時間計測処理から参照される軽量な共通部品を探しているとき。

## Do not read this when

- Codex CLI 呼び出し、プロンプト生成、Structured Output、ログ保存、リトライなど、時間計測以外の実行時仕様を調べたいとき。
- 個別サブコマンドの業務フロー、引数解析、git 操作、ファイル生成処理そのものを確認したいとき。
- タイムスタンプ文字列やログファイル名など、壁時計時刻に基づく日時フォーマットを調べたいとき。
- `INDEX.md` 自動生成や oracle ルーティングの仕様を理解したいだけで、ステップ所要時間の実装が不要なとき。
- Python の一般的な時間計測 API や `perf_counter` の詳細な仕様だけを調べたいとき。

## hash

- 397c50f2d3692e74114114f8c19a2e4152d5f3cf6f8a73dc42ee51e43364f00d
