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

- `INDEX.md` の自動メンテナンス処理を実装する共通モジュールです。
- 配置対象ディレクトリの列挙、除外条件の適用、既存目次ブロックの再利用、内容ハッシュ比較、必要時の `INDEX.md` 書き込みを扱います。
- Codex CLI に Structured Output schema 付きで目次生成を依頼し、返却 JSON を検証して Markdown の目次ブロックへ変換します。
- `.cmoc` の gitignore 保証、INDEX 更新差分だけを対象にした自動コミット、gitignore 判定、バイナリ判定、`memo` 除外などの補助処理を含みます。
- ハッシュ欄、見出し、Summary、Read this when、Do not read this when の固定フォーマット検証と既存 `INDEX.md` の項目単位パースを行います。

## Read this when

- `INDEX.md` の生成・更新・自動コミットの流れを確認したいとき。
- どのディレクトリに `INDEX.md` を配置し、どの名前やパスを除外するかを調べたいとき。
- 既存の目次情報をハッシュ一致時に再利用する条件や、再生成される条件を確認したいとき。
- Codex CLI に目次情報生成を依頼するプロンプト、Structured Output schema、JSON 検証処理を変更したいとき。
- `memo`、ドットパス、`build`、`tmp`、`__pycache__`、gitignore 対象、バイナリファイルの扱いを確認したいとき。
- `INDEX.md` の Markdown ブロック形式、hash セクション、既存エントリのパースやフォーマット検証に関わる不具合を調査するとき。

## Do not read this when

- 個別サブコマンドの CLI 仕様やユーザー向け挙動だけを調べたいとき。
- Codex CLI 実行ラッパーそのもの、JSON パースの低レベル実装、リトライやログ保存の詳細だけを確認したいとき。
- リポジトリ探索、`.cmoc` の ignore 保証、コミット処理などの共通 git/repo 操作の本体実装だけを読みたいとき。
- 生成された `INDEX.md` の内容そのものを確認したいだけで、生成ロジックが不要なとき。
- cmoc のテスト規約、開発環境、Python コーディング規約など、開発者向けルールだけを調べたいとき。

## hash

- 911fa78749629cf1ca97f70502bca882cdf6c53952df7a7ebfa62f175f4d60cb

# `repo.py`

## Summary

- git リポジトリ検出、カレントディレクトリ移動、現在ブランチ名・HEAD commit 取得、cmoc ブランチ名判定など、リポジトリ操作の共通処理を実装するモジュール。
- `.cmoc` を git 追跡対象外に保つため、root `.gitignore` への `/.cmoc/` 追加、既存 tracked `.cmoc` の index 解除、保証状態の検証を行う。
- 未コミット差分の検出、差分パス一覧取得、差分なし検証、oracles 配下だけの差分検証、指定 pathspec の clean 検証など、サブコマンド実行前の git 状態チェックを提供する。
- `cmoc init` 用に、初期化差分だけを一時 index で commit し、既存 staged 差分を復元する処理を持つ。
- oracle ファイル列挙、変更済み oracle ファイル列挙、削除済み oracle ファイル判定を実装し、`INDEX.md` と root `.gitignore` 対象を除外する。
- cmoc ブランチの base commit 記録ファイルパス生成と読み取り、指定パス差分の commit、git コマンド実行ラッパー、root `.gitignore` 判定ヘルパーを含む。

## Read this when

- cmoc の各サブコマンドで `<repo-root>` を発見し、以降の git 操作をリポジトリルート基準で実行したいとき。
- 現在ブランチ、HEAD commit、cmoc ブランチ名形式、cmoc ブランチ作成元 commit の扱いを確認したいとき。
- `.cmoc` を `.gitignore` と git index の両面から追跡対象外にする処理を調べたいとき。
- 未コミット差分の有無、差分パス一覧、oracles 配下だけに限定した差分検証、初期化対象パスの clean 検証を利用または修正したいとき。
- `cmoc init` が生成した差分だけを commit し、実行前から stage 済みだった利用者差分を保持する仕組みを理解したいとき。
- `cmoc eval-oracles` などで oracle ファイル全体、変更済み oracle ファイル、削除済み oracle ファイルを列挙する条件を確認したいとき。
- root `.gitignore` だけを使った oracle ファイル除外判定や、Git の ignore semantics に近い判定方法を確認したいとき。
- 共通の `git` 実行方法、`CmocError` への変換箇所、標準出力・標準エラーの扱いを確認したいとき。

## Do not read this when

- Codex CLI 呼び出し、プロンプト構成、Structured Output、ログ保存、リトライ方針など、LLM 連携仕様だけを調べたいとき。
- 個別サブコマンドのユーザー向け入出力、進捗表示、終了メッセージ、CLI 引数仕様だけを確認したいとき。
- oracle の正本仕様本文や、どの oracle ファイルを読むべきかの仕様ルーティングだけを調べたいとき。
- cmoc の Python コーディング規約、テスト規約、開発環境ルールだけを確認したいとき。
- git 以外のファイルシステム操作、Codex 実行ログ、自然言語メッセージ生成、評価結果レポートの実装を探しているとき。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。

## hash

- abe347f0e97b031203741aec3568493f1bd67f79cff0af9e346b393170f22de9

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
