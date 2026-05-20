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

- `commons.codex.run_codex_exec` の Codex CLI 呼び出しラッパーを検証する pytest ファイルです。
- Structured Output 利用時の JSON parse 失敗、JSON Schema 検証失敗、semantic validation 失敗に対する 3 回リトライ、成功時の出力返却、失敗時の `CmocError` 詳細をテストします。
- `--output-schema` に渡す schema ファイルの生成と引数指定、schema 内容、codex exec ログへの `output_schema` 記録を検証します。
- stdout 進捗表示では、prompt と stdout を元文字列の先頭 80 文字で切ってから改行を可視化する仕様をテストします。
- 通常の `run_codex_exec` 呼び出し直前に `commons.indexing.maintain_indexes` が実行されること、`skip_index_maintenance=True` で明示的にスキップできることを検証します。
- テスト内では一時ディレクトリに fake `codex` 実行ファイルを作り、`PATH` を差し替えて Codex CLI の標準出力、引数、試行回数を制御します。
- 補助関数 `_git` は、一時 repo 内で git コマンドを実行するために使われます。

## Read this when

- `commons.codex.run_codex_exec` のリトライ、Structured Output、ログ出力、進捗表示、INDEX メンテナンス連携に関するテストを確認したいとき。
- Codex CLI を fake 実行ファイルで置き換える pytest の書き方や、`monkeypatch` による `PATH` 差し替えの例を探しているとき。
- Structured Output の schema ファイル渡し、JSON Schema 検証、追加の semantic validator の失敗処理を変更する前後で、期待されるテスト範囲を把握したいとき。
- `run_codex_exec` が出す stdout 進捗の 80 文字切り詰めと改行可視化の仕様を確認したいとき。
- `run_codex_exec` と `commons.indexing.maintain_indexes` の呼び出し順や、INDEX 生成・merge conflict 解消向けのスキップ指定を調べたいとき。

## Do not read this when

- cmoc の個別サブコマンド仕様や CLI ワークフロー全体の挙動を調べたいだけのとき。
- `commons.codex.run_codex_exec` の実装そのものを読みたいとき。
- INDEX.md 生成ロジックの詳細実装や oracle ルーティング仕様そのものを調べたいとき。
- Codex CLI 連携以外のテスト、たとえば branch、apply、merge、eval-oracles、init のテストを探しているとき。
- pytest の一般的な使い方だけを知りたいとき。

## hash

- b1df0598dd73a2e31ff62e10f8a2b6cef46ddc4741a50a011fe631d86eeb0430

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
- `find_repo_root`、`.cmoc` の ignore 設定、tracked な `.cmoc` ファイルの untrack、cmoc ブランチ判定、branch base commit 記録パスをテストします。
- `list_oracle_files` が `oracles/INDEX.md` と root `.gitignore` 対象を除外し、Git と同じ slash pattern や `**` の階層 semantics を扱うことを検証します。
- `changed_oracle_files` が base commit 以降の履歴変更、未コミット変更、未追跡ディレクトリ、rename 後パスを部分評価対象として扱い、gitignored oracle を除外することを検証します。
- `has_deleted_oracle_files` が committed、staged、working tree、履歴途中の oracle 削除を全体評価切替条件として検出し、rename、`INDEX.md`、gitignored ファイルの削除を除外することを検証します。
- `assert_only_oracles_uncommitted` が `cmoc apply` の事前条件として oracles 外の未コミット差分を拒否することをテストします。
- テスト用 git リポジトリを初期化する `_init_repo` と、指定 repo 上で git コマンドを実行する `_git` ヘルパーを含みます。

## Read this when

- `commons.repo` の実装を変更し、repo root 探索、`.cmoc` ignore、oracle ファイル列挙、変更 oracle 抽出、削除検出、cmoc ブランチ判定の期待挙動を確認したいとき。
- root `.gitignore` の pattern 解釈、slash 付き pattern、`**`、tracked だが gitignored な oracle ファイルの扱いをテストで確認したいとき。
- `cmoc eval-oracles` の部分評価対象や、oracle 削除時に全体評価へ切り替える条件を理解・変更したいとき。
- `cmoc apply` の事前条件として、oracles 外の未コミット変更を拒否する処理のテストを確認したいとき。
- rename された oracle ファイルを削除ではなく rename 後パスの評価対象として扱う仕様を確認したいとき。
- pytest の `tmp_path` と実 git コマンドを使った repo 関連テストの書き方を参考にしたいとき。

## Do not read this when

