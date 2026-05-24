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

- `codex exec` の共通呼び出し処理をまとめるモジュールです。
- モデル指定、reasoning effort、`read-only` / `workspace-write` サンドボックス、Structured Output の設定を共通化しています。
- `--output-last-message` の回収、JSON / JSON Schema の再検証、意味的検証失敗時のリトライを扱います。
- quota 枯渇時の待機と `--resume` 再開、`logs/codex_exec` 配下への呼び出しログ保存、進捗通知の出力を担います。
- Codex CLI の応答を cmoc 側で安全に扱うための JSON object 解析、schema 検査、補助関数群も含みます.

## Read this when

- `codex exec` の実行フローや共通引数の組み立て方法を確認したいとき。
- Structured Output 用の JSON schema ファイル生成や、JSON 応答の再検証方法を調べたいとき。
- quota 枯渇時の待機、疎通確認、`--resume` 再開の挙動を確認したいとき。
- 呼び出しログ、`--output-last-message`、フロントマター付きログの保存規則を確認したいとき。
- `cmoc` から Codex CLI を呼ぶ共通処理を修正・拡張したいとき。

## Do not read this when

- サブコマンド固有の入出力仕様やユーザー向け操作手順だけを調べたいとき。
- `src/commons` 以外の実装配置やファイル構造を探したいとき。
- Python の一般的な開発規約、設計規約、テスト規約だけを確認したいとき。
- `codex exec` 以外のコマンド実装や、各サブコマンド本体の振る舞いだけを知りたいとき。
- `INDEX.md` の生成・更新ロジックだけを調べたいとき。

## hash

- 0f114d42532b162a680d06811c30cda58613a38716e34e6c0fd23e08e8d5e3d4

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

- `src/commons/indexing.py` は `<repo-root>` 配下の `INDEX.md` を列挙・生成・更新し、必要なら変更分を自動コミットする共通モジュールです。
- 配置対象ディレクトリと直下項目を、`memo`、隠し項目、`build` / `tmp` / `__pycache__`、`gitignore` 対象、バイナリらしいファイルを除外しながら判定します。
- 既存の `INDEX.md` ブロックを解析して再利用し、ハッシュ一致かつ固定フォーマット一致なら再生成を避けます。
- 新規生成時は Codex CLI を Structured Output schema 付きで呼び出し、JSON を検証して Markdown の目次ブロックへ変換します。

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

- 45561ccdf742f1b3f4bd7957aae3a05c67bfa27949e4edbe036f819c8cb42bf9

# `repo.py`

## Summary

- `src/commons/repo.py` は、`<repo-root>` の探索と cwd の切り替え、現在ブランチ名・`HEAD` commit の取得、`cmoc_<time-stamp>` 形式のブランチ判定をまとめる共通モジュールです。
- `.cmoc` を `.gitignore` と git index の両面から追跡対象外に保つ保証処理と、その検証、既に tracked されている `.cmoc` の除去を扱います。
- 未コミット差分の検査、指定パスだけを対象にした commit 作成、stage 済み差分の退避と復元など、git 操作を安全に包む処理を提供します。
- `oracles` と実装ファイルの列挙、変更済み・削除済みファイルの収集、rename や untracked を含む差分判定を実装しています。
- `cmoc branch` の作成元 commit を記録・読み出しする `.cmoc/branch/<branch>.txt` の規則と、git 呼び出しの共通ラッパーを持つ基盤です。

## Read this when

- `cmoc` の各サブコマンドから git リポジトリの root、現在ブランチ、`HEAD` commit、変更パスを取得したいとき。
- .cmoc を git 追跡対象外にする保証、`.gitignore` への `/.cmoc/` 追加、tracked な `.cmoc` の index 除去を確認したいとき。
- `cmoc init` などで、利用者が事前に stage していた差分を壊さずに初期化差分だけを commit する仕組みを確認したいとき。
- `oracles` と実装ファイルの列挙規則、`INDEX.md` と `.git` の除外規則、root `.gitignore` の扱いを調べたいとき。
- 部分評価や部分適用のために、base commit 以降の commit 差分、working tree 差分、staging area 差分、untracked ファイルをどう集めるか確認したいとき。
- oracle または実装ファイルの削除有無で full 評価・full 適用へ切り替える判定ロジックを確認したいとき。
- `cmoc branch` の作成元 commit を記録・読み出しする `.cmoc/branch/<branch>.txt` の規則を確認したいとき。

## Do not read this when

- `cmoc` の CLI 引数定義、サブコマンド本体、ユーザー向け出力だけを調べたいとき。
- `CmocError` の表示形式や共通エラーハンドリング全体だけを調べたいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、リトライなど別の共通機能だけを調べたいとき。
- oracle の正本仕様そのものや `oracles` 配下のルーティングを調べたいとき。
- 自動テストの構成や Fake Codex CLI の使い方だけを確認したいとき。
- README、AGENTS、memo などのファイルアクセス規則やリポジトリ運用ルールだけを確認したいとき。

## hash

- 48dae14a2437e2fb30082e6cbd9774239ea1cb56f77d6a86bd80e3014f54423d

# `subcommand_log.py`

## Summary

- `src/commons/subcommand_log.py` は、各サブコマンド実行の標準出力と標準エラー出力をコンソールと `<repo-root>/logs/sub_commands/<time-stamp>.log` の両方へ tee する共通ログ管理モジュールです。
- `SubcommandLogContext` と `current_subcommand_log()` で現在のサブコマンドログ状態を共有し、`add_quota_wait()` で quota 回復待ち時間を累積できます。
- `subcommand_log()` は一意なログファイル作成と開始メッセージ表示を担い、`_ensure_logs_excluded()` は `logs/` が git の未コミット差分にならないよう `.git/info/exclude` を更新します。

## Read this when

- サブコマンドの stdout / stderr をコンソールとログファイルへ同時保存する仕組みを確認したいとき。
- 現在実行中のサブコマンドのログ状態や、quota 回復待ち時間の加算方法を確認したいとき。
- ログファイルの保存先、ファイル名の払い出し方法、開始時に表示される相対パスのメッセージを確認したいとき。
- `logs/` をサブコマンド自身の差分として扱わないための除外設定の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数解析、実行手順だけを調べたいとき。
- `INDEX.md` の自動生成や更新の仕組みだけを調べたいとき。
- タイムスタンプ生成や経過時間表示など、別の共通ユーティリティを調べたいとき。
- エラー整形や共通エラーハンドリング全体だけを調べたいとき。

## hash

- 36cdcf848fb187db08ca3eb3235152049037f79bec4eed84d3c1a46382fedb67

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
