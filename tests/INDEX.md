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

- `commons.codex.run_codex_exec` の Codex CLI 呼び出しラッパーに関する pytest テストをまとめたファイルです。
- Structured Output の JSON parse 失敗、JSON Schema 不一致、意味的バリデーション失敗に対する 3 回リトライとエラー詳細を検証します。
- `--output-schema` に渡すスキーマファイル生成、ログへの試行情報・スキーマパス・標準出力情報の記録、stdout 進捗表示の 80 文字切り詰めと改行可視化を検証します。
- 通常の Codex CLI 呼び出し直前に `commons.indexing.maintain_indexes` が実行されることと、`skip_index_maintenance=True` で INDEX メンテナンスをスキップできることを検証します。
- テスト内では一時ディレクトリに fake `codex` 実行ファイルを作成し、`PATH` を差し替えて `run_codex_exec` の外部コマンド連携を制御します。

## Read this when

- `run_codex_exec` の Structured Output 対応、JSON 再試行、スキーマ検証、意味的バリデーション、エラー詳細のテストを確認したいとき。
- Codex CLI 呼び出し時に `--output-schema` がどのように渡され、`.cmoc/logs/codex_exec` のログへ何が残るべきかを確認したいとき。
- stdout 進捗表示で prompt と stdout の先頭 80 文字を扱う仕様のテスト例を探しているとき。
- Codex 呼び出し前の `INDEX.md` 自動メンテナンス実行や、INDEX 生成・merge conflict 解消向けのスキップ指定を確認したいとき。
- fake `codex` コマンド、`monkeypatch`、一時 git repo を使った `commons.codex` 周辺のテストパターンを参考にしたいとき。

## Do not read this when

- `run_codex_exec` の実装そのものを読みたいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など個別サブコマンドの CLI 挙動テストを探しているとき。
- INDEX 生成ロジック自体の詳細実装や、`commons.indexing` の単体テストを確認したいとき。
- Codex CLI ではなく git 操作、oracle 評価、ファイルマージ処理などのテストを探しているとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。

## hash

- ff401a6a7b166b183f603554871dc502f0b7a0c4ccfa196b2404298ee0d8e030

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

- `tests/test_repo.py` は、`commons.repo` の git リポジトリ共通処理を検証する pytest テストファイルです。
- `find_repo_root` による親ディレクトリ探索、`ensure_cmoc_ignored` による `.cmoc` ignore 追記・冪等性・tracked `.cmoc` ファイルの index 除外を扱います。
- `list_oracle_files` の oracle ファイル列挙について、`INDEX.md` 除外、root `.gitignore` の尊重、tracked かつ ignored なファイルの除外、slash pattern、`**` semantics、oracles 配下 `.gitignore` の非使用、root 起点 basename pattern の扱いを検証します。
- `changed_oracle_files` の部分評価対象抽出について、cmoc ブランチ base commit からの committed 差分、未コミット変更、未追跡ディレクトリ配下の新規 oracle、gitignore 除外、slash pattern の階層 semantics を検証します。
- `has_deleted_oracle_files` による base..HEAD、working tree、staging area の oracle 削除検出と、削除時の全体評価切替条件を検証します。
- `assert_only_oracles_uncommitted` が `cmoc apply` の事前条件として oracles 外の未コミット差分を拒否することを検証します。
- `is_cmoc_branch` の cmoc ブランチ命名規則判定と、`branch_base_commit_path` の `.cmoc/branch` 配下記録先生成を検証します。
- テスト補助として、一時 git リポジトリを初期化する `_init_repo` と、指定 repo 上で git コマンドを実行する `_git` を定義しています。

## Read this when

- `commons.repo` の実装を変更し、リポジトリ root 探索、`.cmoc` ignore 保証、oracle ファイル列挙、oracle 差分抽出、oracle 削除検出の期待挙動を確認したいとき。
- root `.gitignore` の pattern 解釈を `list_oracle_files` や `changed_oracle_files` に反映する実装を修正するとき。
- `INDEX.md` や gitignored ファイルを oracle 列挙・部分評価対象から除外する条件を確認したいとき。
- `cmoc eval-oracles` の部分評価・全体評価切替に関係する、変更 oracle 抽出や oracle 削除検出のテスト観点を確認したいとき。
- `cmoc apply` の事前条件として、未コミット差分が oracles 配下だけかどうかを判定する仕様を確認したいとき。
- cmoc ブランチ名の形式や branch base commit 記録ファイルのパス生成を変更・確認したいとき。
- pytest 上で一時 git リポジトリを作って `commons.repo` の git 連携処理をテストする方法を参考にしたいとき。

