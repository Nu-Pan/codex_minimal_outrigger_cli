# `conftest.py`

## Summary

- pytest 実行時に `<cmoc-root>/src` を Python の import path 先頭へ追加するテスト共通設定ファイルです。
- `tests` 配下のテストから cmoc 本体の `src` 配下モジュールを直接 import できるようにします。
- `Path(__file__).resolve().parents[1] / "src"` で `<cmoc-root>/src` を解決し、`sys.path.insert(0, ...)` で優先的に参照されるよう設定します。

## Read this when

- pytest で `src` 配下の cmoc 実装モジュールを import できる理由を確認したいとき。
- テスト実行時の Python import path 設定や `sys.path` の変更箇所を探しているとき。
- `tests` 配下の共通 pytest 設定が何をしているか把握したいとき。

## Do not read this when

- 個別テストケースの内容や期待値を調べたいとき。
- cmoc の CLI 挙動、サブコマンド仕様、ユーザー向け出力仕様を確認したいとき。
- pytest fixture、mock、Fake Codex CLI などの具体的なテスト補助機能を探しているとき。
- 本番コードの実装ロジックやアプリケーション設定の詳細を調べたいとき。

## hash

- 70811f2ee49ed59eeb60c3c17354146e78b9c21d8ab9bfbcb46007f9d6c8eb57

# `test_codex.py`

