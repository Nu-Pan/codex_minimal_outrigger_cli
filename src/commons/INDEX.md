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

- Codex CLI 呼び出しに関する共通処理を提供するモジュールです。
- `run_codex_exec` により `codex exec` を実行し、read-only / workspace-write の sandbox 指定、Structured Output schema の指定、実行直前の INDEX 保守、標準出力の進捗表示、`.cmoc/logs/codex_exec` へのフルログ保存をまとめて扱います。
- Structured Output が必要な呼び出しでは、JSON parse、cmoc 側の JSON Schema subset 検査、任意の意味検査 validator を行い、失敗時は最大 3 回までリトライします。
- Codex CLI の失敗や JSON 検証失敗を `CmocError` として、ログパス、stderr、最後の stdout、schema パスなどの診断情報付きで報告します。
- `parse_json_object` は Codex CLI の応答文字列を JSON object として読み、object 以外の場合は `CmocError` に変換します。
- 内部ヘルパーとして、出力 schema ファイルの保存、Codex 実行ログの追記、JSON Schema subset の再帰検証、JSON Schema type 判定、stdout 表示用の 80 文字短縮処理を含みます。

## Read this when

- cmoc から `codex exec` を呼び出す共通経路を実装・修正したいとき。
- Codex CLI 呼び出し時の sandbox 指定、cwd、prompt 引き渡し、stdout / stderr の扱いを確認したいとき。
- Structured Output 用の JSON schema をどこに保存し、`--output-schema` にどう渡すかを調べたいとき。
- Codex CLI の JSON 応答を cmoc 側で parse・schema 検証・意味検査・リトライする流れを確認したいとき。
- `codex exec` 実行ログが `.cmoc/logs/codex_exec` 配下にどの形式で保存されるかを確認したいとき。
- `codex exec` 直前に `maintain_indexes` が呼ばれる条件や、`skip_index_maintenance` の用途を調べたいとき。
- Codex CLI 失敗時や Structured Output 検証失敗時の `CmocError` メッセージ、修正ヒント、詳細診断の内容を確認したいとき。
- Codex CLI の応答を dict として扱うための `parse_json_object` の挙動を確認したいとき。
- cmoc が対応している JSON Schema subset の `type`、`required`、`properties`、`additionalProperties`、`items` の検証範囲を調べたいとき。

## Do not read this when

- 個別サブコマンドのプロンプト内容や業務ロジックだけを調べたいとき。
- INDEX 生成・保守そのもののファイル列挙、除外規則、目次更新ロジックを詳しく調べたいとき。
- Codex CLI を使わない通常のファイル操作、git 操作、パス探索、タイムスタンプ生成だけを確認したいとき。
- `.cmoc` ディレクトリ全体の仕様や git 追跡対象外保証を調べたいとき。
- cmoc の CLI 引数定義、サブコマンド登録、エントリーポイントの構成を調べたいとき。
- テスト用 Fake Codex CLI の実装やテスト fixtures の詳細を調べたいとき。
- JSON Schema の完全な仕様や外部ライブラリによる汎用 schema 検証を調べたいとき。
- Codex CLI 自体のインストール方法、認証方法、一般的な使い方だけを確認したいとき。

## hash

- f1cd1ba9ba47409f280781903248f88be8ff681cc69c785b36e8ab7ddcbfba7f

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

- `src/commons/errors.py` は、cmoc 全体で使う実行時エラー型と、仕様で要求される stdout 向けエラーレポート整形処理を定義する共通エラーモジュールです。
- `CmocError` はユーザーに提示する要約メッセージ、次に取るべき操作の配列、詳細文、終了コードを保持する cmoc 固有の例外型です。
- `format_error_report` は `CmocError` の場合は保持された `actions`、`detail`、`message` を使い、それ以外の例外では汎用の復旧操作、例外文字列、例外クラス名を使って、`ERROR`、`Summary`、`Next actions`、`Detail`、`Call stack` からなるエラーレポート文字列を生成します。

## Read this when

- cmoc 全体で捕捉・表示する共通エラー形式を確認したいとき。
- ユーザーに次の操作を提示する cmoc 固有エラーを追加または送出したいとき。
- 例外から stdout 向けのエラーレポートを作る処理、特に `Summary`、`Next actions`、`Detail`、`Call stack` の構成を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析、実行順序、正常系の出力仕様を調べたいとき。
- エラーをどこで捕捉して終了コードへ反映するかなど、CLI エントリーポイント側の制御フローを調べたいとき。
- 外部コマンド実行、git 操作、ファイル探索など、エラー発生元となる個別処理の実装を調べたいとき。

## hash

- 08b0686d128c1b8f2a51f93cb0e274aa9b2d34a26b2b4ccea425e88ad291b46d

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