## Do not read this when

- cmoc の CLI コマンド引数、stdout 表示、Codex CLI 呼び出し、Structured Output などのユーザー向け実行時仕様だけを調べたいとき。
- `commons.repo` 以外の実装、たとえばサブコマンド本体、Codex 実行ラッパー、ログ保存、プロンプト生成のテストを探しているとき。
- oracle 正本仕様そのものの内容や、`oracles` 配下のルーティング情報を確認したいだけのとき。
- README、AGENTS、memo、oracles などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- gitignore pattern の一般仕様だけを調べており、cmoc の oracle ファイル列挙・差分抽出での適用挙動が不要なとき。

## hash

- 436bb2308067b9d20eb7220f14d6174748f1586a508f639c1ace9c38a6758c3c

# `test_subcommands.py`

## Summary

- サブコマンド本体の決定論的な制御ロジックを検証する pytest ファイル。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の主要な副作用、エラー条件、標準出力、commit 内容を一時 git リポジトリ上で確認する。
- Fake Codex CLI や monkeypatch を使い、oracle 評価、apply の不整合 JSON schema、レポート保存、repeat 上限、INDEX メンテナンス後の禁止パス再検査をテストする。
- Typer の公開コマンドが各 impl 関数へ直接委譲すること、`cmoc --help` の Usage 表示、merge conflict 解消 prompt と conflict marker 検出 helper の挙動も扱う。
- テスト補助として `_init_repo` と `_git` を定義し、各ケースで独立した git リポジトリを作成して検証する。

## Read this when

- サブコマンド実装の制御フローや git 副作用に対する既存テスト範囲を把握したいとき。
- `cmoc init` の `.cmoc` ignore 追加、tracked `.cmoc` 追跡解除、既存 `.gitignore` 差分の扱いを確認したいとき。
- `cmoc branch` のブランチ名生成、base commit 記録、進捗表示のテストを探しているとき。
- `cmoc eval-oracles` のレポート保存、underscore module 配置、評価 prompt の禁止事項を検証するテストを確認したいとき。
- `cmoc apply` の cmoc ブランチ制約、oracle 外差分拒否、`.cmoc` 保証 commit、oracle commit、Codex JSON schema、repeat 上限、完了・未完了レポートのテストを調べたいとき。
- `cmoc merge` の明示ブランチ merge と削除、自動解決失敗時の案内抑制、conflict prompt、conflict marker 検出のテストを確認したいとき。
- CLI エントリーポイントが共通 runner ではなく個別 impl に委譲していることや、`python -m main --help` のコマンド名表示を検証するテストを見たいとき。

## Do not read this when

- 個別サブコマンドの仕様そのものを確認したいだけで、テストコードの期待値や検証方法が不要なとき。
- サブコマンド実装の内部コードを修正したいだけで、既存テストの構造や対象ケースをまだ調べる必要がないとき。
- INDEX 生成、Codex CLI 呼び出し、ログ保存などの共通仕様を調べたいが、このテストファイルの具体的な検証ケースには関心がないとき。
- pytest、monkeypatch、一時 git リポジトリを使ったテスト補助実装ではなく、ユーザー向け CLI の使い方だけを知りたいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。

## hash

- cd300b3b292ef79e690fc45cb32edc10979a4bc8b9eb5a5fd178952a3e8eb74d

# `test_timestamps.py`

## Summary

- `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の出力形式を検証するテストファイルです。
- cmoc timestamp が `YYYY-MM-DD_HH-MM_SS_mmm` 形式で、日時要素とミリ秒がゼロ埋めされることを確認します。
- 経過時間表示が stdout 用の固定幅 ` h  m  s` 形式になり、秒の小数第 1 位が切り捨てで表示されることを確認します。

## Read this when

- タイムスタンプ文字列の仕様や `make_timestamp` の期待フォーマットを確認したいとき。
- サブコマンド完了時などに表示する経過時間文字列のフォーマットを確認したいとき。
- `commons.timestamps` または `commons.timing` の出力仕様を変更し、その既存テスト影響を把握したいとき。

## Do not read this when

- タイムスタンプや経過時間表示と関係のない CLI サブコマンド仕様を調べているとき。
- 日時生成処理そのものの実装詳細だけを読みたいとき。
- Codex CLI 呼び出し、ログ保存、oracle 評価などの高レベルな実行仕様を確認したいとき。

## hash

- 05d4e42195653c5b491aa1c7a212a92f0c106b6988f231389a2ab14348ca30dc