## Summary

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` の挙動を Fake Codex CLI で検証するテスト群の目次です。
- Structured Output の schema ファイル生成、JSON / テキスト出力の再試行、意味的検証失敗時のエラー表示、`enum` や文字列長制約を含む schema 検証を扱います。
- 呼び出しログ、`subcommand_log` への通知、出力プレビュー、`--resume` 再実行、quota 枯渇時の待機と疎通確認、`INDEX.md` 事前メンテナンスと `skip_index_maintenance` の扱いも確認します。
- ファイル末尾には、テスト用 git リポジトリを初期化して `git` を実行する補助関数 `_git` があります。

## Read this when

- `run_codex_exec()` の引数、`--output-schema`、`--output-last-message`、`--resume`、`skip_index_maintenance`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の構文検証・意味的検証のリトライ条件や、JSON schema の `enum` / `minLength` などの制約検証を確認したいとき。
- `logs/codex_exec` の呼び出しログ、`logs/sub_commands` の通知、標準出力の進捗表示や 80 文字の出力プレビュー規則を確認したいとき。
- quota 枯渇時の待機・疎通確認・`--resume` 再開の流れや、Codex 呼び出し前後で `INDEX.md` を保守するかどうかを確認したいとき。
- テスト用 git リポジトリを作る `_git` 補助関数の使い方を確認したいとき。

## Do not read this when

- `cmoc` のユーザー向けサブコマンド仕様や `oracles` 側の正本仕様だけを知りたいとき。
- `tests` 全体の共通 fixture やディレクトリ配置規則だけを確認したいとき。
- `commons.codex` 以外の共通モジュールや `src/sub_commands` の業務ロジックだけを調べたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールや編集可否だけを確認したいとき。
- `INDEX.md` の生成・更新仕様そのものを調べたいとき。

## hash

- bb67a5afb844602d4b3a50bf64a29321499e14e1f33e9b6d0828e8895bbdc38b

# `test_file_naming.py`

## Summary

- `tests/test_file_naming.py` はリポジトリ構成のファイル名が命名規則に従うことを検証するテストです。
- ルート直下のルーティングファイルが指定のないファイル名としてスネークケースの `routing.md` になっていることを確認します。
- 旧名の `ROUTING.md` が残存していないことを確認します。
- `routing.md` が現行の oracle `INDEX.md` 入口を案内し、存在しない旧 `oracles/docs` 配下を直接参照していないことを確認します。

## Read this when

- リポジトリ直下のルーティングファイル名に関する回帰テストを確認したいとき。
- `routing.md` と `ROUTING.md` の期待状態をテスト観点から確認したいとき。
- `routing.md` の oracle 参照先が現行構成に追従していることを検証したいとき。

## Do not read this when

- cmoc のサブコマンド仕様や Codex CLI 連携の挙動を確認したいとき。
- Python 実装規約、INDEX.md メンテナンス、git 共通処理など別機能のテストを探しているとき。
- README、AGENTS、oracles、memo などの編集可否やファイルアクセス規則だけを確認したいとき。

## hash

- 2de90d094eb10a99efef725b983166cbb500ae3fa6e3ee48e8c915ad4ea809b1

# `test_indexing.py`

## Summary

- `commons.indexing.maintain_indexes` による `INDEX.md` メンテナンス処理を検証する pytest テスト群です。
- gitignore 除外、空ディレクトリへの空 `INDEX.md` 作成、`build` / `tmp` の目次掲載、非 UTF-8 バイナリ除外、UTF-8 文字境界、`memo` ディレクトリの扱いを確認します。
- 既存 `INDEX.md` の不備による再生成、Structured Output のリトライ、最新 `INDEX.md` の再利用、自動コミット範囲、`.cmoc` ignore の責務境界を確認します。
- テスト用 git リポジトリを作成する `_init_repo` と、git コマンドを実行する `_git` の補助関数を含みます。

## Read this when

- `maintain_indexes` がどのファイル・ディレクトリを `INDEX.md` の目次対象にするか確認したいとき。
- `INDEX.md` 生成時の gitignore 除外、空ディレクトリ処理、`build` / `tmp` の掲載と配置除外の関係を確認したいとき。
- 非 UTF-8 バイナリ、UTF-8 文字境界、`memo` ディレクトリの扱いがどうなるかをテスト観点から確認したいとき。
- 既存 `INDEX.md` が壊れている場合の再生成、Structured Output のリトライ、最新判定による Codex CLI 呼び出し有無を確認したいとき。
- `INDEX.md` メンテナンス後に自動コミットがどの差分だけを含むかを確認したいとき。
- テスト用 git リポジトリの作り方や、`_init_repo` / `_git` の使い方を確認したいとき。

## Do not read this when

- `commons.indexing` の実装本体だけを追いたいとき。
- `INDEX.md` の正本仕様そのものを知りたいとき。仕様断片は `oracles/app_specs/indexing.md` を読むべきです。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など個別サブコマンドの仕様を調べたいとき。
- Codex CLI 呼び出し共通仕様、ログ保存、エラーハンドリングなど `INDEX.md` メンテナンス以外の実行仕様を調べたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールや編集可否だけを確認したいとき。

## hash

- 1c90b7ee2b0b5c82bca7456807efba2c157a977aac9ad26d7dac41a96b812cdf

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` の git リポジトリ共通処理を検証するテスト群の目次です。
- .cmoc の ignore 保証、既に tracked な `.cmoc` 配下ファイルの index 解除、cmoc ブランチ判定、branch base commit の保存先を扱います。
- oracle ファイル列挙では `INDEX.md` の除外、root `.gitignore` のみを使う判定、`/` 付き pattern、`**` pattern、tracked な ignored file の扱いを確認します。
- 実装ファイル列挙では `oracles`、`.git`、`INDEX.md`、gitignore 対象を除外して、実装対象だけを返すことを確認します。
- 変更・削除検出では、base commit からの oracle / 実装の差分抽出、rename、未追跡ディレクトリ、履歴上の戻し、削除判定、`assert_no_uncommitted_changes` を確認します。

## Read this when

- `commons.repo` の git リポジトリ探索や `.cmoc` ignore 保証のテスト観点を確認したいとき。
- `.cmoc` 配下に既に tracked なファイルがある場合に、index から外す挙動を確認したいとき。
- oracle ファイル列挙で `INDEX.md`、root `.gitignore`、`/` 付き pattern、`**` pattern をどう扱うか確認したいとき。
- 実装ファイル列挙で `oracles` や `INDEX.md` を除外し、実装対象だけを返す条件を確認したいとき。
- `changed_oracle_files` が base commit と working tree / staged / committed 変更をどう拾うか確認したいとき。
- rename 後の oracle を削除ではなく変更として扱うか、削除検出とどう分かれるか確認したいとき。
- `has_deleted_oracle_files` と `has_deleted_implementation_files` の削除判定条件を確認したいとき。
- `cmoc apply` の前提条件として、未コミット差分を拒否する `assert_no_uncommitted_changes` の挙動を確認したいとき。
- cmoc ブランチ名の判定規則や、branch base commit の保存パスを確認したいとき。
- テスト用 git リポジトリを作る `_init_repo` と、そこで git コマンドを実行する `_git` の補助実装を見たいとき。

