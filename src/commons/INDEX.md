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

- Codex CLI 呼び出しに関する共通処理を提供するモジュール。
- `run_codex_exec` で `codex exec` を実行し、read-only または workspace-write のサンドボックス指定、Structured Output schema 指定、stdout 進捗表示、`.cmoc/logs/codex_exec` へのフルログ保存をまとめて扱う。
- `codex exec` 実行直前の INDEX 保守、JSON またはテキスト出力の検証、最大 3 回のリトライ、Codex CLI 失敗時や検証失敗時の `CmocError` 生成を担当する。
- `parse_json_object` で Codex CLI の JSON 応答が object であることを保証する。
- Structured Output 用 schema ファイルの保存、Codex 呼び出しログの追記、cmoc が使う JSON Schema subset の再帰的検査、表示用の 80 文字切り詰めを内部ヘルパーで実装している。

## Read this when

- cmoc から Codex CLI を呼び出す共通経路を実装・修正・調査したいとき。
- `codex exec` のサンドボックス指定、実行ディレクトリ、コマンド引数、prompt の渡し方を確認したいとき。
- Codex CLI 呼び出し前に `maintain_indexes` がいつ実行され、どの条件でスキップされるかを調べたいとき。
- Structured Output の schema ファイル作成、`--output-schema` 引数、JSON parse、schema 検査、意味検証の流れを確認したいとき。
- Codex CLI の stdout/stderr、prompt、returncode、schema パスが `.cmoc/logs/codex_exec` にどのように保存されるかを調べたいとき。
- Codex CLI の失敗、JSON 以外の応答、schema 不一致、テキスト検証失敗がどのようにリトライまたは `CmocError` 化されるかを確認したいとき。
- cmoc 内で使う JSON Schema subset の対応 type、required、properties、additionalProperties、items の検査仕様を確認したいとき。
- Codex CLI の JSON 応答を dict として扱うための `parse_json_object` の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの仕様やユーザー向け CLI ワークフローだけを調べたいとき。
- INDEX 生成・保守ロジックそのもののディレクトリ走査、対象除外、目次生成 prompt の詳細を調べたいとき。
- タイムスタンプ生成の形式や実装だけを確認したいとき。
- `CmocError` クラスの構造、表示形式、共通エラーレポートの詳細だけを調べたいとき。
- Codex CLI と無関係なファイル操作、git 操作、oracle 読み込み、サブコマンド分岐の実装を探しているとき。
- Python の一般的な JSON Schema 検証ライブラリ利用方法や Codex CLI 自体の外部仕様だけを調べたいとき。

## hash

- fcdb548a3b35daaf4f95299b513e7f08276f8edca4d1fd9041240ba9178d45b4

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
- リポジトリ配下の配置対象ディレクトリを列挙し、直下項目ごとの目次ブロックを生成・再利用・更新します。
- `INDEX.md` 生成用の Structured Output schema、Codex CLI へのプロンプト生成、JSON payload 検証を定義します。
- 目次対象から除外するディレクトリ名、ドット始まり項目、`memo`、gitignore 対象、バイナリらしいファイルの判定を扱います。
- ファイル内容またはディレクトリ直下項目の hash から更新要否を判定し、必要に応じて `INDEX.md` を書き換え、自動コミット対象パスをまとめます。
- 既存 `INDEX.md` ブロックのパース、hash 抽出、固定フォーマット検証、Markdown bullet への変換を行う補助関数群を含みます。

## Read this when

- `maintain_indexes` による `INDEX.md` の作成・更新・自動コミット条件を確認したいとき。
- `INDEX.md` 配置対象ディレクトリや目次作成対象項目の除外規則を実装・修正したいとき。
- `memo`、ドット始まり項目、`build`、`tmp`、`__pycache__`、gitignore 対象、バイナリ判定の扱いを調べたいとき。
- 目次情報生成時に Codex CLI へ渡すプロンプト、read-only 実行、Structured Output schema、JSON 検証の流れを確認したいとき。
- 既存 `INDEX.md` の目次ブロックを hash とフォーマットに基づいて再利用する条件を調べたいとき。
- `INDEX.md` の Markdown ブロック形式、`Summary`、`Read this when`、`Do not read this when`、`hash` セクションの生成規則を確認したいとき。
- INDEX メンテナンス処理が `.gitignore` の `.cmoc` ignore 保証や `commit_if_changed` とどう連携するか確認したいとき。

## Do not read this when

