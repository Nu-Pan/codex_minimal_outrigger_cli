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

- `commons.indexing.maintain_indexes` による `INDEX.md` メンテナンス処理の pytest テストです。
- 直下項目ごとの目次生成、`.gitignore` 対象の除外、空ディレクトリへの空 `INDEX.md` 作成、`build`・`tmp` の親目次への掲載と配下配置除外を検証しています。
- 非 UTF-8 バイナリの目次除外、repo root 直下以外の `memo` ディレクトリへの `INDEX.md` 配置、必須セクション欠落時の再生成、Structured Output 不一致時のリトライを検証しています。
- 既存 `INDEX.md` が最新のときは Codex CLI を呼ばないこと、自動コミット時に `INDEX.md` などメンテナンス対象パスだけをコミットし、ユーザー作業ファイルを含めないことを確認しています。
- テスト用 git リポジトリを作成する `_init_repo` と、指定 repo 上で git コマンドを実行する `_git` ヘルパーを含みます。

## Read this when

- `maintain_indexes` の挙動変更に合わせて INDEX 生成・更新テストを追加または修正するとき。
- `INDEX.md` の対象項目、除外規則、空ディレクトリ、`build`・`tmp`、バイナリファイル、`memo` ディレクトリの扱いをテストで確認したいとき。
- Structured Output schema、Codex CLI 呼び出し、無効 JSON 出力時のリトライ、最新 INDEX での Codex CLI 呼び出し抑止を検証したいとき。
- `commit_changes=True` の自動コミット対象がメンテナンス差分だけに限定されることを確認したいとき。
- 一時ディレクトリ上に git repo を作るテストヘルパーや、pytest の `monkeypatch` を使った `run_codex_exec` 差し替え例を探しているとき。

## Do not read this when

- cmoc の CLI サブコマンド仕様やユーザー向けワークフローを確認したいだけのとき。
- `commons.indexing` の実装そのものを読みたいとき。
- Codex CLI 実行ラッパー全般、プロンプト構成、ログ保存などの実装詳細を調べたいとき。
- `INDEX.md` 以外のテスト、または oracle 評価・branch・apply・merge など別機能のテストを探しているとき。
- リポジトリ運用ルール、編集禁止ファイル、AGENTS.md の制約だけを確認したいとき。

## hash

- 112fdf77fa2659d03b32d453b9a6ac54e3b0deffadbbd00dbce0bc0636526810

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

- `tests/test_subcommands.py` は、cmoc の主要サブコマンド本体と CLI ランチャー周辺の決定論的な制御ロジックを検証する pytest ファイルです。
- `cmoc init` について、`.cmoc` ignore ルールの追加、tracked `.cmoc` の追跡解除、既存 `.gitignore` 差分や既存 staged 差分を初期化 commit に混ぜないこと、unborn HEAD での初回 commit 作成を確認します。
- `cmoc branch` について、`cmoc_` で始まる作業ブランチ作成、base commit 記録、作成試行の stdout 表示を確認します。
- `cmoc eval-oracles` について、Fake Codex CLI による評価レポート保存、ハイフン付き実体ファイルとアンダースコア付き wrapper の分離、評価 prompt が実装参照を禁じること、prompt の文言順序を確認します。
- `cmoc apply` について、不整合なし時の完了レポート、`repeat` によるループ上限、必須項目を欠くレポートの拒否、cmoc ブランチ外実行の拒否、oracle 外差分の事前拒否、`.cmoc` ignore 保証 commit と oracle commit の順序、INDEX メンテナンス後の禁止領域差分検出、不整合 JSON schema の検証を扱います。
- `cmoc merge` について、明示 cmoc ブランチの merge と削除、自動解決失敗時の手動 merge state 案内抑制、conflict 解消 prompt で `oracles` 編集を常に禁じること、conflict marker 検査が git 管理対象全体を見ることを確認します。
- Typer の main 関数が共通 runner ではなく各 impl にだけ委譲すること、`cmoc --help` の Usage 表示、サブコマンドエラー時の終了コードと stdout エラーレポート、`bin/cmoc` が `.venv` Python 必須で missing venv 時も stdout に共通エラーを出すことを検証します。
- テスト補助として、一時 git repository を作る `_init_repo` と、指定 repo 内で git コマンドを実行する `_git` を定義しています。

## Read this when

- サブコマンド本体の制御ロジックに関する既存テストの範囲を把握したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の仕様変更に対して、どの回帰テストを更新または追加すべきか判断したいとき。
- `.cmoc` ignore 保証、oracle ファイル commit、cmoc ブランチ制約、merge 後のブランチ削除など、git 操作を伴うサブコマンド挙動の期待値を確認したいとき。
- Codex CLI 呼び出しを monkeypatch した apply や eval-oracles のテスト方法、Structured Output の schema 検証、レポート保存の検証方法を参考にしたいとき。
- CLI entry point、Typer 委譲、`python -m main`、`bin/cmoc` ランチャー、共通エラーレポートのテストを確認したいとき。
- conflict 解消 prompt、conflict marker 検査、merge 自動解決失敗時の表示制御を変更するとき。
- 一時 git repository を使う pytest の書き方や、このファイル内の `_init_repo`、`_git` helper を利用するテストを追加したいとき。

## Do not read this when

- oracle 仕様断片そのものや、仕様ファイル間のルーティング情報を調べたいだけのとき。
- cmoc の実装コードそのものの構造や関数定義を読みたいとき。
- `maintain_indexes` や INDEX 生成ロジックの詳細実装だけを調べたいとき。
- サブコマンドのエンドユーザー向け説明や README に載せる操作手順だけを確認したいとき。
- pytest ではなく手動実行での動作確認手順、インストール手順、環境構築手順だけが必要なとき。
- `memo`、README、AGENTS、oracles など、このテストファイル外の編集可否やリポジトリ運用ルールだけを確認したいとき。

## hash

- 01903fa80abd84158f03ca56ebf616fcc7f297fe76c5ca1ece8075f8facce6c0

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
