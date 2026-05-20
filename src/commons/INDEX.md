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

- Codex CLI 呼び出しの共通処理を実装するモジュールです。
- `run_codex_exec` は `codex exec` の実行、サンドボックス引数の選択、実行直前の INDEX 保守、`.cmoc/logs/codex_exec` へのフルログ保存、Structured Output 用 schema ファイル保存、stdout 進捗表示、失敗時の `CmocError` 化を担当します。
- Structured Output を期待する呼び出しでは最大 3 回まで JSON 解析、schema subset 検査、任意の意味検査をリトライし、全失敗時には最後の stdout、stderr、検証エラー、ログパスを診断情報として返します。
- `parse_json_object` は Codex CLI の JSON 応答を Python の dict として保証し、object 以外なら `CmocError` を送出します。
- 内部 helper として、Codex 呼び出しログ追記、output schema 書き出し、cmoc が使う JSON Schema subset の再帰検証、JSON Schema type 判定、prompt/stdout の先頭 80 文字表示用整形を提供します。

## Read this when

- cmoc から `codex exec` を呼び出す共通処理の実装や挙動を確認したいとき。
- Codex CLI 呼び出し時の read-only / workspace-write サンドボックス指定、作業ディレクトリ、コマンドライン引数の組み立てを調べたいとき。
- Codex 実行前に INDEX 保守がどの条件で走るか、また `skip_index_maintenance` が何を抑止するか確認したいとき。
- `.cmoc/logs/codex_exec` 配下のログファイルや Structured Output schema ファイルがいつ、どの形式で保存されるか調べたいとき。
- Structured Output を期待する Codex 呼び出しの JSON parse、schema 検査、追加 validator、最大 3 回リトライ、失敗時診断の流れを確認したいとき。
- Codex CLI の戻り値が JSON object であることを保証したい処理や、`parse_json_object` のエラー変換を確認したいとき。
- cmoc 側で対応している JSON Schema subset、`required`、`properties`、`additionalProperties: false`、`items`、`type` の検査範囲を調べたいとき。
- 利用者向け stdout 進捗表示で prompt や stdout がどのように 80 文字へ切り詰められるか確認したいとき。

## Do not read this when

- 個別サブコマンドのユーザー向け仕様やワークフローだけを知りたいとき。
- INDEX 生成対象、除外規則、目次情報フォーマットなど、INDEX 保守そのものの詳細実装を調べたいとき。
- タイムスタンプ形式の仕様や `make_timestamp` の実装だけを確認したいとき。
- `CmocError` の表示形式、終了ステータス、共通エラーハンドリング全体を調べたいとき。
- Codex CLI ではなく git 操作、ブランチ作成、merge、oracle 評価などの個別ドメイン処理を実装したいとき。
- Python パッケージ構成、CLI エントリーポイント、テスト規約など、cmoc 開発全体の設計ルールだけを確認したいとき。

## hash

- 4530d9fc3c7ee519b4549c038a18dbf8de40457fb481e182b4b6d6fd223b1230

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

- `src/commons/repo.py` は、cmoc が対象 git リポジトリを扱うための共通処理を集約するモジュールです。
- リポジトリルートの探索と cwd 移動、現在ブランチ名や HEAD commit の取得、cmoc 作業ブランチ名の形式判定を提供します。
- `.cmoc` を git 追跡対象外に保つため、root `.gitignore` への `/.cmoc/` 追加、既存 tracked `.cmoc` の index からの除去、ignore 保証の検証を行います。
- 未コミット差分の有無確認、差分 path の列挙、指定 pathspec の clean 検証、oracle 以外の未コミット差分禁止など、サブコマンド実行前の作業ツリー検査を扱います。
- `cmoc init` 用に、初期化差分だけを一時 index で commit し、利用者が事前に stage していた差分を復元する処理を持ちます。
- 指定 path に差分がある場合だけ add/commit する共通 commit 処理を提供し、`.cmoc` を新規 add 対象から除外します。
- `oracles` 配下の評価対象ファイル列挙、base commit 以降に変更された oracle ファイルの抽出、oracle ファイル削除有無の判定を行います。
- oracle 列挙では `INDEX.md` と root `.gitignore` 対象を除外し、root `.gitignore` の判定には一時 git repository と `git check-ignore --no-index --stdin` を使います。
- cmoc branch の作成元 commit を `.cmoc/branch/<branch>.txt` から読み書きするためのパス解決と読み取り処理を提供します。
- すべての git 呼び出しは `run_git` に集約され、repo root を cwd に固定して stdout/stderr を取得します。

## Read this when

- cmoc の各サブコマンドから共通で使う git 操作、repo root 探索、cwd 固定の実装を確認したいとき。
- `.cmoc` を git 追跡対象外にする保証、root `.gitignore` への `/.cmoc/` 追加、tracked `.cmoc` の index 除去を実装または調査するとき。
- `cmoc init` が利用者の既存 staged 差分を混ぜずに初期化差分だけ commit する仕組みを確認したいとき。
- 未コミット差分がある場合のエラー、oracle 配下だけの差分許可、指定 pathspec の clean 検査など、実行前ガードを調べるとき。
- oracle ファイル列挙、変更済み oracle の部分評価対象抽出、oracle 削除時の全評価切り替え条件を確認したいとき。
- root `.gitignore` のみを使って oracle ファイルや削除 path の除外判定を行う処理を調べたいとき。
- cmoc 作業ブランチ名の形式判定、ブランチ作成元 commit ファイルの場所、base commit 読み取りを確認したいとき。
- git コマンド実行時の共通ラッパー、stdout/stderr の扱い、追加 env や stdin の渡し方を確認したいとき。

## Do not read this when

- CLI 引数定義、サブコマンドの argparse 構成、ユーザー向けコマンドルーティングだけを調べたいとき。
- Codex CLI 呼び出し、プロンプト生成、Structured Output、ログ保存、リトライ方針など LLM 連携部分を調べたいとき。
- oracle ファイルの本文評価ロジックや Codex への評価依頼内容そのものを確認したいとき。
- `INDEX.md` の目次情報フォーマットや自動生成プロンプトの詳細だけを調べたいとき。
- cmoc のエラー表示全体の整形、例外クラス定義、CLI 最上位の例外捕捉だけを調べたいとき。
- テスト実装、Fake Codex CLI、pytest fixture などテスト側の構成だけを確認したいとき。
- 一般的な git の使い方や gitignore の仕様を調べており、cmoc 固有の共通処理を読む必要がないとき。

## hash

- 9d01c66b37aad588fed9bf08efdba80d9cf9c692c8610cae8941e1071afa24af

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