## Do not read this when

- `cmoc` のユーザー向け CLI 仕様やサブコマンドの入出力だけを知りたいとき。
- `commons.repo` 以外の本体実装や別モジュールのテストを探しているとき。
- oracle 正本仕様そのものを知りたいとき。仕様断片は `oracles/app_specs` 側を読むべきです。
- `INDEX.md` の自動生成やメンテナンス仕様だけを知りたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールや編集可否だけを確認したいとき。

## hash

- 5a7be4c42e04c978dec15c037abb1f5efc9d5cef15bf7b5acbfad4caa9801200

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc のサブコマンド実行制御と CLI 入口の決定論的な挙動を検証するテスト群の目次です。
- `run_command` の stdout への tee、ファイルログ保存、終了コード反映、共通エラーレポート生成を横断して扱います。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の各フローに加えて、prompt、Structured Output、検証ヘルパー、補助関数の挙動をまとめています。
- `main.py` のコマンド登録と互換 alias、`bin/cmoc` の起動条件、`src` の Python ソースに future annotations を使わない制約も回帰対象です。

## Read this when

- サブコマンドの CLI 入口がどの実装関数へ委譲されるか確認したいとき。
- `run_command` の stdout とファイルへの tee、ログ保存、例外時の終了コードやエラーレポートを確認したいとき。
- `cmoc init` の `.cmoc` ignore 追加、tracked ファイルの追跡解除、初期 commit の挙動を確認したいとき。
- `cmoc branch` のブランチ作成、base commit 記録、ブランチ名生成と衝突時の再試行を確認したいとき。
- `cmoc eval-oracles` の評価レポート、severity 集約、prompt 制約、削除済み oracle の扱いを確認したいとき。
- `cmoc apply` の discrepancy 調査、修正ループ、Structured Output schema、commit 連鎖の挙動を確認したいとき。
- `cmoc merge` の branch マージ、衝突解消 prompt、branch 削除条件を確認したいとき。
- `main.py` の `--help`、`eval-oracle` と `eval-oracles` の両立、`cmoc apply --help` の表示を確認したいとき。
- `bin/cmoc` の実行前提や、`src` の Python ソースに future annotations がないかを確認したいとき。

## Do not read this when

- `src/sub_commands` の個別実装本体だけを追いたいとき。
- `src/commons` の共通基盤仕様だけを知りたいとき。
- `oracles` 側の正本仕様だけを確認したいとき。
- `tests/test_indexing.py` や `tests/test_repo.py` など、別のテスト群の仕様を探しているとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールや編集可否だけを確認したいとき。
- `INDEX.md` の自動生成やメンテナンス仕様だけを知りたいとき。

## hash

- e91f758adbbf78c79c8233e6abc18965cfe566d0535dcfbdcbe1a34d27edb411

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の仕様を確認するテスト群の目次です。
- タイムスタンプはローカルタイムゾーン基準で `YYYY-MM-DD_HH-MM_SS_mmm` 形式にゼロ埋めされることを検証します。
- `format_duration` の固定幅表示、小数 1 桁の切り捨て、そして同一ファイル内の補助関数が caller first, callee last で並ぶことを確認します。

## Read this when

- タイムスタンプ生成の書式、ミリ秒表現、aware datetime のローカルタイムゾーン変換を確認したいとき。
- サブコマンドなどで使う経過時間表示の書式や丸め方を確認したいとき。
- `commons.timestamps` や `commons.timing` の変更がこのテスト群に影響するか判断したいとき。
- テスト内の関数配置順や `inspect.getsourcelines()` を使った順序検証の意図を確認したいとき。

## Do not read this when

- タイムスタンプや経過時間表示と関係のない CLI サブコマンド仕様だけを調べたいとき。
- 日時のパースや UTC 固定など、`make_timestamp` 以外の日時処理を探しているとき。
- Codex CLI 呼び出し、ログ保存、`INDEX.md` 自動生成など別の共通仕様を調べたいとき。
- 別のテスト群や `tests` 全体の配置規則を確認したいとき。

## hash

- 86539d333fc59e712b7d1da968c1e89542375bc49ee7fef7e0ce81b4dc030a01