- CLI サブコマンドの stdout 表示、Codex CLI 呼び出し、ログ保存、Structured Output などのアプリケーション実行時仕様だけを調べたいとき。
- `commons.repo` 以外の実装、例えばサブコマンド本体、プロンプト生成、oracle 評価ロジック、マージ処理だけを調べたいとき。
- cmoc のユーザー向け README、インストール手順、全体ワークフローだけを確認したいとき。
- `oracles` 配下の正本仕様そのものを探しており、テストコードの具体的な期待値が不要なとき。
- ファイル編集可否、AGENTS.md、README.md、memo、oracles などのリポジトリ運用ルールだけを確認したいとき。

## hash

- 21961dece8d207046beb6a78a540ace87e7148a5745d990adf635f7147f87670

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc の主要サブコマンド本体と CLI ランチャーまわりの決定論的な制御ロジックを検証する pytest ファイルです。
- `cmoc init` について、`.cmoc` の ignore 追加、tracked `.cmoc` ファイルの追跡解除、既存 `.gitignore` 差分や実行前 staged 差分を初期化 commit に混ぜないこと、unborn HEAD で初回 commit を作れることをテストします。
- `cmoc branch` について、`cmoc_` で始まる作業ブランチ作成、base commit 記録、作成試行の stdout 表示をテストします。
- `cmoc eval-oracles` について、Fake Codex CLI を使った評価レポート保存、PEP 8 形式の `eval_oracles.py` 実装ファイル配置、評価 prompt が実装・テスト参照を禁止して仕様だけから判断させることをテストします。
- `cmoc apply` について、不整合なし時の完了レポート保存、`repeat` 指定によるループ上限と未収束終了、必須項目不足レポートの拒否、非 cmoc ブランチ拒否、ユーザー由来の oracle 外差分拒否、`.cmoc` ignore 保証 commit と oracle commit の順序をテストします。
- `apply` の内部補助処理について、INDEX メンテナンス後に禁止領域差分が出た場合の commit 前停止、不整合調査 JSON schema の必須項目不足や近似キー拒否をテストします。
- `cmoc merge` について、明示された cmoc ブランチを clean tree に merge して安全なら削除すること、自動解決失敗時に不適切な手動解決案内を出さないこと、conflict 解消 prompt が常に `oracles` 編集を禁止すること、conflict marker 検査が git 管理対象全体を見ることをテストします。
- Typer の `main` 関数群について、共通 runner や動的 import に頼らず各 subcommand の impl 関数だけへ委譲することを検証します。
- `cmoc --help` と `bin/cmoc` について、Usage に `cmoc` が表示されること、ランチャーが system python3 にフォールバックせず venv Python を要求すること、venv 不在時の共通エラーレポートを stdout に出すことをテストします。
- 末尾には、テスト用 git repository を初期化する `_init_repo` と、指定 repository で git コマンドを実行する `_git` ヘルパーがあります。

## Read this when

- サブコマンド実装を変更したあと、どの決定論的テストが影響を受けるか把握したいとき。
- `cmoc init` の `.cmoc` ignore 保証、追跡解除、既存差分や staged 差分の保護、初回 commit 対応の期待挙動を確認したいとき。
- `cmoc branch` のブランチ命名、base commit 記録、進捗表示に関するテストを探しているとき。
- `cmoc eval-oracles` のレポート保存、評価 prompt、`eval_oracles.py` のファイル配置に関するテストを確認したいとき。
- `cmoc apply` の不整合ループ、Structured Output schema、レポート生成、終了コード、commit 順序、禁止差分検査に関するテストを確認したいとき。
- `cmoc merge` の merge 成功時の branch 削除、自動 conflict 解消失敗時の案内、conflict prompt、conflict marker 検査範囲に関するテストを確認したいとき。
- Typer エントリーポイントや `bin/cmoc` ランチャーのふるまいを変更し、既存テストの期待値を確認したいとき。
- 一時 git repository を使うサブコマンドテストのセットアップ方法や `_git` ヘルパーの使い方を確認したいとき。

## Do not read this when

- cmoc の正本仕様断片そのものを確認したいだけのとき。このファイルは仕様ではなく実装テストです。
- サブコマンドの詳細実装を読みたいとき。実装は `src/sub_commands` 配下を確認してください。
- INDEX メンテナンス処理の実装詳細だけを調べたいとき。該当実装や専用テストを読む方が適しています。
- Codex CLI 呼び出し共通処理、ログ保存、タイムスタンプ生成などの実装詳細だけを調べたいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。
- pytest やテスト環境全体の規約だけを確認したいとき。開発ルール側の仕様や設定ファイルを読む方が適しています。

## hash

- f323a5236ba88ad362b567d44bcd1bfafb8c165f039994e4ee3f396d33002e2e

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
