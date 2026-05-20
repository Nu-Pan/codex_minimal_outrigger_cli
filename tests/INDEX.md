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

- `commons.codex.run_codex_exec` の Codex CLI 呼び出しラッパーに対する pytest テストです。
- Structured Output の JSON parse 失敗、JSON Schema 検証失敗、JSON 意味検証失敗、非 JSON テキスト意味検証失敗について、3 回リトライされることと `CmocError` の詳細内容を検証します。
- `--output-schema` に渡す schema ファイル生成、実行ログへの試行情報・schema パス・stdout 情報の記録、stdout 進捗表示の 80 文字切り詰めと改行可視化を検証します。
- 通常の `run_codex_exec` 呼び出し直前に INDEX メンテナンスが実行されること、および `skip_index_maintenance=True` でその処理を明示的にスキップできることを検証します。
- テスト内では一時ディレクトリに fake `codex` 実行ファイルを作成し、`PATH` 差し替え、試行回数ファイル、pytest の `monkeypatch` と `capsys` を使って外部 Codex CLI 呼び出しを隔離しています。

## Read this when

- `run_codex_exec` のリトライ条件、Structured Output 処理、JSON Schema 検証、意味検証コールバックの期待挙動を確認したいとき。
- Codex CLI 呼び出し時の fake `codex` を使ったテスト方法、`PATH` の差し替え、試行回数の記録方法を参考にしたいとき。
- `.cmoc/logs/codex_exec/*.log` に記録される attempt、stdout、output_schema、validation error などのテスト期待値を確認したいとき。
- stdout 進捗表示で prompt/stdout を 80 文字に切り、改行を `\n` として表示する仕様のテストを探しているとき。
- `run_codex_exec` が通常呼び出し前に `commons.indexing.maintain_indexes` を呼ぶこと、または `skip_index_maintenance` によるスキップ挙動を確認したいとき。

## Do not read this when

- `run_codex_exec` の実装そのものを修正したいだけで、テスト期待値や既存テストケースを確認する必要がないとき。
- cmoc のサブコマンド仕様、ユーザー向け CLI ワークフロー、oracle 仕様の詳細を調べたいとき。
- INDEX.md 生成ロジック全体やディレクトリ走査規則を調べたいとき。ただし `run_codex_exec` 直前メンテナンスとの接点だけを確認する場合は読む価値があります。
- Codex CLI の一般的な使い方や実際の外部 Codex 実行結果を知りたいとき。ここでは fake 実行ファイルによる単体テストだけを扱います。
- pytest の基本的な使い方、Python 標準ライブラリ、git コマンド一般の挙動だけを調べたいとき。

## hash

- 31da93958e3b87ea8e750eb46d9fc6105b2c31d22f7ac4aecc98176f55ca97c7

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

- `tests/test_subcommands.py` は、cmoc の主要サブコマンドと CLI ランチャー周辺の決定論的な制御ロジックを検証する pytest テストファイルです。
- `cmoc init` について、`.cmoc` の ignore 追加、tracked `.cmoc` ファイルの追跡解除、既存 `.gitignore` 差分や stage 済み差分を初期化 commit に混ぜないこと、unborn HEAD での初回 commit 作成を検証します。
- `cmoc branch` について、`cmoc_` で始まる作業ブランチ作成、base commit の `.cmoc/branch/<branch>.txt` 記録、作成試行の stdout 表示を検証します。
- `cmoc eval-oracles` について、Fake Codex CLI による評価レポート保存、サブコマンド本体ファイルとラッパーファイルの分離、評価 prompt が実装参照を禁じること、prompt の文言順序を検証します。
- `cmoc apply` について、不整合なし時の完了レポート保存、`repeat` 指定によるループ上限と未収束終了、不完全レポート拒否、cmoc ブランチ外実行拒否、oracle 外差分の事前拒否、`.cmoc` ignore 保証 commit と oracle commit の分離を検証します。
- `cmoc apply` の補助処理として、INDEX メンテナンス後に禁止領域差分が発生した場合の commit 停止、不整合調査 JSON schema の必須項目不足や近似キー拒否を検証します。
- `cmoc merge` について、明示された cmoc ブランチの merge と安全な branch 削除、自動解決失敗時に不要な手動 merge state 案内を stderr に出さないこと、conflict 解消 prompt が oracles 編集を常に禁じること、conflict marker 検査が git 管理対象全体を見ることを検証します。
- `main` と `bin/cmoc` について、Typer 関数が共通 runner ではなく各 impl に直接委譲すること、`cmoc --help` の Usage 表示、サブコマンドエラー時の非ゼロ終了、ランチャーが venv Python を必須にし、venv 欠如時の共通エラーレポートを stdout に出すことを検証します。
- テスト用ヘルパーとして、git 初期化済み一時リポジトリを作る `_init_repo` と、指定リポジトリで git コマンドを実行する `_git` を定義しています。

## Read this when

- cmoc のサブコマンド実装を変更した後、どの振る舞いが `tests/test_subcommands.py` で固定されているか確認したいとき。
- `cmoc init` の `.cmoc` ignore 保証、tracked `.cmoc` の扱い、既存 staged/unstaged 差分を commit に混ぜない制御を確認したいとき。
- `cmoc branch` のブランチ命名、base commit 記録、stdout 進捗表示に関する回帰テストを探しているとき。
- `cmoc eval-oracles` のレポート保存、Fake Codex CLI の使い方、評価 prompt の禁止事項や文言順序を確認したいとき。
- `cmoc apply` の不整合調査 JSON、Structured Output schema、repeat ループ、収束・未収束レポート、commit 分離、禁止差分拒否のテストを確認したいとき。
- `cmoc merge` の明示ブランチ merge、branch 削除、conflict prompt、conflict marker 検査の期待挙動を確認したいとき。
- Typer の `main`、CLI help 表示、サブコマンドエラー時の終了コード、`bin/cmoc` ランチャーの venv 必須挙動や stdout エラー出力を確認したいとき。
- テスト内で一時 git リポジトリを作って git 状態や commit 履歴を検証する既存パターンを流用したいとき。

## Do not read this when

- 個別サブコマンドの実装コードそのものを読みたいとき。このファイルは実装ではなく pytest による期待挙動の固定です。
- oracle 正本仕様のルーティングや仕様本文を調べたいとき。仕様確認は `oracles/INDEX.md` から必要な仕様断片へ進んでください。
- INDEX 自動生成ロジックやファイル目次生成の実装詳細だけを調べたいとき。該当実装や専用テストを読む方が適切です。
- Codex CLI 呼び出しの低レベル実装、ログ保存処理、共通エラー整形処理の内部構造を直接確認したいとき。
- pytest 全体の共通 fixture、テスト規約、開発環境ルールだけを確認したいとき。
- README、AGENTS、oracles、memo の編集可否など、リポジトリ運用ルールだけを確認したいとき。

## hash

- fab3f2a2add10d50263b5b9ef70f35e840828cde6450c5f2843865480c041d92

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
