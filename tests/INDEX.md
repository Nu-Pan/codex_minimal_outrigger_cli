# `conftest.py`

## Summary

- pytest execution helper that prepends the repository's src directory to sys.path so tests can import cmoc source modules without installation.
- Defines SRC as the repository root's src path relative to tests/conftest.py and inserts it at the front of Python's import search path.

## Read this when

- Investigating how tests import modules from <cmoc-root>/src.
- Debugging pytest import errors, module resolution order, or test environment setup.
- Changing the test suite's Python path/bootstrap behavior.

## Do not read this when

- Looking for individual test cases or assertions for cmoc behavior.
- Investigating application runtime import behavior outside pytest.
- Changing cmoc implementation code under <cmoc-root>/src.

## hash

- 32bfe11389fb732e9ac0cc6ecb2e14bf9722d848696fc618e360ef72c19633e7

# `test_codex.py`

## Summary

- `commons.codex.run_codex_exec` の振る舞いを検証する pytest テストファイル。
- Structured Output 利用時の JSON parse 失敗、JSON Schema 検証失敗、意味的バリデーション失敗に対する 3 回リトライとエラー詳細出力を検証する。
- `--output-schema` に渡す schema ファイル生成、codex exec 引数、ログへの試行情報・schema パス記録を検証する。
- Structured Output 指定時に `output_schema` が必須であることを検証する。
- 通常の Codex CLI 呼び出し直前に `commons.indexing.maintain_indexes` が実行されることと、`skip_index_maintenance=True` で明示的にスキップできることを検証する。
- テスト用の fake `codex` 実行ファイルを一時ディレクトリに作成し、`PATH` 差し替え、`tmp_path`、`monkeypatch`、`pytest.raises` を使って外部 Codex CLI 呼び出しを隔離している。

## Read this when

- `run_codex_exec` のリトライ、Structured Output、schema ファイル渡し、ログ出力に関する期待挙動を確認したいとき。
- Codex CLI 呼び出しラッパーのエラー詳細に `Last JSON error`、`Last stdout`、`Log` などが含まれるかを調べたいとき。
- `expect_json=True` と `output_schema`、`json_validator` の組み合わせに関するテストを追加・修正するとき。
- Codex CLI 呼び出し前の `INDEX.md` メンテナンス実行や `skip_index_maintenance` の仕様をテスト側から確認したいとき。
- fake `codex` コマンドを使った CLI ラッパーの単体テストパターンを参照したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など個別サブコマンドの CLI 仕様や統合テストを調べたいとき。
- `INDEX.md` 生成ロジックそのものの実装詳細や、目次メンテナンス対象ファイルの走査規則を調べたいとき。
- Codex CLI ラッパーではなく、git 操作、oracle 評価、ブランチ作成、マージ処理の実装を確認したいとき。
- 実際の Codex CLI の一般的な使い方や外部サービスとしての挙動を知りたいとき。
- cmoc のユーザー向け README やリポジトリ運用ルールだけを確認したいとき。

## hash

- 8e795a51180bf7dbecb39c8f35e9ac8facbd3fdae5515ad4c52b175f32f8a071

# `test_indexing.py`

## Summary

- `commons.indexing.maintain_indexes` による `INDEX.md` 自動メンテナンス処理を検証する pytest テストファイルです。
- git 管理下の一時リポジトリを作成し、目次エントリ生成、gitignore 対象の除外、空ディレクトリへの空 INDEX 作成、build/tmp の扱い、ネストした memo ディレクトリの扱いを確認します。
- 既存 INDEX エントリの必須セクション欠落時の再生成、Structured Output schema 不一致時のリトライ、最新 INDEX では Codex CLI を呼ばないこと、自動コミット時にメンテナンス対象パスだけをコミットすることを検証します。
- テスト用 git リポジトリ作成と git コマンド実行の補助関数 `_init_repo` と `_git` を含みます。

## Read this when

- `maintain_indexes` の期待挙動や回帰テストの対象範囲を確認したいとき。
- `INDEX.md` 生成時に gitignore、空ディレクトリ、build/tmp、memo ディレクトリがどう扱われるべきかを調べたいとき。
- INDEX エントリの hash が最新でも必須セクションが欠ける場合の再生成条件を確認したいとき。
- INDEX 生成用 Codex CLI の Structured Output schema、リトライ、未呼び出し条件をテストで確認したいとき。
- `commit_changes=True` による自動コミットがユーザー作業ファイルを巻き込まないことを確認したいとき。

## Do not read this when

- cmoc の CLI サブコマンド仕様やユーザー向けワークフローを調べたいだけのとき。
- `commons.indexing` の実装詳細を直接修正したいが、まず実装コードを読むべきとき。
- INDEX 以外の機能、たとえば branch、apply、merge、eval-oracles のテストを探しているとき。
- pytest や git 操作の一般的な使い方だけを知りたいとき。

## hash

- 7e58154a1a5e5987a5f2c7550e41f0147143513e45f5953660963380f90faf04

# `test_repo.py`

## Summary

