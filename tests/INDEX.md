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
- Structured Output の schema ファイル生成、JSON / テキストの再試行、意味的検証失敗、出力プレビューを扱います。
- Codex CLI 呼び出しログ、`subcommand_log` への通知、`INDEX.md` 事前メンテナンスと `skip_index_maintenance`、workspace-write 時の oracle 保護を確認します。
- quota 枯渇時の待機・疎通確認・`--resume` 再実行、`session_id` 抽出、`_resume_command`、`_prepare_codex_exec_paths` も扱います。
- 末尾にはテスト用 git リポジトリ初期化用の `_init_git_repo` / `_git` と、`_FailingTextIO` / `_RecordingTextIO` があります。

## Read this when

- `commons.codex.run_codex_exec()` の呼び出し、`read_only` / `workspace-write`、`--json`、`--output-schema`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の parse 失敗、schema 不一致、意味的検証失敗に対するリトライやエラー表示を追いたいとき。
- Codex CLI 呼び出しログ、`subcommand_log` 通知、出力プレビュー、quota 枯渇時の疎通確認と `resume` 再実行の流れを確認したいとき。
- `INDEX.md` 事前メンテナンス、`skip_index_maintenance`、workspace-write 時の oracle 保護、`session_id` 抽出や `_resume_command` を追いたいとき。

## Do not read this when

- `commons.indexing.maintain_indexes` の実装や `INDEX.md` 生成ルールそのものを確認したいとき。
- `tests/test_subcommands.py` や `tests/test_repo.py` など、別のテスト群の観点だけを追いたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。

## hash

- 003b5da29d284f8685fada729fd262e86f2909a3b98ce9edec049fb0f7f32a9d

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

- 7d1d5e3ee475ea2400b2805fb00e37dc75bbaa85b011fb77d4ea8ea50155494f

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

- `tests/test_subcommands.py` は、`cmoc` のサブコマンド本体に関する決定論的な制御ロジックをまとめて検証するテスト群の入口です。
- 先頭では `run_command` の共通動作、標準出力・エラー出力・終了コード・ログ記録・例外時の集計を確認します。
- 続いて `init`、`session fork/join/abandon`、`eval-oracles`、`apply fork/join/abandon` の状態遷移、前提条件、失敗時の扱いを広く検証します。
- 後半では CLI の Typer 登録、ヘルプ表示、互換 alias、`bin/cmoc` の起動前提、補助関数、プロンプト、JSON schema 検証を確認します。

## Read this when

- `cmoc` のサブコマンド群全体に対する回帰テストの入口を把握したいとき。
- `run_command` の標準出力・標準エラー出力・終了コード・ログ記録・例外時の集計挙動を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`eval-oracles` の状態遷移や失敗時の扱いを横断して追いたいとき。
- CLI の Typer 登録、互換 alias、`bin/cmoc` の起動条件、共通エラーレポートの文面を確認したいとき。
- `apply` と `session` の前提条件、`oracles` と `INDEX.md` の扱い、補助関数やプロンプト検証の観点を素早く整理したいとき。

## Do not read this when

- `src/sub_commands` や `src/main.py` の実装ロジックそのものを追いたいときは、このテスト入口ではなく該当実装を直接読むべきです。
- `commons.indexing` や `INDEX.md` の生成・更新ルールだけを確認したいときは、このファイルではなく別の目次文書を参照すべきです。
- `tests/test_repo.py`、`tests/test_codex.py`、`tests/test_timestamps.py` など、別のテスト群の観点だけを知りたいときはこのファイルを読む必要はありません。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト目次ではなく該当ルール文書を確認すべきです。

## hash

- 72aaadfb685204927d24984faf67e7573d5bbc404aaa4d38730a54cd4fce459c

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
