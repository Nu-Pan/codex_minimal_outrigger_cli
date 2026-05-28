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

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` とその周辺補助処理を検証するテスト群の入口です。
- Structured Output の schema ファイル生成、JSON / text の再試行、schema 検証失敗や意味的検証失敗を扱います。
- Codex CLI 呼び出しログ、`subcommand_log` 通知、`INDEX.md` 事前メンテナンス、`skip_index_maintenance`、workspace-write 時の `oracles` 保護を確認します。
- quota 枯渇時の待機と `resume` 再実行、`session_id` 抽出、`_resume_command`、`_prepare_codex_exec_paths` も扱います。
- 末尾には、テスト用 git repo 初期化の補助関数と、ログ用の補助関数があります。

## Read this when

- `commons.codex.run_codex_exec()` の引数組み立て、`read_only` / `workspace-write`、`--json`、`--output-schema`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の parse 失敗、JSON Schema 不一致、意味的検証失敗に対するリトライやエラー表示を追いたいとき。
- Codex CLI 呼び出しログ、`subcommand_log` 通知、出力プレビュー、quota 枯渇時の待機と `resume` サブコマンド再実行の流れを確認したいとき。
- `INDEX.md` 事前メンテナンス、`skip_index_maintenance`、workspace-write 時の `oracles` 保護、`session_id` 抽出や `_resume_command` を追いたいとき。
- `_prepare_codex_exec_paths` のログ予約、JSON Schema の文字列長・enum 検証、テスト用 git リポジトリ初期化の補助関数を確認したいとき。

## Do not read this when

- `commons.codex.run_codex_exec()` や周辺補助処理の実装そのものを確認したいときは、`src/commons/codex.py` を読むべきです。
- `commons.indexing.maintain_indexes()` の実装や `INDEX.md` 生成ルールそのものを確認したいときは、`src/commons/indexing.py` や `oracles/app_specs/indexing.md` を読むべきです。
- `tests/test_repo.py`、`tests/test_indexing.py`、`tests/test_subcommands.py` など、別のテスト群だけを追いたいときには適しません。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト群を読む必要はありません。

## hash

- f7f4af5a498ccab7b771969c0ed545c3f4825c2c069fb9fc64aeb9b5c64f6701

# `test_file_naming.py`

## Summary

- `tests/test_file_naming.py` はリポジトリ構成のファイル名が命名規則に従うことを検証するテストです。
- 旧ルーティングファイルである `routing.md` と `ROUTING.md` が残存していないことを確認します。
- ルート直下の案内ファイルを増やさず、現行のルーティング入口を `INDEX.md` 群へ統合していることを検証します。

## Read this when

- リポジトリ直下に旧ルーティングファイルが残っていないことを確認したいとき。
- `routing.md` と `ROUTING.md` の不存在をテスト観点から確認したいとき。
- ルーティング入口を `INDEX.md` 群へ一本化する方針の回帰テストを探すとき。

## Do not read this when

- cmoc のサブコマンド仕様や Codex CLI 連携の挙動を確認したいとき。
- Python 実装規約、INDEX.md メンテナンス、git 共通処理など別機能のテストを探しているとき。
- README、AGENTS、oracles、memo などの編集可否やファイルアクセス規則だけを確認したいとき。

## hash

- 8cffbbd037cfef7eddae93b596fc8e14a5e496a69ec1a9cc344e42ba99a22f43

# `test_indexing.py`

## Summary

- `tests/test_indexing.py` は `commons.indexing.maintain_indexes()` による `INDEX.md` メンテナンスの回帰テスト群です。
- `gitignore` 除外、空ディレクトリ、`build` / `tmp`、symlink、バイナリ、UTF-8 境界、`memo` の扱いを検証します。
- `INDEX.md` の不備検出・再生成、Structured Output のリトライ、既存 `INDEX.md` の再利用、親子 `INDEX.md` の連鎖更新を確認します。
- メンテナンス後の自動コミット範囲と、`.cmoc` の ignore 責務境界も扱います。
- テスト用 git リポジトリ初期化用の `_init_repo` と `_git` を含みます。

## Read this when

- `tests/test_indexing.py` が `commons.indexing.maintain_indexes()` のどの挙動を検証しているか確認したいとき。
- `gitignore` 除外、空ディレクトリ、`build` / `tmp`、symlink、バイナリ、UTF-8 境界、`memo` の扱いを見直したいとき。
- 既存 `INDEX.md` の不備検出、再生成、再利用、Structured Output のリトライを確認したいとき。
- `INDEX.md` メンテナンス後の自動コミット範囲や、`.cmoc` の ignore 責務境界を確認したいとき。
- テスト用 git リポジトリの初期化や、`_init_repo` / `_git` の使い方を確認したいとき。

## Do not read this when

- `commons.indexing.maintain_indexes()` の実装そのものを確認したいとき。
- `INDEX.md` の生成・更新ルール全体だけを確認したいとき。
- `tests/test_codex.py`、`tests/test_repo.py`、`tests/test_subcommands.py` など、別のテスト群を見たいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。

## hash

- 1fc4845deecf3398ea99338c7803bc64551e50edaa66f47868c44a24133cf0e0

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` の git リポジトリ共通処理を検証するテスト群の入口です。
- .cmoc の ignore 保証、tracked な `.cmoc` の untrack、cmoc ブランチ判定、`session_id` 抽出、apply worktree path 復元を扱います。
- `oracles` / 実装ファイルの列挙、変更・削除検出、`INDEX.md` / `.gitignore` / `.git/info/exclude` / `memo` の除外条件、`commit_if_changed` の index 復元と `assert_no_uncommitted_changes` の前提を確認します。
- `.cmoc/sessions/<session-id>.json` の読み書き、固定スキーマ検証、active session 探索と session start commit 参照を扱います。
- ファイル末尾には、テスト用 git リポジトリを初期化する `_init_repo` と、git コマンド実行用の `_git` 補助関数があります。

