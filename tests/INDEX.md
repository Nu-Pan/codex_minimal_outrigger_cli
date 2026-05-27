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

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` の振る舞いを Fake Codex CLI で検証するテスト群の入口です。
- Structured Output の schema ファイル生成、JSON とテキストの再試行、意味的検証失敗時の詳細エラー、`enum` や文字列長制約の検査を扱います。
- 呼び出しログ、`subcommand_log` への通知、`INDEX.md` 事前メンテナンスと `skip_index_maintenance`、quota 枯渇時の待機・疎通確認・`--resume` 再実行も確認します。
- ファイル末尾には、テスト用 git リポジトリを初期化して `git` を実行する補助関数 `_init_git_repo` と `_git`、および `_FailingTextIO` / `_RecordingTextIO` があります。

## Read this when

- `commons.codex.run_codex_exec()` の引数、`--output-schema`、`--output-last-message`、`--resume`、`skip_index_maintenance`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の parse 失敗、意味的検証失敗、JSON Schema の `enum` や文字列長制約に対するリトライとエラー表示を確認したいとき。
- Codex CLI 呼び出しログ、`subcommand_log` への通知、出力プレビュー、quota 枯渇時の待機と疎通確認、再実行の流れを確認したいとき。
- Codex 呼び出し前後の `INDEX.md` メンテナンスの有無や、`skip_index_maintenance` による明示スキップを確認したいとき。
- テスト用 git リポジトリを初期化して `git` を実行する補助関数 `_init_git_repo` と `_git`、ならびに `_TeeTextIO` の補助テストを確認したいとき。

## Do not read this when

- `cmoc` の個別サブコマンド正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/INDEX.md` 側を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `commons.codex.run_codex_exec()` 以外の実装や、`tests` 配下の別テスト群だけを追いたいときは、このファイルでは範囲が広すぎます。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト目次ではなく別の案内を参照すべきです。

## hash

- e4860b4c71a56d69dab03afe3d94b071487da810591b3e401c816decd518ae98

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

- `commons.indexing.maintain_indexes` による `INDEX.md` メンテナンス処理の回帰テスト群です。
- `gitignore` 除外、空ディレクトリ、`build` / `tmp`、バイナリ、UTF-8 境界、`memo`、既存 `INDEX.md` の再生成と再利用、自動コミット範囲を検証します。
- Structured Output のリトライ、親子 `INDEX.md` の再生成連鎖、`.cmoc` ignore の責務境界も確認します。
- テスト用 git リポジトリを作る `_init_repo` と、`git` 実行用の `_git` を含みます。

## Read this when

- `maintain_indexes` がどのファイル・ディレクトリを `INDEX.md` の目次対象にするか確認したいとき。
- `gitignore` 除外、空ディレクトリ、`build` / `tmp`、バイナリ、UTF-8 文字境界、`memo` ディレクトリの扱いを見直したいとき。
- 既存 `INDEX.md` の不備検出、再生成、空セクション再利用、Structured Output のリトライを確認したいとき。
- `INDEX.md` メンテナンス後の自動コミット範囲や、`.cmoc` の ignore をこのテスト観点から確認したいとき。
- テスト用 git リポジトリの初期化や、`_init_repo` / `_git` の使い方を確認したいとき。

## Do not read this when

- `commons.indexing.maintain_indexes` の実装ロジックそのものを追いたいとき。
- `INDEX.md` の正本仕様や生成・更新ルールだけを確認したいとき。
- `cmoc init`、`session`、`apply`、`eval-oracles` など他サブコマンドの仕様だけを調べたいとき。
- Codex CLI 呼び出し仕様、ログ保存、エラーハンドリングなど、`INDEX.md` メンテナンス以外の共通仕様を知りたいとき。

## hash

- 49d9ea4e8e66e30cea9f0aa3fb053cef770bbd4db07f1c626b5340d7c60af380

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` の git リポジトリ共通処理を検証するテスト群の入口です。
- .cmoc の ignore 保証、tracked な `.cmoc` の untrack、cmoc ブランチ判定、`session_id` 抽出、apply worktree path 復元を扱います。
- `oracles` / 実装ファイルの列挙、変更・削除検出、`INDEX.md` / `.gitignore` / `.git/info/exclude` / `memo` の除外条件、`commit_if_changed` の index 復元と `assert_no_uncommitted_changes` の前提を確認します。
- .cmoc/sessions/<session-id>.json` の読み書き、固定スキーマ検証、active session 探索と session start commit 参照を扱います。
- ファイル末尾には、テスト用 git リポジトリを初期化する `_init_repo` と、git コマンド実行用の `_git` 補助関数があります。

## Read this when

- `tests/test_repo.py` が `commons.repo` のどの機能を検証しているか確認したいとき。
- .cmoc の ignore 保証、tracked な `.cmoc` の index 解除、cmoc ブランチ判定、`session_id` 抽出を見直したいとき。
- `oracles` / 実装ファイルの列挙、変更検出、削除検出、`INDEX.md`、`.gitignore`、`.git/info/exclude`、`memo` の扱いを確認したいとき。
- session state の読み書き、active session の探索、`commit_if_changed` や `assert_no_uncommitted_changes` の前提条件を把握したいとき。
- テスト用 git リポジトリの初期化や、`_init_repo` / `_git` 補助関数の役割を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックそのものを追いたいときは、このテスト目次ではなく実装本体を読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト目次ではなく別の案内を参照すべきです。
- `tests/test_codex.py` や `tests/test_indexing.py` など、別のテスト群の観点だけを追いたいときは、このファイルでは範囲が広すぎます。

## hash

- beed7146d8f022c1f8900f9a0371fc5a9bf9c61f1c73ded396d29333f01fc771

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、`cmoc` サブコマンド群の決定論的な制御フロー、状態遷移、エラー報告、ログ出力を横断的に検証する回帰テストの入口です。
- `cmoc init`、`session fork/join/abandon`、`apply fork/join/abandon`、`eval-oracles` の挙動に加えて、`main` の Typer ルーティングと `bin/cmoc` ランチャーの公開形も確認します。
- prompt / report の生成と検証、Structured Output の扱い、`eval-oracle` 互換 alias、補助関数の順序やテスト用 helper の妥当性もこのファイルで確認します。

## Read this when

- `run_command` の tee、共通エラーレポート、終了コード、ログ保存の挙動を追いたいとき。
- `cmoc init` の `.cmoc` ignore と commit、`session` / `apply` の fork・join・abandon の状態遷移や rollback を確認したいとき。
- `eval-oracles` のレポート生成、Structured Output 検証、削除済み oracle の扱い、評価結果集約を確認したいとき。
- `main` の Typer ルーティング、`eval-oracle` 互換 alias、`bin/cmoc` の起動条件や help 表示を確認したいとき。
- このファイル内の prompt / report 検証 helper や、テスト用補助関数の意図を把握したいとき。

## Do not read this when

- 個別サブコマンドの正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/INDEX.md` 側を読むべきです。
- `src/sub_commands` や `src/main.py` の実装本体を追いたいときは、このテスト目次ではなく `src/` 側を読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`oracles/app_specs/indexing.md` を参照すべきです。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト目次ではなく別の案内を参照すべきです。

## hash

- f3a916385801e932f18def77f2c1ec15f1c91191f01b7a51d2fafa658901cb60

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