- `commons.repo` の git リポジトリ共通処理を検証する pytest テストファイルです。
- `find_repo_root`、`ensure_cmoc_ignored`、`list_oracle_files`、`changed_oracle_files`、`has_deleted_oracle_files`、`assert_only_oracles_uncommitted`、`is_cmoc_branch`、`branch_base_commit_path` の挙動を対象にしています。
- 一時ディレクトリ上に git リポジトリを作成し、`.cmoc` の ignore・untrack、oracle ファイル列挙、`.gitignore` パターン解釈、部分評価対象抽出、oracle 削除検出、cmoc ブランチ名判定、branch base commit 記録先を確認します。
- テスト補助として、初期 commit 済みリポジトリを作る `_init_repo` と、指定リポジトリで git コマンドを実行する `_git` を定義しています。

## Read this when

- `commons.repo` の git 関連ユーティリティを変更し、既存テストが期待する振る舞いを確認したいとき。
- `.cmoc` を `.gitignore` に追加する処理や、既に tracked な `.cmoc` 配下ファイルを git index から外す処理のテストを確認したいとき。
- `oracles` 配下のファイル列挙で `INDEX.md`、root `.gitignore`、tracked だが ignore 対象のファイル、slash 付きパターン、root 起点 basename パターンをどう扱うか確認したいとき。
- cmoc ブランチの base commit からの oracle 変更抽出や、未コミット・未追跡 oracle ファイルを部分評価対象に含める条件を確認したいとき。
- oracle ファイル削除時に全体評価へ切り替えるための検出条件と、未コミット削除を除外する条件を確認したいとき。
- `cmoc apply` の事前条件として、未コミット差分が oracles 外にある場合に拒否するテストを確認したいとき。
- cmoc ブランチ名の正規形式や `.cmoc/branch/<branch>.txt` への base commit 記録パスを確認したいとき。

## Do not read this when

- cmoc の CLI サブコマンド全体の仕様やユーザー向けワークフローを調べたいだけのとき。
- oracle 評価、apply、merge など個別サブコマンドの高水準仕様を確認したいだけのとき。
- `commons.repo` の実装詳細だけを読みたいとき。
- pytest の一般的な書き方や git の一般的な使い方だけを調べたいとき。
- `oracles` 配下の正本仕様断片やルーティング情報を調べたいとき。
- README、AGENTS、memo、oracles などのリポジトリ運用上の閲覧・編集可否だけを確認したいとき。

## hash

- e5a95acdf7de86f1e0a42d6001d5a0415524883b6097ccc286660326704fc9f5

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc CLI のサブコマンド群に関する pytest ベースの統合寄りテストをまとめたファイルです。
- `init`、`goal`、`ask`、`status`、`attach`、`finish`、`delete`、`sync`、`run`、`check`、`diff`、`list`、`log`、`doctor`、`version`、`help` などの挙動を、主に Typer の `CliRunner` と一時ディレクトリ上のダミーリポジトリで検証します。
- 設定ファイルや状態ファイル、添付ファイル、ログ、Git 連携、Codex 実行のモック、複数ブランチの文脈分離など、サブコマンドがファイルシステムへ与える影響も確認します。

## Read this when

- cmoc のサブコマンドを追加・変更し、その CLI 出力、終了コード、状態保存、設定ファイル更新、ファイル生成の期待値を確認したいとき。
- `goal`、`ask`、`finish`、`delete`、`sync`、`run`、`check` などのコマンドが、プロジェクト状態や Git ブランチ状態とどう連動するべきかを調べたいとき。
- テストで使われている `CliRunner`、一時リポジトリ、Codex 呼び出しのモック、添付ファイルの検証方法を参考にしたいとき。

## Do not read this when

- CLI 実装本体の構造やコマンド定義そのものを確認したいとき。この場合は `src` 配下の実装ファイルを読むべきです。
- 正本仕様断片を確認したいとき。この場合は `oracles/INDEX.md` から必要な仕様ファイルへ辿るべきです。
- README や AGENTS.md など、リポジトリ全体の説明・運用ルールを確認したいだけのとき。

## hash

- 416a72a80607589eaeb35cbd446d187c06a953f58bbc613e31621bb21eb5e7b4

# `test_timestamps.py`

## Summary

- Tests the cmoc timestamp formatting helper `commons.timestamps.make_timestamp`.
- Verifies that a `datetime` value is formatted as `YYYY-MM-DD_HH-MM_SS_mmm` with zero-padded date/time fields and millisecond precision.
- Uses a fixed datetime value with microseconds to confirm truncation or conversion to a three-digit millisecond suffix.

## Read this when

- You are changing timestamp generation or formatting behavior.
- You are modifying `commons.timestamps.make_timestamp` or related timestamp utilities.
- You need to understand the expected cmoc timestamp string format used by tests.

## Do not read this when

- You are working on CLI argument parsing, command routing, or unrelated command behavior.
- You are changing filesystem operations, repository discovery, or process execution logic unrelated to timestamps.
- You only need broad test suite structure and do not need timestamp-specific expectations.

## hash

- 04907b2d4b3124b790c583ea06e2afecdf812378b4b933143c989e15ecfb0373