## Read this when

- `tests/test_repo.py` が `commons.repo` のどの機能を検証しているか確認したいとき。
- `.cmoc` の ignore 保証、tracked な `.cmoc` の追跡解除、cmoc ブランチ判定、`session_id` 抽出を見直したいとき。
- `oracles` / 実装ファイルの列挙、変更検出、削除検出、`INDEX.md`、`.gitignore`、`.git/info/exclude`、`memo` の扱いを確認したいとき。
- session state の読み書き、active session の探索、`commit_if_changed` や `assert_no_uncommitted_changes` の前提条件を把握したいとき。
- テスト用 git リポジトリの初期化や、`_init_repo` / `_git` 補助関数の役割を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックそのものを追いたいとき。
- `INDEX.md` の生成・更新ルールだけを確認したいとき。
- `tests/test_codex.py` や `tests/test_indexing.py` など、別のテスト群の観点だけを追いたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。

## hash

- 7b0496e9dd91cb9180a4b5633298859ba050bfa172ae9227a412869c5ddea155

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は `run_command` と共通エラーレポート、終了コード伝播、サブコマンドログ出力の回帰テスト群の入口です。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`eval-oracles` の制御フロー、state 更新、cleanup、競合処理をまとめて検証します。
- `apply fork` の差分検出や Structured Output 検証、`apply join` のマージと強制解決、`apply abandon` の破棄処理、`eval-oracles` の評価レポート生成を扱います。
- `Fake Codex CLI`、`INDEX.md` 更新、`oracles` / `memo` の制約、`main` と `bin/cmoc` の登録経路、補助関数の順序チェックも確認します。

## Read this when

- サブコマンド群がどの回帰テストでカバーされているか確認したいとき。
- `run_command` のログ出力、例外時レポート、終了コードの扱いを追いたいとき。
- `cmoc init`、`session`、`apply`、`eval-oracles` の制御ロジックをテスト観点で見直したいとき。
- `main` の Typer 登録や `cmoc --help`、`eval-oracle` の互換エイリアス、`bin/cmoc` の起動経路を確認したいとき。
- `Fake Codex CLI` や Structured Output、`INDEX.md` 更新、`oracles` / `memo` の扱いを確認したいとき。

## Do not read this when

- 個別サブコマンドの正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/` を直接読むべきです。
- `src/` 側の実装ロジックや関数本体だけを追いたいときは、このテスト目次ではなく実装コードを読むべきです。
- `tests/test_indexing.py` や `tests/test_repo.py` など、別のテスト群だけを見たいときは適しません。
- テスト規約や `Fake Codex CLI` の一般方針だけを確認したいときは、`oracles/dev_rules/test_rules.md` を読むべきです。

## hash

- c1a2b3ce2a96c3d37381199e9560c211f9832028b7b1c16cbfcfbdc812cde890

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