- 個別サブコマンドの CLI 仕様やユーザー向け挙動だけを調べたいとき。
- Codex CLI 実行ラッパーそのもの、JSON パースの詳細、リポジトリ共通処理の実装を調べたいとき。
- `INDEX.md` のルーティング文書としての内容を読みたいだけで、自動生成・更新ロジックに関心がないとき。
- cmoc の全体ワークフロー、oracle 評価、branch、apply、merge などの仕様を調べたいとき。
- Python パッケージ構成、CLI エントリーポイント、テスト規約など、INDEX メンテナンス以外の開発ルールを探しているとき。
- 特定ファイルの内容 hash を確認・再計算したいだけのとき。

## hash

- 65d87fde3b9ccbf060cd681882097d7555d2bbdc3fdfd66b85494fb73143b30f

# `repo.py`

## Summary

- `src/commons/repo.py` は、cmoc が対象リポジトリを扱うための共通処理をまとめたモジュールです。
- git リポジトリルートの探索と cwd 移動、現在ブランチ名や HEAD commit hash の取得、cmoc 作業ブランチ名の判定を提供します。
- `.cmoc` が git 追跡対象外であることを保証するため、root `.gitignore` への `/.cmoc/` 追加、既存 tracked `.cmoc` の index 除外、保証状態の検証を行います。
- 未コミット差分の有無確認、未コミット差分が oracle 配下だけかどうかの検査、指定 pathspec の clean 検査、変更パス一覧の取得を扱います。
- `cmoc init` や pathspec 指定 commit のために、一時 git index を使って既存 staged 差分を混ぜずに必要な差分だけ commit し、commit 後に元の staged 差分を復元します。
- oracle ファイル列挙、変更済み oracle ファイル列挙、削除済み oracle ファイル有無判定を実装し、`INDEX.md` と root `.gitignore` 対象ファイルを評価対象から除外します。
- cmoc branch の base commit 記録ファイルの読み書き先パス解決と、記録ファイル欠落時の利用者向け `CmocError` を扱います。
- git 実行は `run_git` に集約され、repo root 固定の cwd、stdout/stderr 捕捉、任意の環境変数・stdin・check 指定を共通化しています。

## Read this when

- cmoc の各サブコマンドで `<repo-root>` を発見し、以降の git 操作をリポジトリルート基準に固定する処理を確認したいとき。
- `.cmoc` ディレクトリを git 追跡対象外に保つ仕様、`.gitignore` への `/.cmoc/` 追加、tracked `.cmoc` の index 除外処理を実装・修正したいとき。
- 未コミット差分の検査、clean working tree 要件、oracle 配下だけの差分許可、指定 pathspec の差分検査に関する共通処理を調べたいとき。
- `cmoc init` が発生させた差分だけを commit し、利用者が事前に stage していた無関係差分を commit に混ぜない仕組みを確認したいとき。
- 特定 pathspec だけを commit する処理、一時 index、`commit-tree`、`update-ref`、既存 staged 差分復元の流れを調べたいとき。
- oracle ファイルの全件評価・部分評価・削除検知で、どのファイルを対象に含めるか、`INDEX.md` や root `.gitignore` 対象をどう除外するか確認したいとき。
- cmoc branch の作成元 commit を `.cmoc/branch/<branch>.txt` から読む処理や、記録ファイルが無い場合のエラーを確認したいとき。
- git コマンド呼び出しの共通ラッパー、`CmocError` への変換箇所、git の stdout/stderr の扱いを調べたいとき。

## Do not read this when

- 個別サブコマンドの CLI 引数、stdout 表示、終了ステータスなど、ユーザー向け実行仕様だけを確認したいとき。
- Codex CLI の呼び出し、プロンプト構成、Structured Output、ログ保存、リトライなど、Codex 連携処理を調べたいとき。
- oracle の正本仕様本文や、oracle 評価プロンプトの内容そのものを読みたいとき。
- `CmocError` クラスの定義やエラー表示フォーマットだけを確認したいとき。
- ファイルシステム上の INDEX.md 自動生成ロジックや、目次情報の JSON schema だけを調べたいとき。
- Python パッケージ構成、CLI エントリーポイント、サブコマンドのルーティングだけを確認したいとき。
- README、AGENTS、oracles、memo の編集可否など、リポジトリ運用ルールだけを確認したいとき。

## hash

- 24164cfead162546386e0c8fbb28f02a2cd9458916008464c314302ec81d5d36

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