- git リポジトリと cmoc 作業ディレクトリに関する共通処理を実装するモジュールです。
- リポジトリルート探索と cwd 移動、現在ブランチ名や HEAD commit の取得、cmoc ブランチ名形式の判定を扱います。
- `.cmoc` を git 追跡対象外に保つための `.gitignore` 追記、tracked `.cmoc` の index 除外、保証状態の検証を行います。
- 未コミット差分の有無や対象 path の clean 判定、oracle 配下だけに差分が限定されていることの検証、差分がある場合だけの git add/commit を提供します。
- oracle ファイルの全列挙、base commit 以降に変更された oracle ファイルの部分列挙、削除済み oracle の検出、cmoc branch の base commit 記録ファイルの読み書きパス解決を扱います。
- root `.gitignore` の単純な pattern 評価、gitignore 判定の fallback、cwd 固定の `git` コマンド実行ラッパーを含みます。

## Read this when

- cmoc コマンド実行時に `<repo-root>` を見つけて、そのリポジトリルートへ移動する処理を確認したいとき。
- 現在の git ブランチ名、HEAD commit hash、`cmoc_<time-stamp>` 形式のブランチ判定を使う処理を調べたいとき。
- `.cmoc` ディレクトリが git に追跡されないことを保証する実装、`.gitignore` への `/.cmoc/` 追加、tracked `.cmoc` の index 除外を確認したいとき。
- 未コミット差分の検出、clean working tree の強制、oracle 配下だけの差分許可、特定 pathspec の差分検査を実装・調査するとき。
- init や oracle 更新後に、指定パスへ差分がある場合だけ git add/commit する共通処理を確認したいとき。
- `oracles` 配下の評価対象ファイル列挙、`INDEX.md` 除外、root `.gitignore` 対象除外、部分評価対象となる変更済み oracle ファイルの収集を調べたいとき。
- cmoc branch 作成元 commit を `.cmoc/branch/<branch>.txt` から読む処理や、その保存パスを確認したいとき。
- このモジュールの `run_git` を通した git 実行、stdout/stderr の扱い、`check=False` を使う git コマンドの呼び出し方を確認したいとき。

## Do not read this when

- CmocError クラスそのものの表現、終了ステータス、共通エラー表示の仕組みだけを調べたいとき。
- Codex CLI 呼び出し、プロンプト生成、Structured Output、サンドボックス設定など LLM 連携処理を調べたいとき。
- CLI サブコマンドの argparse 定義、コマンド名、引数、サブコマンド間のルーティングだけを確認したいとき。
- コンソール出力、進捗表示、完了時間レポートなど UI 表示の仕様や実装だけを調べたいとき。
- oracle ファイルの内容評価、Codex による oracle 判定、評価結果 JSON の処理を調べたいとき。
- `INDEX.md` の本文生成、目次更新順序、Structured Output のスキーマ組み立てなど、ルーティング文書生成の詳細を調べたいとき。
- タイムスタンプ生成、cmoc ブランチ名の作成処理、作業ブランチ作成フロー全体を調べたいが、ブランチ名の形式判定だけでは足りないとき。
- Python パッケージ構成、テスト規約、開発環境、依存関係など cmoc 開発ルール全般だけを確認したいとき。

## hash

- 7ddc854646eb1f88368408f463541fb7de4010b4631e0fd3d552c2379a4baac7

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

- サブコマンド実行中のステップ別経過時間と全体経過時間を計測し、標準出力へレポートする共通ユーティリティです。
- `StepTimer` は作成時にサブコマンド全体の開始時刻を記録し、`start()` でステップを切り替え、直前ステップを自動的に確定します。
- `finish_current()` は実行中ステップがある場合だけ経過時間を保存する冪等な確定処理で、`report()` は未確定ステップを含めてステップ別秒数と合計秒数を表示します。

## Read this when

- サブコマンドの処理区間ごとの経過時間を計測・表示する実装を確認したいとき。
- `StepTimer` の生成、ステップ開始、現在ステップ確定、レポート出力の呼び出し順を調べたいとき。
- 完了時の `step timings` や `total elapsed` の stdout 出力形式を確認・変更したいとき。
- ステップ切り替え時に直前ステップがどのように自動確定されるかを確認したいとき。

## Do not read this when

- 日時文字列、ファイル名用タイムスタンプ、ログディレクトリ名などの壁時計時刻を生成する処理を探しているとき。
- サブコマンド固有の業務ロジック、Codex CLI 呼び出し、git 操作、oracle 評価処理を調べたいとき。
- 進捗メッセージやエラー表示など、経過時間以外のコンソール出力仕様を確認したいとき。
- テスト用の時間固定、Fake Codex CLI、pytest 側の検証実装を探しているとき。

## hash

- 2e8cd0e39512e7f3a2d8945e1abf5e8e96929611985513666e5c8ebd2c4535b3
