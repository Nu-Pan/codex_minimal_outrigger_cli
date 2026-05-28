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
- `_prepare_codex_exec_paths` のログ予約、JSON Schema の文字列長・`enum` 検証、テスト用 git リポジトリ初期化の補助関数を確認したいとき。

## Do not read this when

- `src/commons/codex.py` の実装そのものを確認したいとき。
- `commons.indexing.maintain_indexes()` や `INDEX.md` の生成ルールそのものを確認したいとき。
- `tests/test_indexing.py`、`tests/test_repo.py`、`tests/test_subcommands.py` など、別のテスト群だけを追いたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。

## hash

- c9359bf4586fc6ba492f5222dbd6b15201542f6de2f70cd759383430888c37a7

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

- `tests/test_indexing.py` は `commons.indexing.maintain_indexes()` による `INDEX.md` メンテナンスの回帰テスト群の入口です。
- `.gitignore`、`.git/info/exclude`、空ディレクトリ、`build` / `tmp`、symlink、バイナリ、UTF-8 境界、`memo` の扱いを確認します。
- 既存 `INDEX.md` の再利用・再生成、Structured Output のリトライ、親子 `INDEX.md` の連鎖更新、自動コミット範囲を確認します。
- テスト用 git リポジトリ初期化の `_init_repo` と git 実行補助の `_git` を含みます。

## Read this when

- `commons.indexing.maintain_indexes()` の除外条件や更新条件を確認したいとき。
- 既存 `INDEX.md` の再利用・再生成・再生成リトライの挙動を追いたいとき。
- symlink、バイナリ、UTF-8 境界、空ディレクトリ、`memo` の扱いを確認したいとき。
- 自動コミット範囲やテスト用 git リポジトリ初期化の `_init_repo` / `_git` の役割を見たいとき。

## Do not read this when

- `src/commons/indexing.py` の実装ロジックそのものを追いたいとき。
- `INDEX.md` の全体仕様や生成ルールを確認したいとき。
- `tests/test_repo.py` や `tests/test_subcommands.py` など別のテスト群だけを見たいとき。
- `README.md`、`AGENTS.md`、`memo` の扱いだけを確認したいとき。

## hash

- 841f4a092a17535683043227da6f43a1b98cccf49114c02921f550af2c86afc7

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

- 34619cc03e45edd61570226c862272014935f60a647313125a6c4be820352a64

# `test_subcommands.py`

## Summary

- cmoc の主要サブコマンドと CLI 入口の決定論的な制御ロジックを扱うテスト群の目次です。
- `run_command` のログ出力、終了コード、例外時レポート、`repo_root` 解決失敗時の扱いを確認します。
- `init`、`session`、`apply`、`review oracles` の各コマンド登録とヘルプ表示を回帰確認します。
- conflict marker の判定、補助関数の並び順、`bin/cmoc` ランチャーの挙動も含みます。

## Read this when

- cmoc の主要サブコマンド入口や、`main.py` から各 impl への委譲関係を確認したいとき。
- `run_command`、`StepTimer`、`start_step`、`format_error_report` の出力や終了集計を追いたいとき。
- `init`、`session` 系、`apply` 系、`review oracles` 系の状態遷移、例外処理、CLI 登録、ヘルプ表示を広く回帰確認したいとき。
- conflict marker 判定や `bin/cmoc` ランチャーの振る舞いを確認したいとき。

## Do not read this when

- `src/sub_commands/*` の個別実装ロジックだけを追いたいとき。
- `commons.repo` や `commons.indexing` など共通処理の詳細だけを確認したいとき。
- `tests/test_codex.py`、`tests/test_indexing.py`、`tests/test_repo.py` など別のテスト群だけを見たいとき。
- `oracles` 配下の正本仕様や `INDEX.md` の生成ルールそのものを確認したいとき。

## hash

- 8207af38db1a2c453ca8d97c9f9156a0138cc4a388cd34591ff666a89d954a7a

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
